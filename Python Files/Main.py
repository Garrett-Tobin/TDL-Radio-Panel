# Import Libraries
# import RPi.GPIO as GPIO
import tkinter as tk
import time

# Import Pin Numbers
import PinNumbers

TDLwindow = tk.Tk()

def createTDLWindow(windowTitle):
    windowTitle.title("TDL-Radio-Panel") # Set Window Title
    windowTitle.geometry('300x300') # Set Window Size



createTDLWindow(TDLwindow)
# Create Quit Button
quit_btn = tk.Button(TDLwindow, text="Quit Program", command=TDLwindow.destroy)
quit_btn.pack(pady=20)

TDLwindow.mainloop()
