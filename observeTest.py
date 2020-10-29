# iPhoneでpython
# https://news.mynavi.jp/article/zeropython-56/
import speech_recognition as sr
# ライブラリの読込
import pyaudio
import wave
import numpy as np
from datetime import datetime
import queue as q
import os
import pydub
from pydub import AudioSegment
# 自作関数
import csvOperate
import getLocalfileName as getFN

preAudioFileNameQ  = q.Queue()
postAudioFileNameQ = q.Queue()

# # もちろんネットにつながってくれていないとダメ
# pythonのSpeechRecognitionを使って音声認識
# https://qiita.com/seigot/items/62a85f1a561bb820532a
def fileRecognition(AUDIO_FILE = "gootes.wav"):
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    try:
        print("Prepare Recognize ")
        result=r.recognize_google(audio, language='ja-JP')
        print("Google Speech Recognition thinks you said " + result)
        return result
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "understand audio"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "miss request"

# 音を監視して一定以上の音量を録音する
# https://qiita.com/mix_dvd/items/dc53926b83a9529876f7
def RecordAudio(threshold = 0.1, RECORD_SECONDS = 5.0):#閾値
    # バージョンの表示 1.18.5
    # print(np.__version__)
    # 音データフォーマット
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5

    # 音の取込開始
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = chunk
    )

    while True:
        # 音データの取得
        data = stream.read(chunk)
        # ndarrayに変換
        x = np.frombuffer(data, dtype="int16") / 32768.0

        # 閾値以上の場合はファイルに保存
        if x.max() > threshold:
            filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".wav"
            preAudioFileNameQ.put(filename)
            print("Record",filename)

            # RECORD_SECONDS秒間の音データを取込
            all = []
            all.append(data)
            for ii in range(0, int(RATE / chunk * int(RECORD_SECONDS))):
                data = stream.read(chunk)
                all.append(data)
            data = b''.join(all)

            # 音声ファイルとして出力
            out = wave.open(filename,'w')
            out.setnchannels(CHANNELS)
            out.setsampwidth(2)
            out.setframerate(RATE)
            out.writeframes(data)
            out.close()

            print("Audio File Saved.")
            return filename
    stream.close()
    p.terminate()

# preQ内にある音声ファイルをspeechrecognaizeにいれる
def srFromQ():
    # キューからデータがなくなるまで取り出しを行う
    while not preAudioFileNameQ.empty():
        name = str(preAudioFileNameQ.get())
        postAudioFileNameQ.put(name)
        contents = fileRecognition(name)#音声認識の結果をcontentsに入れる
        if(contents=="understand audio"):
            os.remove(name)
        csvOperate.addwriteCsv(date = name[:8], time = name[8:14], contents = contents, openFileName = "csvTes.csv")

# 音声ファイルの音量を変える（Pydub）
# https://qiita.com/nyancook/items/786cffd0b07bad8b4444
def ChangeAudioVolume(FILE_NAME = "20201029164210.wav"):
    base_sound = AudioSegment.from_file(FILE_NAME, format="wav")  # 音声を読み込み
    # base_sound = base_sound + 10　#nデシベル音量を挙げる（※解析が必要）
    base_sound.export("Volume"+FILE_NAME, format="wav")
    print("Volume Up Audio File Saved")

# pa = pyaudio.PyAudio()
# for i in range(pa.get_device_count()):
#     print(pa.get_device_info_by_index(i))
filename = "NonDirect1_self.wav"
while True:
    # sound = pydub.AudioSegment.from_mp3("tomo1013_1.mp3")
    # sound.export("output.wav", format="wav")
    # if(preAudioFileNameQ.empty()):
    filename = RecordAudio(threshold=0.0, RECORD_SECONDS=3.0)# 一定の閾値で音声の録音をスタート
    contents = fileRecognition(filename)#音声認識の結果をcontentsに入れる
    ChangeAudioVolume(FILE_NAME = filename)
    if(contents=="understand audio"):#何も認識できなければ音声ファイルを削除する
        os.remove(filename)
        os.remove("Volume"+filename)
    else:
        csvOperate.addwriteCsv(date = filename[:8], time = filename[8:14], contents = contents, openFileName = "csvTes.csv")
        
