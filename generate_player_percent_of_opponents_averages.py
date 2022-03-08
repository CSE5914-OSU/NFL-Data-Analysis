import numpy as np
import pandas as pd

data_columns = ['completions', 'attempts', 'passing_yards',
   'passing_tds', 'interceptions', 'sacks', 'sack_yards', 
   'passing_air_yards',  'passing_first_downs', 'passing_epa',
   'carries', 'rushing_yards', 'rushing_tds', 'rushing_fumbles',
   'rushing_fumbles_lost', 'rushing_first_downs', 'rushing_epa',
   'receptions', 'receiving_yards', 'receiving_tds', 'receiving_fumbles', 
   'receiving_fumbles_lost', 'receiving_first_downs', 
   'receiving_epa', 'fantasy_points', 'fantasy_points_ppr']

player_header_columns = ["player_id", "player_name", "recent_team", "season", "week"]
team_header_columns = ["team", "season", "week", "opponent", "home"]

df_player_weekly_data = pd.read_csv('Season/all_weeks_player_data.csv')[
    [*player_header_columns, *data_columns]
]

df_player_weekly_data = df_player_weekly_data[(df_player_weekly_data.season >= 2004)]

df_team_weekly_data = pd.read_csv('Season/weekly_team_defense_running_averages.csv')[
    [*team_header_columns, *data_columns]
]

df_team_weekly_data = df_team_weekly_data[(df_team_weekly_data.season >= 2004)]

print(df_player_weekly_data)
print(df_team_weekly_data)
