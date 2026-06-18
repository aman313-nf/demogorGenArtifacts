# Company profile — Annaly Capital Management (NLY)

> DLP/data-security demo profile. Researched June 2026.

## 0. What's distinctive — the non-obvious risks (the spine of this demo)
Annaly is a **mortgage REIT** — a "financial markets" firm — yet it custodies
**consumer borrower PII at real scale**, which inverts the usual assumption for a
markets shop. Two distinctive traits:
1. **Tiny workforce, huge consumer-data footprint.** ~190 employees, but via
   **Onslow Bay** (whole-loan acquisition) and a **fully-scaled MSR platform
   servicing ~608,000 loans / $192B UPB** (Rocket as subservicer), they hold
   loan-level **borrower SSNs, addresses, DOBs, loan numbers** — GLBA NPI at
   consumer scale handled by a markets org without a big consumer-ops/security team.
2. **Everyday work product looks sensitive but isn't.** They trade agency MBS all
   day — their files are saturated with **CUSIPs, pool numbers, trade IDs** (public
   securities identifiers). A detector that flags those (there's a CUSIP detector)
   buries them in noise. The precision story is "don't alert on our securities data."

So the real risks are: borrower loan-level PII (loan tapes / servicing files), MNPI
(public-company positions/hedging/earnings), and counterparty wire instructions —
while the precision win is staying quiet on CUSIPs/pool numbers.

## 1. What they do
- Internally-managed **mortgage REIT** (NYSE: NLY) investing across four segments:
  **Agency MBS**, **Residential Credit** (Onslow Bay — Non-QM whole loans &
  securitizations), **MSR** (~608k serviced loans), and Corporate. Spread investing
  funded largely by **repo**, with heavy hedging/liquidity management.
- **Regulatory regime:** **GLBA** (borrower NPI from whole loans + servicing),
  **SEC / Reg FD + insider trading** (public co → MNPI), **SOX**, state privacy
  (CCPA-type). Plus the HR/corporate layer.
- **Stage/scale:** large balance sheet (~$80B+), **~190 employees** — a high
  value-per-person, sophisticated org; small security/ops surface relative to the
  sensitivity of the data it touches.

## 2. Team structure → personas (who leaks what)
| Team | ~Size | Sensitive data they handle |
| --- | --- | --- |
| Agency MBS / Portfolio (trading) | ~30 | **MNPI** (positions/hedging), CUSIPs/pool#, market-data keys |
| Onslow Bay / Residential Credit Ops | ~25 | **whole-loan tapes** — borrower SSN/DOB/address/loan# |
| MSR / Servicing Oversight | ~20 | **608k-loan servicing data**, subservicer (Rocket) exchange |
| Treasury / Repo Ops | ~15 | **counterparty wire instructions** — bank acct/ABA/IBAN/SWIFT |
| Finance / SEC Reporting | ~20 | pre-release earnings, **MNPI**, SOX |
| Risk Analytics Eng | ~15 | DB connection strings, market-data vendor API keys, AWS |
| People / HR | ~10 | employee SSNs, payroll, direct deposit |

**Defining personas:** the **portfolio/trading** desk (MNPI + CUSIPs) and the
**Onslow Bay / MSR** ops teams (borrower PII at scale) — the protagonists, not a
generic support/HR org.

## 3. Integration / tooling surfaces → carriers
Email (.eml — loan tapes, wire instructions, subservicer exchange), Google Drive
(loan tapes, board decks, positions sheets), Snowflake (loan-level / servicing
warehouse), GitHub/config (analytics & risk system secrets, market-data keys),
Slack (ops chatter — a borrower SSN to resolve a servicing issue; a key pasted to
debug). Pick 6–7.

## 4. False-positive concerns → near-misses (the precision story)
**Work-product near-misses dominate.** Annaly's files are full of identifiers that
*look* sensitive but are public/benign:
- **CUSIPs** (9-char security identifiers — there's a CUSIP detector; firing on
  them = pure noise), **pool numbers**, **trade/deal IDs**.
- **loan numbers shaped like SSNs** (`NNN-NN-NNNN`-ish) in tapes — must not alert.
- placeholder/test API keys in analytics config.
Lead with the CUSIP inversion — staying quiet on everyday securities data is the
credible "no alert fatigue" story for a trading shop.

## 5. False-negative concerns → evasion variants (recall story)
- Borrower **SSN spaced/dashed oddly** in a loan tape or pasted into Slack to
  resolve a servicing issue.
- **Wire account/routing spelled out** in a treasury email rather than a labeled field.
- **MNPI in prose** — positions/hedging described in an email or memo, no labeled
  field for a detector to anchor on.

## 6. Demo narrative
Open on the **loan tape** — bulk borrower SSN/address from Onslow Bay/MSR, the
GLBA nightmare a markets firm doesn't expect to be holding — then the **precision
inversion**: a positions/trade file full of CUSIPs the tool must *not* alert on,
beside a real borrower SSN it catches. Then **MNPI** (a hedging/earnings memo that
no regex catches — the content-detection gap) and **counterparty wire
instructions**. Close with the **infra secrets** + HR layer. Through-line: for a
small markets firm custodying 600k borrowers' data, DLP value = **catch the
borrower PII + MNPI, stay silent on the CUSIPs**.
