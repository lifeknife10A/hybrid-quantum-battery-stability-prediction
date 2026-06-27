from pathlib import Path
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


project_folder = Path(__file__).resolve().parents[1]
local_package_folder = project_folder / ".python_packages"

if local_package_folder.exists():
    sys.path.insert(0, str(local_package_folder))

if sys.platform == "darwin":
    libomp_folder = Path(
        "/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/"
        "site-packages/sklearn/.dylibs"
    )

    current_library_path = os.environ.get("DYLD_LIBRARY_PATH", "")

    if libomp_folder.exists() and str(libomp_folder) not in current_library_path:
        if current_library_path:
            os.environ["DYLD_LIBRARY_PATH"] = (
                str(libomp_folder) + os.pathsep + current_library_path
            )
        else:
            os.environ["DYLD_LIBRARY_PATH"] = str(libomp_folder)

        os.execv(sys.executable, [sys.executable] + sys.argv)

from xgboost import XGBClassifier
from xgboost import XGBRegressor


processed_folder = project_folder / "data" / "processed"
metadata_folder = project_folder / "data" / "metadata"
model_folder = project_folder / "data" / "models"

input_csv_path = processed_folder / "lithium india scored.csv"
prediction_output_path = processed_folder / "xgboost predictions with india scores.csv"
result_markdown_path = metadata_folder / "xgboost_baseline_results.md"
classifier_model_path = model_folder / "xgboost_stability_classifier.json"
regressor_model_path = model_folder / "xgboost_energy_above_hull_regressor.json"

random_state = 42
test_size = 0.20

base_feature_columns = [
    "space_group_number",
    "band_gap",
    "is_metal",
    "theoretical",
    "deprecated",
    "number_of_elements",
    "has_o",
    "has_fe",
    "has_p",
    "has_mn",
    "has_co",
    "has_ni",
    "has_ti",
    "has_c",
    "has_si",
    "has_s",
    "has_al",
    "has_la",
    "has_zr",
    "has_f",
    "has_cu",
    "has_high_caution_element",
]

categorical_feature_columns = [
    "crystal_system",
    "battery_family",
]

boolean_feature_columns = [
    "is_metal",
    "theoretical",
    "deprecated",
    "has_o",
    "has_fe",
    "has_p",
    "has_mn",
    "has_co",
    "has_ni",
    "has_ti",
    "has_c",
    "has_si",
    "has_s",
    "has_al",
    "has_la",
    "has_zr",
    "has_f",
    "has_cu",
    "has_high_caution_element",
]

columns_kept_for_predictions = [
    "material_id",
    "formula",
    "crystal_system",
    "battery_family",
    "is_stable",
    "energy_above_hull",
    "band_gap",
    "india_feasibility_score",
    "india_decision_label",
    "india_rule_reason",
]


def check_required_columns(dataframe):
    required_columns = (
        base_feature_columns
        + categorical_feature_columns
        + [
            "material_id",
            "formula",
            "is_stable",
            "energy_above_hull",
            "india_feasibility_score",
            "india_decision_label",
            "india_rule_reason",
        ]
    )

    missing_columns = []

    for column_name in required_columns:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Input file is missing required columns: {missing_text}")


def create_feature_table(dataframe):
    feature_dataframe = dataframe[base_feature_columns + categorical_feature_columns].copy()

    for column_name in boolean_feature_columns:
        feature_dataframe[column_name] = feature_dataframe[column_name].map(
            {
                True: 1,
                False: 0,
                "True": 1,
                "False": 0,
                "true": 1,
                "false": 0,
            }
        )

    for column_name in base_feature_columns:
        feature_dataframe[column_name] = pd.to_numeric(
            feature_dataframe[column_name],
            errors="coerce",
        )

    feature_dataframe = pd.get_dummies(
        feature_dataframe,
        columns=categorical_feature_columns,
        dummy_na=True,
        dtype=int,
    )

    return feature_dataframe


