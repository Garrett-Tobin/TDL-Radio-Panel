import RPi.GPIO as GPIO
import tkinter as tk
import time

# Below prints out current version of RPi.GPIO and runs tkinter test
# gpio_version = GPIO.VERSION 
# print(gpio_version)
# tkinter._test();

# Creating Window
window = tk.Tk();
window.title("TDL-Radio-Panel") # Set Window Title
window.geometry('300x300') # Set Window Size

# Title
title_lbl = tk.Label(window, text="TDL-Radio-Panel POC", font=("Times New Roman", 14))
title_lbl.pack(pady=10)

# Main SpinBox
delayTime_SpinBox = tk.Spinbox(window, from_=1, to_=10, width=5, font=("Times New Roman", 12))
delayTime_SpinBox.pack(pady=5)

# Get Value from Main SpinBox
def get_delay_time_cmd():
	print("Delay Time SpinBox Value:", delayTime_SpinBox.get())

# Button To Retrieve SpinBox value
get_delay_time_btn = tk.Button(window, text="Get Delay Time", command=get_delay_time_cmd, font=("Times New Roman", 12))
get_delay_time_btn.pack(pady=5)

# Create Quit Button
quit_btn = tk.Button(window, text="Quit Program", command=window.destroy)
quit_btn.pack(pady=20)

# Enter Window Mainloop
window.mainloop()
