# Literature Review — Intelligent Disease Risk Assessment

**Project:** MedRisk · **Stage:** pre-defense 0 · **Date:** 19 October 2026
**Sources used:** 18 (13 scientific publications, 5 grey/primary-data sources)
**Core recency:** 14 of 18 sources are from 2017–2024; foundational works from 1988–2008 are
retained where they are the origin of the clinical scores used as baselines.

---

## 1. Scope of the review

The review answers three questions that directly shape the project:
(1) what approaches exist for estimating cardiovascular and diabetes risk;
(2) what is already known about ML-based disease prediction, its limits and failure modes;
(3) which limitations MedRisk must take into account by design.

## 2. Clinical risk scores — the classical baseline

**Framingham Risk Score.** D'Agostino et al. (2008) derived a general cardiovascular profile
for the Framingham Heart Study cohort, converting age, sex, total/HDL cholesterol, blood
pressure, treatment, smoking and diabetes into a 10-year risk. It is one of the most cited
baselines in the field, but its coefficients were fitted on a US (predominantly white) cohort,
and recalibration for other populations is a known requirement.

**SCORE / SCORE2.** Conroy et al. (2003) built the European SCORE project to estimate
10-year risk of *fatal* cardiovascular events using data from 12 European cohorts, with
country-specific calibration. SCORE2 (SCORE2 working group, 2021) extended this to
non-fatal + fatal events with recalibrated models for low-, moderate- and high-risk European
regions. SCORE-family models demonstrate the field's consensus that **population calibration
matters** — a lesson directly applied in our evaluation (we report calibration, not only AUC).

**QRISK.** Hippisley-Cox et al. (2007) derived QRISK for the UK population with a Cox model,
explicitly addressing underestimation of risk in deprived populations; QRISK3 (Hippisley-Cox
et al., 2017) added many variables (e.g., atypical antipsychotics, corticosteroids, severe
mental illness, migraine, erectile dysfunction, sleep apnoea) and ethnic-group interactions,
and was validated on >7 million patients. QRISK3 shows the modern direction of clinical
scores: **more features, explicit fairness/interaction terms, large validation cohorts**.

**Limitations of clinical scores relevant to this project:** linear/proportional-hazards
assumptions; fixed feature sets; cohort- and country-specific coefficients; dependence on
laboratory values that a lay user may not have; they are not designed to explain themselves
to the patient.

## 3. Machine learning for disease risk prediction

**Foundational datasets.** Two datasets remain the workhorses of the field and are the planned
training data for MedRisk: the **Cleveland heart-disease database** (Detrano et al., 1989),
where a probability algorithm was validated via coronary angiography, and the **Pima Indians
diabetes dataset** (Smith et al., 1988), one of the earliest applications of the ADAP learning
algorithm to forecasting diabetes onset. Both have documented limitations (small size, single
population, measurement noise) which we treat in the data-quality report.

**Deep learning on EHR.** Rajkomar et al. (2018) showed that deep models trained on
electronic health records (FHIR-formatted) match or exceed clinical scores for several
endpoints, and — importantly for engineering design — that models can be retrained cheaply
("gluon" pipeline). This supports our choice of a **retraining-ready pipeline** rather than a
static scoring table.

**Reviews of the field.** Miotto et al. (2018) review deep learning for healthcare and
conclude that representation learning over raw clinical data yields gains, but that
**interpretability and data quality are the main bottlenecks**. Litjens et al. (2017) survey
deep learning in medical image analysis and report the same pattern for imaging: performance
gains are real, yet external validation and workflow integration lag behind. Esteva et al.
(2017) and Gulshan et al. (2016) are landmark examples of task-specific systems reaching
specialist-level performance (skin cancer, diabetic retinopathy) — but both are
narrow-task systems with curated inputs, not population-risk tools; they show what
well-scoped problems achieve and justify our deliberately narrow scope (two endpoints).

## 4. Bias, explainability and clinical safety

Obermeyer et al. (2019) demonstrated that a widely used population-health algorithm used
*healthcare cost* as a proxy for *health needs*, systematically under-serving Black patients.
The lesson: **the choice of prediction target and features is an ethical decision**, and
subgroup analysis is mandatory. Our evaluation plan therefore requires per-group metric
reporting and an explicit discussion of proxy targets.

Lundberg & Lee (2017) introduced SHAP (SHapley Additive exPlanations), a unified, theoretically
grounded method for attributing model output to input features. SHAP is the planned explanation
mechanism in MedRisk: it is model-agnostic, per-prediction, and its global aggregation lets us
perform the face-validity check against clinical knowledge (research question 2 of the diploma).

Topol (2019) describes "high-performance medicine" as the convergence of human judgement and
AI, with the clinician supervising. Kelly et al. (2019) catalogue the challenges of delivering
clinical impact with AI: dataset shift, automation bias, lack of prospective evaluation,
regulatory hurdles, and the "last-mile" integration problem. Char et al. (2018) analyse the
barriers to implementing ML in health care, including rapid obsolescence of models and the
need for new regulatory pathways (see also the FDA's Clinical Decision Support Software
guidance, 2022, which defines when such software is regulated).

The WHO (2021) *Ethics and governance of artificial intelligence for health* sets six principles:
autonomy, well-being, safety, transparency, accountability, equity. MedRisk maps each of these
to a concrete design decision (see [requirements](../requirements/requirements-specification.md),
NFR-6…NFR-10).

## 5. Synthesis — what already exists and what is missing