def train_classifier(feature_dataframe, dataframe):
    target = dataframe["is_stable"].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        feature_dataframe,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )

    classifier = XGBClassifier(
        n_estimators=250,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.90,
        colsample_bytree=0.90,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=random_state,
        n_jobs=4,
    )

    classifier.fit(x_train, y_train)

    predicted_labels = classifier.predict(x_test)
    predicted_probabilities = classifier.predict_proba(x_test)[:, 1]

    accuracy = accuracy_score(y_test, predicted_labels)
    report = classification_report(
        y_test,
        predicted_labels,
        target_names=["unstable", "stable"],
        zero_division=0,
    )

    return classifier, accuracy, report, predicted_probabilities


def train_regressor(feature_dataframe, dataframe):
    usable_rows = dataframe["energy_above_hull"].notna()
    filtered_features = feature_dataframe.loc[usable_rows].copy()
    target = dataframe.loc[usable_rows, "energy_above_hull"].copy()

    x_train, x_test, y_train, y_test = train_test_split(
        filtered_features,
        target,
        test_size=test_size,
        random_state=random_state,
    )

    regressor = XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.90,
        colsample_bytree=0.90,
        objective="reg:squarederror",
        random_state=random_state,
        n_jobs=4,
    )

    regressor.fit(x_train, y_train)

    predicted_values = regressor.predict(x_test)

    mean_absolute_error_value = mean_absolute_error(y_test, predicted_values)
    root_mean_squared_error_value = np.sqrt(mean_squared_error(y_test, predicted_values))
    r2_value = r2_score(y_test, predicted_values)

    return (
        regressor,
        len(filtered_features),
        mean_absolute_error_value,
        root_mean_squared_error_value,
        r2_value,
    )


def add_predictions(dataframe, feature_dataframe, classifier, regressor):
    output_dataframe = dataframe[columns_kept_for_predictions].copy()

    output_dataframe["predicted_stable_probability"] = classifier.predict_proba(
        feature_dataframe
    )[:, 1]
    output_dataframe["predicted_is_stable"] = classifier.predict(feature_dataframe).astype(
        bool
    )
    output_dataframe["predicted_energy_above_hull"] = regressor.predict(feature_dataframe)

    output_dataframe["final_recommendation_score"] = (
        output_dataframe["predicted_stable_probability"] * 60
        + (output_dataframe["india_feasibility_score"] / 100) * 40
    ).round(2)

    output_dataframe = output_dataframe.sort_values(
        by=[
            "final_recommendation_score",
            "predicted_stable_probability",
            "india_feasibility_score",
        ],
        ascending=[False, False, False],
    )

    return output_dataframe


def get_feature_importance_table(model, feature_columns, number_of_features):
    importance_dataframe = pd.DataFrame(
        {
            "feature": feature_columns,
            "importance": model.feature_importances_,
        }
    )

    importance_dataframe = importance_dataframe.sort_values(
        by="importance",
        ascending=False,
    )

    return importance_dataframe.head(number_of_features)


def dataframe_to_markdown(dataframe):
    if dataframe.empty:
        return "_No rows found._"

    headers = list(dataframe.columns)
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for _, row in dataframe.iterrows():
        row_values = []
        for column_name in headers:
            value = row[column_name]
            if pd.isna(value):
                value_text = ""
            else:
                value_text = str(value)
            row_values.append(value_text.replace("|", "/"))
        lines.append("| " + " | ".join(row_values) + " |")

    return "\n".join(lines)


