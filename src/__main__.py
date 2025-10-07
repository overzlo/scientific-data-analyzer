from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .analyzer import load_data, compute_stats, plot_series, plot_histogram


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scientific Data Analyzer: load CSV, compute stats, and create plots"
    )
    parser.add_argument("csv", type=str, help="Path to CSV file")
    parser.add_argument("column", type=str, help="Numeric column name to analyze/plot")

    parser.add_argument(
        "--output", type=str, default="plot.png", help="Output path for line plot (default: plot.png)"
    )
    parser.add_argument(
        "--show", action="store_true", help="Show plots interactively in addition to saving"
    )
    parser.add_argument(
        "--ma-window", type=int, default=None, help="Moving average window to overlay on line plot"
    )
    parser.add_argument(
        "--title", type=str, default=None, help="Title for the line plot"
    )

    parser.add_argument(
        "--hist", action="store_true", help="Also build a histogram of the selected column"
    )
    parser.add_argument(
        "--hist-bins", type=int, default=20, help="Number of bins for histogram (default: 20)"
    )
    parser.add_argument(
        "--hist-output", type=str, default="hist.png", help="Output path for histogram (default: hist.png)"
    )

    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 2

    # Load data
    df = load_data(csv_path)

    # Compute and print stats
    try:
        stats = compute_stats(df, args.column)
    except Exception as e:
        print(f"Failed to compute stats for column '{args.column}': {e}")
        return 3

    print("Statistics:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Plot series
    out_path = Path(args.output)
    try:
        saved = plot_series(
            df,
            args.column,
            output_path=out_path,
            title=args.title or f"Series: {args.column}",
            show=bool(args.show),
            ma_window=args.ma_window,
        )
        print(f"Line plot saved to: {saved}")
    except Exception as e:
        print(f"Failed to create line plot: {e}")
        return 4

    # Plot histogram if requested
    if args.hist:
        try:
            hist_saved = plot_histogram(
                df,
                args.column,
                bins=int(args.hist_bins),
                output_path=Path(args.hist_output),
                show=bool(args.show),
            )
            print(f"Histogram saved to: {hist_saved}")
        except Exception as e:
            print(f"Failed to create histogram: {e}")
            return 5

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
