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

def _main():

    # データセットの読み込み
    train_x = pd.read_csv('../input/train.csv') 
    test_x = pd.read_csv('../input/test.csv')

    #隣接した道路の長さ（LotFrontage）の欠損値の補完（後のfill_na関数は0埋めしてしまうが、道路の長さは意味が変わってくるので、例外的に処理する）
    train_x['LotFrontage'] = train_x.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))
    test_x['LotFrontage'] = test_x.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))

    # 欠損値を埋める
    train_x = fill_na(train_x)
    test_x  = fill_na(test_x)

    # ラベリング（＝DataFrameに含まれるObject型のSeriesを、Int型に変換する）
    train_x, test_x = labeling_dataset(train_x, test_x)
    
    # print(train_x)
    # print(test_x)

if __name__=="__main__":
    _main()


