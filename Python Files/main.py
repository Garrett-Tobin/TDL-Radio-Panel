# Import Libraries
import lgpio
import tkinter as tk
import time

# Import Pin Numbers
import PinNumbers

# Import Functions
import functions

def handleDelayButton():
    delayTime = functions.grabDelayTime(delayDisplay_lbl, delayTime_SpinBox)

ADC_ON = False

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
    delayTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=10, width=5, font=("Times New Roman", 12))
    delayTime_SpinBox.pack(pady=5)

    # Button to Set Delay Time
    setDelayTime_btn = tk.Button(TDLwindow, text="Set Desired Delay Time", font=("Times New Roman", 16), command=handleDelayButton)
    setDelayTime_btn.pack(pady=20)

    # Button to start Delay
    startDelay_btn = tk.Button(TDLwindow, text="Start Capture and Delay", font=("Times New Roman", 16), command=startDelay)
    startDelay_btn.pack(pady=20)
    
    # Label to Display Current Delay Time
    delayDisplay_lbl = tk.Label(TDLwindow, text="Current Delay Time: 0", font=("Times New Roman", 16))
    delayDisplay_lbl.pack(pady=3)

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
    while True:
        try:
            TDLwindow.update_idletasks()  # Update Tkinter tasks
            TDLwindow.update()  # Refresh the window

            # Update TRI-STATE on oscillator (not sure about this one)
            
            # Update RST Pin if need to Reset the ADC (Set to Active Low to reset pin)

            # Send register instructions to ADC using SDI pin (Not sure what this entails)

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
    lgpio.gpiochip_close(chip)  # Close the GPIO chip
    print("GPIO chip closed. Exiting program.")
