# WMTMW 3-Way In-Wall Speaker Design

## Home Theater L/C/R — Detailed Build Plan

> **Project:** 3x identical WMTMW in-wall speakers for Left, Center, and Right channels  
> **Application:** Dedicated basement home theater (Movies, TV, Gaming)  
> **Listening Distance:** ~9 feet  
> **Amplification:** High-end receiver or separates, minimum 125W per channel  
> **Subwoofer:** Yes — L/C/R will cross over at 50–70 Hz  
> **Matching Speakers:** Mechano23 (sides + rears), potentially Atmos  
> **Budget:** Sub-$600 per speaker (not including MDF)  
> **Date:** March 2026 (measurements updated March 28, 2026)

---

## Table of Contents

1. [Design Overview](#1-design-overview)
2. [Physical Constraints & Feasibility](#2-physical-constraints--feasibility)
3. [Driver Selection](#3-driver-selection)
4. [Verified Pricing & Stock](#4-verified-pricing--stock)
5. [Cost Breakdown](#5-cost-breakdown)
6. [Driver Arrangement](#6-driver-arrangement)
7. [Wiring Strategy](#7-wiring-strategy)
8. [Crossover Architecture](#8-crossover-architecture)
9. [Enclosure Design — Detailed Engineering](#9-enclosure-design--detailed-engineering)
10. [Output & Sensitivity Estimates](#10-output--sensitivity-estimates)
11. [Off-Axis & Lobing Analysis](#11-off-axis--lobing-analysis)
12. [Timbre Matching Strategy](#12-timbre-matching-strategy)
13. [Risk Assessment](#13-risk-assessment)
14. [Build Process — Step by Step](#14-build-process--step-by-step)
15. [Required Tools & Software](#15-required-tools--software)
16. [Parts Shopping List](#16-parts-shopping-list)
17. [Reference Information](#17-reference-information)

---

## 1. Design Overview

```
Configuration:  WMTMW  (Woofer – Midrange – Tweeter – Midrange – Woofer)
Type:           3-way, sealed, passive crossover
Mounting:       In-wall, flush with drywall
Wall:           2×6 construction, 16" on center studs
Drivers:        5 per speaker (2 woofers, 2 midranges, 1 tweeter)
Crossovers:     ~400 Hz  /  ~2.5 kHz  (Linkwitz-Riley 4th order acoustic targets)
Impedance:      4–6 Ω nominal
Sensitivity:    ~87–88 dB (2.83V / 1m, in-wall half-space)
```

### Why WMTMW?

- **Vertical symmetry** — critical for identical L/C/R behavior
- **Double midranges** — increased power handling in the dialogue band (400 Hz – 2.5 kHz)
- **Reduced floor/ceiling reflections** — vertical lobing actually improves clarity for seated listeners
- **Industry standard** — used by JBL Synthesis, Revel, KEF Ci, and other high-end in-wall designs
- **Timbre matching** — uses the same drivers as the Mechano23 surrounds

---

## 2. Physical Constraints & Feasibility

### Depth Budget

```
                              ┌─── Room side
                              │
    Drywall (removed):        │  0.50"   ← Speaker baffle sits here (flush)
    Front baffle (3/4" MDF):  │  0.75"   ← Rabbeted to 1/2" at L/R edges only
                              │            (flush with drywall; full 3/4" at center)
    Internal depth:           │  4.25"   ← Driver + air space + polyfill
    Back panel (1/2" MDF):    │  0.50"
                              │
    Total stud cavity used:   │  5.50"
                              └─── Back of wall

    Deepest driver (6.5" woofer):  2.44" mounting depth
    Clearance behind driver:       1.81"  ← Room for air + stuffing
```

**Verdict: Depth is NOT a concern.** All drivers fit with 1.5"+ clearance.

### Width

```
    Stud spacing:              16" on center
    Stud width:                 1.5"
    Clear opening:             14.5"  between studs
    Enclosure external width:  14.25" (0.125" clearance per side)
    Front baffle width:        16.00" (3/4" overlap onto each stud face)
    Internal width:            13.25" (after 1/2" MDF side panels)
    Largest driver:             6.73" (SB17MFC35-8 frame) — fits easily
```

### Height

```
    Enclosure height:          48.00" (flush with baffle, no T/B overhang)
    Driver stack (C-to-C):     24.00" (bottom woofer to top woofer)
    Frame extent:              30.74" (bottom woofer frame to top woofer frame)
    Cap space (top & bottom):   8.64" each — provides woofer volume
```

**Verdict: The in-wall design is fully feasible in a standard 2×6 wall.**

---

## 3. Driver Selection

### Woofer — SB Acoustics SB17MFC35-8

| Parameter          | Value                                    |
|--------------------|------------------------------------------|
| **Size**           | 6.5" (165 mm)                            |
| **Cone Material**  | Polypropylene                            |
| **Impedance**      | 8 Ω                                      |
| **Mounting Depth** | ~2.4" (~60 mm)                           |
| **Frame**          | Vented cast aluminum, 171 mm diameter    |
| **Quantity**       | 2 per speaker                            |
| **Role**           | Bass (50–70 Hz – 400 Hz via sub + crossover) |

**Official T/S Parameters (SB Acoustics):**
```
Fs = 33 Hz      Qts = 0.37     Vas = 39 L      Sensitivity = 88 dB (2.83V/1m)
Qes = 0.40      Qms = 4.9      Mms = 11.8 g    Bl = 5.9 Tm
Re = 5.7 Ω      Le = 0.15 mH   Sd = 118 cm²    Xmax = 5.5 mm (one-way)
Power = 60 W     Magnet = 0.54 kg                Net weight = 1.56 kg
```

**Why this driver:**
- In stock at Madisound ($75.90 each)
- Well-damped polypropylene cone simplifies crossover (no sharp breakup peaks)
- Shallow mounting depth fits 2×6 wall with margin
- SB Acoustics quality at a reasonable price point
- Excellent sealed alignment in 12.9L chambers (Qtc ≈ 0.70 with polyfill — ideal Butterworth)
- F3 ≈ 63 Hz with polyfill — supports a 50–70 Hz sub crossover with room gain
- SB17NRX2L35-8 (Norex, NEW) was evaluated and rejected: its very low Qts (0.28)
  makes it severely overdamped in 12.9L (Qtc = 0.49, F3 ≈ 105 Hz) — excellent driver
  but needs a 5–6L box, not 12L. See Section 9.7 for full comparison.

**Measured T/S Parameters (DATS V3, free-air, post-break-in):**

Break-in: 1hr ~27 Hz tone + 15 hrs pink noise (3rd round); measured with
18.26g added mass (putty + quarter on jewelry scale). Piston diameter 122.4 mm.

| Parameter | Published | Woofer 1 | Woofer 2 | Notes |
|-----------|-----------|----------|----------|-------|
| Re        | 5.7 Ω     | 5.726 Ω  | 5.806 Ω  | Both within spec |
| Fs        | 33 Hz     | 36.67 Hz | 35.16 Hz | 11%/6.5% high — still loosening |
| Qms       | 4.9       | 5.114    | 5.322    | Slightly higher than published |
| Qes       | 0.40      | 0.506    | 0.460    | Higher — see alignment note |
| Qts       | 0.37      | 0.460    | 0.423    | 24%/14% above published |
| Vas       | 39 L      | 22.74 L  | 24.64 L  | Lower follows from stiff Fs |
| Mms       | 11.8 g    | 16.12 g  | 16.18 g  | See Mms note below |
| BL        | 5.9 Tm    | 6.483 Tm | 6.721 Tm | Higher than published |
| Zmax      | —         | 63.6 Ω   | 73.05 Ω  | |
| Le        | 0.15 mH   | 0.208 mH | 0.200 mH | |
| SPL       | 88 dB     | 85.35 dB | 85.57 dB | |

*Woofer matching: Fs gap 1.5 Hz (4.3%), Qts gap 0.037 (8.8%) — acceptable pair.*

**Mms note:** Both woofers consistently measure ~16.15g (vs published 11.8g).
The mid drivers, measured with the same technique and scale, match published Mms
within 3–4% (see below) — validating the measurement method. The woofer Mms
discrepancy is genuine, not a measurement artifact. The sealed alignment still
works well with measured values (see Section 9.7).

**Measured alignment in 14.9 L effective chamber (with polyfill):**
- Woofer 1: Qtc ≈ 0.73, Fc ≈ 58 Hz, F3 ≈ 55 Hz — just above Butterworth
- Woofer 2: Qtc ≈ 0.69, Fc ≈ 58 Hz, F3 ≈ 59 Hz — just below Butterworth
- Average: Qtc ≈ 0.71, F3 ≈ 57 Hz — essentially ideal Butterworth
- **Current enclosure design works as-is. No changes needed.**

SB Acoustics publishes post-break-in T/S values. These drivers may continue
to loosen with use, moving closer to published specs over time.

### Midrange — SB Acoustics SB13PFCR25-08

| Parameter          | Value                                    |
|--------------------|------------------------------------------|
| **Size**           | 5" (130 mm)                              |
| **Cone Material**  | Composite paper                          |
| **Impedance**      | 8 Ω                                      |
| **Surround**       | Rubber                                   |
| **Frame**          | Round, 150 mm diameter                   |
| **Mounting Depth** | ~2.0" (~55 mm)                           |
| **Quantity**       | 2 per speaker                            |
| **Role**           | Midrange (400 Hz – 2.5 kHz via crossover)|

**Official T/S Parameters (SB Acoustics):**
```
Fs = 45 Hz      Qts = 0.33     Vas = 13.4 L    Sensitivity = 87 dB (2.83V/1m)
Qes = 0.39      Qms = 2.2      Mms = 10.0 g    BL = 6.2 Tm
Re = 5.6 Ω      Le = 0.77 mH   Sd = 87 cm²     Piston diameter = 105.2 mm
```

**Why this driver:**
- **Same driver as the Mechano23 woofer** (8 Ω variant) — ensures timbre matching across the entire speaker system
- ASR-measured in the Mechano23 with remarkably low distortion and flat midrange response
- Paper cone with natural, smooth sound — ideal for dialogue clarity
- In its 400 Hz – 2.5 kHz operating band, this driver is in its absolute sweet spot
- Proven performer: Amir called the Mechano23 "a masterpiece"

**Measured T/S Parameters (DATS V3, free-air, post-break-in):**

Break-in: 30 min ~36 Hz tone + 15 hrs pink noise; measured with added mass on
jewelry scale. Piston diameter 105.2 mm (from Sd = 87 cm²).

| Parameter | Published | Mid 3   | Mid 4   | Notes |
|-----------|-----------|---------|---------|-------|
| Re        | 5.6 Ω     | 5.784 Ω | 5.442 Ω | Within spec |
| Fs        | 45 Hz     | 52.69 Hz| 51.68 Hz| 15–17% high — still loosening |
| Qms       | 2.2       | 2.729   | 2.663   | Higher — suspension stiff |
| Qes       | 0.39      | 0.462   | 0.418   | |
| Qts       | 0.33      | 0.395   | 0.361   | 20%/9% above published |
| Vas       | 13.4 L    | 9.28 L  | 9.73 L  | Low — follows from elevated Fs |
| Mms       | 10.0 g    | 10.42 g | 10.33 g | **+3–4% — validates measurement technique** |
| BL        | 6.2 Tm    | 6.571 Tm| 6.609 Tm| +6% — slight over-spec |
| Zmax      | —         | 39.95 Ω | 40.12 Ω | |
| Le        | 0.77 mH   | 0.530 mH| 0.529 mH| |
| SPL       | 87 dB     | 86.57 dB| 86.96 dB| |

*Mid matching: Fs gap 1.0 Hz (1.9%), Mms gap 0.09g (0.9%), BL gap 0.6% — excellent pair.*

**Mms validation:** The mid Mms values (10.42/10.33g vs published 10.0g) confirm
the jewelry scale + putty added-mass technique is accurate. This validates that
the woofer Mms discrepancy (~16.15g vs 11.8g published) is a genuine driver
characteristic, not measurement error.

The elevated Fs (52–53 Hz vs 45 published) is consistent with incomplete break-in.
For the mids, Fs does not drive the enclosure design — the 14.8 L shared chamber
is well oversized, and the crossover high-pass at 400 Hz dominates the low end.

### Tweeter — Scan-Speak Discovery H2606/9200

| Parameter          | Value                                    |
|--------------------|------------------------------------------|
| **Size**           | 26 mm (1") dome                          |
| **Dome Material**  | Textile (soft dome)                      |
| **Impedance**      | 6 Ω                                      |
| **Sensitivity**    | 95 dB (2.83V / 1m)                      |
| **Loading**        | Horn-loaded (built-in waveguide)         |
| **Mounting Depth** | ~0.9" (~22 mm)                           |
| **Faceplate**      | ∅104 mm (round)                          |
| **Quantity**       | 1 per speaker                            |
| **Role**           | Treble (2.5 kHz+ via crossover)          |

**Why this driver:**
- **Same tweeter as the Mechano23** — ensures timbre matching
- Horn-loaded design provides controlled directivity and high sensitivity
- Textile dome per builder preference (no ribbon tweeters)
- The horn loading is what gave the Mechano23 its nearly perfect directivity matching at crossover (praised in ASR review)
- High 95 dB sensitivity will be padded down ~10–13 dB to match midranges — standard practice, already done in the Mechano23 crossover

---

## 4. Verified Pricing & Stock

> **All prices verified live from Madisound (madisoundspeakerstore.com) — March 2026**

| Qty/Spk | Driver                        | Unit Price | Stock Status   |
|---------|-------------------------------|------------|----------------|
| 2       | SB Acoustics SB17MFC35-8      | $75.90     | **IN STOCK**   |
| 2       | SB Acoustics SB13PFCR25-08    | $36.80     | **IN STOCK**   |
| 1       | Scan-Speak H2606/9200         | $47.80     | **IN STOCK**   |

### Alternate Sources

| Retailer       | Location           | Notes                                      |
|----------------|--------------------|--------------------------------------------|
| **Madisound**  | Madison, WI        | Primary source. Best selection of SB & SS   |
| **Solen**      | St-Hubert, QC      | Canadian. Carries SB Acoustics & Scan-Speak |
| **Meniscus**   | Grand Rapids, MI   | SB Acoustics dealer. Crossover design help  |

> **Note:** Parts Express does NOT carry SB Acoustics or Scan-Speak drivers.

---

## 5. Cost Breakdown

### Per Speaker

| Category                                           | Cost          |
|----------------------------------------------------|---------------|
| 2× SB17MFC35-8 woofers                            | $151.80       |
| 2× SB13PFCR25-08 midranges                        | $73.60        |
| 1× Scan-Speak H2606/9200 tweeter                  | $47.80        |
| **Subtotal — Drivers**                             | **$273.20**   |
| Crossover components (inductors, caps, resistors)  | $120 – $180   |
| Hardware (binding posts, wire, polyfill, damping)   | $25 – $35     |
| **Total per speaker (not including MDF)**          | **$418 – $488** |

### For All 3 L/C/R Speakers

| Category                    | Cost              |
|-----------------------------|-------------------|
| Drivers (15 total)          | $819.60           |
| Crossover components (×3)   | $360 – $540       |
| Hardware (×3)               | $75 – $105        |
| **Grand Total (3 speakers)**| **$1,255 – $1,465** |

### Budget Headroom

```
Budget:              $600/speaker × 3 = $1,800
Estimated cost:      $1,255 – $1,465
Remaining:           $335 – $545  ← Available for premium crossover parts
                                     or contingency
```

---

## 6. Driver Arrangement

```
            ┌──────────────────────────────────┐
            │           (8.38" cap)            │
            │                                  │
            │     ┌──────────────────────┐     │
            │     │                      │     │
            │     │    6.5" WOOFER       │     │    SB17MFC35-8
            │     │    SB17MFC35-8       │     │    center: 36.00"
            │     │                      │     │
            │     └──────────────────────┘     │
            │    ════════════════════════════   │    ← Divider (1/2" MDF)
            │        ┌──────────────┐          │
            │        │  5" MIDRANGE │          │    SB13PFCR25-08
            │        │  SB13PFCR25  │          │    center: 29.25"
            │        └──────────────┘          │
            │                                  │
            │          ┌──────────┐            │
            │          │ TWEETER  │            │    Scan-Speak H2606/9200
            │          │ H2606    │            │    center: 24.00" (ear height)
            │          └──────────┘            │
            │                                  │
            │        ┌──────────────┐          │
            │        │  5" MIDRANGE │          │    SB13PFCR25-08
            │        │  SB13PFCR25  │          │    center: 18.75"
            │        └──────────────┘          │
            │    ════════════════════════════   │    ← Divider (1/2" MDF)
            │     ┌──────────────────────┐     │
            │     │                      │     │
            │     │    6.5" WOOFER       │     │    SB17MFC35-8
            │     │    SB17MFC35-8       │     │    center: 12.00"
            │     │                      │     │
            │     └──────────────────────┘     │
            │                                  │
            │           (8.38" cap)            │
            └──────────────────────────────────┘

                    ← 14.25" wide →

            Driver stack (C-to-C, bottom woofer to top woofer): 24.00"
            Mid-to-mid (C-to-C, through tweeter): 10.50" (267 mm)
            Total enclosure height: 48.00"
            Tweeter positioned at seated ear height (center of enclosure)
```

---

## 7. Wiring Strategy

Using **8 Ω drivers wired in parallel** for optimal impedance and output.

```
    ┌─────────────────────────────────────────────────┐
    │                                                 │
    │   WOOFER SECTION                                │
    │                                                 │
    │     SB17MFC35-8 (8Ω) ───┬─── = 4 Ω parallel    │
    │     SB17MFC35-8 (8Ω) ───┘                      │
    │                                                 │
    ├─────────────────────────────────────────────────┤
    │                                                 │
    │   MIDRANGE SECTION                              │
    │                                                 │
    │     SB13PFCR25-08 (8Ω) ──┬─── = 4 Ω parallel   │
    │     SB13PFCR25-08 (8Ω) ──┘                     │
    │                                                 │
    ├─────────────────────────────────────────────────┤
    │                                                 │
    │   TWEETER SECTION                               │
    │                                                 │
    │     H2606/9200 (6Ω)  ────────── = 6 Ω          │
    │                                                 │
    └─────────────────────────────────────────────────┘

    System impedance at any frequency: 4–6 Ω nominal
    Safe for any quality receiver or separates amplifier
```

### Why 8 Ω Parallel (Not 4 Ω Series)?

| Approach              | Woofer Z | Mid Z | Pros                          | Cons                      |
|-----------------------|----------|-------|-------------------------------|---------------------------|
| **8Ω parallel (rec)** | 4 Ω      | 4 Ω   | Standard load, clean impedance | Slightly lower Z at dips  |
| 4Ω series             | 8 Ω      | 8 Ω   | Very safe impedance           | Higher Z, less max output |

Both deliver the same acoustic output. Parallel 8 Ω is recommended as it presents a more
standard load to the amplifier and is the approach used in most commercial multi-driver designs.

---

## 8. Crossover Architecture

### Preliminary Topology

```
                        ┌──── LPF ~400 Hz (LR4) ──────── Woofer Pair (4Ω)
                        │      + Zobel network              ↕ parallel
                        │      + Impedance EQ
                        │
    AMP INPUT ──────────┼──── BPF 400 Hz – 2.5 kHz ────── Midrange Pair (4Ω)
                        │      HPF + LPF (LR4 targets)      ↕ parallel
                        │      + Sealed sub-enclosure        + notch filter
                        │        provides natural HPF          (if needed)
                        │
                        └──── HPF ~2.5 kHz (LR4) ────────  Tweeter (6Ω)
                               + L-pad (~10–13 dB atten.)
                               + Zobel network
                               + Impedance EQ
```

### Crossover Design Notes

| Parameter                  | Detail                                                |
|----------------------------|-------------------------------------------------------|
| **Target slopes**          | Linkwitz-Riley 4th order (LR4) acoustic               |
| **Low crossover**          | ~400 Hz (woofer → midrange)                           |
| **High crossover**         | ~2.5 kHz (midrange → tweeter)                         |
| **Tweeter attenuation**    | ~10–13 dB L-pad (95 dB tweeter → ~85 dB system level) |
| **Baffle step comp.**      | **Not needed** — in-wall = infinite baffle             |
| **Design tool**            | VituixCAD (free, Windows)                             |
| **Measurement tools**      | DATS V3 (impedance) + UMIK-1 (frequency response)    |

### In-Wall Advantage: No Baffle Step

A major simplification: flush-mounting in a wall provides infinite baffle loading. The 6 dB
baffle step that plagues bookshelf speakers **does not exist** for in-wall designs. This
eliminates the need for baffle step compensation in the crossover, saving components and
preserving sensitivity.

### Critical Note

> **The crossover will be custom-designed using YOUR measurements of YOUR drivers in YOUR
> enclosure.** The frequencies and component values above are preliminary targets. Final values
> will be determined through VituixCAD simulation using real DATS V3 impedance sweeps and
> UMIK-1 frequency response measurements. This is the standard, proven approach for high-
> quality DIY speakers and is exactly how the Mechano23 was designed.

---

## 9. Enclosure Design — Detailed Engineering

### 9.1 External Dimensions

```
    ┌──────────────────────────────────────────────────────────┐
    │                                                          │
    │   Box External:    14.25" W  ×  5.50" D  ×  48.00" H    │
    │   Front Baffle:    16.00" W  ×  48.00" H  ×  0.75" D    │
    │                                                          │
    │   Box Width:   14.25"  (fits between studs)              │
    │   Baffle Width:16.00"  (0.875" overlap onto each stud)   │
    │   Depth:        5.50"  (full 2×6 stud cavity)            │
    │   Box Height:  48.00"  (flush with baffle, no T/B overhang) │
    │   Baffle Height:  48.00"                                   │
    │                                                          │
    └──────────────────────────────────────────────────────────┘
```

**Baffle mounting:** The 3/4" MDF baffle has a 1/4"-deep rabbet on its back
face on the left and right edges only, reducing those flanges to 1/2" thick —
the same thickness as standard drywall. This makes the baffle face flush with
the wall surface at the sides. The full 3/4" thickness is maintained in the
center for strong driver mounting. No rabbet on top/bottom — the box is flush
with the baffle at those edges (no overhang). The baffle extends 0.875" past
each side of the box to overlap the stud faces. Screws through the baffle
flanges into the studs provide the primary mounting (#8 × 2" pan-head
coarse-thread wood screws, 7/64" pilot holes, ~6" spacing).
A horizontal cross stud at the bottom supports the enclosure weight.

Driver flanges are flush-mounted into ~3mm (1/8") shallow recesses routed into
the front face of the baffle at each driver position. With 3/4" material, this
leaves ~16mm (5/8") behind each recess — solid for T-nut engagement.

**Drywall cutout:** 16.0" wide × 48.0" tall — exposes 3/4" of each stud face
and 3/4" of each horizontal cross stud.

Mount height: Position the speaker so the **tweeter is at seated ear height**
(typically 36–40" from floor). With the tweeter at the vertical center of the
enclosure (24" from bottom), the bottom of the box should be at ~14" from floor.

### 9.2 Panel Construction

| Element          | Material | Thickness | Notes                                           |
|------------------|----------|-----------|--------------------------------------------------|
| Front baffle     | MDF      | 3/4"      | Rabbeted to 1/2" at L/R edges only; driver recesses on front |
| Back panel       | MDF      | 1/2"      | Sealed, screwed + glued                          |
| Side panels      | MDF      | 1/2"      | Line the stud cavity; short span (~4.75") = stiff at 1/2" |
| Top panel        | MDF      | 3/4"      | Sealed; flush with baffle top                    |
| Bottom panel     | MDF      | 3/4"      | Sealed; flush with baffle bottom                 |
| Internal dividers| MDF      | 1/2"      | Horizontal shelves separating chambers           |
| Internal braces  | MDF      | 3/4"      | Horizontal battens, front-to-back ties           |

**All panels are glued permanently.** The entire box including the front baffle
is assembled with PL Premium polyurethane adhesive + 18-gauge brad nails for
maximum rigidity and air-tight seal. PL Premium bonds MDF end grain better than
PVA wood glue (MDF's porous edges wick away water-based PVA). Brad nails hold
alignment while the adhesive cures (24h) without the splitting risk of screws
into MDF edge grain. All internal wiring, stuffing, bracing, and crossover
components (final build) must be installed BEFORE the front baffle is glued on.

**T-nuts:** Press T-nuts into the back of the baffle at all driver mounting
holes. This provides machine-thread engagement for driver removal/reinstallation.
With 3/4" MDF (16mm behind driver recesses), T-nut barrels engage fully. Drivers
are the only components accessible after assembly (they remove through the front).

### 9.2a Baffle Rabbet & Driver Recess Details

The 3/4" baffle has two types of routed features:

**1. Side rabbet (back face) — flush wall interface:**
```
    CROSS-SECTION (horizontal cut through baffle at stud):

    Room side →

    Drywall          Baffle overhang       Baffle center (behind box)
    ┌──────┐    ┌──────┐              ┌─────────────────────┐
    │ 1/2" │    │ 1/2" │              │       3/4"          │
    │      │    │      │──────────────│                     │
    └──────┘    └──────┘  1/4" step   └─────────────────────┘
       ↑            ↑    (rabbet)            ↑
    On stud      On stud               Box sides butt here
    face         face                  (full 3/4" thickness)
```
- Location: back face of baffle, **left and right edges only** (no top/bottom)
- Width: 1" from each side edge (covers 7/8" side overhang)
- Depth: 1/4" (leaves 1/2" at edges = drywall thickness)
- Tool: router table + 1" straight bit + fence, or handheld router + edge guide
- The rabbet extends slightly past the stud overhang into the box footprint;
  the box sides cover it when glued
- Top/bottom: no rabbet needed — box is flush with baffle at those edges
  (no stud overlap, no structural or flush-mounting requirement)

**2. Driver recesses (front face) — flush driver mounting:**
- Location: front face of baffle, centered on each driver cutout
- Diameter: match driver frame OD (171mm woofer, 137mm mid, 104mm tweeter)
- Depth: ~3mm (1/8") — match driver flange thickness
- Remaining material: 19mm - 3mm = 16mm (5/8") — solid for T-nut engagement
- Tool: router + circle jig or MDF template for each driver size
- Drivers sit flush with baffle surface, eliminating local edge diffraction

### 9.3 Internal Dimensions

```
    Internal:  13.25" W  ×  4.25" D  ×  46.50" H

    Width:   14.25" - 2(0.50") = 13.25"
    Depth:    5.50" - 0.75" - 0.50" =  4.25"  (3/4" baffle + 1/2" back)
    Height:  48.00" - 2(0.75") = 46.50"

    Cross-section area:  13.25" × 4.25" = 56.31 sq in
```

### 9.4 Driver Physical Dimensions

> Note: These are from SB Acoustics / Scan-Speak published catalogs. Verify
> against the actual drivers when received. All dimensions are nominal.

| Parameter        | SB17MFC35-8    | SB13PFCR25-08  | H2606/9200      |
|                  | (6.5" woofer)  | (5" midrange)  | (tweeter)       |
|------------------|----------------|----------------|-----------------|
| Frame OD         | 171 mm / 6.73" | ~137 mm / 5.39"| ∅104 mm / 4.09"  |
| Cutout diameter  | 149 mm / 5.87" | ~116 mm / 4.57"| 72 mm / 2.83"    |
| Mounting depth   |  62 mm / 2.44" |  ~55 mm / 2.17"|  ~22 mm / 0.87" |
| Screw holes      | 4× M4          | 4× M4          | 4× M4           |
| Fits 13.25" W?   | YES (6.73")    | YES (5.39")    | YES (4.09")     |
| Fits 4.25" D?    | YES (1.81" clr)| YES (2.08" clr)| YES (3.38" clr) |

H2606/9200 faceplate is round (∅104 mm). All driver recesses are routed as circles.

**All drivers fit comfortably within the enclosure.**

### 9.5 Driver Placement (Baffle Layout)

All 5 drivers mount in a vertical column, centered horizontally on the front
baffle. The tweeter is at the vertical center of the enclosure.

**Center-to-center spacing:**
- Woofer to adjacent midrange: **6.75"** (171 mm)
- Midrange to tweeter:         **5.25"** (133 mm)
- Mid-to-mid (through tweeter):**10.50"** (267 mm) ← critical for lobing

```
    Driver positions measured from BOTTOM of baffle (0" = bottom edge):

    ┌──────────────────────────────┐ ← 48.00" (top of enclosure/baffle)
    │                              │
    │                              │
    │     ┌────────────────┐       │
    │     │   6.5" WOOFER  │       │ ← center at 36.00"
    │     │  SB17MFC35-8   │       │   frame: 31.88" to 38.62"
    │     └────────────────┘       │
    │    ═══════════════════════   │ ← DIVIDER 2 at ~31.54"
    │       ┌────────────┐         │
    │       │ 5" MIDRANGE│         │ ← center at 29.25"
    │       │ SB13PFCR25 │         │   frame: 25.80" to 31.20"
    │       └────────────┘         │
    │         ┌────────┐           │
    │         │TWEETER │           │ ← center at 24.00" (= 24" from bottom)
    │         │H2606   │           │   faceplate: ∅104mm (21.95" to 26.05")
    │         └────────┘           │
    │       ┌────────────┐         │
    │       │ 5" MIDRANGE│         │ ← center at 18.75"
    │       │ SB13PFCR25 │         │   frame: 15.30" to 20.70"
    │       └────────────┘         │
    │    ═══════════════════════   │ ← DIVIDER 1 at ~14.96"
    │     ┌────────────────┐       │
    │     │   6.5" WOOFER  │       │ ← center at 12.00"
    │     │  SB17MFC35-8   │       │   frame: 7.88" to 14.62"
    │     └────────────────┘       │
    │                              │
    │                              │
    └──────────────────────────────┘ ← 0" (bottom of enclosure/baffle)

              ← 14.25" →
```

### 9.6 Internal Chamber Design (2-Divider Approach)

Two 1/2" MDF horizontal dividers create three sealed chambers:

```
    ┌──────────────────────────────┐
    │                              │
    │     UPPER WOOFER CHAMBER     │  14.71" tall
    │     (sealed, polyfill)       │  13.6 L  (0.48 ft³)
    │                              │
    │     [====WOOFER====]         │  ← SB17MFC35-8
    │                              │
    ├══════════════════════════════┤  ← Divider 2 (1/2" MDF) at 31.54"
    │                              │
    │     [====MID====]            │  ← SB13PFCR25-08
    │                              │
    │     MID / TWEETER SECTION    │  16.08" tall
    │     (shared sealed volume)   │  14.8 L  (0.52 ft³)
    │     (acoustic foam damping)  │
    │                              │
    │       [TWEETER]              │  ← H2606/9200
    │                              │
    │     [====MID====]            │  ← SB13PFCR25-08
    │                              │
    ├══════════════════════════════┤  ← Divider 1 (1/2" MDF) at 14.96"
    │                              │
    │     [====WOOFER====]         │  ← SB17MFC35-8
    │                              │
    │     LOWER WOOFER CHAMBER     │  14.71" tall
    │     (sealed, polyfill)       │  13.6 L  (0.48 ft³)
    │                              │
    └──────────────────────────────┘
```

### 9.7 Chamber Volumes & Sealed Alignment

| Chamber           | Height  | Volume     | Volume     | Damping         |
|-------------------|---------|------------|------------|-----------------|
| Lower woofer      | 14.71"  | 13.6 L     | 0.48 ft³   | Polyfill, medium|
| Mid/tweeter       | 16.08"  | 14.8 L     | 0.52 ft³   | Acoustic foam   |
| Upper woofer      | 14.71"  | 13.6 L     | 0.48 ft³   | Polyfill, medium|
| **Total internal**| 46.50"  | **42.0 L** |**1.48 ft³**|                 |

**Woofer sealed alignment (each chamber independently):**

Official SB Acoustics T/S for SB17MFC35-8: Fs = 33 Hz, Qts = 0.37, Vas = 39 L

Without polyfill (13.6 L gross, ~13.1 L net after bracing/driver displacement):
- Qtc = 0.37 × sqrt(1 + 39/13.1) = 0.37 × 2.00 = **0.74**
- Fc = 33 × 2.00 = 65.9 Hz
- F3 ≈ 62 Hz
- Slightly above Butterworth — tight, well-controlled bass

With polyfill (effective +20% volume → ~15.7 L net):
- Qtc = 0.37 × sqrt(1 + 39/15.7) = 0.37 × 1.87 = **0.69**
- Fc = 33 × 1.87 = 61.6 Hz
- F3 ≈ 63 Hz
- **Essentially ideal Butterworth (0.707) — maximally flat, clean transients**

Response at key frequencies (with polyfill, net volume):
```
    120 Hz:  -0.3 dB    (flat)
    100 Hz:  -0.7 dB    (flat)
     80 Hz:  -1.4 dB    (essentially flat)
     70 Hz:  -2.2 dB    (usable, blending with sub)
     60 Hz:  -3.5 dB    (sub taking over)
     50 Hz:  -5.5 dB    (sub dominant, room gain helps)
```

> **Note:** F3 is remarkably stable (~63 Hz) regardless of polyfill or
> minor volume changes. This is because Fc and Qtc effects on F3 cancel
> when Qtc is near 0.707. Room gain (+3–6 dB below 80 Hz in a basement
> theater) effectively extends perceived bass another half-octave.

**Sealed alignment with MEASURED T/S parameters (DATS V3, post-break-in):**

With polyfill (effective ~15.7 L net):

| Parameter      | Published | Woofer 1 (measured) | Woofer 2 (measured) |
|----------------|-----------|---------------------|---------------------|
| Qts            | 0.37      | 0.460               | 0.423               |
| Vas            | 39 L      | 22.74 L             | 24.64 L             |
| **Qtc**        | **0.69**  | **0.72**            | **0.68**            |
| **Fc**         | 61.6 Hz   | 57.4 Hz             | 56.4 Hz             |
| **F3**         | ~63 Hz    | ~54 Hz              | ~58 Hz              |
| Character      | Ideal BW  | Just above BW       | Just below BW       |

Average Qtc ≈ 0.70, average F3 ≈ 56 Hz — essentially ideal Butterworth.
The higher Qts (vs published 0.37) is offset by the lower Vas, and the
result lands right at the Butterworth target. F3 is actually *better*
(lower) than the 63 Hz estimated from published specs.

**This alignment supports a 50–70 Hz sub crossover.** The woofer holds
together well into the 60 Hz range. Room gain in a basement theater
(typically +3–6 dB below 60–80 Hz) further extends perceived bass.
Combined with dual woofers running in parallel, the front stage will
deliver real bass impact down to the sub crossover point.

**Alternative woofer evaluated — SB17NRX2L35-8 (Norex, NEW):**

The NRX2L35-8 was evaluated as a potential upgrade. It has a massively
stronger motor (Bl = 7.84 Tm, magnet = 0.89 kg) giving Qts = 0.28 and
89 dB sensitivity — impressive specs. However, in 13.6 L sealed:

| Parameter     | MFC35-8 (chosen) | NRX2L35-8 (rejected) | NRX2C35-8 (ref)  |
|---------------|-------------------|----------------------|-------------------|
| Cone          | Polypropylene     | Norex                | Norex             |
| Fs            | 33 Hz             | 37.8 Hz              | 36.5 Hz           |
| Qts           | 0.37              | 0.28                 | 0.42              |
| Vas           | 39 L              | 26.1 L               | 27 L              |
| Sensitivity   | 88 dB             | 89 dB                | 87 dB             |
| Bl            | 5.9 Tm            | 7.84 Tm              | 6.25 Tm           |
| Xmax (1-way)  | 5.5 mm            | 4.8 mm               | 5.5 mm            |
| **Qtc in 13.6L** | **0.73**      | **0.48**             | **0.73**          |
| **Qtc net ~13.1L**| **0.74**     | **0.48**             | **0.74**          |
| **F3 (gross)**   | **~62 Hz**    | **~103 Hz**          | **~62 Hz**        |

The NRX2L's Qts of 0.28 means it's severely overdamped in 13.6 L
(Qtc = 0.48). It needs a ~5 L box for Butterworth alignment:
- At 60 Hz: MFC is -3.5 dB, NRX2L is -7.1 dB (3.6 dB worse)
- At 80 Hz: MFC is -1.4 dB, NRX2L is -4.7 dB (3.3 dB worse)
The NRX2L is an excellent driver for small sealed monitors (5–8 L),
but wrong for 13.6 L chambers and a 50–70 Hz crossover target.

In-wall loading does NOT change this: half-space loading adds ~6 dB
across all frequencies equally — it raises the level but does not
change the rolloff shape, Qtc, or F3. Both drivers benefit equally.

**Midrange sealed alignment (pair sharing 14.8 L):**
Using approximate T/S: Fs ~65 Hz, Qts ~0.44, Vas ~4.5 L each
- Effective Vas for parallel pair: 9.0 L
- Qtc = 0.44 × sqrt(1 + 9.0/14.0) = 0.44 × 1.28 = **0.56**
- Sealed F3 ≈ 105 Hz (irrelevant — HPF crossover at 400 Hz dominates)
- **Flat, well-controlled response through the 400–2500 Hz operating band**

### 9.8 Why 2 Dividers (Not 4)?

A simpler 2-divider design (3 chambers) is recommended over 4 dividers (5 chambers):

| Approach       | Dividers | Chambers | Pros                     | Cons                   |
|----------------|----------|----------|--------------------------|------------------------|
| **2 dividers** | 2        | 3        | Simpler build, proven    | Shared mid volume      |
| 4 dividers     | 4        | 5        | Full isolation per driver | Complex, tight spacing |

- The mid/tweeter shared volume is standard in MTM and WMTMW designs
- The tweeter (H2606/9200) has a sealed back — it does not interact with the shared volume
- Both mids play the same signal in parallel — back-radiation reinforcement, not interference
- Acoustic foam between the mids eliminates standing waves in the shared cavity
- Commercial WMTMW in-walls (JBL, Revel, KEF) all use this approach

### 9.9 Cross-Section (Side View — Depth)

```
    Room side                              Back of wall
    ←────────────── 5.50" ──────────────→

    ┌────┬─────────────────────────┬────┐
    │    │                         │    │
    │ B  │     D R I V E R         │ B  │
    │ A  │     [══════D══════]     │ A  │
    │ F  │      ↑ 2.44" max        │ C  │
    │ F  │                         │ K  │
    │ L  │     1.56" clearance     │    │
    │ E  │     (air + polyfill)    │ P  │
    │    │                         │ A  │
    │ 3  │                         │ N  │
    │ /  │                         │ E  │
    │ 4  │  Crossover: internal    │ L  │
    │ "  │  on back panel (final)  │    │
    │    │  or external (proto)    │ 3  │
    │    │                         │ /  │
    │    │                         │ 4  │
    │    │                         │ "  │
    └────┴─────────────────────────┴────┘
    0.75"         4.25"             0.50"
```

### 9.10 Divider Construction Detail

Each divider is a rectangular piece of 1/2" MDF cut to fit the full internal
cross-section (13.25" × 4.25"). It seals against the front baffle, back panel,
and both side panels.

```
    DIVIDER (top view, looking down):

    ┌──────────────────────────────────────┐  ← Front baffle
    │                                      │
    │  ┌────────────────────────────────┐  │
    │  │                                │  │
    │  │   1/2" MDF DIVIDER             │  │  13.25" wide × 4.25" deep
    │  │   glued + caulked to all       │  │
    │  │   four surrounding surfaces    │  │
    │  │                                │  │
    │  └────────────────────────────────┘  │
    │                                      │
    └──────────────────────────────────────┘  ← Back panel

    Side →                           ← Side
```

**Critical:** Notch each divider around the driver cutout on the front baffle.
The divider sits behind the baffle at the height between two driver cutouts.
Since the cutout gap is ~1.5", and the divider is 0.5" thick, there is ~0.5"
clearance on each side of the divider to the nearest cutout edge.

### 9.11 Internal Bracing

The enclosure panels will resonate if left unsupported. The two dividers already
break the 45.0" internal height into three shorter sections, but each section
still has unsupported back and side panel spans that need bracing.

**Bracing strategy: horizontal battens + front-to-back ties**

```
    WOOFER CHAMBER (top view, looking down — each woofer chamber identical):

    ┌──────────────────────────────────────┐  ← Front baffle (3/4")
    │                                      │
    │  ┌──┐                          ┌──┐  │
    │  │  │  ← front-to-back tie →   │  │  │  2× MDF blocks (3/4" × 3/4" × 4.25")
    │  │  │  glued to baffle + back   │  │  │  positioned left + right of driver
    │  └──┘                          └──┘  │  (must clear woofer cutout + magnet)
    │                                      │
    │  ════════════════════════════════════ │  ← horizontal batten on back panel
    │                                      │     (3/4" × 3/4" × 13.25")
    └──────────────────────────────────────┘  ← Back panel (1/2")

    Side →                           ← Side


    MID/TWEETER CHAMBER (top view, looking down):

    ┌──────────────────────────────────────┐  ← Front baffle (3/4")
    │                                      │
    │  ┌──┐                          ┌──┐  │
    │  │  │  ← front-to-back tie →   │  │  │  2× MDF blocks (3/4" × 3/4" × 4.25")
    │  │  │  between tweeter and      │  │  │  positioned between mid and tweeter
    │  └──┘  each mid cutout         └──┘  │  cutouts (there are 2 gaps to brace)
    │                                      │
    └──────────────────────────────────────┘  ← Back panel (1/2")

    NOTE: Acoustic foam on the back + side walls already provides damping in
    this chamber. The front-to-back ties couple the 3/4" baffle to the
    1/2" back panel for maximum rigidity.
```

**Bracing cut list (per speaker):**

| Piece | Size | Qty | Location |
|-------|------|-----|----------|
| Back panel batten | 3/4" × 3/4" × 13.25" | 2 | Center of each woofer chamber back panel |
| Front-to-back tie | 3/4" × 3/4" × 4.25" | 6 | 2 per chamber, flanking driver cutouts |

**Placement rules:**
- Back panel battens: center vertically in each woofer chamber (~7.35" from
  divider/panel edge). Glue flat against the inside of the back panel. This
  breaks the back panel's longest unsupported span in half.
- Front-to-back ties: glue between the front baffle and back panel, positioned
  to avoid driver cutouts and magnets. Minimum 1" clearance from any cutout
  edge. These tie the 3/4" baffle to the 1/2" back panel.
- In the woofer chambers: place ties at roughly 3" and 10" from the left edge
  (symmetrically flanking the woofer cutout, which is centered at 6.375").
- In the mid/tweeter chamber: place ties in the gaps between the tweeter and
  each mid cutout, offset to clear the driver magnets.

**Why this works:**
- The dividers are the primary bracing — they break all four long panels
  into 14-16" sections
- The back panel battens halve the remaining unsupported spans
- The front-to-back ties couple the 3/4" baffle to the 1/2" back panel,
  creating an extremely rigid sandwich structure
- Combined with damping material, panel resonances are pushed above the
  audible range or sufficiently damped to be inaudible

### 9.12 Damping & Stuffing

Proper stuffing is critical for both sound quality and effective volume.

**Woofer chambers (each independently):**
```
    Material:   Polyester polyfill (loose)
    Fill level: ~50% by volume (loosely stuffed, not packed)
    Effect:     Increases effective volume by ~15-20%
                (~12.4 L net behaves like ~14.9 L with polyfill)
                Lowers Qtc from ~0.75 to ~0.70 (ideal Butterworth)
    Purpose:    Absorbs standing waves between back panel and baffle
                Damps the sealed box impedance peak
                Reduces internal reflections that color the sound
    
    Application:
    - Pull apart the polyfill into loose, fluffy clouds
    - Distribute evenly throughout the chamber
    - Do NOT pack tightly — air must flow through the fibers
    - Keep clear of the driver cutout (don't block the cone's excursion)
    - Approximately 1 standard bag (12 oz) per woofer chamber
```

**Mid/tweeter chamber:**
```
    Material:   1" acoustic foam (open-cell) OR 1" polyester felt
    Coverage:   Back panel + both side walls + top/bottom of this chamber
    Purpose:    Absorbs standing waves (the 16" height creates a ~425 Hz
                standing wave that falls right in the midrange operating band)
                Prevents reflections back through the mid cones
    
    Application:
    - Cut foam/felt to fit and glue (spray adhesive) to:
      • Entire back panel inside this chamber
      • Both side walls inside this chamber
      • Top surface of divider 1 (chamber floor)
      • Bottom surface of divider 2 (chamber ceiling)
    - Do NOT cover the front baffle area (drivers mount there)
    - Do NOT block the front-to-back ties (glue foam around them)
    - Optionally add a small amount of loose polyfill in the remaining
      air space (~25% fill) for additional absorption
```

**Tweeter note:** The H2606/9200 has a sealed back chamber — it does not
interact with the shared mid/tweeter volume. No special damping treatment
is needed for the tweeter beyond what's already in the chamber.

### 9.13 Construction Details Summary

| Element          | Material       | Thickness | Notes                                  |
|------------------|----------------|-----------|----------------------------------------|
| Front baffle     | MDF            | 3/4"      | L/R side rabbet; driver recesses; flush w/ drywall |
| Back panel       | MDF            | 1/2"      | Sealed, PL Premium + brad nails        |
| Side panels      | MDF            | 1/2"      | Line the stud cavity; short span = stiff |
| Top/bottom       | MDF            | 3/4"      | Sealed                                 |
| Internal dividers| MDF            | 1/2"      | 2× horizontal shelves, glued + caulked |
| Back battens     | MDF            | 3/4"×3/4" | 2× horizontal, one per woofer chamber  |
| Front-to-back ties| MDF           | 3/4"×3/4" | 6× blocks tying baffle to back panel   |
| Damping (woofer) | Polyfill       | —         | ~50% fill, ~12 oz per chamber          |
| Damping (mids)   | Acoustic foam  | 1"        | Back + sides + floor + ceiling of chamber |
| Sealing          | PL Premium + caulk | —     | All joints PL Premium + silicone bead  |
| Driver mounting  | T-nuts         | —         | Pressed into baffle back at all holes  |

### 9.14 Sealed Design Rationale

For in-wall speakers with dedicated subwoofers:
- **Sealed** is simpler, more predictable, better transient response
- No port = no port noise, no port tuning complexity, no depth penalty
- The subwoofer handles everything below 50–70 Hz
- Woofers play cleanly from the sub crossover point (~60 Hz) up to ~400 Hz
- With polyfill, the sealed alignment (Qtc ≈ 0.70) gives ideal Butterworth
  response, with F3 ≈ 63 Hz

### 9.15 Enclosure Height — Measure First, Then Size

> **The enclosure height should be finalized AFTER measuring the actual
> drivers with DATS V3.** Published T/S parameters are typical values;
> your drivers may differ by ±10–15%. This changes the optimal volume.

**Workflow:**
1. Order drivers (2× SB17MFC35-8 for prototype)
2. Measure free-air T/S with DATS V3 → actual Fs, Qts, Vas
3. Calculate optimal Vb for Butterworth (Qtc = 0.707 with polyfill):
   `Vb_physical = Vas / ((0.707 / Qts)² − 1) / 1.2`
4. Add back bracing displacement (~0.2 L) and driver displacement (~0.2 L):
   `Vb_gross = Vb_physical + 0.4 L`
5. Calculate chamber height: `height = Vb_gross / 0.869 L per inch`
6. Calculate enclosure height: `2 × chamber_height + 17.09" + 1.50"`

**How actual Qts affects enclosure height:**

| Actual Qts | Need Vb (physical) | Chamber height | Enclosure height |
|------------|-------------------|----------------|-----------------|
| 0.35       | 11.0 L            | 12.6"          | ~44"            |
| **0.37**   | **12.7 L**        | **14.6"**      | **~48"**        |
| 0.40       | 15.7 L            | 18.1"          | ~55"            |

The mid/tweeter section (16.08") and dividers (1.00") are fixed by driver
spacing. Only the woofer chamber heights flex with the measurement data.

> **Back panel thickness as adjustment variable:** The back panel is currently
> now 1/2" MDF (changed from 3/4" to gain internal depth). This increased
> internal depth from 4.00" to 4.25", adding ~6% more volume per chamber,
> which compensated for the height reduction (49.50" baffle → 48.00" to fit
> 4' MDF stock) and preserved the Butterworth sealed alignment.

**Height vs. alignment trade-offs (with polyfill):**

| Enclosure | Woofer chamber | Qtc w/ fill | F3     | Character              |
|-----------|---------------|-------------|--------|------------------------|
| 48"       | 14.7"         | 0.70        | ~63 Hz | Ideal Butterworth      |
| 46"       | 13.7"         | 0.72        | ~63 Hz | Very good              |
| 44"       | 12.7"         | 0.74        | ~63 Hz | Acceptable, slight warmth |
| 42"       | 11.7"         | 0.77        | ~64 Hz | Mild bass bump          |
| 40"       | 10.7"         | 0.80        | ~64 Hz | Getting boomy           |

> F3 is remarkably stable (~63 Hz) because Fc and Qtc effects cancel
> near Butterworth. The trade-off is bass *quality*, not extension.

---

## 10. Output & Sensitivity Estimates

### System Sensitivity (In-Wall, Half-Space)

| Section     | Sensitivity (2.83V/1m) | With wall loading | Notes                    |
|-------------|------------------------|-------------------|--------------------------|
| Woofer pair | ~84 dB                 | ~90 dB            | +6 dB half-space at LF   |
| Mid pair    | ~82 dB                 | ~85 dB            | +3 dB half-space         |
| Tweeter     | ~95 dB (native)        | ~85 dB (padded)   | L-pad brings to match    |
| **System**  |                        | **~87–88 dB**     | **Balanced across band** |

### SPL at Listening Position (9 feet / 2.7 m)

| Condition              | SPL at seat |
|------------------------|-------------|
| 1 watt (2.83V)         | ~78–79 dB   |
| 10 watts               | ~88–89 dB   |
| 50 watts               | ~95–96 dB   |
| 125 watts (continuous) | ~99–100 dB  |
| Peak (short-term)      | ~105–106 dB |

> **For home theater reference level:** Dialog normalization targets ~85 dB with peaks to
> 105 dB. With subwoofers handling bass, these speakers comfortably reach reference levels
> at your 9-foot listening distance.

---

## 11. Off-Axis & Lobing Analysis

### 11.1 Your Listening Geometry

```
    135" projector screen
    ┌─────────────────────────────────────────────────┐
    │                                                 │
    L                      C                          R
    ↑                      ↑                          ↑
    speaker                speaker                    speaker
    │←──── ~6 ft ────→│                    │←── ~6 ft ──→│
    │                      │                          │
    │                      ↓ ~9-10 ft                 │
    │                                                 │
    │                  [LISTENER]                      │
    │                  (center seat)                   │
    │                                                 │
    │  ← ~30° angle ──→│                              │
```

- Center channel: **on-axis** (0° horizontal)
- Left/Right channels: **~30° horizontal off-axis**
- Vertical: **~0°** (tweeter at ear height)

### 11.2 The Critical Distinction: Horizontal vs Vertical Off-Axis

**The WMTMW vertical driver array ONLY creates lobing in the VERTICAL plane.**
It does NOT affect horizontal dispersion at all. This is fundamental physics:
comb filtering between two sources only occurs in the plane containing both
sources. Since the mids are stacked VERTICALLY, the comb filtering is VERTICAL.

```
    VERTICAL PLANE (side view):        HORIZONTAL PLANE (top view):

         M ─── lobing here              M
         │     (floor/ceiling)          ─┼─ no lobing here
         T                              T   (single point source
         │                              ─┼─  at each frequency)
         M ─── lobing here              M
```

**At your 30° horizontal off-axis L/R listening angle, the dual midranges
behave as a SINGLE point source.** There is zero comb filtering horizontally
from the WMTMW arrangement. The horizontal response is determined ONLY by
each individual driver's own directivity characteristics.

### 11.3 Horizontal Off-Axis Response at 30° (L/R Speakers)

At each frequency, only one driver section is active. Here is the expected
horizontal response at 30° for each section individually:

| Frequency Range | Active Driver(s)     | Driver Size | Behavior at 30°             |
|-----------------|----------------------|-------------|-----------------------------|
| 50 – 400 Hz     | Woofer pair (6.5")  | 171 mm      | Omnidirectional, <1 dB down |
| 400 – 1000 Hz   | Mid pair (5")       | 137 mm      | ~1 dB down (wide pattern)   |
| 1000 – 2000 Hz  | Mid pair (5")       | 137 mm      | ~2 dB down (mild narrowing) |
| 2000 – 2500 Hz  | Mid pair (5")       | 137 mm      | ~3 dB down (transitional)   |
| 2500 – 5000 Hz  | Tweeter (horn 26mm) | 104mm horn  | ~2–3 dB down (controlled)   |
| 5000 – 10000 Hz | Tweeter (horn 26mm) | 104mm horn  | ~4–6 dB down (narrowing)    |
| 10000 – 20000 Hz| Tweeter (horn 26mm) | 104mm horn  | ~6–10 dB down (beaming)     |

**Key takeaway:** At 30° horizontal, the overall response is ~2–4 dB quieter
in the upper frequencies. This is NORMAL for ALL speakers (including $20k+
commercial in-walls) and is expected behavior at the L/R listening position.

### 11.4 Why the Crossover Transition Matters Most

The most critical point for off-axis performance is the **directivity match at
the crossover frequency** (~2500 Hz). At this frequency:

- The 5" midrange is ~3 dB down at 30° horizontal (beginning to beam)
- The horn-loaded H2606/9200 tweeter is ~2–3 dB down at 30° (horn controls it)
- **These match within ~1 dB** → smooth off-axis response through the crossover

This directivity matching at crossover is EXACTLY what made the Mechano23
exceptional. Amir specifically praised the "nearly perfect directivity matching"
between the SB13PFC and H2606/9200 in his ASR review. We are using the same
driver combination, so we inherit this same smooth off-axis transition.

### 11.5 What Your Ears Actually Hear at 30°

1. **Direct sound:** ~2–3 dB less treble energy than on-axis. Your brain
   perceives this as a very slightly warmer tonal balance.

2. **Room reflections:** Contribute significantly to perceived tonality. The
   reflections fill in the frequency response, partially compensating for
   the direct sound reduction.

3. **AVR room correction:** Audyssey, Dirac, YPAO, or similar will measure
   the actual in-room response at your seat and apply EQ to compensate for
   level differences between L, C, and R. This is standard practice and
   works extremely well.

4. **Net result:** After room correction, the L/R speakers will sound
   essentially identical to the center channel at your listening position.
   The tonal match between all three will be excellent because they use the
   same drivers and crossover topology.

### 11.6 Vertical Lobing (Dual Midranges)

Two midranges spaced 10.50" (267 mm) apart center-to-center create vertical
interference patterns. This is a property of ALL multi-driver speakers.

| Vertical Angle | First Null Frequency | In Midrange Band? | Effect              |
|----------------|---------------------|--------------------|---------------------|
| 0° (on-axis)   | None                | No — perfect sum   | Ideal response      |
| 10°            | ~3,700 Hz           | No — above band    | Negligible          |
| 15°            | ~2,480 Hz           | Borderline         | Mids rolling off    |
| 30°            | ~1,280 Hz           | Yes                | Reduces reflections |
| 45°            | ~  910 Hz           | Yes                | Reduces reflections |

### 11.7 Why Vertical Lobing Is Actually Beneficial

1. **You are at 0° vertical.** Seated at 9 feet with the tweeter at ear
   height, you are at 0° vertical for all three L/C/R speakers. The direct
   sound is unaffected by vertical lobing.

2. **L/R speakers at ~30° horizontal are still at ~0° vertical.** Your
   horizontal off-axis angle does NOT introduce vertical off-axis. The
   vertical angle depends on height difference, not horizontal position.

3. **Lobing reduces floor/ceiling reflections.** The vertical nulls at 30°+
   actually IMPROVE clarity by reducing energy bouncing off the floor and
   ceiling before reaching your ears. This is a well-documented benefit of
   vertically-arrayed designs.

4. **Industry standard.** Every high-end in-wall (JBL Synthesis SCL, Revel
   W553L, KEF Ci5160RL) uses this configuration and accepts this tradeoff.

5. **Room treatments will help.** You plan to add treatments later, which
   will further reduce any reflected lobing artifacts.

6. **Crossover design mitigates.** The midranges naturally roll off above
   2.5 kHz, reducing their contribution at frequencies where the first null
   appears at moderate vertical angles.

### 11.8 Is Off-Axis Performance a Problem for These Drivers?

**No.** Specifically:

| Concern                           | Assessment | Why                              |
|-----------------------------------|------------|----------------------------------|
| Horizontal lobing from WMTMW      | **None**   | Vertical array = no H comb       |
| 30° H off-axis for L/R            | **Normal** | All speakers behave this way     |
| Directivity match at crossover    | **Good**   | Same driver pairing as Mechano23 |
| Vertical lobing from dual mids    | **Managed**| Benefits > costs for seated HT   |
| Timbre change at 30° horizontal   | **Minor**  | AVR room correction compensates  |
| Worse than commercial alternatives| **No**     | Same physics, same tradeoffs     |

### 11.9 Time Alignment (Driver Acoustic Center Offset)

The three driver types have different mounting depths, meaning their acoustic
centers (where sound effectively originates) are at different distances behind
the baffle face. At crossover frequencies where two drivers overlap, a path
length difference creates a phase offset that affects summation.

**Mounting depths and acoustic centers (from baffle front face):**

| Driver          | Mount depth | Acoustic center* | Offset from tweeter |
|-----------------|-------------|-------------------|---------------------|
| SB17MFC35-8     | 62 mm / 2.44" | ~50 mm / 2.0"  | ~38 mm / 1.5" back  |
| SB13PFCR25-08   | 55 mm / 2.17" | ~40 mm / 1.6"  | ~28 mm / 1.1" back  |
| H2606/9200      | 22 mm / 0.87" | ~12 mm / 0.5"  | 0 (reference)       |

*Acoustic center ≈ voice coil plane for cone drivers (roughly 70–80% of
mounting depth). The H2606/9200 is horn-loaded — the dome sits at the horn
throat, recessed inside the waveguide. Its acoustic center at crossover
frequencies is near the throat, much closer to the baffle face than the
mounting depth suggests (~10–15 mm, not 22 mm). Exact values are frequency-
dependent and will come from impulse response measurements.

**Phase impact at crossover frequencies:**

| Crossover  | Drivers overlapping | Offset  | Wavelength | Phase shift |
|------------|---------------------|---------|------------|-------------|
| ~400 Hz    | Woofer → Mid        | ~10 mm  | 860 mm     | ~4°         |
| ~2500 Hz   | Mid → Tweeter       | ~28 mm  | 137 mm     | ~74°        |

The 400 Hz crossover is a non-issue — 4° of phase offset is negligible.

The 2500 Hz crossover has a meaningful ~74° offset. However, this is
**within the range that the crossover network can compensate.** An LR4
crossover already manages 360° of phase rotation across the passband; an
additional ~74° is absorbed by adjusting component values. VituixCAD
handles this automatically when you feed it real impulse response data.

**Physical correction options (if needed after VituixCAD modeling):**

1. **Do nothing (likely outcome).** The crossover compensates electrically.
   This is what most commercial WMTMW designs do, including the JBL SCL-3
   and Revel W553L. It works because LR4 slopes are steep enough that the
   ~74° offset only matters in a narrow overlap band.

2. **Recess the tweeter.** Mill a ~1.1" (28 mm) pocket into the 3/4" baffle
   at the tweeter location, pushing the tweeter forward relative to the mids.
   This physically aligns mid and tweeter acoustic centers.
   - Pro: eliminates the offset at the source
   - Con: 3/4" baffle is only 19 mm — a 28 mm recess would go all the way
     through and then some. **Not physically possible** without a double-
     thickness baffle or sub-baffle approach.
   - Even a partial recess (the full 3/4" / 19 mm) would only correct ~68%
     of the offset — meaningful but incomplete.

3. **Add a tweeter sub-baffle.** Glue a ~1.1" (28 mm) MDF spacer (with
   chamfered or radiused edges) behind the tweeter cutout, bringing the
   tweeter mounting surface forward. The tweeter would protrude ~1.1" from
   the main baffle plane. This avoids the diffraction step of a recess,
   but creates a significant bump on the baffle and may interfere with
   the adjacent midranges (only 20 mm clearance to mid faceplates).

4. **Digital time alignment (active crossover only).** With a MiniDSP or
   similar DSP processor running an active crossover (separate amplifier
   channel per driver section), per-band delay is straightforward (~0.08 ms
   on the tweeter channel for 28 mm). **This is NOT available with the
   passive crossover in this design** — a single amplifier channel feeds
   the whole speaker, so there is no way to selectively delay only the
   tweeter. Would require converting to a fully active topology.

**Recommendation: defer to crossover design phase.** Do NOT modify the baffle
for time alignment until you have real measurement data in VituixCAD. The
tool will show you the actual phase response of each driver in the enclosure,
and the optimizer will find component values that achieve proper summation
including the physical offset. Only if VituixCAD cannot achieve a smooth
summed response should you consider physical corrections — and in practice,
~28 mm at 2.5 kHz is at the upper end of what passive crossovers handle
but still feasible, especially with steep LR4 slopes limiting the overlap
band. The physical options are constrained by the tight driver spacing.

---

## 12. Timbre Matching Strategy

### Driver Family Across the System

| Speaker          | Tweeter              | Midrange / Woofer      | Match? |
|------------------|----------------------|------------------------|--------|
| **Mechano23**    | Scan-Speak H2606/9200 | SB Acoustics SB13PFCR25-4 | —  |
| **(sides/rears)**|                      |                        |        |
| **WMTMW LCR**   | Scan-Speak H2606/9200 | SB Acoustics SB13PFCR25-08 | Yes |
| **(this design)**| *(same tweeter)*     | *(same driver, 8Ω ver.)* |      |
| **Atmos**        | Scan-Speak H2606/9200 | SB Acoustics SB13PFCR25   | Yes |
| **(future)**     | *(same tweeter)*     | *(same driver)*          |      |

The 4 Ω and 8 Ω versions of the SB13PFCR25 are acoustically identical — same cone, surround,
spider, and motor topology. Only the voice coil winding differs. There is no audible difference
in the midrange operating band.

**Result:** Your entire 7.x.4+ speaker system will share the same tweeter and midrange driver
family, ensuring cohesive timbre across all channels.

---

## 13. Risk Assessment

| Risk                                | Level       | Mitigation                                           |
|-------------------------------------|-------------|------------------------------------------------------|
| Crossover design complexity         | **Medium**  | VituixCAD + DATS V3 + UMIK-1. Step-by-step guidance. |
| Driver breakup resonances           | **Low**     | Paper and poly cones have well-damped breakups.       |
| Vertical lobing from dual mids      | **Low**     | Only vertical plane. Horizontal off-axis unaffected.  |
| L/R off-axis at 30° horizontal      | **Very Low**| Normal for all speakers. AVR correction compensates.  |
| In-wall depth constraint            | **Very Low**| All drivers confirmed to fit with 1.5"+ margin.      |
| Timbre mismatch with Mechano23      | **Very Low**| Same tweeter, same midrange driver (8Ω variant).      |
| Budget overrun                      | **Very Low**| $273/spk drivers, $600 budget = $327 for xover/hw.   |
| Driver stock / availability         | **Low**     | All drivers confirmed IN STOCK at Madisound.          |
| Crossover iteration taking too long | **Medium**  | Start with one prototype. Measure, iterate, replicate.|
| Driver time alignment (mid→tweeter) | **Low-Med** | ~74° at 2.5 kHz — LR4 crossover can compensate. See 11.9.  |
| Woofer Qts above published specs    | **Low**     | Measured Qtc 0.69–0.73 in box — still Butterworth. No changes needed. |
| Woofer Mms above published specs    | **Low**     | Validated by mid measurements. Alignment works with measured values. |

### Honest Bottom Line

> The chance of building a great-sounding speaker is **high**. The Mechano23 drivers are
> ASR-proven performers. Scaling them to a 3-way WMTMW with proper measurement-based crossover
> design is well-trodden ground. The main effort is in the crossover development — plan for
> 2–4 iterations to get it dialed in.

---

## 14. Build Process — Step by Step

### Strategy: Prototype First

Build ONE speaker first to validate the enclosure and develop the crossover.
The prototype uses an external crossover (accessible from the unfinished room
behind the wall) with individual driver cables routed out the top. Final
speakers get an internal crossover with binding post cup.

### Phase 1: Procurement (Prototype Only)

```
Step 1 ─── Order prototype drivers from Madisound:
           • 2× SB17MFC35-8    (woofers for prototype)
           Optionally use existing Mechano23 mid (4Ω) + tweeter for testing.
           
Step 2 ─── Order MDF: two 4×8 sheets of 3/4" (box + baffle) and one 4×8 sheet of 1/2" (dividers)

Step 3 ─── Order hardware: T-nuts (M4, qty 20+), foam gasket tape,
           16 AWG wire, polyfill, acoustic foam, PL Premium adhesive,
           18ga brad nails (1.5" and 1"), silicone caulk
```

### Phase 2: Cut

```
Step 4 ─── Cut 3/4" MDF panels (baffle, top, bottom):
           • Front baffle:    16.00" × 48.00"  (×1)
           • Top panel:       14.25" × 4.75"   (×1)
           • Bottom panel:    14.25" × 4.75"   (×1)

Step 5 ─── Cut 1/2" MDF panels:
           • Back panel:      14.25" × 48.00"  (×1)
           • Side panels:      4.75" × 46.50"  (×2)  ← fits between top + bottom panels
           • Divider 1:       13.25" × 4.25"   (×1)
           • Divider 2:       13.25" × 4.25"   (×1)

Step 5b ── Cut 3/4" MDF bracing pieces:
           • Back panel battens:   3/4" × 3/4" × 13.25"  (×2)
           • Front-to-back ties:   3/4" × 3/4" × 4.25"   (×6)

Step 6 ─── Route baffle side rabbet (back face):
           1/4" deep × 1" wide on left and right edges only
           (Router table + straight bit + fence)

Step 6b ── Cut driver holes in front baffle:
           • 2× 149mm (5.87") holes for woofers
                (centers at 12.00" and 36.00" from bottom, 8.00" from sides)
           • 2× 116mm (4.57") holes for midranges
                (centers at 18.75" and 29.25" from bottom, 8.00" from sides)
           • 1× 72mm (2.83") hole for tweeter
                (center at 24.00" from bottom, 8.00" from sides)
           NOTE: "from bottom" means from baffle bottom edge (flush with box bottom)

Step 6c ── Route driver recesses (front face):
           ~3mm (1/8") deep to frame OD at each driver position
           (Router + circle jig or MDF template per driver size)

Step 7 ─── Drill mounting screw holes per driver templates
           Press T-nuts into back of baffle at all mounting holes

Step 8 ─── Drill wire pass-through holes in dividers:
           2× 1/2" holes per divider (for woofer cables)

Step 9 ─── Drill cable exit holes in top panel:
           (Prototype) 3× 1/2" holes for cables to external crossover
           (Final)     1× binding post cup hole in back panel
```

### Phase 3: Dry Fit

```
Step 10 ── Dry-assemble box (no glue) — verify all panels align squarely
Step 11 ── Test-fit drivers in baffle — confirm cutouts and screw holes
Step 12 ── Verify divider positions: 14.96" and 31.54" from bottom (inside)
Step 13 ── Mark divider SLOT LINES on side panels (both bottom and top of
           each divider, not just center):
             Divider 1: 14.71" (bottom surface) and 15.21" (top surface)
             Divider 2: 31.29" (bottom surface) and 31.79" (top surface)
           Mark on both side panels while they are still accessible.
           Drop the divider into this slot during assembly — rest it on the
           lower line, confirm it seats flush against the back panel face.
Step 13b── Dry-fit each divider: confirm it sits flush with the back panel
           face. Any gap will create an air leak between chambers. Check
           with finger and straight edge from open top and front. Fix fit.
Step 14 ── Mark bracing positions (front-to-back tie locations, batten positions)
Step 14b── Cut cardboard template of baffle hole pattern. Test-fit against
           box opening to confirm F-B tie positions clear all driver cutouts
           by ≥1" before installing ties. Mid/tweeter chamber gap is tight —
           verify each tie position visually with the template.
```

### Phase 4: Glue Box (without front baffle)

```
    All structural joints get PL Premium polyurethane adhesive + 18ga brad nails.
    PL Premium bonds MDF end grain better than PVA wood glue. Brad nails
    hold alignment while adhesive cures (24h) without splitting MDF.
    The box is assembled as an open-front box first. The front baffle goes
    on LAST after all internal work (wiring, bracing, stuffing) is complete.

Step 15 ── BEFORE assembling the box, glue back panel battens to the back
           panel while it is still flat and fully accessible:
           • Position battens at the vertical midpoint of each woofer chamber
             (~7.35" above/below the divider lines marked in step 13)
           • Apply PL Premium, press in place
           • Shoot 1" brads through the back panel FACE (outside) into each
             batten end-grain to lock position during cure
           This is far easier than reaching into a 13.25" × 4.25" box.

Step 16 ── Apply PL Premium bead to joint, press back panel to bottom panel
           Shoot 1.5" 18ga brads every 4-6" to lock alignment

Step 17 ── Glue both side panels to back + bottom
           *** SQUARENESS CHECK: before shooting brads, measure both
           diagonals (corner to corner) of the open box. They must be equal.
           Rack the assembly on a flat surface until diagonals match, then
           nail. A racked box cannot be fixed after cure. ***

Step 18 ── Install divider 1: rest on lower slot line (14.71" from bottom)
           *** Run woofer cable through divider hole BEFORE gluing ***
           Glue, press flush to back panel, brad through sides into divider edges.
           Seal cable hole with silicone.

Step 19 ── Install divider 2: rest on lower slot line (31.29" from bottom)
           *** Run woofer cable through divider hole BEFORE gluing ***
           Same process.

Step 20 ── Glue top panel to sides + back
Step 21 ── Let cure 24 hours
```

### Phase 5: Seal + Brace + Damp + Wire (all internal work before baffle)

```
    *** THIS IS THE LAST CHANCE TO ACCESS THE INTERIOR ***
    Everything below must be done before the front baffle is glued on.

Step 22 ── Seal all internal joints with PL Premium fillet or silicone bead
Step 23 ── Seal wire pass-throughs in dividers with silicone (around wires)

Step 24 ── Install front-to-back ties:
           • 2× in each woofer chamber (flanking driver cutout positions)
           • 2× in mid/tweeter chamber (in gaps between driver positions)
           • Verify positions against cardboard template (Step 14b) — each
             tie must clear all driver cutouts by ≥1". Mid/tweeter gap is
             tight; measure before committing.
           • Glue front face flush with box opening, back end against back panel
           • Shoot 1" brads through back panel FACE (outside) into each tie
             end-grain to lock alignment during cure
           — the baffle will glue to the front faces when applied
           
Step 25 ── Woofer chambers: stuff with polyfill (~50% fill, ~12 oz each)
           Pull apart into fluffy clouds, distribute evenly, don't pack

Step 26 ── Mid/tweeter chamber: glue 1" acoustic foam to:
           • Back panel (inside this chamber)
           • Both side walls (inside this chamber)
           • Top surface of divider 1 (floor of this chamber)
           • Bottom surface of divider 2 (ceiling of this chamber)
           Cut foam around the front-to-back ties
           Optionally add small amount of loose polyfill (~25% fill)

Step 27 ── Route driver cables:
           (Prototype) Each driver gets its own labeled 2-conductor cable
           • Lower woofer cable already through divider 1 → exits top
           • Upper woofer cable already through divider 2 → exits top
           • Lower mid, tweeter, upper mid cables route within mid/tweeter
             chamber → exit through top panel holes
           (Final build) Route all cables to crossover mount point on
           back panel. Install crossover board + binding post cup now.

Step 28 ── VERIFY everything is in place:
           □ All joints sealed
           □ All bracing glued and cured
           □ All stuffing/foam installed
           □ All cables routed and tested for continuity
           □ (Final build) Crossover installed and connected
           □ Nothing is rattling or loose inside
```

### Phase 6: Glue Front Baffle + Mount Drivers

```
    *** POINT OF NO RETURN — interior is permanently sealed ***

Step 28b── Pre-mark divider positions on the FRONT FACE of the baffle before
           spreading any glue. Transfer the slot positions from the side panel
           marks (use a square off the baffle side edges):
             Divider 1 top surface: 15.21" from baffle bottom → draw line
             Divider 2 top surface: 31.79" from baffle bottom → draw line
           These are your blind brad lines — once PL is spread you cannot
           see the divider edges. Shooting brads blind into a 1/2" edge over
           a 48" span is how brads miss; pre-marking eliminates the guesswork.

Step 29 ── Apply PL Premium to the front edges of: side panels, top panel,
           bottom panel, both dividers, and all front-to-back tie ends
Step 30 ── Press front baffle onto box, align carefully
           Shoot 1.5" 18ga brads along the pre-marked divider lines + around
           the full perimeter
           Ensure divider edges and tie ends make contact with the baffle
Step 31 ── Let cure 24 hours

Step 32 ── Mount drivers into baffle with machine screws into T-nuts
           Use foam gasket tape between every driver flange and baffle
Step 33 ── Connect driver cables to driver terminals (observe polarity!)
           (Prototype: cables exit top, connect to driver terminals from front)
```

### Phase 7: Install In Wall

```
Step 34 ── Cut drywall opening (16.0" × 48.0")
Step 35 ── Install cross stud at bottom of opening (weight support ledge)
Step 36 ── Slide box into wall cavity, rest on cross stud
Step 37 ── Screw baffle flanges into studs and cross studs
           Hardware: #8 × 2" pan-head coarse-thread wood screws
           Pre-drill: 7/64" pilot through flange + into stud, ~1-1/2" deep
           Layout: ~9-10 screws per side stud (6" spacing over 48"),
                   plus 2-3 screws into bottom cross stud = ~20-23 total
           Torque: snug only — stop when head seats on MDF, do not strip
Step 38 ── Route cables over top of enclosure to unfinished room side
Step 39 ── Connect to external crossover board
```

### Phase 8: Driver Measurement

```
    ╔═══════════════════════════════════════════════════════════════╗
    ║  PASS 1: IMPEDANCE (DATS V3)                                ║
    ╚═══════════════════════════════════════════════════════════════╝

Step 40 ── Connect DATS V3 to PC, run calibration with reference resistor

Step 41 ── For each driver (one at a time):
           a) Connect DATS leads to the driver's cable (red = +, black = -)
           b) Driver must be installed in the sealed enclosure
           c) Click "Impedance" → DATS sweeps
           d) Verify: single impedance peak visible
              • Woofer peak: ~55-70 Hz (sealed resonance, Fc ≈ 62-66 Hz)
              • Mid peak: ~100-150 Hz (sealed resonance)
              • Tweeter peak: ~500-800 Hz (sealed dome resonance)
              • Double peak = AIR LEAK — find and fix it
           e) Export as .zma file

           File names:
              lower_woofer_sealed.zma
              lower_mid_sealed.zma
              tweeter_sealed.zma
              upper_mid_sealed.zma
              upper_woofer_sealed.zma

Step 42 ── Compare woofer pair impedance — peaks within 1-2 Hz = good match
           Compare mid pair impedance — same check

    ╔═══════════════════════════════════════════════════════════════╗
    ║  PASS 2: FREQUENCY RESPONSE (REW + UMIK-1)                  ║
    ╚═══════════════════════════════════════════════════════════════╝

Step 43 ── Setup REW:
           • Input device: UMIK-1
           • Load UMIK-1 calibration file (from miniDSP.com, serial-specific)
           • Sample rate: 48 kHz
           • Output: your audio interface or amplifier

Step 44 ── For each driver (one at a time, all others DISCONNECTED):

           Far-field measurement (valid above ~200-300 Hz):
           a) Connect amplifier to ONLY the driver under test
           b) Set amp to moderate level (~80-85 dB at 1m)
           c) Place UMIK-1 at 1 meter, on-axis to tweeter position,
              pointing at the baffle
           d) REW → Measure → sweep (512k samples, 20 Hz–20 kHz)
           e) Export as .frd text file

           Nearfield measurement (for woofers and mids only):
           f) Move UMIK-1 to within 5mm of the driver's dust cap center
              — Almost touching but NOT touching the cone
              — Perpendicular to the cone surface
           g) REW → Measure → sweep (same settings)
           h) Export as separate .frd file

           File names:
              lower_woofer_farfield.frd     lower_woofer_nearfield.frd
              lower_mid_farfield.frd        lower_mid_nearfield.frd
              tweeter_farfield.frd          (no nearfield needed)
              upper_mid_farfield.frd        upper_mid_nearfield.frd
              upper_woofer_farfield.frd     upper_woofer_nearfield.frd

Step 45 ── (Optional but recommended) Repeat far-field at 15° and 30° horizontal
           for each driver. VituixCAD uses off-axis data to optimize the
           crossover for the full listening window.
```

### Phase 9: Crossover Design

```
Step 46 ── Import all .frd and .zma files into VituixCAD:
           • Create driver entries for each driver type
           • Set design axis (on-axis to tweeter, 1m)
           • VituixCAD splices nearfield + farfield automatically

Step 47 ── Set crossover targets:
           • Low pass: ~400 Hz (LR4 acoustic target) → woofer pair
           • Band pass: ~400–2500 Hz → mid pair
           • High pass: ~2500 Hz (LR4 acoustic target) → tweeter
           • Tweeter L-pad: ~10–13 dB attenuation

Step 48 ── Run VituixCAD optimizer → get initial component values

Step 49 ── Review results:
           • Summed frequency response (should be ±2 dB, 50 Hz–20 kHz)
           • Impedance curve (minimum should stay above 3 Ω)
           • Phase response (smooth through crossover regions)
           • Off-axis response (if off-axis data was measured)
           • Power response / directivity index

Step 50 ── Order crossover components based on VituixCAD design:
           • Air-core inductors (woofer section may need iron-core for value)
           • Film capacitors (polypropylene preferred)
           • Power resistors (wire-wound, non-inductive)
```

### Phase 10: Crossover Prototype & Testing

```
Step 51 ── Build crossover on a test board (NOT soldered permanently)
           Use screw terminals or alligator clips for easy component swaps

Step 52 ── Connect crossover to driver cables from prototype speaker
           Connect amplifier input to crossover

Step 53 ── Measure completed speaker with UMIK-1 at 1m:
           • Full-range frequency response
           • Impedance verification (DATS at crossover input)
           • Compare to VituixCAD prediction

Step 54 ── Iterate crossover values as needed:
           • Adjust component values
           • Re-measure
           • Repeat until satisfied (expect 2–4 iterations)

Step 55 ── Listening tests with familiar material at the listening position
```

### Phase 11: Finalize & Replicate

```
Step 56 ── Solder final crossover boards (3 total)
Step 57 ── Order remaining drivers for the other 2 speakers:
           • 4× SB17MFC35-8 woofers
           • 6× SB13PFCR25-08 midranges (or 4 if reusing prototype mids)
           • 2× H2606/9200 tweeters (or 3 if not reusing Mechano23 tweeter)
Step 58 ── Build remaining 2 enclosures (identical to prototype)
           For final speakers: install crossover + binding post cup inside
           the box BEFORE gluing the front baffle (Phase 5, Step 27)
Step 59 ── Install all 3 speakers in wall
Step 60 ── Full system measurement with REW + UMIK-1
Step 61 ── Receiver calibration (Audyssey, Dirac, YPAO, etc.)
```

---

## 15. Required Tools & Software

### Measurement Equipment (Already Owned)

| Tool                | Purpose                                    |
|---------------------|--------------------------------------------|
| UMIK-1              | Frequency response measurement with REW    |
| DATS V3             | Driver impedance and T/S parameter measurement |

### Software (Free)

| Software    | Platform | Purpose                                     | URL                        |
|-------------|----------|---------------------------------------------|----------------------------|
| VituixCAD   | Windows  | Crossover simulation and optimization       | kimmosaunisto.net           |
| REW         | All      | Room and speaker measurement                | roomeqwizard.com            |
| DATS V3 SW  | Windows  | Driver impedance analysis (comes with DATS) | parts-express.com           |

### Woodworking Tools (Already Owned / Standard)

- Table saw or circular saw with guide
- Router (for driver cutouts — optional, jigsaw works too)
- Drill / driver
- Clamps
- Wood glue + caulk gun
- Sandpaper (120, 220 grit)

### Electronics Tools

| Tool                    | Purpose                              | Notes           |
|-------------------------|--------------------------------------|-----------------|
| Soldering iron          | Crossover assembly                   | Already owned   |
| Solder (rosin core)     | Connections                          | 60/40 or lead-free |
| Wire strippers          | Speaker wire prep                    | Standard        |
| Multimeter              | Verify connections, measure resistance | Recommended    |
| Alligator clip leads    | Prototype crossover testing          | ~$5–10          |

---

## 16. Parts Shopping List

### Madisound Order — Drivers (All 3 Speakers)

| Qty | Part Number      | Description                      | Unit Price | Extended  |
|-----|------------------|----------------------------------|------------|-----------|
| 6   | SB17MFC35-8      | SB Acoustics 6.5" Poly, 8Ω      | $75.90     | $455.40   |
| 6   | SB13PFCR25-08    | SB Acoustics 5" Paper, 8Ω       | $36.80     | $220.80   |
| 3   | H2606/9200       | Scan-Speak 26mm Horn Dome, 6Ω   | $47.80     | $143.40   |
|     |                  | **Driver Subtotal**              |            | **$819.60** |

### Hardware (Estimated — Source from Madisound / Parts Express)

| Qty | Item                                    | Est. Price  |
|-----|-----------------------------------------|-------------|
| 3   | Binding post terminal cups (pair)       | $10 ea      |
| 1   | Roll of 16 AWG speaker wire (25 ft)     | $15         |
| 3   | Bags of polyfill (1 lb each)            | $8 ea       |
| 1   | Roll of acoustic damping foam/felt      | $15         |
| 2   | Tubes of PL Premium adhesive            | $8 ea       |
| 1   | Box of 18ga brad nails (1.5" + 1")     | $10         |
| 1   | Tube of silicone caulk                  | $6          |
| 75  | #8 × 2" pan-head coarse wood screws     | $10         |
| 1   | 7/64" drill bit (pilot holes)           | $4          |
| 60+ | T-nuts (M4) for driver mounting         | $8          |
| 3   | Rolls of foam gasket tape (driver flanges)| $6 ea      |
| 1   | Can of spray adhesive (for acoustic foam)| $8          |
|     | **Hardware Subtotal**                   | **~$145**   |

### Crossover Components (Per Speaker — Values TBD After Measurement)

> Exact values will be determined by VituixCAD after driver measurements.
> Budget estimate based on typical 3-way WMTMW crossover complexity.

| Category         | Typical Qty/Speaker | Est. Cost/Speaker |
|------------------|--------------------:|------------------:|
| Air-core inductors | 4–6               | $30 – $50         |
| Film capacitors    | 6–10              | $40 – $70         |
| Power resistors    | 4–8               | $10 – $20         |
| PCB or terminal board | 1              | $5 – $10          |
| **Crossover Subtotal** |                | **$85 – $150**    |

### Grand Total Estimate (All 3 Speakers, Not Including MDF)

| Category              | Cost              |
|-----------------------|-------------------|
| Drivers               | $819.60           |
| Hardware              | ~$145             |
| Crossover components  | $255 – $450       |
| **Grand Total**       | **$1,220 – $1,415** |
| Budget (3 × $600)     | $1,800            |
| **Under budget by**   | **$385 – $580**   |

---

## 17. Reference Information

### The Mechano23 — Foundation for This Design

| Detail              | Value                                                         |
|---------------------|---------------------------------------------------------------|
| Designer            | XMechanik (ASR & diyAudio member)                             |
| Software used       | XMachina (custom crossover optimization tool)                 |
| ASR Review          | Thread #54066 — Rated "Great" (86.7% of voters)              |
| Amir's quote        | *"A masterpiece... I can't think of a more optimized design"* |
| Configuration       | 2-way bookshelf, ported                                       |
| Woofer              | SB Acoustics SB13PFCR25-4                                    |
| Tweeter             | Scan-Speak Discovery H2606/9200                               |
| Crossover point     | ~3.5 kHz, higher-order network                                |
| System sensitivity  | ~83 dB (2.83V/1m) — lower than average                       |
| Key strength        | Nearly perfect directivity matching at crossover              |

### Key Design Principles Applied

1. **Measurement-based design** — No guessing. Every driver measured, every crossover simulated.
2. **Timbre matching** — Same tweeter and midrange driver across all speakers in the system.
3. **In-wall advantages exploited** — No baffle step, half-space loading, wall acts as infinite baffle.
4. **Sealed alignment** — Simpler, more predictable, better transient response (with subwoofer support).
5. **Vertical symmetry** — WMTMW arrangement for consistent L/C/R behavior.
6. **Proven drivers** — ASR-reviewed and community-tested.
7. **Budget discipline** — Premium where it matters (drivers), economical where it doesn't (MDF, hardware).

### Useful Links

| Resource                  | URL / Location                                         |
|---------------------------|--------------------------------------------------------|
| Mechano23 ASR Review      | audiosciencereview.com — Thread #54066                 |
| Mechano23 Design Thread   | audiosciencereview.com — search "Mechano23"            |
| VituixCAD Download        | kimmosaunisto.net                                      |
| REW Download              | roomeqwizard.com                                       |
| Madisound                 | madisoundspeakerstore.com                              |
| Solen                     | solen.ca                                               |
| Meniscus Audio            | meniscusaudio.com                                      |
| diyAudio Forum            | diyaudio.com — Multi-Way section                       |
| AVS Forum DIY             | avsforum.com — DIY Speakers section                    |

---

*Document generated March 2026. All pricing verified from Madisound.*  
*Design to be refined with actual driver measurements during build process.*
