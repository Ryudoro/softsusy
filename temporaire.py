def plot_branching_ratios_on_ax(ax_neutralino, ax_chargino, neutralino_df, chargino_df, title_neutralino, title_chargino):
    # Neutralinos
    decay_products_neutralino = neutralino_df['decay_products'].unique()
    num_decay_products_neutralino = len(decay_products_neutralino)
    bar_positions_neutralino = np.arange(num_decay_products_neutralino)

    for i, decay_product in enumerate(decay_products_neutralino):
        ax_neutralino.bar(bar_positions_neutralino[i], neutralino_df[neutralino_df['decay_products'] == decay_product]['branching_ratio'].mean(), label=decay_product)

    ax_neutralino.set_xticks(bar_positions_neutralino)
    ax_neutralino.set_xticklabels(decay_products_neutralino, rotation=45, ha='right')
    ax_neutralino.set_ylabel('Branching Ratio')
    ax_neutralino.set_title(title_neutralino)
    ax_neutralino.legend()

    # Charginos
    decay_products_chargino = chargino_df['decay_products'].unique()
    num_decay_products_chargino = len(decay_products_chargino)
    bar_positions_chargino = np.arange(num_decay_products_chargino)

    for i, decay_product in enumerate(decay_products_chargino):
        ax_chargino.bar(bar_positions_chargino[i], chargino_df[chargino_df['decay_products'] == decay_product]['branching_ratio'].mean(), label=decay_product)

    ax_chargino.set_xticks(bar_positions_chargino)
    ax_chargino.set_xticklabels(decay_products_chargino, rotation=45, ha='right')
    ax_chargino.set_ylabel('Branching Ratio')
    ax_chargino.set_title(title_chargino)
    ax_chargino.legend()

def update_graph(m1_value, m2_value, mu_value, tan_beta_value):
    nmix, umix, neutralino_df, chargino_df = load_data_from_files(m1_value, m2_value, mu_value, tan_beta_value)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))

    plot_mixing_matrix_on_ax(ax1, nmix, "Neutralino Mixing Matrix")
    plot_mixing_matrix_on_ax(ax2, umix, "Chargino Mixing Matrix")
    plot_branching_ratios_on_ax(ax3, ax4, neutralino_df, chargino_df, "Neutralino Decay Branching Ratios", "Chargino Decay Branching Ratios")

    plt.tight_layout()
    plt.show()


def plot_mixing_matrix_on_ax(ax, mixing_matrix, title):
    im = ax.imshow(mixing_matrix, cmap='viridis', vmin=-1, vmax=1)
    ax.figure.colorbar(im, ax=ax)
    
    # Affichez les valeurs de la matrice de mixage dans chaque cellule
    for i in range(mixing_matrix.shape[0]):
        for j in range(mixing_matrix.shape[1]):
            ax.text(j, i, f"{mixing_matrix[i, j]:.2f}", ha="center", va="center", color="w" if mixing_matrix[i, j] > 0.5 else "k")

    ax.set_xticks(np.arange(mixing_matrix.shape[1]))
    ax.set_yticks(np.arange(mixing_matrix.shape[0]))
    ax.set_xticklabels([f"{i+1}" for i in range(mixing_matrix.shape[1])])
    ax.set_yticklabels([f"{i+1}" for i in range(mixing_matrix.shape[0])])
    
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_title(title)