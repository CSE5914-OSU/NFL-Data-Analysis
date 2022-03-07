import pandas as pd
import numpy as np
import pyreadr

def played(array):
	"""
		@param array
			An array with float and/or integer data
		@returns
			True if there is any non-zero entry from the previous week and
			False otherwise.
	"""
	for r in array:
		if r!=0:
			return True

	return False

def create_df_week(
	df_data: pd.DataFrame, 
	week: int, 
	year: int, 
	sum_columns: list, 
	df_schedule: pd.DataFrame
):
	"""
		Creates each team's single week data.

		@param df_data
			each player's game by game data
		@param week
			week of the season that should be generated
		@param season
			the current season
		@param sum_columns
			The columns that should have each player's stats summed
		@param df_schedule
			A dataframe that has nfl scheduling data

		@returns a dataframe with each teams data for the week
	"""
	teams = []
	df_week = pd.DataFrame(columns=["team", "season", "week", "opponent", "home", *sum_columns])
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
			(df_data.week==week)
		]

		summed = df_temp[sum_columns].sum()

		df_game = df_schedule[
			(df_schedule.home_team.isin([team]) | df_schedule.away_team.isin([team])) &
			(df_schedule.season==year) & (df_schedule.week==week)
		]
		if len(df_game.to_numpy())==0:
			continue

		home = df_game["home_team"].to_numpy()[0]
		away = df_game["away_team"].to_numpy()[0]
		if team == home:
			opponent = away
			home = 1
		elif team == away:
			opponent = home
			home = 0

		if played(summed):
			df_week = pd.concat([df_week, pd.DataFrame(
				[[team, year, week, opponent, home, *summed.array]], 
				columns=["team", "season", "week", "opponent", "home", *sum_columns])
			])

	return df_week


def main():
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



	df_all_seasons_data = pd.DataFrame(
		columns=["team", "season", "week", "opponent", "home", *sum_columns]
	)

	for year in range(1999,2022):
		df_schedule = pyreadr.read_r('Schedules/sched_'+str(year)+'.rds')[None]
		print("Year =", year)
		for week in range(1,18):
			print("\tWeek =", week)
			df_data = pd.read_csv("Game-By-Game/player_stats_"+str(year)+".csv")
			df_all_seasons_data = pd.concat(
				[df_all_seasons_data, 
					create_df_week(df_data, week, year, sum_columns, df_schedule)
				]
			)

	df_all_seasons_data.to_csv("Season/all_teams_seasons_data.csv")


if __name__ == "__main__":
	main()