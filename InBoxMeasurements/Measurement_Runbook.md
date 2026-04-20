# WMTMW In-Wall Measurement Runbook

Session runbook for in-box acoustic and electrical characterization of the prototype WMTMW in-wall speaker. Data targets both **LoudspeakerLab** (primary) and **VituixCAD** (secondary) for crossover design.

**Companion file:** `Measurement_Runbook.html` — printable version with SVG diagrams for arc geometry, mic placement, and signal chain. Print that one for use in the basement.

**Estimated session time:** 4.5–6 hours including setup and verification.

---

## 0. Tweeter Protection — READ FIRST

The Scan-Speak H2606/9200 voice coil can burn out in **seconds** if driven with low-frequency content at 2.83 V. Every tweeter-related step below exists to prevent that. Do not skip any of them.

| # | Rule | Why |
|---|------|-----|
| 1 | During 2.83 V calibration (Step 5), the **tweeter must be physically disconnected** at the wall. Only the calibration woofer is connected. | 60 Hz sine at 2.83 V into a tweeter destroys it instantly. |
| 2 | For every tweeter sweep, set REW **sweep start frequency to 300 Hz**. Tweeter Fs is ~650 Hz; 300 Hz gives margin but stays well below the intended ~2.5 kHz crossover. | The default 20 Hz sweep start applies full voltage below Fs where excursion peaks. |
| 3 | Use **256 k sweep length** for tweeter, not 512 k. Shorter exposure. | Limits thermal dose. |
| 4 | Tweeter distortion sweeps run at **1 V**, not 2.83 V. Label files `T_THD_1V.txt`. | 2.83 V extended stepped sine is thermally punishing. |
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
- Speaker wire for desk-speaker tap to Arcam Center terminal
- Earplugs

**Signal chain**

