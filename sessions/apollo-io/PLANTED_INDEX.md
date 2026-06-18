# Planted index — Apollo.io demo data

**Session `apollo-io-846eef`** · 26 planted items across 7 carriers · synthetic, format-valid.

## The demo story

For a company whose product IS a 275M-contact PII database, DLP value isn't 'flag every email' — it's bulk-exfil detection + precision. Open on a bulk contact-DB export to a personal Drive (their 2018 breach in miniature), then the infra secret that would hand over the whole database; then the precision inversion (stay quiet on routine business-contact product data, catch a genuine personal-mobile leak); round out with ingested customer-CRM custody and the HR layer.

**Coverage** — category: PII 16, secret 9, financial 1 · challenge: 🎯 17, 🟡 6, 🫥 3.

Legend: 🎯 straightforward · 🟡 benign near-miss (should NOT alert) · 🫥 evasive true positive.

---

## `enrichment-platform.env`  ·  _GitHub_  ·  4 item(s)

- 🎯 **secret/db_connection_string** @ CONTACT_DB_URL — `postgres://svc_ohbvrp:oiVgRV5IfLBcbfno@db-`  
  _Priya Nair (Data Platform Eng)_ — Connection string to the 275M-contact database — one leaked cred = the whole product DB (their 2018 nightmare)
- 🎯 **secret/aws_secret_key** @ AWS_SECRET_ACCESS_KEY — `WmTSHf6pWkLUyifDLkDmWJ6UuVTAIjvFu7WICPhD`  
  _Priya Nair (Data Platform Eng)_ — Scraper/S3 master credential committed to source — infra + bulk-data compromise
- 🎯 **secret/google_api_key** @ MAPS_GEOCODE_KEY — `AIza0cZuzren68K4TunPFz46PDjqipVJIqVLB5L`  
  _Priya Nair (Data Platform Eng)_ — Google API key in source — billing abuse
- 🟡 **secret/placeholder_key** @ EXAMPLE_KEY — `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`  
  _Priya Nair (Data Platform Eng)_ — Well-known placeholder key — a good detector allowlists it (no alert fatigue)

## `ci-build.log`  ·  _CI_  ·  3 item(s)

- 🎯 **secret/aws_secret_key** @ export line — `UCr_lgotu2iXW7GboIRoL3u6aHwnMztVuaP-coUN`  
  _Priya Nair (Data Platform Eng)_ — Secret echoed into a CI log — logs are broadly readable and long-retained
- 🫥 **secret/db_connection_string** @ heredoc — `postgres://svc_pdp4k8:ffUF0eWIXi\niQE8Jk@d`  
  _Priya Nair (Data Platform Eng)_ — Contact-DB URL split across lines in a log — line-anchored regexes miss it
- 🟡 **secret/git_sha** @ build id — `d669cbee3772a077021721a278f64f7fd633dbdd`  
  _Priya Nair (Data Platform Eng)_ — Build commit SHA — not a secret

## `contact_export_q1.csv`  ·  _Google Drive_  ·  6 item(s)

- 🎯 **PII/email** @ work_email col — `rromano@northwind.io`  
  _Diego Santos (SDR (dogfoods Apollo))_ — One of 30 prospect rows in a bulk export sitting on a personal Drive — THE 2018-breach scenario; the signal is bulk volume + destination, not any single email
- 🎯 **PII/phone** @ phone col — `(890) 869-2612`  
  _Diego Santos (SDR (dogfoods Apollo))_ — Prospect phone in a bulk contact dump — bulk PII egress is the crown-jewel exfil risk
- 🎯 **PII/email** @ work_email col — `madeyemi@northwind.io`  
  _Diego Santos (SDR (dogfoods Apollo))_ — One of 30 prospect rows in a bulk export sitting on a personal Drive — THE 2018-breach scenario; the signal is bulk volume + destination, not any single email
- 🎯 **PII/phone** @ phone col — `(312) 454-4139`  
  _Diego Santos (SDR (dogfoods Apollo))_ — Prospect phone in a bulk contact dump — bulk PII egress is the crown-jewel exfil risk
