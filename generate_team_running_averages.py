import pandas as pd

def weight(year_ago: int, week_ago: int):
    if year_ago > 0:
        return 2**(-year_ago)
    else:
        return 1.5**(-weeks_ago/17)

def create_df_week(
    df_weekly_team_data: pd.DataFrame, 
    week: int, 
    year: int, 
    sum_columns: list, 
    header_columns: list
):
    teams = []
    df_week = pd.DataFrame(columns=[*header_columns, *sum_columns])
    for index, row in df_weekly_team_data.iterrows():
        team = row["team"]
        if team not in teams:
            teams.append(team)

        if len(teams)==32:
            break

    print(teams)



def main():
    df_weekly_team_data = pd.read_csv("Season/all_teams_seasons_data.csv")
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

    header_columns = ["team", "season", "week", "opponent", "home"]

    df_all_seasons_data = pd.DataFrame(
        columns=[*header_columns, *avg_columns]
    )

    for year in range(2002, 2021):
        for week in range(1, 18):
            df_all_seasons_data = pd.concat(
                [
                    df_all_seasons_data, 
                    create_df_week(df_weekly_team_data, week, year, avg_columns, header_columns)
                ]
            )

    df_all_seasons_data.to_csv("Season/weekly_team_running_averages.csv")



if __name__ == "__main__":
    main()