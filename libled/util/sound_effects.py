# -*- coding: utf-8 -*-
import struct
import numpy as np
# import scipy.signal as sg


# defines
CHUNK = 1024
MAX_x16 = 32768.0
MAX_x32 = 2147483648.0


def get_buffer(input_data, samplewidth=2):
    if samplewidth == 2:
        d = np.frombuffer(input_data, np.int16)
        d = d.astype(np.float32)
    elif samplewidth == 4:
        d = np.frombuffer(input_data, np.int32)
    return d


def set_buffer(input_data):
    d = input_data
    # d = d.astype(np.int16)
    return struct.pack('h' * len(d), *d)


def gain(input_data, gain):
    output_data = input_data * gain
    return output_data


def resamplingrate(input_data, src_fs=44100, dst_fs=44100):
    # 正規化 -1 ~ 1
    d = input_data / MAX_x16

    if src_fs < dst_fs:
        # upsampling
        d = upsampling(d, src_fs, dst_fs)
    else:
        # downsampling
        d = downsampling(d, src_fs, dst_fs)

    # 正規化 -32768 ~ 32767
    out_d = [int(x * 32767.0) for x in d]
    return out_d


def upsampling(input_data, src_fs, dst_fs):
    return input_data


def downsampling(input_data, src_fs, dst_fs):
    return input_data