- 🎯 **PII/email** @ work_email col — `ghaddad@northwind.io`  
  _Diego Santos (SDR (dogfoods Apollo))_ — One of 30 prospect rows in a bulk export sitting on a personal Drive — THE 2018-breach scenario; the signal is bulk volume + destination, not any single email
- 🎯 **PII/phone** @ phone col — `(633) 387-5563`  
  _Diego Santos (SDR (dogfoods Apollo))_ — Prospect phone in a bulk contact dump — bulk PII egress is the crown-jewel exfil risk

## `apollo_app_results.json`  ·  _Apollo Platform_  ·  5 item(s)

- 🟡 **PII/email** @ results[].work_email — `mpark@northwind.io`  
  _Lena Park (Account Executive)_ — Routine business-contact data in normal in-product context — THIS IS THE PRODUCT; flagging it = unusable alert fatigue. Must NOT alert.
- 🟡 **PII/email** @ results[].work_email — `leriksson@northwind.io`  
  _Lena Park (Account Executive)_ — Routine business-contact data in normal in-product context — THIS IS THE PRODUCT; flagging it = unusable alert fatigue. Must NOT alert.
- 🟡 **PII/email** @ results[].work_email — `hnguyen@northwind.io`  
  _Lena Park (Account Executive)_ — Routine business-contact data in normal in-product context — THIS IS THE PRODUCT; flagging it = unusable alert fatigue. Must NOT alert.
- 🫥 **PII/phone** @ note_field — `(647) 820-9379`  
  _Lena Park (Account Executive)_ — A prospect's PERSONAL mobile pasted into a free-text note amid routine business data — the needle that SHOULD fire even though surrounding product data shouldn't
- 🎯 **PII/email** @ note_field — `mei.personal@gmail.com`  
  _Lena Park (Account Executive)_ — Personal (consumer) email of an individual — genuinely sensitive PII, distinct from business-contact product data; GDPR/CCPA-relevant

## `customer_acme_sfdc_sync.csv`  ·  _Salesforce CRM_  ·  2 item(s)

- 🎯 **PII/email** @ email col — `rnakamura@acmecorp.com`  
  _Aisha Diallo (Customer Success)_ — A CUSTOMER's synced Salesforce leads — third-party PII under Apollo's custody; leaking it breaks customer trust, not just Apollo's own data
- 🎯 **PII/phone** @ phone col — `(904) 936-4228`  
  _Aisha Diallo (Customer Success)_ — Customer CRM contact phone ingested for enrichment — Apollo is processor/custodian of this third-party data

## `sdr_outreach_slack.txt`  ·  _Slack_  ·  3 item(s)

- 🫥 **PII/phone** @ Diego message — `8228 7062 79`  
  _Diego Santos (SDR (dogfoods Apollo))_ — A prospect's personal cell shared in Slack as spaced digits in prose — evades field/format-anchored detection
- 🎯 **secret/db_connection_string** @ Marcus message — `postgres://svc_ngey59:YVkQfsGQONvf08Wp@db-`  
  _Marcus Lindqvist (Platform Eng)_ — Prod contact-DB URL pasted into Slack to debug — credential leaves the repo into chat history
- 🟡 **secret/uuid4** @ sequence id — `acf5e81e-7131-4269-b118-e36477097749`  
  _Diego Santos (SDR (dogfoods Apollo))_ — Sequence UUID — high-entropy but benign; should not alert

## `employee_master.csv`  ·  _Google Drive_  ·  3 item(s)

- 🎯 **PII/ssn** @ ssn col — `026-06-4012`  
  _Sofia Reyes (People/HR)_ — Employee SSNs in an HR master sheet — the universal, always-over-shared dataset
- 🎯 **financial/bank_account** @ direct_deposit_acct col — `76936763`  
  _Sofia Reyes (People/HR)_ — Employee direct-deposit account numbers
- 🎯 **PII/drivers_license** @ drivers_license col — `E0163287`  
  _Sofia Reyes (People/HR)_ — Driver's license numbers — identity-theft-grade PII
