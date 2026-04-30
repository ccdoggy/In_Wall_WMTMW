# WMTMW In-Wall Speaker — Development History & Session Log

> **Purpose:** This file preserves the full design development history so that
> if a session closes, a new session can read this file and pick up where we
> left off. It contains all decisions, rationale, open questions, and current
> state.
>
> **Last updated:** April 30, 2026
> **Primary design file:** `/home/cyc/WMTMW_InWall_Speaker_Design.md`

---

## 1. Project Background

### The User's Setup
- Dedicated basement home theater
- ~9 foot listening distance from front wall
- 135" diagonal projector screen
- L/R speakers are ~6 feet from center channel
- L/R listening angle: ~30° horizontal off-axis
- Already built **Mechano23** speakers for sides + rears
  - Mechano23 uses: SB Acoustics SB13PFCR25-4 (5" woofer, 4 ohm) + Scan-Speak H2606/9200 (tweeter, 6 ohm)
  - Confirmed standard Mechano23 build per ASR thread #54066
- Has UMIK-1 measurement mic and DATS V3 driver measurement device
- Has VituixCAD-capable Windows PC
- Budget: sub $600/speaker (not including MDF)
- Minimum 125W amplification for L/C/R
- Will have dedicated subwoofer(s)
- Prefers soft dome tweeters, no ribbons

### The Goal
Design and build 3x identical WMTMW in-wall speakers for L/C/R channels,
mounted in a 2x6 wall (16" OC studs), timbre-matched to the Mechano23
surrounds.

---

## 2. Decision Log (Chronological)

### Decision 1: Configuration — WMTMW
**Choice:** WMTMW (Woofer-Midrange-Tweeter-Midrange-Woofer)
**Alternatives considered:** WTMW (asymmetric), MTM (no woofer section), WTW (2-way)
**Rationale:**
- Tweeter at center = at ear height (most directional driver aimed at ears)
- Vertical symmetry = identical dispersion for L, C, and R
- Dual midranges = necessary for power handling at reference levels (single 5" mid clips at ~102W needed for 100 dB peaks at 9 feet; dual mids need only ~25W each)
- Industry standard for high-end in-wall (JBL Synthesis, Revel, KEF Ci)
- Reduced floor/ceiling reflections from vertical lobing

**Re-reviewed in session:** Confirmed. The power handling math proves dual mids are necessary, not just for symmetry. A single 5" mid would be pushed past its thermal limits on loud movie transients at 9-foot distance.

### Decision 2: Driver Selection — Timbre Matching Priority
**Choice:** Use the same midrange driver and tweeter as the Mechano23
**Rationale:**
- Ensures cohesive timbre across all channels (L/C/R + sides + rears)
- The SB13PFC + H2606/9200 combination has proven directivity matching (ASR-measured)
- The 8-ohm variants (SB13PFCR25-08) are acoustically identical to the 4-ohm Mechano23 versions

### Decision 3: Woofer — SB17MFC35-8
**Choice:** SB Acoustics SB17MFC35-8 (6.5" polypropylene, 8 ohm)
**Alternatives considered:**
- SB17NRX2C35-4 (Norex) — OUT OF STOCK at Madisound
- SB17NBAC35-4 (aluminum) — OUT OF STOCK at Madisound
- SB17CRC35-4 (carbon fiber) — OUT OF STOCK at Madisound
- Scan-Speak 18W/8531G — excellent but ~$150 each (budget concern)
- Satori MW16P-8 — premium but ~$100+ each
**Rationale:**
- In stock at Madisound ($75.90 each)
- Adequate for the 50-400 Hz role (woofer bandwidth)
- Polypropylene = well-damped, no sharp breakup peaks, simpler crossover
- Shallow enough for 2x6 wall (2.44" mounting depth, 1.56" clearance)
- Budget-friendly (saves money for crossover components)

**Re-reviewed in session 2:** Confirmed adequate. Sealed F3 ~63 Hz means it holds together well at a 50–70 Hz sub crossover (room gain assists below 80 Hz). Not exciting but solid for its operating band. The crossover dominates the sound; cone material differences are minimal for 60–400 Hz.

**Re-reviewed in session 3:** Official SB Acoustics T/S parameters corrected:
Fs = 33 Hz, Qts = 0.37, Vas = 39 L (previous doc values were significantly wrong).
Sealed Qtc = 0.75 in 13.1 L (without fill, net ~12.7 L) → 0.70 with polyfill = near-ideal Butterworth.
F3 ≈ 63 Hz (stable regardless of fill). Previous doc values of 57 Hz were incorrect.
SB17NRX2L35-8 (Norex, NEW) was evaluated as a potential upgrade — rejected because its
very low Qts (0.28) makes it severely overdamped in 13.1 L chambers (Qtc = 0.48, F3 ≈ 104 Hz).
The NRX2L needs a ~5 L box for proper alignment. MFC35-8 confirmed as correct choice for
this box volume and the user's 50–70 Hz sub crossover preference.

### Decision 4: Midrange — SB13PFCR25-08
**Choice:** SB Acoustics SB13PFCR25-08 (5" paper cone, 8 ohm, round frame)
**Rationale:**
- Same driver as Mechano23 woofer (8 ohm variant) — timbre matching
- Paper cone, natural midrange character, low distortion
- 8 ohm for parallel wiring (4 ohm per pair)
- In stock at Madisound ($36.80 each)
- ASR-proven in the Mechano23 with "a masterpiece" verdict

### Decision 5: Tweeter — Scan-Speak H2606/9200
**Choice:** Scan-Speak Discovery H2606/9200 (26mm horn-loaded textile dome, 6 ohm)
**Rationale:**
- Same tweeter as Mechano23 — timbre matching
- Horn-loaded = controlled directivity, high sensitivity (95 dB)
- The horn loading provides the directivity matching at crossover that made the Mechano23 exceptional
- Textile dome per user preference (no ribbons)
- In stock at Madisound ($47.80 each)

### Decision 6: Sealed Enclosure
**Choice:** Sealed (no port)
**Rationale:**
- Subwoofer handles everything below 50–70 Hz
- Sealed = simpler, more predictable, better transient response
- No port noise, no port tuning complexity, no depth penalty
- In-wall mounting provides half-space loading (free +3–6 dB)

### Decision 7: Enclosure Dimensions
**Choice:** Box: 14.25" W × 5.50" D × 48.00" H; Baffle: 16.00" W × 49.50" H × 0.50" D
**Rationale:**
- Box width: 14.25" fits between 16" OC studs with 1/8" clearance per side
- Baffle width: 16.00" overlaps each stud face by 3/4" for mounting screws
- Depth: 5.50" uses full 2x6 stud cavity
- Box height: 48" provides adequate volume for woofer chambers (13.1 L each)
- Baffle height: 49.50" overlaps cross studs top and bottom by 3/4"
- Baffle: 1/2" MDF = same thickness as drywall = flush with wall automatically
- Internal: 12.75" × 4.25" × 46.50" (with 3/4" MDF sides/top/bottom, 1/2" baffle, 3/4" back)

### Decision 8: 2-Divider Chamber Design
**Choice:** Two 1/2" MDF horizontal dividers creating 3 chambers
(upper woofer / mid-tweeter section / lower woofer)
**Alternatives considered:** 4 dividers (5 chambers, each driver isolated)
**Rationale:**
- Simpler construction
- The mids and tweeter sharing a volume is standard in MTM/WMTMW designs
- Both mids play the same signal — back-radiation reinforcement, not interference
- Tweeter (H2606/9200) has sealed back — doesn't interact with shared volume
- Acoustic foam damping eliminates standing waves in shared cavity
- Commercial WMTMW in-walls use this approach

### Decision 9: Flush In-Wall Mounting (NOT angled)
**Choice:** All three speakers mounted flat/flush in the wall
**Alternative discussed:** Angling L/R speakers 30° to face the listener
**Rationale for NOT angling:**
- The 2-3 dB treble rolloff at 30° is trivially corrected by AVR room EQ
- Angling creates 7"+ wall protrusion — no longer an in-wall speaker
- Loses infinite baffle loading (baffle step returns, 6 dB compensation needed)
- Creates asymmetric diffraction and reflections
- No commercial or DIY builder does this — for good physics reasons
- The Mechano23 driver combination already excels at off-axis response

### Decision 10: Wiring — 8-Ohm Parallel
**Choice:** 8-ohm drivers wired in parallel for each section
**Rationale:**
- Woofer pair: 8Ω parallel = 4Ω — standard amp load
- Mid pair: 8Ω parallel = 4Ω — standard amp load
- Tweeter: 6Ω (single driver)
- System impedance: 4-6Ω nominal

---

## 3. Off-Axis Analysis (Critical Finding)

### Horizontal Off-Axis (L/R at 30°)
**The WMTMW vertical array creates lobing ONLY in the vertical plane.**
Horizontal dispersion is determined by individual driver directivity, not
the multi-driver arrangement. At 30° horizontal:
- No comb filtering from the WMTMW arrangement
- Each driver section is ~2-3 dB down in the upper frequencies
- The directivity match between SB13PFC and H2606/9200 at the 2.5 kHz
  crossover is excellent (within ~1 dB at 30°)
- AVR room correction easily compensates for the level difference

### Vertical Lobing (Dual Midranges)
Mid-to-mid spacing: 10.50" (267 mm) center-to-center
- First null at 15° vertical: ~2,480 Hz (borderline, mids rolling off)
- First null at 30° vertical: ~1,280 Hz (reduces floor/ceiling reflections)
- Listener is at 0° vertical (tweeter at ear height) — unaffected

**Conclusion:** Off-axis performance is NOT a problem for this design.

---

## 4. Enclosure Engineering Summary

### Dimensions *(superseded by Sessions 4 & 5 — see design doc Section 9 for current values)*
| Part | Dimension |
|------|-----------|
| Box external | 14.25" W × 5.50" D × 48.00" H |
| Front baffle | 16.00" W × 49.50" H × 0.50" thick (1/2" MDF) |
| Box internal | 12.75" W × 4.25" D × 46.50" H |
| Drywall cutout | 16.0" W × 49.5" H |
| Stud overlap | 0.75" per side |

### Driver Positions (from bottom of baffle)
| Driver | Center | Frame extent |
|--------|--------|-------------|
| Lower woofer (SB17MFC35-8) | 11.25" | 7.88" – 14.62" |
| Lower mid (SB13PFCR25-08) | 18.00" | 15.30" – 20.70" |
| Tweeter (H2606/9200) | 23.25" | 21.20" – 25.30" |
| Upper mid (SB13PFCR25-08) | 28.50" | 25.80" – 31.20" |
| Upper woofer (SB17MFC35-8) | 35.25" | 31.88" – 38.62" |

Note: baffle "from bottom" includes 0.75" flange below box bottom.
Driver centers relative to box bottom are 0.75" less than listed above.

### Internal Divider Positions (from bottom, inside)
| Divider | Position | Between |
|---------|----------|---------|
| Divider 1 | 14.96" | Lower woofer / mid-tweeter section |
| Divider 2 | 31.55" | Mid-tweeter section / upper woofer |

### Chamber Volumes *(superseded by Session 4 — 3/4" baffle, 4.00" depth; see Session 4 table)*
| Chamber | Height | Volume | Qtc (sealed) |
|---------|--------|--------|-------------|
| Lower woofer | 14.71" | 13.1 L (0.46 ft³) | 0.75 (0.70 w/fill) |
| Mid/tweeter | 16.09" | 14.3 L (0.50 ft³) | 0.56 (pair) |
| Upper woofer | 14.70" | 13.1 L (0.46 ft³) | 0.75 (0.70 w/fill) |

### Driver Physical Dimensions
| Parameter | SB17MFC35-8 | SB13PFCR25-08 | H2606/9200 |
|-----------|-------------|---------------|------------|
| Frame OD | 171mm / 6.73" | ~137mm / 5.39" | 104mm / 4.09" (sq) |
| Cutout | 149mm / 5.87" | ~116mm / 4.57" | ~74mm / 2.91" |
| Mount depth | 62mm / 2.44" | ~55mm / 2.17" | ~22mm / 0.87" |

### MDF Cutting List (per speaker) *(superseded by Sessions 4 & 5 — see design doc Phase 2 for current cut list)*
**3/4" MDF:**
- Front baffle: 14.25" × 48.00" (×1)
- Back panel: 14.25" × 48.00" (×1)
- Side panels: 4.00" × 48.00" (×2)
- Top panel: 14.25" × 4.00" (×1)
- Bottom panel: 14.25" × 4.00" (×1)

**1/2" MDF:**
- Divider 1: 12.75" × 4.00" (×1)
- Divider 2: 12.75" × 4.00" (×1)

---

## 5. Pricing (Verified at Madisound, March 2026)

### Per Speaker
| Item | Cost |
|------|------|
| 2× SB17MFC35-8 woofers | $151.80 |
| 2× SB13PFCR25-08 mids | $73.60 |
| 1× H2606/9200 tweeter | $47.80 |
| **Driver total** | **$273.20** |
| Crossover (estimated) | $85 – $150 |
| Hardware | $25 – $35 |
| **Total per speaker** | **$383 – $458** |

### All 3 Speakers
| Item | Cost |
|------|------|
| Drivers (15 total) | $819.60 |
| Crossover components | $255 – $450 |
| Hardware | $75 – $105 |
| **Grand total** | **$1,150 – $1,375** |
| Budget (3 × $600) | $1,800 |
| **Under budget by** | **$425 – $650** |

---

## 6. What I (the AI) Can and Cannot Do

### File Formats I Can Read
| Format | Description | Can read? |
|--------|-------------|-----------|
| `.frd` | Frequency response (text: freq, SPL, phase) | YES |
| `.zma` | Impedance data (text: freq, Z, phase) | YES |
| `.csv` | Comma-separated values | YES |
| `.txt` | Plain text exports | YES |
| `.mdat` | REW binary project file | NO (export to .frd) |
| `.vcad` | VituixCAD project (possibly XML) | LIKELY (need to test) |

### What I Can Do
- Read and interpret .frd and .zma measurement files
- Calculate crossover component values (LR4, Zobel, L-pad, impedance EQ)
- Design crossover topologies and suggest starting values
- Walk through VituixCAD setup step-by-step
- Troubleshoot measurements (identify leaks, resonances, anomalies)
- Review VituixCAD results and suggest refinements
- Calculate sealed alignments, sensitivity, SPL projections
- Help with the iterative crossover design process

### What I Cannot Do
- Run WinISD, VituixCAD, REW, or any Windows software
- Replace VituixCAD's crossover optimizer (requires the simulation engine)
- Generate accurate frequency response predictions from T/S parameters alone
- See screenshots (terminal-based — user must describe or export data as text)

### Recommended Workflow
1. User measures drivers → exports .frd and .zma files
2. User saves files to home directory
3. AI reads files, interprets, helps set up VituixCAD
4. User runs VituixCAD optimizer
5. User exports results, AI reviews and suggests changes
6. Iterate until satisfied

---

## 7. Remaining Design Items

All design items have been resolved as of Session 2.

| Item | Status | Resolution |
|------|--------|------------|
| Binding post location | **RESOLVED** | Back panel, binding post cup (final build) |
| Crossover mounting | **RESOLVED** | External for prototype, internal for final |
| Wiring diagram | **RESOLVED** | Full signal path defined, both configurations |
| Grille design | **RESOLVED** | No grille, painted flat black |
| Trim ring | **RESOLVED** | Not needed — 3/4" baffle rabbeted to 1/2" at edges = flush w/ drywall |
| Measurement procedure | **RESOLVED** | Full DATS + REW step-by-step in build process |
| Cable routing | **RESOLVED** | Prototype: out top to external XO; Final: internal |
| Drywall cutout | **RESOLVED** | 16.0" × 49.5" |
| Assembly order | **RESOLVED** | 56-step process across 11 phases |

---

## 8. Prototype Strategy

### Smart Prototype Plan (Minimum Cost)
The user owns existing Mechano23 drivers (SB13PFCR25-4, 4 ohm + H2606/9200).
These can be used for prototyping without buying all new drivers.

**Phase 1 prototype:**
1. Build full WMTMW enclosure (all 5 driver holes)
2. Buy only 2× SB17MFC35-8 woofers ($151.80)
3. Install: 2 woofers + 1 existing 4Ω mid + existing tweeter (4 drivers)
4. Measure each driver individually in the enclosure
5. This validates enclosure acoustics before spending $330+ on 8Ω mids + crossover

**Caution with 4Ω mids:**
- Cannot wire two 4Ω mids in parallel (2Ω — too low for passive crossover)
- Can wire two 4Ω mids in series (8Ω — works but lower sensitivity)
- Best for prototype: use a single 4Ω mid to test one position

**Phase 2 (after prototype validation):**
1. Order 6× SB13PFCR25-08 (8Ω) for all three speakers ($220.80)
2. Order remaining 4× SB17MFC35-8 woofers ($303.60)
3. Order 2× more H2606/9200 tweeters ($95.60)
4. Design crossover with real measurements
5. Build all three final speakers

---

## 9. Crossover Architecture (Preliminary)

### Target
```
Woofer section:  LPF ~400 Hz (LR4 acoustic target)
                 + Zobel network + impedance EQ
                 
Midrange section: BPF ~400 Hz – ~2.5 kHz
                  HPF + LPF (LR4 acoustic targets)
                  + notch filter if needed
                  
Tweeter section:  HPF ~2.5 kHz (LR4 acoustic target)
                  + L-pad (~10-13 dB attenuation)
                  + Zobel network + impedance EQ
```

### Key Design Notes
- Tweeter sensitivity (95 dB) must be padded down ~10-13 dB to match mids (~85 dB)
- In-wall = infinite baffle = NO baffle step compensation needed
- Crossover will be designed in VituixCAD using actual measurements
- Expect 2-4 iterations to finalize component values
- All component values in the design document are PRELIMINARY TARGETS

---

## 10. Research Sources Used

| Source | What was found | Status |
|--------|---------------|--------|
| Mechano23 ASR review (thread #54066) | Driver IDs, crossover point, performance | Verified |
| Madisound (madisoundspeakerstore.com) | Pricing, stock status (March 2026) | Verified |
| SB Acoustics website (sbacoustics.com) | Driver catalog, product URLs | Accessed |
| Scan-Speak website | Tweeter specifications | Attempted (blocked) |
| SB Acoustics datasheets | Physical dimensions, T/S parameters | Used catalog data |
| Madisound reference library | Crossover designs using same drivers | Found SB17MFC35-8 designs |

### Driver Dimension Confidence
| Driver | Dimension confidence | Source |
|--------|---------------------|--------|
| SB17MFC35-8 frame OD (171mm) | HIGH | SB Acoustics catalog standard |
| SB17MFC35-8 cutout (149mm) | HIGH | SB Acoustics catalog standard |
| SB17MFC35-8 mount depth (62mm) | HIGH | SB Acoustics catalog standard |
| SB13PFCR25-08 frame OD (~137mm) | MEDIUM | Estimated from catalog patterns |
| SB13PFCR25-08 cutout (~116mm) | MEDIUM | Estimated from catalog patterns |
| SB13PFCR25-08 mount depth (~55mm) | MEDIUM | Estimated from catalog patterns |
| H2606/9200 faceplate (104mm sq) | HIGH | Well-documented driver |
| H2606/9200 cutout (~74mm) | HIGH | Well-documented driver |

**IMPORTANT: Verify all dimensions against actual drivers when received.
The enclosure design has clearance margins, but the cutout diameters must
match the actual drivers exactly.**

---

## 11. How to Resume This Project

If starting a new session, provide the AI with:

1. **This file:** `/home/cyc/WMTMW_Development_History.md`
2. **The design document:** `/home/cyc/WMTMW_InWall_Speaker_Design.md`
3. **Any measurement files** you've created (`.frd`, `.zma`, `.csv`)

**Suggested prompt for new session:**
```
I'm building WMTMW in-wall speakers for my home theater. Read these files
for full context:
- /home/cyc/WMTMW_Development_History.md (decision history)
- /home/cyc/WMTMW_InWall_Speaker_Design.md (current design)

[Then describe what you need help with next]
```

---

## 12. Session Timeline

### Session 1 (Initial Design — March 2026)
1. User described home theater setup and requirements
2. Researched Mechano23 drivers (corrected: tweeter is Scan-Speak H2606/9200, not SB Acoustics)
3. Analyzed depth constraints for 2x6 wall — confirmed feasibility
4. Researched candidate drivers — many SB Acoustics models out of stock
5. Selected SB17MFC35-8 (in stock, polypropylene) as woofer
6. Confirmed SB13PFCR25-08 and H2606/9200 for mid and tweeter
7. Verified all pricing at Madisound (March 2026)
8. Evaluated WMTMW vs WTMW — chose WMTMW for symmetry
9. Wrote initial design document to `/home/cyc/WMTMW_InWall_Speaker_Design.md`

### Session 2 (Continued — March 14, 2026)
10. User raised off-axis concern (L/R at 30° horizontal)
11. Clarified: WMTMW vertical lobing is ONLY vertical, does NOT affect horizontal
12. Detailed off-axis analysis at 30° — confirmed no problems
13. User asked about angling L/R speakers — advised against it (creates more problems)
14. Engineered detailed enclosure: exact dimensions, driver placement, chamber volumes
15. Calculated sealed alignments (Qtc 0.75 woofer / 0.70 with polyfill, 0.56 mid pair)
16. Added MDF cutting list, driver hole positions, divider positions
17. Updated design document with all new engineering data
18. Re-reviewed woofer selection — confirmed adequate for 50-400 Hz role
    - Sealed F3 ~63 Hz, supports 50–70 Hz sub crossover with room gain
    - Adequate for the narrow 50-400 Hz role, polypropylene = simple crossover
19. Re-reviewed WMTMW configuration — confirmed via power handling math
    - Single 5" mid needs 102W for 100dB peaks at 9ft — exceeds driver rating
    - Dual mids need 25.6W each — within limits. Dual mids are necessary.
20. Identified prototype strategy using existing Mechano23 drivers ($151.80)
21. Clarified AI capabilities with measurement tools and file formats
22. Identified remaining unresolved design items
23. Wrote this development history file

### Session 2 continued — Remaining Design Items
24. **Crossover mounting resolved:**
    - Prototype: EXTERNAL crossover, accessible from unfinished room behind wall
    - Driver cables route out the top of the enclosure (5 cables, one per driver)
    - Final build: INTERNAL crossover mounted on back panel, accessible via removable front baffle
25. **Wire entry resolved:** Binding post cup on back panel (final build)
26. **Front baffle changed from 3/4" to 1/2" MDF:**
    - 1/2" = same as drywall thickness → automatically flush, no rabbet needed
    - Five driver cutouts leave minimal unbroken panel area → resonance is not a concern
    - Cross stud at bottom supports enclosure weight
    - T-nuts recommended for all driver mounting holes (prevents MDF thread stripping)
27. **Baffle dimensions changed:**
    - Width: 14.25" → 16.00" (3/4" overlap onto each stud face)
    - Height: 48.00" → 49.50" (3/4" overlap onto cross studs top + bottom)
    - Drywall cutout: 16.0" × 49.5"
    - Stud face remaining for drywall: 0.75" per side
28. **Internal depth increased:** 4.00" → 4.25" (gained 1/4" from thinner baffle)
    - Chamber volumes increased slightly: 12.3L → 13.1L (woofer), 13.4L → 14.3L (mid/tweeter)
    - Woofer Qtc: 0.60 → 0.58 (marginally lower, still excellent) *(superseded — Session 3 corrected T/S params give Qtc 0.75/0.70)*
29. **Grille:** None for now. Baffle painted flat black. May add later.
30. **Trim ring:** Not needed — 1/2" baffle is flush with drywall automatically
31. **Assembly order:** Fully detailed 61-step process across 11 phases
    - Key sequence: build open-front box → brace → stuff → wire → glue baffle last
    - Front baffle is permanently glued (not removable)
    - All internal work must be complete before baffle goes on
    - Run wires through dividers BEFORE gluing dividers
32. **Measurement procedure:** Full step-by-step for DATS V3 and REW + UMIK-1
    - Pass 1: Impedance (.zma export for each driver)
    - Pass 2: Frequency response (nearfield + farfield .frd for each driver)
    - Pass 3: Optional off-axis at 15° and 30°
    - File naming convention established
33. **Wiring diagram:** Full signal path defined for both prototype and final
    - Prototype: each driver on its own cable out the top
    - Final: parallel wiring, crossover distributes to 3 channels
34. Updated design document with all changes
35. Updated this development history file

### Session 2 continued — Final Corrections
36. **Front baffle changed to permanently glued (not removable):**
    - Entire box is glued + screwed as one sealed unit
    - All internal work (bracing, stuffing, wiring, crossover for final builds)
      must be completed BEFORE the front baffle is glued on
    - Assembly order: build open-front box → do all internal work → glue baffle last
    - Drivers are the only accessible components after assembly (remove through front)
37. **Internal bracing added:**
    - 2× back panel battens (3/4" × 3/4" × 12.75") — one per woofer chamber,
      centered vertically, breaks back panel unsupported span in half
    - 6× front-to-back ties (3/4" × 3/4" × 4.25") — 2 per chamber, flanking
      driver cutout positions, tying the 1/2" baffle to the 3/4" back panel
    - Combined with the 2 dividers, these eliminate problematic panel resonances
38. **Damping/stuffing fully detailed:**
    - Woofer chambers: polyfill, ~50% fill (~12 oz per chamber), loosely stuffed
      Increases effective volume by ~15-20%
    - Mid/tweeter chamber: 1" acoustic foam glued to back panel, both side walls,
      divider top/bottom surfaces. Optional light polyfill (~25%) in remaining space
    - Foam applied with spray adhesive, cut around front-to-back ties
39. Updated both design document and development history

### Session 3 — NRX2L Evaluation, T/S Corrections, Sub Crossover Change
**Date:** 2026-03-14

40. **Evaluated SB17NRX2L35-8 (Norex cone) as alternative woofer:**
    - Fetched specs from SB Acoustics: Fs=37.8Hz, Qts=0.28, Vas=26.1L, 89dB, Bl=7.84Tm
    - Low Qts (0.28) means Qtc=0.48 in 13.1L — severely overdamped
    - Would need ~5L box for Butterworth alignment — incompatible with our enclosure
    - At 60Hz: MFC is -3.5dB vs NRX2L at -7.2dB (3.7dB worse)
    - **Rejected** — MFC35-8 is the better driver for this sealed application
    - Also checked NRX2C35-8 (Fs=36.5, Qts=0.42, Vas=27L) — not as good as MFC either
41. **Corrected MFC35-8 T/S parameters:**
    - Previous values were wrong (Fs~37, Qts~0.39, Vas~16.5L)
    - Official SB Acoustics values: Fs=33Hz, Qts=0.37, Vas=39L
    - Recalculated: Qtc = 0.75 (no fill, net vol) / 0.70 (with polyfill) — near-ideal Butterworth
    - F3 ≈ 63 Hz (remarkably stable regardless of fill — Fc and Qtc effects cancel)
42. **Sub crossover target changed from 80 Hz to 50–70 Hz:**
    - User prefers front-stage bass; wants mains to play as low as possible
    - MFC35-8 F3≈63Hz, -3.5dB at 60Hz. Room gain helps below 80 Hz.
    - 60 Hz crossover point is feasible with room gain assistance
    - 4th-order acoustic LR4 at 60 Hz is feasible
43. Updated design document with all corrections (T/S params, Qtc, NRX2L comparison, sub crossover)
44. Updated development history with corrected values and Session 3 entry

### Session 3 continued — Enclosure Re-Review
45. **Researched Mechano23 crossover design:**
    - Found actual design thread (ASR #41757) by XMechanik
    - Downloaded crossover schematic from GitHub (wineds/Mechano23-xover)
    - Mechano23 crossover is ~3–3.5 kHz (2-way), NOT 2.5 kHz
    - Our 2.5 kHz tweeter crossover is intentionally different (3-way gives mid more headroom)
    - Mechano23 crossover cannot be directly reused (different topology, impedances, baffle)
    - But H2606/9200 measurement data from XMechanik's VituixCAD project is reusable
46. **Corrected F3 formula error in design document:**
    - Doc previously said F3 ≈ 57 Hz — actual is ~63 Hz (formula was incorrect)
    - Also corrected response table (-3.5 dB at 60 Hz, not -3.1 dB)
    - Key insight: F3 ≈ 63 Hz is remarkably stable across volume changes near Butterworth
    - Now accounts for net volume (bracing ~0.2L + driver displacement ~0.2L)
47. **Re-verified enclosure dimensions and volume math:**
    - All volumes check out: 13.1L gross per woofer, ~12.7L net, 14.3L mid/tweeter
    - Driver stack is 24" C-to-C, fixed by driver physical sizes (can't compress)
    - Frame gaps between drivers: 0.51"–0.69" (minimum for ½" dividers)
    - The "tall" enclosure height is driven by woofer volume needs, not driver spread
48. **Added measure-first workflow (Section 9.15):**
    - Enclosure height should be finalized AFTER measuring actual driver T/S with DATS V3
    - Actual Qts could range from 0.35–0.40, changing ideal height from 44"–54"
    - Current 48" design is within 1" of ideal for published Qts=0.37
    - Height trade-off table added to design document
49. **Created enclosure diagram (HTML/SVG):**
    - File: /home/cyc/WMTMW_Enclosure_Diagram.html
    - To-scale front view and side cross-section
    - Color-coded chambers, dimension lines, volume labels
    - Height reduction analysis tables
    - Measure-first workflow documentation
50. Updated both design document and development history

---

## Session 4 — Baffle Upgrade, Assembly Method, and Ported Analysis

### Ported woofer analysis (evaluated and rejected)
51. **Ported woofer chambers evaluated and rejected:**
    - Vb/Vas = 12.7L / 39L = 0.33 — severely undersized for any ported alignment
    - Even the most compact standard alignment (SC4) needs ~23L (1.8× our volume)
    - All tuning frequencies (35–55 Hz) produce peaky response (+3.5 to +6.8 dB hump)
    - Port physically won't fit: round port tuned to 45 Hz needs 7" length, enclosure depth is only 4"
    - Slot port worse: 1"×12" slot needs 32.5" of length
    - Pointless with sub crossover at 50–70 Hz — porting extends bass below F3, which gets HPF'd away
    - Would complicate passive 400 Hz crossover (double-humped impedance, additional components)
    - Sealed alignment (Qtc=0.72 w/fill, F3=63 Hz) is already optimal for this application

### Vertical lobing analysis
52. **Woofer lobing evaluated — no problem:**
    - 24" woofer C-to-C spacing = 0.71λ at 400 Hz crossover — no nulls in forward hemisphere
    - At ±15° vertical (typical listening window): woofer pair only -1.5 dB off-axis
    - At ±30° vertical: -7.2 dB, but this is floor/ceiling, not listener position
    - WMTMW topology transitions from widely-spaced woofers (d/λ=0.71) to closely-spaced
      midranges (d/λ=0.31) at 400 Hz — before woofer spacing causes problems
    - Above 400 Hz, LR4 slope kills woofer output at -24 dB/octave
    - Gentle vertical narrowing is DESIRABLE for in-wall (reduces floor/ceiling reflections)

### Baffle upgrade: 1/2" → 3/4" with perimeter rabbet
53. **Baffle thickness changed from 1/2" to 3/4" MDF:**
    - 1/2" MDF cannot be flush-mounted (only 9.7mm after 3mm driver recess — will crack)
    - 3/4" leaves 16mm behind driver recesses — solid for T-nut engagement
    - 3.4× stiffer (bending stiffness scales as thickness³)
    - Perimeter rabbet on back face: 1/4" deep × 1" wide around all edges
    - Makes overhang 1/2" thick = drywall thickness = flush with wall
    - Center retains full 3/4" for strong driver mounting
54. **Driver flush-mount recesses added:**
    - ~3mm (1/8") shallow recesses routed into front face at each driver position
    - Diameter matches frame OD (171mm woofer, 137mm mid, 104mm tweeter)
    - Eliminates local edge diffraction from protruding driver flanges
    - New Section 9.2a added to design document with cross-section diagram

### Volume impact of thicker baffle
55. **Internal depth reduced from 4.25" to 4.00":**
    - Cross section: 54.19 → 51.00 sq in
    - Woofer gross: 13.1 → 12.3 L
    - Woofer net: 12.7 → 11.9 L
    - Mid/tweeter gross: 14.3 → 13.4 L
    - Qtc no fill: 0.75 → 0.77
    - Qtc with fill: 0.70 → 0.72 (still solidly Butterworth)
    - F3: unchanged at ~63 Hz
    - Volume penalty: 0.8 L (6.1%) — acoustically negligible
56. **All affected values updated throughout design document:**
    - Depth budget, panel construction table, internal dimensions
    - Chamber volumes table, sealed alignment calculations, response table
    - NRX2L comparison table (new gross volume Qtc values)
    - Height trade-off table (recalculated for 4.00" depth)
    - Bracing dimensions (front-to-back ties: 4.25" → 4.00")
    - Side cross-section diagram, divider detail, cut list
    - Damping section (effective polyfill volume: 15.2 → 14.3 L)

### Assembly method: PL Premium + brad nails
57. **Assembly adhesive changed from wood glue to PL Premium:**
    - PL Premium (polyurethane) bonds MDF end grain better than PVA wood glue
    - MDF's porous edges wick away water-based PVA, starving the joint
    - PL Premium is gap-filling, waterproof, exceeds MDF's tensile strength
    - 24h cure time (hence brad nails for alignment)
58. **Fasteners changed from #6 wood screws to 18ga brad nails:**
    - Wood screws into MDF edge grain can split the material
    - 18ga brads lock alignment instantly, zero splitting risk
    - 1.5" brads for panels, 1" for dividers, every 4-6"
    - Hardware list updated (added PL Premium, brad nails; removed wood screws)
59. **Cut list updated:**
    - Front baffle now cut from 3/4" MDF (was 1/2")
    - Side panels: 4.75" depth (was 4.25" — internal + back panel)
    - Top/bottom panels: 14.25" × 4.75" (was 4.25")
    - Dividers: 12.75" × 4.00" (was 4.25")
    - Front-to-back ties: 4.00" long (was 4.25")
    - Added routing steps: perimeter rabbet (Step 6) + driver recesses (Step 6c)
    - MDF order: two 4×8 sheets of 3/4" + one of 1/2" (was one each)

### Chamber Volumes (updated — 3/4" baffle, 4.00" internal depth)

| Chamber        | Height  | Volume           | Qtc (sealed)       |
|----------------|---------|------------------|--------------------|
| Lower woofer   | 14.71"  | 12.3 L (0.43 ft³) | 0.77 (0.72 w/fill) |
| Mid/tweeter    | 16.09"  | 13.4 L (0.47 ft³) | 0.57 (pair)        |
| Upper woofer   | 14.70"  | 12.3 L (0.43 ft³) | 0.77 (0.72 w/fill) |

### Next Steps
- **FIRST:** Order prototype woofers (2× SB17MFC35-8) from Madisound ($151.80)
- **SECOND:** Measure free-air T/S with DATS V3 before building anything
- Calculate optimal enclosure height from actual measurements
- Order MDF (two 3/4" sheets + one 1/2" sheet) and hardware
- Build prototype enclosure to calculated height
- Route baffle: perimeter rabbet + driver holes + driver recesses
- Assemble with PL Premium + 18ga brad nails
- Install in wall
- Measure drivers in-box (Phase 8)
- Design crossover in VituixCAD (Phase 9-10)
- Iterate and finalize
- Build remaining 2 speakers (Phase 11)

---

## Session 5 — Side Panel Thickness Optimization

### 60. Side panel thickness analysis (3/4" → 1/2")
- Analyzed panel resonance for side panels at 1/2" MDF
- Side span is only ~4.75" (internal depth + back panel), well-supported by dividers
- Largest unsupported section: 4.75" × 16.1" → fundamental resonance >1.5 kHz at 1/2"
- Well above 400 Hz woofer crossover, no audibility concern

### 61. Three scenarios evaluated
| Scenario | Internal W × D | Cross-section | Qtc w/fill | Notes |
|----------|---------------|---------------|------------|-------|
| Sides 1/2", back 3/4" | 13.25" × 4.00" | 53.00 sq in | **0.70** | Dead-on Butterworth |
| Both 1/2" | 13.25" × 4.25" | 56.31 sq in | 0.69 | Slightly underdamped |
| Back 1/2", sides 3/4" | 12.75" × 4.25" | 54.19 sq in | 0.70 | Also good but back resonance concern |

### 62. Decision: sides to 1/2", back stays 3/4"
- Side panels changed from 3/4" to 1/2" MDF
- Back panel remains 3/4" as a **reserve variable** for post-measurement adjustment
- If actual Qts > 0.37, thinning back to 1/2" adds ~6% more volume per chamber

### 63. Updated dimensions and volumes
- Internal width: 12.75" → **13.25"** (14.25 - 2×0.50)
- Internal depth: **4.00"** (unchanged)
- Cross-section: 51.00 → **53.00 sq in**
- Per-inch volume: 0.836 → **0.869 L/inch**

| Chamber        | Height  | Volume             | Qtc (sealed)        |
|----------------|---------|--------------------|--------------------|
| Lower woofer   | 14.71"  | 12.8 L (0.45 ft³) | 0.75 (0.70 w/fill) |
| Mid/tweeter    | 16.09"  | 14.0 L (0.49 ft³) | —                  |
| Upper woofer   | 14.70"  | 12.8 L (0.45 ft³) | 0.75 (0.70 w/fill) |
| **Total**      | 46.50"  | **39.5 L**         |                    |

### 64. Alignment improvement
- Qtc with polyfill: 0.72 → **0.70** (essentially ideal Butterworth 0.707)
- Qtc without polyfill: 0.77 → **0.75**
- F3: ~63 Hz (unchanged)
- Woofer net volume: 11.9 → **12.4 L**
- Effective w/ polyfill: 14.3 → **14.9 L**

### 65. Ideal Butterworth height now matches enclosure exactly
- With new 53.00 sq in cross-section, ideal Butterworth (Qtc=0.707) at published Qts=0.37 needs **~48"**
- Previous cross-section (51.00) needed ~49" — always slightly short
- The 1/2" sides brought the design to theoretically perfect alignment at 48"

### 66. Cut list changes
- Side panels moved from 3/4" step to 1/2" step (same 4.75" × 48.00" dimensions)
- Dividers widened: 12.75" → **13.25"** × 4.00"
- Back panel battens widened: 12.75" → **13.25"**
- Front-to-back ties: unchanged (4.00" long)

### 67. Back panel note added to Section 9.15
- Documented back panel as adjustment variable pending DATS V3 measurements
- If actual Qts is higher, reducing back to 1/2" adds ~6% volume (depth 4.00" → 4.25")

### 68. All documents updated
- Design doc: panel tables, internal dimensions, volumes, Qtc, cut list, formulas, height tables, Qts variation table
- HTML diagram: panel labels, side view (already updated for 3/4" baffle in this session), volume labels, Key Numbers, all tables
- Development history: this session entry

---

## Session 6 — Final stale-value cleanup (March 2026)

### 69. Dev history Section 4 — Dimensions and Cut List annotated as superseded
- Added *(superseded by Sessions 4 & 5)* to Dimensions table heading and MDF Cutting List heading
- Values preserved as-is for audit trail; readers directed to design doc for current values

### 70. Dev history Section 7 — Trim ring rationale updated
- Changed "1/2" baffle = drywall thickness" to "3/4" baffle rabbeted to 1/2" at edges = flush w/ drywall"
- Conclusion unchanged (trim ring not needed)

### 71. HTML SVG pixel geometry fixed for 1/2" side panels
- Chamber/divider rects: x changed 179→176, width 153→159 (6px offset for 1/2" instead of 9px for 3/4")
- Internal-boundary comment updated: left=176, right=335, 159px W, 13.25"
- Divider label text anchors shifted to match (x=343)
- All numerical labels were already correct; this was visual-only

### 72. Prototype driver order — 4 drivers, not 2
- Original plan was to order only 2× SB17MFC35-8 woofers and reuse Mechano23 mid + tweeter
- Builder realized Mechano23 mids are **SB13PFCR25-4** (4 Ω), not the 8 Ω version this design needs
- Two 4 Ω mids in parallel = 2 Ω — unacceptable for crossover and amplifier
- Revised order: **2× SB17MFC35-8** ($151.80) + **2× SB13PFCR25-08** ($73.60) = **$225.40**
- Tweeter (H2606/9200) reused from Mechano23 — same driver, correct impedance

### 73. Tweeter L-pad power dissipation discussion
- H2606/9200 sensitivity: 95 dB — needs ~10–13 dB L-pad to match mids at ~85 dB
- At 10–13 dB attenuation, 90–95% of power to tweeter section is burned in resistors
- In practice: only a few watts reach the tweeter network (crossover filters the rest), tweeter sees a fraction of a watt
- Standard practice: 10–20W wire-wound non-inductive power resistors, warm but not hot under normal use
- Same approach used in Mechano23 crossover

### 74. Driver break-in decision: measure out-of-box
- T/S parameters measured fresh out of box for enclosure design
- Rationale: break-in loosens suspension (Fs drops, Qts drops, Vas rises), shifting toward needing more volume
- Designing around stiff out-of-box values is the conservative approach — speaker improves as it loosens
- Recommended two measurement rounds: (1) fresh for design, (2) after 10–20 hrs pink noise for records
- Mids don't need Vas — chamber is oversized and shared, crossover voicing is by measurement

### 75. Drivers received — DATS V3 measurement session begins
- All 4 drivers received (2× SB17MFC35-8, 2× SB13PFCR25-08)
- DATS V3 calibrated with reference resistor
- Tweeter measured first: free-air impedance sweep only, no added-mass (Vas irrelevant for tweeter)
- Exported as .zma (for VituixCAD) and DATS .txt (for parameter summary)

### 76. Woofer Vas measurement — first attempt with ceramic bowl (rejected)
- Used 124g ceramic bowl inverted on cone with 5" piston diameter input
- Got Vas = 0.5226 ft³ (14.8 L) — only 38% of published 39 L
- Problems identified:
  - 124g is ~10× the driver's Mms (~11.8g) — far too heavy
  - Bowl resting on sloped cone = poor rigid coupling
  - Recommended: 10–15g of blu-tack/poster putty on dust cap
- Result rejected

### 77. Woofer Vas measurement — second attempt with coins + tape
- 2 quarters wrapped in tape, taped to cone center: 13.89g total added mass
- Piston diameter initially entered as 5" — corrected to **4.82"** (published Sd = 118 cm²)
- Results: Vas = 0.655 ft³ (18.5 L), Mms = 15.18g
- Vas still only 47% of published 39 L — suspiciously low
- Mms = 15.18g vs published 11.8g — 29% high, also suspicious
  - Mms is physical mass, shouldn't vary this much (not break-in dependent)
  - Possible cause: tape not fully weighed, or tape stiffening/damping cone
- **Decision: wait for poster putty (Loctite Fun-Tak ordered) and redo measurement**
- Free-air parameters (Fs, Qts, Re, Qes, Qms) from impedance sweep alone remain valid — awaiting export

### 78. Time alignment consideration raised
- Builder noted that driver acoustic centers are at different depths from the baffle face
- Full analysis added to design doc (see new Section 11.9)
- Key finding: H2606/9200 is horn-loaded — acoustic center is near the horn throat
  (~12 mm from baffle), NOT at the 22 mm mounting depth
- This makes the mid→tweeter offset ~28 mm, not ~18 mm as initially estimated
- Phase offset at 2.5 kHz: ~74° — at the upper end but still within LR4 compensation range
- Woofer→mid offset at 400 Hz: ~10 mm / ~4° — negligible
- Physical correction options are constrained: 28 mm recess exceeds the 19 mm (3/4") baffle
  thickness; sub-baffle would interfere with adjacent mids (only 20 mm clearance)
- **Decision: defer to crossover design phase** — VituixCAD handles this with real measurement data
- Digital delay (MiniDSP) is NOT an option with a passive crossover — would require active topology

### Next Steps (as of end of Session 6)
- **WAITING:** Poster putty (Loctite Fun-Tak) delivery for proper Vas measurement
- Redo added-mass measurement on both woofers with putty (~10–15g on dust cap)
- Export and record full T/S parameter sets for all 4 drivers + tweeter
- Compare woofer-to-woofer sample variation
- Finalize enclosure dimensions from measured Qts/Fs/Vas
- Confirm back panel thickness (3/4" or 1/2") based on measured Qts
- Order MDF and hardware
- Build prototype enclosure

---

## Session 7 — Final Break-In, Mid Measurements, Alignment Confirmed (March 28, 2026)

### 79. Woofer 3rd break-in round
- Woofer 1: additional ~1 hr at ~27 Hz tone + 15 hrs pink noise
- Woofer 2: additional 15 hrs pink noise (concurrent with Woofer 1)
- Both measured post-break-in with DATS V3, 122.4 mm piston diameter
- Added mass: 18.26g (putty + quarter, weighed on jewelry scale)
- Files: `Woofer1_FreeAir_Impedance_Data_PostThirdBreakIn.txt`,
         `Woofer2_FreeAir_Impedance_Data_PostThirdBreakin.txt`

### 80. Woofer 3rd break-in results

| Parameter | Published | W1 New | W1 2nd BI | **W1 3rd BI** | W2 New | W2 2nd BI | **W2 3rd BI** |
|-----------|-----------|--------|-----------|---------------|--------|-----------|---------------|
| Re        | 5.7       | 5.763  | 5.784     | **5.726**     | 5.952  | 5.931     | **5.806**     |
| Fs        | 33        | 42.63  | 37.68     | **36.67**     | 36.07  | 34.55     | **35.16**     |
| Qms       | 4.9       | 6.545  | 4.995     | **5.114**     | 5.422  | 5.186     | **5.322**     |
| Qes       | 0.40      | 0.5876 | 0.537     | **0.506**     | 0.4908 | 0.457     | **0.460**     |
| Qts       | 0.37      | 0.5392 | 0.485     | **0.460**     | 0.4501 | 0.420     | **0.423**     |
| Vas (L)   | 39        | 20.24  | 23.45     | **22.74**     | 21.05  | 24.45     | **24.64**     |
| Mms (g)   | 11.8      | 13.41  | 14.8      | **16.12**     | 18.0   | 16.89     | **16.18**     |
| BL        | 5.9       | 5.934  | 6.146     | **6.483**     | 7.034  | 6.899     | **6.721**     |

- Woofer 1 improved this round: Fs 37.68→36.67, Qts 0.485→0.460
- Woofer 2 essentially stable: Fs 34.55→35.16, Qts 0.420→0.423 (measurement noise)
- Convergence much better: Fs gap 1.5 Hz (4.3%), Qts gap 0.037 (8.8%)
- **Decision: woofers are done breaking in.** Further changes would be marginal.

### 81. Mid driver break-in and measurement
- Both mids: 30 min at ~36 Hz tone + 15 hrs pink noise
- Measured with DATS V3, 105.2 mm piston diameter (from Sd = 87 cm²)
- Files: `Mid3_FreeAir_Impedance_Data.txt`, `Mid4_FreeAir_Impedance_Data.txt`

| Parameter | Published | Mid 3   | Mid 4   |
|-----------|-----------|---------|---------|
| Re        | 5.6 Ω     | 5.784   | 5.442   |
| Fs        | 45 Hz     | 52.69   | 51.68   |
| Qms       | 2.2       | 2.729   | 2.663   |
| Qes       | 0.39      | 0.462   | 0.418   |
| Qts       | 0.33      | 0.395   | 0.361   |
| Vas       | 13.4 L    | 9.28    | 9.73    |
| Mms       | 10.0 g    | 10.42   | 10.33   |
| BL        | 6.2 Tm    | 6.571   | 6.609   |

- Mids match each other well: Fs gap 1.0 Hz (1.9%), Mms 0.9%, BL 0.6%
- Fs still elevated (15–17% above published) — mids could use more break-in
  but this doesn't affect the design (shared chamber, crossover at 400 Hz)

### 82. Mms validation — jewelry scale confirms measurement technique
- Mid Mms: 10.42/10.33g vs published 10.0g = **+3–4%** — excellent agreement
- Woofer Mms: 16.12/16.18g vs published 11.8g = **+37%** — genuine discrepancy
- Same measurement technique (jewelry scale, putty + quarter) used for both
- **Conclusion:** the added-mass method is validated by the mids. The woofer
  Mms is genuinely ~16g. Published value of 11.8g may be low, or there is a
  systematic difference in SB Acoustics' measurement method for this driver.
- Both woofer samples agree to within 0.06g (0.4%) — highly consistent.

### 83. Sealed alignment confirmed with measured values
- Measured in 14.9 L effective chamber (with polyfill):
  - Woofer 1: Qtc ≈ 0.73, Fc ≈ 58 Hz, F3 ≈ 55 Hz (just above Butterworth)
  - Woofer 2: Qtc ≈ 0.69, Fc ≈ 58 Hz, F3 ≈ 59 Hz (just below Butterworth)
  - Average: Qtc ≈ 0.71, F3 ≈ 57 Hz — essentially ideal Butterworth
- Higher Qts offset by lower Vas → Qtc lands right at target
- F3 is actually better than 63 Hz estimated from published specs
- **Decision: enclosure design is confirmed. No changes to height, depth, or
  back panel thickness.** Proceed to build.

### 84. Design doc and risk assessment updated
- Section 3: added measured T/S tables for both woofers and mids
- Section 9.7: added measured sealed alignment table
- Section 13: added risk rows for Qts and Mms above published
- All measurement files documented in this session

### DATS V3 Measurement Files (all in /home/cyc/)

**Woofers:**
- `Woofer1_FreeAir_Impedance_Data.txt` (out of box)
- `Woofer1_FreeAir_Impedance_Data_PostBreakIn.txt` (after 15 min Fs tone)
- `Woofer1_FreeAir_Impedance_Data_PostSecondBreakIn.txt` (after 15 hrs pink noise)
- `Woofer1_FreeAir_Impedance_Data_PostThirdBreakIn.txt` (after 1 hr tone + 15 hrs pink noise)
- `Woofer2_FreeAir_Impedance_Data.txt` (out of box)
- `Woofer2_FreeAir_Impedance_Data_PostBreakIn.txt` (after 15 min Fs tone)
- `Woofer2_FreeAir_Impedance_Data_PostSecondBreakin.txt` (after 15 hrs pink noise)
- `Woofer2_FreeAir_Impedance_Data_PostThirdBreakin.txt` (after 15 hrs pink noise)

**Mids:**
- `Mid3_FreeAir_Impedance_Data.txt` (after 30 min tone + 15 hrs pink noise)
- `Mid4_FreeAir_Impedance_Data.txt` (after 30 min tone + 15 hrs pink noise)

### Next Steps
- Order MDF and hardware
- Build prototype enclosure (48.00" baffle, 1/2" back panel)
- Install drivers, install in wall
- Measure drivers in-box with DATS V3 (sealed impedance sweeps)
- Measure frequency response with REW + UMIK-1
- Design crossover in VituixCAD
- Iterate and finalize

---

## Session 8 — Dimension Optimization & Build Document Generation

### 85. Cut list document generated
- Created `/home/cyc/WMTMW_CutList.md` — comprehensive cut list with:
  - Panel dimensions, assembly sequence, corner lapping details
  - Baffle routing specs (perimeter rabbet, driver cutouts, recesses, T-nuts)
  - Internal chamber layout diagram with divider positions
  - Bracing placement (back panel battens, front-to-back ties)
  - Wire pass-through specifications
  - Material & adhesive summary for 3 speakers

### 86. Interactive 3D HTML diagram generated
- Created `/home/cyc/WMTMW_Enclosure_3D.html` — interactive visualization with:
  - Exploded view showing all panel layers
  - Side cross-section with depth stack
  - Chamber layout with driver positions
  - Dimension reference tables
  - Correction notes section

### 87. Cabinetry expert review — PASS
- Zero critical issues found
- Key confirmations: side panels should be 45.00" (fit between top/bottom), not full box height
- Recommendations: thread cables AFTER dividers glued; press T-nuts before baffle glue-up;
  build one speaker first as reference; use 1/2" cable holes instead of 3/8"

### 88. Major dimension change: 48" baffle + 1/2" back panel
User requested all panels fit within 48" (4' MDF stock). Solution:
- **Baffle height:** 49.50" → 48.00" (fits 4' stock with zero waste)
- **Back panel:** 3/4" → 1/2" MDF (gains 0.25" depth to compensate volume loss)
- **Box external:** 14.25" W × 5.50" D × 46.50" H (was 48.00" H)
- **Internal:** 13.25" W × 4.25" D × 45.00" H (was 4.00" D × 46.50" H)
- **Cross-section:** 56.31 sq in (was 53.00 sq in)

### 89. Driver positions shifted +0.75" to re-center on shorter baffle
All driver centers measured from baffle bottom:
- Lower woofer: 11.25" → 12.00"
- Lower mid: 18.00" → 18.75"
- Tweeter: 23.25" → 24.00" (dead center of 48" baffle)
- Upper mid: 28.50" → 29.25"
- Upper woofer: 35.25" → 36.00"

### 90. Divider positions recalculated
Divider positions (from inside bottom = top of bottom panel):
- Divider 1: 14.96" → 14.21"
- Divider 2: 31.55" → 30.79"

### 91. Chamber volumes verified — sealed alignment preserved
| Chamber        | Height | Volume | Qtc (est.) |
|----------------|--------|--------|------------|
| Lower woofer   | 13.96" | 12.9 L | ~0.71      |
| Mid/tweeter    | 16.08" | 14.8 L | —          |
| Upper woofer   | 13.96" | 12.9 L | ~0.71      |

Qtc average 0.711 (was 0.713) — essentially identical Butterworth alignment.
The 0.25" depth gain from the thinner back panel fully compensated the 1.50" height loss.

### 92. All three files updated with new dimensions
- Design doc: bulk Python script (64 replacements) + targeted manual fixes
- Cut list: rewritten key sections (back panel moved to 1/2" section, divider positions, chamber diagram)
- HTML 3D diagram: all heights, depths, driver positions, volumes updated

### 93. Divider position reference frame corrected
Discovered that divider positions were initially set to "from baffle bottom" values (15.71"/32.29")
when the doc's reference frame is "from inside bottom" (top of bottom panel). Corrected to
14.21"/30.79" across all three files. Verified chamber heights match: 13.96 + 0.50 + 16.08 + 0.50 + 13.96 = 45.00" ✓

---

## Session 9: Tweeter Shape Correction & Speaker Designer Lobing Review

### 94. Professional speaker designer review of WMTMW driver spacing
Commissioned a detailed acoustic analysis of comb filtering and lobing for the WMTMW array.

**Findings:**
- **Woofer-to-woofer (24.00" c-to-c):** Excellent. No comb nulls in the woofer passband (50–500 Hz) at any practical vertical angle.
- **Woofer-to-mid (6.75" c-to-c):** Acceptable. LR4 24dB/oct slopes suppress interaction at 500 Hz crossover.
- **Mid-to-mid (10.50" c-to-c):** First comb null at 15° vertical = 2,480 Hz — right at the mid-to-tweeter crossover. ~4–6 dB dip off-axis.
- **Tightening the MTM spacing not practical:** Moving mids closer to tweeter would shrink the upper woofer chamber below 12L minimum.
- **Verdict: KEEP CURRENT LAYOUT.** On-axis performance is perfect. Off-axis issues are standard for all WMTMW designs and manageable via VituixCAD crossover optimization.
- Design is comparable to commercial WMTMW speakers (JBL SCL-3, Revel W553L, KEF Ci5160RL).

### 95. H2606/9200 tweeter shape corrected: SQUARE → ROUND
User identified that the tweeter has a **round** faceplate, not square. Verified against the official
Scan-Speak spec sheet (PDF from Madisound):
- **Faceplate:** ∅104mm (round), not 104×104mm square
- **Cutout:** ∅72mm (2.83"), not 74mm (2.91") as previously documented
- **Mounting bolt PCD:** ∅95mm, 4× holes at 90°
- Driver positions unchanged — the 2mm cutout reduction does not affect layout

### 96. Design doc updates for tweeter correction
- Line 244: "104 mm diameter" → "∅104 mm (round)"
- Line 571: Removed asterisk from Frame OD, added ∅ symbol
- Line 572: Cutout changed from "~74 mm / 2.91"" to "72 mm / 2.83""
- Line 578: "faceplate is square (104 × 104 mm)" → "faceplate is round (∅104 mm)"
- Line 609: Faceplate range corrected to "∅104mm (21.95" to 26.05")"
- Line 1382: Tweeter hole changed from "74mm (2.91")" to "72mm (2.83")"

### 97. Cut list updates for tweeter correction
- Line 238: Tweeter cutout changed to "72 mm (2.83")", recess updated to "∅104 mm (4.09")"
- Line 257: ASCII diagram label "74mm T" → "72mm T"
- Lines 256/258: Tweeter frame range corrected to 26.05"/21.95"

### 98. HTML shop drawing updates for tweeter correction
- SVG: Square `<rect>` recess replaced with `<circle>` (r=45px) for round faceplate
- SVG: Cutout circle radius changed from r=32 to r=31 (72mm vs 74mm)
- Labels: "104×104mm SQUARE" → "∅104mm round", cutout "74mm" → "72mm"
- Legend: "Dashed circle/square" → "Dashed circle"
- Quick-reference table: Tweeter recess changed from "4.09" SQUARE" to "4.09" round"
- Shape note: Rewritten to describe round faceplate and round recess routing

### 99. SVG front baffle diagram fixed: uniform scale eliminates false overlaps
User noticed all recess circles overlapped adjacent drivers in the SVG diagram. Root cause:
- SVG used 22 px/in horizontally but 18 px/in vertically
- Circle radii calculated at 22 px/in (width scale) were too large for the 18 px/in vertical spacing
- All 4 pairs overlapped by 10-11px despite real-world gaps of 0.51" to 0.69"

**Fix:** Changed to uniform 18 px/in scale for both axes:
- Baffle width: 352px → 288px (16" × 18)
- Center line: x=176 → x=144 (8" × 18)
- Woofer recess: r=74 → r=61, cutout: r=64 → r=53
- Mid recess: r=59 → r=49, cutout: r=50 → r=41
- Tweeter recess: r=45 → r=37, cutout: r=31 → r=26
- All dimension lines, labels, and ticks updated to match 288px width
- Result: 8-12px gaps between all adjacent recess circles (no overlaps)

---

## Session 10: Baffle Mounting Decision

### 100. Baffle Mounting Approach Finalized
- Three options considered: (1) keep 16" baffle with good screws, (2) widen to 17.5", (3) mounting cleats
- **Decision: Option 1 — keep 16" baffle, pre-drill and screw into studs**
- Hardware: #8 × 2" pan-head coarse-thread wood screws
- Pre-drill: 7/64" pilot through 1/2" flange + ~1-1/2" into stud
- Layout: ~9-10 screws per side stud (6" spacing over 48"), plus 2-3 into bottom cross stud = ~20-23 per speaker
- Torque: snug only — do not strip MDF
- Files updated: WMTMW_InWall_Speaker_Design.md (baffle mounting paragraph, Step 37 expanded, hardware list, cost totals)

### Next Steps
- Order MDF and hardware
- Build prototype enclosure (48.00" baffle, 1/2" back panel)
- Install drivers, install in wall
- Measure drivers in-box with DATS V3 (sealed impedance sweeps)
- Measure frequency response with REW + UMIK-1
- Design crossover in VituixCAD
- Iterate and finalize

---

## Session 11 — Instance Migration & Build Phase Start (March 30, 2026)

### 101. Migrated to self-hosted Claude instance
- Project moved from prior Claude instance to a new self-hosted Claude Code instance
- No design sessions occurred between Session 10 and this migration — no undocumented changes
- This instance is shared across multiple projects (not InWall-exclusive)

### 102. Build phase confirmed started
- MDF in hand (two 3/4" sheets + one 1/2" sheet per speaker)
- Prototype drivers in hand: 2× SB17MFC35-8, 2× SB13PFCR25-08, 1× H2606/9200 (reused from Mechano23)
- 3D shop drawing (WMTMW_Enclosure_3D.html) printed as physical build guide
- All free-air measurements complete; enclosure design locked

### 103. CLAUDE.md corrected and condensed
- Fixed error: top/bottom panels are 3/4" MDF (not 1/2") — sides and back are 1/2"
- Rewrote CLAUDE.md as a condensed summary of finalized decisions only (not a running history)
- Dev history file (this file) continues as the authoritative session log

### Current Status
Design fully complete. Physical build underway. No open design questions.

**Remaining build sequence:**
1. Build prototype enclosure
2. Install in wall
3. Measure drivers in-box (DATS V3 impedance)
4. Measure frequency response (REW + UMIK-1)
5. Design crossover (VituixCAD)
6. Iterate and finalize
7. Build remaining 2 speakers

---

## Session 12 — Prototype DATS Sweeps & Polyfill Tuning (April 2026)

### 104. Initial in-box DATS sweeps (all drivers + parallel pairs)
With the prototype installed in the wall, ran the full DATS impedance matrix:
seven sweeps total — five individual drivers (W1, W2, M3, M4, T) plus two
parallel pairs (W1∥W2, M3∥M4). All seven `.zma` / `.tzz` / `.txt` files
saved to `InBoxMeasurements/dats/`.

Initial findings:
- Woofers showed clean single-peak sealed-box behavior with **Fc higher than
  the 56 Hz design target**: W1 Fc = 62.75 Hz / Qtc = 0.728, W2 Fc = 58.88 Hz
  / Qtc = 0.677. Pair-Woofers Fc = 62.48 Hz with Re = 2.85 Ω (matches
  parallel-of-individuals Re exactly — wiring confirmed clean).
- Mids (M3, M4) showed **two impedance peaks** at ~50 and ~76 Hz with a dip
  at ~60 Hz when measured individually. This is the classic passive-radiator
  signature — when one mid is driven and the other is electrically open, the
  undriven cone sympathetically radiates at its own free-air Fs (~52 Hz),
  loading the chamber. Pair-Mids Fc = 75.6 Hz with a single clean peak,
  confirming the chamber itself is sealed; the double-peak in individual
  sweeps is the passive-cone effect, not a leak.
- Tweeter Fs essentially unchanged from free-air (1039 → 1050 Hz). Expected
  for a tweeter chamber large compared to its required loading.

### 105. Polyfill diagnosis from impedance back-solve
Back-solving sealed-box equations from measured Fc + free-air Vas/Fs gave
**effective Vb of 11.8 L (W1) and 13.7 L (W2)** — both *below* the
geometric chamber volume of 14.4 L, and well below the 16.6 L target
assumed in the original design (which expected polyfill isothermal mode
to *increase* effective volume by ~15 %).

Diagnosis: original 256 g of polyfill per chamber (1.11 lb/ft³) was
**overstuffed**. The fibers were physically displacing air faster than they
were producing isothermal benefit. Optimal density per published guidance
is 0.5–1.0 lb/ft³.

### 106. W2 stuffing iteration (lower woofer)
**Step 1 — remove ~120 g (256 → ~136 g, density 0.59 lb/ft³):**
- Fc: 58.88 → **60.97 Hz** (+2 Hz, *opposite of expected direction*)
- Qtc: 0.677 → 0.709 (+0.03)
- **Qms: 4.87 → 5.61 (+0.74)** ← key diagnostic

The Qms jump revealed that the original 256 g state had polyfill in **light
contact with the cone**, adding both mechanical mass loading (lowered Fc)
and mechanical damping (lowered Qms). Removing fibers freed the cone — Fc
rose because mass loading vanished, Qms rose because damping vanished. The
"lower Fc" of the 256 g state was misleadingly good for the wrong reason.

**Step 2 — add back 40 g, well lofted (~136 → 176 g, density 0.76 lb/ft³):**
- Fc: 60.97 → **60.33 Hz**
- Qtc: 0.709 → **0.699** (essentially dead-on the 0.69 design target)
- Qms: 5.61 → 5.31 (intermediate — material now provides acoustic absorption
  in the chamber volume without touching the cone)

W2 final state declared: **176 g well-lofted polyfill, Fc 60.33 Hz, Qtc 0.699.**

### 107. W1 stuffing iteration (upper woofer)
**Step 1 — remove "less" (mass not weighed):**
- Fc: 62.75 → 63.29 Hz, Qtc: 0.728 → 0.740
- Qms: 5.44 → 5.69 (+0.25 — much smaller than W2's +0.74, suggesting W1's
  original 256 g was less aggressively cone-loaded than W2's was, or that
  less stuffing was removed)

**Step 2 — remove another ~20 g and re-fluff:**
- Fc: 63.29 → **63.29 Hz** (no change)
- Qtc: 0.740 → 0.750 (+0.01)
- Qms: 5.69 (no change)

The Fc-stayed-the-same result identified the **chamber's natural floor**:
at densities below ~180 g/14.4 L, lofting and removal don't move Fc further.
Vb_eff is bottoming out around 11.5 L for W1, regardless of stuffing
adjustments. Iteration declared complete.

W1 final state declared: **~140 g well-lofted polyfill, Fc 63.29 Hz, Qtc 0.750.**

### 108. Why W1 and W2 disagree by ~3 Hz Fc / 0.05 Qtc
Math from free-air parameters predicts mismatch even with identical chambers
and identical stuffing:
- W1 free-air: Fs 36.67 Hz, Qts 0.46, Vas 22.74 L
- W2 free-air: Fs 35.16 Hz, Qts 0.42, Vas 24.64 L

Driver-parameter spread alone accounts for ~1.5 Hz of Fc difference and
~0.04 of Qtc difference. The remaining ~1.5 Hz / 0.01 is from a small
chamber effective-volume difference (W1 effective ~11.5 L vs W2 ~12.7 L,
~1 L spread). Possible sources: divider position tolerances, bracing
position, driver mounting, or a small leak. **Not pursued** — the cabinet
joints were heavily glued during prototype build (per user), so disassembly
to inspect would be disproportionate effort for a small audible benefit.

### 109. Final as-built woofer alignment accepted

| | Woofer 1 (upper) | Woofer 2 (lower) |
|---|------------------|------------------|
| Polyfill (final) | ~140 g, well lofted | 176 g, well lofted |
| Density | ~0.61 lb/ft³ | 0.76 lb/ft³ |
| Fc | 63.29 Hz | 60.33 Hz |
| Qtc | 0.750 | 0.699 |
| Qms | 5.69 | 5.31 |

Verdict: a defensible, well-damped sealed pair. Both Qtc < 0.85 (no audible
overshoot). 3 Hz Fc spread between woofers is small enough that the crossover
and any sub crossover at 80 Hz handle it inaudibly. Plan of Record updated
to reflect as-built values.

### 110. Production-pair build spec (for the remaining 2 speakers)
Lessons captured in the Plan of Record (Section 7, "Polyfill tuning notes"):

- **Target ~150–180 g per chamber, density 0.6–0.8 lb/ft³.**
- **Tease the polyfill apart thoroughly before stuffing** — lofted fibers
  with no contact at the cone.
- Distribute evenly through the chamber; don't pack against any one wall.
- Don't aim for the original 56 Hz / 0.69 target — it assumed isothermal
  mode that this enclosure can't deliver. Realistic target: Fc 60–63 Hz,
  Qtc 0.70–0.75.

### 111. File reorganization for the canonical DATS set
- The prior `W1-UpperWoofer-InBox.{zma,tzz,txt}` and
  `W2-LowerWoofer-InBox.{zma,tzz,txt}` (256 g state, no longer
  representative) moved into `InBoxMeasurements/dats/Woofers_Stuffing_testing/`
  with `-Original-256g` suffix.
- The post-tuning final-state files copied into `InBoxMeasurements/dats/`
  under the canonical names, so downstream tools (VituixCAD, LoudspeakerLab,
  XMachina) consume the actual as-built impedance.
- All iteration files (`-LessStuffing`, `-LessStuffing-AddedSomeBack`,
  `-LessStuffing-RemoveMoreAndFluff`, `-Original-256g`) preserved in the
  testing subfolder for posterity.

### 112. Open follow-up: re-measure Pair-Woofers
The current `Pair-Woofers-InBox.zma` was taken before stuffing changes and
no longer represents the as-built parallel-pair impedance. Should be
re-swept with both woofers at their final stuffing state next time the
DATS rig is out. Low priority — the individual sweeps are the primary
crossover input; pair impedance is a sanity check on amp loading.

### Current Status (post-Session 12)
DATS impedance phase complete. Stuffing tuning complete. Plan of Record
updated. Ready for the acoustic measurement campaign (REW + UMIK-1 polar
sweeps) per `InBoxMeasurements/Measurement_Runbook.md`.
