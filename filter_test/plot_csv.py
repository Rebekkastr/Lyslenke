# Opprette to lister, en som forblir uendret og en som smoothing testes på
# Lese CSV fil til listene 
import csv 
import matplotlib.pyplot as plt 
import numpy as np 

unchanged_data = []
smooth_data = []

path = r"C:\Users\reba9\Documents\Git_repos\Lyslenke\dataset\data.csvb"

with open(path, mode = 'r') as file: 
    csvFile = csv.reader(file)
    next(csvFile) # skal ikke ha med header "Soundlevel" i listene
    for row in csvFile:
        value = float(row[0]) # legger inn tallet og ikke hver rad som en liste 
        unchanged_data.append(value)
        smooth_data.append(value)

fs_level = 8000 / 256 # 31,25 verdier per sekund
data = np.array(unchanged_data)
time = np.arange(len(data)) / fs_level # gjør det om til skunder 

start = 900 
stop = 1500 

plot_size = 800 
plt.figure()
plt.plot(time[start:stop], unchanged_data[start:stop], label = "Original signal")
plt.plot(time[start:stop], smooth_data[start:stop], label = "Smooth signal", linewidth = 2)
plt.title("Original vs Smooth sound signal")
plt.xlabel("Time in seconds")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.show()


