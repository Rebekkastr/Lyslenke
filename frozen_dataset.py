import time 
import serial 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 

MAX_SAMPLES = 2000 
dataset = []


def animate(i, dataList, ser): 
    global dataset 
    line = ser.readline().decode("ascii").strip()

    try: 