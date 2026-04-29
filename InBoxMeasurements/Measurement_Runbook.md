# WMTMW In-Wall Measurement Runbook

Session runbook for in-box acoustic and electrical characterization of the prototype WMTMW in-wall speaker. Data targets both **LoudspeakerLab** (primary) and **VituixCAD** (secondary) for crossover design.

## Companion tools

| File | Purpose |
|------|---------|
| `Measurement_Runbook.html` | Printable version with SVG diagrams for arc geometry, mic placement, signal chain. Print this for basement use. |
| `sweep_wizard.py` | Python wizard that drives the acoustic-sweep sequence on Windows. Attempts to auto-trigger REW via its HTTP API; falls back to guided-prompt mode if the API is unavailable. Enforces tweeter safety (300 Hz sweep start, 256 k length) and the naming convention below. Logs progress to `sweep_log.csv` for resume after interruption. |
| `measurement_matrix.py`, `rew_api.py`, `prompts.py` | Wizard internals. |

This .md remains the ground-truth reference — every filename, sweep range, and safety rule in the wizard matches what's documented here. If the wizard fails or you prefer fully manual, execute this document top-to-bottom.

**Estimated session time:** 4.5–6 hours including setup and verification.

---

## 0. Tweeter Protection — READ FIRST

The Scan-Speak H2606/9200 voice coil can burn out in **seconds** if driven with low-frequency content at 2.83 V. Every tweeter-related step below exists to prevent that. Do not skip any of them.

| # | Rule | Why |
|---|------|-----|
| 1 | During 2.83 V calibration (Step 6), the **tweeter must be physically disconnected** at the wall. Only the calibration woofer is connected. | 60 Hz sine at 2.83 V into a tweeter destroys it instantly. |
| 2 | For every tweeter sweep, set REW **sweep start frequency to 300 Hz**. Tweeter Fs is ~650 Hz; 300 Hz gives margin but stays well below the intended ~2.5 kHz crossover. | The default 20 Hz sweep start applies full voltage below Fs where excursion peaks. |
| 3 | Use **256 k sweep length** for tweeter, not 512 k. Shorter exposure. | Limits thermal dose. |
| 4 | Tweeter distortion sweeps run at **1 V**, not 2.83 V. Label files `T-Tweeter-Distortion-1V.txt`. | 2.83 V extended stepped sine is thermally punishing. |
| 5 | Before the first tweeter sweep, with the tweeter **disconnected**, run a dry sweep and view REW's generator spectrum. Confirm no content below 300 Hz. Then connect the tweeter. | Catches misconfigured sweep range before it reaches the driver. |
| 6 | **Wear hearing protection** during tweeter sweeps. At 95 dB/2.83 V sensitivity, on-axis SPL is ~95 dB at 1 m for the full sweep duration. | Hearing damage threshold. |
| 7 | If you hear any tick, buzz, or stress during a tweeter sweep, **STOP immediately** and investigate. | Thermal or excursion damage is silent until it isn't. |

**Calibration-woofer convention:** use W2 (lower woofer) as the 2.83 V calibration load. Keep it connected throughout. All other drivers — including the tweeter — are disconnected at the wall during calibration.

---

## 1. Equipment & Signal Chain

**Hardware**

