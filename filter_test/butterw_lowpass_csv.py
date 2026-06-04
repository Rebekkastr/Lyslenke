import csv 
import matplotlib.pyplot as plt 
import numpy as np 
from scipy.signal import butter, filtfilt

unchanged_data = []

path = r"C:\Users\reba9\Documents\Git_repos\Lyslenke\dataset\data.csv"

# Opening CSV file 
with open(path, mode = 'r') as file: 
    csvFile = csv.reader(file)
    next(csvFile) # skal ikke ha med header "Soundlevel" i listene
    for row in csvFile:
        value = float(row[0]) # legger inn tallet og ikke hver rad som en liste 
        unchanged_data.append(value)

# Creating a numpy-array from CSV-values 
data = np.array(unchanged_data)

# Samplingfrequency 
fs = 8000/256 

# Timeaxe 
time = np.arange(len(data)) / fs 

# Apply butterworth low-pass filter 
def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low')
    return filtfilt(b, a, data)

cutoff = 5 # starting low because fs = 31.25 Hz 
filtered_data = butter_lowpass_filter(data, cutoff, fs)
 
# Area to plot rom CSV file 
start = 900
stop = 1500 

plt.figure(figsize=(10, 4))
plt.plot(time[start:stop], data[start:stop], label="Original signal")
plt.plot(time[start:stop], filtered_data[start:stop], label="Filtered signal", linewidth=2)
plt.title("Original vs Butterworth Low-pass")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.show()