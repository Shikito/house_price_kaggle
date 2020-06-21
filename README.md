# House Price Kaggle

## 想定環境
- Windows 10


## インストール

1. 仮想環境のインストール

house_price_kaggleディレクトリで以下を実行

```shell
(Get-Content -Path "house_price_kaggle.yml" -Encoding Default) -join "`n" `  | % { [Text.Encoding]::UTF8.GetBytes($_) } ` | Set-Content -Path "house_price_kaggle.yml" -Encoding Byte
conda env create -f house_price_kaggle.yml
```

2. データセットのインストール

house_price_kaggleディレクトリで以下を実行

```shell
activate house_price_kaggle
pip install kaggle
kaggle competitions download -c house-prices-advanced-regression-techniques
Expand-Archive house-prices-advanced-regression-techniques.zip
ren house-prices-advanced-regression-techniques input
rm house-prices-advanced-regression-techniques.zip
```

## 仮想環境の更新(パッケージの追加/削除を反映)
```shell
conda env export -n house_price_kaggle > house_price_kaggle.yml
conda env update -f house_price_kaggle.yml
```
## 使い方
```shell
cd src
python main.py # 訓練データが表示されます
```
