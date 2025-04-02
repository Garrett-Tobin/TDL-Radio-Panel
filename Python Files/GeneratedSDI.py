import spidev
import time
import tkinter as tk
import PinNumbers
import functions

# Global Variables
delayTime = 0
captureTime = 0
captured_data = []  # Store 16-bit signals from ADC
chip = spidev.SpiDev()  # Create SPI object

# ----------------------- GUI Handlers -----------------------

def handleDelayButton():
    """Sets the delay time from SpinBox"""
    global delayTime
    delayTime = int(functions.grabDelayTime(delayDisplay_lbl, delayTime_SpinBox))

def handleCaptureButton():
    """Sets the capture time from SpinBox"""
    global captureTime
    captureTime = int(functions.grabCaptureTime(captureDisplay_lbl, captureTime_SpinBox))

def startConversion():
    """Triggers ADC conversion by sending a start signal"""
    # Your ADC conversion logic (e.g., sending CONVST high)
    pass

def readADC():
    """Reads the 16-bit signal from the ADS8681W ADC"""
    start_time = time.time()
    while time.time() - start_time < captureTime:
        # Read 16-bit data from ADC over SPI (ADS8681W)
        adc_data = chip.xfer2([0x00, 0x00])  # Send 2 bytes for 16-bit data
        adc_data = (adc_data[0] << 8) | adc_data[1]  # Combine the two bytes into a 16-bit signal
        
        # Store the 16-bit data
        captured_data.append(adc_data)

        print(f"Captured 16-bit ADC: {bin(adc_data)}")

def outputSignal():
    """Outputs the stored 12-bit signal to DAC82001 DAC via SPI"""
    if not captured_data:
        print("No data to output!")
        return

    for signal in captured_data:
        # DAC82001 requires 12-bit data, so extract the lower 12 bits from the 16-bit data
        dac_data = signal & 0x0FFF  # Mask to get the lower 12 bits
        
        # Send the 12-bit signal over SPI to DAC
        chip.xfer2([dac_data >> 4 & 0xFF, dac_data & 0xFF])  # Send 2 bytes (12-bit data split)
        print(f"Outputted 12-bit signal to DAC: {bin(dac_data)}")

def startDelay():
    """Handles ADC conversion, delay, and DAC output"""
    readADC()  # Read 16-bits from ADC and store it

    if delayTime > 0:
        time.sleep(delayTime)
        print(f"Delayed for {delayTime}s")

    outputSignal()  # Output stored 12-bit signal to DAC
    print("END DELAY")

# ----------------------- GUI Setup -----------------------

TDLwindow = tk.Tk()  # Create main window
functions.setupPins(chip)  # Set up GPIO
functions.createTDLWindow(TDLwindow)

# Labels & Inputs
tk.Label(TDLwindow, text="T.D.L-Radio-Panel P.O.C.", font=("Times New Roman", 24)).pack(pady=20)
tk.Label(TDLwindow, text="Input Desired Delay Time", font=("Times New Roman", 16)).pack(pady=10)

delayTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=20, width=5, font=("Times New Roman", 12))
delayTime_SpinBox.pack(pady=5)

tk.Label(TDLwindow, text="Input Desired Signal Capture Time", font=("Times New Roman", 16)).pack(pady=10)

captureTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=5, width=5, font=("Times New Roman", 12))
captureTime_SpinBox.pack(pady=5)

# Buttons
tk.Button(TDLwindow, text="Set Desired Delay Time", font=("Times New Roman", 16), command=handleDelayButton).pack(pady=10)
tk.Button(TDLwindow, text="Set Desired Capture Time", font=("Times New Roman", 16), command=handleCaptureButton).pack(pady=10)
tk.Button(TDLwindow, text="Start Capture and Delay", font=("Times New Roman", 16), command=startDelay).pack(pady=20)

# Labels for Values
delayDisplay_lbl = tk.Label(TDLwindow, text="Current Delay Time: 0", font=("Times New Roman", 16))
delayDisplay_lbl.pack(pady=3)

captureDisplay_lbl = tk.Label(TDLwindow, text="Current Capture Time: 0", font=("Times New Roman", 16))
captureDisplay_lbl.pack(pady=3)

indicator_lbl = tk.Label(TDLwindow, text="Off", font=("Times New Roman", 16), bg="red", fg="white")
indicator_lbl.pack(side="right", padx=20)

# Quit Button
quit_btn = tk.Button(TDLwindow, text="Quit Program", command=TDLwindow.destroy)
quit_btn.pack(side="bottom", pady=20)

# ----------------------- Main Loop -----------------------

def mainLoop():
    global initial_state

    while True:
        try:
            TDLwindow.update_idletasks()
            TDLwindow.update()

            if initial_state:
                chip.open(0, 0)  # Open SPI bus (bus 0, device 0)
                initial_state = False

            time.sleep(0.01)  # Reduce CPU usage

        except tk.TclError:
            print("Program closed. Cleaning up...")
            break

# Start Main Loop in Separate Thread
import threading
threading.Thread(target=mainLoop, daemon=True).start()

TDLwindow.mainloop()  # Run Tkinter main loop

# ----------------------- Cleanup -----------------------
chip.close()  # Close SPI bus
print("SPI closed. Exiting program.")
