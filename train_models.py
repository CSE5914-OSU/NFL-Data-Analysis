import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import linear_model, neural_network
import matplotlib.pyplot as plt
import pickle
from colorama import Fore, Style
import threading
global num_threads
num_threads = 0

def train(
	df_train_X,
	df_train_Y,
	df_test_X,
	df_test_Y,
	active,
	solver,
	shape,
	week,

):
	print(f'{Fore.RED}')
	model = neural_network.MLPRegressor(
		hidden_layer_sizes=shape,
		max_iter=1000,
		solver=solver,
		activation=active,
		verbose=True,
		warm_start=True, 
		tol=1e-4,
		early_stopping=True,
		n_iter_no_change=40
	).fit(df_train_X, df_train_Y)
	print(f'{Style.RESET_ALL}')
	Y_pred = model.predict(df_test_X)
	Y_test = df_test_Y.to_numpy()
	score = np.sqrt(sum((Y_test-Y_pred)**2)/len(Y_test))

	filename = 'models/'+str(active)+'_'+str(solver)+'_'+str(shape)+'_week_'+str(week)+'.sav'
	pickle.dump(model, open(filename, 'wb'))
	print(f'{Fore.GREEN}')
	print('model', count, filename)
	print('\tscore = ', score)
	print(f'{Style.RESET_ALL}')

if __name__ == "__main__":
	activations = ['relu']
	solvers = ['adam']
	shapes = [
		(1000, 500, 500, 500, 500),
	]
	weeks = list(range(1, 18))
	df_data = pd.read_csv("training_data2.csv").fillna(0)
		
	count = 0
	threads = []
	for week in weeks:
		end_x = len(df_data.columns)-2
		end_x = len(df_data.columns)-2
		df_train_X = df_data[
		    (df_data.season != 2021) | 
		    (df_data.week<week)
		].iloc[:, 5:end_x]
		df_test_X = df_data[
		    (df_data.season == 2021) & 
		    (df_data.week==week)
		].iloc[:, 5:end_x]

		df_train_Y = df_data[
		    (df_data.season != 2021) | 
		    (df_data.week<week)
		].iloc[:, end_x:]
		df_test_Y = df_data[
		    (df_data.season == 2021) & 
		    (df_data.week==week)
		].iloc[:, end_x:]
		for solver in solvers:
			for shape in shapes:
				for active in activations:
					train(
						df_train_X,
						df_train_Y,
						df_test_X,
						df_test_Y,
						active,
						solver,
						shape,
						week
					)
					# threads.append(t)

	# for t in threads:
	# 	t.start()

	# for t in threads:
	# 	t.join()

					


