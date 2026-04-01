# WMTMW In-Wall Speaker — Plan of Record

> **3× identical WMTMW sealed in-wall speakers for L/C/R**
> **Last updated:** March 29, 2026
> **Companion files:** `WMTMW_InWall_Speaker_Design.md` · `WMTMW_Enclosure_Plans.html`

---

## 1. Project Summary

Dedicated basement home theater, ~9 ft listening distance, 135" projector screen.
L/R speakers at ~30° horizontal off-axis. Subwoofer(s) handle below 50–70 Hz.
Timbre-matched to Mechano23 surrounds (same mid driver family + tweeter).
Amplification: 125W+ per channel. Budget: <$600/speaker (not including MDF).

---

## 2. Configuration

```
Type:           WMTMW 3-way, sealed, passive crossover
Mounting:       In-wall, flush with drywall (2×6 studs, 16" OC)
Crossovers:     ~400 Hz / ~2.5 kHz (LR4 acoustic targets)
Impedance:      4–6 Ω nominal (8 Ω drivers wired parallel per section)
Sensitivity:    ~87–88 dB (2.83V/1m, half-space)
```

---

## 3. Drivers

| Role | Driver | Qty/Spkr | Impedance | Price | Source |
|------|--------|----------|-----------|-------|--------|
| Woofer | SB Acoustics SB17MFC35-8 (6.5" PP) | 2 | 8 Ω | $75.90 | Madisound |
| Midrange | SB Acoustics SB13PFCR25-08 (5" paper) | 2 | 8 Ω | $36.80 | Madisound |
| Tweeter | Scan-Speak H2606/9200 (26mm horn dome) | 1 | 6 Ω | $47.80 | Madisound |

**Driver cost per speaker: $273.20 · All 3 speakers: $819.60**

### Measured T/S Parameters (DATS V3, post-break-in)

**Woofers** (18.26g added mass, 122.4mm piston dia):

| Param | Published | Woofer 1 | Woofer 2 |
|-------|-----------|----------|----------|
| Re | 5.7 Ω | 5.726 | 5.806 |
| Fs | 33 Hz | 36.67 | 35.16 |
| Qts | 0.37 | 0.460 | 0.423 |
| Vas | 39 L | 22.74 L | 24.64 L |
| Mms | 11.8 g | 16.12 | 16.18 |
| BL | 5.9 Tm | 6.483 | 6.721 |

Woofer matching: Fs gap 1.5 Hz (4.3%), Qts gap 0.037 (8.8%) — acceptable.
Mms ~16g is genuine (validated by mid measurement technique agreement).

**Mids** (105.2mm piston dia):

| Param | Published | Mid 3 | Mid 4 |
|-------|-----------|-------|-------|
| Re | 5.6 Ω | 5.784 | 5.442 |
| Fs | 45 Hz | 52.69 | 51.68 |
| Qts | 0.33 | 0.395 | 0.361 |
| Mms | 10.0 g | 10.42 | 10.33 |

Mid matching: excellent (Fs gap 1.9%, Mms 0.9%).

---

## 4. Enclosure Dimensions

```
BOX EXTERNAL:     14.25" W  ×  5.50" D  ×  48.00" H
FRONT BAFFLE:     16.00" W  ×  48.00" H ×  0.75" thick (rabbeted to 1/2" at L/R edges)
BOX INTERNAL:     13.25" W  ×  4.25" D  ×  46.50" H
DRYWALL CUTOUT:   16.00" W  ×  48.00" H
STUD OVERLAP:     0.875" per side (baffle flange, L/R only — no T/B overhang)
BOX CLEARANCE:    0.125" per side in stud cavity
```

### Panel Thicknesses

| Panel | Material | Thickness |
|-------|----------|-----------|
| Front baffle | MDF | 3/4" (rabbeted to 1/2" at perimeter) |
| Top / Bottom | MDF | 3/4" |
| Side panels | MDF | 1/2" |
| Back panel | MDF | 1/2" |
| Dividers (×2) | MDF | 1/2" |

### Depth Stack

```
Baffle 0.75" + Internal 4.25" + Back 0.50" = 5.50" (fills 2×6 cavity)
Box height matches baffle height (48.00") — no top/bottom overhang.
```

---

## 5. Baffle Details

**Side rabbet (back face):** 1/4" deep × 1" wide on left and right edges only.
Reduces side flanges to 1/2" = drywall thickness = flush wall surface.
No rabbet on top/bottom — box is flush with baffle at those edges.

**Driver recesses (front face):** ~3mm (1/8") deep, diameter matches frame OD.
Drivers sit flush with baffle. Remaining material behind recess: 16mm — solid for T-nuts.

**Mounting to studs:** #8 × 2" pan-head coarse-thread wood screws.
Pre-drill 7/64" through flange into stud. ~9–10 screws per side stud (6" spacing),
2–3 into bottom cross stud. ~20–23 screws total per speaker. Snug only — do not strip MDF.

---

## 6. Driver Layout (from baffle bottom edge)

| Driver | Center | Frame Extent | Cutout | Recess (frame OD) |
|--------|--------|-------------|--------|-------------------|
| Lower woofer | 12.00" | 7.88"–14.62" | ∅149mm / 5.87" | ∅171mm / 6.73" |
| Lower mid | 18.75" | 15.30"–20.70" | ∅116mm / 4.57" | ∅137mm / 5.39" |
| Tweeter | 24.00" | 21.95"–26.05" | ∅72mm / 2.83" | ∅104mm / 4.09" |
| Upper mid | 29.25" | 25.80"–31.20" | ∅116mm / 4.57" | ∅137mm / 5.39" |
| Upper woofer | 36.00" | 31.88"–38.62" | ∅149mm / 5.87" | ∅171mm / 6.73" |

All drivers centered horizontally at 8.00" from baffle edges.
Tweeter faceplate is round (∅104mm). All recesses are circular.
Driver stack C-to-C (bottom woofer to top woofer): 24.00".
Mid-to-mid C-to-C: 10.50" (267mm).

---

## 7. Internal Chambers

Two 1/2" MDF horizontal dividers create three sealed chambers.

| Chamber | Height | Volume | Damping |
|---------|--------|--------|---------|
| Lower woofer | 14.71" | 13.6 L | Polyfill ~50% |
| Mid / Tweeter (shared) | 16.08" | 14.8 L | 1" acoustic foam on walls |
| Upper woofer | 14.71" | 13.6 L | Polyfill ~50% |

**Divider positions** (from inside bottom):
- Divider 1: 14.96" (center) — lower woofer / mid-tweeter boundary
- Divider 2: 31.54" (center) — mid-tweeter / upper woofer boundary

Height check: 14.71 + 0.50 + 16.08 + 0.50 + 14.71 = 46.50" ✓

### Sealed Woofer Alignment (measured, with polyfill ~15.7 L effective)

| | Woofer 1 | Woofer 2 | Average |
|---|----------|----------|---------|
| Qtc | 0.72 | 0.68 | **0.70** |
| Fc | 57 Hz | 56 Hz | 57 Hz |
| F3 | ~54 Hz | ~58 Hz | **~56 Hz** |

Essentially ideal Butterworth (0.707). **Enclosure confirmed.**

---

## 8. Internal Bracing

| Element | Qty | Size | Placement |
|---------|-----|------|-----------|
| Back panel battens | 2 | 3/4" × 3/4" × 13.25" | Flat on back panel, one per woofer chamber, centered vertically |
| Front-to-back ties | 6 | 3/4" × 3/4" × 4.25" | 2 per chamber, flanking driver cutouts, bridging baffle to back |

---

## 9. Wiring

```
Woofer pair:   8 Ω parallel = 4 Ω
Mid pair:      8 Ω parallel = 4 Ω
Tweeter:       6 Ω (single)
System:        4–6 Ω nominal
```

**Prototype:** Each driver on its own 16 AWG cable, routed out the top to an external crossover board.
**Final build:** Internal crossover on back panel, binding post cups on back.

---

## 10. Crossover Architecture (Preliminary — values TBD after measurement)

```
Woofer:   LPF ~400 Hz (LR4) + Zobel + impedance EQ
Mid:      BPF ~400 Hz – 2.5 kHz (LR4 slopes) + notch filter if needed
Tweeter:  HPF ~2.5 kHz (LR4) + L-pad (~10–13 dB) + Zobel + impedance EQ
```

- No baffle step compensation needed (in-wall = infinite baffle)
- Tweeter 95 dB sensitivity padded down to ~85 dB to match mids
- Time alignment (~28mm mid→tweeter offset, ~74° at 2.5 kHz): handled by crossover network
- Final values from VituixCAD using real in-box measurements

---

## 11. Assembly Method

**Adhesive:** PL Premium polyurethane (bonds MDF end grain, gap-filling, 24h cure).
**Fasteners:** 18ga brad nails (1.5" panels, 1" dividers) for alignment during cure. No screws into MDF edges.
**Driver mounting:** M4 screws into T-nuts pressed into baffle back. Foam gasket tape under all flanges.

### Assembly Sequence (abbreviated)

1. Cut all panels; route baffle (L/R side rabbet + driver holes + recesses)
2. Press T-nuts into baffle back; drill mounting bolt holes
3. Lay back panel flat → glue bottom panel → glue side panels → glue battens
4. Thread woofer cables through divider holes **before** gluing dividers
5. Glue dividers at marked positions
6. Glue top panel; let cure 24h; seal all joints (PL Premium fillet + silicone bead)
7. Install front-to-back ties; stuff woofer chambers (polyfill); line mid chamber (foam)
8. Route all driver cables; verify everything before closing
9. Glue baffle onto front edges; brad nail perimeter + divider edges; cure 24h
10. Mount drivers with M4 screws + foam gasket tape

*Full step-by-step: see `WMTMW_InWall_Speaker_Design.md` Phases 1–6.*

---

## 12. Wall Installation

1. Cut drywall opening: 16.0" × 48.0"
2. Install horizontal cross stud at bottom of opening (weight support)
3. Slide box into cavity, rest on cross stud
4. Pre-drill 7/64" through baffle flanges into studs
5. Drive #8 × 2" pan-head coarse wood screws (~20–23 per speaker, 6" spacing)
6. Route cables over top to unfinished room side → connect to external crossover
7. Position tweeter at seated ear height (~36–40" from floor)

---

## 13. Measurement & Crossover Design Plan

### Tools
- **DATS V3:** impedance sweeps (.zma export)
- **UMIK-1 + REW:** frequency response (.frd export), nearfield + farfield
- **VituixCAD:** crossover simulation and optimization (Windows)

### Workflow
1. ✅ Measure free-air T/S for all prototype drivers (done — see Section 3)
2. Build prototype enclosure and install in wall
3. Measure each driver individually in-box (impedance + frequency response)
4. Import .zma and .frd into VituixCAD
5. Design crossover — optimize for flat on-axis + smooth power response
6. Build crossover on prototype board, measure system response
7. Iterate 2–4 rounds until satisfied
8. Finalize component values, order quality parts, build final crossovers

---

## 14. MDF & Materials Summary (per speaker)

| Material | Pieces | Notes |
|----------|--------|-------|
| 3/4" MDF | Baffle + top + bottom + 8 brace pieces | ~12.5 sq ft |
| 1/2" MDF | Back + 2 sides + 2 dividers | ~11.0 sq ft |

**For all 3 speakers:** ~1.5 sheets 3/4" + ~1.5 sheets 1/2" (4×8). Order 2+2 for waste/test cuts.

---

## 15. Budget

| Category | Cost (all 3 speakers) |
|----------|----------------------|
| Drivers (15 total) | $819.60 |
| Hardware (screws, T-nuts, gasket tape, polyfill, foam, adhesive, brad nails, etc.) | ~$145 |
| Crossover components (est.) | $255 – $450 |
| **Grand Total** | **$1,220 – $1,415** |
| Budget (3 × $600) | $1,800 |
| **Under budget by** | **$385 – $580** |

*MDF not included in budget (~$80–120 for all sheets).*

---

## 16. Key Design Decisions (rationale summary)

| Decision | Choice | Why |
|----------|--------|-----|
| WMTMW config | Yes | Symmetry for L/C/R, dual mids for power handling, industry standard |
| Sealed (no port) | Yes | Sub handles LF; sealed = simpler, better transients, fits depth |
| 8 Ω parallel | Yes | Standard 4 Ω load per section, proven in commercial designs |
| 3/4" baffle | Yes | Strong driver mounting, T-nut engagement, rabbeted to 1/2" at L/R edges |
| No T/B rabbet | Yes | No studs at top/bottom; box flush with baffle; extra woofer volume |
| 1/2" sides + back | Yes | Sufficient stiffness at short spans, maximizes internal volume |
| PL Premium + brads | Yes | Best MDF edge-grain bond, no splitting risk |
| 16" baffle width | Keep | 3/4" stud overlap is adequate with pre-drilled #8 screws at 6" spacing |
| No physical time alignment | Correct | 28mm offset at 2.5 kHz handled by LR4 crossover; physical options don't fit |
| No baffle step comp | Correct | In-wall = infinite baffle, no step exists |

---

## 17. Status

### Completed
- [x] Driver selection and procurement (prototype set: 2 woofers, 2 mids, 1 tweeter reused)
- [x] Free-air T/S measurement of all prototype drivers (3 break-in rounds for woofers)
- [x] Sealed alignment confirmed with measured values (Qtc ≈ 0.70, F3 ≈ 56 Hz)
- [x] Full enclosure engineering (dimensions, chambers, bracing, damping)
- [x] Baffle layout with all driver positions and routing specs
- [x] Cut list finalized
- [x] Wall installation method finalized (pre-drilled #8 × 2" pan-heads)
- [x] Off-axis and lobing analysis (no issues for seated HT listening)

### Next Steps
1. ~~Order MDF (2× 3/4" sheets + 2× 1/2" sheets) and hardware~~ ✓ complete
2. Build prototype enclosure ← **current task**
3. Route baffle (perimeter rabbet + driver holes + flush recesses)
4. Assemble with PL Premium + brad nails
5. Install in wall, mount drivers
6. Measure drivers in-box (DATS V3 impedance + REW/UMIK-1 frequency response)
7. Design crossover in VituixCAD
8. Iterate and finalize crossover
9. Order remaining drivers (4× woofers, 2× tweeters, 6× mids for final 3 speakers)
10. Build all 3 final speakers

---

*This document reflects the current plan. Update it as decisions are made — do not rely on the Development History for current values.*
