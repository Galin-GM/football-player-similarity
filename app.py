import streamlit as st

from src.modelling import (
    find_similar_players,
    get_player_labels
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
    results = find_similar_players(selected_player, number_of_results)

    st.subheader(f"Players similar to {selected_player}")

    st.dataframe(results, hide_index=True)