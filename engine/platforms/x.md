# X (Twitter) Platform

Rules for creating X posts. Based on the open-sourced algorithm (xAI January 2026 release) and confirmed engagement weights.

---

## Algorithm: Grok-Powered Transformer (2026)

X uses a three-stage pipeline:
1. **Candidate Sourcing** — pulls ~1,500 posts from 500M daily tweets (50% from people you follow, 50% from people you don't)
2. **Neural Network Ranking** — Grok-powered transformer scores each post by predicting how likely YOU are to engage
3. **Filtering** — author diversity caps, negative feedback suppression, content safety

The "For You" feed is fully algorithmic. Half of what people see is from accounts they DON'T follow. This is where viral reach happens.

---

## Ranking Signals (Confirmed Weights)

From the open-sourced algorithm code:

| Signal | Weight | What It Means |
|--------|--------|--------------|
| Reply + author replies back | 150x | THE most powerful signal. You reply AND they respond. |
| Retweet/Repost | 20x | Someone shares to their network |
| Reply | 13.5x | Someone writes back |
| Profile click | 12x | Someone checks who you are |
| Link click | 11x | Someone clicks through |
| Bookmark | 10x | Someone saves for later |
| Dwell time (2+ min) | 10x | Someone reads the whole thing |
| Like | 1x | Weakest signal. Almost irrelevant alone. |

**Key insight:** One genuine reply chain where you engage back = 150 likes. Conversation is everything. Likes are nearly worthless.

---

## What Gets Reach

1. **Spark replies.** Posts people want to argue with, answer, or add to. Ask questions. State opinions. Be intentionally incomplete.
2. **Reply to your replies.** The +150x signal. Respond to every genuine reply in the first 30 minutes. This is the single highest-leverage action.
3. **Bookmarkable content.** Frameworks, data, reference material. Bookmarks are 10x likes.
4. **Stay in your niche.** X uses SimClusters (145,000 topic clusters). Consistent topics = stronger cluster match = more discovery.
5. **Native media.** Video uploaded directly (not YouTube links). Images that require tap-to-expand.

---

## What Kills Reach

| Killer | Impact | Why |
|--------|--------|-----|
| External links in post body | -50 to -80% reach | X wants users ON the platform |
| Getting muted/blocked | Destroys future reach | Negative signals compound for 30 days |
| Posting too often | Diminishing returns | Author diversity cap: ~3 posts per feed window |
| Engagement bait | Down-ranked | "Like if you agree" detected and suppressed |
| AI/spam content | Flagged by Grox classifier | Low-quality patterns get suppressed |
| Unedited AI output | Detected | March 2026 reply downvote system targets AI spam |
| Hashtag spam | -40% reach | Max 1-2 relevant hashtags. Multiple = penalty |

---

## Format Priority (What Performs Best)

| Rank | Format | Why |
|------|--------|-----|
| 1 | Text-only (opinion/question) | Outperforms video by 30% on X. Sparks replies. |
| 2 | Native video (<2:20) | 3.4-5x distribution boost. Hook in first 3 seconds. |
| 3 | Native images/infographics | Tap-to-expand counts as engagement signal |
| 4 | Threads (4-8 tweets) | Dwell time compounds. 1-2 per week. |
| 5 | Polls | Dwell time + reply generation |
| AVOID | Link-first posts | Severely throttled |

**Text-first is king on X.** Unlike every other platform, plain text outperforms video.

---

## Post Specs

| Spec | Recommendation |
|------|---------------|
| Character limit (free) | 280 |
| Character limit (Premium) | 4,000 |
| Sweet spot | 71-100 characters for engagement, 240-259 for max likes |
| Hashtags | 0-1. More than 2 = penalty |
| Images | 1200x675px or vertical (forces tap-to-expand) |
| Video | Native upload only. Under 2:20. Hook in 3 seconds. Captioned (80% watch muted). |
| Threads | 4-8 tweets. Include visuals. 1-2 per week max. |
| Links | NEVER in the main post. Always in a reply to your own post. |

---

## Posting Best Practices

| Factor | Recommendation |
|--------|---------------|
| Frequency | 2-3 posts/day (including replies). Space 4-6 hours apart. |
| Best days | Tuesday, Wednesday, Thursday |
| Best times | 9 AM-3 PM weekdays (your audience's timezone) |
| Critical window | First 30 minutes. Be present. Reply to every engagement. |
| Reply to replies | Within first 30 min. This is the +150x signal. |
| Engage on others' posts | 15-30 min/day replying to bigger accounts in your niche |

---

## The First 30 Minutes Rule

X evaluates your post's early performance to decide whether to expand it:

- **0-5 min:** 3+ engagements → initial boost (shown to 2-3x more followers)
- **5-15 min:** 10+ engagements → secondary boost (shown to non-followers)
- **15-30 min:** 50+ engagements → viral amplification (broad audience)
- **After 30 min:** Momentum slows. Needs sustained engagement.

**Implication:** Post ONLY when you can be present for the next 30 minutes to reply. Never post and leave.

---

## Post Structure

```
[Strong opening — opinion, question, or claim]
[Body — 1-3 short lines]
[Close — question, challenge, or incomplete thought that invites reply]
```

### Reply-generating patterns:

| Pattern | Example | Why It Works |
|---------|---------|-------------|
| Open question | "What's your biggest [X] failure?" | Demands specific experience |
| Fill-in-the-blank | "The most underrated skill is ___" | Low friction to complete |
| Intentional gap | List with obvious missing item | People can't resist adding |
| Hot take + nuance | "Hot take: [X]. But here's why..." | Invites debate, reduces blocks |
| Correctable statement | Slightly wrong claim | Experts will correct you |
| Specific opinion | "Tool X is better than Y because..." | Forces people to pick sides |

---

## X Premium

Premium subscribers get significant algorithmic advantages:

| Factor | Free | Premium |
|--------|------|---------|
| Median reach | <100 impressions | 600+ (roughly 10x) |
| In-network boost | None | 4x |
| Out-of-network boost | None | 2x |
| Reply visibility | Baseline | Prioritized in threads |
| Character limit | 280 | 4,000 |
| Video upload | 140s / 512MB | Extended |
| Link suppression | Severe | Reduced |

**Premium is nearly required for organic growth in 2026.** The reach gap is the largest of any social platform.

---

## TweepCred (Account Reputation)

Every account has a hidden reputation score (0-100):
- **Below 65:** Only 3 of your tweets are considered for distribution
- **Above 65:** All tweets eligible
- **Factors:** Account age, follower-to-following ratio, engagement quality, interactions with high-quality accounts
- **Premium boost:** +4 to +16 points

---

## X-Specific Anti-Patterns

Beyond general anti-AI rules, avoid these on X:
- "Like and RT for..." (engagement bait, detected and suppressed)
- Posting 10+ times a day (author diversity cap kills individual post reach)
- Threads about nothing (dwell time only works if content is actually good)
- Ratio-bait without nuance (gets replies but also blocks, which destroy future reach)
- Generic engagement pod activity (Grox spam classifier detects coordinated low-follower replies)
- Buying followers that don't engage (lowers your engagement rate, which the algorithm reads as "shown and ignored")

**On the reply-generating patterns above:** use them, but don't run the same one every day — "Hot take: [X]. But here's why..." as a daily skeleton reads as AI and the Grox classifier is tuned for exactly these repeated templates. The reply they generate still has to be earned with a specific, arguable claim. "Tool X is better than Y" generates nothing; "Claude is better than GPT for refactoring because it holds 10 files in context without losing the thread" generates a fight. Specificity is what makes a post arguable — vague takes get scrolled past.

---

## Key Differences from LinkedIn

| Factor | LinkedIn | X |
|--------|----------|---|
| Top signal | Saves | Replies (especially author reply-back) |
| Best format | Text + data | Text-only |
| Link handling | In first comment | In reply to own post |
| Hashtags | 3-5 | 0-1 |
| Tone | Professional-conversational | Direct, punchy, opinionated |
| Post length | 800-1,500 chars sweet spot | 71-280 chars sweet spot |
| Best days | Thu-Sun | Tue-Thu |
| Premium impact | Moderate | Nearly required |
| Memes | Image + caption | Text-first humor often wins |
| Content decay | Slower (days) | Fast (half-life ~6 hours) |
