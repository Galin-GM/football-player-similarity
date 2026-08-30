import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from src.config import DATA_PATH

# Load data and features
df = pd.read_csv(DATA_PATH)
forwards_df = df.loc[df['PrimaryPos'].isin(['FW'])].copy()
features = ['Gls90', 'Ast90', 'Sh/90', 'Fld/90', 'Off/90', 'Crs/90']
X = forwards_df[features].copy()

# Standardise features
scaler = StandardScaler()
X_scaled = scaler.fit(X).transform(X)

# Nearest neighbour model
forwards_lookup = forwards_df.reset_index(drop=True).copy()

forwards_lookup['PlayerLabel'] = (
    forwards_lookup['Player'] + " - " + forwards_lookup['Squad']
)

nearest_model = NearestNeighbors(metric='euclidean')
nearest_model.fit(X_scaled)


def get_player_labels():
    return sorted(
        forwards_lookup['PlayerLabel'].tolist()
    )

def find_similar_players(player_label, number_of_results=5):
    matching_positions = forwards_lookup.index[
        forwards_lookup["PlayerLabel"].eq(player_label)
    ].tolist()

    if not matching_positions:
        raise ValueError(
            f"No forward found with the label: {player_label}"
        )

    if number_of_results < 1:
        raise ValueError(
            "number_of_results must be at least 1"
        )

    query_position = matching_positions[0]

    maximum_results = len(forwards_lookup) - 1
    number_of_results = min(
        number_of_results,
        maximum_results
    )

    distances, positions = nearest_model.kneighbors(
        X_scaled[[query_position]],
        n_neighbors=number_of_results + 1
    )

    neighbour_pairs = [
        (position, distance)
        for position, distance in zip(
            positions[0],
            distances[0]
        )
        if position != query_position
    ][:number_of_results]

    neighbour_positions = [
        position for position, distance in neighbour_pairs
    ]

    neighbour_distances = [
        distance for position, distance in neighbour_pairs
    ]

    result_columns = [
    "PlayerLabel",
    *features
    ]

    results = forwards_lookup.iloc[
        neighbour_positions
    ][result_columns].copy()

    results["Distance"] = neighbour_distances

    return results.reset_index(drop=True)





