# CSVファイルの文字化け
# https://qiita.com/devrookiecom/items/faf2b6ee6f9e058022cc
# 書き込みで謎の改行が入る
# https://qiita.com/ryokurta256/items/defc553f5165c88eac95

import csv

def addwriteCsv(date, time, contents, openFileName = "csvTes.csv"):
    file = open(openFileName, 'a', newline="")
    w = csv.writer(file)
    w = w.writerow([date,time,contents])
    file.close()

def readCsv(openFileName = "csvTes.csv"):
    file = open(openFileName, 'r')
    data = csv.reader(file)
    for row in data:
        for col in row:
            print(col, end=',')
        print()
    file.close()