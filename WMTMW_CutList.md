# WMTMW In-Wall Speaker — Detailed Cut List & Assembly Reference

> **Per speaker. Build 3 identical units for L/C/R.**
> **Generated:** March 28, 2026
> **Companion files:**
> - Design doc: `/home/cyc/WMTMW_InWall_Speaker_Design.md`
> - 3D Diagram: `/home/cyc/WMTMW_Enclosure_3D.html`

---

## 1. Finished Enclosure Dimensions

```
    EXTERNAL (box only, excluding baffle):
    Width:   14.25"
    Depth:    5.50"
    Height:  46.50"

    INTERNAL (air space):
    Width:   13.25"    (14.25 − 2×0.50 side panels)
    Depth:    4.25"    (5.50 − 0.75 baffle − 0.50 back)
    Height:  45.00"    (46.50 − 2×0.75 top/bottom panels)

    BAFFLE (overhangs box for stud/drywall interface):
    Width:   16.00"    (overhangs box 0.875" per side)
    Height:  48.00"    (overhangs box 0.75" top + bottom)
    Thick:    0.75"    (rabbeted to 0.50" at perimeter edges)

    WALL CAVITY (2×6, 16" OC):
    Clear opening:  14.50" wide  ×  unlimited height
    Stud depth:      5.50"
    Box clearance:   0.125" per side (14.25" box in 14.50" opening)
```

---

## 2. MDF Cut List (Per Speaker)

### From 3/4" (19 mm) MDF

| # | Piece          | Qty | Width    | Height/Length | Notes                              |
|---|----------------|-----|----------|---------------|------------------------------------|
| 1 | **Front baffle** | 1 | 16.00"  | 48.00"        | Rabbeted + driver holes + recesses |
| 2 | **Top panel**    | 1 | 14.25"  | 4.75"         | Spans full width inside back panel |
| 3 | **Bottom panel** | 1 | 14.25"  | 4.75"         | Spans full width inside back panel |

### From 1/2" (12.7 mm) MDF

| # | Piece          | Qty | Width    | Height/Length | Notes                              |
|---|----------------|-----|----------|---------------|------------------------------------|
| 4 | **Back panel**   | 1 | 14.25"  | 46.50"        | Structural backbone of box         |
| 5 | **Side panels**  | 2 | 4.75"   | 45.00"        | Fit between top & bottom panels    |
| 6 | **Divider 1**    | 1 | 13.25"  | 4.25"         | Lower woofer / mid-tweeter boundary|
| 7 | **Divider 2**    | 1 | 13.25"  | 4.25"         | Mid-tweeter / upper woofer boundary|

### From 3/4" (19 mm) MDF — Bracing strips (rip from offcuts)

| # | Piece                | Qty | Cross-section | Length  | Notes                        |
|---|----------------------|-----|---------------|---------|------------------------------|
| 8 | **Back panel battens** | 2 | 3/4" × 3/4" | 13.25"  | Glue flat to back panel      |
| 9 | **Front-to-back ties** | 6 | 3/4" × 3/4" | 4.25"   | Glue between baffle and back |

### Summary Per Speaker

| Material     | Pieces | Total board area (approx)      |
|--------------|--------|--------------------------------|
| 3/4" MDF     | 1 main + 8 brace = 9  | ~12.5 sq ft          |
| 1/2" MDF     | 5 panels + 2 dividers | ~11.0 sq ft          |
| **For 3 speakers** | | ~37.5 sq ft 3/4" + ~33.0 sq ft 1/2" |

> **MDF order:** One 4×8 sheet of 3/4" MDF + one 4×8 sheet of 1/2" MDF
> covers all 3 speakers with waste for test cuts.

---

## 3. Panel Dimension Verification

### How the dimensions derive from the design constraints

```
DEPTH STACK (front to back):
    Baffle:          0.75"  (3/4" MDF)
    Internal depth:  4.25"  (driver clearance + air)
    Back panel:      0.50"  (1/2" MDF)
    ─────────────────────
    Total:           5.50"  ← matches 2×6 stud cavity ✓

WIDTH STACK (left to right):
    Left side panel:   0.50"  (1/2" MDF)
    Internal width:   13.25"
    Right side panel:  0.50"  (1/2" MDF)
    ─────────────────────────
    Total:            14.25"  ← fits 14.50" stud opening (0.125" clearance/side) ✓

HEIGHT STACK (bottom to top):
    Bottom panel:      0.75"  (3/4" MDF)
    Internal height:  45.00"
    Top panel:         0.75"  (3/4" MDF)
    ─────────────────────────
    Total:            46.50"  ✓
```

