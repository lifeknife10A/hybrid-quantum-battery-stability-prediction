# Improved QML Step 02: PCA Dataset

Generated on: 2026-07-04

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
| improved_pca_1 | 0.3223 | 0.3223 |
| improved_pca_2 | 0.1320 | 0.4543 |
| improved_pca_3 | 0.1175 | 0.5718 |
| improved_pca_4 | 0.0804 | 0.6522 |
| improved_pca_5 | 0.0692 | 0.7214 |
| improved_pca_6 | 0.0599 | 0.7813 |
| improved_pca_7 | 0.0523 | 0.8336 |
| improved_pca_8 | 0.0439 | 0.8775 |
