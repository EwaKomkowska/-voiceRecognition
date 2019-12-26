import wave
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt


def chooseSex():
    return


def inputSignal (fileName):
    signal_wave = wave.open(fileName, 'r')
    sample_frequency = 16000
    data = np.fromstring(signal_wave.readframes(sample_frequency), dtype=np.int16)
    sig = signal_wave.readframes(-1)
    sig = np.fromstring(sig, 'Int16')

    sig = sig[:]

    #sig = sig[25000:32000]
    left, right = data[0::2], data[1::2]
    lf, rf = abs(np.fft.rfft(left)), abs(np.fft.rfft(right))

    plt.figure(1)
    a = plt.subplot(211)
    a.set_xlabel('time [s]')
    a.set_ylabel('sample value [-]')
    plt.plot(sig)
    c = plt.subplot(212)
    Pxx, freqs, bins, im = c.specgram(sig, NFFT=1024, Fs=16000, noverlap=900)
    c.set_xlabel('Time')
    c.set_ylabel('Frequency')
    plt.show()
    return


if __name__ == '__main__':

    for i in range(1, 10):
        try:
            #fileName = input("Podaj nazwe pliku")
            fileName = 'train/00' + str(i) + '_K.wav'
            inputSignal(fileName)
        except FileNotFoundError:
            fileName = 'train/00' + str(i) + '_M.wav'
            inputSignal(fileName)
            #print("Podany plik nie istnieje")
