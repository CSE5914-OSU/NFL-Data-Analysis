import pandas as pd
import numpy as np

def weight(years_ago: int, weeks_ago: int):
    if years_ago > 0:
        return 2**(-years_ago)
    else:
        return 1.5**(-weeks_ago/17)

def weighted_sum(arr):
    if len(arr)>0:
        arr_without_lead = arr[:, 2:]
        my_arr = np.array([0.0]*len(arr_without_lead[0]))
        ws = []
        for i, d in enumerate(arr):
            week_ago = arr[i][1]
            year_ago = arr[0][0]-arr[i][0]+3
            ws.append(weight(year_ago, week_ago))
            my_arr += ws[i]*arr_without_lead[i]

        return my_arr/sum(ws)
    else:
        return np.array([])

def create_df_week(
    df_weekly_player_data: pd.DataFrame, 
    week: int, 
    year: int, 
    sum_columns: list, 
    header_columns: list,
    players: list
):
    df_week = pd.DataFrame(columns=[*header_columns, *sum_columns])

    df_weekly_player_data = df_weekly_player_data[
        (df_weekly_player_data.season >= year-3) &
        (df_weekly_player_data.season <= year) 
    ]

    for player in players:
        player_week_temp = (df_weekly_player_data[
            (df_weekly_player_data.player_id == player) &
            (df_weekly_player_data.season >= year-3) &
            (df_weekly_player_data.season < year) |
            (
                (df_weekly_player_data.season == year) & 
                (df_weekly_player_data.week < week) &
                (df_weekly_player_data.player_id == player)
            )
        ])[["season", "week",*sum_columns]].to_numpy()

        np_weighted_sum = weighted_sum(player_week_temp)

        if len(np_weighted_sum) > 0:

            player_week_temp = (df_weekly_player_data[
                (df_weekly_player_data.player_id == player) &
                (df_weekly_player_data.season == year) &
                (df_weekly_player_data.week == week)
            ])[header_columns].to_numpy()

            if len(player_week_temp)>0:
                df_data = pd.DataFrame([[*player_week_temp[0], *np_weighted_sum]], columns=[*header_columns, *sum_columns])
                df_week = pd.concat([df_week, df_data])

    print(df_week)
    return df_week

def main():
    df_weekly_player_data = pd.read_csv("Season/all_weeks_player_data.csv")
    avg_columns = ['completions', 'attempts', 'passing_yards',
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

    header_columns = ["player_id", "player_name", "recent_team", "season", "week"]

    df_all_seasons_data = pd.DataFrame(
        columns=[*header_columns, *avg_columns]
    )

    players = []
   
    for index, row in df_weekly_player_data.iterrows():
        player_id = row["player_id"]
        if player_id not in players:
            players.append(player_id)



    for year in range(1999, 2022):
        print('year =', year)
        for week in range(1, 18):
            print('\tweek =', week)
            df_all_seasons_data = pd.concat(
                [
                    df_all_seasons_data, 
                    create_df_week(df_weekly_player_data, week, year, avg_columns, header_columns, players)
                ]
            )
            


    df_all_seasons_data.to_csv("Season/running_player_averages.csv")



if __name__ == "__main__":
    main()