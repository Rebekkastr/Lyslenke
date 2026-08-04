#generates one frequency/one note in a file called frequence.wav

import numpy as np
from scipy.io.wavfile import write 

SAMPLE_RATE = 44100 
DURATION = 5.0 

def sine_wave(freq, duration, volume=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return volume * np.sin(2 * np.pi * freq * t)

# 1 frekvens: A4 = 440 Hz 
tone = sine_wave(440, DURATION)

# Normaliser 
tone = tone/np.max(np.abs(tone))

# Konverter til 16 bit WAV
audio = np.int16(tone * 32767)

write("one_tone.wav", SAMPLE_RATE, audio)
print("Saved frequence.wav")