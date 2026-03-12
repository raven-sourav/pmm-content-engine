# Research Protocol — Deep Research Before Drafting

Research runs BEFORE drafting. Always. No exceptions.

---

## Stage 1: Web Research Synthesis

Search the theme from MULTIPLE angles (minimum 5-8 queries):

| Angle | Search Pattern |
|-------|---------------|
| Statistics | `"{theme}" statistics data 2024 2025` |
| Contrarian | `"{theme}" criticism problems wrong` |
| Case studies | `"companies {theme} case study example"` |
| Recent (90 days) | `"{theme}" 2025 latest news trends` |
| Adjacent domains | Analogies from sales, engineering, design, behavioral economics |
| Practitioner | `"{theme}" lessons learned advice` |

**Priority sources:** Lenny's Newsletter, First Round Review, a16z, HBR, practitioner blogs, company reports, academic research.
**De-prioritize:** Generic listicles, SEO filler, undated content.

**Output: Research Brief** containing:
- Key claims (with source URLs, dates, confidence)
- Evidence anchors (stats, case studies, analogies — each with source)
- Contrarian angles (with supporting evidence, novelty estimate)
- Narrative hooks (compelling openings tied to evidence)
- Saturation report (how much has already been said, what's under-explored)

**Freshness scores:** <30 days = 1.0, 30-90 = 0.7, 90-180 = 0.4, >180 = 0.2

---

## Stage 2: Gap Map Construction

Cross-reference research against:
- User's past posts (from ChromaDB)
- Reference writers' posts (from ChromaDB)
- PMM value landscape (from Brain)

**Output: Gap Map** containing:
- Already said (claims well-covered — SKIP, REFRAME, or DEEPEN)
- White space (angles nobody has covered well — highest value)
- User unique angles (where the user has unique standing to contribute)
- Recommended angles (3 angles ranked by novelty + freshness + evidence support)

---

## Stage 3: Insight Novelty Scoring

Before assigning angles, score every candidate insight on a 1-5 Insight Novelty Scale:

| Score | Level | Definition | Example |
|-------|-------|------------|---------|
| 5 | **Earned** | Could only come from operator experience or original synthesis of non-obvious sources. Reader thinks "I never connected those dots." | Connecting churn data to a positioning failure nobody else blamed |
| 4 | **Opinionated** | Takes a clear stance backed by evidence. Not obvious, but not shocking. Reader thinks "That's a sharp take, and they backed it up." | Arguing messaging should be owned by product, not marketing — with specific data |
| 3 | **Informed** | Accurate, well-sourced, but most practitioners in the space would nod along. No surprise. | "Companies that invest in positioning see better win rates" |
| 2 | **Surface** | True but generic. Could appear in any PMM blog or LinkedIn post. No edge. | "Product marketing is about knowing your customer" |
| 1 | **Obvious** | Platitude or widely known fact dressed up as insight. | "Differentiation matters in competitive markets" |

**Gate rule:** Only insights scoring 4+ ("Opinionated" or "Earned") proceed to drafting. Insights scoring 3 may proceed ONLY if combined with a 4+ insight to create a sharper argument.

**How to score:**
1. Ask: "Would a PMM with 3 years of experience already know this?" — If yes, it's a 3 or below.
2. Ask: "Does this require having DONE the thing, not just read about it?" — If yes, it's likely a 4+.
3. Ask: "Can I reverse this claim and it still sounds reasonable?" — If yes, it's a 2 or below.
4. Ask: "Does this connect two things that aren't usually connected?" — If yes, it's likely a 5.

---

## Stage 4: Anchor Assignment + Angle Generation

Assign specific evidence anchors to each of the 3 recommended angles.

**Output: DraftBrief** with 3 angle assignments:
- Contrarian angle + evidence + suggested hook + Insight Novelty Score
- Framework angle + evidence + suggested hook + Insight Novelty Score
- Story angle + evidence + suggested hook + Insight Novelty Score

**Validation:**
- Reject any angle with no evidence anchor.
- Reject any angle with Insight Novelty Score below 4.
- If all angles score below 4, go back to Stage 2 and dig deeper — the research hasn't found the real insight yet.

---

## Requirements

- Every claim must have a source URL
- At least 3 evidence anchors total
- At least 1 contrarian angle
- If >60% of results converge on the same claim, flag as saturated
- Never repeat what the user has already written about
