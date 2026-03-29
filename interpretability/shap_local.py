import shap
import matplotlib.pyplot as plt


def plot_local_explanation(model, X, index: int, save_path=None):
    """
    Explain a single prediction.
    """

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    shap.force_plot(
        explainer.expected_value,
        shap_values[index],
        X.iloc[index],
        matplotlib=True,
        show=False
    )

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()