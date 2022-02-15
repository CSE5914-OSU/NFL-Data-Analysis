import pandas as pd
import numpy as np


def season(df_data):
	"""
		Very simple season data aggregator. It adds up all the data and gives season totals.
		@param df_data 
			A dataframe in the format of week by week player data.
	"""
	used_ids = []
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

	season_data = pd.DataFrame( columns=["player_id", "player_name", "games_played", "season", *sum_columns])
	for index, row in df_data.iterrows():
		player_id = row["player_id"]

		if player_id not in used_ids:
			player_name = row["player_name"]
			seas = row["season"]
			used_ids.append(player_id)
			df_temp = df_data[
				df_data.player_id.isin([player_id]) & 
				(df_data.season_type=="REG")]
			summed = df_temp[sum_columns].sum()
			
			df_player = pd.DataFrame(
				[[player_id, player_name, len(df_temp.index), seas, *summed.array]], 
				columns=["player_id", "player_name", "games_played", "season", *sum_columns])
			
			season_data = pd.concat([season_data, df_player])

	return season_data



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
	df_all_season_data = pd.DataFrame(columns=["player_id", "player_name", "games_played", "season", *sum_columns])

	for i in range(1999,2022):
		print(i)
		df_data = pd.read_csv("Game-By-Game/player_stats_"+str(i)+".csv")
		df_all_season_data = pd.concat([df_all_season_data, season(df_data)])

	df_all_season_data.to_csv("Season/all_seasons_data.csv")