```
Laptop 3.5mm stereo out
   ├── L channel ─RCA─► Arcam 7.1-in "Front Left"  ─► Arcam FL amp ─► DUT wires at wall
   └── R channel ─RCA─► Arcam 7.1-in "Center"      ─► Arcam Center amp ─► Desk speaker (fixed position)

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
- Laptop L channel = sweep → DUT (calibrated to 2.83 V)
- Laptop R channel = REW timing-reference pilot → desk speaker (REW-attenuated, typically −20 dB)
- Arcam volume is **locked** for the entire session after Step 5. Do not touch.

---

## 3. Floor Arc Setup

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

## 4. Pre-Session Setup (30–45 min)

1. HVAC off. Note the time; you have limited quiet minutes.
2. Deploy toddler distraction.
3. Arcam: power on, input = 7.1 Multichannel, all DSP off (Direct mode), tone controls flat, bass management off. Set volume to the minimum first — you'll calibrate it in Step 5.
4. Connect L-RCA to Arcam 7.1 FL input, R-RCA to Arcam 7.1 Center input.
5. Wire desk speaker to Arcam Center speaker terminals. Place desk speaker on a shelf or stand — anywhere — and **do not move it again** until the session ends.
6. At the wall terminals: disconnect every driver. We'll connect one at a time.
7. REW preferences:
   - Input device: UMIK-1 (load 0° cal file)
   - Output device: laptop stereo out
   - Analysis → Use Acoustic Timing Reference: **ON**, channel = Right
   - Measurement default: log sweep, 512 k length, 20 Hz – 20 kHz, level −12 dBFS
   - Auto-name template: `{name}` with sequential suffix off (we'll name manually per sweep — fast enough with the template pre-loaded)
8. Verify channel assignment: use REW's generator to send a 1 kHz tone on **left only**. Confirm only the FL Arcam output is active (touch the FL terminal wire — should see meter movement; desk speaker should be silent). Repeat with right only — desk speaker plays, FL is silent. If both channels play on one output, Arcam is not in Multichannel Direct mode.

---

## 5. 2.83 V Calibration (10 min)

1. Connect **only W2 (lower woofer)** to Arcam FL terminals. All other drivers disconnected. **Verify tweeter wires are not touching each other or anything conductive.**
2. REW Generator → 60 Hz sine wave, left channel only, level −20 dBFS. Start.
3. DMM on AC V mode, probes across the W2 terminals at the wall.
4. Slowly raise Arcam volume until DMM reads **2.83 V** (±0.02 V).
5. **Stop generator.** Do not touch the Arcam volume knob for the remainder of the session. Consider taping over it.
6. Note the final Arcam volume setting in your log.

**Your non-True-RMS meter is fine here.** A standard averaging meter reads RMS correctly on a pure 60 Hz sine.

---

## 6. Timing Reference Verification (5 min)

1. Mic at 0° tape X (1 m on-axis).
2. W2 still connected to FL. Other drivers disconnected.
3. REW Measure → run a throwaway sweep.
4. Check the log: REW must report "Timing reference found" or similar. The IR should show a clean, isolated leading edge.
5. If timing reference not found: raise the pilot level in REW preferences, or raise Arcam Center output if it's too quiet (but then re-lock). Iterate until found.
6. Once locked, **do not move the desk speaker or the mic** except along the arc.

---

## 7. Impedance Sweeps — DATS V3 (30 min)

Mic not needed for this section. Disconnect laptop from Arcam if you like.

Per-driver, all other drivers disconnected at the wall (open terminals):

| File | Driver | Notes |
|------|--------|-------|
| `W1_inbox.zma` | Upper woofer | Confirm Fc/Qtc vs Plan of Record (Qtc ~0.69, Fc ~56 Hz) |
| `W2_inbox.zma` | Lower woofer | Same check |
| `M3_inbox.zma` | Upper mid | |
| `M4_inbox.zma` | Lower mid | |
| `T_inbox.zma`  | Tweeter | Expect Fs ~650 Hz |
| `Wpair_inbox.zma` | W1 ∥ W2 | Wire both to DATS terminals in parallel |
| `Mpair_inbox.zma` | M3 ∥ M4 | Wire both in parallel |

Save all to `InBoxMeasurements/`.

---

## 8. Horizontal Polar Sweeps (90–120 min)

**Outer loop = mic angle (minimizes mic moves). Inner loop = driver (fast cable swap at wall).**

For each angle in `[0, 10, 20, 30, 40, 50, 60, 70, 80, 90]` degrees horizontal:

1. Move tripod so mic tip sits directly over the tape X for that angle. Mic pointed at tweeter. Verify 1 m with string from tweeter to mic tip.
2. Sweep each driver in order (each time: disconnect previous driver, connect next driver, all others stay disconnected):

| Driver | File | Sweep range | Notes |
|--------|------|------------|-------|
| W1 upper woofer | `W1_H{angle}.frd` | 20 Hz – 20 kHz | Full range |
| W2 lower woofer | `W2_H{angle}.frd` | 20 Hz – 20 kHz | |
| M3 upper mid    | `M3_H{angle}.frd` | 20 Hz – 20 kHz | |
| M4 lower mid    | `M4_H{angle}.frd` | 20 Hz – 20 kHz | |
| T  tweeter      | `T_H{angle}.frd`  | **300 Hz – 20 kHz**, 256 k length | See Section 0 |

**Total: 50 sweeps.** Each sweep ~5–10 s measure time + filename entry.

Keep the timing-reference desk speaker in place the entire time.

---

## 9. Vertical Off-Axis (15–20 min)

WMTMW is vertically symmetric around the tweeter, so measure one direction only (upward). Only T, M3, M4 need vertical data — woofers are omni at their operating band.

At **1 m radius from tweeter**:
- **+15° vertical:** mic is 96.6 cm out from baffle, 25.9 cm above tweeter height.
- **+30° vertical:** mic is 86.6 cm out from baffle, 50.0 cm above tweeter height.

Measure these offsets from the 0° on-axis point: raise the tripod by the height delta and pull it in toward the baffle by the distance delta. Verify with the 1 m string from tweeter to mic tip.

Sweeps:

| Driver | File | Notes |
|--------|------|-------|
| T  | `T_V15.frd`, `T_V30.frd` | 300 Hz – 20 kHz, 256 k |
| M3 | `M3_V15.frd`, `M3_V30.frd` | Full range |
| M4 | `M4_V15.frd`, `M4_V30.frd` | Full range |

**Total: 6 sweeps.**

---

## 10. Nearfield Sweeps (15 min)

Mic tip **<5 mm from dust cap center**, pointed axially into the driver. No gate applied. Timing reference remains on (harmless; REW just can't gate nearfield responses tightly).

| Driver | File |
|--------|------|
| W1 | `W1_NF.frd` |
| W2 | `W2_NF.frd` |
| M3 | `M3_NF.frd` |
| M4 | `M4_NF.frd` |

**Tweeter: skip.** LoudspeakerLab auto-splices based on driver diameter for woofers and mids only; tweeter nearfield is meaningless.

**Total: 4 sweeps.**

---

## 11. Distortion Sweeps (20 min)

Mic back at 0° H, 1 m on-axis (tape X). Same Arcam volume.

REW Distortion measurement → stepped sine or long log sweep. Export as text ("Export All as Text" from distortion window).

| Driver | File | Level | Sweep range |
|--------|------|-------|-------------|
| W1 | `W1_THD.txt` | 2.83 V | 20 Hz – 20 kHz |
| W2 | `W2_THD.txt` | 2.83 V | 20 Hz – 20 kHz |
| M3 | `M3_THD.txt` | 2.83 V | 20 Hz – 20 kHz |
| M4 | `M4_THD.txt` | 2.83 V | 20 Hz – 20 kHz |
| T  | `T_THD_1V.txt` | **1 V** | **300 Hz – 20 kHz** |

**Tweeter distortion at 1 V:** in REW, reduce the sweep output level by 9 dB (2.83 V → 1.00 V is a 9.02 dB reduction). Note the level change in the filename. LoudspeakerLab expects files at the calibrated level, but distortion data is used as a relative penalty — you can annotate the actual measurement level at upload.

---

## 12. Export & Sanity Checks (20 min)

Before tearing down the rig:

1. **Export all REW sweeps as .frd** (3-column: freq, SPL, phase). REW → File → Export → Export measurement as FRD. Save to `InBoxMeasurements/frd/`.
2. **Export distortion as text.** Save to `InBoxMeasurements/distortion/`.
3. **Save REW session file (.mdat)** as `InBoxMeasurements/REW_session.mdat` — preserves everything, recoverable if exports are wrong.
4. **DATS .zma files** are already in `InBoxMeasurements/`.

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
├── Measurement_Runbook.md
├── Measurement_Runbook.html
├── REW_session.mdat
├── W1_inbox.zma
├── W2_inbox.zma
├── M3_inbox.zma
├── M4_inbox.zma
├── T_inbox.zma
├── Wpair_inbox.zma
├── Mpair_inbox.zma
├── frd/
│   ├── W1_H00.frd … W1_H90.frd, W1_NF.frd
│   ├── W2_H00.frd … W2_H90.frd, W2_NF.frd
│   ├── M3_H00.frd … M3_H90.frd, M3_V15.frd, M3_V30.frd, M3_NF.frd
│   ├── M4_H00.frd … M4_H90.frd, M4_V15.frd, M4_V30.frd, M4_NF.frd
│   └── T_H00.frd  … T_H90.frd,  T_V15.frd, T_V30.frd
└── distortion/
    ├── W1_THD.txt, W2_THD.txt, M3_THD.txt, M4_THD.txt
    └── T_THD_1V.txt
```

**Total acoustic sweep count:** 50 H + 6 V + 4 NF + 5 THD = **65 acoustic sweeps**, plus 7 impedance sweeps.

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
