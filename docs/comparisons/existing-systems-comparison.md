# Existing System Comparison

**Project:** MedRisk · **Stage:** pre-defense 0 · **Date:** 19 October 2026

Five existing systems were selected: three validated clinical risk calculators (the direct
competitors for the "risk estimation" function), and two consumer health-AI products
(the direct competitors for the "accessible, explainable consumer experience" function).

## 1. Systems under comparison

| ID | System | Type | Notes |
|---|---|---|---|
| S1 | **Framingham / ACC ASCVD Pooled Cohort Equations calculator** | Clinical web calculator | The original validated score (D'Agostino et al., 2008) and its ASCVD adaptation; widely embedded in clinician tools (e.g. MDCalc, ACC tools) |
| S2 | **SCORE2 / SCORE (ESC)** | Clinical web calculator | ESC-endorsed 10-year CVD risk estimation for Europe, region-calibrated (Conroy et al., 2003; SCORE2 working group, 2021) |
| S3 | **QRISK3** | Clinical web calculator | UK QResearch-based, >7 million patients, large feature set (Hippisley-Cox et al., 2017) |
| S4 | **Ada Health (Ada Check & Ada Care)** | Consumer mobile/web app | Symptom checker + health assessment with an AI-driven interview; ~12 M users |
| S5 | **CDC Diabetes Risk Test / Mayo Clinic online risk assessments** | Consumer web quizzes | Simple questionnaires producing a categorical risk level with generic advice |

## 2. Comparison criteria (9)

| # | Criterion | What is compared |
|---|---|---|
| C1 | Target condition(s) | What risk is estimated (CVD, T2D, symptoms, …) |
| C2 | Input data | Questionnaire only vs. required lab values |
| C3 | Model transparency | Is the model/score disclosed and reproducible? |
| C4 | Explainability | Does the user see *why* the risk is what it is? |
| C5 | Evidence & validation | Peer-reviewed validation, cohort size, external validation |
| C6 | Personalization & recalibration | Population-specific coefficients, updates |
| C7 | Accessibility | Free public access, languages, mobile, no installation |
| C8 | Integration (API) | Machine-readable interface for reuse |
| C9 | Privacy posture | Data required to get a result; retention |

## 3. Comparison matrix

| Criterion | S1 Framingham/ASCVD | S2 SCORE2 | S3 QRISK3 | S4 Ada Health | S5 CDC/Mayo quizzes | **MedRisk (target)** |
|---|---|---|---|---|---|---|
| C1 Targets | CVD only | Fatal CVD only | CVD (incl. AF/stroke) | Symptom triage + broad assessments | T2D (CDC) / mixed (Mayo) | **CVD + T2D, one questionnaire** |
| C2 Inputs | Needs TC, HDL, SBP, treatment, smoking, diabetes, age, sex | Same + country calibration | Large set incl. medications, comorbidities, ethnicity | Free-text symptoms + basic questions | 7 plain questions | **Plain questionnaire + optional lab values** |
| C3 Transparency | Formula published, coefficients public | Published, country tables public | Published (BMJ), coefficients public | Proprietary, closed model | Undisclosed scoring | **Open model card; algorithm & metrics published in repo** |
| C4 Explainability | No (score only) | No | Partial (risk factors listed, no per-user attribution) | Generic text answers, no model attribution | No | **Per-factor SHAP attribution + plain-language text** |
| C5 Validation | Peer-reviewed, US cohort | Peer-reviewed, 12+ EU cohorts | Peer-reviewed, >7 M patients, external validation | Limited published validation | Not peer-reviewed as a model | **Reproducible evaluation vs. baselines on public datasets; per-group metrics** |
| C6 Personalization | US coefficients; needs external recalibration | Country-calibrated tables | UK-calibrated, interaction terms | Conversation-driven, adapts questions | None | **Planned: calibration analysis + documented limits; retraining pipeline** |
| C7 Accessibility | Web, free, EN | Web, free, EN | Web, free, EN | App (iOS/Android), EN + major EU languages | Web, free, EN | **Responsive web, EN + KZ/RU planned** |
| C8 Integration | No official API | No official API | No official API | Closed/partner API only | No API | **Public REST API + OpenAPI spec** |
| C9 Privacy | User enters data, no account | Same | Same (via NHS login for GPs) | Account + conversation history stored | No account | **Guest mode, minimal data, hashed credentials, no ads/analytics** |

## 4. Why the proposed solution is needed (evidence-based)

1. **Combination gap.** S1–S3 are validated and transparent but clinician-bound, single-target,
   and give the user no personal attribution ("why is my risk high?"). S4–S5 are accessible
   but opaque (C3) and weakly validated (C5). No system in the sample combines high C3+C4+C5
   with C7.
2. **Explainability gap.** Only QRISK3 even lists contributing risk factors; none of the five
   computes a per-user attribution. Per Obermeyer et al. (2019), opacity in population-health
   algorithms directly produces inequitable outcomes — per-user attribution plus subgroup
   metrics is a requirement, not a feature.
3. **Integration gap.** No system offers a documented API; clinicians and public-health apps
   cannot reuse their estimates (Kelly et al., 2019 — the "last mile" integration problem).
4. **Scope realism.** The comparison also justifies *narrowing*: we do not compete with QRISK3
   on cohort scale; we compete on accessibility, explainability, dual-target coverage and an
   open, reproducible evaluation — feasible for a 3-person, 1-semester project.
5. **Benchmarking.** S1–S3 provide clinically meaningful baselines; the verification plan
   requires our models to be compared against a Framingham-style score computed on the same
   data (see [verification plan](../verification/verification-and-evaluation-plan.md), §4).

*Justification of sample size:* the diploma requirement asks for 3–5 systems; five were
compared — all three dominant validated CVD scores plus the two best-known consumer products,
which together cover both halves of the functional space MedRisk enters.

## 5. References used for this comparison

- D'Agostino et al., *Circulation* 2008 (S1) · Conroy et al., *Eur Heart J* 2003 (S2)
- SCORE2 working group, *Eur Heart J* 2021 (S2) · Hippisley-Cox et al., *BMJ* 2017 (S3)
- Ada Health public documentation & app store listings, accessed October 2026 (S4)
- CDC Diabetes Risk Test; Mayo Clinic online assessments, accessed October 2026 (S5)
