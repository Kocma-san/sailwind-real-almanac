# License / copyright — Real Almanac

## Star data (required)

The bundled catalog (`nav_stars.js`, `data/nav_stars.json`) is a **derived excerpt** of:

**HYG star database v4.4** — David Nash / Astronomy Nexus  
https://www.astronexus.com/projects/hyg  
https://codeberg.org/astronexus/hyg  

License: [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

Sharing requirements:
1. **Attribution** — credit HYG / Astronomy Nexus (already in `nav_stars.js` → `source`).
2. **ShareAlike** — the data (and any adaptation of HYG) must remain under **CC BY-SA 4.0** (or compatible).
3. Do not redistribute the raw `hyg_v44.csv.gz` file without the same license (it is gitignored anyway).

Positions (RA/Dec), magnitudes, and star names are **astronomical facts** compiled in HYG; this is not proprietary official Nautical Almanac code.

## Tool code (HTML / JS / Python)

Written for this project (Realistic Skies–style Aries math, Desmos helpers).  
You may publish the code under a license of your choice; **if the repo includes `nav_stars.js`**, the simplest safe option is to license **the whole repo as CC BY-SA 4.0** to stay aligned with HYG.

## Not redistributed here

| Source | Use |
|--------|-----|
| Realistic Skies (Sailwind mod) | Aries formulas **reimplemented** from mod behavior — no assets / DLL / textures copied |
| Desmos LOP | Link to the external calculator only |
| Stellarium | Not included |

Recommended credit (compatibility / inspiration): **Realistic Skies** mod ([KingCam77/Realistic-Skies](https://github.com/KingCam77/Realistic-Skies)) + Sailwind community Desmos LOP.

## Summary

| OK to share? | Condition |
|--------------|-----------|
| Yes | HYG attribution + **CC BY-SA 4.0** on the data (ideally the whole repo) |
| Avoid | “All rights reserved” on `nav_stars.js` without ShareAlike |
| Not needed | Separate permission for Desmos / Stellarium (links only) |
