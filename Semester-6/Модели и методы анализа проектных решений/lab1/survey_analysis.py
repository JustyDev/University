from __future__ import annotations

import math
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEPS_DIR = BASE_DIR / ".deps"
if DEPS_DIR.exists():
    sys.path.insert(0, str(DEPS_DIR))

import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage

QUESTIONS = [
    {
        "code": "Q1",
        "text": "Как часто вы используете AI-инструменты в разработке?",
        "options": {
            1: "Не использую",
            2: "Редко, для отдельных задач",
            3: "Регулярно несколько раз в неделю",
            4: "Практически ежедневно",
        },
    },
    {
        "code": "Q2",
        "text": "Насколько глубоко AI встроен в ваш рабочий процесс?",
        "options": {
            1: "Не встроен",
            2: "Используется на одном этапе работы",
            3: "Используется на нескольких этапах",
            4: "Покрывает почти весь цикл разработки",
        },
    },
    {
        "code": "Q3",
        "text": "Насколько уверенно вы формулируете запросы к AI?",
        "options": {
            1: "Нет опыта",
            2: "Базовый уровень",
            3: "Уверенный уровень",
            4: "Продвинутый уровень",
        },
    },
    {
        "code": "Q4",
        "text": "Насколько вы доверяете AI-коду после собственной проверки?",
        "options": {
            1: "Почти не доверяю",
            2: "Доверяю только простым фрагментам",
            3: "Доверяю типовым решениям",
            4: "Часто принимаю AI-решение после ревью",
        },
    },
    {
        "code": "Q5",
        "text": "Как ваша команда относится к применению AI?",
        "options": {
            1: "Использование запрещено",
            2: "Отношение нейтральное",
            3: "Использование разрешено и ограниченно регламентировано",
            4: "Использование поощряется",
        },
    },
    {
        "code": "Q6",
        "text": "Насколько технически интегрированы AI-инструменты в вашу среду?",
        "options": {
            1: "Интеграции нет",
            2: "Использую только веб-интерфейсы",
            3: "Есть плагины/расширения в IDE",
            4: "Есть интеграция в IDE и/или командные процессы",
        },
    },
    {
        "code": "Q7",
        "text": "Какой прирост продуктивности вы ощущаете от AI?",
        "options": {
            1: "Почти никакого",
            2: "Небольшой, до 10%",
            3: "Заметный, 10-30%",
            4: "Существенный, более 30%",
        },
    },
    {
        "code": "Q8",
        "text": "Планируете ли вы расширять использование AI в ближайший год?",
        "options": {
            1: "Нет",
            2: "Скорее нет, чем да",
            3: "Скорее да, чем нет",
            4: "Да, планирую активное расширение",
        },
    },
]


def load_responses():
    source_path = BASE_DIR / "survey_responses.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Input file not found: {source_path}")
    return pd.read_csv(source_path, encoding="utf-8-sig")


