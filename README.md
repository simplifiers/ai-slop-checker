# AI Slop Checker

**AI slop checker for German and English.** It checks articles and newsletters written with help from a language model for missing substance, unsourced claims, stock phrases and machine-like rhythm. Plain Python, no dependencies, runs offline. The command is `slop-check`.

[Deutsche Fassung](README.de.md)

## The problem

Most tools against "AI slop" hunt for a list of words and the long dash. Delete them all and the text can still say nothing. A paragraph can be free of every listed phrase and still fit any company, any topic, any reader.

Removing slop phrases isn't enough. The fix is substance. That means a number from your own data, a named source, a step someone can follow, or an example only you could give. slop-check looks for missing substance first and for phrases second.

## A 30-second example

`draft.md`:

```
In today's fast-paced world, content marketing is more important than ever.
Experts agree that companies with a clear strategy grow 73 % faster.
It's not about producing more. It's about producing better.
```

```
$ slop-check draft.md --lang en

slop-check 0.1.0  |  TOO SHORT FOR A VERDICT  |  31 words
Below 120 words there is no overall verdict, only the individual findings.

== Substance (FAIL 2, TELL 0, HINT 0)
  [FAIL] S-02 Vague attribution (line 2)
      > Experts agree
      "Studies show", "experts say", "according to a survey": an authority is invoked but not named.
      Fix: Name and link the source, or rewrite the sentence as your own experience.
  [FAIL] S-01 Figure without a source (line 2)
      > 73 %
      Figure "73 %" without a source in the same sentence.
      Fix: Add the source as a link or (source: name) in the same sentence, mark the figure as your own experience, or cut it.

== Stock phrases (FAIL 0, TELL 1, HINT 0)
  [TELL] P-01 In today's fast-paced world (line 1)
      > In today's fast-paced world
      Stock phrase "In today's fast-paced world" (In today's fast-paced world): Era framing with no content.
      Fix: Cut it or replace it with a concrete statement.

== Structure (FAIL 0, TELL 0, HINT 1)
  [HINT] T-01 Contrast template (line 3)
      > It's not about producing more. It's
      "It's not X. It's Y." and similar set-ups that invent a position only to knock it down. Once is a hint, twice is a pattern.
      Fix: Drop the straw position and argue your point directly.

slop-check does not tell whether AI wrote a text. It shows patterns you can check.
```

For each finding, slop-check quotes the passage and suggests a fix. Below 120 words it lists findings without an overall verdict. A full article gets `pass` or `revise`. It does not rewrite your text and it does not invent the missing detail.

## Install

With pip, straight from GitHub:

```
pip install git+https://github.com/simplifiers/ai-slop-checker
```

With pipx, so it gets its own environment:

```
pipx install git+https://github.com/simplifiers/ai-slop-checker
```

As a Claude skill:

```
npx skills add simplifiers/ai-slop-checker
```

The skill ships with its own copy of the checker, so Claude can run it with any Python 3.9 or newer. Both installs give you the command `slop-check` and the same command under the name `ai-slop-checker`.

To install by hand, download `ai-slop-checker-skill.zip` from the releases page and unpack it into your skills folder (for Claude Code that is `~/.claude/skills/`). Or download the repository as a ZIP and run `python -m slopcheck` inside it.

## Usage

Check a file:

```
slop-check draft.md
```

Set the language when the text is short or mixed:

```
slop-check draft.md --lang de
```

Compare the text with the notes or transcript it was written from. slop-check lists facts from the source that are missing in the text, and numbers in the text that the source does not contain:

```
slop-check draft.md --source interview-notes.md
```

Write a report you can open in a browser or send to a colleague. It is a single HTML file with no external resources:

```
slop-check draft.md --format html --out report.html
```

JSON for scripts and editors:

```
slop-check draft.md --format json
```

Fail a build when a text needs work:

```
slop-check draft.md --fail-on revise
```

`python -m slopcheck` works everywhere `slop-check` does.

## What it checks

Findings come in three levels. `fail` means fix this before publishing. `tell` means a pattern that is typical of generated text. `hint` means worth a second look. Single words are only flagged on their own when they are strong evidence. Weaker ones count when several appear together.

| Category | What it looks for | Two examples |
|---|---|---|
| Substance | Text that sounds like content but carries none | "Experts agree that..." with no expert named. A sentence you could paste into any article on any topic. |
| Facts | Claims that need a source | A percentage or study with no reference. A number from your notes that got lost on the way into the text. |
| Phrases | Stock wording | "In today's fast-paced world". "Let's dive in." |
| Structure | Recurring shapes | "It's not X. It's Y." Lists of three in every paragraph. |
| Rhythm | Sentence and paragraph length, vocabulary, word length, lists of three and colons, measured against human texts | Short sentences in short paragraphs. Synonyms swapped so often that it reads as forced. |
| Form | Typography and layout | Emoji in front of every bullet. The long dash, as a style rule you can switch off. |

Every pattern with its ID, a bad and a better example: [docs/patterns.md](docs/patterns.md).

