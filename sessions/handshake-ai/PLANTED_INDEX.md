# Planted index — Handshake AI demo data

**Session `handshake-ai-1cb263`** · 99 planted items across 13 carriers · synthetic, format-valid (no real identities or live credentials).

## The demo story

Handshake AI's nightmare has two acts. **Act 1 — existential / IP:** a **frontier-lab API key committed to a repo** and **confidential `Atlas Labs` `Project Meridian` eval rubric pasted into Slack** — either breaches the NDA-bound trust the \$100M AI business runs on. **Act 2 — PII at scale:** the **contractor payout roster** (TIN/SSN + bank/routing for \$100/hr experts) and a **Snowflake export of student PII** (FERPA) sitting in shared Drive. Then we **earn credibility on precision:** the platform is saturated with internal IDs, UUIDs and content hashes shaped like secrets/SSNs — a good detector stays quiet on those while still catching the **spaced TIN** and the **base64 / line-split lab key** a naive detector misses.

Suggested surfacing order: lab-key-in-repo → confidential eval data in Slack → contractor payout roster → Snowflake student export → precision sweep over the near-misses.

**Coverage** — by category: PII 50, financial 26, secret 19, confidential 4 · by challenge: 🎯 70, 🟡 18, 🫥 11.

Legend: 🎯 straightforward · 🟡 benign near-miss (should NOT alert) · 🫥 evasive true positive.

---

## `ai-platform.env`  ·  _GitHub_  ·  5 item(s)

- 🎯 **secret/openai_key** @ OPENAI_API_KEY — `sk-proj-OhbVrpoiVgRV5IfLBcbfnoGMbJmTPSIAoCLr`  
  _Raj Patel (Platform Engineering)_ — Frontier-lab API key in committed source — direct account compromise + breach of the NDA Atlas Labs signed; the crown-jewel leak
- 🎯 **secret/openai_key** @ ATLAS_LABS_API_KEY — `sk-proj-9Wvgfygw2wMqZcUDIh7yfJs1ON43xKmTecQo`  
  _Raj Patel (Platform Engineering)_ — Customer (Atlas Labs) egress key for Project Meridian hardcoded — leaking a customer's key ends the partnership
- 🎯 **secret/aws_secret_key** @ AWS_SECRET_ACCESS_KEY — `PhDeOZIiBOB_Y6sHrFH2ZUCr_lgotu2iXW7GboIR`  
  _Raj Patel (Platform Engineering)_ — Cloud master credential in source — full infra compromise
- 🎯 **secret/db_connection_string** @ DATABASE_URL — `postgres://svc_hsbkda:9U4UqGWlG6g3Ot1O@db-gm`  
  _Raj Patel (Platform Engineering)_ — Prod DB connection string with inline password — lateral movement to all user PII
- 🟡 **secret/placeholder_key** @ EXAMPLE_KEY — `YOUR_API_KEY_HERE`  
  _Raj Patel (Platform Engineering)_ — Well-known AWS example key — a good detector allowlists it, telling the no-alert-fatigue story

## `settings.py`  ·  _GitHub_  ·  3 item(s)

- 🎯 **secret/slack_bot_token** @ SLACK_BOT_TOKEN — `xoxb-279368618081-757132452561-uFbh7x41Ztpdp`  
  _Mei Lin (ML Infra (ex-Cleanlab))_ — Slack bot token in source — workspace takeover, read every ops channel
- 🎯 **secret/jwt** @ INTERNAL_JWT — `qq8vH2BzNZV45pFCiRcDCajhDieQjEJ-Bq8F.80ymm3T`  
  _Mei Lin (ML Infra (ex-Cleanlab))_ — Signed service JWT committed — impersonate the eval service
- 🟡 **secret/git_sha** @ PINNED_MODEL_COMMIT — `85ed03241b4d419b1b673bd4755d05ad7853c1f7`  
  _Mei Lin (ML Infra (ex-Cleanlab))_ — 40-hex git SHA pinning a checkpoint — high-entropy but NOT a secret; over-firing here trains reviewers to ignore alerts

## `atlas-deploy_service-account.json`  ·  _GitHub_  ·  2 item(s)