### Panel depth explanation (why sides/top/bottom are 4.75")

```
SIDE VIEW — panel lapping (depth direction):

    ┌─────────┬────────────────────────────────┬─────────┐
    │ BAFFLE  │        INTERNAL SPACE          │  BACK   │
    │  0.75"  │           4.25"                │  0.50"  │
    └─────────┴────────────────────────────────┴─────────┘
              │←──── side/top/bottom panel ────→│
              │           4.75"                 │

    Side, top, and bottom panels are 4.75" in the depth direction because
    they span from the inside face of the back panel to the front face of
    the box (where the baffle's back face will glue on).

    4.75" = internal depth (4.25") + back panel thickness (0.50")
    The baffle glues onto the FRONT edges of the sides, top, and bottom.
```

---

## 4. Assembly — Panel Lapping Detail

```
CORNER LAPPING — TOP VIEW (looking down):

              ← 16.00" (baffle) →
    ┌──────────────────────────────────────────┐
    │               BAFFLE (3/4")              │  ← overhangs 0.875" per side
    │    ┌────────────────────────────────┐    │
    │    │  ┌──┬──────────────────────┬──┐│    │
    │    │  │S │                      │S ││    │
    │    │  │I │   INTERNAL SPACE     │I ││    │
    │    │  │D │      13.25" W        │D ││    │
    │    │  │E │       × 4.25" D      │E ││    │
    │    │  │  │                      │  ││    │
    │    │  │½"│                      │½"││    │
    │    │  └──┴──────────────────────┴──┘│    │
    │    │          BACK PANEL (1/2")     │    │
    │    └────────────────────────────────┘    │
    │              ← 14.25" →                  │
    └──────────────────────────────────────────┘

CORNER LAPPING — FRONT VIEW (looking at baffle):

    ┌──────────────────────────────────────────┐ ← 48.00" baffle top
    │                BAFFLE                     │
    │  ┌────────────────────────────────────┐  │ ← 46.50" box top
    │  │           TOP PANEL (3/4")         │  │   14.25" × 4.75"
    │  ├──┬──────────────────────────────┬──┤  │
    │  │  │                              │  │  │
    │  │S │                              │S │  │
    │  │I │    INTERNAL: 13.25" × 45.00" │I │  │   Side panels
    │  │D │                              │D │  │   4.75" × 45.00"
    │  │E │                              │E │  │   (1/2" thick)
    │  │  │                              │  │  │
    │  ├──┴──────────────────────────────┴──┤  │
    │  │         BOTTOM PANEL (3/4")        │  │   14.25" × 4.75"
    │  └────────────────────────────────────┘  │ ← box bottom
    │                                          │
    └──────────────────────────────────────────┘ ← baffle bottom

    Side panels FIT BETWEEN top and bottom panels.
    Top/bottom panels are full width (14.25"), same as back panel.
    Back panel covers the entire back face (14.25" × 46.50").
```

### Assembly sequence

```
Step 1:  Lay back panel flat (14.25" × 46.50" × 1/2")
Step 2:  Glue bottom panel (14.25" × 4.75") perpendicular to back, at bottom edge
         Brad nail every 4-6". Bottom panel's back edge is flush with back panel inside face.
Step 3:  Glue both side panels (4.75" × 45.00" × 1/2") against back panel inside face,
         resting ON TOP of the bottom panel. Side panels sit 0.50" in from each edge.
Step 4:  Glue internal bracing (back panel battens) at woofer chamber centers
Step 5:  Thread woofer cables through divider holes BEFORE gluing dividers
Step 6:  Glue Divider 1 at 14.21" above bottom panel top surface (center of divider)
Step 7:  Glue Divider 2 at 30.79" above bottom panel top surface (center of divider)
Step 8:  Glue top panel (14.25" × 4.75") on top of side panel edges, flush with back
Step 9:  Let cure 24 hours
Step 10: Seal all joints (PL Premium fillet or silicone bead)
Step 11: Install front-to-back ties (6× 3/4" × 3/4" × 4.25" blocks)
Step 12: Stuff woofer chambers with polyfill (~50% fill)
Step 13: Line mid/tweeter chamber with 1" acoustic foam
Step 14: Route all driver cables
Step 15: Verify everything before closing:
         □ All joints sealed   □ Bracing cured   □ Stuffing in place
         □ Cables routed       □ Nothing loose
Step 16: Glue baffle onto front edges of sides, top, bottom, dividers, and ties
         Brad nail around perimeter + at divider edges
Step 17: Let cure 24 hours
Step 18: Mount drivers with M4 screws into T-nuts (foam gasket tape under flanges)
```

