---
name: arrangement-coach
description: "Full arrangement structure guide for Ableton Arrangement View. Covers section templates, 5-genre bar maps, two workflows (build from scratch + promote Session View loops), drop/build transition patterns, master automation, and MCP tool workflow."
genre: edm, house, techno, deep-house, lo-fi, pop, hip-hop, emotional-house, uk-garage
---

# Arrangement Coach

## 1. When to Use This Skill

Trigger phrases: "arrange the track", "build a full arrangement", "add sections", "structure the song", "where should the drop be", "add a buildup", "how long should the breakdown be", "promote my loops to an arrangement", "take these clips and build a song", "turn my session into an arrangement".

Two use cases — pick the right workflow from Section 4:
- **Build from scratch** — tracks exist but no arrangement clips yet; create structure from a genre template
- **Session → Arrangement promotion** — Session View clips already exist; map them into a structured arrangement

## 2. Section Templates

| Section | Typical Bars | Energy | Content |
|---------|-------------|--------|---------|
| Intro | 8–16 | Low | Drums only or drums+bass. No pads, no leads. Let the listener orient. |
| Buildup | 8–16 | Rising | Add layers bar by bar. Filter opens. Hi-hats added. Snare roll or riser on last 4 bars. |
| Drop | 16–32 | Peak | All elements: drums, bass, pad, lead/arp. Full velocity. Tight, punchy mix. |
| Breakdown | 8–16 | Low | Strip to pad/melody only. Remove drums entirely. Space for tension. |
| Buildup 2 | 4–8 | Rising | Shorter than first. Greater urgency. Same filter-sweep pattern. |
| Drop 2 | 16–32 | Peak | Same as Drop 1 or a variation (alternate bass, extra texture). |
| Verse | 8–16 | Medium | Core groove established. Melodic content present. (Pop/Lo-fi) |
| Chorus | 8 | Peak | All elements at full velocity. Memorable hook. (Pop/Lo-fi) |
| Bridge | 8 | Medium | Contrast section — different chord, different energy. (Pop) |
| Outro | 8–16 | Falling | Remove layers one by one. End on drums only or full mute. |

## 3. Genre Structures

Formula: Beats Start = (Start Bar − 1) × 4. Use `start_bar`/`end_bar` directly in `create_arrangement_midi_clip`.

**House (128 BPM, ~5.5 min, ~136 bars):**

| Section | Start Bar | End Bar | Beats Start |
|---------|-----------|---------|-------------|
| Intro | 1 | 16 | 0.0 |
| Buildup 1 | 17 | 32 | 64.0 |
| Drop 1 | 33 | 64 | 128.0 |
| Breakdown | 65 | 80 | 256.0 |
| Buildup 2 | 81 | 88 | 320.0 |
| Drop 2 | 89 | 120 | 352.0 |
| Outro | 121 | 136 | 480.0 |

**Techno (138 BPM, ~7 min, ~168 bars):**

| Section | Start Bar | End Bar | Beats Start |
|---------|-----------|---------|-------------|
| Intro | 1 | 32 | 0.0 |
| Buildup 1 | 33 | 48 | 128.0 |
| Drop 1 | 49 | 80 | 192.0 |
| Breakdown | 81 | 96 | 320.0 |
| Buildup 2 | 97 | 104 | 384.0 |
| Drop 2 | 105 | 152 | 416.0 |
| Outro | 153 | 168 | 608.0 |

**Deep House (122 BPM, ~6.5 min, ~164 bars):**

| Section | Start Bar | End Bar | Beats Start |
|---------|-----------|---------|-------------|
| Intro | 1 | 16 | 0.0 |
| Groove Intro | 17 | 32 | 64.0 |
| Breakdown 1 | 33 | 48 | 128.0 |
| Buildup | 49 | 56 | 192.0 |
| Drop | 57 | 96 | 224.0 |
| Breakdown 2 | 97 | 112 | 384.0 |
| Buildup 2 | 113 | 120 | 448.0 |
| Drop 2 | 121 | 148 | 480.0 |
| Outro | 149 | 164 | 592.0 |

