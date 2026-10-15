# Patterns

[Deutsche Fassung](patterns.de.md)

<!-- This page is generated from `slopcheck/patterns/*.json` by `scripts/build_docs.py`. Edit the JSON files, not this page. -->

Each pattern has an ID, a short name, a description and two examples. The better example never adds facts that the bad one does not have. Where a real detail is needed, it shows a placeholder in square brackets.

## Contents

- [Substance](#substance) (8 patterns)
- [Facts](#facts) (3 patterns)
- [Phrases](#phrases) (73 patterns)
- [Structure](#structure) (9 patterns)
- [Rhythm](#rhythm) (10 patterns)
- [Form](#form) (8 patterns)

## Substance

Passages that sound like content but carry none: vague attributions, sentences that would fit any article on any topic, advice without steps, smoothed-over specifics. These matter most.

### S-01 Figure without a source

Severity: `fail`

Percentages, shares, amounts, large numbers or multiples with no source in the same sentence. Measurements, years, versions, legal sections and times do not count.

**Bad:**

> 73% of customers read reviews before buying.

**Better:**

> A link to the survey in the same sentence, or: At our shop, [your number from your own experience] out of ten customers ask about reviews first.

**Fix:** Add the source as a link or (source: name) in the same sentence, mark the figure as your own experience, or cut it.

### S-02 Vague attribution

Severity: `fail`

"Studies show", "experts say", "according to a survey": an authority is invoked but not named.

**Bad:**

> Studies show that short texts work better.

**Better:**

> Name the study with a link, or write what you observed yourself: [your observation].

**Fix:** Name and link the source, or rewrite the sentence as your own experience.

### S-03 Person without a source

Severity: `tell`

A named person is quoted or paraphrased without a source in the sentence. Check that the person exists and said this.

**Bad:**

> Marketing expert Thomas Weber says content is everything.

**Better:**

> [Name] told us on [date]: "[exact quote]", or a link to the original source.

**Fix:** Add a link to the original source or cut the person. Allow your own name with the config key own_names.

### S-04 Interchangeable paragraph

Severity: `hint`

A longer paragraph without a single concrete detail: no number, name, place, date, example or first-hand experience. It could appear in any text on the topic.

**Bad:**

> Good communication is the basis of all collaboration. Those who communicate clearly avoid misunderstandings and build trust.

**Better:**

> Add one detail only you know: [a case from your work, with a place or time].

**Fix:** Add one concrete detail from your own experience or cut the paragraph.

### S-05 Little concrete detail

Severity: `tell`

Across the whole text there are very few concrete details per 100 words (numbers, names, dates, examples, first-hand experience). Threshold is provisional.

**Bad:**

> A whole article made of general advice.

**Better:**

> At least one example from your practice per section: [case], [time span], [result].

**Fix:** Add your own cases, sourced figures and examples.

### S-06 Advice without steps

Severity: `tell`

A paragraph piles up instructions ("you should", "make sure") but gives neither steps nor an example.

**Bad:**

> You should know your audience. You should post regularly. Make sure to focus on quality.

**Better:**

> A numbered list of the steps you actually take, with one example: [step 1], [step 2].

**Fix:** Break the advice into steps or add an example from practice.

### S-07 Smoothed-over detail

Severity: `tell`

A concrete detail is replaced by a vague one: "a leading provider", "well-known companies", "numerous clients".

**Bad:**

> A leading company already uses the method.

**Better:**

> Name the company if you may, or describe it: [industry], [size], [what they do with it].

**Fix:** Name it, or describe the detail that makes the case specific.

### S-08 Figure from your own experience

Severity: `hint`

A figure in an I or we sentence. It may be first-hand. Check that it is right and that you could back it up.

**Bad:**

> We cut costs by 40%.

**Better:**

> We cut costs from [amount] to [amount], measured over [time span].

**Fix:** Add the time span and what was measured.

## Facts

Numbers, studies and named people that need a source, and facts from your notes that went missing on the way into the text.

### S-11 Fact from the source is missing

Severity: `tell`

A number, date, name or link is in your notes but not in the draft.

**Bad:**

> Notes: 15,000 subscribers. Draft: lots of subscribers.

**Better:**

> Carry the detail over from your notes if it matters to the reader.

**Fix:** Check whether the detail was dropped on purpose.

### S-12 New figure or link without support

Severity: `fail`

A figure or link is in the draft but in none of the sources, and the sentence has no citation. Typical of invented details.

**Bad:**

> Notes: no figure. Draft: 73% of readers stay longer.

**Better:**

> Only use figures from your notes, or add the source.

**Fix:** Check and source the detail, or cut it. Open links and check that they support the claim.

### S-13 New name or date

Severity: `tell`

A name or date is in the draft but in none of the sources.

**Bad:**

> Notes: a client in Leeds. Draft: client Mary Hollis in Leeds.

**Better:**

> Stay with the detail from your notes: [as in your notes].

**Fix:** Check that the name or date is right.

## Phrases

Stock wording that shows up far more often in generated text than in edited writing. Strong single words are flagged on their own, weaker ones only in clusters.

### P-01 In today's fast-paced world

Severity: `tell`

Era framing with no content.

**Bad:**

> In today's fast-paced world, every minute counts.

**Better:**

> Since [month/year], we answer requests within [your time span].

**Fix:** Cut it or replace it with a concrete statement.

### P-02 In the digital age

Severity: `tell`

Era label instead of a concrete trigger.

**Bad:**

> In the digital age, everything changes.

**Better:**

> Since [concrete change], teams have to [concrete consequence].

**Fix:** Cut it or replace it with a concrete statement.

### P-03 Ever-evolving landscape

Severity: `tell`

Landscape image for a market.

**Bad:**

> In the ever-evolving landscape of SEO, ...

**Better:**

> Name the one change that affects your readers.

**Fix:** Cut it or replace it with a concrete statement.

### P-04 Now more than ever

Severity: `tell`

Escalation without a comparison point.

**Bad:**

> Visibility matters now more than ever.

**Better:**

> Say what changed and when.

**Fix:** Cut it or replace it with a concrete statement.

### P-05 It's important to note

Severity: `tell`

Announces a point instead of making it.

**Bad:**

> It's important to note that backups take time.

**Better:**

> Backups take time: plan [your duration] for them.

**Fix:** Cut it or replace it with a concrete statement.

### P-06 It's no secret that

Severity: `tell`

Claims common knowledge instead of showing it.

**Bad:**

> It's no secret that customers read reviews.

**Better:**

> Customers read reviews: [what they ask you about first].

**Fix:** Cut it or replace it with a concrete statement.

### P-07 Delve into

Severity: `tell`

Overused verb in generated prose.

**Bad:**

> Let's delve into the details.

**Better:**

> Cut the sentence and start with the first detail.

**Fix:** Cut it or replace it with a concrete statement.

### P-08 Let's dive in

Severity: `tell`

Swimming metaphor as a transition.

**Bad:**

> Let's dive in.

**Better:**

> Cut it and start.

**Fix:** Cut it or replace it with a concrete statement.

### P-09 Welcome to the world of

Severity: `tell`

Greeting instead of an opening.

**Bad:**

> Welcome to the world of email marketing!

**Better:**

> Open with the question that brought the reader here.

**Fix:** Cut it or replace it with a concrete statement.

### P-10 Imagine a world

Severity: `tell`

Invented scenario as a hook.

**Bad:**

> Imagine a world where your shop sells while you sleep.

**Better:**

> Tell a real case: [what happened to one of your clients].

**Fix:** Cut it or replace it with a concrete statement.

### P-11 In this article, you'll learn

Severity: `tell`

Table of contents instead of content.

**Bad:**

> In this article, you'll learn everything about taxes.

**Better:**

> Give the most important answer in the first sentence.

**Fix:** Cut it or replace it with a concrete statement.

### P-12 Plays a crucial role

Severity: `tell`

Importance claimed, not explained.

**Bad:**

> Page speed plays a crucial role.

**Better:**

> Say what happens when page speed drops: [your observation].

**Fix:** Cut it or replace it with a concrete statement.

### P-13 Of paramount importance

Severity: `tell`

Importance label without a reason.

**Bad:**

> Data protection is of paramount importance.

**Better:**

> Data protection decides [concrete consequence] here.

**Fix:** Cut it or replace it with a concrete statement.

### P-14 The key to success

Severity: `tell`

Success promise with no content.

**Bad:**

> Consistency is the key to success.

**Better:**

> Name what consistency changed in your case.

**Fix:** Cut it or replace it with a concrete statement.

### P-15 Unlock the potential

Severity: `tell`

Potential rhetoric without a result.

**Bad:**

> Unlock the full potential of your website.

**Better:**

> Name the result the reader can reach.

**Fix:** Cut it or replace it with a concrete statement.

### P-16 Harness the power

Severity: `tell`

Power metaphor for using a tool.

**Bad:**

> Harness the power of automation.

**Better:**

> Say which task automation takes over.

**Fix:** Cut it or replace it with a concrete statement.

### P-17 Take it to the next level

Severity: `tell`

Step image without a measure.

**Bad:**

> Take your marketing to the next level.

**Better:**

> Say what is different afterwards: [your measure].

**Fix:** Cut it or replace it with a concrete statement.

### P-18 Elevate your

Severity: `tell`

Lifting verb for any improvement.

**Bad:**

> Elevate your brand.

**Better:**

> Say what changes for the brand.

**Fix:** Cut it or replace it with a concrete statement.

### P-19 Navigate the complexities

Severity: `tell`

Navigation metaphor for difficulty.

**Bad:**

> We help you navigate the complexities of tax law.

**Better:**

> Name the one rule readers get wrong.

**Fix:** Cut it or replace it with a concrete statement.

### P-20 A testament to

Severity: `tell`

Grand framing for a simple fact.

**Bad:**

> The result is a testament to hard work.

**Better:**

> Say what the team did.

**Fix:** Cut it or replace it with a concrete statement.

### P-21 Game-changer

Severity: `tell`

Ad-copy superlative.

**Bad:**

> This feature is a real game-changer.

**Better:**

> Say what the feature changes and for whom.

**Fix:** Cut it or replace it with a concrete statement.

### P-22 Revolutionize

Severity: `tell`

Exaggeration without before and after.

**Bad:**

> AI is revolutionizing accounting.

**Better:**

> AI now handles [concrete task] in accounting.

**Fix:** Cut it or replace it with a concrete statement.

### P-23 Seamless

Severity: `tell`

Promises no friction, does not show it.

**Bad:**

> The software integrates seamlessly.

**Better:**

> The software reads [concrete format] directly.

**Fix:** Cut it or replace it with a concrete statement.

### P-24 Leverage

Severity: `tell`

Consultant verb for 'use'.

**Bad:**

> Leverage your data to grow.

**Better:**

> Use [which data] to decide [what].

**Fix:** Cut it or replace it with a concrete statement.

### P-25 Synergy

Severity: `tell`

Consultant word without a mechanism.

**Bad:**

> This creates synergy between teams.

**Better:**

> Name what one team takes off the other's plate.

**Fix:** Cut it or replace it with a concrete statement.

### P-26 Holistic

Severity: `tell`

Buzzword that pretends completeness.

**Bad:**

> We offer a holistic approach.

**Better:**

> List what the approach covers.

**Fix:** Cut it or replace it with a concrete statement.

### P-27 Cutting-edge

Severity: `tell`

Novelty label without a comparison.

**Bad:**

> Cutting-edge technology.

**Better:**

> Say what the technology does that older tools do not.

**Fix:** Cut it or replace it with a concrete statement.

### P-28 Innovative solutions

Severity: `tell`

Empty label for an offer.

**Bad:**

> We deliver innovative solutions.

**Better:**

> Say what the offer does.

**Fix:** Cut it or replace it with a concrete statement.

### P-29 Multifaceted

Severity: `tell`

Complexity claimed instead of shown.

**Bad:**

> The issue is multifaceted.

**Better:**

> Name the two sides of the issue.

**Fix:** Cut it or replace it with a concrete statement.

### P-30 In the realm of

Severity: `tell`

Kingdom image for a topic.

**Bad:**

> In the realm of finance, ...

**Better:**

> In finance, ...

**Fix:** Cut it or replace it with a concrete statement.

### P-31 Hand in hand

Severity: `tell`

Image of connection without a mechanism.

**Bad:**

> SEO and content go hand in hand.

**Better:**

> Explain how one depends on the other.

**Fix:** Cut it or replace it with a concrete statement.

### P-32 At the end of the day

Severity: `tell`

Filler idiom.

**Bad:**

> At the end of the day, results matter.

**Better:**

> Cut it or name the result.

**Fix:** Cut it or replace it with a concrete statement.

### P-33 Last but not least

Severity: `tell`

List filler.

**Bad:**

> Last but not least: the costs.

**Better:**

> Name the point without announcing it.

**Fix:** Cut it or replace it with a concrete statement.

### P-34 Embark on a journey

Severity: `tell`

Journey metaphor for a process.

**Bad:**

> Embark on your journey to better sleep.

**Better:**

> Describe the first step.

**Fix:** Cut it or replace it with a concrete statement.

### P-35 In conclusion / To sum up

Severity: `tell`

Closing formula instead of a closing thought.

**Bad:**

> In conclusion, planning helps.

**Better:**

> End with the reader's next step.

**Fix:** Cut it or replace it with a concrete statement.

### P-36 Robust

Severity: `tell`

Engineering adjective used as a quality seal.

**Bad:**

> A robust solution for your team.

**Better:**

> Say what the solution withstands: [load, errors, time span].

**Fix:** Cut it or replace it with a concrete statement.

### P-37 Tapestry

Severity: `tell`

Weaving image for variety.

**Bad:**

> A rich tapestry of cultures.

**Better:**

> Name two of the cultures and what they bring.

**Fix:** Cut it or replace it with a concrete statement.

### P-38 The X landscape

Severity: `tell`

Landscape image for a market or field.

**Bad:**

> The marketing landscape is shifting.

**Better:**

> Say what shifted and for whom.

**Fix:** Cut it or replace it with a concrete statement.

### P-39 Pivotal

Severity: `tell`

Importance adjective.

**Bad:**

> A pivotal moment for the company.

**Better:**

> Say what the company decided at that moment.

**Fix:** Cut it or replace it with a concrete statement.

### P-40 Foster

Severity: `tell`

Abstract verb for building something.

**Bad:**

> Foster a culture of trust.

**Better:**

> Say what you do so people trust each other.

**Fix:** Cut it or replace it with a concrete statement.

### P-41 Empower

Severity: `tell`

Abstract verb for enabling.

**Bad:**

> We empower teams to grow.

**Better:**

> Say what teams can do afterwards.

**Fix:** Cut it or replace it with a concrete statement.

### P-42 Streamline

Severity: `tell`

Process verb without the process.

**Bad:**

> Streamline your workflow.

**Better:**

> Name the step you remove.

**Fix:** Cut it or replace it with a concrete statement.

### P-43 The ultimate guide

Severity: `tell`

Superlative in the title.

**Bad:**

> The ultimate guide to newsletters

**Better:**

> Newsletters: [the concrete promise the text keeps]

**Fix:** Cut it or replace it with a concrete statement.

### P-44 Valuable insights

Severity: `tell`

Judgement instead of content.

**Bad:**

> The report offers valuable insights.

**Better:**

> Name the one finding from the report.

**Fix:** Cut it or replace it with a concrete statement.

### P-45 Meticulous

Severity: `tell`

Diligence adjective.

**Bad:**

> Meticulously crafted content.

**Better:**

> Say what you checked and how.

**Fix:** Cut it or replace it with a concrete statement.

### P-46 Intricate

Severity: `tell`

Complexity adjective.

**Bad:**

> The intricate details of the process.

**Better:**

> Name the detail that trips people up.

**Fix:** Cut it or replace it with a concrete statement.

### P-47 Underscore

Severity: `tell`

Emphasis verb.

**Bad:**

> This underscores the importance of planning.

**Better:**

> Say what goes wrong without planning.

**Fix:** Cut it or replace it with a concrete statement.

### P-48 Showcase

Severity: `tell`

Display verb.

**Bad:**

> The project showcases our expertise.

**Better:**

> Say what the project solved.

**Fix:** Cut it or replace it with a concrete statement.

### P-49 Boasts

Severity: `tell`

Brochure verb.

**Bad:**

> The city boasts many museums.

**Better:**

> The city has [number] museums, including [one you know].

**Fix:** Cut it or replace it with a concrete statement.

### P-50 Nestled

Severity: `tell`

Travel-brochure image.

**Bad:**

> Nestled in the hills, the hotel ...

**Better:**

> The hotel is in the hills, [distance] from [place].

**Fix:** Cut it or replace it with a concrete statement.

### P-51 Vibrant / bustling

Severity: `tell`

Brochure adjectives.

**Bad:**

> A vibrant, bustling city.

**Better:**

> Describe what you saw there.

**Fix:** Cut it or replace it with a concrete statement.

### P-52 A myriad of / plethora of

Severity: `tell`

Quantity word with no quantity.

**Bad:**

> A myriad of options.

**Better:**

> Name the two options that matter.

**Fix:** Cut it or replace it with a concrete statement.

### P-53 Here's the thing

Severity: `tell`

Spoken-style setup line.

**Bad:**

> Here's the thing: nobody reads manuals.

**Better:**

> Say it directly.

**Fix:** Cut it or replace it with a concrete statement.

### P-54 The good news?

Severity: `tell`

Suspense formula.

**Bad:**

> The good news? There is a fix.

**Better:**

> Name the fix directly.

**Fix:** Cut it or replace it with a concrete statement.

### P-55 This is where X comes in

Severity: `tell`

Stage entrance for a product or concept.

**Bad:**

> This is where automation comes in.

**Better:**

> Say which task automation takes over.

**Fix:** Cut it or replace it with a concrete statement.

### P-56 Cornerstone

Severity: `tell`

Building image for importance.

**Bad:**

> Trust is the cornerstone of a brand.

**Better:**

> Name what customers base trust on.

**Fix:** Cut it or replace it with a concrete statement.

### P-57 Paradigm shift

Severity: `tell`

Big-change label.

**Bad:**

> A paradigm shift in marketing.

**Better:**

> Say what people do differently now.

**Fix:** Cut it or replace it with a concrete statement.

### P-58 Whether you're a beginner or a pro

Severity: `tell`

Audience-everyone formula.

**Bad:**

> Whether you're a beginner or a seasoned pro, ...

**Better:**

> Write for one reader and say who.

**Fix:** Cut it or replace it with a concrete statement.

### P-59 Look no further

Severity: `tell`

Ad-copy formula.

**Bad:**

> Looking for a good CRM? Look no further.

**Better:**

> Name the CRM and why it fits.

**Fix:** Cut it or replace it with a concrete statement.

### P-60 It goes without saying

Severity: `tell`

Says what supposedly need not be said.

**Bad:**

> It goes without saying that quality matters.

**Better:**

> Cut it.

**Fix:** Cut it or replace it with a concrete statement.

### P-61 In a world where

Severity: `tell`

Movie-trailer opening.

**Bad:**

> In a world where data is everything, ...

**Better:**

> Open with the problem your readers have today.

**Fix:** Cut it or replace it with a concrete statement.

### P-62 Unprecedented / transformative

Severity: `tell`

Superlatives without a comparison.

**Bad:**

> An unprecedented, transformative shift.

**Better:**

> Say what changed compared to [your reference point].

**Fix:** Cut it or replace it with a concrete statement.

### P-63 Rest assured

Severity: `tell`

Reassurance formula.

**Bad:**

> Rest assured, your data is safe.

**Better:**

> Say how the data is protected.

**Fix:** Cut it or replace it with a concrete statement.

### P-64 Not only ... but also (as a pattern)

Severity: `tell`

Double construction that inflates both halves.

**Bad:**

> It saves not only time but also money.

**Better:**

> It saves time and money.

**Fix:** Cut it or replace it with a concrete statement.

### P-65 Crucial

Severity: `hint`

Frequent importance word.

**Bad:**

> Planning is crucial.

**Better:**

> Say what planning prevents.

**Fix:** Cut it or replace it with a concrete statement.

### P-66 Vital / essential

Severity: `hint`

Must-have words, often without a reason.

**Bad:**

> A newsletter is essential.

**Better:**

> Say what is missing without one.

**Fix:** Cut it or replace it with a concrete statement.

### P-67 Best practices

Severity: `hint`

Jargon, often without content.

**Bad:**

> We follow best practices.

**Better:**

> Name the one practice you use.

**Fix:** Cut it or replace it with a concrete statement.

### P-68 Dynamic

Severity: `hint`

Energy adjective without content.

**Bad:**

> A dynamic team.

**Better:**

> Say what the team does.

**Fix:** Cut it or replace it with a concrete statement.

### P-69 Numerous benefits

Severity: `tell`

Quantity claimed, not listed.

**Bad:**

> The method offers numerous benefits.

**Better:**

> Name the two main benefits.

**Fix:** Cut it or replace it with a concrete statement.

### P-70 Make a difference

Severity: `tell`

Effect claimed without a comparison.

**Bad:**

> Small details make all the difference.

**Better:**

> Name the detail and what it changed.

**Fix:** Cut it or replace it with a concrete statement.

### P-71 Increasingly important

Severity: `tell`

Trend claim without a date.

**Bad:**

> Reviews are increasingly important.

**Better:**

> Say how you notice reviews matter more.

**Fix:** Cut it or replace it with a concrete statement.

### P-72 Optimal results

Severity: `hint`

Promise without a measure.

**Bad:**

> Get optimal results.

**Better:**

> Name the result you expect.

**Fix:** Cut it or replace it with a concrete statement.

### P-73 In essence / Essentially

Severity: `hint`

Compression announcement.

**Bad:**

> In essence, it is about trust.

**Better:**

> Say what the trust rests on.

**Fix:** Cut it or replace it with a concrete statement.

## Structure

Recurring shapes: the setup and reveal, lists of three everywhere, headings that ask questions the paragraph never answers, a summary after every section.

### T-01 Contrast template

Severity: `tell`

"It's not X. It's Y." and similar set-ups that invent a position only to knock it down. Once is a hint, twice is a pattern.

**Bad:**

> It's not about reach. It's about trust.

**Better:**

> Trust brings us more enquiries than reach: [your observation].

**Fix:** Drop the straw position and argue your point directly.

### T-02 Stacked lists of three

Severity: `tell`

Three items in a row again and again ("fast, simple and secure"). One is normal, many sound mechanical.

**Bad:**

> Fast, simple and secure. Clear, precise and accessible.

**Better:**

> Name only the quality you can back up, and back it up.

**Fix:** Shorten the lists: two items, or one with evidence.

### T-03 Connector at the start of a sentence

Severity: `tell`

Repeated sentence openers like "Moreover", "Furthermore", "Additionally". They stack rather than connect.

**Bad:**

> Moreover, it is cheap. Furthermore, it is fast.

**Better:**

> It is cheap and fast because [reason].

**Fix:** Cut the connector or state the relation (because, so, but).

### T-04 Same sentence openings

Severity: `tell`

Three or more sentences in a row start with the same word.

**Bad:**

> You plan. You write. You check.

**Better:**

> Vary the openings or turn the steps into a list.

**Fix:** Vary the openings or merge the sentences.

### T-05 Rhetorical question as opener

Severity: `tell`

A paragraph opens with a question it answers itself right away. Once is fine, repeated it reads like a template.

**Bad:**

> Why does this matter? Because customers compare.

**Better:**

> Customers compare before they get in touch: [how you notice].

**Fix:** Write the answer as the first sentence.

### T-06 Colon reveal

Severity: `tell`

A short lead-in with a colon or question mark builds fake suspense ("The result:", "The reason?").

**Bad:**

> The result? More enquiries.

**Better:**

> We got more enquiries afterwards, about [your number] a week instead of [before].

**Fix:** Build a normal sentence: subject, verb, claim.

### T-07 Grand closing line

Severity: `tell`

The last sentence ends with a grand gesture ("The future is yours", "The first step starts today").

**Bad:**

> The future belongs to those who act now.

**Better:**

> End with a concrete next step: [what the reader can do tomorrow].

**Fix:** Cut the closing line or replace it with a concrete step.

### T-08 Summary ending

Severity: `tell`

The text ends by repeating itself ("In summary", "All in all").

**Bad:**

> In summary, planning is important.

**Better:**

> End with an open question from your practice or the next step.

**Fix:** Cut the closing paragraph or replace it with something new.

### T-09 Trailing participle clause

Severity: `tell`

A sentence gets an interpretation tacked on at the end (", highlighting ...", ", underscoring ...").

**Bad:**

> Revenue rose, highlighting the importance of SEO.

**Better:**

> Revenue rose. Most of it came from [your source of enquiries].

**Fix:** Cut the tail or turn it into its own sentence with evidence.

## Rhythm

Measured on the whole text and compared with a range from human-written reference texts. Too even is a finding, and so is overshooting the other way.

### R-01 Short sentences

Severity: `hint`

Average words per sentence. Generated expert texts have markedly shorter sentences on average than the human texts in the comparison band.

**Bad:**

> Every sentence is short. Every sentence ends fast. No thought develops.

**Better:**

> Join thoughts that belong together into one sentence and give the reason [because ...].

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-02 Uniform sentence lengths

Severity: `hint`

Spread of sentence lengths within paragraphs (coefficient of variation). Very even sentences sit on the generated-text side.

**Bad:**

> All sentences have about the same length and shape.

**Better:**

> Mix short and long sentences, the way you talk.

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-03 Short paragraphs

Severity: `hint`

Average words per paragraph. Generated texts split content into many short paragraphs.

**Bad:**

> One paragraph, one sentence. Then the next paragraph.

**Better:**

> Merge paragraphs that carry one thought together.

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-04 High vocabulary variety

Severity: `hint`

Vocabulary variety (MATTR, 50-word window). Generated texts repeat words less often and switch synonyms more than human texts.

**Bad:**

> Solution, approach, method, strategy: four words for one thing.

**Better:**

> Keep the technical term when you mean the same thing.

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-05 Long words

Severity: `hint`

Average word length in letters. Generated texts reach for long, abstract words more often.

**Bad:**

> Operational efficiencies are strategically maximised.

**Better:**

> Say what gets faster: [process].

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-06 Nominal style

Severity: `hint`

Words ending in -tion, -sion, -ment, -ness, -ity per 1,000 words.

**Bad:**

> The implementation of the optimisation follows the assessment.

**Better:**

> We optimise after we have assessed [object].

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-07 Many lists of three

Severity: `hint`

Lists of the form "A, B and C" per 1,000 words. Adds a measured rate to pattern T-02.

**Bad:**

> Fast, secure and simple. Clear, precise and accessible.

**Better:**

> Name only what is true, even if it is two things.

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-08 Many colons

Severity: `hint`

Colons in running text per 1,000 words (not times or links).

**Bad:**

> The goal: growth. The path: clarity. The result: success.

**Better:**

> Write full sentences instead of "term: explanation".

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-09 Trailing participles (rate)

Severity: `hint`

Clauses like ", ensuring ..." or ", making ..." per 1,000 words. Adds a measured rate to pattern T-09.

**Bad:**

> We review every text, ensuring the highest quality.

**Better:**

> We review every text because [reason].

**Fix:** Only a hint: a single value outside the band is common in human texts too. It counts only in combination (R-10).

### R-10 Many measurements on the AI side

Severity: `tell`

At least as many measured features as the band's verdict limit sit outside the band on the generated-text side at the same time. A single feature is only a hint, the combination is a finding.

**Bad:**

> Short sentences, short paragraphs, many colons and lists of three in one text.

**Better:**

> Rewrite in your own structure: fewer subheadings, longer thoughts, concrete examples [from your work].

**Fix:** Work on the reported measurements one by one, not just swapping words.

## Form

Typography and layout: long dashes used as a stylistic device, emoji bullets, bold words scattered through running text.

### F-01 Em dash

Severity: `tell`

Style rule: the em dash (U+2014) outside quotations. Many readers see long dashes as typical of AI. In our measurements it does not separate human from generated text, so it is a style rule you can switch off (config "dashes").

**Bad:**

> The result — more enquiries.

**Better:**

> The result: more enquiries.

**Fix:** Replace it with a period, comma, colon or parentheses.

### F-02 En dash used as a dash

Severity: `tell`

The en dash (U+2013) is right between numbers (10–20); between words it works as a dash.

**Bad:**

> Fast – and cheap.

**Better:**

> Fast and cheap.

**Fix:** Replace it with a comma, period or colon.

### F-03 Hyphen used as a dash

Severity: `tell`

" - " with spaces stands in for a dash.

**Bad:**

> Fast - and cheap.

**Better:**

> Fast and cheap.

**Fix:** Replace it with a comma, period or colon.

### F-04 Emojis

Severity: `hint`

Emojis in expert text. Default: more than one per section is a hint. With emojis: no, each one is a finding.

**Bad:**

> 🚀 Start now 💪

**Better:**

> Start now.

**Fix:** Remove the emoji.

### F-05 Bold overload

Severity: `tell`

Many bold passages in one paragraph. When everything is emphasised, nothing is.

**Bad:**

> **Important:** Use **clear** goals and **measurable** values.

**Better:**

> Use clear goals and measurable values. Bold at most the one term readers need to find again.

**Fix:** Reduce bold to one term per section.

### F-06 Label heading

Severity: `tell`

Headings like "What is X?", "Conclusion" or "Introduction" say where you are, not what you learn.

**Bad:**

> ## Conclusion

**Better:**

> ## What to change first tomorrow

**Fix:** Rewrite the heading as a statement or promise.

### F-08 Too many headings

Severity: `tell`

Many headings for little text. The text breaks into fragments.

**Bad:**

> A new subheading every 60 words.

**Better:**

> Merge sections until each one has something to say.

**Fix:** Merge sections.

### F-09 Banned word (your list)

Severity: `fail`

A word from your own banned list (option --forbid or forbid in .slopcheck.json).

**Bad:**

> [a word from your list]

**Better:**

> [your preferred wording]

**Fix:** Replace or cut the word.
