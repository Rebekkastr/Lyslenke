# This code analyses the frequency and divides it into bass, mid and treble. 
import csv 
from pathlib import Path
import numpy as np 
import matplotlib.pyplot as plt 

# ---- Configurations - create a new file for this? ----
# 1 second window with a samplingfrequency of 8000. Start set to 2 seconds after the thone has begun. 
SAMPLE_RATE = 8000 
WINDOW_SECONDS = 1 
START_SECOND = 2 

# Path to the CSV file containing the recorded autdio samples 
CSV_PATH = Path(
    r"C:\Users\reba9\Documents\Git_repos\Lyslenke\csv\frequency.csv"
)

# Defining the frequency ranges for bass, mid and treble, given in Hz.
FREQUENCY_BANDS = {
    "Bass": (20, 250),
    "Mid": (250, 2000), 
    "Treble": (2000, 4000),
}

# Defining the temporary reference magnitude values for each frequency band 
# --- Will calibrate the values later using different songs ---
REFERENCE_VALUES = {
    "Bass": 4_000_000,
    "Mid": 20_000_000,
    "Treble": 500_000,
}


# -----------------------------
# Functions
# -----------------------------


def read_audio_samples(path):
    data = [] # empty list for sounddata 
    """Function that reads the recorded audio samples from a CSV file."""
    with path.open("r", newline="") as file: # opening the csv file using path
        csv_file = csv.reader(file)
        next(csv_file, None)  # Skip header

        for row in csv_file:
            if not row:
                continue

            try:
                data.append(float(row[0])) # from string to float 
            except ValueError:
                print(f"Skipping invalid value: {row[0]}") # handling error 

    return np.array(data, dtype=float) # Returning a numpy array


def select_analysis_window(data, sample_rate, start_second, window_seconds):
    number_of_samples = int(sample_rate * window_seconds) 
    """This function sets the window for how much data to retrieve from the recorded data. """
    start_index = int(start_second * sample_rate)
    stop_index = start_index + number_of_samples

    signal = data[start_index:stop_index] # Extracting data using start and stop index

# Securing that there is enough samples in the extracted data 
    if len(signal) < number_of_samples:
        raise ValueError(
            f"Not enough samples. Expected {number_of_samples}, "
            f"but found {len(signal)}."
        )
    
    return signal


def calculate_fft(signal, sample_rate):
    """This function converst the time-domain singal into frequency-domain."""
    number_of_samples = len(signal) # count number of samples in selected window 

    # Remove DC offset
    signal = signal - np.mean(signal)  # Remove the average value so the signal oscillates around zero 

    # Applying FFT and finding the magnitude
    fft_values = np.fft.rfft(signal)
    fft_magnitude = np.abs(fft_values)

    # Create frequencyaxes 
    frequencies = np.fft.rfftfreq(
        number_of_samples,
        d=1 / sample_rate,
    )

    return frequencies, fft_magnitude # returning two NumPy-arrays


def find_peak(frequencies, magnitudes):
    """Find the frequency and magnitude of the highest peak."""
    peak_index = np.argmax(magnitudes)

    peak_frequency = frequencies[peak_index]
    peak_magnitude = magnitudes[peak_index]

    return peak_frequency, peak_magnitude


def find_band_peak(frequencies, magnitudes, lower_limit, upper_limit):
    """Find the highest FFT peak inside one frequency band."""
    # Create a mask that selects only the desired frequency band
    band_mask = (
        (frequencies >= lower_limit)
        & (frequencies < upper_limit)
    )

    # Retrieve the frequencies and magnitudes within the band  
    band_frequencies = frequencies[band_mask]
    band_magnitudes = magnitudes[band_mask]

    # Stops the script if no FFT values were found in the selected frequency band 
    if len(band_magnitudes) == 0:
        raise ValueError(
            f"No FFT values found between "
            f"{lower_limit} Hz and {upper_limit} Hz."
        )

    return find_peak(band_frequencies, band_magnitudes) # Using the find_peak function to return the peak withing the bands. 


def get_led_level(magnitude, reference):
    """Convert magnitude to an LED level from 0 to 3."""
    if reference <= 0:
        raise ValueError("Reference value must be greater than zero.")

    percentage = magnitude / reference

    if percentage < 0.25:
        return 0
    elif percentage < 0.50:
        return 1
    elif percentage < 0.75:
        return 2
    else:
        return 3


def display_leds(level):
    """Create a simple text representation of three LEDs."""
    return "*" * level + "-" * (3 - level)


def plot_frequency_spectrum(frequencies, magnitudes):
    """Plot the FFT frequency spectrum."""
    plt.plot(frequencies, magnitudes)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("FFT frequency spectrum")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# -----------------------------
# Main program
# -----------------------------

def main():
    data = read_audio_samples(CSV_PATH)

    signal = select_analysis_window(
        data=data,
        sample_rate=SAMPLE_RATE,
        start_second=START_SECOND,
        window_seconds=WINDOW_SECONDS,
    )

    frequencies, fft_magnitude = calculate_fft(
        signal=signal,
        sample_rate=SAMPLE_RATE,
    )

    overall_frequency, overall_magnitude = find_peak(
        frequencies,
        fft_magnitude,
    )

    print(f"Peak frequency: {overall_frequency:.1f} Hz")
    print(f"Peak magnitude: {overall_magnitude:.1f}")
    print()

    band_results = {}

    for band_name, frequency_range in FREQUENCY_BANDS.items():
        lower_limit, upper_limit = frequency_range

        peak_frequency, peak_magnitude = find_band_peak(
            frequencies=frequencies,
            magnitudes=fft_magnitude,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
        )

        led_level = get_led_level(
            magnitude=peak_magnitude,
            reference=REFERENCE_VALUES[band_name],
        )

        band_results[band_name] = {
            "frequency": peak_frequency,
            "magnitude": peak_magnitude,
            "led_level": led_level,
        }

    for band_name, result in band_results.items():
        print(
            f"{band_name}: "
            f"{result['frequency']:.1f} Hz, "
            f"magnitude {result['magnitude']:.1f}"
        )

    print()

    for band_name, result in band_results.items():
        led_level = result["led_level"]

        print(
            f"{band_name} LEDs: "
            f"{led_level} "
            f"{display_leds(led_level)}"
        )

    plot_frequency_spectrum(
        frequencies,
        fft_magnitude,
    )


if __name__ == "__main__":
    main()

