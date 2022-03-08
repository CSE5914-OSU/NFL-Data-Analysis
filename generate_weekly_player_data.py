import pandas as pd
import numpy as np

if __name__ == "__main__":
    columns = ['player_id', 'player_name', 'recent_team', 'season', 'week', 'completions', 'attempts', 'passing_yards',
       'passing_tds', 'interceptions', 'sacks', 'sack_yards', 'sack_fumbles',
       'sack_fumbles_lost', 'passing_air_yards', 'passing_yards_after_catch',
       'passing_first_downs', 'passing_epa', 'passing_2pt_conversions',
       'dakota', 'carries', 'rushing_yards', 'rushing_tds', 'rushing_fumbles',
       'rushing_fumbles_lost', 'rushing_first_downs', 'rushing_epa',
       'rushing_2pt_conversions', 'receptions', 'targets', 'receiving_yards',
       'receiving_tds', 'receiving_fumbles', 'receiving_fumbles_lost',
       'receiving_air_yards', 'receiving_yards_after_catch',
       'receiving_first_downs', 'receiving_epa', 'receiving_2pt_conversions',
       'special_teams_tds', 'fantasy_points', 'fantasy_points_ppr']

    all_weeks_player_data = pd.DataFrame(columns=columns)
    for i in range(1999,2022):
        print(i)
        df_data = pd.read_csv("Game-By-Game/player_stats_"+str(i)+".csv")[columns]
        all_weeks_player_data = pd.concat([all_weeks_player_data, df_data])

    all_weeks_player_data.to_csv("Season/all_weeks_player_data.csv")

    print(all_weeks_player_data)