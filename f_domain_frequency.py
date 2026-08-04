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

signal = np.array(data)
fs = 8000 
N = len(signal)

fft_values = np.fft.rfft(signal)
fft_magnitude = np.abs(fft_values)

frequencies = np.fft.rfftfreq(N, d=1/fs)

plt.figure()
plt.plot(frequencies, fft_magnitude)
plt.title("FFT of single frequency")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.xlim(0, 1000)
plt.grid(True)
plt.show()