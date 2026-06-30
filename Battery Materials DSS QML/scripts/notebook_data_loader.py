from pathlib import Path

import pandas as pd


def load_presentation_data(project_folder):
    processed_folder = Path(project_folder) / "data" / "processed"

    def load_csv(file_name):
        return pd.read_csv(processed_folder / file_name)

    lithium_scored_dataframe = load_csv("lithium india scored.csv")
    final_shortlist_dataframe = load_csv("final india battery shortlist.csv")
    dss_family_ranking_dataframe = load_csv(
        "dss battery family recommendation ranking.csv"
    )
    dss_compound_ranking_dataframe = load_csv("dss compound recommendation ranking.csv")
    dss_material_ranking_dataframe = dss_compound_ranking_dataframe.copy()
    qml_ready_dataframe = load_csv("qml_ready_lithium_india.csv")
    qml_predictions_dataframe = load_csv("qml baseline predictions.csv")
    tuned_qml_predictions_dataframe = load_csv("qml tuned best predictions.csv")
    qml_exhaustive_results_dataframe = load_csv(
        "qml exhaustive feature combination results.csv"
    )
    qml_exhaustive_top_results_dataframe = load_csv(
        "qml exhaustive feature combination top results.csv"
    )
    qml_exhaustive_best_result = qml_exhaustive_top_results_dataframe.iloc[0]
    improved_qml_dataset_dataframe = load_csv("improved qml feature pca.csv")
    improved_qml_tuning_results_dataframe = load_csv("improved qml tuning results.csv")
    improved_qml_predictions_dataframe = load_csv("improved qml best predictions.csv")
    improved_qml_threshold_results_dataframe = load_csv(
        "improved qml threshold results.csv"
    )
    improved_qml_threshold_predictions_dataframe = load_csv(
        "improved qml threshold predictions.csv"
    )
    improved_qml_alignment_scores_dataframe = load_csv(
        "improved qml alignment scores.csv"
    )
    improved_qml_alignment_results_dataframe = load_csv(
        "improved qml alignment results.csv"
    )
    improved_qml_alignment_predictions_dataframe = load_csv(
        "improved qml alignment predictions.csv"
    )
    best_qml_repeated_split_results_dataframe = load_csv(
        "best qml repeated split results.csv"
    )
    best_qml_repeated_split_predictions_dataframe = load_csv(
        "best qml repeated split predictions.csv"
    )
    qml_vs_logistic_results_dataframe = load_csv(
        "qml vs logistic repeated split results.csv"
    )
    qml_vs_logistic_summary_dataframe = load_csv(
        "qml vs logistic repeated split summary.csv"
    )
    qml_vs_logistic_predictions_dataframe = load_csv(
        "qml vs logistic repeated split predictions.csv"
    )

    dataset_summary = pd.DataFrame(
        [
            get_summary_row("Lithium India scored", lithium_scored_dataframe),
            get_summary_row("Final India shortlist", final_shortlist_dataframe),
            get_summary_row("DSS compound ranking", dss_compound_ranking_dataframe),
            get_summary_row("DSS family context", dss_family_ranking_dataframe),
            get_summary_row("QML-ready dataset", qml_ready_dataframe),
            get_summary_row("QML test predictions", qml_predictions_dataframe),
            get_summary_row(
                "Tuned QML test predictions",
                tuned_qml_predictions_dataframe,
            ),
            get_summary_row(
                "Exhaustive QML tuning results",
                qml_exhaustive_results_dataframe,
            ),
            get_summary_row(
                "Exhaustive QML top results",
                qml_exhaustive_top_results_dataframe,
            ),
            get_summary_row("Improved QML PCA dataset", improved_qml_dataset_dataframe),
            get_summary_row(
                "Improved QML tuning results",
                improved_qml_tuning_results_dataframe,
            ),
            get_summary_row(
                "Improved QML test predictions",
                improved_qml_predictions_dataframe,
            ),
            get_summary_row(
                "Improved QML threshold results",
                improved_qml_threshold_results_dataframe,
            ),
            get_summary_row(
                "Improved QML threshold predictions",
                improved_qml_threshold_predictions_dataframe,
            ),
            get_summary_row(
                "Improved QML alignment scores",
                improved_qml_alignment_scores_dataframe,
            ),
            get_summary_row(
                "Improved QML alignment results",
                improved_qml_alignment_results_dataframe,
            ),
            get_summary_row(
                "Improved QML alignment predictions",
                improved_qml_alignment_predictions_dataframe,
            ),
            get_summary_row(
                "Best QML repeated split results",
                best_qml_repeated_split_results_dataframe,
            ),
            get_summary_row(
                "Best QML repeated split predictions",
                best_qml_repeated_split_predictions_dataframe,
            ),
            get_summary_row("QML vs Logistic results", qml_vs_logistic_results_dataframe),
            get_summary_row("QML vs Logistic summary", qml_vs_logistic_summary_dataframe),
            get_summary_row(
                "QML vs Logistic predictions",
                qml_vs_logistic_predictions_dataframe,
            ),
        ]
    )

    return (
        lithium_scored_dataframe,
        final_shortlist_dataframe,
        dss_family_ranking_dataframe,
        dss_compound_ranking_dataframe,
        dss_material_ranking_dataframe,
        qml_ready_dataframe,
        qml_predictions_dataframe,
        tuned_qml_predictions_dataframe,
        qml_exhaustive_results_dataframe,
        qml_exhaustive_top_results_dataframe,
        qml_exhaustive_best_result,
        improved_qml_dataset_dataframe,
        improved_qml_tuning_results_dataframe,
        improved_qml_predictions_dataframe,
        improved_qml_threshold_results_dataframe,
        improved_qml_threshold_predictions_dataframe,
        improved_qml_alignment_scores_dataframe,
        improved_qml_alignment_results_dataframe,
        improved_qml_alignment_predictions_dataframe,
        best_qml_repeated_split_results_dataframe,
        best_qml_repeated_split_predictions_dataframe,
        qml_vs_logistic_results_dataframe,
        qml_vs_logistic_summary_dataframe,
        qml_vs_logistic_predictions_dataframe,
        dataset_summary,
    )


def get_summary_row(dataset_name, dataframe):
    return {
        "dataset": dataset_name,
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
    }
