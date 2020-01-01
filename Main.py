import soundfile as sf
import numpy as np
import sys
import scipy.signal as sig


def determine_sex(input_freq, threshold):
    if input_freq > threshold:
        return 'K'
    else:
        return 'M'


def hps(param):
    res = np.copy(param)
    length = 0
    for i in range(2, 6):
        decimated = sig.decimate(param, i)
        length = len(decimated)
        res[:length] += decimated
    return res, np.argmax(res[:length])


def process_signal(filename):
    signal, sample_rate = sf.read(filename)
    channels = len(np.shape(signal))

    # Dealing with stereo input
    if channels > 1:
        signal = signal.sum(axis=1) / 2

    signal = signal - np.mean(signal)
    signal = signal * np.kaiser(len(signal), 40)

    max_freq = 5000
    min_freq = 60

    transformed = np.log(np.abs(np.fft.fft(signal)))
    transformed = transformed - np.mean(transformed)
    transformed = transformed[:max_freq]

    for i in range(0, min_freq):
        transformed[i] = 0

    hps_chart, max_arg = hps(transformed)

    return sample_rate * max_arg / len(signal)


if __name__ == '__main__':

    try:
        filename = sys.argv[1]
        freq = process_signal(filename)
        result = determine_sex(freq, 150)
        print(result)
    except FileNotFoundError:
        print('M')
        exit(0)



