# WMTMW In-Wall Speaker Project

3× identical WMTMW sealed in-wall speakers (L/C/R) for a dedicated basement home theater.
135" projector screen, ~9 ft listening distance, 125W+ per channel amplification.

## Design Summary

- **Type:** WMTMW 3-way, sealed, passive crossover
- **Mounting:** In-wall, flush with drywall (2×6 studs, 16" OC)
- **Crossovers:** ~400 Hz / ~2.5 kHz (LR4 acoustic targets)
- **Impedance:** 4–6 Ω nominal
- **Sensitivity:** ~87–88 dB (2.83V/1m, half-space)
- **Enclosure:** 16" W × 48" H × 5.25" D (stud cavity depth)

## Drivers (per speaker)

| Role | Driver | Qty |
|------|--------|-----|
| Woofer | SB Acoustics SB17MFC35-8 (6.5") | 2 |
| Midrange | SB Acoustics SB13PFCR25-08 (5") | 2 |
| Tweeter | Scan-Speak H2606/9200 (26mm horn dome) | 1 |

## Repository Contents

| File / Folder | Purpose |
|---------------|---------|
| [`WMTMW_PlanOfRecord.md`](WMTMW_PlanOfRecord.md) | **Primary spec** — all finalized dimensions, drivers, assembly, crossover targets, status |
| [`WMTMW_InWall_Speaker_Design.md`](WMTMW_InWall_Speaker_Design.md) | Full engineering detail, crossover math, risk log |
| [`WMTMW_Enclosure_Plans.html`](WMTMW_Enclosure_Plans.html) | Printable shop drawings — cut list, baffle layout, chamber details, assembly sequence |
| [`WMTMW_Development_History.md`](WMTMW_Development_History.md) | Session-by-session decision log — historical reference only |
| [`FreeAirMeasurements/`](FreeAirMeasurements/) | DATS V3 free-air impedance files for all prototype drivers |
| [`InBoxMeasurements/`](InBoxMeasurements/) | *(next phase)* In-box impedance (.zma) + frequency response (.frd) |
| [`CrossoverDesign/`](CrossoverDesign/) | *(next phase)* VituixCAD project files, schematic notes, component values |

## Build Status

**Prototype enclosure is built and installed in wall.** See [`WMTMW_PlanOfRecord.md §17`](WMTMW_PlanOfRecord.md#17-status) for the full status and next steps.

Upcoming: in-box driver measurements → VituixCAD crossover design → prototype crossover → iteration → final 3-speaker build.

## Sealed Alignment (measured, prototype woofers)

| | Woofer 1 | Woofer 2 | Average |
|--|----------|----------|---------|
| Qtc | 0.71 | 0.67 | **0.69** |
| Fc | 56 Hz | 55 Hz | 56 Hz |
| F3 | ~56 Hz | ~58 Hz | **~57 Hz** |

Essentially ideal Butterworth. Subwoofer(s) handle below 50–70 Hz.
