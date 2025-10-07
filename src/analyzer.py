from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


Number = Union[int, float, np.number]


@dataclass(frozen=True)
class Stats:
    mean: float
    min: float
    max: float
    std: float

    def to_dict(self) -> Dict[str, float]:
        return {"mean": self.mean, "min": self.min, "max": self.max, "std": self.std}


def load_data(csv_path: Union[str, Path], parse_dates: Optional[Union[str, list[str]]] = None) -> pd.DataFrame:
    """
    Load CSV data using pandas.read_csv.

    :param csv_path: Path to a CSV file.
    :param parse_dates: Column name or list of columns to parse as dates.
    :return: pandas DataFrame with loaded data.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    df = pd.read_csv(csv_path)
    if parse_dates is not None:
        df = df.copy()
        df[parse_dates] = pd.to_datetime(df[parse_dates])
    return df


def _series_from(df: pd.DataFrame, column: Union[str, int, pd.Series]) -> pd.Series:
    if isinstance(column, pd.Series):
        s = column
    elif isinstance(column, (str, int)):
        s = df[column]
    else:
        raise TypeError("column must be a Series, column name, or index")
    # Convert to numeric if possible; coerce errors to NaN and drop them for stats
    s = pd.to_numeric(s, errors="coerce")
    return s


def compute_stats(df: pd.DataFrame, column: Union[str, int, pd.Series]) -> Dict[str, float]:
    """
    Compute basic statistics: mean, min, max, sample std (ddof=1).
    Non-numeric values are coerced to NaN and ignored.
    :returns: dict with keys mean, min, max, std
    """
    s = _series_from(df, column).dropna()
    if s.empty:
        raise ValueError("No numeric data available to compute statistics")
    mean = float(np.mean(s))
    min_v = float(np.min(s))
    max_v = float(np.max(s))
    # Sample standard deviation (unbiased, ddof=1); if only one value, std=0.0
    std = float(np.std(s, ddof=1)) if len(s) > 1 else 0.0
    return Stats(mean=mean, min=min_v, max=max_v, std=std).to_dict()


def plot_series(
    df: pd.DataFrame,
    column: Union[str, int, pd.Series],
    output_path: Optional[Union[str, Path]] = None,
    title: Optional[str] = None,
) -> Path:
    """
    Plot a line chart of the selected column and save it as an image.

    :param df: DataFrame with data.
    :param column: Column to plot (name, index, or Series).
    :param output_path: File path to save the plot (e.g., 'plot.png'). If None, saves to 'plot.png' in CWD.
    :param title: Optional plot title.
    :return: Path to the saved image file.
    """
    s = _series_from(df, column)

    # Choose an index for x-axis if DataFrame has a datetime-like column named 'date' or 'time'
    x = None
    for candidate in ("date", "time", "timestamp", "Date", "Time", "Timestamp"):
        if candidate in df.columns:
            try:
                x_candidate = pd.to_datetime(df[candidate], errors="coerce")
                if x_candidate.notna().any():
                    x = x_candidate
                    break
            except Exception:
                pass

    fig, ax = plt.subplots(figsize=(8, 4.5))
    if x is not None:
        ax.plot(x, s.values, marker="o", linestyle="-")
        ax.set_xlabel("Time")
    else:
        ax.plot(s.values, marker="o", linestyle="-")
        ax.set_xlabel("Index")
    ax.set_ylabel(str(column))
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.set_title(title or f"Series: {column}")
    fig.tight_layout()

    out = Path(output_path) if output_path is not None else Path("plot.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    return out
