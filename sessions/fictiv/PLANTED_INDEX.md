# Fictiv — planted demo data: briefing

**Synthetic data only.** Every value below is fabricated but format-valid (Luhn-valid cards, ABA-valid routing, mod-97 IBAN, correctly-prefixed keys) so a real detector fires — none maps to a real person, account, or live credential.

## The story

Fictiv is the *AWS of manufacturing*: 6,000+ product companies upload proprietary CAD and drawings under NDA, and Fictiv routes them to a global network of contract manufacturers across China, India, Japan, and Mexico — under U.S. export control (EAR/ITAR). Open on the nightmare: a **Supply Chain Manager emails a Shenzhen partner** a customer's confidential drawing — the unreleased design described in prose, an **ITAR/ECCN export marking** in the body, the customer's contact PII attached. That one message is a **trade-secret leak _and_ a potential export-control violation**. Then walk the platform `.env` (a leaked Stripe/GitHub/AWS key exposes the system holding *every* customer's IP), the supplier payout sheet (GB IBAN, India PAN, US routing), and HR (SSNs). Close on **precision**: the part, drawing, and quote numbers shaped like credit cards and SSNs that Nightfall *correctly stays quiet* on — proving it understands Fictiv's data instead of pattern-matching digits.

**32 planted values** across **7 carriers** — 17 straightforward · 6 FP near-misses (precision) · 9 FN-evasive (recall). Scan report card: see `detector_results.json` / the app's Detector-results tab (100% precision on near-misses; recall gaps are the design-IP/export-marking coverage gap + deliberate evasions).

---

## RFQ + drawing handoff to an offshore partner — Email (LEAD)

`carriers/rfq_supplier_handoff.eml`

- **design_ip** — 🔴 FN-evasive · *IP* · body — design context  
  `monolithic Ti-6Al-4V rotor-hub redesign tha…`  
  _Priya Nair (Supply Chain Ops)_ — A customer's unannounced product architecture, described in free-text prose and sent to a China-based partner — the crown-jewel trade-secret leak Fictiv's whole NDA-based business exists to prevent. No regex hook; only context catches it.
- **export_control_marking** — 🔴 FN-evasive · *IP* · body — export status  
  `ECCN 9E991; some features may fall under IT…`  
  _Priya Nair (Supply Chain Ops)_ — An ECCN/ITAR export-control marking in body text on a file headed offshore. Fictiv only permits EAR99/9E991 and auto-deletes ITAR drawings — this is the regulator-facing violation, and it's in prose, not a labeled field.
- **order_id_like_pan** — 🟡 FP near-miss · *PCI* · drawing number  
  `3218196001338908`  
  _Priya Nair (Supply Chain Ops)_ — A 16-digit drawing number that looks like a credit card but fails Luhn. Manufacturing is full of these — a good detector must stay quiet or bury ops in noise.
- **email** — ✅ straightforward · *PII* · customer contact email  
  `daniel.brooks@halcyonaero.com`  
  _Priya Nair (Supply Chain Ops)_ — Customer engineer's contact PII shared outside the account — minor next to the IP, but it's the linkage that ties the leaked design to a named program.
- **phone** — ✅ straightforward · *PII* · customer contact phone  
  `(960) 481-5012`  
  _Priya Nair (Supply Chain Ops)_ — Direct line for the customer's mechanical lead, exposed to a third-party shop.

## Pre-launch program discussion — Slack (#sourcing-aerospace)

`carriers/program_slack.txt`

- **design_ip** — 🔴 FN-evasive · *IP* · Priya 2:18 message  
  `Halcyon's Gen-3 'Project Stratus' eVTOL — t…`  
  _Priya Nair (Supply Chain Ops)_ — An unreleased customer product — codename, materials, mass targets, reveal date — discussed in a Slack channel. Pure free-text trade secret + competitive intel; the second context for design-IP recall, in chat rather than email.
- **order_id_like_pan** — 🟡 FP near-miss · *PCI* · Priya 2:22 message  
  `1693406088356159`  
  _Priya Nair (Supply Chain Ops)_ — A 16-digit quote number that looks like a PAN but fails Luhn — the same precision story as part/drawing numbers, now in a chat surface.

## Platform production config — GitHub

`carriers/platform-api.env`

- **aws_access_key** — ✅ straightforward · *secret* · AWS_ACCESS_KEY_ID  
  `AKIAM80O2RAK1VRJNVGF`  
  _Wei Chen (Platform Eng)_ — AWS key in a committed .env — direct access to the infra holding every customer's CAD and order data. Note for the demo: the API-Key detector live-validates against providers, so it abstains on this inactive synthetic key while it DID catch the GitHub, Stripe, and DB credentials beside it — a key-validation tuning point, and proof it isn't just regexing prefixes.
- **db_connection_string** — ✅ straightforward · *secret* · DATABASE_URL  
  `postgres://svc_0czuzr:en68K4TunPFz46PD@db-j…`  
  _Wei Chen (Platform Eng)_ — Production Aurora/Postgres connection string — the quote/order database that stores customer designs and PII.
- **stripe_live_key** — ✅ straightforward · *secret* · STRIPE_SECRET_KEY  
  `sk_live_VJIqVLB5LzxoiGFfWd3hjOkY`  
  _Wei Chen (Platform Eng)_ — Live Stripe key = direct payment-fraud and PCI exposure.
- **github_pat** — ✅ straightforward · *secret* · GITHUB_DEPLOY_TOKEN  
  `ghp_RBMeyyMDHqJ38aRUhR4IWrXPvhsBkDa9U4Uq`  
  _Wei Chen (Platform Eng)_ — A GitHub deploy token with access to private CAD-processing repos — leaks the source that handles every customer's geometry.
- **placeholder_key** — 🟡 FP near-miss · *secret* · STRIPE_TEST_KEY  
  `xoxb-000000000000-000000000000-XXXXXXXXXXXX…`  
  _Wei Chen (Platform Eng)_ — A well-known Stripe example/test key. A precise detector allowlists it — firing here is exactly the alert fatigue that erodes trust in the tool.

## On-call incident thread — Slack (#incident-quote-api)

`carriers/eng_oncall_slack.txt`

- **github_pat** — ✅ straightforward · *secret* · Diego 9:43 message  
  `ghp_jmsn9dLVIdVuddLEG62Hkd9Gf2leMeR3pzh8`  
  _Diego Santos (Platform Eng / on-call)_ — An engineer pastes a live GitHub deploy token into Slack to force a rollback — the single most common way infra secrets escape, and Slack history keeps it forever.
- **db_connection_string** — ✅ straightforward · *secret* · Wei 9:45 message  
  `postgres://svc_4kplmc:NfAQLKHu7qnQTupq@db-z…`  
  _Wei Chen (Platform Eng)_ — Production DB connection string shared in chat — read access to the order/IP store.
- **aws_access_key** — 🔴 FN-evasive · *secret* · Wei 9:52 message (runbook)  
  `QUtJQVQzVUVBM0dFOE42UUlXRVA=`  
  _Wei Chen (Platform Eng)_ — A service-account key base64-wrapped in a runbook snippet — still a live secret, but the encoding hides it from naive scanners. Tests recall on obfuscation.
- **git_sha** — 🟡 FP near-miss · *secret* · Diego 10:04 message  
  `b95e909348334896a68f812d810a485ed03241b4`  
  _Diego Santos (Platform Eng / on-call)_ — A 40-hex git commit SHA — high-entropy and key-shaped, but not a secret. Over-flagging these in eng channels is pure alert fatigue.

## Global supplier payouts — Google Drive / warehouse export

`carriers/supplier_payouts_2026Q2.csv`

- **iban** — ✅ straightforward · *financial* · iban column (Nordmann)  
  `GB42YFQD48932528809570`  
  _Omar Haddad (Accounts Payable)_ — Foreign supplier IBAN in a payout sheet on a shared drive — the cross-border banking sprawl that comes with paying 4,100+ partners.
- **us_routing** — ✅ straightforward · *financial* · routing_swift column (Pinnacle)  
  `248963831`  
  _Omar Haddad (Accounts Payable)_ — US bank routing number for a domestic supplier payout.
- **bank_account** — ✅ straightforward · *financial* · bank_account column (Shenzhen Yuhang)  
  `6578713315`  
  _Omar Haddad (Accounts Payable)_ — Raw supplier bank-account number — sensitive, but no off-the-shelf detector covers a bare account number (an honest coverage gap to discuss).
- **india_pan** — ✅ straightforward · *PII* · tax_id column (Anand Precision)  
  `ASRPH9301W`  
  _Omar Haddad (Accounts Payable)_ — India PAN for an India-based partner — shows Nightfall's international coverage, which matters for a company with a full India manufacturing center.
- **us_routing** — 🔴 FN-evasive · *financial* · notes column (Saltillo)  
  `031 051 837`  
  _Omar Haddad (Accounts Payable)_ — A routing number typed with spaces in a free-text note — whitespace-fragile detectors miss it. Tests recall on loosely-formatted financial data.

## HR employee master — Google Drive

`carriers/employee_master.csv`

- **ssn** — ✅ straightforward · *PII* · ssn column (row 1)  
  `144-55-3007`  
  _Hannah Larsson (People / HR)_ — Employee SSN in an HR master sheet on a shared drive — the universal HR exposure.
- **dob** — 🔴 FN-evasive · *PII* · dob column (row 1)  
  `05/15/1965`  
  _Hannah Larsson (People / HR)_ — A date of birth sitting in a bare, unlabeled spreadsheet column — no 'DOB:' cue for a context-aware detector to latch onto. The recall blind spot of structured exports: the data is sensitive, but the column gives the detector nothing to grab.
- **full_name** — ✅ straightforward · *PII* · full_name column (row 1)  
  `Priya Santos`  
  _Hannah Larsson (People / HR)_ — Employee name; on its own low-risk, but the join key for the rest of the row.
- **street_address** — 🔴 FN-evasive · *PII* · home_address column (row 1)  
  `1490 O'Farrell St, San Francisco, CA 94115`  
  _Hannah Larsson (People / HR)_ — A home address isolated in a spreadsheet cell, with no label around it — like the DOB, a context-aware detector under-fires on it here even though it lights up the same address in an email body. Format-distinctive types (SSN, name) detect in cells; addresses and dates need context. The structured-export recall blind spot.
- **internal_id_like_ssn** — 🟡 FP near-miss · *PII* · employee_id column  
  `EMP-927-80-2604`  
  _Hannah Larsson (People / HR)_ — An internal employee ID formatted NNN-NN-NNNN — looks like an SSN but isn't. A good detector stays quiet; a naive one cries SSN on every row.
- **ssn** — 🔴 FN-evasive · *PII* · ssn column (row 2)  
  `052 848 857`  
  _Hannah Larsson (People / HR)_ — An SSN entered with spaces instead of dashes — a classic whitespace evasion that trips up brittle detectors. Tests recall.

## Order export with payment data — Product / billing

`carriers/order_export.csv`

- **credit_card_visa** — ✅ straightforward · *PCI* · card_number column (ORD-100482)  
  `4620450533158696`  
  _Omar Haddad (Accounts Payable)_ — A full customer PAN in an order-export CSV outside the cardholder data environment = a PCI-DSS scope violation.
- **order_id_like_pan** — 🟡 FP near-miss · *PCI* · part_number column (ORD-100482)  
  `0733754330365414`  
  _Marcus Reyes (Manufacturing Eng)_ — A 16-digit part number that looks card-shaped but fails Luhn. The precision win: Nightfall stays quiet while a regex-only tool screams PCI on every order row.
- **credit_card_visa** — 🔴 FN-evasive · *PCI* · billing_note column (ORD-100483)  
  `4232 2602 5634 2165`  
  _Omar Haddad (Accounts Payable)_ — A card number captured over the phone and typed with spaces into a free-text note — the messy reality of how PANs actually leak. Tests recall on spaced digits.
- **cvv** — ✅ straightforward · *PCI* · cvv column (ORD-100482)  
  `359`  
  _Omar Haddad (Accounts Payable)_ — A stored CVV — never permitted under PCI. No standalone detector maps to a bare 3-digit CVV (a coverage gap worth naming), but storing it at all is the violation.
- **email** — ✅ straightforward · *PII* · billing_email column (ORD-100482)  
  `procurement@halcyonaero.com`  
  _Omar Haddad (Accounts Payable)_ — Customer procurement contact in a billing export.
