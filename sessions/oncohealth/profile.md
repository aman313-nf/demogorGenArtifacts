# Company profile — OncoHealth

Prospect for a Nightfall DLP/data-security demo. Synthetic data only; this profile
drives *what* we plant and *why each finding lands for OncoHealth specifically*.

---

## 0. What's distinctive — the non-obvious risks (the demo's spine)

OncoHealth is a **digital oncology management** company: it sits between health
plans/employers, oncology practices, and patients, running **prior authorization /
utilization management (OneUM)**, **oncology analytics (Oncology Insights)**, and the
**Iris** virtual supportive-care platform (24/7 oncology nurses, mental-health
therapists, dietitians, peer mentors). It touches **12M+ lives**. That means it holds
the single most sensitive data class in existence: **a named person + their cancer
diagnosis + genomic markers + drug regimen + mental-health state** — all at once,
governed by HIPAA *and* GINA (genetic) *and* heightened psychotherapy-note rules.

1. **Prior-authorization clinical packets — the crown-jewel PHI.** A OneUM PA request
   bundles patient identity (name/DOB/member ID/MRN) + cancer diagnosis (ICD-10
   C-codes) + biomarker results + chemo/radiation regimen + a clinical narrative, and
   it flows *between organizations*: an external oncology practice → OncoHealth
   reviewers → the payer. One leaked PA packet is a maximally damaging,
   cancer-diagnosis-level breach. *(fact: OneUM streamlines oncology PAs → implication:
   the richest possible PHI transits org boundaries → use case: the leak that defines
   their risk.)*

2. **Iris care-team & peer-mentor coordination leaks PHI in free text.** The defining
   workforce — oncology-certified **nurses, social workers, psychologists, dietitians,
   and (quasi-external) peer mentors** — coordinates patient care 24/7 in chat and
   notes, describing a patient's cancer *and* emotional/mental-health state in prose
   with no labeled fields. Mental-health notes about cancer patients carry the highest
   confidentiality bar. This is the recall crown jewel and the surface a generic demo
   would miss.

3. **The clinical criteria library is a false-positive minefield.** OncoHealth's PA
   decision criteria and clinical guidelines are *dense with ICD-10 codes and drug
   names by design* — that's the work product. A naive, code-matching detector fires on
   every criteria document and floods reviewers with alerts on their own library. The
   precision pitch: **detect PHI by patient context, not by code** (Nightfall's
   PHI detector stays quiet on a criteria doc; a regex/code detector does not).

4. **Genomic/biomarker data is protected but uncovered.** BRCA1/2, EGFR, ALK, HER2,
   PD-L1, KRAS, MSI status drive every treatment decision here. Genetic information is
   its own protected class under GINA — yet no off-the-shelf detector recognizes it.
   A coverage gap, alongside **MRN** and **health-plan member IDs** (also uncovered).

5. **Analytics re-identification risk.** Oncology Insights shares "de-identified"
   real-world datasets with payers and life-science researchers under BAAs. A single
   residual identifier left in — a DOB, an MRN, a rare-cancer + ZIP combination — flips
   a de-identified extract back into PHI and breaches the agreement.

These five are the lead talking points; the secrets/HR layers are supporting cast.

## 1. What they do
- **Industry / sub-vertical:** digital oncology management / health-tech (UM &
  prior-auth, oncology analytics, telehealth supportive care). Customers: health plans,
  employers, providers, life-science researchers; end-users are cancer patients.
- **Products:** **OneUM** (oncology-specific utilization management / prior auth, incl.
  radiation oncology), **Oncology Insights** (real-world-data analytics on oncology drug
  spend), **Iris by OncoHealth** (24×7 virtual oncology nurses, mental-health therapy,
  nutrition, peer mentors; mobile/telehealth).
- **Regulatory regime:** **HIPAA/HITECH** (PHI — the core), **GINA** (genetic data),
  **42 CFR Part 2 / psychotherapy-note rules** (mental health), **SOC 2/HITRUST**
  expectations, BAAs with payers and researchers, state privacy laws. Formerly Oncology
  Analytics (rebrand).
- **Stage / scale:** PE-backed (Arsenal Capital Partners) with strategic investment from
  **McKesson**; serves **12M+ individuals** across the US + Puerto Rico; hundreds of
  employees incl. a large remote clinical workforce.

