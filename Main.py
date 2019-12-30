import soundfile as sf
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt


threshold = 155


def hps(param):
    res = np.copy(param)
    for i in range(2, 7):
        decimated = sig.decimate(param, i, ftype='fir')
        res[:len(decimated)] += decimated
    return res, np.argmax(res[:len(decimated)])


def process_signal(filename):
    signal, czestotliwosc = sf.read(filename)

    # Dealing with stereo input
    if len(np.shape(signal)) > 1:
        signal = signal.sum(axis=1) / 2

    shape = np.shape(signal)[0]
    signal = signal - np.mean(signal)
    signal = signal * np.kaiser(shape, 55)

    transformed = np.abs(np.fft.rfft(signal))
    transformed = transformed - np.mean(transformed)

    plt.figure(1)

    #Plot a signal spectrum
    a = plt.subplot(211)
    a.set_xlabel('Frame [s / freq]')
    a.set_ylabel('Volume')

    plt.plot(signal)

    # Plot a spectrogram from given file
    c = plt.subplot(212)

    hps_chart, max_arg = hps(transformed)

    plt.plot(hps_chart)

    c.set_xlabel('Frequency [Hz]')
    c.set_ylabel('Amplitude')
    plt.show()
    return max_arg


if __name__ == '__main__':

    men = []
    women = []
    corrupted_files = []

    files = ['001_K.wav', '002_M.wav', '003_K.wav', '004_M.wav', '005_M.wav', '006_K.wav', '007_M.wav', '008_K.wav',
             '009_K.wav', '010_M.wav', '011_M.wav', '012_K.wav', '013_M.wav', '014_K.wav', '015_K.wav', '016_K.wav',
             '017_M.wav', '018_K.wav', '019_M.wav', '020_M.wav', '021_M.wav', '022_K.wav', '023_M.wav', '024_M.wav',
             '025_K.wav', '026_M.wav', '027_M.wav', '028_K.wav', '029_K.wav', '030_M.wav', '031_K.wav', '032_M.wav',
             '033_M.wav', '034_K.wav', '035_M.wav', '036_K.wav', '037_K.wav', '038_M.wav', '039_M.wav', '040_K.wav',
             '041_K.wav', '042_M.wav', '043_M.wav', '044_K.wav', '045_M.wav', '046_K.wav', '047_K.wav', '048_K.wav',
             '049_M.wav', '050_K.wav', '051_K.wav', '052_M.wav', '053_M.wav', '054_K.wav', '055_K.wav', '056_M.wav',
             '057_K.wav', '058_M.wav', '059_K.wav', '060_K.wav', '061_M.wav', '062_K.wav', '063_M.wav', '064_M.wav',
             '065_M.wav', '066_K.wav', '067_K.wav', '068_K.wav', '069_K.wav', '070_M.wav', '071_M.wav', '072_K.wav',
             '073_K.wav', '074_K.wav', '075_M.wav', '076_M.wav', '077_K.wav', '078_M.wav', '079_K.wav', '080_M.wav',
             '081_K.wav', '082_M.wav', '083_K.wav', '084_M.wav', '085_K.wav', '086_K.wav', '087_M.wav', '088_K.wav',
             '089_M.wav', '090_M.wav', '091_M.wav']

    file = files[72]

    # for file in files:
    freq = process_signal('train/' + file)
    print(file, ", ", freq)

    if freq > 0:
        if file[4] == 'M':
            men.append(freq)
        else:
            women.append(freq)
    else:
        corrupted_files.append(file)

    # print('Kobiety')
    # print('Średnia: ', np.mean(women))
    # print('Max: ', np.max(women))
    # print('Min: ', np.min(women))
    # print()
    # print('Mężczyźni')
    # print('Średnia: ', np.mean(men))
    # print('Max: ', np.max(men))
    # print('Min: ', np.min(men))
    # print('\n')
