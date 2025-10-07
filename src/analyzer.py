from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Union, Tuple

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
    show: bool = False,
    ma_window: Optional[int] = None,
    style: Optional[str] = "ggplot",
) -> Path:
    """
    Plot a line chart of the selected column and save it as an image.

    :param df: DataFrame with data.
    :param column: Column to plot (name, index, or Series).
    :param output_path: File path to save the plot (e.g., 'plot.png'). If None, saves to 'plot.png' in CWD.
    :param title: Optional plot title.
    :param show: If True, also display the plot window (interactive) in addition to saving it.
    :param ma_window: If set (>=2), overlay a moving average with the given window size.
    :param style: Matplotlib style name to use (e.g., 'ggplot'); set None to use default.
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

    if style:
        try:
            plt.style.use(style)
        except Exception:
            pass

    fig, ax = plt.subplots(figsize=(8, 4.5))
    if x is not None:
        ax.plot(x, s.values, marker="o", linestyle="-", label=str(column))
        ax.set_xlabel("Time")
    else:
        ax.plot(s.values, marker="o", linestyle="-", label=str(column))
        ax.set_xlabel("Index")
    ax.set_ylabel(str(column))
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.set_title(title or f"Series: {column}")

    # Overlay moving average if requested
    if ma_window is not None and isinstance(ma_window, int) and ma_window >= 2:
        ma = s.rolling(window=ma_window, min_periods=1, center=False).mean()
        if x is not None:
            ax.plot(x, ma.values, color="C3", linewidth=2.0, label=f"MA({ma_window})")
        else:
            ax.plot(ma.values, color="C3", linewidth=2.0, label=f"MA({ma_window})")

    ax.legend(loc="best")
    fig.tight_layout()

    out = Path(output_path) if output_path is not None else Path("plot.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close(fig)
    return out



def plot_histogram(
    df: pd.DataFrame,
    column: Union[str, int, pd.Series],
    bins: int = 20,
    output_path: Optional[Union[str, Path]] = None,
    title: Optional[str] = None,
    show: bool = False,
    style: Optional[str] = "ggplot",
) -> Path:
    """
    Plot a histogram of the selected column and save it as an image.

    :param df: DataFrame with data.
    :param column: Column to plot (name, index, or Series).
    :param bins: Number of histogram bins.
    :param output_path: File path to save the plot (e.g., 'hist.png'). If None, saves to 'hist.png' in CWD.
    :param title: Optional plot title.
    :param show: If True, also display the plot window (interactive) in addition to saving it.
    :param style: Matplotlib style name to use; set None to use default.
    :return: Path to the saved image file.
    """
    s = _series_from(df, column).dropna()

    if style:
        try:
            plt.style.use(style)
        except Exception:
            pass

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(s.values, bins=bins, color="C0", alpha=0.8, edgecolor="black")
    ax.set_xlabel(str(column))
    ax.set_ylabel("Count")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.set_title(title or f"Histogram: {column}")
    fig.tight_layout()

    out = Path(output_path) if output_path is not None else Path("hist.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close(fig)
    return out
