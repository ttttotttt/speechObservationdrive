import soundfile as sf
 
def wavload(path):
    data, samplerate = sf.read(path)
    return data, samplerate

import wave
import numpy as np
from matplotlib import pyplot as plt
def wave_plot(path="NonDirect1_self.wav"):

    data, samplerate = wavload(path)
    
    t = np.arange(0, len(data))/samplerate
    plt.plot(t, data)
    plt.show()
    plt.close()

wave_plot("Direct1_self.wav")
wave_plot()



# http://ism1000ch.hatenablog.com/entry/2014/05/13/175911
# #coding:utf-8
# import wave
# import numpy as np
# import matplotlib.pyplot as plt

# def wave_plot(filename="NonDirect1_self.wav"):
#     # open wave file
#     wf = wave.open(filename,'r')
#     print(wf.getparams())

#     # load wave data
#     chunk_size = 1024
#     amp  = (2**8) ** wf.getsampwidth() / 2
#     data = wf.readframes(chunk_size)   # バイナリ読み込み
#     data = np.frombuffer(data,'int16') # intに変換
#     data = data / amp                  # 振幅正規化

#     # make time axis
#     rate = wf.getframerate()  # フレームレート[1/s]
#     size = float(chunk_size*2)  # 波形サイズ
#     x = np.arange(0, size/rate, 1.0/rate) # 
#     print(x)

#     # plot
#     plt.plot(x,data)
#     plt.show()

# wave_plot()