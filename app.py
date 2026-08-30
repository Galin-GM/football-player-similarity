import streamlit as st
import matplotlib.pyplot as plt

from src.modelling import (
    find_similar_players,
    get_player_labels,
    get_player_stats,
    get_player_percentiles
)

st.set_page_config(
    page_title="Football Player Similarity"
)

st.title("Football Player Similarity")

st.write(
    "Select a forward to find statistically similar players using per 90 performance data"
)

player_options = get_player_labels()

selected_player = st.selectbox(
    "Select a player",
    options=player_options
)

number_of_results = st.slider(
    "Number of similar players",
    min_value=1,
    max_value=10,
    value=5
)

if st.button("Find similar players"):
    selected_stats = get_player_stats(selected_player)

    results = find_similar_players(selected_player, number_of_results)

    comparison_labels = [
        selected_player,
        *results['PlayerLabel'].tolist()
    ]

    percentile_comparison = get_player_percentiles(comparison_labels)

    feature_names = {
        "Gls90": "Goals",
        "Ast90": "Assists",
        "Sh/90": "Shots",
        "Fld/90": "Fouls drawn",
        "Off/90": "Offsides",
        "Crs/90": "Crosses"
    }

    heatmap_data = (
        percentile_comparison
        .set_index('PlayerLabel')
        .rename(columns=feature_names)
    )

    st.subheader("Selected player")
    st.dataframe(selected_stats, hide_index=True)

    st.subheader("Most similar players")
    st.dataframe(results, hide_index=True)
    st.caption("Lower similarity value means the players are more statistically similar.")

    # Percentile comparison heatmap
    figure_height = max(3, len(heatmap_data) * 0.6)

    fig, ax = plt.subplots(
        figsize=(10, figure_height)
    )

    heatmap = ax.imshow(
        heatmap_data,
        cmap="YlGn",
        aspect="auto",
        vmin=0,
        vmax=100
    )

    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(
        heatmap_data.columns,
        rotation=30,
        ha="right"
    )

    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)

    for row in range(len(heatmap_data.index)):
        for column in range(len(heatmap_data.columns)):
            value = heatmap_data.iloc[row, column]

            ax.text(
                column,
                row, 
                f"{value:.0f}",
                ha="center",
                va="center",
                color="black"
            )

    fig.colorbar(
        heatmap,
        ax=ax,
        label="Percentile"
    )

    ax.set_title("Forward percentile comparison")
    fig.tight_layout()
    st.pyplot(fig)
    st.caption("Percentiles compare each player with all eligible forwards. "
                   "A value of 80 means the player ranks higher than 80% of forwards for that statistic. " \
                   "All features are per 90 minutes.")
    plt.close(fig)