---

## 5. Baffle Routing Details

### 5.1 Perimeter Rabbet (back face of baffle)

```
    PURPOSE: Makes the baffle overhang edges 1/2" thick = drywall thickness = flush mount

    Rabbet dimensions:
    • Width:  1" from each edge (all four edges)
    • Depth:  1/4" (removes material from the back face)
    • Result: 3/4" center → 1/2" at edges

    CROSS-SECTION (baffle at edge):

    Room side (front) →
    ┌──────────────────────────────┐
    │          3/4" full           │  ← center (behind box)
    │                  ┌──────────┘
    │    1/2" at edge  │  1/4" rabbet step
    │                  │
    └──────────────────┘
    │←── 1" rabbet ──→│

    Tool: Router table + 1" straight bit + fence, OR handheld router + edge guide
    Run all four edges. The rabbet extends slightly past the stud overhang;
    the box panels cover it when assembled.
```

### 5.2 Driver Cutouts (through the baffle)

All drivers centered horizontally at 8.00" from baffle side edges.
Vertical positions measured from baffle bottom edge (0"):

| Driver         | Center from bottom | Cutout diameter | Recess diameter | Recess depth |
|----------------|-------------------|-----------------|-----------------|--------------|
| Lower woofer   | 12.00"            | 149 mm (5.87")  | 171 mm (6.73")  | 3 mm (1/8")  |
| Lower mid      | 18.75"            | 116 mm (4.57")  | 137 mm (5.39")  | 3 mm (1/8")  |
| Tweeter        | 24.00"            | 72 mm (2.83")   | ∅104 mm (4.09") | 3 mm (1/8")  |
| Upper mid      | 29.25"            | 116 mm (4.57")  | 137 mm (5.39")  | 3 mm (1/8")  |
| Upper woofer   | 36.00"            | 149 mm (5.87")  | 171 mm (6.73")  | 3 mm (1/8")  |

```
    FRONT VIEW OF BAFFLE (all holes centered at 8.00" from sides):

    16.00"
    ┌──────────────────────────────────────┐  48.00"
    │                                      │
    │          ┌────────────────┐           │  ← 38.62"
    │          │  149mm WOOFER  │           │    center 36.00"
    │          └────────────────┘           │  ← 31.88"
    │                                      │
    │            ┌────────────┐             │  ← 31.20"   (frame)
    │            │ 116mm MID  │             │    center 29.25"
    │            └────────────┘             │  ← 25.80"   (frame)
    │                                      │
    │              ┌────────┐               │  ← 26.05"   (frame)
    │              │ 72mm T │               │    center 24.00"
    │              └────────┘               │  ← 21.95"   (frame)
    │                                      │
    │            ┌────────────┐             │  ← 20.70"   (frame)
    │            │ 116mm MID  │             │    center 18.75"
    │            └────────────┘             │  ← 15.30"   (frame)
    │                                      │
    │          ┌────────────────┐           │  ← 14.62"
    │          │  149mm WOOFER  │           │    center 12.00"
    │          └────────────────┘           │  ←  7.88"
    │                                      │
    └──────────────────────────────────────┘   0.00"
```

### 5.3 Driver recesses (front face, shallow pockets)

```
    Each driver gets a shallow recess on the FRONT face of the baffle
    so the driver flange sits flush with the surface.

    • Diameter: matches driver frame OD (see table above)
    • Depth: ~3 mm (1/8") — match flange thickness
    • Tool: router + circle jig or MDF template
    • Remaining material behind recess: 19mm - 3mm = 16mm (5/8") — solid for T-nuts
```

### 5.4 T-nut locations

```
    Each driver has 4× M4 screw holes at 90° intervals around the cutout.
    Use actual driver as template — hold driver against baffle, mark holes.
    Drill through-holes, press T-nuts into BACK face of baffle.
```

---

## 6. Internal Chamber Layout

### Divider positions (from inside bottom = top surface of bottom panel)

