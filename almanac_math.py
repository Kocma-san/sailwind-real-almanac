"""Sailwind Realistic Skies — Real sky almanac helpers (match in-game ModItemAlmanac)."""
from __future__ import annotations

import math


def gha_aries_at_hour(day: int, hour: int, year_len: int = 92, siderial: bool = True) -> float:
    """GHA Aries in degrees at an integer hour (Aestrin time), matching calcAries()."""
    if siderial:
        siderial_time = float(hour) + (float(day) * 24.0 + float(hour)) / float(year_len)
    else:
        siderial_time = float(hour)
    return (siderial_time * 15.0) % 360.0


def gha_aries_min_sec_correction(minute: int, second: int, year_len: int = 92, siderial: bool = True) -> float:
    """Minute/second adjustment from almanac last pages, matching calcAriesHr()."""
    frac = float(minute) / 60.0 + float(second) / 3600.0
    if siderial:
        siderial_time = frac + frac / float(year_len)
    else:
        siderial_time = frac
    return (siderial_time * 15.0) % 360.0


def gha_aries(day: int, hour: int, minute: int = 0, second: int = 0, year_len: int = 92, siderial: bool = True) -> float:
    """Full GHA Aries = hourly table + min/sec correction (Desmos input #2)."""
    base = gha_aries_at_hour(day, hour, year_len, siderial)
    corr = gha_aries_min_sec_correction(minute, second, year_len, siderial)
    return (base + corr) % 360.0


def deg_to_disp(val: float, latlike: bool = False, tenths: bool = True) -> str:
    """Match ModItemAlmanac.degToDisp / degToDisp2 formatting."""
    neg = val < 0
    val = abs(val) % 360.0
    deg = math.floor(val)
    arcmin = (val - deg) * 60.0
    if tenths:
        arc = f"{arcmin:04.1f}"
    else:
        arc = f"{int(round(arcmin)):02d}"
    if latlike:
        hemi = "S" if neg else "N"
        return f"{hemi}{deg}°{arc}"
    sign = "-" if neg else " "
    return f"{sign}{deg}°{arc}"
