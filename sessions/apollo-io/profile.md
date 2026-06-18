# Company profile — Apollo.io

> DLP/data-security demo profile. Researched June 2026.

## 0. What's distinctive — the non-obvious risks (the spine of this demo)
Apollo.io's defining trait flips the usual DLP assumption: **their product *is* bulk
personal PII at scale** (275M+ B2B contacts — names, work emails, phones, titles,
companies). For most companies an email/phone is *the sensitive thing to catch*; at
Apollo that data is the deliverable and flows everywhere by design (exports, API,
CRM sync, sequences, dialer). So the real risks are:
1. **Bulk contact-DB exfil** — a rep or integration dumping a large contact list to
   a CSV / personal drive. This is literally their 2018 breach (125.9M emails / 200M
   records stolen from the prospect DB). The signal is *volume + destination*, not
   the presence of one email.
2. **The precision inversion** — work emails/phones/names are everywhere by design;
   a DLP that flags each one is unusable (catastrophic alert fatigue). The credible
   story is *distinguishing legitimate product data from a genuine leak.*
3. **Ingested customer-CRM custody** — Apollo pulls customers' Salesforce/HubSpot
   data for enrichment/sync; that third-party PII under Apollo's care leaking breaks
   customer trust.
4. **Contact-DB / infra secrets** — DB creds, enrichment/scraper keys, platform API
   keys; one leaked key = access to the 275M-contact database itself.

## 1. What they do
- AI-native B2B **sales-intelligence + engagement** platform (contact database +
  sequences + dialer + meeting intelligence + pipeline). Founded 2015, ~1,604
  employees, ~16,000 customer teams. Core asset: 230–275M+ contacts / 73M accounts,
  65+ data points each, ~97% email accuracy.
- **Regulatory regime**: GDPR & CCPA are front-and-center — Apollo operates as both
  Data Processor and Controller; CCPA opt-out of sale/sharing; faced GDPR scrutiny
  after the 2018 breach. SOC 2 for selling to enterprises. Plus the HR/corporate layer.
- **Stage / scale**: private, growth-stage, ~1,600 staff → real HR data + high data
  volume + heavy dogfooding of their own product.

## 2. Team structure → personas (who leaks what)
| Team | ~Size | Sensitive data they handle |
| --- | --- | --- |
| Data Platform / Enrichment Eng | ~120 | contact-DB connection strings, scraper/API keys, the 275M DB itself |
| Platform / Backend Eng | ~150 | AWS keys, service creds, customer PII in logs |
| **SDRs / AEs (dogfood Apollo)** | ~300 | **bulk prospect exports, sequences full of contact PII, dialer logs** |
| Customer Success / Onboarding | ~80 | **ingested customer CRM data** (Salesforce/HubSpot) |
| RevOps / Data | ~40 | contact exports, enrichment tables |
| People / HR | ~25 | employee SSNs, payroll, direct deposit |

**Defining persona = the SDR/AE who lives in the product** — they're the protagonist
of the bulk-export and sequence carriers, not generic engineers.

## 3. Integration / tooling surfaces → carriers
GitHub (`.env`/config — DB + scraper creds), CI logs, Google Drive (bulk exports,
HR sheets), **the Apollo product itself** (in-app results / sequence data = the
business-contact data), Salesforce/HubSpot (ingested customer CRM), Slack (reps
sharing contacts / debugging). 6–7 carriers across these.

## 4. False-positive concerns → near-misses (the precision story)
**Work-product near-misses dominate here.** Ordinary business-contact data — work
emails, work phones, names, titles in their normal in-product/app context — must
**not** alert; that's the entire product and over-flagging it is unusable. The art
is firing on the *bulk dump to the wrong place* and on genuinely sensitive items
(a prospect's personal mobile, a leaked DB) while staying silent on routine
business-contact data. Generic near-misses too: internal record IDs, UUID
list/sequence ids, placeholder API keys.

## 5. False-negative concerns → evasion variants (recall story)
- Contact PII exported in odd shapes (phone spaced/dashed; a personal mobile slipped
  into a Slack message as prose).
- DB creds / API keys base64-wrapped or line-split in a runbook/CI log.
- A genuinely sensitive personal record buried inside a large file of routine
  business contacts (needle-in-product-data).

## 6. Demo narrative
Open on the **bulk contact export** — a 30-row prospect dump to a personal Drive,
i.e. their 2018 breach in miniature — then the **infra secret** that would hand over
the whole 275M DB. Then the **precision inversion**: show routine business-contact
data the tool correctly stays quiet on, next to a genuine personal-mobile leak it
catches — the "we won't drown you in alerts on your own product" story. Round out
with **ingested customer-CRM custody** and the **HR layer**. The through-line: for a
company whose product is PII, DLP value = *bulk-exfil + precision*, not "flag every
email."
