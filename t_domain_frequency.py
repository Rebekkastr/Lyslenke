# Create a timedomain for frequency.wav

import csv 
import numpy as np
import matplotlib.pyplot as plt

data = []

path = r"C:\Users\reba9\Documents\Git_repos\Lyslenke\csv\frequency.csv"

with open(path, "r") as file: 
    csvFile = csv.reader(file)
    next(csvFile)

    for row in csvFile: 
        if len(row) > 0:
            data.append(float(row[0]))


fs = 8000
time = np.arange(len(data)) / fs 
start_time = 1.2
duration = 0.05 
start = int(start_time * fs)
stop = int((start_time + duration) * fs)

plt.figure()
plt.plot(time[start:stop], data[start:stop])
plt.title("Time domain of single frequency")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

