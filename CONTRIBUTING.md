# Contributing to AI Slop Checker

Thanks for helping. Most useful contributions are new or better patterns, and reports of false alarms with the sentence that triggered them.

## Patterns

Patterns live in `slopcheck/patterns/en.json` and `slopcheck/patterns/de.json`, one catalogue per language. Each entry has an `id`, a `name`, a `description`, a `bad` example and a `better` example.

Rules for examples:

- `better` must not add facts that `bad` does not contain. Where a real detail is needed, write a placeholder such as `[number from your data]` or `[name of the customer]`.
- Keep examples short and in the language of the pattern.
- No copied wording from other projects or from Wikipedia.
- Prefer conditional rules ("three of these in one paragraph") over absolute bans. Single words are only flagged when they are strong evidence on their own.

After changing patterns, rebuild the docs:

```
python scripts/build_docs.py
```

## Rhythm bands

The bands in `slopcheck/bands/` are measured, not tuned by hand. `slopcheck/meter.py` computes every feature exactly as it was computed for the measurement, so a change to a definition there makes the bands wrong until they are measured again. A band holds only statistics (percentiles) from freely licensed texts, never the texts themselves, and names its sources and licences.

## Tests

```
python -m unittest discover -s tests
python scripts/build_docs.py --check
python -m slopcheck README.md --lang en --fail-on revise
python -m slopcheck README.de.md --lang de --fail-on revise
python scripts/build_skill.py --check
```

After changing code in `slopcheck/`, refresh the copy in `skills/ai-slop-checker/` and the ZIP with `python scripts/build_skill.py`.

The README has to pass slop-check itself. If your change makes it fail, fix the README or the pattern, not the test.

## Code

Standard library only, Python 3.9 or newer. No new dependencies.

## Licence

By contributing you agree that your contribution is released under the MIT licence of this project.
