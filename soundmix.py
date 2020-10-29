import wave, numpy, struct


def upVolume(filename): 
    # Open
    w = wave.open(filename,"rb")
    p = w.getparams()
    f = p[3] # number of frames
    s = w.readframes(f)
    w.close()

    # Edit
    s = numpy.fromstring(s, numpy.int16) * 5 / 10  # half amplitude
    s = struct.pack('h'*len(s), *s)

    # Save
    w = wave.open(filename,"wb")
    w.setparams(p)
    w.writeframes(s)
    w.close()