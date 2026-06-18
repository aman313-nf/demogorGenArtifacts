# Company profile — Handshake AI

> DLP/data-security demo profile. Everything downstream (personas, carriers, planted
> values) derives from this. Researched June 2026.

## 1. What they do
- **Company**: Handshake (joinhandshake.com) — began as the early-career recruiting
  network connecting **18M students/alumni** with employers across **1,500 university
  partners**. In 2024–25 it launched **Handshake AI**, a "startup-within-a-startup"
  that turned its verified-academic network into an **expert data business for frontier
  AI labs**: PhDs and grad students develop prompts, write rubrics, and evaluate model
  outputs ("model validation") that get piped into labs' training pipelines.
- **Two data worlds under one roof**:
  1. **Career network** — student/alumni PII at consumer scale, university (education)
     records, employer accounts.
  2. **Handshake AI** — a network of **500k+ PhDs / 3M+ grad scholars** (contractors
     paid **$40–$125/hr**) and a **proprietary annotation platform** that handles
     **confidential frontier-lab project data** (prompts, eval rubrics, model outputs)
     under strict NDA. Acquired **Cleanlab** (data-quality ML) for talent + tech.
- **Customers**: frontier AI labs (the eval/training data is their IP); plus employers
  and universities on the legacy network.
- **Regulatory / contractual regime**: **FERPA** (student education records via the
  university network), **GDPR/CCPA** (consumer PII at scale), **SOC 2** (table stakes to
  sell to frontier labs), **IRS 1099/W-9** handling for contractor experts (SSN/TIN +
  bank payout data), and **NDA/confidentiality** with labs — arguably their single
  highest-stakes obligation, since a leak of a lab's eval set breaks the trust the
  $100M+ business is built on.
- **Stage / scale**: private, hyper-growth. AI unit scaled **15 → 150 staff in 8
  months**; $0→$50M ARR in 4 months, $100M+ first-year, combined-company ~$300M target.
  Legacy Handshake is several hundred staff. → high data volume, fast-moving org, lots
  of new hires = elevated leak surface.

## 2. Team structure → personas (who leaks what)

| Team | ~Size | Sensitive data they handle |
| --- | --- | --- |
| Engineering / Platform (incl. ex-Cleanlab ML) | ~60 | AWS keys, DB connection strings, **frontier-lab API keys (OpenAI/Anthropic)**, GitHub PATs, JWTs; customer PII in logs |
| AI Training Operations / Program Mgmt | ~40 | **Confidential lab project data** — prompts, eval rubrics, model outputs (IP under NDA); task/project IDs |
| Expert Network / Community Ops | ~25 | Expert PII + **verified academic credentials**, onboarding docs, school emails |
| Payments / Finance Ops | ~12 | **Contractor payouts**: bank account + routing, **SSN/TIN (W-9/1099)**, $/hr rates |
| Trust & Safety / Data Quality | ~15 | Bulk student + expert PII, dedup/labeling datasets, content hashes |
| Sales & Partnerships (labs + employers) | ~20 | Lab **contracts/NDAs**, deal terms in CRM, employer billing |
| People / HR | ~8 | Employee SSNs, offer letters, direct-deposit (HR/corporate layer) |

Provenance threading: secrets leak from **Engineering**; confidential lab eval data from
**AI Training Ops**; SSN/TIN + bank payout data from **Payments**; student PII from
**Trust & Safety / platform exports**; employee SSNs from **HR**.

## 3. Integration / tooling surfaces → carriers (pick 5–7)
Modern SF tech stack. Most central, in scope:
1. **GitHub** — `.env`, source, CI logs → AWS/Stripe/**lab API keys**, DB creds, PATs.
2. **Slack** — export/transcript → ops pasting **confidential lab prompts/rubrics**,
   engineers pasting a token to debug, payout banking in a support thread.
3. **Google Drive (Sheets/CSV/Docs)** — **contractor payout roster** (bank/routing/
   SSN), expert onboarding, lab project briefs.
4. **Snowflake** — warehouse **unload/export CSV** of student/expert PII at scale.
5. **Annotation platform (their own product)** — **task JSON** with confidential lab
   eval content + PII embedded in expert free-text answers.
6. **Email (.eml)** — partnerships/NDA thread or contractor onboarding (W-9 request).
   *(Salesforce CRM optional if we want a 7th.)*

## 4. False-positive concerns → near-misses (precision / no-alert-fatigue story)
- **Internal user/expert/student IDs shaped like SSNs** (`NNN-NN-NNNN`) — a marketplace
  with 18M users is full of these; over-firing here = constant noise.
- **Placeholder/example API keys** in their **integration docs & SDK samples** handed to
  labs/experts (`sk-…EXAMPLE`, `YOUR_OPENAI_KEY`) — must be allowlisted.
- **UUIDs / git SHAs / content hashes** — project IDs, task IDs, dataset/model checkpoint
  hashes (very Cleanlab-flavored) that look like high-entropy secrets.
- **Employer invoice / order IDs shaped like PANs** (Luhn-failing) — billing artifacts.

## 5. False-negative concerns → evasion variants (recall / robustness story)
- **Frontier-lab API key split across lines / base64-wrapped** in a Slack debug paste or
  config blob — the key that, if missed, leaks a customer lab's account.
- **SSN/TIN with spaces instead of dashes** in contractor onboarding free text / email.
- **Confidential PII inside expert free-text answers** — e.g. a medical- or legal-domain
  RLHF task where the expert pastes a realistic record (identifier + fact split across
  sentences) into the annotation platform JSON — sensitive data in prose, not a labeled
  field.
- **Bank account + routing spelled out** in a payout support message rather than a form.

## 6. Demo narrative
Handshake AI's nightmare has two acts. **Act 1 — existential/IP**: a **frontier-lab API
key committed to a repo** and **confidential lab eval prompts pasted into Slack** —
either one breaches the NDA-bound trust their $100M AI business runs on. **Act 2 — PII at
scale**: the **contractor payout roster** (SSN/TIN + bank/routing for $100/hr experts)
and a **Snowflake export of student PII** sitting in shared Drive — FERPA + consumer-
privacy exposure across millions. Then we **earn credibility on precision**: their
platform is saturated with internal IDs, UUIDs, and content hashes shaped like
secrets/SSNs — a good detector stays quiet on those (allowlisted example keys, ID-shaped
non-PII) while still catching the **spaced SSN** and the **line-split lab key** a naive,
whitespace-fragile detector misses. Order to surface: lab-key-in-repo → confidential
eval data in Slack → contractor payout roster → Snowflake student-PII export → precision
sweep over the near-misses.
