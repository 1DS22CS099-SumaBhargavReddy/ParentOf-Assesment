import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Use headless Agg backend for non-interactive environments
import matplotlib.pyplot as plt

EXCEL_FILE = "Copy of Task 1 Dataset.xlsx"
STATIC_DIR = "static/plots"


def create_visualizations():
    print("Loading dataset...")
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: {EXCEL_FILE} not found. Run process_data.py first!")
        return

    df = pd.read_excel(EXCEL_FILE)

    # Ensure output directory exists
    os.makedirs(STATIC_DIR, exist_ok=True)
    print(f"Output directory verified: {STATIC_DIR}")

    # Columns of interest
    rate_cols = [
        "Accuracy Rate",
        "Response Rate",
        "Error Rate",
        "Persistence Rate",
        "Consistency Rate",
        "Overall Performance Score",
    ]

    # Set styling parameters for premium aesthetics
    plt.rcParams["figure.facecolor"] = "#0d1117"
    plt.rcParams["axes.facecolor"] = "#161b22"
    plt.rcParams["text.color"] = "#c9d1d9"
    plt.rcParams["axes.labelcolor"] = "#8b949e"
    plt.rcParams["xtick.color"] = "#8b949e"
    plt.rcParams["ytick.color"] = "#8b949e"
    plt.rcParams["axes.edgecolor"] = "#30363d"
    plt.rcParams["grid.color"] = "#21262d"

    # --- Plot 1: Distributions ---
    print("Generating Plot 1: Rate Distributions...")
    fig, axes = plt.subplots(3, 2, figsize=(12, 14))
    axes = axes.flatten()
    colors = ["#58a6ff", "#ff7b72", "#7ee787", "#d2a8ff", "#ffa657", "#ff79c6"]

    for idx, col in enumerate(rate_cols):
        ax = axes[idx]
        ax.hist(df[col], bins=25, color=colors[idx], alpha=0.8, edgecolor="#161b22", density=True)
        # Add smooth estimation curve
        df[col].plot(kind="kde", ax=ax, color="#f0f6fc", linewidth=1.5, linestyle="--")
        ax.set_title(f"{col} Distribution", fontsize=12, pad=10, fontweight="bold")
        ax.set_xlim(0, 100)
        ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig(f"{STATIC_DIR}/rate_distributions.png", dpi=150, facecolor="#0d1117")
    plt.close()

    # --- Plot 2: Correlation Matrix ---
    print("Generating Plot 2: Correlation Heatmap...")
    corr = df[rate_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 7))
    cax = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    # Add colorbar
    cbar = fig.colorbar(cax, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color="#8b949e")
    cbar.ax.set_ylabel("Correlation Coefficient", rotation=-90, va="bottom", color="#8b949e")

    # Set labels
    ax.set_xticks(range(len(rate_cols)))
    ax.set_yticks(range(len(rate_cols)))
    ax.set_xticklabels([col.replace(" Rate", "").replace(" Score", "") for col in rate_cols], rotation=45, ha="right")
    ax.set_yticklabels([col.replace(" Rate", "").replace(" Score", "") for col in rate_cols])

    # Annotate cells with values
    for i in range(len(rate_cols)):
        for j in range(len(rate_cols)):
            val = corr.iloc[i, j]
            color = "white" if abs(val) > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontweight="bold")

    ax.set_title("Cognitive Metrics Correlation Heatmap", fontsize=14, pad=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{STATIC_DIR}/correlation_matrix.png", dpi=150, facecolor="#0d1117")
    plt.close()

    # --- Plot 3: Boxplots ---
    print("Generating Plot 3: Performance Boxplots...")
    fig, ax = plt.subplots(figsize=(10, 6))
    box = ax.boxplot(
        [df[col] for col in rate_cols],
        labels=[col.replace(" Rate", "").replace(" Score", "") for col in rate_cols],
        patch_artist=True,
        medianprops={"color": "#f0f6fc", "linewidth": 2},
        boxprops={"facecolor": "#58a6ff", "edgecolor": "#f0f6fc", "alpha": 0.7},
        whiskerprops={"color": "#8b949e", "linewidth": 1.5},
        capprops={"color": "#8b949e", "linewidth": 1.5},
    )

    # Color individual boxes uniquely
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)

    ax.set_ylabel("Score (0 - 100)", fontsize=11, labelpad=10)
    ax.set_title("Quartile Performance Comparison", fontsize=14, pad=15, fontweight="bold")
    ax.grid(True, axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{STATIC_DIR}/performance_boxplots.png", dpi=150, facecolor="#0d1117")
    plt.close()

    # --- Plot 4: Trade-offs (Response vs Persistence) ---
    print("Generating Plot 4: Response vs. Persistence Scatter...")
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(
        df["Response Rate"],
        df["Persistence Rate"],
        c=df["Overall Performance Score"],
        cmap="viridis",
        alpha=0.8,
        edgecolor="#161b22",
        linewidths=0.5,
    )

    cbar = fig.colorbar(scatter)
    cbar.ax.yaxis.set_tick_params(color="#8b949e")
    cbar.ax.set_ylabel("Overall Performance Score", rotation=-90, va="bottom", color="#8b949e")

    ax.set_xlabel("Response Rate (Speed & Streaks)", fontsize=11, labelpad=10)
    ax.set_ylabel("Persistence Rate (Resilience & Focus)", fontsize=11, labelpad=10)
    ax.set_title("Response vs. Persistence Trade-off", fontsize=14, pad=15, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{STATIC_DIR}/tradeoff_scatter.png", dpi=150, facecolor="#0d1117")
    plt.close()

    print("[SUCCESS] All visualizations generated successfully inside static/plots/!")


if __name__ == "__main__":
    create_visualizations()
