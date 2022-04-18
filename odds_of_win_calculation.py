import numpy as np

def calc_win_odds(
	team_1_players_projections: list,
	team_2_players_projections: list,
	team_1_players_projections_stdev: list,
	team_2_players_projections_stdev: list,
	n_sim: int = 100000
):
	"""Calculates the odds that a fantasy team will beat another team.

	"""
	team_1_projection = sum(team_1_players_projections)
	team_2_projection = sum(team_2_players_projections)
	team_1_stdev = np.sqrt(sum(np.array(team_1_players_projections_stdev)**2))
	team_2_stdev = np.sqrt(sum(np.array(team_2_players_projections_stdev)**2))

	team_1_sim = np.random.normal(
		loc=team_1_projection,
		scale=team_1_stdev,
		size=n_sim
	)

	team_2_sim = np.random.normal(
		loc=team_2_projection,
		scale=team_2_stdev,
		size=n_sim
	)

	team_1_win = 0

	for team_1, team_2 in zip(team_1_sim, team_2_sim):
		if team_1 > team_2:
			team_1_win += 1

	return team_1_win/n_sim

def calc_win_odds_simple(
	team_1_players_projections: list,
	team_2_players_projections: list,
	n_sim: int = 100000
):
	"""Calculates the odds that a fantasy team will beat another team.

	Args:
		team_1_players_projections: List of projections for the players from
			team 1
		team_2_players_projections: List of projections for the players from
			team 2
		n_sim: The number of simulations to run. The larger the number, the more
			accurate the result, but it runs slower.

	"""
	team_1_projection = sum(team_1_players_projections)
	team_2_projection = sum(team_2_players_projections)
	team_1_stdev = np.sqrt(team_1_projection)
	team_2_stdev = np.sqrt(team_2_projection)

	team_1_sim = np.random.normal(
		loc=team_1_projection,
		scale=team_1_stdev,
		size=n_sim
	)

	team_2_sim = np.random.normal(
		loc=team_2_projection,
		scale=team_2_stdev,
		size=n_sim
	)

	team_1_win = 0

	for team_1, team_2 in zip(team_1_sim, team_2_sim):
		if team_1 > team_2:
			team_1_win += 1

	return team_1_win/n_sim

if __name__ == "__main__":
	team_size = 13
	team_1_projection = [9 for _ in range(team_size)]
	team_2_projection = [10 for _ in range(team_size)]

	team_1_win_odds = calc_win_odds_simple(
		team_1_projection,
		team_2_projection,
	)

	print(team_1_win_odds)
