import time
import tkinter as tk
# import lgpio

import PinNumbers

def setupPins(chip):
    # Setup Outputs
    # lgpio.gpio_claim_output(chip, CONVST)
    # lgpio.gpio_claim_output(chip, SDI)
    # lgpio.gpio_claim_output(chip, RST)
    # lgpio.gpio_claim_output(chip, SDIN)
    # lgpio.gpio_claim_output(chip, SYNC)
    # lgpio.gpio_claim_output(chip, RESET)
    # lgpio.gpio_claim_output(chip, TRI_STATE)
    
    # Setup Inputs
    # lgpio.gpio_claim_input(chip, RVS)
    # lgpio.gpio_claim_input(chip, ALRM)
    # lgpio.gpio_claim_input(chip, SDO_O)
    
    print("TESTING setupPins")

def createTDLWindow(windowTitle):
    windowTitle.title("TDL-Radio-Panel") # Set Window Title
    windowTitle.geometry('600x600') # Set Window Size

