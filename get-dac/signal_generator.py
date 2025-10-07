import numpy as np
import time

def get_sin_wave_amplitude(freq, time):
    signal = np.sin(2*np.pi*freq*time)
    shifted = signal+1
    normalized = shifted / 2.0
    return normalized

def wait_for_sampling_period(sampling_frequency):
    if sampling_frequency <= 0:
        raise ValueError("Частота дискретизации должна быть положительной. Введите еще раз.\n")
    
    period = 1.0 / sampling_frequency
    time.sleep(period)