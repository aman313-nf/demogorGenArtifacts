# OncoHealth — planted demo data: briefing

**Synthetic data only.** Patient names, identifiers, and notes are fabricated; ICD-10 codes, drug names, and genomic markers are real clinical *terms* (not tied to anyone). Values are format-valid (valid SSNs, Luhn-valid NPIs starting 1/2, real C-code diagnoses) so a real detector fires — none maps to a real person or record.

## The story

OncoHealth is a **digital oncology management** company — prior-auth/UM (OneUM), oncology analytics (Oncology Insights), and the **Iris** telehealth platform — holding the most sensitive data class there is: **cancer diagnosis + genomic markers + oncology mental-health notes**, under HIPAA *and* GINA. Open on the crown jewel: a **prior-auth packet** from an external oncology practice — a named patient, DOB, member ID, **breast cancer (C50.911)**, a **BRCA1** result, a **pembrolizumab** regimen. Then the **Iris care-team Slack**, where a nurse and a peer mentor discuss the same kind of patient's **lung cancer and suicidal ideation** in prose — and the context-aware **PHI detector catches the whole combo** where a regex never could (recall). Then the precision turn: point that detector at the **clinical criteria library** — dense with the *same* codes and drugs — and it **stays quiet** (no patient), while naive code-matching would flood reviewers. Close on the **gaps**: **genomic markers, MRNs, and member IDs** that off-the-shelf detectors miss, and a **'de-identified' research export** with a residual DOB/MRN that quietly turns it back into PHI.

