from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


LAB3_DIR = Path(__file__).resolve().parent
DATA_PATH = LAB3_DIR.parent / "lab1" / "shoes_normed.csv"
RESULT_PATH = LAB3_DIR / "shoes_kmeans_result.csv"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, header=None)
    df.columns = [f"feature_{idx + 1}" for idx in range(df.shape[1])]
    return df


def evaluate_kmeans(df: pd.DataFrame, min_k: int = 2, max_k: int = 8) -> pd.DataFrame:
    metrics = []
    upper_k = min(max_k, len(df) - 1)

    for k in range(min_k, upper_k + 1):
        model = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = model.fit_predict(df)
        metrics.append(
            {
                "k": k,
                "inertia": model.inertia_,
                "silhouette": silhouette_score(df, labels),
            }
        )

    return pd.DataFrame(metrics)


def main() -> None:
    df = load_data()
    metrics_df = evaluate_kmeans(df)

    best_k = int(metrics_df.sort_values("silhouette", ascending=False).iloc[0]["k"])
    model = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    labels = model.fit_predict(df)

    result_df = df.copy()
    result_df["cluster"] = labels

    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(df)
    result_df["pca_1"] = components[:, 0]
    result_df["pca_2"] = components[:, 1]
    result_df.to_csv(RESULT_PATH, index=False)

    cluster_sizes = result_df["cluster"].value_counts().sort_index()
    cluster_profile = result_df.groupby("cluster").mean(numeric_only=True)
    cluster_feature_diff = (
        cluster_profile.drop(columns=["pca_1", "pca_2"])
        .drop(columns=["cluster"], errors="ignore")
        .max(axis=0)
        .sub(
            cluster_profile.drop(columns=["pca_1", "pca_2"])
            .drop(columns=["cluster"], errors="ignore")
            .min(axis=0)
        )
        .sort_values(ascending=False)
        .head(10)
    )

    print("K-means для shoes_normed.csv")
    print(f"Путь к данным: {DATA_PATH}")
    print(f"Размер датасета: {df.shape[0]} объектов, {df.shape[1]} признаков")
    print()

    print("Метрики качества для разных k:")
    print(metrics_df.round(4).to_string(index=False))
    print()

    print(f"Оптимальное число кластеров по silhouette score: {best_k}")
    print("Размеры кластеров:")
    print(cluster_sizes.to_string())
    print()

    print("Средние значения признаков по кластерам (первые 15 признаков):")
    print(cluster_profile.iloc[:, :15].round(3).to_string())
    print()

    print("Признаки с наибольшими различиями между кластерами:")
    print(cluster_feature_diff.round(3).to_string())
    print()

    print("Краткий анализ результата:")
    print(
        f"- Наилучшее разбиение получилось при k={best_k}, "
        f"silhouette score = {metrics_df['silhouette'].max():.4f}."
    )
    print(
        "- Датасет небольшой и бинарный, поэтому k-means разделил объекты "
        "на несколько компактных групп по сходству признаков."
    )
    print(
        f"- Самый крупный кластер содержит {cluster_sizes.max()} объектов, "
        f"самый маленький - {cluster_sizes.min()} объектов."
    )
    print(
        "- Различия между кластерами видны по средним значениям признаков: "
        "чем выше среднее значение признака в кластере, тем чаще этот признак "
        "встречается у объектов данного кластера."
    )
    print(
        f"- Первые две компоненты PCA объясняют "
        f"{pca.explained_variance_ratio_.sum():.4f} доли дисперсии и могут "
        "использоваться для двумерной визуализации кластеров."
    )
    print()
    print(f"Результат с метками кластеров сохранен в: {RESULT_PATH}")


if __name__ == "__main__":
    main()