def write_results(
    dataframe,
    feature_dataframe,
    classifier_accuracy,
    classifier_report,
    regression_row_count,
    regression_mae,
    regression_rmse,
    regression_r2,
    classifier,
    regressor,
    prediction_dataframe,
):
    classifier_importance = get_feature_importance_table(
        classifier,
        list(feature_dataframe.columns),
        15,
    )
    regressor_importance = get_feature_importance_table(
        regressor,
        list(feature_dataframe.columns),
        15,
    )

    top_india_recommendations = prediction_dataframe[
        prediction_dataframe["india_decision_label"].isin(
            ["Recommend", "Research Candidate"]
        )
    ].head(20)

    top_columns = [
        "material_id",
        "formula",
        "battery_family",
        "india_decision_label",
        "india_feasibility_score",
        "predicted_stable_probability",
        "predicted_energy_above_hull",
        "final_recommendation_score",
    ]

    result_text = f"""# XGBoost Baseline Results

Input file: `data/processed/lithium india scored.csv`

Prediction output: `data/processed/xgboost predictions with india scores.csv`

## Problem

Train on all lithium materials first, then use India feasibility columns after
prediction for filtering and ranking.

## Dataset

- Rows used for classification: {len(dataframe):,}
- Rows used for regression: {regression_row_count:,}
- Feature columns after one-hot encoding: {len(feature_dataframe.columns):,}
- Test size: {test_size}
- Random state: {random_state}

## Training Features

The model uses formula-derived, crystal, and basic property columns. It does not
train on `india_feasibility_score`, `india_decision_label`, `energy_above_hull`
for classification, or `is_stable` for regression.

Base features:

{chr(10).join([f"- `{column_name}`" for column_name in base_feature_columns + categorical_feature_columns])}

## Classification Target: `is_stable`

- Model: `XGBClassifier`
- Accuracy: {classifier_accuracy:.4f}

```text
{classifier_report}
```

## Regression Target: `energy_above_hull`

- Model: `XGBRegressor`
- Mean absolute error: {regression_mae:.4f}
- Root mean squared error: {regression_rmse:.4f}
- R2 score: {regression_r2:.4f}

## Top Classifier Features

{dataframe_to_markdown(classifier_importance)}

## Top Regressor Features

{dataframe_to_markdown(regressor_importance)}

## Top India-Friendly Predictions

{dataframe_to_markdown(top_india_recommendations[top_columns])}

## Notes

- This is a baseline model, not the final model.
- The India columns are applied after prediction so the model still learns from
  all lithium families.
- The output file can be used to inspect predicted stable materials and then
  shortlist India-friendly candidates.
"""

    metadata_folder.mkdir(parents=True, exist_ok=True)
    result_markdown_path.write_text(result_text, encoding="utf-8")


def main():
    if not input_csv_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_csv_path}")

    dataframe = pd.read_csv(input_csv_path)
    check_required_columns(dataframe)

    feature_dataframe = create_feature_table(dataframe)

    classifier, classifier_accuracy, classifier_report, _ = train_classifier(
        feature_dataframe,
        dataframe,
    )
    (
        regressor,
        regression_row_count,
        regression_mae,
        regression_rmse,
        regression_r2,
    ) = train_regressor(feature_dataframe, dataframe)

    prediction_dataframe = add_predictions(
        dataframe,
        feature_dataframe,
        classifier,
        regressor,
    )

    processed_folder.mkdir(parents=True, exist_ok=True)
    metadata_folder.mkdir(parents=True, exist_ok=True)
    model_folder.mkdir(parents=True, exist_ok=True)

    prediction_dataframe.to_csv(prediction_output_path, index=False)
    classifier.save_model(classifier_model_path)
    regressor.save_model(regressor_model_path)

    write_results(
        dataframe,
        feature_dataframe,
        classifier_accuracy,
        classifier_report,
        regression_row_count,
        regression_mae,
        regression_rmse,
        regression_r2,
        classifier,
        regressor,
        prediction_dataframe,
    )

    print(f"Rows used for classification: {len(dataframe):,}")
    print(f"Rows used for regression: {regression_row_count:,}")
    print(f"Classifier accuracy: {classifier_accuracy:.4f}")
    print(f"Regression MAE: {regression_mae:.4f}")
    print(f"Regression RMSE: {regression_rmse:.4f}")
    print(f"Regression R2: {regression_r2:.4f}")
    print(f"Predictions saved: {prediction_output_path}")
    print(f"Results saved: {result_markdown_path}")


if __name__ == "__main__":
    main()
