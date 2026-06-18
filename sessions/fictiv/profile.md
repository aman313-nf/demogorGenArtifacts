# Company profile — Fictiv

Prospect for a Nightfall DLP/data-security demo. Synthetic data only; this profile
drives *what* we plant and *why each finding lands for Fictiv specifically*.

---

## 0. What's distinctive — the non-obvious risks (the demo's spine)

Fictiv is a **digital manufacturing marketplace** — the "AWS of manufacturing." Its
entire value prop is that product companies upload their **proprietary mechanical
designs (CAD, 2D drawings, specs)** and Fictiv routes them to a **vetted global
network of contract manufacturers** for quoting and production. That single data
flow — *customer crown-jewel IP transiting Fictiv and fanning out to third-party
shops across China, India, Japan, and Mexico, under NDA and U.S. export control* —
is what makes their risk profile unlike a generic SaaS company's.

1. **Customer design IP leaving to the wrong partner/region.** A sourcing/supply-
   chain manager forwards a customer's confidential drawing or describes an unreleased
   product to an offshore CNC shop. The IP is *prose and geometry*, not a regex-able
   token — and no off-the-shelf detector ships a "design IP" type. This is the
   crown-jewel leak and a deliberate **recall + coverage-gap** story.
   *(fact: platform ingests CAD under NDA → implication: IP routinely crosses an
   external supplier boundary → use case: the leak Fictiv's customers fear most.)*

2. **Export-controlled technical data (EAR/ITAR) crossing borders.** Fictiv's own
   Terms permit only **EAR99 / ECCN 9E991** parts; anything marked **ITAR/USML/CCL**
   is auto-deleted from their servers. So an **ECCN/ITAR marking in a document headed
   to a China-based partner** is an existential, regulator-facing exposure — uniquely
   theirs among DLP prospects.

3. **Manufacturing identifiers that mimic PII/PCI (the precision story).** Their world
   is full of **part numbers, drawing numbers, quote/PO IDs, lot codes, material
   grades** — many shaped exactly like credit cards (16 digits) or SSNs (NNN-NN-NNNN).
   Over-firing on these would bury their ops teams in false alerts. This is the
   alert-fatigue / precision angle, grounded in their actual work product.

4. **Platform secrets = 6,000 customers' IP at once.** The platform (Node/TS/GraphQL
   on AWS — RDS, SQS, Lambda) is the vault. A leaked AWS/RDS/Stripe key in a repo,
   `.env`, or Slack debug thread exposes the system holding *every* customer's designs.

5. **Global supplier payouts & cross-border workforce PII.** Paying 4,100+ partners
   means **foreign IBANs, US routing, India PAN/tax IDs**; a ~400-person workforce
   across **US / India / Mexico** means **SSNs alongside international IDs**.

These five are the lead talking points; the layers below are supporting cast.

## 1. What they do
- **Industry / sub-vertical:** digital/on-demand manufacturing & supply-chain SaaS
  (manufacturing-as-a-service marketplace). Sells CNC machining, injection molding,
  3D printing, sheet metal, die/urethane/compression casting via an instant-quote,
  CAD-upload platform + a managed global partner network.
- **Customers:** 6,000+ product companies incl. ~61% of the Fortune 500 — aerospace,
  medical devices, automotive, robotics, climate tech, semiconductor, eVTOL/EV
  (publicly: Medtronic, J&J, RBC Bearings, plus many stealth hardware startups).
- **Regulatory / contractual regime:** **EAR / ITAR export control** (the defining
  one); **customer NDAs / trade-secret confidentiality** (the trust the business
  rides on); ISO 9001:2015 quality; SOC 2 expectations; PCI-DSS (takes card payment);
  GDPR/CCPA + India/Mexico data laws (global workforce & partners).
- **Stage / scale:** private, ~400 employees, $190M+ raised; **acquired by MISUMI
  Group (Japan), Apr 2025**. Manufacturing centers in US, China, India, Mexico (+Japan
  supply region). 42M+ parts delivered.