- 🎯 **secret/rsa_private_key** @ private_key — `-----BEGIN RSA PRIVATE KEY-----
3U6t3wI973IP`  
  _Mei Lin (ML Infra (ex-Cleanlab))_ — GCP service-account private key committed — full cloud-project compromise
- 🎯 **secret/google_api_key** @ maps_api_key — `AIza3RURz92ZJxfYzaqIhDxRVRqLy0O8xgRoEbN`  
  _Mei Lin (ML Infra (ex-Cleanlab))_ — Google API key alongside the SA key — billing abuse + data access

## `atlas-labs-meridian_eval.json`  ·  _Annotation Platform_  ·  4 item(s)

- 🫥 **confidential/lab_eval_rubric** @ rubric — `Project Meridian rubric v3 (CONFIDENTIAL — A`  
  _Dana Okafor (AI Training Ops)_ — Confidential Atlas Labs eval rubric + held-out benchmark reference — pure IP leak, no regex PII to catch; tests content/classification not pattern matching
- 🫥 **PII/full_name** @ expert_answer — `Mei Choi`  
  _Dana Okafor (AI Training Ops) via Clara Weber_ — Identifiable person (name+DOB) inside an expert's free-text answer — PII in prose, split across a sentence, not a labeled field
- 🫥 **secret/openai_key** @ expert_answer — `sk-proj-Qmzvr3e9XrwPGzR1Iv8bh4qlL9qcgMBwUYuB`  
  _Clara Weber (contractor)_ — Live key buried mid-sentence in a JSON free-text blob — recall test for secrets outside key=value shape
- 🟡 **secret/git_sha** @ dataset_content_hash — `6bd2aa399dac946dc59c0996daeee6f529a27976`  
  _Arjun Shah (Trust & Safety / Data)_ — Dataset content hash (Cleanlab-style) — looks like a secret, isn't

## `eval-pipeline_slack.txt`  ·  _Slack_  ·  4 item(s)

- 🎯 **secret/github_pat** @ Mei message — `ghp_EN2XeDA4OKmTSyFzpjPSa5W3X4gXBolZ9SHD`  
  _Mei Lin (ML Infra (ex-Cleanlab))_ — GitHub PAT pasted in Slack to debug — credential leaves the repo perimeter into chat history
- 🫥 **confidential/lab_eval_rubric** @ Dana message — `Project Meridian rubric (held-out medical be`  
  _Dana Okafor (AI Training Ops)_ — Confidential Atlas Labs rubric quoted in Slack — IP disclosure as prose
- 🫥 **secret/openai_key** @ Mei message 2 — `c2stcHJvai1kSnA2MmhEaVpEUUhKTXU4VzVDTjBVNUdC`  
  _Mei Lin (ML Infra (ex-Cleanlab))_ — Grader API key base64-wrapped in a chat message — whitespace/format-fragile detectors miss it
- 🟡 **secret/uuid4** @ Raj message — `49257af1-b6aa-405b-93d5-f2f7709b7d97`  
  _Raj Patel (Platform Engineering)_ — Task UUID — high-entropy but benign; should not alert

## `ci-build.log`  ·  _CI_  ·  3 item(s)

- 🎯 **secret/aws_secret_key** @ export line — `EIQOkrtDXtBi10Q71hA1XcW9aTMX1C-CI3-dXRZv`  
  _Raj Patel (Platform Engineering)_ — Secret echoed into CI build log — logs are widely readable and long-retained
- 🫥 **secret/openai_key** @ heredoc — `sk-proj-1D6iNIb6zLKQbfPBi3Dl\ndqyunDuvW4yrW8`  
  _Raj Patel (Platform Engineering)_ — Lab key split across two lines in a log — line-anchored regexes miss it
- 🟡 **secret/git_sha** @ build id — `210760474f36e8b5359309cc6273931bdb2a0df3`  
  _Raj Patel (Platform Engineering)_ — Build commit SHA — not a secret

## `partnerships_meridian_nda.eml`  ·  _Email_  ·  2 item(s)

- 🎯 **secret/openai_key** @ body key — `sk-proj-eh15FMIbOGKpTjsBaNwpKAlQQfHxe9HIGYGJ`  
  _Nicole Tran (Partnerships)_ — Production egress key shared in plaintext email to onboard a lab integration — secret leaves the org boundary