Named people are listed separately under "people to verify". slop-check cannot tell whether a quoted person exists or said what the text claims. You have to check that.

Texts under a minimum length get the verdict `too_short` instead of a judgement, because the measurements are not reliable on a few sentences.

The verdict is `revise` when there is at least one `fail`, when tells come from five or more different patterns, or when six or more rhythm measurements sit on the side of generated text at once. Otherwise it is `pass`. Hints never count.

## How the rhythm check is calibrated

Nine measurements are compared with a band of human texts: words per sentence, spread of sentence lengths, words per paragraph, vocabulary variety (MATTR), letters per word, nominal style, lists of three, colons and, in English only, trailing participles such as ", ensuring". The band runs from the 10th to the 90th percentile.

For the public band we used freely licensed news texts written before 2022, 157 German and 162 English Wikinews articles. For the comparison we generated 40 blog articles per language. Only measurements that point the same way in every register we measured (news, parliamentary speeches, encyclopedia articles) made it into the band. Four common suspects did not separate human from generated text in our measurements and are left out: dashes, passive voice, connector openings, parentheses.

One value outside the band is common in human texts and is only a hint. From six values on the generated side, the verdict is `revise`. We held back every fourth text when building the band and tested the rule on those: it fired on 2 of 39 German and 0 of 40 English news articles, and on 4 of 10 German and 5 of 10 English generated articles (source: the `evaluation` field in `slopcheck/bands/de-basic.json` and `en-basic.json`). The rhythm rule catches part of generated text; the other checks do the rest.

There is a limit. All comparison texts so far come from one model. Other models and prompts may land elsewhere. News is also not the same register as an expert blog post, which is why single values only count as hints. A band calibrated on real expert articles is part of AI Editorial Team.

## What it does not do

- It is not an AI detector. A finding says a passage is generic or unsupported. It says nothing about who or what wrote it, and a clean report does not prove a human wrote the text.
- It does not rewrite. You get findings with suggested fixes. Your voice stays yours.
- It does not check people or quotes against real sources. It lists them so you can.
- It does not measure whether your text shows up in AI search.

If you want the full workflow with research, an interview about your own experience and automatic source checks, there is AI Editorial Team (redaktion.ai), and a free Claude skill that walks you through it: https://app.redaktion.ai/lite?lang=en&ref=github

## Configuration

Put a `.slopcheck.json` next to your texts or in the project root:

```json
{
  "lang": "en",
  "allow": ["robust regression", "leverage ratio"],
  "forbid": ["synergy", "best-in-class"],
  "disable": ["T-02"],
  "own_names": ["Jane Doe"],
  "sources": ["notes/interview.md"],
  "fail_on": "revise"
}
```

| Key | Meaning |
|---|---|
| `lang` | `de` or `en`. Without it, slop-check detects the language. |
| `address` | German only: `du` or `sie`. The other form is then a hard finding. Without it, a mix of both is flagged. |
| `allow` | Terms that are never reported as stock phrases, for example technical terms. |
| `forbid` | Extra words you never want in your texts. |
| `disable` | Pattern IDs to switch off. |
| `own_names` | Your own name and your colleagues' names, so they are not listed as people to verify. |
| `emojis` | `allow`, `limit` or `no`. |
| `dashes` | Style rule for the long dash: `tell` (default), `fail` or `off`. Many readers see long dashes as typical of AI, but they do not separate human from generated text in our measurements. |
| `sources` | Source files for the fact check, same as `--source`. |
| `fail_on` | `revise` to exit with code 1 when a text needs work. |

Command line options override the file. `--config FILE` points to a config somewhere else.

## GitHub Action

Check your Markdown on every pull request:

```yaml
name: Text quality
on: pull_request
jobs:
  slop-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: simplifiers/ai-slop-checker@main
        with:
          paths: content/blog/*.md
          lang: en
          fail-on: revise
```

## Contributing

Patterns live in `slopcheck/patterns/en.json` and `slopcheck/patterns/de.json`, one catalogue per language. Each entry has an `id`, `name`, `description`, `bad` and `better`. The better example must not add facts that the bad one lacks. Where a real detail is needed, use a placeholder such as `[number from your data]`. Reports of false alarms are just as useful: open an issue with the sentence that triggered it.

This README is checked by slop-check in CI. If a change makes it fail, the README gets fixed, not the check. Details in [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

These projects shaped the ideas behind slop-check. No wording was copied from them.

- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop)
- [FeedHive/ai-slop-detector](https://github.com/FeedHive/ai-slop-detector)
- [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop)
- [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill)
- [ilien-dev/quiron](https://github.com/ilien-dev/quiron)
- The Wikipedia guide [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

The rhythm band contains statistics derived from [Wikinews](https://www.wikinews.org/) articles by Wikinews contributors, licensed under [CC BY 2.5](https://creativecommons.org/licenses/by/2.5/). No text from Wikinews is included, only percentiles.

## Licence

MIT. See [LICENSE](LICENSE).
