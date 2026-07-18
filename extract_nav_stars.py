"""Extract navigational stars from HYG for Sailwind Real-sky almanac."""
from __future__ import annotations

import csv
import gzip
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
HYG_GZ = DATA / "hyg_v44.csv.gz"
OUT_JSON = DATA / "nav_stars.json"
OUT_JS = Path(__file__).resolve().parent / "nav_stars.js"

# Official-ish nautical almanac navigational stars (common set).
NAV_NAMES = {
    "Acamar", "Achernar", "Acrux", "Adhara", "Aldebaran", "Alioth", "Alkaid",
    "Alnahi", "Alphard", "Alphecca", "Alpheratz", "Altair", "Ankaa", "Antares",
    "Arcturus", "Atria", "Avior", "Bellatrix", "Betelgeuse", "Canopus", "Capella",
    "Deneb", "Denebola", "Diphda", "Dubhe", "Eligon", "Enif", "Fomalhaut",
    "Gacrux", "Gienah", "Hadar", "Hamal", "Kaus Australis", "Kochab", "Markab",
    "Menkar", "Menkent", "Miaplacidus", "Mirfak", "Nunki", "Peacock", "Polaris",
    "Pollux", "Procyon", "Rasalhague", "Regulus", "Rigel", "Rigil Kentaurus",
    "Sabik", "Schedar", "Shaula", "Sirius", "Spica", "Suhail", "Vega", "Zubenelgenubi",
}

# Alternate names used in some HYG versions
ALIASES = {
    "Alpha Crucis": "Acrux",
    "Alpha Centauri": "Rigil Kentaurus",
    "Toliman": "Rigil Kentaurus",
    "Rigel Kentaurus": "Rigil Kentaurus",
    "Al Na'ir": "Alnahi",
    "Alnair": "Alnahi",
    "Elnath": "Eligon",
    "Alnath": "Eligon",
}


def sha_from_ra_hours(ra_hours: float) -> float:
    """Sidereal Hour Angle in degrees from RA in hours."""
    ra_deg = ra_hours * 15.0
    return (360.0 - ra_deg) % 360.0


def deg_to_dms(val: float, latlike: bool = False) -> str:
    neg = val < 0
    val = abs(val) % 360.0
    deg = math.floor(val)
    arcmin = (val - deg) * 60.0
    if latlike:
        hemi = "S" if neg else "N"
        return f"{hemi}{deg}°{arcmin:04.1f}"
    sign = "-" if neg else " "
    return f"{sign}{deg}°{arcmin:04.1f}"


def main() -> None:
    if not HYG_GZ.exists():
        raise SystemExit(f"Missing {HYG_GZ}")

    with gzip.open(HYG_GZ, "rt", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    print(f"HYG stars loaded: {len(rows)}")
    print(f"Columns: {list(rows[0].keys())[:15]}...")

    by_proper: dict[str, dict] = {}
    for r in rows:
        proper = (r.get("proper") or "").strip()
        if not proper:
            continue
        proper = ALIASES.get(proper, proper)
        mag = r.get("mag")
        if mag in ("", None):
            continue
        try:
            mag_f = float(mag)
            ra = float(r["ra"])
            dec = float(r["dec"])
        except (KeyError, ValueError):
            continue
        prev = by_proper.get(proper)
        if prev is None or mag_f < prev["mag"]:
            by_proper[proper] = {
                "name": proper,
                "mag": mag_f,
                "ra_hours": ra,
                "dec": dec,
                "sha": sha_from_ra_hours(ra),
                "hip": r.get("hip") or None,
                "hr": r.get("hr") or None,
                "con": r.get("con") or None,
                "spect": r.get("spect") or None,
            }

    stars = []
    missing = []
    for name in sorted(NAV_NAMES):
        if name in by_proper:
            stars.append(by_proper[name])
        else:
            missing.append(name)

    # Fill remaining bright named stars up to ~60 for visibility in Real sky
    extras = [
        s for n, s in by_proper.items()
        if n not in NAV_NAMES and n != "Sol" and s["mag"] <= 2.0
    ]
    extras.sort(key=lambda s: s["mag"])
    for s in extras:
        if len(stars) >= 60:
            break
        stars.append(s)

    stars.sort(key=lambda s: s["mag"])

    for s in stars:
        s["sha_disp"] = deg_to_dms(s["sha"])
        s["dec_disp"] = deg_to_dms(s["dec"], latlike=True)

    payload = {
        "source": "HYG v4.4 (CC BY-SA 4.0) — https://www.astronexus.com/projects/hyg",
        "note": "SHA = (360 - RA_deg) mod 360. Tuned for Sailwind Realistic Skies 'Real' skybox + Desmos LOP.",
        "count": len(stars),
        "stars": stars,
        "missing_nav_names": missing,
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUT_JS.write_text(
        "window.NAV_STARS = " + json.dumps(payload, indent=2) + ";\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(stars)} stars -> {OUT_JSON.name}, {OUT_JS.name}")
    if missing:
        print("Missing nav names:", ", ".join(missing))
    print("Top 10:")
    for s in stars[:10]:
        print(f"  {s['name']:16} mag={s['mag']:5.2f} SHA={s['sha']:8.3f} Dec={s['dec']:+8.3f}")


if __name__ == "__main__":
    main()