**Lo-fi Downtempo (85 BPM, ~4 min, ~80 bars):**

| Section | Start Bar | End Bar | Beats Start |
|---------|-----------|---------|-------------|
| Intro | 1 | 8 | 0.0 |
| Verse 1 | 9 | 24 | 32.0 |
| Chorus 1 | 25 | 32 | 96.0 |
| Verse 2 | 33 | 48 | 128.0 |
| Chorus 2 | 49 | 64 | 192.0 |
| Outro | 65 | 80 | 256.0 |

No drops — energy builds through subtle layering and variation. Keep all velocities 10–15 below standard defaults for warmth (e.g. kick 95, snare 85, bass 75, pad 55).

**Emotional House / UK Garage (Fred again, Bicep, Four Tet — 108–130 BPM, ~5 min, ~120 bars):**

Characteristic sound: long sparse intro, vocal-led breakdown at emotional peak, no hard EDM drop formula. Energy builds through texture layering, not filter sweeps. Velocity restraint throughout — nothing hits full tilt until the peak.

| Section | Start Bar | End Bar | Beats Start |
|---------|-----------|---------|-------------|
| Intro | 1 | 8 | 0.0 |
| Verse 1 | 9 | 24 | 32.0 |
| Pre-peak | 25 | 32 | 96.0 |
| Peak | 33 | 64 | 128.0 |
| Breakdown | 65 | 72 | 256.0 |
| Rebuild | 73 | 80 | 288.0 |
| Peak 2 | 81 | 112 | 320.0 |
| Outro | 113 | 128 | 448.0 |

Layer guidance:
- Intro: texture/arp only — no drums, no bass
- Verse 1: piano + bass + texture; drums enter quietly (loose pattern, low velocity)
- Pre-peak: all tracks enter; keep drums at 70–80 velocity, pad underneath
- Peak: full kit (tight pattern) + piano hi register + bass + pad hi-reg + arp; max velocity kick ~95 (not 110 — this genre stays warm)
- Breakdown: piano + vocal only; everything else silent; this is the emotional moment
- Rebuild: loose drums + bass + pad re-enter; same texture as pre-peak
- Peak 2: same as Peak 1 or slight variation
- Outro: strip to piano + pad + texture; fade over 8 bars

**Pop / Hip-hop (95 BPM, ~3.5 min, ~84 bars):**

| Section | Start Bar | End Bar | Beats Start |
|---------|-----------|---------|-------------|
| Intro | 1 | 8 | 0.0 |
| Verse 1 | 9 | 24 | 32.0 |
| Pre-Chorus | 25 | 28 | 96.0 |
| Chorus 1 | 29 | 36 | 112.0 |
| Verse 2 | 37 | 52 | 144.0 |
| Pre-Chorus 2 | 53 | 56 | 208.0 |
| Chorus 2 | 57 | 64 | 224.0 |
| Bridge | 65 | 72 | 256.0 |
| Chorus Out | 73 | 84 | 288.0 |

8-bar sections; energy peaks at every chorus. Intro and verse are stripped; chorus gets all elements.

## 4. Tool Workflow

Choose the path that matches the situation.

---

### Path A — Build from scratch
*(Tracks exist but arrangement is empty)*

**Step 1 — Read current state**
`get_session_info` to see tracks. `get_arrangement_info` to confirm arrangement is empty or note existing clips.

**Step 2 — Select template**
Choose genre structure from Section 3. Note `start_bar`/`end_bar` for each section.

**Step 3 — Confirm plan before executing**
State the full mapping before placing any clips:
> "I'll create a [genre] arrangement with [N] sections across [M] tracks:
> - Intro (bars 1–16): Kick + Bass tracks
> - Buildup 1 (bars 17–32): Kick + Bass + filter automation
> - Drop 1 (bars 33–64): Kick + Bass + Pad + Lead
> Proceed?"

