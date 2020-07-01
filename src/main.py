import GPy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import preprocessing

from utils.df_na import *

def labeling_dataset(train_x, test_x):
    for i, dtype in enumerate(train_x.dtypes):
        if dtype == 'object':
            col = train_x.columns[i]
            
            # ラベルリストの作成
            le = preprocessing.LabelEncoder()
            le.fit(train_x[col].values)

            # ラベルリストの修正（以下の場合に対処するため）
            ## train_x[col]に'None'がなく、test_x[col]に'None'がある時、
            ## le.classes_(ラベルリスト)に'None'がないので、test_x[col]に含まれる'None'にラベルを割り当てられない。
            if not np.any(le.classes_ == 'None'):
                le.classes_ = np.insert(le.classes_, 0, 'None')
            
            # ラベルの割り当て
            train_x[col] = le.transform(train_x[col].values)
            test_x[col]  = le.transform(test_x[col].values)
            
    return train_x, test_x

def normalizing_dataset(train_x, scaler_func):
    # normalize

    mm_list = []

    for i, dtype in enumerate(train_x.dtypes):
        # if dtype == 'object':
        col = train_x.columns[i]
        # ラベルリストの作成
        mm = scaler_func()
        mm.fit(train_x[col].values[:, None])
       
        # ラベルの割り当て
        train_x[col] = mm.transform(train_x[col].values[:, None])
        mm_list.append(mm)

    return train_x, mm_list

def _main():

    # データセットの読み込み
    train_x = pd.read_csv('../input/train.csv') 
    test_x = pd.read_csv('../input/test.csv')

    # print(train_x)

    # import ipdb; ipdb.set_trace()

    #隣接した道路の長さ（LotFrontage）の欠損値の補完（後のfill_na関数は0埋めしてしまうが、道路の長さは意味が変わってくるので、例外的に処理する）
    train_x['LotFrontage'] = train_x.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))
    test_x['LotFrontage'] = test_x.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))

    # 欠損値を埋める
    train_x = fill_na(train_x)
    test_x  = fill_na(test_x)

    # ラベリング（＝DataFrameに含まれるObject型のSeriesを、Int型に変換する）
    train_x, test_x = labeling_dataset(train_x, test_x)
    # train_x, mm_list = normalizing_dataset(train_x, preprocessing.MinMaxScaler)
    train_x, mm_list = normalizing_dataset(train_x, preprocessing.StandardScaler)

    kernel = GPy.kern.Matern52(train_x.shape[-1] - 1, ARD=True)
    # kernel = GPy.kern.RBF(1)
    # kernel = GPy.kern.RBF(1) + GPy.kern.Bias(1) + GPy.kern.Linear(1)

    model = GPy.models.GPRegression(train_x.drop(columns='SalePrice')[:1000], train_x["SalePrice"][:1000][:, None], kernel=kernel)
    model.optimize(messages=True, max_iters=1e5)
    # model.plot()
    # plt.savefig('output/fig3.png')

    my_first_story = train_x.values[0]
    fixed_inputs = []
    for i, v in enumerate(my_first_story):
        fixed_inputs.append((i, v))
    
    # import ipdb; ipdb.set_trace()

    for column in train_x.columns[:-1]:    
        free_index = int(np.where(train_x.columns == column)[0])
        model.plot(fixed_inputs=fixed_inputs[:free_index] + fixed_inputs[free_index+1:-1], plot_data=False)
        plt.savefig(f'output/fig3-slice_{column}.png')

    # prediction
    # x_pred = np.linspace(0, 100, 100)
    # x_pred = x_pred[:, None]
    # y_qua_pred = model.predict_quantiles(x_pred, quantiles=(2.5, 50, 97.5))[0]

if __name__=="__main__":
    _main()


