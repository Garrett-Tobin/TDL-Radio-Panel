# Import Libraries
# import lgpio
import tkinter as tk
import time

# Import Pin Numbers
import PinNumbers
# Import Functions
import functions


TDLwindow = tk.Tk()

def createTDLWindow(windowTitle):
    windowTitle.title("TDL-Radio-Panel") # Set Window Title
    windowTitle.geometry('300x300') # Set Window Size

# Set up all GPIO Pins as input or output
chip = 12
functions.setupPins(chip)

createTDLWindow(TDLwindow)
# Create Quit Button
quit_btn = tk.Button(TDLwindow, text="Quit Program", command=TDLwindow.destroy)
quit_btn.pack(pady=20)

TDLwindow.mainloop()
