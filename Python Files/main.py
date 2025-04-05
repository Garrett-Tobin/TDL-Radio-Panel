import spidev
import tkinter as tk
import time
import PinNumbers
import functions
import lgpio

# Global Variables
initial_state = True
output_filename = "captured_output.txt"
SPI_BUS = 0  # SPI bus number
SPI_DEVICE_ADC = 0  # ADC on CE0 (GPIO 9 (MISO)) originally GPIO 22
SPI_DEVICE_DAC = 1  # DAC on CE1 (GPIO 10 (MOSI)) originally GPIO 16
captureTime = 0
delayTime = 0
captured_data = []  # Store 32-bit signals
CYCLE = 1/(50e6)

# GPIO Setup
try:
    chip = lgpio.gpiochip_open(0)  # Open GPIO chip for pin control
except Exception as e:
    print(f"Error initializing GPIO chip: {e}")
    exit()

# Functions for handling PCB Devices
def reset_devices():
    """Resets the ADC (ADS8681W) and DAC (DAC82001) using RST and RESET pins"""
    try:
        print("Resetting ADC (ADS8681W) and DAC (DAC82001)...")
        # Set both reset pins LOW
        lgpio.gpio_write(chip, PinNumbers.RST, 0)  # Reset ADC
        lgpio.gpio_write(chip, PinNumbers.RESET, 0)  # Reset DAC
        time.sleep(0.1)  # 10ms delay (ensure proper reset)

        # Set both reset pins HIGH
        lgpio.gpio_write(chip, PinNumbers.RST, 1)
        lgpio.gpio_write(chip, PinNumbers.RESET, 1)
        time.sleep(0.1)  # Wait after reset

        print("Reset complete. Initializing SPI...")
    except Exception as e:
        print(f"Error resetting devices: {e}")

reset_devices()

# Initialize SPI
try:
    spi_adc = spidev.SpiDev()
    spi_dac = spidev.SpiDev()
    spi_adc.open(SPI_BUS, SPI_DEVICE_ADC)
    spi_dac.open(SPI_BUS, SPI_DEVICE_DAC)
    spi_adc.max_speed_hz = 50000000  # 50 MHz per ADS8681W datasheet
    spi_dac.max_speed_hz = 50000000  # 50 MHz per DAC82001 datasheet
    spi_adc.mode = 0b00  # Mode for ADS8681W
    spi_dac.mode = 0b00  # Mode for DAC82001
except Exception as e:
    print(f"Error initializing SPI devices: {e}")
    exit()

# Initialize Pins for ADC (ADS8681W) and DAC (DAC82001)
try:
    functions.setupPins(chip)
except Exception as e:
    print(f"Error setting up pins: {e}")

# GUI Handlers
def handleCaptureButton():
    global captureTime
    try:
        captureTime = int(functions.grabCaptureTime(captureDisplay_lbl, captureTime_SpinBox))
    except Exception as e:
        print(f"Error handling capture time input: {e}")

def handleDelayButton():
    global delayTime
    try:
        delayTime = int(functions.grabDelayTime(delayDisplay_lbl, delayTime_SpinBox))
    except Exception as e:
        print(f"Error handling delay time input: {e}")

def startConversion():
    """Activates CONVST for ADC and waits for RVS pin to signal ready data"""
    try:
        # Activate CONVST to start ADC conversion
        lgpio.gpio_write(chip, PinNumbers.CONVST, 1)
        time.sleep(CYCLE)  # Small delay to allow ADC to start conversion
        lgpio.gpio_write(chip, PinNumbers.CONVST, 0)  # Deactivate CONVST to finish start

        # Wait for RVS pin to go low (indicating ADC data is ready)
        while lgpio.gpio_read(chip, PinNumbers.RVS) == 0:
            time.sleep(CYCLE)  # Small delay before checking again
        # print("ADC data is ready")
    except Exception as e:
        print(f"Error during ADC conversion: {e}")

def pulseSYNC():
    """Pulses the SYNC pin to prepare DAC for receiving data"""
    try:
        lgpio.gpio_write(chip, PinNumbers.SYNC, 1)  # Set SYNC high
        time.sleep(CYCLE)  # Small delay
        lgpio.gpio_write(chip, PinNumbers.SYNC, 0)  # Set SYNC low
    except Exception as e:
        print(f"Error pulsing SYNC pin: {e}")