## 2. Team structure → personas / who-leaks-what

| Team | ~Size | Sensitive data they handle |
| --- | --- | --- |
| **Supply Chain / Sourcing Ops** *(defining persona)* | ~70 | **Customer CAD/drawings & specs, RFQs, export-control status — shared with offshore partners** |
| Manufacturing / Mechanical Engineers (DFM) | ~40 | Customer part geometry, tolerances, proprietary designs in review notes |
| Software Engineering (platform) | ~50 | AWS/RDS/Stripe keys, DB conn strings, customer PII in logs |
| Finance / Accounts Payable | ~12 | Supplier bank accounts, IBANs, India/Mexico tax IDs, customer card data |
| Customer/Account Management | ~30 | Customer contacts, order/quote data, pre-launch program details |
| People / HR | ~8 | SSNs, payroll, offer letters, global employee IDs |

**Defining persona:** the **Supply Chain / Sourcing Manager**, who lives at the seam
between customer IP and the external manufacturing network. They are the protagonist
of the lead carriers (the RFQ handoff to a Shenzhen partner, the pre-launch program
Slack channel) — that seam is precisely the leak Fictiv worries about most.

## 3. Integration / tooling surfaces → carriers
Confirmed/likely stack: **Node.js, TypeScript, GraphQL, AWS (RDS, SQS, Lambda, EC2)**;
GitHub; Google Workspace (Gmail/Drive); Slack; Snowflake-style warehouse; Stripe for
payments; their **own platform** (quote/order DB). In scope (6–7 central surfaces):
- **Email (Gmail)** — RFQ/drawing handoff to an offshore partner *(lead)*.
- **GitHub** — platform `.env` / config with live keys.
- **Google Drive / warehouse export** — supplier payout sheet; HR employee master.
- **Slack** — eng on-call secret paste; supply-chain pre-launch program channel.
- **Product / billing** — order export CSV with card data.

## 4. False-positive concerns → near-misses (lead with work-product ones)
- **Part / drawing / quote numbers shaped like PANs or SSNs** *(most resonant — their
  work product)*: a 16-digit part number that fails Luhn; a `NNN-NN-NNNN` drawing
  revision code. A good detector must *not* alert on these or ops drowns in noise.
- **Placeholder / example API keys** in sample config and docs (`AKIA…EXAMPLE`,
  `sk_test_…`) — should be allowlisted.
- **Git SHAs / UUIDs** in CI and Slack — high-entropy but not secrets.

## 5. False-negative concerns → evasion variants
- **Customer design IP in free-text prose** (RFQ emails, Slack program threads) — no
  token to regex; only context catches it. *(the crown-jewel recall test.)*
- **Export-control markings in body text** rather than a structured field.
- **Bank/PAN/SSN digits spaced or dashed** in emails from international partners or
  reimbursement notes (whitespace-fragile detectors miss them).
- **Secrets base64-wrapped or line-split** in runbooks / pasted config.

## 6. Demo narrative
Open on the nightmare: a Supply Chain Manager emails a **Shenzhen partner** a
customer's confidential drawing — proprietary design described in prose, an **ITAR/ECCN
export marking** in the body, customer contact PII attached. That one message is a
trade-secret leak *and* a potential export-control violation — the two things that
could end a customer relationship or draw a regulator. Then show the platform `.env`
(a leaked AWS/Stripe key = every customer's IP exposed), the global supplier payout
sheet (IBANs, India PAN), and HR (SSNs). Finally, turn to **precision**: the part and
drawing numbers shaped like cards and SSNs that Nightfall *correctly stays quiet* on —
proving the tool understands their data instead of just pattern-matching digits. The
spine: *protect the customer IP and export-controlled data that Fictiv's entire
business — and now MISUMI's — depends on, without burying ops in false alarms.*
