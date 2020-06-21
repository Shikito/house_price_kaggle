import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# データの欠損値を取得
def get_na(all_data):
    return all_data.isnull().sum()[all_data.isnull().sum()>0].sort_values(ascending=False)

# 列ごとの欠損値の数を棒グラフで表示
def plot_na_bar(all_data):
    all_data_na = get_na(all_data)
    plt.figure(figsize=(20,10))
    plt.xticks(rotation='90')
    sns.barplot(x=all_data_na.index, y=all_data_na)
    plt.show()

# ---------- 欠損値を埋める関数  -----------------------------------#
# - float型には0を、object型には'None'を代入                         #
# - これ以外の欠損値処理がしたい場合は、この関数の前に処理をしておくこと # 
# ---------------------------------------------------------------- #
def fill_na(all_data : pd.DataFrame):

    all_data_na = get_na(all_data)
    # 欠損値があるカラムをリスト化
    na_col_list = all_data.isnull().sum()[all_data.isnull().sum()>0].index.tolist()

    #欠損があるカラムのデータ型を確認
    all_data[na_col_list].dtypes.sort_values()

    #欠損値が存在するかつfloat型のリストを作成
    float_list = all_data[na_col_list].dtypes[all_data[na_col_list].dtypes == "float64"].index.tolist()

    #欠損値が存在するかつobject型のリストを作成
    obj_list = all_data[na_col_list].dtypes[all_data[na_col_list].dtypes == "object"].index.tolist()

    #float型の場合は欠損値を0で置換
    all_data[float_list] = all_data[float_list].fillna(0)

    #object型の場合は欠損値を"None"で置換
    all_data[obj_list] = all_data[obj_list].fillna("None")

    #欠損値が全て置換できているか確認
    all_data.isnull().sum()[all_data.isnull().sum() > 0]

    return all_data