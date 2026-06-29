# Improved QML Step 02: PCA Dataset

Generated on: 2026-06-28

## Output Dataset

`data/processed/improved qml feature pca.csv`

## Purpose

The original QML dataset used hand-selected features. This improved experiment
uses feature importance first, then PCA to compress the strongest features into
small quantum-ready component sets.

## Dataset Size

- Rows: 1,000
- Columns: 14
- PCA components saved: 8

## PCA Explained Variance

| component | explained_variance_ratio | cumulative_explained_variance |
| --- | --- | --- |
| improved_pca_1 | 0.3222 | 0.3222 |
| improved_pca_2 | 0.1349 | 0.4571 |
| improved_pca_3 | 0.1138 | 0.5709 |
| improved_pca_4 | 0.0881 | 0.6590 |
| improved_pca_5 | 0.0763 | 0.7353 |
| improved_pca_6 | 0.0619 | 0.7972 |
| improved_pca_7 | 0.0557 | 0.8528 |
| improved_pca_8 | 0.0434 | 0.8962 |
