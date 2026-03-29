import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def cluster_shap_values(shap_values, n_clusters=3, random_state=42):
    """
    Perform K-means clustering on SHAP values.
    """

    if isinstance(shap_values, list):
        shap_values = shap_values[1]  # binary classification case

    scaler = StandardScaler()
    shap_scaled = scaler.fit_transform(shap_values)

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans.fit_predict(shap_scaled)

    return labels, kmeans


def attach_clusters(df: pd.DataFrame, labels):
    """
    Attach cluster labels to dataset.
    """
    df = df.copy()
    df["cluster"] = labels
    return df


def compute_cluster_summary(df: pd.DataFrame, shap_values):
    """
    Compute mean SHAP value per cluster.
    """

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    shap_df = pd.DataFrame(shap_values, columns=df.columns.drop("cluster"))
    shap_df["cluster"] = df["cluster"].values

    summary = shap_df.groupby("cluster").mean()
    return summary