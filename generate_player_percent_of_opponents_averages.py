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

df_player_percent_of_opponent_average = pd.DataFrame(columns=[
    [*player_header_columns, *data_columns]
])

week = 1
year = 1998
for index, row in df_player_weekly_data.iterrows():
    if year != row['season']:
        year = row['season']
        print(year)
    player_team = row['recent_team']
    player_opponent = df_team_weekly_data[
        (df_team_weekly_data.team == player_team) &
        (df_team_weekly_data.season == row['season']) &
        (df_team_weekly_data.week == row['week'])
    ]['opponent'].to_numpy()

    if len(player_opponent) == 0:
        continue
    else:
        player_opponent = player_opponent[0]

    player_opponent_data = df_team_weekly_data[
        (df_team_weekly_data.team == player_opponent) &
        (df_team_weekly_data.season == row['season']) &
        (df_team_weekly_data.week == row['week'])
    ][data_columns].to_numpy()

    if len(player_opponent_data)!=0:
        player_opponent_data = player_opponent_data[0]

    player_data = row[data_columns].to_numpy()


    if len(player_opponent_data)==0 or len(player_data)==0:
        continue

    for i, x in enumerate(player_opponent_data):
        if x==0:
            if player_data[i] != 0:
                player_opponent_data[i] = player_data[i]
            else:
                player_opponent_data[i] = 1

    player_percentages_data = player_data/player_opponent_data



    print(player_percentages_data)

    
