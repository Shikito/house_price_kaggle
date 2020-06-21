# House Price Kaggle

## 想定環境
- Windows 10


## インストール

1. 仮想環境のインストール
```python
cd house_price_kaggle
conda env create -n house_price_kaggle -f house_price_kaggle.yml python=3.7
```

2. データセットのインストール
```shell
activate house_price_kaggle
pip install kaggle
cd house_price_kaggle
kaggle competitions files -c house-prices-advanced-regression-techniques
```