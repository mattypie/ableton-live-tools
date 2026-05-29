Python scripts for dealing with Ableton Live and its session files.

## Tools Collection

- [Extract Locators](<docs/Extract Locators.md>): `src/extract_locators.py` extracts Ableton Live arrangement locators from `.als` session files and writes timestamped tracklists. It supports tempo changes, linear tempo ramps, offsets, TSV exports, Mixcloud exports, JSON exports, optional key stripping, configurable TSV heading rows, and optional locator metadata columns.

- [Extract Timeline](<docs/Extract Timeline.md>): `src/extract_timeline.py` extracts a precise Ableton Live arrangement timeline from `.als` session files. It writes an interleaved event stream for tempo, tempo ramps, time signatures, detected keys, locators, clip boundaries, song end, and optional generated bar/beat grid rows, with real wall-clock time and sample indexes when a sample rate is available.

## Project Notes

- [Performance and Output Roadmap](<docs/Performance and Output Roadmap.md>): Tracks profiling results, optimization candidates, validation notes, and candidate export formats for future releases.

## License

Please read [LICENSE](LICENSE) for the terms of use.