- 🫥 **confidential/contract_terms** @ subject/body — `Project Meridian integration — egress key (C`  
  _Nicole Tran (Partnerships)_ — Confidential Atlas Labs/Project Meridian relationship disclosed in email metadata + body

## `expert_payouts.csv`  ·  _Google Drive_  ·  28 item(s)

- 🎯 **PII/ssn** @ tin_ssn r1 — `651-60-4952`  
  _Sofia Reyes (Payments Ops)_ — Contractor TIN/SSN ($125/hr expert Soren Schmidt) in a shared-drive payout sheet — bulk PII at scale
- 🎯 **financial/bank_account** @ bank_account r1 — `12004711382`  
  _Sofia Reyes (Payments Ops)_ — Expert payout bank account — financial data outside any controlled system
- 🎯 **financial/us_routing** @ routing r1 — `675869265`  
  _Sofia Reyes (Payments Ops)_ — ABA routing number paired with the account = funds-movement risk
- 🟡 **PII/internal_id_like_ssn** @ expert_id r1 — `EXP-674-51-4626`  
  _Sofia Reyes (Payments Ops)_ — Internal expert ID shaped like an SSN — over-firing here buries the real TINs
- 🫥 **PII/ssn** @ tin_ssn r2 — `3802 8726 5`  
  _Sofia Reyes (Payments Ops)_ — TIN entered with spaces instead of dashes — recall test on whitespace-fragile SSN/TIN regex
- 🎯 **financial/bank_account** @ bank_account r2 — `35158506431`  
  _Sofia Reyes (Payments Ops)_ — Expert payout bank account — financial data outside any controlled system
- 🎯 **financial/us_routing** @ routing r2 — `713900536`  
  _Sofia Reyes (Payments Ops)_ — ABA routing number paired with the account = funds-movement risk
- 🟡 **PII/internal_id_like_ssn** @ expert_id r2 — `EXP-201-72-7686`  
  _Sofia Reyes (Payments Ops)_ — Internal expert ID shaped like an SSN — over-firing here buries the real TINs
- 🎯 **PII/ssn** @ tin_ssn r3 — `213-76-3539`  
  _Sofia Reyes (Payments Ops)_ — Contractor TIN/SSN ($100/hr expert Priya Navarro) in a shared-drive payout sheet — bulk PII at scale
- 🎯 **financial/bank_account** @ bank_account r3 — `529042284`  
  _Sofia Reyes (Payments Ops)_ — Expert payout bank account — financial data outside any controlled system
- 🎯 **financial/us_routing** @ routing r3 — `210205394`  
  _Sofia Reyes (Payments Ops)_ — ABA routing number paired with the account = funds-movement risk
- 🟡 **PII/internal_id_like_ssn** @ expert_id r3 — `EXP-905-82-4362`  
  _Sofia Reyes (Payments Ops)_ — Internal expert ID shaped like an SSN — over-firing here buries the real TINs
- 🎯 **PII/ssn** @ tin_ssn r4 — `432-68-1863`  
  _Sofia Reyes (Payments Ops)_ — Contractor TIN/SSN ($100/hr expert Diego Haddad) in a shared-drive payout sheet — bulk PII at scale
- 🎯 **financial/bank_account** @ bank_account r4 — `77589178`  
  _Sofia Reyes (Payments Ops)_ — Expert payout bank account — financial data outside any controlled system
- 🎯 **financial/us_routing** @ routing r4 — `390847009`  
  _Sofia Reyes (Payments Ops)_ — ABA routing number paired with the account = funds-movement risk
- 🟡 **PII/internal_id_like_ssn** @ expert_id r4 — `EXP-116-32-5347`  
  _Sofia Reyes (Payments Ops)_ — Internal expert ID shaped like an SSN — over-firing here buries the real TINs
- 🎯 **PII/ssn** @ tin_ssn r5 — `503-92-7268`  
  _Sofia Reyes (Payments Ops)_ — Contractor TIN/SSN ($125/hr expert Pablo Reyes) in a shared-drive payout sheet — bulk PII at scale
- 🎯 **financial/bank_account** @ bank_account r5 — `15921249`  
  _Sofia Reyes (Payments Ops)_ — Expert payout bank account — financial data outside any controlled system
