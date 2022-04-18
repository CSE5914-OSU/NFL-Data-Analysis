import numpy as np
import pandas as pd

df_player_running_percent = pd.read_csv('Season/percent_of_opponent_running_averages.csv')
df_team_defense = pd.read_csv('Season/weekly_team_defense_running_averages.csv')
df_season_data = pd.read_csv('Season/all_seasons_data.csv')
df_all_weeks_player_data = pd.read_csv('Season/all_weeks_player_data.csv')

data_player_percent_columns = ['completions', 'attempts', 'passing_yards',
   'passing_tds', 'interceptions', 'sacks', 'sack_yards', 
   'passing_air_yards',  'passing_first_downs', 'passing_epa',
   'carries', 'rushing_yards', 'rushing_tds', 'rushing_fumbles',
   'rushing_fumbles_lost', 'rushing_first_downs', 'rushing_epa',
   'receptions', 'receiving_yards', 'receiving_tds', 'receiving_fumbles', 
   'receiving_fumbles_lost', 'receiving_first_downs', 
   'receiving_epa', 'fantasy_points', 'fantasy_points_ppr']

data_player_percent_times_opp = [
    play+'_times_opponent' for play in data_player_percent_columns
]

generic_columns = ['completions', 'attempts', 'passing_yards',
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

data_opponent_columns = [g+'_opponent' for g in data_player_percent_columns]

data_past_season_columns =  [g+'_prev_season' for g in generic_columns]

player_header_columns = [
    "player_id", "player_name", "recent_team", "season", "week"
]

team_header_columns = [
    "team", "season", "week", "opponent", "home"
]

columns = [
    *player_header_columns,
    'home',
    *data_player_percent_columns,
    *data_player_percent_times_opp,
    *data_opponent_columns,
    *data_past_season_columns
]

features = pd.DataFrame(columns=columns)

years = range(2004, 2022)
weeks = range(1, 18)
for year in years:
    print('Year =', year)
    df_data_player_percent = df_player_running_percent[
        (df_player_running_percent.season == year)
    ]
    df_data_opponent_defense = df_team_defense[
        (df_team_defense.season == year)
    ]

    df_data_season_data = df_season_data[
        (df_season_data.season == year)
    ]

    df_data_all_weeks_player_data = df_all_weeks_player_data[
        (df_all_weeks_player_data.season == year)
    ]

    for week in weeks:
        print('\tWeek =', week)
        df_data_player_percent_week = df_data_player_percent[
            (df_data_player_percent.week == week)
        ]
        df_data_opponent_defense_week = df_data_opponent_defense[
            (df_data_opponent_defense.week == week)
        ]
        df_data_all_weeks_player_data_week = df_data_all_weeks_player_data[
            (df_data_all_weeks_player_data.week == week)
        ]
        
        for index, row in df_data_player_percent_week.iterrows():

            data_player_percent_week_nump = df_data_player_percent_week[
                df_data_player_percent_week.player_id == row['player_id']
            ][data_player_percent_columns].to_numpy()

            df_data_opponent_defense_week_nump = df_data_opponent_defense_week[
                df_data_opponent_defense_week.opponent == row['recent_team']
            ][data_player_percent_columns].to_numpy()

            df_data_season_data_nump = df_data_season_data[
                df_data_season_data.player_id == row['player_id']
            ][generic_columns].to_numpy()

            df_data_all_weeks_player_data_week_nump = df_data_all_weeks_player_data_week[
                df_data_all_weeks_player_data_week.player_id == row['player_id']
            ][player_header_columns].to_numpy()

            results = df_data_all_weeks_player_data[
                df_data_all_weeks_player_data.player_id == row['player_id']
            ][['fantasy_points', 'fantasy_points_ppr']].to_numpy()

            opponent_times_player = data_player_percent_week_nump[0]*df_data_opponent_defense_week_nump[0]
            
            if len(data_player_percent_week_nump[0])!=len(data_player_percent_columns):
                data_player_percent_week_nump[0] = [0]*len(data_player_percent_columns)

            if len(df_data_opponent_defense_week_nump[0])!=len(data_opponent_columns):
                df_data_opponent_defense_week_nump[0] = [0]*len(data_opponent_columns)

            if len(df_data_season_data_nump[0])!=len(data_past_season_columns):
                df_data_season_data_nump[0] = [0]*len(data_past_season_columns)

            if len(df_data_all_weeks_player_data_week_nump[0])!=len(player_header_columns):
                df_data_all_weeks_player_data_week_nump[0] = [0]*len(player_header_columns)

            if len(opponent_times_player)!=len(data_player_percent_times_opp):
                opponent_times_player = [0]*len(data_player_percent_times_opp)


            features = pd.concat(
                [
                    features,
                    pd.DataFrame(
                        [[
                            *data_player_percent_week_nump[0],
                            *df_data_opponent_defense_week_nump[0],
                            *opponent_times_player,
                            *df_data_season_data_nump[0],
                            *df_data_all_weeks_player_data_week_nump[0],
                            *results[0]

                        ]],
                        columns=[
                            *data_player_percent_columns,
                            *data_opponent_columns,
                            *data_player_percent_times_opp,
                            *data_past_season_columns,
                            *player_header_columns,
                            'fantasy_points_result',
                            'fantasy_points_ppr_result'
                        ]
                    )
                ]
            )



features.to_csv('training_data2.csv')
