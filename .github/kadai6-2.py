import requests
import pandas as pd
from datetime import datetime

# 参照オープンデータ：気象庁「過去の気象データダウンロード」
# 概要：日本国内の気象観測データを都道府県・地点ごとに取得可能。
# エンドポイント：気象庁提供のCSVファイル
# 使い方：URLに都道府県番号、地点番号、年月日を指定し、CSVを取得可能

# 2024年6月の「東京・千代田区（東京）」の気温データを取得
# 東京都 = prefCode=44, 千代田 = blockNo=47662
PREF_CODE = 44
BLOCK_NO = 47662
YEAR = 2024
MONTH = 6

# CSVファイルのURL
CSV_URL = (
    f"https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php"
    f"?prec_no={PREF_CODE}&block_no={BLOCK_NO}&year={YEAR}&month={MONTH}&view=p1"
)

# 上記URLはHTMLページなので、実際にはCSVを別URLで取得する
# 気象庁の仕様に従い、CSVファイルは POST リクエストでダウンロードする必要あり
# pandasの read_html を使ってテーブルを抽出

print(f"{YEAR}年{MONTH}月の東京都千代田区（東京）の気象データを取得中...")

# pandasでHTMLテーブルを直接取得
tables = pd.read_html(CSV_URL, encoding="utf-8")

# 最初のテーブルが日ごとの気象データ
df = tables[0]

# 不要な行や列の処理
df = df[pd.to_numeric(df['日'], errors='coerce').notnull()]
df.reset_index(drop=True, inplace=True)

# 列名をわかりやすく変更
df.rename(columns={
    '日': '日付',
    '平均気温(℃)': '平均気温',
    '最高気温(℃)': '最高気温',
    '最低気温(℃)': '最低気温'
}, inplace=True)

# 日付列を年月日形式に整形
df['日付'] = df['日付'].astype(int)
df['年月日'] = df['日付'].apply(lambda d: f"{YEAR}-{MONTH:02d}-{d:02d}")
df = df[['年月日', '平均気温', '最高気温', '最低気温']]

# 結果表示
print(df)