- 🎯 **financial/us_routing** @ routing r5 — `985698472`  
  _Sofia Reyes (Payments Ops)_ — ABA routing number paired with the account = funds-movement risk
- 🟡 **PII/internal_id_like_ssn** @ expert_id r5 — `EXP-967-61-7984`  
  _Sofia Reyes (Payments Ops)_ — Internal expert ID shaped like an SSN — over-firing here buries the real TINs
- 🎯 **PII/ssn** @ tin_ssn r6 — `565-93-3523`  
  _Sofia Reyes (Payments Ops)_ — Contractor TIN/SSN ($100/hr expert Zoe Andersson) in a shared-drive payout sheet — bulk PII at scale
- 🎯 **financial/bank_account** @ bank_account r6 — `73657661565`  
  _Sofia Reyes (Payments Ops)_ — Expert payout bank account — financial data outside any controlled system
- 🎯 **financial/us_routing** @ routing r6 — `452711112`  
  _Sofia Reyes (Payments Ops)_ — ABA routing number paired with the account = funds-movement risk
- 🟡 **PII/internal_id_like_ssn** @ expert_id r6 — `EXP-719-65-2624`  
  _Sofia Reyes (Payments Ops)_ — Internal expert ID shaped like an SSN — over-firing here buries the real TINs
- 🎯 **PII/ssn** @ tin_ssn r7 — `601-72-9203`  
  _Sofia Reyes (Payments Ops)_ — Contractor TIN/SSN ($125/hr expert Felix Romano) in a shared-drive payout sheet — bulk PII at scale
- 🎯 **financial/bank_account** @ bank_account r7 — `1656049451`  
  _Sofia Reyes (Payments Ops)_ — Expert payout bank account — financial data outside any controlled system
- 🎯 **financial/us_routing** @ routing r7 — `983273158`  
  _Sofia Reyes (Payments Ops)_ — ABA routing number paired with the account = funds-movement risk
- 🟡 **PII/internal_id_like_ssn** @ expert_id r7 — `EXP-198-57-3131`  
  _Sofia Reyes (Payments Ops)_ — Internal expert ID shaped like an SSN — over-firing here buries the real TINs

## `students_export.csv`  ·  _Snowflake_  ·  15 item(s)

- 🎯 **PII/email** @ school_email r1 — `nandersson29@umich.edu`  
  _Arjun Shah (Trust & Safety / Data)_ — Student .edu email (Univ. of Michigan) in a Snowflake unload — FERPA + CCPA exposure at scale
- 🎯 **PII/dob** @ dob r1 — `07/28/1985`  
  _Arjun Shah (Trust & Safety / Data)_ — Student DOB — FERPA education-record identifier
- 🎯 **PII/email** @ school_email r2 — `klindqvist85@stanford.edu`  
  _Arjun Shah (Trust & Safety / Data)_ — Student .edu email (Stanford University) in a Snowflake unload — FERPA + CCPA exposure at scale
- 🎯 **PII/dob** @ dob r2 — `12/09/1951`  
  _Arjun Shah (Trust & Safety / Data)_ — Student DOB — FERPA education-record identifier
- 🎯 **PII/email** @ school_email r3 — `olarsson24@umich.edu`  
  _Arjun Shah (Trust & Safety / Data)_ — Student .edu email (Univ. of Michigan) in a Snowflake unload — FERPA + CCPA exposure at scale
- 🎯 **PII/dob** @ dob r3 — `03/19/1992`  
  _Arjun Shah (Trust & Safety / Data)_ — Student DOB — FERPA education-record identifier
- 🟡 **PII/internal_id_like_ssn** @ student_id r3 — `STU-447-54-1100`  
  _Arjun Shah (Trust & Safety / Data)_ — Student ID shaped like an SSN (STU-NNN-NN-NNNN) — classic education false-positive source
- 🎯 **PII/email** @ school_email r4 — `lschmidt4@berkeley.edu`  
  _Arjun Shah (Trust & Safety / Data)_ — Student .edu email (UC Berkeley) in a Snowflake unload — FERPA + CCPA exposure at scale
- 🎯 **PII/dob** @ dob r4 — `02/24/1983`  
  _Arjun Shah (Trust & Safety / Data)_ — Student DOB — FERPA education-record identifier
