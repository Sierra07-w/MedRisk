# ML pipeline (planned from milestone M1)

```
ml/pipeline/   # download, clean, impute, encode, split (seeded)
ml/train/      # baseline (logistic regression), LightGBM training, tuning
ml/evaluate/   # metrics, calibration, subgroup analysis, plots
ml/reports/    # committed machine-readable results (JSON + figures)
```

Training data: public datasets only (UCI Cleveland Heart Disease, Pima Indians Diabetes).
Raw and processed data are **not committed** (see `.gitignore`); reproducible download
scripts will live in `data/`.
