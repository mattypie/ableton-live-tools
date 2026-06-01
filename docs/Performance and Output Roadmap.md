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

- [x] Add target-aware parsing to `src/extract_timeline.py`, so clip, media, audio-header, and sample metadata are collected only when the selected event types or columns require them.
- [x] Add a tag-name fast path in XML start-element handlers, so most unrelated XML elements can return before expensive path matching.
- [x] Add a tag-name fast path in XML end-element handlers, so most unrelated closing tags skip deeper parser-state checks.
- [x] Replace fixed tuple-slice path checks with direct parent/depth checks for hot XML paths.
- [x] Defer media-path and audio-header work until an output column or metadata block actually needs source file details.
- Avoid JSON serialization for TSV `details` cells unless the selected columns include `details`.
- Keep streaming XML parsing as the default model, because it preserves the large memory savings already achieved in `2026.05.16`.

## 2026.05.31 Measured Improvements

Benchmarks were run on `examples/validation/RYM_2026-03.als` with Python 3.14.5. Each row uses the median of seven runs and the elapsed time reported by the CLI.

| Tool / Export Shape | Baseline Median | Optimized Median | Change |
| --- | ---: | ---: | ---: |
| `extract_locators.py` metadata TSV + JSON | `0.844s` | `0.691s` | `18.1%` faster |
| `extract_timeline.py` locator-only TSV | `1.568s` | `0.698s` | `55.5%` faster |
| `extract_timeline.py` beat grid with tempo, time signature, key, locator, and sample index | `1.631s` | `0.773s` | `52.6%` faster |
| `extract_timeline.py` full TSV + JSON | `1.645s` | `0.783s` | `52.4%` faster |

Implemented changes:

- Added tag-name fast paths to both XML parsers.
- Added tag-name fast paths to both XML end handlers.
- Added target-aware timeline parsing so lightweight exports can skip clip/sample structures.
- Replaced fixed tuple-slice path checks with direct parent/depth checks.
- Added an end-to-end `unittest` CLI validation suite under `tests/`.
- Added `scripts/benchmark_validation.py` so validation benchmarks can be repeated consistently and compared against a git ref.

Validation:

- `python3 -m py_compile src/extract_locators.py src/extract_timeline.py tests/test_cli_validation.py`
- `python3 -m unittest discover -s tests`
- `python3 scripts/benchmark_validation.py --compare-ref=main`
- `git diff --check`
- Full timeline TSV output compared byte-for-byte against `main`.
- Full timeline JSON output differs from `main` only in the expected script-version metadata field.
- Core beat-grid timeline TSV output compared byte-for-byte against `main`.

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
