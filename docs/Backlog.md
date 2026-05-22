# Backlog

Ideas for future Ableton Live tools and utilities. This document is intentionally lightweight: each entry should be easy to expand into a release plan, issue, or implementation checklist later.

## Project Health Checker

Inspect an Ableton Live session and report anything that might make the project hard to open, transfer, archive, render, or collaborate on.

Possible checks:

- Missing audio files.
- Referenced files outside the project folder.
- Mixed sample rates or bit depths.
- Missing, unknown, or unavailable plugins.
- Disabled clips or devices.
- Frozen tracks and freeze-file references.
- External preset references.
- Very long file paths.
- Suspicious routing, sends, or track delay.
- Ableton Live version used to create the set.

Possible outputs:

- Terminal summary.
- Markdown report.
- JSON report for automation or CI.

## Semantic ALS Diff

Compare two `.als` files and report meaningful musical/project changes instead of raw XML differences.

Possible comparisons:

- Locators added, removed, renamed, or moved.
- Tracks added, removed, renamed, reordered, recolored, or regrouped.
- Clips moved, shortened, lengthened, disabled, renamed, or retimed.
- Tempo, time signature, and key/scale changes.
- Devices, plugins, and effects added, removed, reordered, or changed.
- Mixer changes such as volume, pan, sends, mute state, and track delay.
- Automation added, removed, or changed.
- Sample references changed.

Possible outputs:

- Human-readable Markdown diff.
- Terminal summary.
- JSON diff for Git hooks or release automation.

## Sample & Plugin/Effects Manifest

Create a bill of materials for everything the Live Set depends on.

Possible fields:

- Audio file paths, relative paths, sizes, sample rates, bit depths, durations, and checksums.
- Which clips use each audio file.
- Missing-file status.
- Built-in Ableton devices.
- Third-party plugins and effects.
- Max for Live devices.
- Preset references where available.
- Track and device-chain location for each dependency.

Possible outputs:

- TSV manifest.
- JSON manifest.
- Markdown archive report.

## Project Inventory

Produce a broad inventory of the contents of an Ableton Live project, covering all MIDI files, sound files, plugins, effects, devices, tracks, groups, and arrangement/session elements that can be reasonably extracted from the `.als` file.

Possible fields:

- Tracks, groups, returns, and master track.
- Track names, colors, routing, sends, and clip counts.
- MIDI clips and MIDI note counts.
- Audio clips and source media.
- Locators.
- Tempo and time signature map.
- Session and clip scale/key metadata.
- Devices, plugins, effects, racks, and macros.
- Automation envelope counts by track/device/parameter.

Possible outputs:

- Markdown project summary.
- TSV tables for spreadsheet review.
- JSON for scripting and future tools.

## Plugin Manifest

Extract every plugin/effect used in the session, with views sorted by author and by plugin/effect name.

Possible fields:

- Plugin/effect name.
- Manufacturer/author, where detectable.
- Format or device type, such as Ableton native, AU, VST, VST3, or Max for Live.
- Track name.
- Device-chain position.
- Rack location and macro context.
- Enabled/disabled state.
- Preset reference, where available.
- Duplicate usage count.
- Missing or unavailable status, where detectable.

Possible outputs:

- `plugins_by_author.tsv`
- `plugins_by_name.tsv`
- Markdown plugin report.
- JSON manifest for automation.