Wait for confirmation.

**Step 4 — Create section clips**
For each section × each track:
```
create_arrangement_midi_clip(
  track_index=<1-based>,
  start_bar=<section start>,
  end_bar=<section end>,
  name="<Section> <Role>"   ← e.g. "Drop Kick", "Buildup Bass"
)
```
Name all clips — required for `clip_name` addressing in `manage_clip_automation`.

**Step 5 — Fill clips with notes**
```
add_notes_to_arrangement_clip(track_index, clip_name="Drop Kick", notes=[...])
```
Use genre-edm-production patterns: kick at beats 0, 1, 2, 3 per bar; snare at 1, 3; 8th-note hats every 0.5 beats.
For bass: root note per chord, held 3.8 beats, starting at bar boundaries (0.0, 4.0, 8.0…).
For breakdown sections: fill pad/melody tracks only; leave drum track clips empty.
MIDI map (verify against your kit): kick=C1/36, snare=D1/38, closed hat=F#1/42, open hat=A#1/46.

**Step 6 — Add buildup automation**
```
manage_clip_automation(
  track_index=<pad or bass track>,
  clip_name="Buildup Bass",
  action="add_point",
  parameter_name="Filter Cutoff",   ← use parameter_name (string), NOT parameter_id
  time_in_beats=0.0, value=0.05
)
manage_clip_automation(..., time_in_beats=<buildup length in beats>, value=1.0)
```
Result: full filter sweep from nearly-closed to wide-open over the buildup.

Note: the correct MCP parameter key is `parameter_name` (a human-readable string like "Filter Cutoff", "volume", "panning"). Use `get_device_parameters` to see the available parameter names for a specific device. The automation-coach skill incorrectly shows `parameter_id` in its code example — ignore that; `parameter_name` is the correct key.

**Step 7 — Verify**
`get_arrangement_info` to confirm clip positions and lengths.
`control_arrangement_view(action="play")` to audition.

---

### Path B — Session → Arrangement promotion
*(User has Session View clips; promote them into a structured arrangement)*

**Step 1 — Assess current state**
`get_session_info` to read all tracks and their clip slots. Note which slots have clips, their lengths, and what role each track plays (drums, bass, pad, etc.).

**Step 2 — Select template and map clips**
Choose genre structure from Section 3. Map each existing session clip to sections:
e.g. "4-bar drum loop → Intro, Drop 1, Drop 2; 8-bar bass loop → Drop 1 and Drop 2 only; pad clip → Breakdown only"

**Step 3 — Confirm plan before executing**
State the mapping explicitly before touching anything:
> "I'll promote your session clips into a [genre] arrangement:
> - Drum clip (slot 1) → Intro bars 1–16, Drop 1 bars 33–64, Drop 2 bars 89–120
> - Bass clip (slot 1) → Drop 1 bars 33–64, Drop 2 bars 89–120
> - Pad clip (slot 1) → Breakdown bars 65–80 only
> Buildup sections (bars 17–32, 81–88) will be created new.
> Proceed?"

Wait for confirmation.

**Step 4 — Place session clips into arrangement**
```
duplicate_clip_to_arrangement(
  track_index=<1-based>,
  clip_index=<1-based session slot>,     ← clip_index, NOT clip_slot_index
  destination_bar=<section start bar>    ← destination_bar, NOT start_bar
)
```
Each call places **one copy** of the clip at the destination — the clip does NOT auto-loop to fill the section. Calculate how many placements you need: `section_length_bars / clip_length_bars`. For a 4-bar clip covering a 32-bar drop, that is 8 calls at bars N, N+4, N+8 … N+28. Use a loop rather than listing every call manually.

