import pandas as pd
import numpy as np

def played(summed_array):
	for summed in summed_array:
		if summed!=0:
			return True
	
	return False

def create_df_week(df_data: pd.DataFrame, week: int, year: int, sum_columns: list):
	teams = []
	df_week = pd.DataFrame( columns=["team", "season", "week", *sum_columns])
	for index, row in df_data.iterrows():
		team = row["recent_team"]
		if team not in teams:
			teams.append(team)

		len_teams = len(teams)
		if len_teams==32 or (len_teams==31 and year<2002):
			break

	for team in teams:
		df_temp = df_data[
			df_data.recent_team.isin([team]) & 
			(df_data.season_type=="REG") &
			(df_data.week==week)]
		summed = df_temp[sum_columns].sum()
		if played(summed):
			df_week = pd.concat([df_week, pd.DataFrame(
					[[team, year, week, *summed.array]], 
					columns=["team", "season", "week", *sum_columns])])

	return df_week


if __name__ == "__main__":
	sum_columns = ['completions', 'attempts', 'passing_yards',
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

	df_all_season_data = pd.DataFrame(
		columns=["team", "season", "week", *sum_columns]
	)

	for year in range(1999,2022):
		print("Year =", year)
		for week in range(1,18):
			print("\tWeek =", week)
			df_data = pd.read_csv("Game-By-Game/player_stats_"+str(year)+".csv")
			df_all_season_data = pd.concat(
				[df_all_season_data, 
					create_df_week(df_data, week, year, sum_columns)
				]
			)

	df_all_season_data.to_csv("Season/all_teams_seasons_data.csv")
