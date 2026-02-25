import numpy as np 
import time 

def get_sin_wave_amplitude(freq,t):
    raw_sin = np.sin(2*np.pi*freq*t)

    shift_sin = raw_sin + 1 

    norm_sin = shift_sin / 2 

    return norm_sin 

def wait_for_sampling_period(samp_freq):
    samp_period = 1/samp_freq
    time.sleep(samp_period)