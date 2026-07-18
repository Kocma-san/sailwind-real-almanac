"""Sanity checks for Sailwind Real almanac math vs ModItemAlmanac formulas."""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from almanac_math import (  # noqa: E402
    deg_to_disp,
    gha_aries,
    gha_aries_at_hour,
    gha_aries_min_sec_correction,
)


def almost(a: float, b: float, eps: float = 1e-4) -> None:
    assert abs(a - b) < eps, f"{a} != {b}"


def test_hour_table_day0() -> None:
    # day 0 hour 0 -> 0°
    almost(gha_aries_at_hour(0, 0, 92, True), 0.0)
    # day 0 hour 1 -> 1h + 1/92 hour of sidereal advance
    expected = (1.0 + 1.0 / 92.0) * 15.0
    almost(gha_aries_at_hour(0, 1, 92, True), expected % 360.0)


def test_min_sec_correction() -> None:
    # 30 min exactly: 0.5h + 0.5/92, *15
    expected = (0.5 + 0.5 / 92.0) * 15.0
    almost(gha_aries_min_sec_correction(30, 0, 92, True), expected % 360.0)


def test_full_aries_add() -> None:
    base = gha_aries_at_hour(10, 20, 92, True)
    corr = gha_aries_min_sec_correction(15, 30, 92, True)
    total = gha_aries(10, 20, 15, 30, 92, True)
    almost(total, (base + corr) % 360.0)


def test_no_siderial() -> None:
    almost(gha_aries_at_hour(5, 3, 92, False), 45.0)
    almost(gha_aries_min_sec_correction(30, 0, 92, False), 7.5)


def test_disp() -> None:
    assert deg_to_disp(12.5, False, True).strip().startswith("12°")
    assert deg_to_disp(-10.25, True, True).startswith("S")


def test_nav_stars_file() -> None:
    import json

    path = ROOT / "data" / "nav_stars.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["count"] >= 40
    names = {s["name"] for s in data["stars"]}
    assert "Sirius" in names
    assert "Polaris" in names
    assert "Sol" not in names
    for s in data["stars"]:
        sha = (360.0 - s["ra_hours"] * 15.0) % 360.0
        almost(s["sha"], sha)


if __name__ == "__main__":
    test_hour_table_day0()
    test_min_sec_correction()
    test_full_aries_add()
    test_no_siderial()
    test_disp()
    test_nav_stars_file()
    print("OK — all almanac tests passed")
