import spidev
import tkinter as tk
import time
import numpy as np
import lgpio
import PinNumbers

# Constants
SPI_BUS = 0
SPI_DEVICE_DAC = 1  # DAC on CE1 (GPIO 10)
SAMPLE_RATE = 5000  # Hz (Adjust for smoothness vs performance)
AMPLITUDE = 32767  # 16-bit max value (for full-scale DAC output)
WAVEFORM_TYPE = "sine"  # Options: "sine", "square", "triangle"
CYCLE = 1 / SAMPLE_RATE

# GPIO Setup
chip = lgpio.gpiochip_open(0)  # Open GPIO chip
spi_dac = spidev.SpiDev()
spi_dac.open(SPI_BUS, SPI_DEVICE_DAC)
spi_dac.max_speed_hz = 50000000
spi_dac.mode = 0b00  # Mode for DAC82001

# Generate Waveform Data
def generate_waveform(samples=100):
    if WAVEFORM_TYPE == "sine":
        return [int(AMPLITUDE * (np.sin(2 * np.pi * i / samples) + 1) / 2) for i in range(samples)]
    elif WAVEFORM_TYPE == "square":
        return [AMPLITUDE if i < samples / 2 else 0 for i in range(samples)]
    elif WAVEFORM_TYPE == "triangle":
        return [int(AMPLITUDE * (2 * abs(2 * (i / samples) - 1))) for i in range(samples)]
    return []

waveform_data = generate_waveform()

# Function to Output Waveform Continuously
def output_waveform():
    while running:
        for value in waveform_data:
            data_bytes = [(value >> 8) & 0xFF, value & 0xFF]  # 16-bit format
            lgpio.gpio_write(chip, PinNumbers.SYNC, 0)  # Start frame
            spi_dac.xfer2(data_bytes)
            lgpio.gpio_write(chip, PinNumbers.SYNC, 1)  # End frame
            time.sleep(CYCLE)  # Control waveform frequency

# GUI Setup
root = tk.Tk()
root.title("Waveform Generator")
running = True

def quit_program():
    global running
    running = False
    spi_dac.close()
    lgpio.gpiochip_close(chip)
    root.destroy()
    print("Program exited.")

tk.Label(root, text="DAC Waveform Output", font=("Arial", 18)).pack(pady=10)
tk.Button(root, text="Quit", font=("Arial", 14), command=quit_program).pack(pady=20)

# Start Waveform Output
import threading
wave_thread = threading.Thread(target=output_waveform)
wave_thread.daemon = True
wave_thread.start()

root.mainloop()
