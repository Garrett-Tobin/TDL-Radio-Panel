import spidev
import lgpio
import time
import tkinter as tk

# SPI Configuration
SPI_BUS = 0
SPI_ADC_DEVICE = 0  # ADS8681W on SPI0 CE0
SPI_DAC_DEVICE = 1  # DAC82001 on SPI0 CE1
spi_adc = spidev.SpiDev()
spi_dac = spidev.SpiDev()
spi_adc.open(SPI_BUS, SPI_ADC_DEVICE)
spi_dac.open(SPI_BUS, SPI_DAC_DEVICE)
spi_adc.max_speed_hz = 67000000  # 67 MHz for ADS8681W
spi_dac.max_speed_hz = 50000000  # 50 MHz for DAC82001

# GPIO Configuration
chip = lgpio.gpiochip_open(0)
ADC_CONVST = 17  # GPIO 17 (Pin 11) triggers ADC conversion
DAC_SYNC = 27  # GPIO 27 (Pin 13) synchronizes DAC output
lgpio.gpio_claim_output(chip, ADC_CONVST, 0)
lgpio.gpio_claim_output(chip, DAC_SYNC, 1)

# Global Variables
delayTime = 0
captureTime = 0
captured_data = []

# GUI Handlers
def handleDelayButton():
    global delayTime
    delayTime = int(delayTime_SpinBox.get())

def handleCaptureButton():
    global captureTime
    captureTime = int(captureTime_SpinBox.get())

def startConversion():
    lgpio.gpio_write(chip, ADC_CONVST, 1)
    time.sleep(0.000001)  # 1us pulse for conversion start
    lgpio.gpio_write(chip, ADC_CONVST, 0)
    time.sleep(0.000001)

def readADC():
    start_time = time.time()
    while time.time() - start_time < captureTime:
        startConversion()
        adc_response = spi_adc.xfer2([0x00, 0x00, 0x00, 0x00])  # Read 32 bits
        adc_data = (adc_response[0] << 24) | (adc_response[1] << 16) | (adc_response[2] << 8) | adc_response[3]
        captured_data.append(adc_data)
        print(f"Captured 32-bit ADC Data: {bin(adc_data)}")

def outputSignal():
    if not captured_data:
        print("No data to output!")
        return
    
    lgpio.gpio_write(chip, DAC_SYNC, 0)  # Enable DAC transfer
    for signal in captured_data:
        signal_bytes = [(signal >> 24) & 0xFF, (signal >> 16) & 0xFF, (signal >> 8) & 0xFF, signal & 0xFF]
        spi_dac.xfer2(signal_bytes)  # Send 32-bit data
        print(f"Outputted 32-bit Signal: {bin(signal)}")
    lgpio.gpio_write(chip, DAC_SYNC, 1)  # Disable DAC transfer

def startDelay():
    readADC()
    if delayTime > 0:
        time.sleep(delayTime)
        print(f"Delayed for {delayTime}s")
    outputSignal()
    print("END DELAY")

# GUI Setup
TDLwindow = tk.Tk()
tk.Label(TDLwindow, text="T.D.L-Radio-Panel P.O.C.", font=("Times New Roman", 24)).pack(pady=20)
delayTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=20, width=5)
delayTime_SpinBox.pack()
captureTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=5, width=5)
captureTime_SpinBox.pack()
tk.Button(TDLwindow, text="Set Delay Time", command=handleDelayButton).pack()
tk.Button(TDLwindow, text="Set Capture Time", command=handleCaptureButton).pack()
tk.Button(TDLwindow, text="Start", command=startDelay).pack()

TDLwindow.mainloop()

# Cleanup
spi_adc.close()
spi_dac.close()
lgpio.gpiochip_close(chip)
print("GPIO and SPI closed. Exiting program.")

