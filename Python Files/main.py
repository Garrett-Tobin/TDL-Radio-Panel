# Import Libraries
import lgpio
import tkinter as tk
import time

# Import Pin Numbers
import PinNumbers

# Import Functions
import functions

initial_state = True
delayTime = 0
captureTime = 0

def handleDelayButton():
    global delayTime
    delayTime = int(functions.grabDelayTime(delayDisplay_lbl, delayTime_SpinBox))
    
def handleCaptureButton():
    global captureTime
    captureTime = int(functions.grabCaptureTime(captureDisplay_lbl, captureTime_SpinBox))
    
def captureSignal():
    # This function will simulate capturing the signal and store it with a timestamp
    start_time = time.time() # Record Start Time
    while time.time() - start_time < captureTime: # Run For a Given Duration
        current_state = lgpio.gpio_read(chip, PinNumbers.SDO_O) # Read GPIO State
        
        timestamp = time.time()- start_time
        # print(f"Time {timestamp:.3f}s state: {current_state}")
        captured_data.append((timestamp, current_state)) # Append the Data to a list
        
        time.sleep(0.00001)
    print(f"Captured Signal for {captureTime}s")

def outputSignal():
    replay_start_time = time.time()
    for timestamp, state in captured_data:
        # Wait until the correct replay time
        while time.time() - replay_start_time < timestamp:
            time.sleep(0.00001)
            
        # Output stored signal to LED
        lgpio.gpio_write(chip, PinNumbers.SDIN, state)
        state_str = "ON" if state else "OFF"
        # print(f"Replayed: Time {timestamp:.3f}s | LED {state_str}")

def startDelay():
    if delayTime > 0:
        captureSignal()
        time.sleep(delayTime)
        print(f"Delayed for {delayTime}s")
        outputSignal()
    print("END DELAY")


ADC_ON = False
# list to store captured data (timestamp, signal state)
captured_data = []

try:
    TDLwindow = tk.Tk()  # Set up the main window

    # Set up all GPIO Pins as input or output
    chip = lgpio.gpiochip_open(0)  # Open the GPIO chip
    functions.setupPins(chip)

    # Setup and Configure the Tkinter Window
    functions.createTDLWindow(TDLwindow)

    # Create Title Label
    title_lbl = tk.Label(TDLwindow, text="T.D.L-Radio-Panel P.O.C.", font=("Times New Roman", 24))
    title_lbl.pack(pady=20)

    # Delay Time Capture Label
    delayCapture_lbl = tk.Label(TDLwindow, text="Input Desired Delay Time", font=("Times New Roman", 16))
    delayCapture_lbl.pack(pady=10)

    # SpinBox to Input Delay Time
    delayTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=20, width=5, font=("Times New Roman", 12))
    delayTime_SpinBox.pack(pady=5)

    # Capture Time Capture Label
    captureTimeCapture_lbl = tk.Label(TDLwindow, text="Input Desired Signal Capture Time", font=("Times New Roman", 16))
    captureTimeCapture_lbl.pack(pady=10)

    # SpinBox to Input Capture Time
    captureTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=5, width=5, font=("Times New Roman", 12))
    captureTime_SpinBox.pack(pady=5)

    # Button to Set Delay Time
    setDelayTime_btn = tk.Button(TDLwindow, text="Set Desired Delay Time", font=("Times New Roman", 16), command=handleDelayButton)
    setDelayTime_btn.pack(pady=10)
    
    # Button to Set Capture Time
    setCaptureTime_btn = tk.Button(TDLwindow, text="Set Desired Capture Time", font=("Times New Roman", 16), command=handleCaptureButton)
    setCaptureTime_btn.pack(pady=10)

    # Button to start Delay
    startDelay_btn = tk.Button(TDLwindow, text="Start Capture and Delay", font=("Times New Roman", 16), command=startDelay)
    startDelay_btn.pack(pady=20)
    
    # Label to Display Current Delay Time
    delayDisplay_lbl = tk.Label(TDLwindow, text="Current Delay Time: 0", font=("Times New Roman", 16))
    delayDisplay_lbl.pack(pady=3)

    # Label to Display Current Capture Time
    captureDisplay_lbl = tk.Label(TDLwindow, text="Current Capture Time: 0", font=("Times New Roman", 16))
    captureDisplay_lbl.pack(pady=3)

    # On Indicator (Just for Test Purposes Right Now)
    indicator_lbl = tk.Label(TDLwindow, text="Off", font=("Times New Roman", 16), bg="red", fg="white")
    indicator_lbl.pack(side="right", padx=20)

    # Create Quit Button
    quit_btn = tk.Button(TDLwindow, text="Quit Program", command=TDLwindow.destroy)
    quit_btn.pack(side="bottom", pady=20)

    # Run the interface in a loop
    TDLwindow.update_idletasks()
    TDLwindow.update()

    # Infinite loop that runs until the user closes the program
    while TDLwindow.winfo_exists():
        try:
            TDLwindow.update_idletasks()  # Update Tkinter tasks
            TDLwindow.update()  # Refresh the window
            
            while initial_state:
                # Update TRI-STATE on oscillator (not sure about this one)
                lgpio.gpio_write(chip, PinNumbers.TRI_STATE, 1) # Check if this needs to be set to high or low
                # Update RST Pin if need to Reset the ADC (Set to Active Low to reset pin)
                lgpio.gpio_write(chip, PinNumbers.RST, 0)
                # Send register instructions to ADC using SDI pin (Not sure what this entails)   
                
                initial_state = False

            # Indicate to ADC to start converting using CONVST (Done after interface button is pressed)

            # Read RVS pin (When high signal is being read and when Low samples are being put together)
            # Have a while loop that runs until samples are ready to be read
            
            # When samples are prepared read them and capture them from SDO-O

            # Delay the program 

            # Update RESET to reset DAC if needed

            # Send SYNC signal to prepare DAC for conversion to analog

            # Send captured digital signal to SDIN
            
            time.sleep(0.1)  # Prevents excessive CPU usage

        except tk.TclError:
            # Catches when the window is closed and breaks the loop
            print("Program closed. Cleaning up...")
            break

finally:
    lgpio.gpio_write(chip, PinNumbers.TRI_STATE, 0)
    lgpio.gpiochip_close(chip)  # Close the GPIO chip
    print("GPIO chip closed. Exiting program.")