- 🎯 **PII/email** @ school_email r5 — `wnakamura44@uw.edu`  
  _Arjun Shah (Trust & Safety / Data)_ — Student .edu email (Univ. of Washington) in a Snowflake unload — FERPA + CCPA exposure at scale
- 🎯 **PII/dob** @ dob r5 — `03/12/1969`  
  _Arjun Shah (Trust & Safety / Data)_ — Student DOB — FERPA education-record identifier
- 🎯 **PII/email** @ school_email r6 — `mfischer20@mit.edu`  
  _Arjun Shah (Trust & Safety / Data)_ — Student .edu email (MIT) in a Snowflake unload — FERPA + CCPA exposure at scale
- 🎯 **PII/dob** @ dob r6 — `03/25/1989`  
  _Arjun Shah (Trust & Safety / Data)_ — Student DOB — FERPA education-record identifier
- 🎯 **PII/email** @ school_email r7 — `dkowalski85@umich.edu`  
  _Arjun Shah (Trust & Safety / Data)_ — Student .edu email (Univ. of Michigan) in a Snowflake unload — FERPA + CCPA exposure at scale
- 🎯 **PII/dob** @ dob r7 — `07/16/1988`  
  _Arjun Shah (Trust & Safety / Data)_ — Student DOB — FERPA education-record identifier

## `employee_master.csv`  ·  _Google Drive_  ·  18 item(s)

- 🎯 **PII/ssn** @ ssn r1 — `047-29-6476`  
  _Priya Nair (People/HR)_ — Employee SSN (Imani Choi) in the HR master sheet — the universal, always-over-shared dataset
- 🎯 **financial/bank_account** @ direct_deposit r1 — `432445107`  
  _Priya Nair (People/HR)_ — Employee direct-deposit account number
- 🎯 **PII/drivers_license** @ drivers_license r1 — `X6226838`  
  _Priya Nair (People/HR)_ — Driver's license number — identity-theft-grade PII
- 🎯 **PII/ssn** @ ssn r2 — `044-56-0308`  
  _Priya Nair (People/HR)_ — Employee SSN (Priya Diallo) in the HR master sheet — the universal, always-over-shared dataset
- 🎯 **financial/bank_account** @ direct_deposit r2 — `9696641605`  
  _Priya Nair (People/HR)_ — Employee direct-deposit account number
- 🎯 **PII/drivers_license** @ drivers_license r2 — `F9751613`  
  _Priya Nair (People/HR)_ — Driver's license number — identity-theft-grade PII
- 🎯 **PII/ssn** @ ssn r3 — `537-11-6485`  
  _Priya Nair (People/HR)_ — Employee SSN (Tariq Diallo) in the HR master sheet — the universal, always-over-shared dataset
- 🎯 **financial/bank_account** @ direct_deposit r3 — `521818835`  
  _Priya Nair (People/HR)_ — Employee direct-deposit account number
- 🎯 **PII/drivers_license** @ drivers_license r3 — `L2312432`  
  _Priya Nair (People/HR)_ — Driver's license number — identity-theft-grade PII
- 🎯 **PII/ssn** @ ssn r4 — `182-99-8096`  
  _Priya Nair (People/HR)_ — Employee SSN (Soren Schmidt) in the HR master sheet — the universal, always-over-shared dataset
- 🎯 **financial/bank_account** @ direct_deposit r4 — `799552717744`  
  _Priya Nair (People/HR)_ — Employee direct-deposit account number
- 🎯 **PII/drivers_license** @ drivers_license r4 — `S0581477`  
  _Priya Nair (People/HR)_ — Driver's license number — identity-theft-grade PII
- 🎯 **PII/ssn** @ ssn r5 — `294-10-1480`  
  _Priya Nair (People/HR)_ — Employee SSN (Diego Volkov) in the HR master sheet — the universal, always-over-shared dataset
- 🎯 **financial/bank_account** @ direct_deposit r5 — `79807935978`  
  _Priya Nair (People/HR)_ — Employee direct-deposit account number
- 🎯 **PII/drivers_license** @ drivers_license r5 — `E0715182`  
  _Priya Nair (People/HR)_ — Driver's license number — identity-theft-grade PII
