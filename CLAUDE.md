# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hardware/acoustical engineering project — not a software project. Goal: design and build 3 identical WMTMW in-wall speakers (L/C/R) for a dedicated basement home theater. No build/test/lint commands apply.

**Design is complete. Physical build is underway.**

## Source of Truth

**`WMTMW_PlanOfRecord.md` is the authoritative spec.** Read it for all current dimensions, driver specs, assembly details, and next steps. It is kept up to date as decisions are made.

Do not rely on `WMTMW_Development_History.md` for current values — it is a historical session log only.

## Documentation Map

| File / Folder | Purpose |
|---------------|---------|
| `WMTMW_PlanOfRecord.md` | **Primary spec** — all finalized dimensions, drivers, assembly, crossover targets, status |
| `WMTMW_InWall_Speaker_Design.md` | Full engineering detail, crossover math, risk log |
| `WMTMW_Enclosure_3D.html` | Interactive 3D shop drawings (printed for build reference) |
| `WMTMW_Development_History.md` | Session-by-session decision log — historical only, do not read in full |
| `FreeAirMeasurements/` | DATS V3 free-air impedance files (.txt, .tzz, .zma) for all prototype drivers |
| `InBoxMeasurements/` | *(next phase)* In-box impedance (.zma) + frequency response (.frd) from REW/UMIK-1 |
| `CrossoverDesign/` | *(next phase)* VituixCAD project files, schematic notes, prototype BOM, final component values |

## Build Status (as of March 2026)

Current task: **Build prototype enclosure**

Next measurement session:
1. Install prototype in wall
2. Measure each driver in-box with DATS V3 → save `.zma` to `InBoxMeasurements/`
3. Measure frequency response with UMIK-1 + REW → save `.frd` to `InBoxMeasurements/`
4. Import into VituixCAD on Windows PC → design crossover → save project to `CrossoverDesign/`
