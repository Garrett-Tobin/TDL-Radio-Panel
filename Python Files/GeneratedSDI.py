import spidev
import lgpio
import tkinter as tk
import time
import PinNumbers
import functions

# Global Variables
initial_state = True
SPI_BUS = 0  # SPI bus number
SPI_DEVICE_ADC = 0  # ADC on CE0
SPI_DEVICE_DAC = 1  # DAC on CE1
captureTime = 0
delayTime = 0
captured_data = []  # Store 32-bit signals

# Initialize SPI
spi_adc = spidev.SpiDev()
spi_dac = spidev.SpiDev()
spi_adc.open(SPI_BUS, SPI_DEVICE_ADC)
spi_dac.open(SPI_BUS, SPI_DEVICE_DAC)
spi_adc.max_speed_hz = 67000000  # 50 MHz per ADS8681W datasheet
spi_dac.max_speed_hz = 50000000  # 50 MHz per DAC82001 datasheet
spi_adc.mode = 0b11  # Mode for ADS8681W
spi_dac.mode = 0b00  # Mode for DAC82001

# Initialize GPIO
chip = lgpio.gpiochip_open(0)

# GUI Handlers
def handleCaptureButton():
    global captureTime
    captureTime = int(functions.grabCaptureTime(captureDisplay_lbl, captureTime_SpinBox))

def handleDelayButton():
    global delayTime
    delayTime = int(functions.grabDelayTime(delayDisplay_lbl, delayTime_SpinBox))

def readADC():
    """Reads a 32-bit signal from the ADC (ADS8681W)"""
    start_time = time.time()
    while time.time() - start_time < captureTime:
        adc_data = spi_adc.xfer2([0x00, 0x00, 0x00, 0x00])  # 4 bytes (32 bits)
        result = (adc_data[0] << 24) | (adc_data[1] << 16) | (adc_data[2] << 8) | adc_data[3]
        captured_data.append(result)
        print(f"Captured 32-bit ADC: {bin(result)}")

def outputSignal():
    """Outputs the stored 32-bit signal to DAC (DAC82001)"""
    if not captured_data:
        print("No data to output!")
        return

    for signal in captured_data:
        captured_data.pop(0)  # Retrieve and remove the oldest stored signal
        data_bytes = [(signal >> 24) & 0xFF, (signal >> 16) & 0xFF, (signal >> 8) & 0xFF, signal & 0xFF]
        spi_dac.xfer2(data_bytes)  # Send 4 bytes
        print(f"Outputted 32-bit signal: {bin(signal)}")

def startConversion():
    readADC()  # Read from ADC
    if delayTime > 0:
        time.sleep(delayTime)
        print(f"Delayed for {delayTime}s")
    outputSignal()  # Output to DAC
    print("Conversion complete")

# GUI Setup
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
tk.Button(TDLwindow, text="Start Capture", font=("Times New Roman", 16), command=startConversion).pack(pady=20)

captureDisplay_lbl = tk.Label(TDLwindow, text="Current Capture Time: 0", font=("Times New Roman", 16))
captureDisplay_lbl.pack(pady=3)

delayDisplay_lbl = tk.Label(TDLwindow, text="Current Delay Time: 0", font=("Times New Roman", 16))
delayDisplay_lbl.pack(pady=3)

quit_btn = tk.Button(TDLwindow, text="Quit Program", command=TDLwindow.destroy)
quit_btn.pack(side="bottom", pady=20)

TDLwindow.mainloop()

# Cleanup
spi_adc.close()
spi_dac.close()
lgpio.gpiochip_close(chip)
print("SPI and GPIO closed. Exiting program.")