- 🎯 **PII/ssn** @ ssn r6 — `450-68-8565`  
  _Priya Nair (People/HR)_ — Employee SSN (Liam Santos) in the HR master sheet — the universal, always-over-shared dataset
- 🎯 **financial/bank_account** @ direct_deposit r6 — `4665905151`  
  _Priya Nair (People/HR)_ — Employee direct-deposit account number
- 🎯 **PII/drivers_license** @ drivers_license r6 — `R6449251`  
  _Priya Nair (People/HR)_ — Driver's license number — identity-theft-grade PII

## `contractor_onboarding.eml`  ·  _Email_  ·  2 item(s)

- 🫥 **PII/ssn** @ body TIN — `4535 4447 6`  
  _Liam Brennan (Expert Network Ops)_ — TIN written with spaces in email prose — evades dash-anchored SSN/TIN detection
- 🫥 **financial/bank_account** @ body account — `8156-1497-8`  
  _Liam Brennan (Expert Network Ops)_ — Bank account dash-grouped in free text — recall test on financial formats

## `payout_support_ticket.txt`  ·  _Zendesk_  ·  2 item(s)

- 🎯 **PII/ssn** @ requester message — `247-94-1699`  
  _Priya Rossi (contractor)_ — Contractor pasted a full SSN into a support ticket — same PII, a third surface (CX tooling) and a free-text framing, not a spreadsheet cell
- 🎯 **PII/phone** @ requester message — `(796) 952-6447`  
  _Priya Rossi (contractor)_ — Phone number in a support ticket — secondary identifier, broadens the PII surface

## `salesforce_opportunities.csv`  ·  _Salesforce CRM_  ·  11 item(s)

- 🎯 **PII/email** @ contact_email r1 — `marcus.volkov@initech.co`  
  _Nicole Tran (Partnerships)_ — Customer contact PII (Atlas Labs) exported from CRM into a flat file
- 🟡 **financial/order_id_like_pan** @ opportunity_number r1 — `5462914865281685`  
  _Nicole Tran (Partnerships)_ — 16-digit opportunity number shaped like a card PAN (Luhn-fail) — must not alert as PCI
- 🎯 **PII/email** @ contact_email r2 — `hannah.acharya@umbrella-health.org`  
  _Nicole Tran (Partnerships)_ — Customer contact PII (Beacon Research) exported from CRM into a flat file
- 🟡 **financial/order_id_like_pan** @ opportunity_number r2 — `2357332214188805`  
  _Nicole Tran (Partnerships)_ — 16-digit opportunity number shaped like a card PAN (Luhn-fail) — must not alert as PCI
- 🎯 **PII/email** @ contact_email r3 — `camila.silva@initech.co`  
  _Nicole Tran (Partnerships)_ — Customer contact PII (Cirrus Labs) exported from CRM into a flat file
- 🟡 **financial/order_id_like_pan** @ opportunity_number r3 — `2292706537947383`  
  _Nicole Tran (Partnerships)_ — 16-digit opportunity number shaped like a card PAN (Luhn-fail) — must not alert as PCI
- 🎯 **PII/email** @ contact_email r4 — `andre.andersson@initech.co`  
  _Nicole Tran (Partnerships)_ — Customer contact PII (Beacon Research) exported from CRM into a flat file
- 🟡 **financial/order_id_like_pan** @ opportunity_number r4 — `7468862392407581`  
  _Nicole Tran (Partnerships)_ — 16-digit opportunity number shaped like a card PAN (Luhn-fail) — must not alert as PCI
- 🎯 **PII/email** @ contact_email r5 — `diego.costa@umbrella-health.org`  
  _Nicole Tran (Partnerships)_ — Customer contact PII (Northstar AI) exported from CRM into a flat file
- 🟡 **financial/order_id_like_pan** @ opportunity_number r5 — `7901043289861434`  
  _Nicole Tran (Partnerships)_ — 16-digit opportunity number shaped like a card PAN (Luhn-fail) — must not alert as PCI
- 🫥 **confidential/contract_terms** @ nda_terms r1 — `Project Meridian expert pool, exclusivity 18`  
  _Nicole Tran (Partnerships)_ — Confidential Atlas Labs deal terms (Project Meridian) in a CRM export — competitively sensitive, no regex PII
