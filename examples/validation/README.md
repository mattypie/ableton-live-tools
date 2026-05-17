# Validation Fixtures

These files are canonical examples for future testing and validation of
`src/extract_locators.py`.

## Files

- `RYM_2026-03.als`: Ableton Live session used as the validation input.
- `RYM_2026-03_locators.tsv`: Expected TSV output generated with the standard options, with no high precision and no custom heading names.
- `RYM_2026-03_mixcloud.txt`: Expected Mixcloud output generated with the standard options.
- `RYM_2026-03_locators_highres.tsv`: Expected TSV output generated with high precision, custom headings, and a 27-second offset.
- `RYM_2026-03_mixcloud_highres.txt`: Expected Mixcloud output generated with high precision, custom headings, and a 27-second offset.

## High-Resolution Output Command

The `_highres` files were generated with:

```bash
python3 ~/git/ableton-live-tools/src/extract_locators.py "RYM_2026-03.als" --precision=3 -o RYM_2026-03_locators_highres.tsv -m RYM_2026-03_mixcloud_highres.txt --time-header=Time --label-header=Title --add-offset=27
```

## Validation Note

For future checks, ignore the first actual track when its title is
`Mysterium - Show Intro`; that entry was added manually.
