import time
import tkinter as tk
import lgpio

import PinNumbers

def setupPins(chip):
    # Setup Outputs
    lgpio.gpio_claim_output(chip, PinNumbers.CONVST)
    lgpio.gpio_claim_output(chip, PinNumbers.SDI)
    lgpio.gpio_claim_output(chip, PinNumbers.RST)
    lgpio.gpio_claim_output(chip, PinNumbers.SDIN)
    lgpio.gpio_claim_output(chip, PinNumbers.SYNC)
    lgpio.gpio_claim_output(chip, PinNumbers.RESET)
    lgpio.gpio_claim_output(chip, PinNumbers.TRI_STATE)
    
    # Setup Inputs
    lgpio.gpio_claim_input(chip, PinNumbers.RVS)
    lgpio.gpio_claim_input(chip, PinNumbers.ALRM)
    lgpio.gpio_claim_input(chip, PinNumbers.SDO_O)
    # End of setupPins(chip)

def grabDelayTime(label, spinBox):
    # Grab the Delay Time from the SpinBox
    time = spinBox.get() # Grab the spinBox Value
    label.config(text=f"Current Delay Time: {time}") # Update the Label
    return time

def createTDLWindow(windowTitle):
    windowTitle.title("TDL-Radio-Panel") # Set Window Title
    windowTitle.geometry('600x600') # Set Window Size

