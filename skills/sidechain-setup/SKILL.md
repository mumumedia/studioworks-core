---
name: sidechain-setup
description: Use when the user wants to set up sidechain compression - typically kick → bass, kick → pads, vocals → music bed. Examples - "sidechain my bass to the kick", "make the synths duck under the vocal", "add pumping to the chords".
---

# Sidechain Setup

Set up sidechain compression routing. Different DAWs/MCP servers expose this differently — read the available tools and use the simplest path.

## Workflow

### 1. Identify the source and target

- **Source** = trigger (the track that *causes* the duck) — usually kick or vocal
- **Target** = the track that *gets ducked* — usually bass, pads, or music bed

Confirm with user: "Sidechain target = bass on track 2, source = kick on track 1?"

### 2. Choose the technique

#### A. Compressor sidechain (standard for kick→bass)

- Add Compressor to the target track
- Enable sidechain input on the compressor
- Route source: select the kick track as the input
- Settings:
  - Ratio: 4:1
  - Attack: 5 ms
  - Release: 80-120 ms (release should match the tempo — at 120 BPM, 1 beat = 500ms, so 125ms ≈ 1/16 note)
  - Threshold: set so that GR shows -4 to -6 dB on each kick hit
  - Output gain: +1 to +2 dB to compensate

#### B. Glue Compressor sidechain (more musical for buses)

Same as above but using Glue Compressor — gives a more "analog" pumping sound, typical for house/EDM masters where you want musical pumping.

#### C. LFO Tool / volume automation (creative)

If the user wants extreme rhythmic pumping (EDM-style 4/4 pump):

- Use Auto Filter or a volume LFO modulator if no LFO Tool plugin
- LFO shape: sawtooth (fast attack, slow release looks like ⏐╲⏐╲)
- Sync to 1/4 notes
- Depth: -6 to -12 dB
- This is used when there's no actual kick (e.g., during a breakdown) but you want the pump feel.

#### D. Volume envelope automation (per-clip)

For surgical control on a specific section:

- Show automation on the target track
- Draw a manual ducking envelope tied to the source's hits
- Useful for vocal-driven ducking on a music bed

### 3. Apply

**There is no `add_device` MCP tool.** Adding the Compressor to the target track is always a manual step. Tell the user to do it first, then use `set_device_parameter` for everything else.

Instruct the user to:
1. Click the target track
2. Drag **Compressor** from Audio Effects into the device chain
3. Expand the **Sidechain** section and set **Audio From** to the source track (e.g. Kick)
4. Confirm done — then proceed with parameter setting below

> *"Please add an Ableton Compressor to the [target] track, expand its Sidechain section, and set Audio From to [source]. Tell me when it's in place and I'll dial in the settings."*

Once the user confirms, use `get_device_parameters` to read current values and confirm the compressor is present, then `set_device_parameter` for ratio, attack, release, threshold, and — critically — **`S/C On`**:

**`S/C On` must be explicitly set to 1.0.** Routing the "Audio From" source in the UI and activating the sidechain are separate steps in Ableton's API. After the user does the manual routing, `S/C On` is still Off (0.0) until you set it.

```
set_device_parameter(track_index, device_index, parameter_name="S/C On", value=1.0)
```

**Parameter values are normalized 0–1, not the actual units.** `set_device_parameter` does not accept "150" for 150ms or "-18" for -18dB. Use this calibration loop:
1. Set an estimated value
2. Call `get_device_parameters` and read the `display_value`
3. Adjust and repeat until the display matches the target

For the Release parameter especially, the curve is logarithmic — small value changes produce large ms jumps at high values. Start low and step up.

> *"Note: `add_device` is not yet implemented. A future enhancement could use `load_browser_item` with the device's browser URI to add native effects programmatically — deferred to Phase 5."*

### 4. Verify

After applying, ask user to play the kick + bass together. Adjust if needed:
- Pumping too obvious? → reduce ratio to 3:1 or release to 60ms
- Pumping not enough? → ratio 6:1 or threshold lower
- Bass dipping too long? → shorten release
- Bass missing the next beat? → release too long, shorten

## Don'ts

- Don't sidechain everything by default — kick→bass is universal, but pad/synth ducking is genre-specific (huge in EDM, rare in jazz).
- Don't use ratios above 8:1 unless going for a deliberate pump effect.
- Don't sidechain the master bus — that's a special-case mastering technique, not a mix move.
- Don't apply without listening — sidechain is a feel adjustment, settings depend on what the user hears.

## Quick reference table

| Use case | Ratio | Attack | Release | GR target |
| --- | --- | --- | --- | --- |
| Kick → bass (rock/pop) | 4:1 | 5 ms | 100 ms | -4 dB |
| Kick → bass (EDM pump) | 8:1 | 1 ms | 200 ms | -10 dB |
| Kick → pad/chord | 3:1 | 10 ms | 150 ms | -3 dB |
| Vocal → music bed | 2:1 | 15 ms | 300 ms | -2 dB |
| Snare → reverb tail | 3:1 | 5 ms | 80 ms | -4 dB |
