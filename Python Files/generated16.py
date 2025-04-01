# Import Libraries
import lgpio
import tkinter as tk
import time

# Import Pin Numbers
import PinNumbers
import functions

# Global Variables
initial_state = True
CYCLE = 1/50000000
delayTime = 0
captureTime = 0
captured_data = []  # Store 24-bit signals
chip = lgpio.gpiochip_open(0)  # Open GPIO chip

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
    """Triggers ADC conversion by setting CONVST HIGH and waiting for RVS LOW"""
    lgpio.gpio_write(chip, PinNumbers.CONVST, 1)  # Start conversion
    time.sleep(CYCLE)  # Small delay to allow ADC to start
    lgpio.gpio_write(chip, PinNumbers.CONVST, 0)  # Return to LOW

    # Wait for RVS to go LOW (indicates ADC data is ready)
    while lgpio.gpio_read(chip, PinNumbers.RVS) == 1:
        time.sleep(CYCLE)

def pulseSYNC():
    """Pulse the SYNC pin to prepare the DAC"""
    lgpio.gpio_write(chip, PinNumbers.SYNC, 1)
    time.sleep(CYCLE) # Small delay to allow DAC to start
    lgpio.gpio_write(chip, PinNumbers.SYNC, 0) 

def readADC():
    """Reads the first 16-bit signal from ADC and appends 8-bit address"""
    start_time = time.time()
    while time.time() - start_time < captureTime:
        startConversion()
        adc_data = 0
        for i in range(16):  # Read only first 16 bits
            bit = lgpio.gpio_read(chip, PinNumbers.SDO_O)
            adc_data = (adc_data << 1) | bit  # Shift left and add new bit
            time.sleep(CYCLE)  # Simulate clock pulse (20ns)

        address = 0b00001000  # 8-bit address
        full_data = (address << 16) | adc_data  # Combine 8-bit address + 16-bit ADC data
        test_data = 0b000010001010101010101010 # Used for Testing
        captured_data.append(test_data)  # Store 24-bit signal

        print(f"Captured 16-bit ADC: {bin(adc_data)}, Full 24-bit Data: {bin(full_data)}")

        # Ignore the remaining 16 bits from ADC output
        for _ in range(16):
            _ = lgpio.gpio_read(chip, PinNumbers.SDO_O)
            time.sleep(CYCLE)  # Continue clocking out unused bits

def outputSignal():
    """Outputs the stored 24-bit signal to DAC via SDO_O"""
    if not captured_data:
        print("No data to output!")
        return

    for signal in captured_data:
        signal = captured_data.pop(0)  # Retrieve the oldest stored signal
        pulseSYNC()
        for i in range(24):  # Send 24-bit signal bit by bit
            bit = (signal >> (23 - i)) & 1  # Extract MSB first
            lgpio.gpio_write(chip, PinNumbers.SDIN, bit)
            time.sleep(CYCLE)  # Simulate clock pulse

        print(f"Outputted 24-bit signal: {bin(signal)}")

def startDelay():
    """Handles ADC conversion, delay, and DAC output"""
    readADC()  # Read first 16-bits from ADC and store it

    if delayTime > 0:
        time.sleep(delayTime)
        print(f"Delayed for {delayTime}s")

    # Maybe need to add SYNC Control here to prepare the DAC
    outputSignal()  # Output stored 24-bit signal to DAC
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
                # Initialize ADC and DAC settings
                lgpio.gpio_write(chip, PinNumbers.TRI_STATE, 1)  # Enable oscillator
                lgpio.gpio_write(chip, PinNumbers.RST, 0)  # Reset ADC
                lgpio.gpio_write(chip, PinNumbers.RESET, 0) # Assumption that 0 Resets DAC (Need to Check this)
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
lgpio.gpio_write(chip, PinNumbers.TRI_STATE, 0)  # Disable TRI_STATE
lgpio.gpiochip_close(chip)  # Close GPIO
print("GPIO closed. Exiting program.")
