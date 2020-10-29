# Python3入門 フォルダ内のファイル一覧を取得する方法
# https://weblabo.oscasierra.net/python/python3-beginning-file-list.html

import glob

def  addwriteCsv():
    files = glob.glob("./compairVoiceFolder/*")
    for file in files:
        print(file)
    return "tes"+".wav"

