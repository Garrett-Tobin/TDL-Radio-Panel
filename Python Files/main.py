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
    TDLwindow = tk.Tk() # Set up the main window

    # Set up all GPIO Pins as input or output
    chip = lgpio.gpiochip_open(0) # Open the GPIO chip
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

    # Label to Display Current Delay Time
    delayDisplay_lbl = tk.Label(TDLwindow, text="Current Delay Time: 0", font=("Times New Roman", 16))
    delayDisplay_lbl.pack(pady=3)

    # On Indicator (Just for Test Purposes Right Now
    indicator_lbl = tk.Label(TDLwindow, text="Off", font=("Times New Roman", 16), bg="red", fg="white")
    indicator_lbl.pack(side="right", padx=20)

    # Create Quit Button
    quit_btn = tk.Button(TDLwindow, text="Quit Program", command=TDLwindow.destroy)
    quit_btn.pack(side="bottom", pady=20)

    TDLwindow.mainloop() # Run the interface in a loop
finally:
    lgpio.gpiochip_close(chip) # Close the GPIO chip
    # End File
