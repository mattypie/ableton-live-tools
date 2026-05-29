# Performance and Output Roadmap

This document records performance findings and export-format candidates for future Ableton Live Tools releases. It is meant to keep profiling notes close to the code without treating unimplemented ideas as shipped behavior.

## 2026.05.29 Profiling Baseline

Benchmarks were run on `examples/validation/RYM_2026-03.als` with Python 3.14.5.

| Tool | Command Shape | Rows / Events | Reported Elapsed Time |
| --- | --- | ---: | ---: |
| `src/extract_locators.py` | TSV + Mixcloud + JSON, all locator columns | 66 locators | `0.873s` |
| `src/extract_timeline.py` | Default timeline TSV + JSON | 2331 events | `1.707s` |
| `src/extract_timeline.py` | Beat grid with tempo, time signature, key, and locator events | 10692 events | `1.695s` |

The main finding is that XML parsing dominates runtime. Output writing is comparatively small, even when both TSV and JSON are enabled.

## Highest-Value Optimization Candidates

- Add target-aware parsing to `src/extract_timeline.py`, so clip, media, audio-header, and sample metadata are collected only when the selected event types or columns require them.
- Add a tag-name fast path in XML start-element handlers, so most unrelated XML elements can return before expensive path matching.
- Replace repeated tuple path checks with parser state and depth counters for hot XML regions such as tempo automation, time signatures, locators, clips, and sample references.
- Defer media-path and audio-header work until an output column or metadata block actually needs source file details.
- Avoid JSON serialization for TSV `details` cells unless the selected columns include `details`.
- Keep streaming XML parsing as the default model, because it preserves the large memory savings already achieved in `2026.05.16`.

## Output Format Candidates

- Standard MIDI File (`.mid`): export tempo map, time signatures, key signatures, and locators as MIDI meta events for DAW interchange.
- WebVTT (`.vtt`): export locators as chapter cues for video, podcast, and web-player workflows.
- CSV (`.csv`): mirror TSV exports for spreadsheet tools that expect comma-separated files.
- Markdown (`.md`): produce human-readable reports for release notes, cue sheets, validation logs, and GitHub pull requests.
- CUE sheet (`.cue`): export locator-based track indexes for long mixes, archives, and CD-style workflows.
- REAPER marker CSV: export locators and timing markers for moving cue data into REAPER.

## 2026.05.29 Validation Notes

The usual validation flow was run after the documentation and compatibility updates:

- `python3 -m py_compile src/extract_locators.py src/extract_timeline.py`
- `git diff --check`
- High-resolution locator TSV and Mixcloud fixture comparison.
- Locator metadata TSV and pretty JSON fixture comparison.
- Extract Timeline locator cross-check against Extract Locators metadata at matching precision.
- Full Extract Timeline TSV + JSON run.
- Beat-grid Extract Timeline run.
- Success and missing-file exit-code checks for both scripts.

Known fixture note: the standard locator TSV and Mixcloud fixtures include the manually added `Mysterium - Show Intro` row. After ignoring that row, the generated timings match the fixture shape. One standard-fixture label has manual capitalization (`Lift Me Up`) while the ALS locator text, high-resolution fixture, and metadata fixture preserve `LIft Me Up`.