def validate_response_table(raw_df) -> None:
    expected_columns = ["respondent_id"] + [q["code"] for q in QUESTIONS]
    missing_columns = [column for column in expected_columns if column not in raw_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    for question in QUESTIONS:
        q_code = question["code"]
        invalid_mask = ~raw_df[q_code].isin(question["options"].keys())
        if invalid_mask.any():
            bad_ids = raw_df.loc[invalid_mask, "respondent_id"].tolist()[:10]
            raise ValueError(
                f"Column {q_code} contains values outside 1..4. Example respondent_id values: {bad_ids}"
            )


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return 0.0, 0.0
    phat = successes / total
    denominator = 1 + z**2 / total
    center = (phat + z**2 / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt((phat * (1 - phat) + z**2 / (4 * total)) / total)
        / denominator
    )
    return center - margin, center + margin


def make_labeled_df(raw_df):
    labeled_df = raw_df.copy()
    for question in QUESTIONS:
        labeled_df[question["code"]] = labeled_df[question["code"]].map(question["options"])
    return labeled_df


def normalize_df(raw_df):
    norm_df = raw_df.copy()
    question_codes = [q["code"] for q in QUESTIONS]
    norm_df[question_codes] = (norm_df[question_codes] - 1) / 3
    return norm_df


def build_confidence_table(raw_df):
    rows: list[dict[str, object]] = []
    sample_size = len(raw_df)
    for question in QUESTIONS:
        q_code = question["code"]
        q_text = question["text"]
        for option_code, option_text in question["options"].items():
            count = int((raw_df[q_code] == option_code).sum())
            share = count / sample_size
            left, right = wilson_interval(count, sample_size)
            rows.append(
                {
                    "question_code": q_code,
                    "question_text": q_text,
                    "option_code": option_code,
                    "option_text": option_text,
                    "count": count,
                    "share": round(share, 4),
                    "ci_lower": round(left, 4),
                    "ci_upper": round(right, 4),
                }
            )
    return pd.DataFrame(rows)


def build_cluster_outputs(raw_df, norm_df):
    question_codes = [q["code"] for q in QUESTIONS]
    features = norm_df[question_codes].to_numpy()
    linkage_matrix = linkage(features, method="ward", metric="euclidean")
    clusters = fcluster(linkage_matrix, t=3, criterion="maxclust")

    cluster_assignments = pd.DataFrame(
        {"respondent_id": raw_df["respondent_id"], "cluster": clusters}
    ).sort_values(["cluster", "respondent_id"])

    cluster_profile_source = raw_df.copy()
    cluster_profile_source["cluster"] = clusters
    cluster_profiles = (
        cluster_profile_source.groupby("cluster")[question_codes]
        .agg(["mean", "median"])
        .round(3)
    )
    cluster_profiles.columns = [f"{col[0]}_{col[1]}" for col in cluster_profiles.columns]
    cluster_sizes = cluster_profile_source.groupby("cluster").size().rename("size")
    cluster_profiles = pd.concat([cluster_sizes, cluster_profiles], axis=1).reset_index()

    linkage_df = pd.DataFrame(
        linkage_matrix,
        columns=["cluster_1", "cluster_2", "distance", "sample_count"],
    )
    sorted_distances = sorted(linkage_matrix[:, 2])
    cut_height = float((sorted_distances[-3] + sorted_distances[-2]) / 2)

    return linkage_df, cluster_assignments, cluster_profiles, cut_height


def main() -> None:
    raw_df = load_responses().sort_values("respondent_id").reset_index(drop=True)
    validate_response_table(raw_df)

    labeled_df = make_labeled_df(raw_df)
    norm_df = normalize_df(raw_df)
    confidence_df = build_confidence_table(raw_df)
    linkage_df, cluster_assignments, cluster_profiles, cut_height = build_cluster_outputs(raw_df, norm_df)

    raw_df.to_csv(BASE_DIR / "survey_responses.csv", index=False, encoding="utf-8-sig")
    labeled_df.to_csv(BASE_DIR / "survey_responses_labeled.csv", index=False, encoding="utf-8-sig")
    norm_df.to_csv(BASE_DIR / "survey_normed.csv", index=False, encoding="utf-8-sig")
    confidence_df.to_csv(BASE_DIR / "confidence_intervals.csv", index=False, encoding="utf-8-sig")
    linkage_df.to_csv(BASE_DIR / "linkage_matrix.csv", index=False, encoding="utf-8-sig")
    cluster_assignments.to_csv(BASE_DIR / "cluster_assignments.csv", index=False, encoding="utf-8-sig")
    cluster_profiles.to_csv(BASE_DIR / "cluster_profiles.csv", index=False, encoding="utf-8-sig")

    with pd.ExcelWriter(BASE_DIR / "survey_responses.xlsx", engine="openpyxl") as writer:
        raw_df.to_excel(writer, sheet_name="numeric", index=False)
        labeled_df.to_excel(writer, sheet_name="labeled", index=False)
        confidence_df.to_excel(writer, sheet_name="confidence_intervals", index=False)

    print("Analysis completed.")
    print("Input file: survey_responses.csv")
    print(f"Respondents: {len(raw_df)}")
    print(f"Selected cut height: {cut_height:.6f}")


if __name__ == "__main__":
    main()