def readADC():
    """Reads a 32-bit signal from the ADC (ADS8681W)"""
    try:
        start_time = time.time()
        with open(output_filename, "w") as file:  # Open output file in write mode
            while time.time() - start_time < captureTime:
                startConversion()  # Start ADC conversion

                adc_data = spi_adc.xfer2([0x00, 0x00, 0x00, 0x00])  # 4 bytes (32 bits)

                result = (adc_data[0] << 24) | (adc_data[1] << 16) | (adc_data[2] << 8) | adc_data[3]
                captured_data.append(result)  # Store captured data

                file.write(f"Captured 32-bit ADC: {bin(result)}\n")
                # print(f"Captured 32-bit ADC: {bin(result)}")
    except Exception as e:
        print(f"Error reading ADC data: {e}")

def outputSignal():
    """Outputs the stored 32-bit signal to DAC (DAC82001)"""
    try:
        if not captured_data:
            print("No data to output!")
            return

        with open(output_filename, "a") as file:
            for signal in captured_data:
                captured_data.pop(0)  # Retrieve and remove the oldest stored signal

                dac_value = (signal >> 16) & 0xFFFF  # Extract the 16 most significant bits (Data Bits)

                data_bytes = [0x08, (dac_value >> 8) & 0xFF, dac_value & 0xFF]
                # file.write(f"Outputted to DAC82001: {data_bytes}\n")

                pulseSYNC()  # Pulse the SYNC pin to prepare the DAC
                spi_dac.xfer2(data_bytes)  # Send 4 bytes to the DAC

                file.write(f"Outputted to DAC82001: {dac_value}\n")
    except Exception as e:
        print(f"Error outputting signal to DAC: {e}")

def startConversionAndDelay():
    """Handles ADC conversion, delay, and DAC output"""
    try:
        print(f"Starting Delay")
        readADC()  # Read from ADC
        if delayTime > 0:
            time.sleep(delayTime)  # Add delay if set
            print(f"Delayed for {delayTime}s")
        outputSignal()  # Output to DAC
        print("Conversion and output complete")
    except Exception as e:
        print(f"Error during conversion and delay: {e}")

# GUI Setup
try:
    TDLwindow = tk.Tk()
    functions.createTDLWindow(TDLwindow)

    tk.Label(TDLwindow, text="ADC-DAC SPI Interface", font=("Times New Roman", 24)).pack(pady=20)

    tk.Label(TDLwindow, text="Input Desired Capture Time", font=("Times New Roman", 16)).pack(pady=10)
    captureTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=5, width=5, font=("Times New Roman", 12))
    captureTime_SpinBox.pack(pady=5)

    tk.Label(TDLwindow, text="Input Desired Delay Time", font=("Times New Roman", 16)).pack(pady=10)
    delayTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=20, width=5, font=("Times New Roman", 12))
    delayTime_SpinBox.pack(pady=5)

    tk.Button(TDLwindow, text="Set Capture Time", font=("Times New Roman", 16), command=handleCaptureButton).pack(pady=10)
    tk.Button(TDLwindow, text="Set Delay Time", font=("Times New Roman", 16), command=handleDelayButton).pack(pady=10)
    tk.Button(TDLwindow, text="Start Capture", font=("Times New Roman", 16), command=startConversionAndDelay).pack(pady=20)

    captureDisplay_lbl = tk.Label(TDLwindow, text="Current Capture Time: 0", font=("Times New Roman", 16))
    captureDisplay_lbl.pack(pady=3)

    delayDisplay_lbl = tk.Label(TDLwindow, text="Current Delay Time: 0", font=("Times New Roman", 16))
    delayDisplay_lbl.pack(pady=3)

    quit_btn = tk.Button(TDLwindow, text="Quit Program", command=TDLwindow.destroy)
    quit_btn.pack(side="bottom", pady=20)

    TDLwindow.mainloop()
except Exception as e:
    print(f"Error initializing GUI: {e}")

# Cleanup
try:
    spi_adc.close()
    spi_dac.close()
    lgpio.gpiochip_close(chip)  # Close GPIO chip
    print("SPI and GPIO closed. Exiting program.")
except Exception as e:
    print(f"Error during cleanup: {e}")
