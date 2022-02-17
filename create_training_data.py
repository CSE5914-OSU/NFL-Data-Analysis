import pandas as pd
import numpy as np


def generate_features(df_seasons: pd.DataFrame, df_last_season: pd.DataFrame, 
		df_this_season: pd.DataFrame, year: int, week: int):
	"""
		Generates the traing data that can be used for training a model.
		@param df_seasons
			A dataframe with all the nfl season data for at least the past 3 
			years of nfl
		@param df_last_season
			A dataframe with the data for the previous year's game by game 
			player data.
		@param df_this_season
			A dataframe with the data for this year's game by game data.
		@param year
			An integer that gives the year for the data that is to be predicted
		@param week
			An integer that gives the week that would like to be predicted
		@returns
			A dataframe that has all of the 'relevant' features and the 
			resulting fantasy points
	"""
	used_ids = []
	columns = ['completions', 'attempts', 'passing_yards',
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

	columns_3_prev_seasons = [[col+"_season-"+str(i) for col in columns ]for i in range(1, 4)]
	columns_10_prev_games = [[col+"_game-"+str(i) for col in columns ]for i in range(1, 11)]
	columns_all = ["player_name", "player_id", "season", "week"]
	for cols in columns_3_prev_seasons:
		for col in cols:
			columns_all.append(col)

	for cols in columns_10_prev_games:
		for col in cols:
			columns_all.append(col)

	print(columns_all)
    
	features = pd.DataFrame(columns = columns_all)

	for index, row in df_this_season.iterrows():
		player_id = row["player_id"]
		if player_id not in used_ids:
			player_name = row["player_name"]
			used_ids.append(player_id)
			temp_seasons = []
			for i in range(1, 4):
				temp_seasons.append(df_seasons[
					df_seasons.player_id.isin([player_id]) & 
					(df_seasons.season==(year-i))][columns].to_numpy())

			last_season_games = (df_last_season[
				df_last_season.player_id.isin([player_id])][columns])

			this_season_games = (df_this_season[
				df_this_season.player_id.isin([player_id])][columns])

			# print(last_season_games)

				
				
					




if __name__ == "__main__":
	df_seasons = pd.read_csv("Season/all_seasons_data.csv")
	years = range(2003, 2022)
	weeks = range(1, 17)
	for year in years:
		for week in weeks:
			df_last_season = pd.read_csv("Game-By-Game/player_stats_"+
				str(year-1)+".csv")
			df_this_season = pd.read_csv("Game-By-Game/player_stats_"+
				str(year)+".csv")
			df_weekly_features = generate_features(df_seasons, df_last_season, 
				df_this_season, year, week)
			print(df_weekly_features.head())
			break