**32 planted values** across **7 carriers** — 17 straightforward · 7 FP near-misses (precision) · 8 FN-evasive (recall). Scan report card (see `detector_results.json` / the app's Detector-results tab): the free-text PHI combo is **caught**; the criteria doc shows raw ICD-10/drug matching **over-firing** while context-aware PHI detection stays **quiet** on the same file; genomic/MRN/member-ID are **not integrated** (coverage gaps).

---

## Prior-authorization request — Secure email / fax intake (LEAD)

`carriers/prior_auth_request.eml`

- **full_name** — ✅ straightforward · *PHI* · Patient field  
  `Margaret Sullivan`  
  _Dr. Robert Cohen (Cedar Valley Oncology — external)_ — Named cancer patient on an inbound PA request — the identity half of PHI.
- **dob** — ✅ straightforward · *PHI* · DOB field  
  `03/14/1958`  
  _Dr. Robert Cohen (Cedar Valley Oncology — external)_ — Date of birth labeled 'DOB' beside the diagnosis — a HIPAA identifier.
- **insurance_member_id** — ✅ straightforward · *PHI* · Member ID field  
  `BCBS043321819`  
  _Dr. Robert Cohen (Cedar Valley Oncology — external)_ — Health-plan member ID. No off-the-shelf detector maps to it — a real coverage gap to name for a company that lives in payer member data.
- **mrn** — ✅ straightforward · *PHI* · MRN field  
  `MRN-60013389`  
  _Dr. Robert Cohen (Cedar Valley Oncology — external)_ — Medical record number — another uncovered identifier (no MRN detector), yet it's the join key that re-links any leaked fragment back to the patient.
- **icd10** — ✅ straightforward · *PHI* · Diagnosis field  
  `C50.911`  
  _Dr. Robert Cohen (Cedar Valley Oncology — external)_ — Cancer diagnosis code C50.911 (breast) — caught by the ICD-10 detector.
- **drug_name** — ✅ straightforward · *PHI* · regimen (clinical note)  
  `pembrolizumab`  
  _Dr. Robert Cohen (Cedar Valley Oncology — external)_ — Oncology drug (pembrolizumab) — the FDA drug-name detector fires; reveals the treatment, which combined with identity is squarely PHI.
- **genomic_marker** — 🔴 FN-evasive · *PHI* · germline result (clinical note)  
  `BRCA1 pathogenic variant`  
  _Dr. Robert Cohen (Cedar Valley Oncology — external)_ — A germline BRCA1 result — genetic data protected under GINA, sitting in prose. No detector recognizes genomic markers: the most distinctive coverage gap here.
- **npi** — ✅ straightforward · *PHI* · Ordering NPI field  
  `1838637944`  
  _Dr. Robert Cohen (Cedar Valley Oncology — external)_ — Ordering provider NPI — ties the packet to a specific oncologist/practice.

## Iris care-team coordination — Slack (#iris-care-team)

`carriers/iris_care_team_slack.txt`

- **phi_note** — 🔴 FN-evasive · *PHI* · Grace 8:12 message  
  `checking in on James Whitfield (DOB 05/02/1961, m…`  
  _Grace Okafor, RN OCN (Iris care team)_ — A nurse describing a named patient's lung cancer AND suicidal ideation in chat — cancer + mental-health PHI in pure prose, with no labeled fields. The context-aware PHI detector catches the whole combo where a regex never could. The recall headline, and the most sensitive data class OncoHealth holds.
- **phi_note** — 🔴 FN-evasive · *PHI* · Marcus 8:24 message  
  `I talked with James Whitfield as his peer mentor …`  
  _Marcus Reyes (Iris peer mentor)_ — A peer mentor — quasi-external staff — discussing the patient's depression and prognosis. The defining-workforce surface a generic demo never thinks to monitor; PHI detection ties it to the patient named upthread.
- **genomic_marker** — 🔴 FN-evasive · *PHI* · Grace 8:12 (genomic)  
  `EGFR exon 19 deletion`  
  _Grace Okafor, RN OCN (Iris care team)_ — EGFR exon 19 deletion in chat — genetic data (GINA) with no detector coverage. The PHI detector flags the surrounding patient context, but the genomic marker itself is an uncovered data type worth a custom detector.

## Clinical PA criteria library — Confluence / Drive

`carriers/clinical_pa_criteria.txt`

- **icd10** — 🟡 FP near-miss · *PHI* · Lung criteria — ICD-10  
  `C34.90`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — An ICD-10 code in a clinical-criteria document with NO patient. A raw ICD-10 detector fires here and floods reviewers with alerts on their own policy library — the alert-fatigue trap. The fix is context, not code matching.
- **drug_name** — 🟡 FP near-miss · *PHI* · Lung criteria — drug  
  `pembrolizumab`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — A drug name in a guideline. Drug-name matching over-fires on criteria the same way — your work product is made of these terms.
- **phi_note** — 🟡 FP near-miss · *PHI* · Lung criteria — disease context  
  `First-line therapy for metastatic non-small cell …`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — The money shot: point the context-aware PHI detector at the SAME criteria doc and it stays SILENT — there's no patient. Same document, naive code-matching screams, PHI detection is quiet. That's the precision argument in one file.

## Member roster export — Snowflake / payer feed

`carriers/member_roster_export.csv`

- **ssn** — ✅ straightforward · *PHI* · legacy_subscriber_ssn column (row 1)  
  `353-78-4334`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — A real subscriber SSN carried in a legacy column of a bulk member roster — SSN detected, and a reminder that payer feeds still drag SSNs into oncology data.
- **icd10** — ✅ straightforward · *PHI* · primary_dx column (row 1)  
  `C61`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — Prostate cancer code C61 tied row-wise to a named member — bulk diagnosis exposure.
- **insurance_member_id** — ✅ straightforward · *PHI* · member_id column (row 1)  
  `BCBS618495931`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — Member ID — uncovered by detectors, but the primary key the payer indexes the patient by.
- **mrn** — ✅ straightforward · *PHI* · mrn column (row 1)  
  `MRN-03413164`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — MRN in a bulk export — another uncovered identifier worth a custom detector.
- **internal_id_like_ssn** — 🟡 FP near-miss · *PHI* · claim_number column  
  `EMP-489-22-6881`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — A claim number formatted NNN-NN-NNNN — looks like an SSN but isn't. A precise detector stays quiet; a naive one flags an SSN on every claim row.
- **ssn** — 🔴 FN-evasive · *PHI* · legacy_subscriber_ssn column (row 2)  
  `045 947 528`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — A real subscriber SSN carried in a legacy column with spaces instead of dashes — a whitespace evasion that brittle detectors miss. Tests recall.
- **dob** — 🔴 FN-evasive · *PHI* · dob column (row 1)  
  `11/02/1949`  
  _Dr. Priya Kapoor (Medical Director, UM)_ — DOB isolated in a bare spreadsheet column — no contextual cue for a context-aware detector to grab. The structured-export recall blind spot (format-distinctive types like names still fire; bare dates don't).

## De-identified research export — Google Drive (Oncology Insights)

`carriers/research_export.eml`

- **internal_id_like_ssn** — 🟡 FP near-miss · *PHI* · subject key  
  `EMP-159-40-2290`  
  _Wei Chen (Oncology Insights / Data Science)_ — A pseudonymous study-subject key formatted like an SSN. It's a de-identified research artifact — a precise detector must stay quiet, or every analytics export becomes an alert.
- **dob** — ✅ straightforward · *PHI* · QA note — residual DOB  
  `07/22/1971`  
  _Wei Chen (Oncology Insights / Data Science)_ — A residual DOB left in a 'de-identified' extract — the exact failure that flips Safe-Harbor data back into PHI and breaches the research BAA. Re-identification risk.
- **mrn** — ✅ straightforward · *PHI* · QA note — residual MRN  
  `MRN-17182278`  
  _Wei Chen (Oncology Insights / Data Science)_ — A source MRN that survived de-identification — uncovered by detectors and a direct re-link to the real patient.

## Platform production config — GitHub

`carriers/platform-api.env`

- **db_connection_string** — ✅ straightforward · *secret* · DATABASE_URL  
  `postgres://svc_kqh3mb:9n7IWUSmTtzQPxC5@db-hchp.in…`  
  _Diego Santos (Platform Engineering)_ — Connection string to the Aurora PHI datastore — members, PA packets, and Iris care notes. One leaked string exposes every patient record at once.
- **openai_key** — ✅ straightforward · *secret* · OPENAI_API_KEY  
  `sk-proj-YEZAmggQBwBAD3UdRPPgdzUvZ3gpmmICiBlrDp37e…`  
  _Diego Santos (Platform Engineering)_ — An LLM key used to summarize clinical notes — leaks the credential AND signals that PHI is flowing to an external model (a BAA / data-residency question).
- **github_pat** — ✅ straightforward · *secret* · GITHUB_DEPLOY_TOKEN  
  `ghp_oevbLJoLoaeTOdoe5c3veGprQFnIiU74KKEp`  
  _Diego Santos (Platform Engineering)_ — A GitHub deploy token for the Iris services — access to the source running the telehealth platform.
- **placeholder_key** — 🟡 FP near-miss · *secret* · SENDGRID_TEST_KEY  
  `xoxb-000000000000-000000000000-XXXXXXXXXXXXXXXXXX…`  
  _Diego Santos (Platform Engineering)_ — A well-known example/test key. A precise detector allowlists it — firing here is the alert fatigue that erodes trust in the tool.

## HR employee master — Google Drive

`carriers/employee_master.csv`

- **ssn** — ✅ straightforward · *PII* · ssn column (row 1)  
  `243-22-6659`  
  _Hannah Larsson (People / HR)_ — Employee SSN in an HR master sheet on a shared drive — the universal HR exposure.
- **internal_id_like_ssn** — 🟡 FP near-miss · *PII* · employee_id column  
  `EMP-985-61-1960`  
  _Hannah Larsson (People / HR)_ — An internal employee ID formatted NNN-NN-NNNN — looks like an SSN but isn't. A good detector stays quiet; a naive one cries SSN on every row.
- **ssn** — 🔴 FN-evasive · *PII* · ssn column (row 2)  
  `169 490 036`  
  _Hannah Larsson (People / HR)_ — An SSN entered with spaces instead of dashes — a classic whitespace evasion. Tests recall on loosely-formatted PII.
- **street_address** — 🔴 FN-evasive · *PII* · home_address column (row 1)  
  `812 Maple Crest Dr, Tampa, FL 33602`  
  _Hannah Larsson (People / HR)_ — A home address isolated in a spreadsheet cell with no label — context-aware address detection under-fires here even though it lights up the same address in prose. The structured-export recall blind spot.
