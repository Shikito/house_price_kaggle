# House Price Kaggle

## 想定環境
- Windows 10


## インストール

1. 仮想環境のインストール
```shell
$ cd house_price_kaggle
$ (Get-Content -Path "house_price_kaggle.yml" -Encoding Default) -join "`n" ` 
 | % { [Text.Encoding]::UTF8.GetBytes($_) } `
 | Set-Content -Path "house_price_kaggle.yml" -Encoding Byte
$ conda env create -f house_price_kaggle.yml
```

2. データセットのインストール
```shell
$ activate house_price_kaggle
$ pip install kaggle
$ cd house_price_kaggle
$ kaggle competitions download -c house-prices-advanced-regression-techniques
$ Expand-Archive house-prices-advanced-regression-techniques.zip
$ ren house-prices-advanced-regression-techniques input
$ rm house-prices-advanced-regression-techniques.zip
```