**Audio clips:** `duplicate_clip_to_arrangement` only works for session MIDI clips. Audio clips already in the arrangement cannot be moved or placed via MCP tools — they must be repositioned manually in Ableton's clip view. Flag this to the user before executing; do not attempt to move audio arrangement clips programmatically.

**Step 5 — Create transition clips**
For buildup sections not covered by existing session clips, create new clips:
```
create_arrangement_midi_clip(track_index, start_bar=17, end_bar=32, name="Buildup Kick")
add_notes_to_arrangement_clip(track_index, clip_name="Buildup Kick", notes=[...])
```
Add progressive hi-hat layering and a snare roll for the last 4 bars of the buildup.

**Step 6 — Verify**
`get_arrangement_info` to confirm all clip positions.
`control_arrangement_view(action="play")` to audition.

## 5. Clip Naming Convention

Always name clips `"<Section> <Role>"` format:
- "Intro Kick", "Intro Bass"
- "Buildup Kick", "Buildup Bass"
- "Drop Kick", "Drop Bass", "Drop Pad", "Drop Lead"
- "Breakdown Pad", "Breakdown Melody"
- "Outro Kick"

Why: `manage_clip_automation(clip_name="Buildup Bass")` targets the exact clip without needing its numeric `clip_index` — essential when many clips share a track across many sections.

## 6. Drop/Build Transition Checklist

**Intro → Buildup:**
- Add hi-hat layer at vel 85 on-beat, vel 65 off-beat.
- Start filter sweep: `manage_clip_automation` on bass/pad, value 0.05 → 1.0 over buildup length.

**Buildup → Drop:**
- All tracks enter at full pattern (drums + bass + pad + lead).
- Reset filter to 1.0 at beat 0.0 of drop clip.
- If reverb/delay built up: step-automate wet to 0.05 at drop beat.

**Drop → Breakdown:**
- Leave drum track arrangement clips empty, or use `delete_notes_from_arrangement_clip` on drum tracks.
- Keep pad and melody clips only.
- Lower pad velocity to 55–65 for intimacy.

**Breakdown → Buildup 2:**
- Kick re-enters on bar 1 of buildup; snare+hat enter on bar 2.
- Begin filter sweep again (same 0.05 → 1.0 pattern, compressed to fewer bars).

## 7. Master Automation (Section-Level Volume Shaping)

After all clips are placed and notes finalized, add subtle section-level volume rides:

| Section | Volume Adjustment | Rationale |
|---------|-----------------|-----------|
| Intro | 0 dB | Reference level |
| Buildup (last 4 bars) | +0.5 to +1 dB | Slight push into the drop |
| Drop | 0 dB | Full impact |
| Breakdown | -1 to -2 dB | Intimacy and perceived space |
| Buildup 2 | 0 → +0.5 dB | Rise back to peak |
| Outro (last 8 bars) | Fade to silence | Remove layers, then mute |

Apply via `manage_clip_automation` with `parameter_name="volume"` on the target track's arrangement clips (note: for MIDI tracks, automate the instrument's output volume parameter or use track-level automation in Ableton, as MIDI clip envelopes do not natively control mixer volume).
Keep adjustments to ±1–3 dB maximum — larger swings overwhelm the mix and mask dynamics.
Do not apply master automation until all clip notes are finalized.

## 8. Don'ts

- Don't place clips without calling `get_arrangement_info` first — overlapping existing clips silently truncates them
- Don't skip naming clips — unnamed clips cannot be targeted by `manage_clip_automation` `clip_name`
- Don't skip the confirm-plan step — stating the mapping before execution prevents misplaced clips that are tedious to undo
- Don't use velocity 100–127 on all elements in the drop — match genre-edm-production mix balance defaults (kick 110, snare 100, hats 85/65, bass 90, pad 65); for emotional house keep kick ≤95 for warmth
- Don't make breakdowns longer than 16 bars in House/Techno — listeners lose energy connection past that point
- Don't apply master automation before clip notes are finalized — volume automation interacts with note velocities