| # | Established knowledge | Consequence for MedRisk |
|---|---|---|
| 1 | Validated linear clinical scores exist for CVD (Framingham, SCORE2, QRISK3) | Use a Framingham-style score as a **required baseline**, not as the product |
| 2 | Gradient boosting/NN models often outperform linear scores on the same inputs | Compare logistic regression vs LightGBM on identical features; report paired CIs |
| 3 | Population calibration and target choice determine real-world usefulness | Report calibration (Brier, calibration curves); pick hard clinical endpoints |
| 4 | SHAP provides accepted post-hoc explanations | SHAP per-prediction explanations + plain-language rendering |
| 5 | Main failures of deployed health AI: dataset shift, bias, opaque "black boxes", poor usability | Subgroup metrics, dataset documentation, disclaimers, human-in-the-loop framing, usability testing |
| 6 | Small legacy datasets (Cleveland, Pima) have known limitations | Document limitations; plan external validation if time permits; avoid overclaiming |

**Gap addressed by the project.** Existing consumer tools do not combine validated-model
comparison, explainability and plain-language UX in one accessible product; clinical scores
are not consumer-facing. MedRisk occupies this gap for a deliberately narrow, well-evaluated
scope.

## 6. Structured analysis table of publications

| # | Source | Type | Year | Used for (project aspect) | Key finding taken into account |
|---|---|---|---|---|---|
| 1 | D'Agostino et al., *Circulation* 117(6):743–753 | Scientific (journal) | 2008 | Baseline clinical score (Framingham) | Linear score, US cohort → needs recalibration elsewhere |
| 2 | Conroy et al., *Eur Heart J* 24(11):987–1003 | Scientific (journal) | 2003 | Baseline (SCORE, fatal CVD) | Country calibration; endpoint definition matters |
| 3 | SCORE2 working group, *Eur Heart J* 42(25):2439–2454 | Scientific (journal) | 2021 | Baseline (SCORE2), calibration practice | Region-specific recalibration of risk models |
| 4 | Hippisley-Cox et al., *BMJ* 335:136 | Scientific (journal) | 2007 | Baseline (QRISK) | Cox model; fairness for deprived groups |
| 5 | Hippisley-Cox & Brindle, *BMJ* 357:j2099 | Scientific (journal) | 2017 | Baseline (QRISK3) | Large validation; many features; interaction terms |
| 6 | Detrano et al., *Am J Cardiol* 63(13):885–890 | Scientific (journal) | 1989 | CVD dataset provenance (Cleveland/UCI) | Dataset origin, angiography-verified labels, small N |
| 7 | Smith et al., *Proc Annu Symp Comput Appl Med Care* | Scientific (proceedings) | 1988 | T2D dataset provenance (Pima/UCI) | Dataset origin, single-population bias |
| 8 | Rajkomar et al., *npj Digit Med* 1:18 | Scientific (journal) | 2018 | ML feasibility on structured health data | Deep models ≥ clinical scores; retrainable pipelines |
| 9 | Miotto et al., *Brief Bioinform* 19(6):1236–1246 | Scientific (review) | 2018 | ML approaches & limitations | Interpretability & data quality are bottlenecks |
| 10 | Litjens et al., *Med Image Anal* 42:60–88 | Scientific (survey) | 2017 | ML landscape & validation gap | External validation lags performance gains |
| 11 | Esteva et al., *Nature* 542(7639):115–118 | Scientific (journal) | 2017 | Scope discipline precedent (narrow task) | Specialist-level results require narrow, curated tasks |
| 12 | Gulshan et al., *JAMA* 316(22):2402–2410 | Scientific (journal) | 2016 | Validation methodology precedent | Large prospective validation design |
| 13 | Obermeyer et al., *Science* 366(6464):447–453 | Scientific (journal) | 2019 | Bias / proxy targets; subgroup analysis | Target-variable choice is an ethical decision |
| 14 | Lundberg & Lee, *NeurIPS 30* | Scientific (proceedings) | 2017 | Explainability method (SHAP) | Unified attribution; used for explanations + face validity |
| 15 | Topol, *Nat Med* 25(1):44–56 | Scientific (review) | 2019 | Human-in-the-loop framing, UX implications | AI augments, does not replace, the decision-maker |
| 16 | Kelly et al., *BMC Med* 17(1):195 | Scientific (journal) | 2019 | Deployment challenges → risks & NFRs | Dataset shift, automation bias, integration "last mile" |
| 17 | Char et al., *NEJM* 378(11):981–983 | Scientific (journal) | 2018 | Regulatory/implementation barriers | Models age quickly; need monitoring & governance |
| 18 | WHO, *Ethics and governance of AI for health* | Grey (international org.) | 2021 | Ethics requirements NFR-6…NFR-10 | Six principles mapped to design decisions |
| — | FDA, *Clinical Decision Support Software* guidance | Grey (regulatory) | 2022 | Scope boundary (non-device CDS) | Positioning as decision support, not diagnosis |
| — | UCI ML Repository (Heart Disease, Diabetes) | Grey (primary data) | ongoing | Training data | Licensing, documentation, known limitations |
| — | WHO fact sheets: cardiovascular diseases / diabetes | Grey (statistics) | 2024 | Motivation, problem statement | Epidemiological justification of the topic |

## 7. Conclusion

The literature supports the technical feasibility of ML-based cardiometabolic risk estimation
and, at the same time, defines a clear set of obligations: benchmark against clinical scores,
report calibration and subgroup behaviour, provide explanations, keep the scope narrow, keep
a human in the loop, and document data limitations. These obligations are directly encoded in
MedRisk's [requirements](../requirements/requirements-specification.md),
[architecture](../architecture/architecture-description.md) and
[verification plan](../verification/verification-and-evaluation-plan.md).
