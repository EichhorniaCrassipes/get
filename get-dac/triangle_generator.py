import numpy as np
import time
from math import *

def get_triangle_amplitude(freq, time):
    x = time*freq
    signal = abs(2*(x - floor(x))-1)
    shifted = signal+1
    normalized = shifted / 2
    return normalized

def wait_for_sampling_period(sampling_frequency):
    if sampling_frequency <= 0:
        raise ValueError("Частота дискретизации должна быть положительной. Введите еще раз.\n")
    
    period = 1.0 / sampling_frequency
    time.sleep(period)