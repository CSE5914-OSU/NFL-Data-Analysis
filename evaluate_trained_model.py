import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import linear_model, neural_network
import matplotlib.pyplot as plt
import pickle


if __name__ == "__main__":
    df_data = pd.read_csv("training_data2.csv").fillna(0)
    # end_train = int(len(df_data.index)*9/10)

    weeks = list(range(1, 18))

    activations = ['relu']
    solvers = ['adam']
    shapes = [
        # (100, 100, 100, 100, 100),
        # (200, 200, 200, 200, 200),
        # (300, 300, 300, 300, 300),
        # (400, 400, 400, 400, 400),
        # (500, 500, 500, 500, 500),
        # (600, 600, 600, 600, 600),
        # (1000, 800, 500, 500, 500),
        # (1000, 800, 600, 400, 200),
        # (500, 400, 300, 200, 100),
        # (700, 500, 500, 300, 300),
        (1000, 500, 500, 500, 500),
        # (1000, 400, 400, 300, 300),
    ]
    res = [[] for s in shapes]
    res_2 = [[] for s in shapes]
    res_3 = [[] for s in shapes]
    x_3 = [[] for s in shapes]

    all_errors = []
    avg_errors = []
    standard_errors = []

    for week in weeks:
        
        end_x = len(df_data.columns)-2
        df_train_X = df_data[
            (df_data.season != 2021) | 
            (df_data.week<week)
        ].iloc[:, 0:end_x]
        df_test_X = df_data[
            (df_data.season == 2021) & 
            (df_data.week==week)
        ].iloc[:, 0:end_x]

        df_train_Y = df_data[
            (df_data.season != 2021) | 
            (df_data.week<week)
        ].iloc[:, end_x:]
        df_test_Y = df_data[
            (df_data.season == 2021) & 
            (df_data.week==week)
        ].iloc[:, end_x:]

        count = 0
        
        for active in activations:
            for solver in solvers:
                for i, shape in enumerate(shapes):
                    count+=1

                    filename = 'models/'+str(active)+'_'+str(solver)+'_'+str(shape)+'_week_'+str(week)+'.sav'
                    model = pickle.load(open(filename, 'rb'))

                    Y_pred = model.predict(df_test_X.iloc[:, 5:end_x])
                    Y_test = df_test_Y.to_numpy()
                    errors = Y_test-Y_pred
                    title = 'model errors week '+str(week)
                    # plt.hist(errors[:,0], bins=100)
                    # plt.ylabel('Number of errors in range')
                    # plt.xlabel('Error')
                    # plt.title(title)
                    # plt.savefig('model_errors_week_'+str(week)+'.png')
                    # plt.figure()
                    stdev = np.sqrt(sum(errors**2) / len(errors))
                    standard_errors.append(stdev)
                    average_error = sum(errors)/len(errors)
                    avg_errors.append(average_error)
                    all_errors = [*all_errors, *errors]
                    res[i].append(stdev[0])
                    res_2[i].append(average_error[0])
                    res_3[i].append(Y_test-Y_pred)
                    players = df_test_X.iloc[:, 1].to_numpy()
                    # print(players)
                    x_3[i].append([players, week])
                    # print(df_test_X[['player_id', 'week']])

        print('week =', week)

    # for i, shape in enumerate(shapes):
        # print(shape)
        # print(
        #     'Standard Error',
        #     np.sqrt(
        #         sum(
        #             np.array(res[i])**2
        #         ) / len(res[i])
        #     )
        # )
        # plt.plot(res[i])
        # plt.title('Standard Error in 2021')
        # plt.xlabel('Week')
        # plt.ylabel('Standard Error')
        # plt.figure()

        # print(
        #     'Average Error',
        #     sum(np.array(res_2[i])/len(res_2[i]))
        # )

        # plt.plot(res_2[i])
        # plt.title('Average Error in 2021')
        # plt.xlabel('Week')
        # plt.ylabel('Average Error')
        # plt.figure()

    header = ['week '+str(week) for week in weeks]
    header.insert(0, 'player_id')
    df_output = pd.DataFrame(columns=header)
    result = {}
    for Ys, Xs in zip(res_3[0], x_3[0]):
        for X, Y in zip(Xs[0], Ys):
            if X not in result:
                result[X] = {Xs[1]: Y[0]}
            else:
                result[X][Xs[1]] = Y[0] 
    
    for k in result:
        temp = [0 for w in weeks]
        temp.insert(0, k)
        for k2 in result[k]:
            temp[k2] = result[k][k2]

        plt.plot(temp[1:])
        plt.show()
        df_temp = pd.DataFrame([temp], columns=header)
        df_output = pd.concat([df_output, df_temp])

    df_output.to_csv('model_errors_2021.csv')

    all_errors = np.array(all_errors)
    stdev = np.sqrt(sum(all_errors**2)/len(all_errors))
    average_error = sum(all_errors)/len(all_errors)
    print(average_error)

    print('Standard Error is', stdev)
    print('Average Error is', average_error)

    plt.plot(weeks, avg_errors)
    plt.plot(weeks, standard_errors)
    plt.legend(['Average Error', 'Average Error PPR', 'Standard Error', 'Standard Error PPR'] )
    plt.title('2021 Model Projections Weekly Errors')
    plt.xlabel('Week')
    plt.ylabel('Error')
    plt.show()