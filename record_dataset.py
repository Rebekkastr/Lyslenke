# importerer time (), serial (kommunikasjon over USB-C) og CSV (for lagring til CSV fil)
import time 
import serial 
import csv

PORT = "COM4" # Definerer hvilken port som skal brukes 
BAUD = 115200 # ønsker 115200 bits per sekund fra ESP32 til PC
N_SAMPLES = 2000 # Antall samples jeg vil ha til CSV filen

ser = serial.Serial(PORT, BAUD, timeout = 1) # starter kommunikasjonen mellom PC-en og ESP32 
time.sleep(2) 

dataset = []

print("Steg 1: ta opp 2000 samples")

while len(dataset) < N_SAMPLES: 
    line = ser.readline().decode("ascii").strip()

    try: 
        value = float(line)
        dataset.append(value)
        print(len(dataset))
    except: 
        pass 

print("Steg 1 fullført, lagrer til CSV")

# åpner og lager en csv fil kalt data.csv 
with open("data.csv", "w", newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(["Soundlevel"]) # header på første rad 
    for values in dataset: 
        csvwriter.writerow([values]) # legger til alle dataene fra dataset til csv filen. 
ser.close()

print("Lagringen til CSV er ferdig.")