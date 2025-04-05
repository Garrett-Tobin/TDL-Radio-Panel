import spidev
import tkinter as tk
import time
import PinNumbers
import functions
import lgpio

# Global Variables
initial_state = True
SPI_BUS = 0  # SPI bus number
SPI_DEVICE_ADC = 0  # ADC on CE0 (GPIO 8) originally GPIO 22
SPI_DEVICE_DAC = 1  # DAC on CE1 (GPIO 7) originally GPIO 16
captureTime = 0
delayTime = 0
captured_data = []  # Store 32-bit signals
CYCLE = 1/(50e6)

# GPIO Setup
chip = lgpio.gpiochip_open(0)  # Open GPIO chip for pin control

# Initialize SPI
spi_adc = spidev.SpiDev()
spi_dac = spidev.SpiDev()
spi_adc.open(SPI_BUS, SPI_DEVICE_ADC)
spi_dac.open(SPI_BUS, SPI_DEVICE_DAC)
spi_adc.max_speed_hz = 50000000  # 50 MHz per ADS8681W datasheet
spi_dac.max_speed_hz = 50000000  # 50 MHz per DAC82001 datasheet
spi_adc.mode = 0b11  # Mode for ADS8681W
spi_dac.mode = 0b00  # Mode for DAC82001

spi_adc.xfer([0xC0, 0x00, 0x00, 0x00])
adc_data = spi_adc.xfer2([0x00, 0x00, 0x00, 0x00])
print(f"Raw ADC SPI Response: {adc_data}")
