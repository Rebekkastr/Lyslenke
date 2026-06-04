#generates multiple an accord 

import numpy as np
from scipy.io.wavfile import write 

SAMPLE_RATE = 44100 
DURATION = 5.0 

def sine_wave(freq, duration, volume=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return volume * np.sin(2 * np.pi * freq * t)

# Accord: C-major = C4, E4, G4 
tone = (
   sine_wave(261.63, DURATION, 0.3) + 
   sine_wave(329.63, DURATION, 0.3) + 
   sine_wave(392.00, DURATION, 0.3) 
 )

# Normalize 
tone = tone/np.max(np.abs(tone))

# Convert to 16 bit WAV
audio = np.int16(tone * 32767)

write("accord.wav", SAMPLE_RATE, audio)
print("Saved accord.wav")