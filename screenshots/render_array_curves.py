#!/usr/bin/env python3
"""Render a 3-line "Array Production" chart from Enphase per-array history.

Pulls 5 per-array sensor histories (East / South_1 / South_2 / West_1 / West_2),
combines into 3 logical groups (East, South, West), aggregates onto a uniform
1-minute time grid, and renders in the dark style of the user's reference card.

Output: /Users/uenyioha/tmp/solar/blog-home-energy-os/screenshots/array-production-day.png
"""

import json
import os
from datetime import datetime, timezone, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

PDT = timezone(timedelta(hours=-7))

INPUTS = {
    "East":    ["/tmp/sensor.solar_array_east.json"],
    "South":   ["/tmp/sensor.solar_array_south_1.json", "/tmp/sensor.solar_array_south_2.json"],
    "West":    ["/tmp/sensor.solar_array_west_1.json", "/tmp/sensor.solar_array_west_2.json"],
}

# Colors chosen to match the user's reference card (East = blue/cyan, South = salmon, West = coral)
COLORS = {
    "East":  "#5dbcd2",  # cyan
    "South": "#e07a5f",  # salmon (warm)
    "West":  "#e8a87c",  # coral / warmer
}

OUTPUT = "/Users/uenyioha/tmp/solar/blog-home-energy-os/screenshots/array-production-day.png"


def load_series(paths):
    rows = []
    for path in paths:
        with open(path) as f:
            arr = json.load(f)
        if not arr or not arr[0]:
            continue
        for pt in arr[0]:
            state = pt.get("state")
            if state in (None, "unknown", "unavailable", ""):
                continue
            try:
                w = float(state)
            except (TypeError, ValueError):
                continue
            ts = pt.get("last_changed") or pt.get("last_updated")
            if not ts:
                continue
            t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            rows.append((t, w))
    if not rows:
        return pd.Series(dtype=float)
    rows.sort(key=lambda r: r[0])
    s = pd.Series([w for _, w in rows], index=[t for t, _ in rows], name="W")
    s.index = pd.to_datetime(s.index, utc=True)
    return s


def main():
    # 1-minute uniform grid in local (PDT) time. Day = May 11, 2026.
    start_local = datetime(2026, 5, 11, 0, 0, 0, tzinfo=PDT)
    end_local   = datetime(2026, 5, 11, 23, 59, 0, tzinfo=PDT)
    grid = pd.date_range(start=start_local.astimezone(timezone.utc),
                         end=end_local.astimezone(timezone.utc),
                         freq="1min", tz="UTC")

    aggregated = {}
    for label, paths in INPUTS.items():
        # Sum the constituent arrays' watts onto the grid
        combined = pd.Series(0.0, index=grid, dtype=float)
        for path in paths:
            s = load_series([path])
            if s.empty:
                continue
            s_grid = s.reindex(grid, method="ffill").fillna(0.0)
            combined = combined.add(s_grid, fill_value=0.0)
        aggregated[label] = combined

    # ---- Render ----
    plt.rcParams["font.family"] = "Helvetica Neue"
    fig, ax = plt.subplots(figsize=(14, 5), dpi=150)
    fig.patch.set_facecolor("#1c1c1e")
    ax.set_facecolor("#1c1c1e")

    # Draw filled areas + lines for each group
    for label in ("East", "South", "West"):
        s = aggregated[label]
        # Convert UTC index to local PDT for display
        x_local = s.index.tz_convert(PDT)
        ax.fill_between(x_local, s.values / 1000.0, alpha=0.18, color=COLORS[label], linewidth=0)
        ax.plot(x_local, s.values / 1000.0, color=COLORS[label], linewidth=2.0, label=label, alpha=0.95)

    # Axes styling
    ax.set_xlim(datetime(2026, 5, 11, 4, 0, 0, tzinfo=PDT),
                datetime(2026, 5, 11, 21, 0, 0, tzinfo=PDT))
    ax.set_ylim(0, 8.5)

    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[6, 9, 12, 15, 18, 21]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%-I %p", tz=PDT))
    ax.set_ylabel("kW", color="#bbbbbb", fontsize=11, rotation=0, labelpad=18, va="center")
    ax.tick_params(colors="#bbbbbb", which="both", labelsize=11)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(True, axis="y", linestyle=":", linewidth=0.6, color="#444444", alpha=0.6)
    ax.grid(False, axis="x")

    # Title
    ax.text(0.012, 1.04, "Array Production — May 11, 2026", transform=ax.transAxes,
            color="#dddddd", fontsize=14, fontweight="normal", va="bottom")

    # Legend at bottom center
    legend = ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=3,
                       frameon=False, fontsize=12, labelcolor="#cccccc")
    for handle in legend.legend_handles:
        handle.set_linewidth(3)

    plt.subplots_adjust(left=0.05, right=0.985, top=0.92, bottom=0.18)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    fig.savefig(OUTPUT, facecolor=fig.get_facecolor(), dpi=150)
    print(f"wrote {OUTPUT}")

    # also print a summary so we can sanity-check
    print()
    for label in ("East", "South", "West"):
        s = aggregated[label]
        peak = s.max()
        peak_t = s.idxmax().tz_convert(PDT)
        total_kwh = s.sum() / 60.0 / 1000.0  # minutes -> hours -> kWh
        print(f"  {label}: peak {peak:>5.0f} W at {peak_t.strftime('%-I:%M %p')}, day total {total_kwh:.1f} kWh")


if __name__ == "__main__":
    main()
