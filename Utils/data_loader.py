import pandas as pd

class PlayerDataLoader:
    @staticmethod
    def load(filepath="players(in).csv"):
        """
        Loads and prepares player data from a CSV file.

        Returns:
            df_sorted (pd.DataFrame): Player DataFrame with normalized columns and position ordering.
            position_id_map (dict): Mapping from position to list of player IDs.
            dict_players (list of dict): Each player's data as a dictionary (optional use).
        """
        # Load CSV
        df = pd.read_csv(filepath, index_col=0)

        # Normalize column names
        df.rename(columns={
            "Name": "name",
            "Position": "position",
            "Skill": "skill",
            "Salary (€M)": "salary"
        }, inplace=True)

        # Define position order and sort accordingly
        position_order = ["GK", "DEF", "MID", "FWD"]
        df_sorted = df.sort_values(
            by="position",
            key=lambda x: x.map({pos: i for i, pos in enumerate(position_order)})
        ).reset_index(drop=True)

        # Add player ID
        df_sorted["id"] = df_sorted.index

        # Optional: list of player dictionaries
        dict_players = df_sorted.to_dict(orient="records")

        # Create position-to-player-ID map
        position_id_map = {
            pos: df_sorted[df_sorted["position"] == pos]["id"].tolist()
            for pos in position_order
        }

        return df_sorted, position_id_map, dict_players
