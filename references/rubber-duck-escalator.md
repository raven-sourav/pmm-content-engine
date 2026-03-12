# Rubber Duck Escalator — 5-Phase Critique Protocol

Every draft passes through 5 sequential phases. Each phase has a unique lens.
Phases see prior phase results (cascading context) to avoid redundant critiques.

---

## Phase 1: MIRROR — Does this reflect real experience?

**Lens:** Experiential authenticity. Is this lived or Googled?

**Look for:**
- Specific moments, decisions, observations from being in the room
- Sensory details, named contexts, emotional textures
- Difference between "In my experience, X" (generic) vs "When I [action] at [context], I noticed [observation]" (real)

**Red flags:** Passive voice for experience, hypothetical framing, generic "lessons learned", reads like a blog summary

**Scoring:**
- 9-10: 2+ specific, verifiable personal moments. Reader could NOT write this without living it.
- 7-8: Experiential framing but moments generic enough anyone could claim them.
- 5-6: Primarily knowledge-reporting with thin experiential veneer.
- 3-4: Blog post or textbook summary.
- 1-2: Pure abstraction, no human signal.

---

## Phase 2: PROBE — What uncomfortable truth is being dodged?

**Lens:** Courage. Does the post confront difficulty or retreat to safety?

**Look for:**
- Claims that sound bold but avoid the hard part
- Missing counterarguments a sharp reader would immediately think of
- Convenient omissions that would complicate the narrative
- "Answer to a question nobody asked" — is this solving a real problem?

**Red flags:** False dichotomy, ignores strongest counterargument, uses "many companies" instead of specifics, thesis requires no courage

**Scoring:**
- 9-10: Directly confronts the hardest question. Reader feels uncomfortable. Author took a real risk.
- 7-8: Addresses difficulty but pulls punches slightly.
- 5-6: Acknowledges complexity then retreats to safe ground.
- 3-4: Avoids all difficulty. Generic advice that offends no one.
- 1-2: Pure platitude.

---

## Phase 3: CHALLENGE — Where is the logic soft?

**Lens:** Rigor. Every claim needs support. Every argument must be non-reversible.

**Look for:**
- Unsupported claims (assertion without evidence)
- Circular reasoning ("X is important because X matters")
- Framework hiding (using a framework name instead of actually arguing)
- False dichotomies, correlation-as-causation
- The reversibility test: swap the thesis — does it still sound true?

**Evidence check:** Does the post cite specific data/examples? At least ONE concrete evidence anchor?

**Scoring:**
- 9-10: Every claim supported. Argument non-reversible. Evidence specific and relevant.
- 7-8: Most claims supported, 1-2 soft spots. Overall logic holds.
- 5-6: Multiple unsupported claims. Framework referenced but not applied.
- 3-4: Mostly assertion. Could be reversed easily.
- 1-2: No logical structure. Pure opinion.

---

## Phase 4: ILLUMINATE — Is the insight earned and non-obvious?

**Lens:** Insight quality + synthesis. Does the post deliver a genuinely non-obvious insight, and does it BUILD to something greater than its parts?

**Look for:**
- Observations sitting side-by-side but not connected
- A pattern the post circles around but never names
- Two ideas from different domains that, connected, create genuine insight
- The "so what?" test: does the reader get a new mental model or just information?
- The insight novelty test: would a PMM with 3 years experience already know this?
- The earned insight test: does this require having DONE the thing, not just read about it?

**Red flags:** List of true things that don't build, "insight" is just a thesis restatement, framework without connection to reader's situation, insight that any informed practitioner would already agree with, opinion without evidence

**Scoring:**
- 9-10: Reveals a connection the reader hasn't seen before. Insight is clearly earned from experience or original synthesis. Clear "aha" moment.
- 7-8: Coherent thread, insight has some edge but a sharp reader might say "I kind of knew that."
- 5-6: Informative but insight is surface-level. Facts, not connections. A well-read PMM already knows this.
- 3-4: A list. True items, no thread. Insight is generic.
- 1-2: No coherent argument or insight. Platitudes.

---

## Phase 5: CRYSTALLIZE — Does it sound like THIS person (and NOT like AI)?

**Lens:** Voice authenticity + AI decontamination. Two checks: does it sound like the author, and does it sound human?

### Check A: Voice Match
- Hook uses one of the 4 hook types (Stat Drop, Scene Drop, Name+Claim, Before/After)?
- Sentence rhythm match? (Short, punchy, direct — not balanced and flowing)
- Vocabulary tier match? (Operator language, not consultant language)
- Tone markers match? (Data-driven, teardown-oriented, startup-focused)

### Check B: AI Pattern Scan
Run the draft against these AI tells. Flag ANY match as a failure:

**Word-level scan:**
- Any AI vocabulary? ("Additionally", "Furthermore", "Moreover", "testament", "landscape", "showcasing", "delve", "realm", "crucial", "pivotal", "robust", "comprehensive", "streamline", "harness")
- Any copula avoidance? ("serves as", "functions as", "acts as" instead of "is")
- Any filler phrases? ("In order to", "It is worth noting", "It's important to remember")
- Any promotional adjectives? ("groundbreaking", "transformative", "revolutionary", "cutting-edge")

