import shap
import matplotlib.pyplot as plt


def plot_dependence(shap_values, X, feature_name, save_path=None):
    """
    SHAP dependence plot for nonlinear analysis.
    """

    shap.dependence_plot(
        feature_name,
        shap_values,
        X,
        show=False
    )

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()