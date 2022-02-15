import pandas as pd
import numpy as np


def generate_features(df_seasons: pd.DataFrame , df_last_season:pd.DataFrame , 
		df_this_season: pd.DataFrame , year: int, week: int):
	"""
		Generates the traing data that can be used for training a model.
		@param df_seasons
			A dataframe with all the nfl season data for at least the past 3 
			years of nfl
		@param df_last_season
			A dataframe with the data for the past game by game player data.
		@param df_this_season
			A dataframe with the data for this year's game by game data.
		@param year
			An integer that gives the year for the data that is to be predicted
		@param week
			An integer that gives the week that would like to be predicted
		@returns
			A dataframe that has all of the 'relevant' features and the resulting 
			fantasy points
	"""
	for index, row in df_this_season.iterrows():
		
		


if __name__ == "__main__":
	df_seasons = pd.read_csv("Season/all_seasons_data.csv")
	years = range(2003, 2022)
	weeks = range(1, 17)
	for year in years:
		for week in weeks:
			df_last_season = pd.read_csv("Game-By-Game/player_stats_"+str(year-1)+".csv")
			df_this_season = pd.read_csv("Game-By-Game/player_stats_"+str(year)+".csv")
			df_weekly_features = generate_features(df_seasons, df_last_season, 
				df_this_season, year, week)
			print(df_weekly_features.head())
			break