**Sentence-level scan:**
- Any "It's not just X, it's Y" patterns?
- Any synonym cycling (same concept, 3+ different words)?
- Any forced rule-of-three lists?
- Any hedging stacks ("could potentially")?
- Any significance inflation ("pivotal moment", "defining shift")?

**Structure-level scan:**
- Balanced hedging with "it depends" conclusion?
- Generic conclusion ("The future looks bright", "Time will tell")?
- Setup-payoff padding ("Let's explore..." → content → "As we've seen...")?
- Any sentence that could appear in a generic ChatGPT response?

**Brevity scan:**
- Any transition sentences that can be deleted without losing meaning?
- Any warm-up paragraph before the actual point?
- Over 1200 characters without strong justification?

### Ultimate tests:
- Is there ONE sentence only THIS person, with THEIR operator experience, could have written?
- Does it feel like a real person talking, or like "content"?
- Read it aloud: does it sound like someone talking, or like something generated?

**Red flags:** MBA voice ("leverage", "synergize"), generic LinkedIn voice ("Here's the thing", "Game-changer"), AI voice (perfectly balanced, hedging every claim, synonym cycling, filler phrases, promotional adjectives), forbidden patterns

**Scoring:**
- 9-10: Unmistakably this person's voice. Zero AI tells. At least one "only they could have written this" sentence. Tight — no filler.
- 7-8: Mostly their voice, 1-2 minor AI patterns slip in. Still reads human.
- 5-6: Competent writing but could be anyone. Multiple AI tells present. Generic vocabulary.
- 3-4: Generic LinkedIn tone. Interchangeable author. Reads like AI with light editing.
- 1-2: Clearly AI-generated. Multiple pattern matches across all levels.

---

## Gate Rules

- **Threshold:** All 5 phases must score 8+ to pass
- **Below 8 on any phase:** Rewrite targeting failures, protect passes
- **Max iterations:** 3 rewrites before flagging to user with notes
- **Abort valve:** If composite score < 4.0 after iteration 1, skip to user — draft needs fundamental rethinking
- **Score inflation prevention:** Critique first, score based on own critique (score-last). Average LinkedIn draft = 5.5. 8+ = top 20%. Must quote specific lines justifying 8+.
- **Regression guard:** If rewrite drops a previously-passing phase, flag REGRESSION
- **Insufficient progress:** If phase improves by only 1 point but still fails, flag INSUFFICIENT PROGRESS

## Rewrite Protocol

When rewriting after failures:
1. Rank failures by severity (lowest score first)
2. Address worst failure's root cause, not symptoms
3. Protect all passing phases — do NOT regress them
4. Maintain core argument and structure unless CHALLENGE flagged structural issues
5. Stay within +/- 15% of original length
6. Use available evidence anchors to strengthen weak claims
7. On iteration 3+: be MORE aggressive — address root cause, not symptoms

---

## Format Calibration

The same 5 phases apply to ALL formats. Scoring expectations adjust by format.

### Newsletter Calibration
- **MIRROR:** Demands 2-3 specific experiential moments (vs 1 for LinkedIn). The longer format must show MORE lived experience, not diluted experience.
- **PROBE:** Same courage bar. Newsletter depth means counterarguments MUST be addressed directly — no dodging.
- **CHALLENGE:** Demands 3+ evidence anchors with newsletter source cross-references. Framework must be fully developed, not just named.
- **ILLUMINATE:** Insight must justify newsletter length. If the insight could fit in a LinkedIn post, the newsletter is padded. Look for the "only I could have written this" section (200+ words).
- **CRYSTALLIZE:** Check 1500-3000 word range. Subject line quality check (specific, not clickbait). AI pattern risk is HIGHER in long form — scan aggressively. Verify P.S. is present and strategic.

### Twitter/X Thread Calibration
- **MIRROR:** Assess thread arc holistically — does the sequence feel like one person's coherent thinking? Not a list of disconnected facts.
- **PROBE:** Each tweet should advance the argument. No filler tweets that exist only to pad the count.
- **CHALLENGE:** Check that each tweet has a micro-claim or micro-evidence. Thread must build, not repeat.
- **CRYSTALLIZE:** Character count validation — EVERY tweet must be ≤280. Voice check per tweet — each should sound like Sourav, not a content generator. Hook tweet must work standalone.
- **Brevity scan (additional):** If removing a tweet doesn't weaken the thread, cut it. A tight 7-tweet thread beats a padded 12-tweet thread.

### Carousel Calibration
- **MIRROR + PROBE:** Assess full narrative arc — do slides progress logically? Does the sequence tell a story?
- **CHALLENGE:** At least 1 evidence anchor per carousel. Each slide must add new information.
- **ILLUMINATE:** Framework/progression must be clear enough to stand without narration.
- **CRYSTALLIZE:** Check visual + text brand consistency (cream bg, Georgia Bold, muted pastels, AllAboutPMM mark). Text per slide ≤4 lines. Cover slide must work as standalone thumbnail.

### LinkedIn Calibration (Default)
No changes from base protocol. 800-1200 characters, 1 evidence anchor minimum, all standard rules apply.
