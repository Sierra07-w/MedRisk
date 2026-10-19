# Project Proposal — MedRisk: Intelligent Disease Risk Assessment System

**Version:** 1.0 · **Date:** 19 October 2026 · **Stage:** pre-defense 0
**Team:** Muslim Syzdykov (SE-2425), Zarina Kosaman (SE-2429), Sara Mukhammad (SE-2419)
**Supervisor:** Aigerim Bakiyeva · **Program:** 6B06102 Software Engineering

---

## 1. Title

- **ENG:** «Development of an intelligent disease risk assessment system based on medical data analysis»
- **RUS:** «Разработка интеллектуальной системы оценки риска заболеваний на основе анализа медицинских данных»

Working name of the product: **MedRisk**.

## 2. Problem statement

Non-communicable diseases — cardiovascular disease (CVD), type 2 diabetes mellitus (T2D),
their complications — are the leading causes of death globally. WHO attributes roughly
**74 % of all deaths** to non-communicable diseases, with CVD alone accounting for about
17–18 million deaths per year. The decisive risk factors (hypertension, dyslipidaemia,
hyperglycaemia, smoking, obesity, physical inactivity) are **measurable and modifiable long
before the disease manifests**.

In Kazakhstan, as in most middle-income countries, cardiovascular mortality is high and
screening coverage in primary care is uneven. Existing instruments do not close the gap:

1. **Validated clinical scores are clinician-bound.** Framingham, SCORE2/SCORE, QRISK3 and
   Pooled Cohort Equations are well validated, but they are applied inside clinics, use
   population-specific coefficients and rarely reach the person who could act on them.
2. **Consumer "health quizzes" are opaque.** Web and mobile tools that claim to estimate
   disease risk seldom disclose their model, are rarely validated, and do not explain which
   factors drive the result.
3. **ML models are under-evaluated.** Published disease-prediction models frequently lack
   calibration analysis, baseline comparison and external validation (Kelly et al., 2019),
   and hidden bias has been demonstrated in deployed health algorithms (Obermeyer et al., 2019).

**Research/practice gap.** There is no accessible tool for our target users that combines
(a) models validated against clinical baselines, (b) transparent, explainable outputs,
(c) plain-language communication of results, and (d) privacy-conscious design.

## 3. Target users

| Segment | Who | Need |
|---|---|---|
| Primary | Adults 30–70 in KZ / CIS, non-medical background | A quick, trustworthy estimate of CVD / T2D risk and a clear list of modifiable factors |
| Secondary | Primary-care professionals | A structured risk summary they can review during a consultation |
| Internal | Project team / supervisor | Reproducible pipeline for training and evaluating the models |

## 4. Aim

**Aim.** To develop and evaluate a web-based intelligent system that assesses an individual's
10-year risk of cardiovascular disease and type 2 diabetes from questionnaire and clinical
indicators, using machine-learning models that are benchmarked against clinical baselines and
whose outputs are explained in plain language.

## 5. Objectives

| # | Objective | Linked outcomes |
|---|---|---|
| O1 | Collect and prepare public medical datasets (UCI Cleveland, Pima Indians Diabetes, Framingham/NHANES-derived); document quality issues (missing values, imbalance, biases) | Data pipeline + data-quality report |
| O2 | Build baseline models (logistic regression, Framingham-style score) and ML models (gradient boosting) for both targets; evaluate with AUC, calibration, per-group analysis | Trained models + evaluation report |
| O3 | Implement explanation layer (SHAP feature contributions → plain-language text) | Explanation module |
| O4 | Design and implement REST API (FastAPI) and persistence (PostgreSQL) | Running backend + OpenAPI spec |
| O5 | Design and implement the responsive web application (questionnaire → report → history) | Web app + UX evaluation |
| O6 | Verify the system (functional, performance, usability testing) against the requirements and metrics of the verification plan | Verification report |
| O7 | Document the project (architecture, decisions, results) and pass pre-defense stages | This repository + reports |

## 6. Expected outcomes

- Reproducible data pipeline and a documented dataset-quality analysis.
- Models with **ROC-AUC ≥ 0.78** on held-out test data for both targets, calibration curves,
  and comparison against logistic-regression and clinical-score baselines.
- REST API documented via OpenAPI, web application with assessment history and factor explanations.
- Usability check: System Usability Scale ≥ 70 in a small internal user test.
- Full documentation set in this repository, tags `pre-defense-1`, `pre-defense-2`, `final-pre-defense`.

## 7. Project scope

### 7.1 In scope (v1)

- Two risk targets: 10-year CVD risk, T2D risk (separate models, single questionnaire).
- Input: structured health questionnaire (age, sex, blood pressure, cholesterol, glucose/HbA1c,
  BMI, smoking, activity, family history, prior diagnoses).
- ML models trained on **public, de-identified datasets** only.
- Web application (desktop + mobile browsers), REST API, PostgreSQL persistence.
- Explainability: per-feature contribution (SHAP) + plain-language summary.
- Privacy: minimal data collection, hashed credentials, no third-party analytics.

### 7.2 Out of scope (v1)

- Diagnosis, treatment recommendations, triage of acute conditions.
- Integration with EHR/HIS/LIS systems; ingestion of laboratory device data.
- Native mobile applications.
- Real patient data collection and clinical trials; regulatory certification
  (medical-device status).
- LLM-based conversational assistant (studied as an optional extension with strict safeguards).

### 7.3 Constraints

| Constraint | Description |
|---|---|
| Time | Milestones M0–M5, final pre-defense at the end of the diploma period |
| Team | 3 students, part-time (study + work), weekly supervision |
| Data | Only public datasets — limits personalization to their feature sets |
| Ethics | No real personal medical data in v1; educational-use disclaimer in the product |

## 8. Research questions of the diploma

1. Do gradient-boosting models over a short questionnaire outperform logistic regression and a
   Framingham-style clinical score for CVD/T2D risk on public datasets (AUC, calibration)?
2. Do SHAP-based explanations agree with clinically known risk factors (face validity)?
3. Does an explanation-first interface change user trust and comprehension versus a bare score
   (small usability study)?

## 9. Methodology

Iterative (Scrum-like) with two-week milestones, weekly supervisor meetings. Stages:
analysis → data & baselines → models & explanations → backend → frontend → evaluation.
All work items tracked in YouTrack; all changes merged through pull requests with a
second-team-member review.