```
    ┌──────────────────────────────┐  ← 45.00" (inside top)
    │                              │
    │     UPPER WOOFER CHAMBER     │  13.96" tall
    │     12.9 L (0.46 ft³)       │  Volume: 13.96" × 56.31 sq in
    │                              │
    │     [====WOOFER====]         │
    │                              │
    ├══════════════════════════════┤  ← 30.79" (Divider 2 center)
    │                              │     30.54" bottom surface
    │     [====MID====]            │     31.04" top surface
    │                              │
    │     MID / TWEETER SECTION    │  16.08" tall
    │     14.8 L (0.52 ft³)       │  Volume: 16.08" × 56.31 sq in
    │                              │
    │       [TWEETER]              │
    │                              │
    │     [====MID====]            │
    │                              │
    ├══════════════════════════════┤  ← 14.21" (Divider 1 center)
    │                              │     13.96" bottom surface → lower chamber height
    │     LOWER WOOFER CHAMBER     │     14.46" top surface
    │     12.9 L (0.46 ft³)       │  13.96" tall
    │                              │  Volume: 13.96" × 56.31 sq in
    │     [====WOOFER====]         │
    │                              │
    └──────────────────────────────┘  ← 0.00" (inside bottom)

    Cross-section: 13.25" × 4.25" = 56.31 sq in

    Height verification:
    13.96" + 0.50" + 16.08" + 0.50" + 13.96" = 45.00" ✓
```

### Divider notching

```
    Each divider must be notched where it crosses behind a driver cutout
    on the baffle. The divider sits between two cutout holes with ~0.5"
    clearance on each side. Measure the actual gap and trim if needed
    during dry-fit.
```

---

## 7. Internal Bracing Placement

### Back panel battens (2 per speaker)

```
    TOP VIEW of woofer chamber (battens glue flat to back panel):

    ┌──────────────────────────────────────┐  ← Baffle (front)
    │                                      │
    │                                      │
    │                                      │
    │  ════════════════════════════════════ │  ← 3/4" × 3/4" × 13.25" batten
    │                                      │     centered vertically in chamber
    └──────────────────────────────────────┘  ← Back panel

    One batten per woofer chamber, centered vertically (~7.35" from divider/panel)
    Breaks the back panel's longest unsupported span in half
```

### Front-to-back ties (6 per speaker)

```
    TOP VIEW of any chamber (ties bridge baffle to back panel):

    ┌──────────────────────────────────────┐  ← Baffle (front)
    │                                      │
    │  ┌──┐                          ┌──┐  │
    │  │  │    3/4" × 3/4" × 4.25"  │  │  │  ← 2 ties per chamber
    │  │  │    glued to baffle back   │  │  │     = 6 total
    │  │  │    + back panel front     │  │  │
    │  └──┘                          └──┘  │
    │                                      │
    └──────────────────────────────────────┘  ← Back panel

    Placement:
    • Woofer chambers: ~3" and ~10" from left edge (flanking woofer cutout)
    • Mid/tweeter chamber: in gaps between tweeter and each mid cutout
    • Minimum 1" clearance from any driver cutout edge
    • Must clear driver magnets on the inside
```

---

## 8. Wire Pass-Throughs

```
    Each divider: 2× 1/2" holes for woofer cables
    Location: near the sides, away from the driver cutout center
    Seal with silicone around wires after threading

    Top panel (prototype): 3× 1/2" holes for cables to external crossover
    Back panel (final):    1× binding post cup hole (size per cup specs)
```

---

## 9. Correction Notes

> **Side panel height:** The original design doc cut list specifies side panels
> at 4.75" × 48.00". This should be **4.75" × 45.00"** because the side panels
> fit BETWEEN the 3/4" top and bottom panels:
> 46.50" - 2(0.75") = 45.00".
>
> **Back panel thickness:** Changed from 3/4" to **1/2" MDF** (Session 8).
> This adds 0.25" to internal depth (4.00" → 4.25"), compensating for the
> volume lost when baffle height was reduced from 49.50" to 48.00".
> Total depth remains 5.50" (0.75" baffle + 4.25" internal + 0.50" back).

---

## 10. Material & Adhesive Summary

| Item                        | Per Speaker | For 3 Speakers |
|-----------------------------|-------------|----------------|
| 3/4" MDF (4×8 sheets)       | ~0.4 sheet  | 1.5 sheets     |
| 1/2" MDF (4×8 sheets)       | ~0.4 sheet  | 1.5 sheets     |
| PL Premium polyurethane      | ~1/2 tube   | 2 tubes        |
| 18ga brad nails (1.5" + 1") | ~100 nails  | 1 box each     |
| Silicone caulk               | —           | 1 tube         |
| T-nuts (M4)                  | 20          | 60+            |
| Foam gasket tape             | 1 roll      | 3 rolls        |
| Polyfill (12 oz bags)        | 2 bags      | 6 bags         |
| Acoustic foam (1" sheets)    | ~2 sq ft    | ~6 sq ft       |
| Spray adhesive               | —           | 1 can          |

---

*Cut list generated March 28, 2026. Verify all driver dimensions against actual hardware before cutting baffle holes.*
