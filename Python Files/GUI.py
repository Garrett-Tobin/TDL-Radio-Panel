import tkinter as tk

# Dummy functions to replace hardware interactions
def reset_devices():
    print("Resetting devices...")

def startConversionAndDelay():
    print("Starting conversion and delay...")

def handleCaptureButton():
    global captureTime
    captureTime = int(captureTime_SpinBox.get())
    captureDisplay_lbl.config(text=f"Current Capture Time: {captureTime}")

def handleDelayButton():
    global delayTime
    delayTime = int(delayTime_SpinBox.get())
    delayDisplay_lbl.config(text=f"Current Delay Time: {delayTime}")

# GUI Setup
TDLwindow = tk.Tk()
TDLwindow.title("ADC-DAC SPI Interface")

tk.Label(TDLwindow, text="ADC-DAC SPI Interface", font=("Times New Roman", 24)).pack(pady=20)

tk.Label(TDLwindow, text="Input Desired Capture Time", font=("Times New Roman", 16)).pack(pady=10)
captureTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=5, width=5, font=("Times New Roman", 12))
captureTime_SpinBox.pack(pady=5)

tk.Label(TDLwindow, text="Input Desired Delay Time", font=("Times New Roman", 16)).pack(pady=10)
delayTime_SpinBox = tk.Spinbox(TDLwindow, from_=1, to_=20, width=5, font=("Times New Roman", 12))
delayTime_SpinBox.pack(pady=5)

tk.Button(TDLwindow, text="Set Capture Time", font=("Times New Roman", 16), command=handleCaptureButton).pack(pady=10)
tk.Button(TDLwindow, text="Set Delay Time", font=("Times New Roman", 16), command=handleDelayButton).pack(pady=10)
tk.Button(TDLwindow, text="Start Capture", font=("Times New Roman", 16), command=startConversionAndDelay).pack(pady=20)

captureDisplay_lbl = tk.Label(TDLwindow, text="Current Capture Time: 0", font=("Times New Roman", 16))
captureDisplay_lbl.pack(pady=3)

delayDisplay_lbl = tk.Label(TDLwindow, text="Current Delay Time: 0", font=("Times New Roman", 16))
delayDisplay_lbl.pack(pady=3)

quit_btn = tk.Button(TDLwindow, text="Quit Program", command=TDLwindow.destroy)
quit_btn.pack(side="bottom", pady=20)

TDLwindow.mainloop()
