"""scientific-data-analyzer package.

Provides simple utilities to load CSV data, compute basic statistics, and plot a time series.
"""
from .analyzer import load_data, compute_stats, plot_series, plot_histogram

__all__ = ["load_data", "compute_stats", "plot_series", "plot_histogram"]
