# LinkedIn Carousel Practices — PMM Brain-Native

---

## Format Specs

- **Dimensions:** 1080x1080px square (LinkedIn optimal)
- **Slide count:** 5-10 slides
- **One key point per slide.** Max 3-4 lines of text per slide.
- **Generated as:** Visual brief + Pillow-based image (uses existing visual skill)

---

## Slide Structure

### Slide 1: Cover
- **Hook** — visual version of the 5 hook types from generation-angles.md
- **Title** — bold, clear, specific. Numbers work well.
- **Brand mark** — "AllAboutPMM" white text on dark pill, bottom-right
- The cover must work as a standalone image (it's the thumbnail in the feed)

**Cover patterns:**
- "X Things Most PMMs Get Wrong About [Topic]"
- "The [Framework Name]: How to [Outcome]"
- "From [Bad State] → [Good State]: A PMM Guide"
- "[Number] That Changed How I Think About [Topic]"

### Slides 2-8/9: Content Slides
- **One key point per slide.** No exceptions.
- **Max 3-4 lines of text.** If it doesn't fit, split into two slides or sharpen.
- **Progressive build:** Each slide builds on the previous. Not random facts — a narrative.
- **Use slide transitions:** "But here's the problem..." / "The fix:" / "Step 1:" / "Most people stop here."
- **Evidence per slide:** Where possible, include a stat, example, or proof point.

**Content slide patterns:**
- Claim + evidence (one stat or example)
- Before → After comparison
- Step in a framework (numbered)
- Common mistake + fix
- Quote or insight attribution

### Slide 9/10: Close
- **CTA** — Follow AllAboutPMM / Comment your approach / Share with your team
- **Brand mark** — same placement as cover
- **Optional:** Summary of key takeaways in 3-4 bullet points

---

## Visual Design Rules

Uses the existing visual signature from `skills/visual/SKILL.md`:
- **Background:** Cream (#F5F2ED)
- **Title font:** Georgia Bold
- **Body font:** Arial Regular
- **Accent colors:** Max 3 muted pastels — yellow (#F7DC6F), pink (#F5B7B1), green (#ABEBC6), teal (#5BA4A4)
- **Outlines:** Thin black (1.5-2px), no gradients, no shadows, no icons
- **Brand mark:** "AllAboutPMM" white text on dark pill, bottom-right corner

---

## Carousel Types (Map to 3 Angles)

| Carousel Type | Maps to Angle | Slide Structure |
|---------------|---------------|-----------------|
| **Framework walkthrough** | Framework/Mental Model | Cover → Context → Steps 1-5 → Application → CTA |
| **Myth-busting** | Opinionated Reframe | Cover → Myth 1 + Reality → Myth 2 + Reality → ... → Core lesson → CTA |
| **Teardown** | Story-Led | Cover → "Here's what [Company] did" → Slide-by-slide analysis → Lessons → CTA |
| **Comparison** | Any | Cover → Option A → Option B → Key differences → When to use each → CTA |
| **Checklist** | Framework/Mental Model | Cover → Item 1 → Item 2 → ... → Summary → CTA |

---

## Content Extraction for Carousels

When atomizing from a newsletter or long-form post:
1. Identify the **core framework or progression** — this becomes the slide sequence
2. Extract **one key point per slide** — the sharpest version of each idea
3. Find **one evidence anchor per 2-3 slides** — stats or examples that fit in 1 line
4. Write **slide transition phrases** — maintain narrative flow between slides
5. Design the **cover hook** — adapted from the post's hook, visual-first

---

## AI Decontamination

Same rules apply per slide. Additional carousel-specific rules:
- No "Let's dive in" on slide 2
- No "Key Takeaways" as a generic header — be specific about what the takeaway IS
- No filler slides that exist only to pad the count
- Every slide must add new information or reframe existing information

---

## Hard Constraints

- **5-10 slides.** Under 5 feels thin. Over 10, people stop swiping.
- **One point per slide.** The moment a slide tries to do two things, split it.
- **Cover must work as thumbnail.** It's the first thing people see in the feed.
- **AllAboutPMM brand consistency** across all visual outputs.
- **At least 1 evidence anchor per carousel** (stat, case study, real example).

---

## Output Template

```
# Carousel: [Title]

**Slides:** [N]
**Type:** [Framework / Myth-busting / Teardown / Comparison / Checklist]
**Evidence anchors:** [list]

---

## Slide-by-Slide Brief

**Slide 1 (Cover):**
- Title: [Hook text]
- Subtitle: [Optional supporting text]

**Slide 2:**
- Header: [Point]
- Body: [2-3 lines max]

...

**Slide N (Close):**
- CTA: [Specific action]
- Brand: AllAboutPMM

---

## Visual Notes
[Any specific design instructions for this carousel]
```
