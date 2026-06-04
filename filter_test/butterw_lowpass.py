import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

fs = 1000
t = np.linspace(0, 1, fs, endpoint=False)
signal = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*120*t) + 0.5*np.random.randn(fs)

def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low')
    return filtfilt(b, a, data)

cutoff = 100  
filtered = butter_lowpass_filter(signal, cutoff, fs)

plt.figure(figsize=(10,4))
plt.plot(t, signal, label='Original Signal')
plt.plot(t, filtered, label='Low-pass Filtered', color='blue')
plt.title('Butterworth Low-pass Filter')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.show()