## 2. Team structure → personas / who-leaks-what

| Team | ~Size | Sensitive data they handle |
| --- | --- | --- |
| **Iris clinical care team** *(defining persona)* | ~150 | **Patient PHI in notes/chat: cancer Dx, mental-health state, genomic results** — nurses, social workers, psychologists, dietitians, peer mentors |
| Medical review / UM (OneUM) | ~80 | Prior-auth packets: Dx, biomarkers, regimens, member IDs, MRNs |
| Data science / Oncology Insights | ~30 | Real-world patient data, de-identified extracts, claims, drug spend |
| Platform Engineering | ~50 | AWS/PHI-DB creds, API keys (telehealth/video), PHI in logs |
| Provider/Payer Operations | ~40 | Member rosters, eligibility/claims feeds from health plans |
| People / HR | ~10 | Employee SSNs, payroll, offer letters |

**Defining persona:** the **Iris oncology nurse** (RN, OCN), who coordinates a patient's
care with a social worker and peer mentor and is the protagonist of the care-team
surface — exactly where cancer + mental-health PHI escapes into prose.

## 3. Integration / tooling surfaces → carriers
Likely stack for a HIPAA health-tech: AWS (PHI data stores), their own platform
(OneUM/Iris app + DB), Snowflake/warehouse for analytics, payer integrations
(eligibility/claims feeds), Salesforce/Zendesk for support, Slack or Teams internal,
Google Workspace/M365, Twilio/Zoom for telehealth, secure fax/email for PA intake. In
scope (6–7 surfaces):
- **Secure email / fax intake** — PA request packet *(lead)*.
- **Slack** — Iris care-team coordination.
- **Payer integration / Snowflake** — member roster export.
- **Confluence / Drive** — clinical PA-criteria library.
- **Drive (analytics)** — de-identified research export.
- **GitHub** — platform `.env` with PHI-DB + telehealth keys.
- **Drive (HR)** — employee master.

## 4. False-positive concerns → near-misses (lead with work-product ones)
- **ICD-10 codes + drug names in the clinical criteria library** *(most resonant — their
  work product)*: a criteria/guideline document is *supposed* to list C50.911, C34.90,
  pembrolizumab, etc. Naive code-matching flags it as PHI → alert fatigue. The right
  answer is context-aware PHI detection that stays quiet when there's no patient.
- **Health-plan member / claim numbers shaped like SSNs** (`NNN-NN-NNNN`) — internal
  identifiers that a naive detector calls an SSN.
- **De-identified / study-subject IDs** in analytics work product that look patient-ish.
- **Placeholder / example API keys** in platform config.

## 5. False-negative concerns → evasion variants
- **PHI in clinician/peer-mentor free text** (Iris chat, care notes) — cancer +
  mental-health described in prose, no labeled field. *(the recall crown jewel.)*
- **Identifier + diagnosis split across adjacent sentences** in a clinical note.
- **MRN / member ID spaced or dashed**; **SSN with spaces** on a faxed intake.
- **Genomic results in prose** ("patient is BRCA1-positive, stage III") — no token a
  regex recognizes.

## 6. Demo narrative
Open on the crown jewel: a **prior-auth packet** emailed in from an external oncology
practice — a named patient, DOB, member ID, **stage IV breast cancer (C50.911)**, a
**BRCA1-positive** result, a **pembrolizumab** regimen, and a free-text clinical note.
That single message is the most damaging breach OncoHealth could suffer. Then the
**Iris care-team Slack**, where a nurse and a peer mentor discuss the same patient's
**anxiety and prognosis** in prose — and Nightfall's **context-aware PHI detector
catches it** where a regex never could (recall). Then turn the precision story:
point the same detector at the **clinical criteria library** — dense with the *same*
ICD-10 codes and drugs — and it **stays quiet**, because there's no patient; a naive
code-matcher would have flooded the team. Close on the **gaps**: genomic markers, MRNs,
and member IDs that off-the-shelf detectors miss, and a **"de-identified" research
export** with one residual identifier that quietly turns it back into PHI. The spine:
*protect cancer-patient PHI — diagnosis, genome, and mental health — across the packets,
chats, and exports where it actually moves, with the context to tell a real patient from
a clinical guideline.*
