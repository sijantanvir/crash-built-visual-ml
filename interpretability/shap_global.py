import shap
import pandas as pd
import matplotlib.pyplot as plt


def compute_shap_values(model, X: pd.DataFrame):
    """
    Compute SHAP values using TreeExplainer.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    return shap_values


def plot_global_importance(shap_values, X: pd.DataFrame, save_path=None):
    """
    Global feature importance (summary plot).
    """
    shap.summary_plot(shap_values, X, show=False)

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()