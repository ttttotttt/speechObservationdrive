import pydub
import os
import sys

def mp3ToWav(FILE_NAME):
    mp3 = sys.argv[1]
    # print(f"IN:{mp3}")

    dirname = os.path.dirname(mp3)
    # baseName = os.path.splitext(os.path.basename(mp3))[0]
    wav = os.path.join(dirname, f"{FILE_NAME}.wav")
    print(f"OUT:{wav}")

    audio = pydub.AudioSegment.from_mp3(FILE_NAME)
    return audio.export(wav, format='wav')