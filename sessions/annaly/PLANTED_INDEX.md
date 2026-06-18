# Planted index — Annaly Capital Management demo data

**Session `annaly-capital-management-a49384`** · 22 planted items across 8 carriers · synthetic, format-valid.

## The demo story

Annaly is a ~190-person mortgage REIT that nonetheless custodies consumer borrower PII at scale (Onslow Bay whole loans + MSR servicing ~608k loans). DLP value = catch the borrower PII (loan tapes), MNPI (positions/hedging/earnings), and counterparty wire instructions — while staying quiet on the CUSIPs/pool numbers/trade IDs their trading work is saturated with. Open on a loan tape, show the CUSIP precision inversion, then MNPI and wires.

**Coverage** — category: PII 10, financial 6, secret 5, confidential 1 · challenge: 🎯 13, 🟡 5, 🫥 4.

Legend: 🎯 straightforward · 🟡 benign near-miss (should NOT alert) · 🫥 evasive true positive.

---

## `loan_tape_onslowbay.csv`  ·  _Email_  ·  4 item(s)

- 🎯 **PII/ssn** @ ssn col — `655-15-0410`  
  _Priya Menon (Onslow Bay / Residential Credit Ops)_ — Borrower SSN in a 30-row whole-loan diligence tape emailed to a counterparty — bulk GLBA NPI from Onslow Bay acquisition; the crown-jewel leak
- 🫥 **PII/ssn** @ ssn col r2 — `2265 8965 5`  
  _Priya Menon (Onslow Bay / Residential Credit Ops)_ — A borrower SSN entered with spaces instead of dashes in the loan tape — recall test on whitespace-fragile SSN regex
- 🎯 **PII/address** @ property_address col — `9873 Maple Ave, Tampa FL 33602`  
  _Priya Menon (Onslow Bay / Residential Credit Ops)_ — Borrower property address — PII tied to the loan, identity-theft relevant
- 🎯 **PII/loan_number** @ loan_number col — `LN-4332181960`  
  _Priya Menon (Onslow Bay / Residential Credit Ops)_ — Loan number — internal identifier with no Nightfall detector (expect 'not integrated')

## `msr_servicing_extract.csv`  ·  _Snowflake_  ·  2 item(s)

- 🎯 **PII/ssn** @ ssn col — `553-07-5734`  
  _Marcus Feld (MSR / Servicing Oversight)_ — Borrower SSN in the MSR servicing extract (~608k loans, subserviced by Rocket Mortgage) — consumer NPI at scale in the data warehouse
- 🎯 **PII/full_name** @ borrower_name col — `Camila Nguyen`  
  _Marcus Feld (MSR / Servicing Oversight)_ — Borrower name in servicing data — PII; in combination with loan/UPB it's a servicing-record leak

## `portfolio_positions.csv`  ·  _Google Drive_  ·  3 item(s)

- 🟡 **financial/cusip** @ cusip col — `214658RA6`  
  _Daniel Okafor (Agency MBS / Portfolio)_ — A CUSIP — public security identifier, NOT sensitive. The CUSIP detector WILL fire; for a trading shop that's pure alert fatigue. The precision story: don't flag our everyday securities data.
- 🟡 **financial/cusip** @ cusip col r2 — `449972280`  
  _Daniel Okafor (Agency MBS / Portfolio)_ — Another CUSIP in the positions file — over-firing on these buries the real findings
- 🟡 **PII/internal_id_like_ssn** @ deal_id col — `EMP-609-84-3344`  
  _Daniel Okafor (Agency MBS / Portfolio)_ — A deal/pool ID shaped like an SSN (NNN-NN-NNNN) — looks like PII but isn't; a good detector stays quiet

## `hedging_strategy_memo.eml`  ·  _Email_  ·  1 item(s)

- 🫥 **confidential/mnpi** @ body — `Ahead of Q3 earnings we are rotating ~$3.2`  
  _Helen Cho (Finance / SEC Reporting)_ — Material non-public information (positions, hedge ratio, pre-release book value) in prose — Reg FD / insider-trading risk, and no regex PII for a detector to anchor on (expect 'not integrated')

## `treasury_wire_instructions.csv`  ·  _Email_  ·  3 item(s)

- 🎯 **financial/us_routing** @ aba_routing col — `210470954`  
  _Sofia Reyes (Treasury / Repo Ops)_ — ABA routing for a repo settlement wire — funds-movement risk; large-dollar counterparty settlement detail
- 🎯 **financial/iban** @ iban col — `DE70CJKX62328588424745`  
  _Sofia Reyes (Treasury / Repo Ops)_ — Counterparty IBAN for an international settlement leg
- 🫥 **financial/bank_account** @ bank_account col — `7123-6851`  
  _Sofia Reyes (Treasury / Repo Ops)_ — Bank account dash-grouped in the sheet — recall test on financial formats; (US bank account has no dedicated detector → may show 'not integrated')

## `risk-analytics.env`  ·  _GitHub_  ·  4 item(s)

- 🎯 **secret/db_connection_string** @ LOAN_WAREHOUSE_DB_URL — `postgres://svc_jdl9jj:vQhAw3Q8WB36Ud9s@db-`  
  _Raj Patel (Risk Analytics Eng)_ — Connection string to the loan/positions warehouse — one cred = access to borrower PII + positions at scale
- 🎯 **secret/google_api_key** @ MARKET_DATA_API_KEY — `AIzaBC4oAv0DzAUguBuQqx9jR7Eef1ffBgVVxZi`  
  _Raj Patel (Risk Analytics Eng)_ — Market-data vendor API key committed to config
- 🎯 **secret/aws_secret_key** @ AWS_SECRET_ACCESS_KEY — `Bt9CnSVoJC2dIdxINRSaxsZisdlBW16RuVNPkgtu`  
  _Raj Patel (Risk Analytics Eng)_ — Cloud master credential in source
- 🟡 **secret/placeholder_key** @ EXAMPLE_KEY — `xoxb-000000000000-000000000000-XXXXXXXXXXX`  
  _Raj Patel (Risk Analytics Eng)_ — Well-known placeholder key — a good detector allowlists it (no alert fatigue)

## `servicing_ops_slack.txt`  ·  _Slack_  ·  3 item(s)

- 🫥 **PII/ssn** @ MSR message — `0518 7133 7`  
  _Marcus Feld (MSR / Servicing Oversight)_ — Borrower SSN pasted (spaced) into Slack to resolve a servicing escalation — PII in chat, third surface beyond the tape/warehouse
- 🟡 **financial/cusip** @ Portfolio message — `7558863U0`  
  _Daniel Okafor (Agency MBS / Portfolio)_ — A CUSIP referenced in ops chatter — detector fires, but it's a public identifier (noise)
- 🎯 **secret/github_pat** @ Eng message — `ghp_rCQBFMCArnWGhwBhsRRLFHQtcozMdant8nXi`  
  _Raj Patel (Risk Analytics Eng)_ — GitHub PAT pasted in Slack to debug — credential leaves the repo into chat history

## `employee_master.csv`  ·  _Google Drive_  ·  2 item(s)

- 🎯 **PII/ssn** @ ssn col — `336-16-0127`  
  _Tom Bauer (People/HR)_ — Employee SSNs in the HR master — the universal, always-over-shared dataset
- 🎯 **PII/drivers_license** @ drivers_license col — `X0607159`  
  _Tom Bauer (People/HR)_ — Employee driver's license numbers — identity-theft-grade PII
