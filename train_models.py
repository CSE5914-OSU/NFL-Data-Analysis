import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import linear_model


if __name__ == "__main__":
	df_data = pd.read_csv("train_square.csv").fillna(0)
	df_data = shuffle(df_data)
	end_train = int(len(df_data.index)*9/10)

	end_x = len(df_data.columns)-2
	df_train_X = df_data.iloc[:end_train, 3:end_x]
	df_test_X = df_data.iloc[end_train:, 3:end_x]

	df_train_Y = df_data.iloc[:end_train, end_x:]
	df_test_Y = df_data.iloc[end_train :, end_x:]

	
	model = linear_model.LinearRegression().fit(df_train_X, df_train_Y)
	Y_pred = model.predict(df_test_X)

	Y_test = df_test_Y.to_numpy()

	score = sum(abs((Y_test-Y_pred))/len(Y_test))

	print(score)