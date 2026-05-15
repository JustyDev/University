
import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import accuracy_score, f1_score, classification_report

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LAB1_DIR   = os.path.join(SCRIPT_DIR, "..", "lab1")
LAB2_DIR   = SCRIPT_DIR

normed = pd.read_csv(os.path.join(LAB1_DIR, "survey_normed.csv"))
feature_cols = [c for c in normed.columns if c.startswith("Q")]
X = normed[feature_cols].values
respondent_ids = normed["respondent_id"].values

Z = linkage(X, method="ward", metric="euclidean")
labels = fcluster(Z, t=3, criterion="maxclust")

labeled_df = normed.copy()
labeled_df["cluster"] = labels
out_labeled = os.path.join(LAB2_DIR, "lab2_labeled.csv")
labeled_df.to_csv(out_labeled, index=False)
print(f"Saved labeled dataset → {out_labeled}")
counts = {int(c): int((labels == c).sum()) for c in np.unique(labels)}
print(f"Cluster distribution: {counts}")

y = labels

models = {
    "Decision Tree": DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=3,
        random_state=42,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=2,
        random_state=42,
    ),
    "GBM": GradientBoostingClassifier(
        n_estimators=200,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.8,
        random_state=42,
    ),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = {}

for name, model in models.items():
    cv_res = cross_validate(
        model, X, y,
        cv=cv,
        scoring=["accuracy", "f1_weighted"],
        return_train_score=False,
    )
    acc_mean = cv_res["test_accuracy"].mean()
    acc_std  = cv_res["test_accuracy"].std()
    f1_mean  = cv_res["test_f1_weighted"].mean()
    f1_std   = cv_res["test_f1_weighted"].std()
    results[name] = dict(
        accuracy_mean=acc_mean, accuracy_std=acc_std,
        f1_mean=f1_mean,        f1_std=f1_std,
    )
    print(f"\n{name}")
    print(f"  CV accuracy  = {acc_mean:.4f} ± {acc_std:.4f}")
    print(f"  CV F1-weighted = {f1_mean:.4f} ± {f1_std:.4f}")

best_name = max(results, key=lambda k: results[k]["accuracy_mean"])
print(f"\nBest model by accuracy: {best_name}")

best_model = models[best_name]
best_model.fit(X, y)

importances = best_model.feature_importances_
feat_imp = pd.DataFrame({"feature": feature_cols, "importance": importances})
feat_imp = feat_imp.sort_values("importance", ascending=False).reset_index(drop=True)
print("\nFeature importances:")
print(feat_imp.to_string(index=False))

feat_imp.to_csv(os.path.join(LAB2_DIR, "lab2_feature_importance.csv"), index=False)

y_pred_full = best_model.predict(X)
print(f"\nClassification report ({best_name}, full data):")
print(classification_report(y, y_pred_full, target_names=["Cluster 1","Cluster 2","Cluster 3"]))

all_model_reports = {}
for name, model in models.items():
    model.fit(X, y)
    y_pred = model.predict(X)
    all_model_reports[name] = {
        "accuracy_cv": results[name]["accuracy_mean"],
        "f1_cv":       results[name]["f1_mean"],
    }

fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#4e79a7" if f in feat_imp["feature"].values[:3] else "#b0bec5"
          for f in feat_imp["feature"]]
ax.barh(feat_imp["feature"], feat_imp["importance"], color=colors)
ax.set_xlabel("Importance")
ax.set_title(f"Feature Importance — {best_name}")
ax.invert_yaxis()
plt.tight_layout()
fig.savefig(os.path.join(LAB2_DIR, "lab2_feature_importance.png"), dpi=120)
plt.close(fig)

fig2, ax2 = plt.subplots(figsize=(7, 4))
names = list(results.keys())
accs  = [results[n]["accuracy_mean"] for n in names]
stds  = [results[n]["accuracy_std"]  for n in names]
ax2.bar(names, accs, yerr=stds, capsize=5, color=["#4e79a7","#f28e2b","#59a14f"])
ax2.set_ylim(0, 1.05)
ax2.set_ylabel("CV Accuracy")
ax2.set_title("Model Accuracy Comparison (5-fold CV)")
plt.tight_layout()
fig2.savefig(os.path.join(LAB2_DIR, "lab2_accuracy_comparison.png"), dpi=120)
plt.close(fig2)

summary = {
    "cluster_counts": counts,
    "results": {k: {kk: float(vv) for kk, vv in v.items()} for k, v in results.items()},
    "best_model": best_name,
    "feature_importance": feat_imp.to_dict(orient="records"),
}
with open(os.path.join(LAB2_DIR, "lab2_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("\nAll outputs saved.")