- Laptop running REW (latest)
- UMIK-1 USB mic + its 0° calibration file (downloaded from miniDSP for your serial)
- DATS V3 + laptop USB
- Arcam AVR350 (dedicated to this session)
- Small passive desk speaker (3–4" single driver) — used **only** as acoustic timing reference
- Tripod with boom arm (for 0° clearance) OR standard tripod + plan for 0° workaround
- Digital multimeter (AC V mode)
- Plumb bob (nut on a string)
- Masking tape, sharpie, tape measure, protractor
- 3.5 mm TRS → 2× RCA Y-splitter cable
- Speaker wire for desk-speaker tap to Arcam Front-Left terminal
- Earplugs

**Signal chain**

> **Terminology.** **DUT** = **driver under test** — the single driver currently being measured at the wall plate. Every other driver is physically disconnected. Diagrams use `DUT` as a short label; prose uses "driver under test".

```
Laptop 3.5mm stereo out
   ├── L channel ─RCA─► Arcam 7.1-in "Front Left"   ─► Arcam FL amp ─► Desk speaker (fixed position, timing ref)
   └── R channel ─RCA─► Arcam 7.1-in "Front Right"  ─► Arcam FR amp ─► driver under test (DUT) at wall

UMIK-1 ─USB─► Laptop (REW input)
DATS V3 ─USB─► Laptop (separate sessions, not simultaneous with REW)
```

Arcam source selection: **7.1 Multichannel Input / Direct** (no DSP, no decoder, no bass management).

---

## 2. Measurement Conventions

**Where distance is measured from.** The UMIK-1 acoustic reference point is the **tip of the mic capsule** (the end closest to the source). The distance "1 m" is measured from the **driver's acoustic center** to that **mic tip**. For a cone driver, acoustic center is roughly the center of the cone at the dust cap plane. For the tweeter, it is the center of the dome.

**Mic orientation.** Mic axis points **directly at the driver under test** (0° incidence). Always. Load the **0° calibration file** in REW, not the 90°.

**On-axis reference.** The single design-axis point is **1 m from the tweeter, perpendicular to the baffle, at tweeter height**. This is the origin for every arc.

**One mic position, all drivers.** At each angle, all five drivers are measured from the same mic position (centered on the tweeter arc). This is close enough for crossover design — LoudspeakerLab and VituixCAD both reconstruct the full system from per-driver data plus the baffle layout.

**Channel levels.**
- Laptop L channel = REW timing-reference pilot → desk speaker on Arcam **Front-Left** (REW-attenuated, typically −20 dB)
- Laptop R channel = sweep → driver under test (DUT) on Arcam **Front-Right**, calibrated to 2.83 V
- Arcam volume is **locked** for the entire session after Step 6. Do not touch.

**File-naming convention.** Every saved file uses the pattern `<DriverTag>-<DriverName>-<AngleOrKind>.<ext>`. Angles are zero-padded to 3 digits so files sort numerically. The wizard enforces this automatically; if you save manually in REW, use the same pattern.

| Driver tag | Driver name | Example filename |
|---|---|---|
| `W1` | UpperWoofer | `W1-UpperWoofer-H000deg.frd` |
| `W2` | LowerWoofer | `W2-LowerWoofer-H090deg.frd` |
| `M3` | UpperMid    | `M3-UpperMid-V015deg.frd` |
| `M4` | LowerMid    | `M4-LowerMid-NearField.frd` |
| `T`  | Tweeter     | `T-Tweeter-H000deg.frd` |
| `Pair` | Woofers / Mids (parallel) | `Pair-Woofers-InBox.zma`, `Pair-Mids-InBox.zma` |

Kind suffixes: `H###deg` horizontal, `V###deg` vertical, `NearField`, `InBox` (impedance), `Distortion`, `Distortion-1V` (tweeter).

**Formats saved per acoustic measurement** (REW): `.frd` (3-col: freq, SPL, phase — for LoudspeakerLab + VituixCAD), `.txt` (REW export with header metadata — backup), `.wav` (impulse response — for reanalysis in other tools). One master `.mdat` session file is saved at the end, preserving everything recoverable.

**Formats saved per impedance measurement** (DATS): `.zma` (3-col: freq, |Z|, phase — primary), `.tzz` (DATS session — backup), `.txt` (tertiary backup).

---

## 3. Impedance Sweeps — DATS V3 (30 min)

**Do this first.** DATS is independent of the acoustic rig — no mic, no Arcam, no REW, no floor arc. Just the laptop, the DATS V3 unit, and clip leads at the wall plate. Knocking out all 7 impedance sweeps up front is quick, satisfying, and verifies every driver is wired correctly at the wall before you invest in the acoustic setup.

Per-driver, all other drivers disconnected at the wall (open terminals):

| File (.zma primary, also save .tzz + .txt) | Driver | Notes |
|------|--------|-------|
| `W1-UpperWoofer-InBox.zma` | Upper woofer | Confirm Fc/Qtc vs Plan of Record (Qtc ~0.69, Fc ~56 Hz) |
| `W2-LowerWoofer-InBox.zma` | Lower woofer | Same check |
| `M3-UpperMid-InBox.zma` | Upper mid | |
| `M4-LowerMid-InBox.zma` | Lower mid | |
| `T-Tweeter-InBox.zma`  | Tweeter | Expect Fs ~650 Hz |
| `Pair-Woofers-InBox.zma` | W1 ∥ W2 | Wire both to DATS terminals in parallel |
| `Pair-Mids-InBox.zma` | M3 ∥ M4 | Wire both in parallel |

Save all to `InBoxMeasurements/dats/`. From DATS, also "Save Project" as `.tzz` alongside (captures the full DATS session for later re-export).

---

## 4. Floor Arc Setup

One-time rigging. Do this before calibration.

1. Drop a **plumb line** from the tweeter's acoustic center straight to the floor. Mark that point with a tape X. This is the **arc origin**.
2. With the tape measure held at the arc origin, extend a string exactly **1.00 m** perpendicular to the baffle (verify perpendicular with a carpenter's square held against the wall). Mark that point as **0° H**.
3. Using a protractor centered on the origin, mark positions for **10°, 20°, 30°, 40°, 50°, 60°, 70°, 80°, 90°** on one side of the 0° line. Each mark is a tape X on the floor at 1.00 m radius from origin.
   - Arc length between adjacent marks at 1 m radius is ~17.4 cm. Double-check by measuring the chord: 10° chord ≈ 17.4 cm, 20° chord ≈ 34.7 cm, etc.
4. At each tape X, also mark the **angle number** with a sharpie so you don't lose track mid-session.
5. **Tripod height:** set the mic tip to exactly **tweeter height** (measure with tape from floor to tweeter center on the baffle, transfer to tripod). This height stays fixed for all horizontal sweeps.
6. At 0°: if the tripod legs conflict with the wall, use a boom arm so the tripod base sits 1.5–2 m back and only the mic extends forward to 1 m. Do not skip 0°.

**Horizontal symmetry:** WMTMW is horizontally symmetric, so one side of the arc (0–90°) covers everything. No need to measure the other side.

---

## 5. Pre-Session Setup (30–45 min)

1. HVAC off. Note the time; you have limited quiet minutes.
2. Deploy toddler distraction.
3. Arcam: power on, input = 7.1 Multichannel, all DSP off (Direct mode), tone controls flat, bass management off. Set volume to the minimum first — you'll calibrate it in Step 6.
4. Connect L-RCA to Arcam 7.1 **FL** input, R-RCA to Arcam 7.1 **FR** input.
5. Wire desk speaker to Arcam **Front-Left** speaker terminals. Place desk speaker on a shelf or stand — anywhere — and **do not move it again** until the session ends.
6. At the wall terminals: disconnect every driver. We'll connect one at a time.
7. REW preferences:
   - Input device: UMIK-1 (load 0° cal file)
   - Output device: laptop stereo out
   - Analysis → Use Acoustic Timing Reference: **ON**, channel = **Left** (the desk speaker is on the L channel via Arcam FL)
   - Measurement default: log sweep, 512 k length, 20 Hz – 20 kHz, level −12 dBFS
   - Auto-name template: `{name}` with sequential suffix off (we'll name manually per sweep — fast enough with the template pre-loaded)
8. Verify channel assignment: use REW's generator to send a 1 kHz tone on **left only** — the desk speaker (on Arcam FL) should play; the FR (DUT) terminals should be silent. Repeat with **right only** — the FR terminals should be active (touch the FR terminal wire — meter movement / brief tap test); desk speaker silent. If both channels play on one output, Arcam is not in Multichannel Direct mode.

---

## 6. 2.83 V Calibration (10 min)

1. Connect **only W2 (lower woofer)** to Arcam **FR** terminals. All other drivers disconnected. **Verify tweeter wires are not touching each other or anything conductive.**
2. REW Generator → 60 Hz sine wave, **right channel only**, level −20 dBFS. Start.
3. DMM on AC V mode, probes across the W2 terminals at the wall.
4. Slowly raise Arcam volume until DMM reads **2.83 V** (±0.02 V).
5. **Stop generator.** Do not touch the Arcam volume knob for the remainder of the session. Consider taping over it.
6. Note the final Arcam volume setting in your log.

**Your non-True-RMS meter is fine here.** A standard averaging meter reads RMS correctly on a pure 60 Hz sine.

---

## 7. Timing Reference Verification (5 min)

1. Mic at 0° tape X (1 m on-axis).
2. W2 still connected to **FR**. Other drivers disconnected.
3. REW Measure → run a throwaway sweep.
4. Check the log: REW must report "Timing reference found" or similar. The IR should show a clean, isolated leading edge.
5. If timing reference not found: raise the pilot level in REW preferences, or raise Arcam FL output if it's too quiet (but then re-lock). Iterate until found.
6. Once locked, **do not move the desk speaker or the mic** except along the arc.

---

## 8. Horizontal Polar Sweeps (105–135 min)

**Why this order.** Moving the mic is slow (tripod + 1 m string check + re-aim at the tweeter). Wire swaps at the wall plate take seconds. So park the mic at one angle and sweep all six driver configurations before moving the mic. Six wiring swaps per mic position, ten mic positions = 60 sweeps.

For each of the ten angles `[000, 010, 020, 030, 040, 050, 060, 070, 080, 090]` (the zero-padded number also goes into the filename):

1. Move tripod so mic tip sits directly over that angle's tape X. Aim the mic at the tweeter. Verify 1 m with the string from tweeter to mic tip.
2. Sweep all six driver configurations without moving the mic. For each: rewire at the wall plate per the row below, then run the sweep. Each saves .frd + .txt + .wav.
3. Move the mic to the next angle's tape X and repeat.

Driver rows for the inner loop:

| Driver / config | Filename stem (→ .frd, .txt, .wav) | Sweep range | Wall wiring |
|-----------------|------------------------------------|------------|-------------|
| W1 upper woofer | `W1-UpperWoofer-H{ddd}deg` | 20 Hz – 20 kHz, 512 k | W1 → FR; all others disconnected |
| W2 lower woofer | `W2-LowerWoofer-H{ddd}deg` | 20 Hz – 20 kHz, 512 k | W2 → FR; all others disconnected |
| M3 upper mid    | `M3-UpperMid-H{ddd}deg`    | 20 Hz – 20 kHz, 512 k | M3 → FR; **M4 wall terminals shorted (jumper + to −)**; others disconnected |
| M4 lower mid    | `M4-LowerMid-H{ddd}deg`    | 20 Hz – 20 kHz, 512 k | M4 → FR; **M3 wall terminals shorted (jumper + to −)**; others disconnected |
| T  tweeter      | `T-Tweeter-H{ddd}deg`      | **300 Hz – 20 kHz, 256 k** | T → FR; others disconnected. See Section 0 |
| Pair `M3 ∥ M4`  | `Pair-Mids-H{ddd}deg`      | 20 Hz – 20 kHz, 512 k | M3 + M4 in parallel → FR; **remove any mid-shorting jumpers**; others disconnected |

**Why short the unused mid.** M3 and M4 share the rear chamber. With one driven and the other electrically open, the undriven cone passively radiates near its free-air Fs (~50 Hz) and contaminates the measurement (visible as a second impedance peak in the in-box DATS data). Shorting the unused voice coil clamps cone motion via back-EMF damping. The wizard requires an explicit yes/no confirmation that the jumper is in place before each single-mid sweep.

**Why the `Pair-Mids` row.** The crossover wires M3 and M4 in parallel, so the operationally accurate measurement is both driven together. The pair sweep captures this directly with no passive cone in the chamber.

**Total: 60 sweeps × 3 output formats = 180 files.** Each sweep ~5–10 s measure time; wizard auto-names and auto-exports.

Keep the timing-reference desk speaker in place the entire time.

---

## 9. Vertical Off-Axis (20–25 min)

WMTMW is vertically symmetric around the tweeter, so measure one direction only (upward). Only T, M3, M4, and the M3∥M4 pair need vertical data — woofers are omni at their operating band.

At **1 m radius from tweeter**:
- **+15° vertical:** mic is 96.6 cm out from baffle, 25.9 cm above tweeter height.
- **+30° vertical:** mic is 86.6 cm out from baffle, 50.0 cm above tweeter height.

Measure these offsets from the 0° on-axis point: raise the tripod by the height delta and pull it in toward the baffle by the distance delta. Verify with the 1 m string from tweeter to mic tip.

Sweeps (each saves .frd + .txt + .wav):

| Driver / config | Filename stems | Wall wiring |
|-----------------|----------------|-------------|
| T  | `T-Tweeter-V015deg`, `T-Tweeter-V030deg` | T → FR; others disconnected. 300 Hz – 20 kHz, 256 k |
| M3 | `M3-UpperMid-V015deg`, `M3-UpperMid-V030deg` | M3 → FR; **M4 wall terminals shorted**; others disconnected |
| M4 | `M4-LowerMid-V015deg`, `M4-LowerMid-V030deg` | M4 → FR; **M3 wall terminals shorted**; others disconnected |
| Pair `M3 ∥ M4` | `Pair-Mids-V015deg`, `Pair-Mids-V030deg` | M3 + M4 in parallel → FR; **remove mid-shorting jumpers**; others disconnected |

The same shorting-confirmation gate applies for single-mid vertical sweeps as for horizontal — the wizard blocks until the jumper is acknowledged.

**Total: 8 sweeps × 3 formats = 24 files.**

---

## 10. Nearfield Sweeps (15 min)

Mic tip **<5 mm from dust cap center**, pointed axially into the driver. No gate applied. Timing reference remains on (harmless; REW just can't gate nearfield responses tightly).

| Driver | Filename stem (→ .frd, .txt, .wav) |
|--------|------|
| W1 | `W1-UpperWoofer-NearField` |
| W2 | `W2-LowerWoofer-NearField` |
| M3 | `M3-UpperMid-NearField`    |
| M4 | `M4-LowerMid-NearField`    |

**Tweeter: skip.** LoudspeakerLab auto-splices based on driver diameter for woofers and mids only; tweeter nearfield is meaningless.

**Total: 4 sweeps × 3 formats = 12 files.**

---

## 11. Distortion Sweeps (20 min)

Mic back at 0° H, 1 m on-axis (tape X). Same Arcam volume.

REW Distortion measurement → stepped sine or long log sweep. Export as text ("Export All as Text" from distortion window).

| Driver | Filename | Level | Sweep range |
|--------|------|-------|-------------|
| W1 | `W1-UpperWoofer-Distortion.txt` | 2.83 V | 20 Hz – 20 kHz |
| W2 | `W2-LowerWoofer-Distortion.txt` | 2.83 V | 20 Hz – 20 kHz |
| M3 | `M3-UpperMid-Distortion.txt`    | 2.83 V | 20 Hz – 20 kHz |
| M4 | `M4-LowerMid-Distortion.txt`    | 2.83 V | 20 Hz – 20 kHz |
| T  | `T-Tweeter-Distortion-1V.txt`   | **1 V** | **300 Hz – 20 kHz** |

**Tweeter distortion at 1 V:** in REW, reduce the sweep output level by 9 dB (2.83 V → 1.00 V is a 9.02 dB reduction). Filename suffix `-1V` records the level. LoudspeakerLab expects files at the calibrated level, but distortion data is used as a relative penalty — annotate the actual measurement level at upload.

**Total: 5 distortion files** (plus REW also auto-saves its internal `.mdat` entry).

---

## 12. Export & Sanity Checks (20 min)

Before tearing down the rig. If the wizard ran, most of this is already done; this checklist covers manual-mode and final backup.

1. **Export all REW sweeps as .frd** (3-column: freq, SPL, phase) → `InBoxMeasurements/frd/`.
2. **Export all REW sweeps as .txt** (REW native, preserves header metadata) → `InBoxMeasurements/txt/`.
3. **Export impulse responses as .wav** for each sweep (REW → File → Export → Export measurement impulse response as WAV) → `InBoxMeasurements/wav/`.
4. **Export distortion as text** (REW → File → Export → Export All as Text from each distortion measurement) → `InBoxMeasurements/distortion/`.
5. **Save REW session** as `InBoxMeasurements/REW_session.mdat` — master recovery file.
6. **DATS files**: `.zma` primary files in `InBoxMeasurements/dats/`, DATS project file `.tzz` alongside, optional `.txt` as tertiary backup.

**Sanity checks (do before you touch the rig):**

- Overlay all 10 `W1_Hxx.frd` sweeps. On-axis should be highest SPL in the forward lobe; off-axis should drop cleanly in the treble (woofer beams above ~2 kHz). No weird notches or level discontinuities.
- Tweeter on-axis should be flat-ish from 2 kHz to 10 kHz, around 95 dB, no sub-300 Hz content (you set the sweep start there — confirm).
- Impedance sweeps: woofer peak near 56 Hz (sealed Fc), tweeter peak near 650 Hz. Mids peak near their in-box Fc (expect ~120–150 Hz given the mid/tweeter shared chamber).
- No clipping in any IR — check REW's overload indicator retroactively.

If any sweep looks wrong, **re-run it now** while the rig is still set up. Re-rigging next weekend costs you an afternoon.

---

## 13. Final File Layout

```
InBoxMeasurements/
├── Measurement_Runbook.md           ← this document
├── Measurement_Runbook.html         ← printable version
├── README.md                        ← wizard usage
├── sweep_wizard.py                  ← wizard entry point
├── measurement_matrix.py            ← sweep/DATS definitions
├── rew_api.py                       ← REW HTTP API adapter
├── prompts.py                       ← UI + logging helpers
├── sweep_log.csv                    ← wizard progress log (auto-created)
│
├── rew/                             ← REW acoustic measurement data
│   ├── WMTMW_session.mdat           ← REW master session (save at end)
│   ├── frd/                         ← 3-col FRD (freq, SPL, phase) for VituixCAD / loudspeakerlab
│   │   ├── W1-UpperWoofer-H000deg.frd … H090deg.frd, NearField.frd
│   │   ├── W2-LowerWoofer-H000deg.frd … H090deg.frd, NearField.frd
│   │   ├── M3-UpperMid-H000deg.frd    … H090deg.frd, V015deg.frd, V030deg.frd, NearField.frd
│   │   ├── M4-LowerMid-H000deg.frd    … H090deg.frd, V015deg.frd, V030deg.frd, NearField.frd
│   │   └── T-Tweeter-H000deg.frd      … H090deg.frd, V015deg.frd, V030deg.frd
│   ├── txt/                         ← REW native text export (mirrors frd/)
│   ├── wav/                         ← impulse response WAV (re-gate later if needed)
│   └── distortion/                  ← REW distortion text exports
│       ├── W1-UpperWoofer-Distortion.txt
│       ├── W2-LowerWoofer-Distortion.txt
│       ├── M3-UpperMid-Distortion.txt
│       ├── M4-LowerMid-Distortion.txt
│       └── T-Tweeter-Distortion-1V.txt
│
└── dats/                            ← DATS V3 impedance measurement data
    ├── W1-UpperWoofer-InBox.zma  (+ .tzz, .txt)
    ├── W2-LowerWoofer-InBox.zma  (+ .tzz, .txt)
    ├── M3-UpperMid-InBox.zma     (+ .tzz, .txt)
    ├── M4-LowerMid-InBox.zma     (+ .tzz, .txt)
    ├── T-Tweeter-InBox.zma       (+ .tzz, .txt)
    ├── Pair-Woofers-InBox.zma    (+ .tzz, .txt)
    └── Pair-Mids-InBox.zma       (+ .tzz, .txt)
```

**Counts.**
- Acoustic sweeps: 60 H + 8 V + 4 NF + 5 THD = **77 sweeps** (H and V each include `Pair-Mids` rows).
- Impedance sweeps: **7** (5 individual + 2 pairs).
- File outputs per acoustic sweep: 3 (.frd, .txt, .wav).
- File outputs per impedance sweep: 3 (.zma, .tzz, .txt).
- Grand total: **77 × 3 + 7 × 3 + 5 distortion + 1 REW session = 258 files**.

---

## 14. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| REW says "Timing reference not found" | Desk speaker not producing audible pilot at mic | Raise R-channel level in REW, or reposition desk speaker closer to mic |
| IR shows ragged/multiple leading edges | Desk speaker moved, or room picked up a new reflection | Re-verify desk speaker position, re-run last sweep |
| On-axis SPL much lower than expected | Wrong driver connected, or phase cancellation from another driver still wired in parallel | Verify only one driver is connected at a time; check polarity |
| Sweep clipping | Arcam volume crept up, or laptop output raised | Re-check 2.83 V on calibration woofer; do not trust the knob |
| Tweeter sweep shows low-frequency noise | REW sweep range not restricted to 300 Hz+ | Check Measure dialog range. Disconnect tweeter and verify generator range first |
| Nearfield shows cone breakup artifacts | Mic too close to cone (coupling) or off-center | Move mic to <5 mm but not touching; center over dust cap |

---

*This runbook is the execution-time companion to `WMTMW_PlanOfRecord.md`. Update the Plan of Record with final crossover values once LoudspeakerLab / VituixCAD design is complete.*
