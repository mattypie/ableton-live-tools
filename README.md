# ableton-live-tools

Python scripts for dealing with Ableton Live and its session files.

## Tools

### Extract Locators

`src/extract_locators.py` extracts Ableton Live arrangement locators from `.als` session files and writes timestamped tracklists. It supports tempo changes, linear tempo ramps, offsets, TSV exports, Mixcloud exports, JSON exports, optional key stripping, configurable TSV heading rows, and optional locator metadata columns.

Read the full guide and release notes in [Extract Locators](<Extract Locators.md>).

### Extract Timeline

`src/extract_timeline.py` extracts a precise Ableton Live arrangement timeline from `.als` session files. It writes an interleaved event stream for tempo, tempo ramps, time signatures, detected keys, locators, clip boundaries, song end, and optional generated bar/beat grid rows, with real wall-clock time and sample indexes when a sample rate is available.

Read the full guide and release notes in [Extract Timeline](<Extract Timeline.md>).

## License

Please read [LICENSE](LICENSE) for the terms of use.
