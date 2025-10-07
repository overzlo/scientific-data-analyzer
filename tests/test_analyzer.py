import math
from pathlib import Path

import pandas as pd

from src.analyzer import load_data, compute_stats, plot_series


def test_compute_stats_basic(tmp_path):
    # Prepare a small CSV
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("""date,temperature
2025-01-01,10
2025-01-02,12
2025-01-03,14
""")

    df = load_data(csv_path)
    stats = compute_stats(df, "temperature")

    assert set(stats.keys()) == {"mean", "min", "max", "std"}
    assert stats["min"] == 10
    assert stats["max"] == 14
    assert math.isclose(stats["mean"], 12.0, rel_tol=1e-9)

    # sample std of [10,12,14] is sqrt(((4+0+4)/2)) = 2.0
    assert math.isclose(stats["std"], 2.0, rel_tol=1e-9)


def test_plot_series_creates_file(tmp_path):
    df = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]),
        "temperature": [10, 12, 14]
    })
    out_path = tmp_path / "plot.png"
    saved = plot_series(df, "temperature", out_path, title="Temperature")
    assert saved == out_path
    assert out_path.exists() and out_path.stat().st_size > 0


def test_load_data_file_not_found(tmp_path):
    missing = tmp_path / "missing.csv"
    try:
        load_data(missing)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
