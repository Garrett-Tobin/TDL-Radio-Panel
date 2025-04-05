# Import Libraries
import lgpio
import time  # To introduce any necessary delays
import functions  # Not used in the code provided

# Pin Definitions
GPIO17 = 22  # Existing pin
GPIO23 = 23   # ADC
GPIO24 = 24      # ADC
GPIO25 = 25      # ADC
GPIO16 = 16     # DAC
GPIO26 = 26     # DAC
GPIO6 = 6     # DAC
GPIO5 = 5 # Oscillator

# Counter variable
counter = 0

# Open GPIO chip
chip = lgpio.gpiochip_open(0)

# Claim pins for output
lgpio.gpio_claim_output(chip, GPIO17)
lgpio.gpio_claim_output(chip, GPIO23)
lgpio.gpio_claim_output(chip, GPIO24)
lgpio.gpio_claim_output(chip, GPIO25)
lgpio.gpio_claim_output(chip, GPIO16)
lgpio.gpio_claim_output(chip, GPIO26)
lgpio.gpio_claim_output(chip, GPIO6)
lgpio.gpio_claim_output(chip, GPIO5)

# Loop to control output on all pins
while counter < 10:
    # Set all pins high (turn on outputs)
    lgpio.gpio_write(chip, GPIO17, 1)
    lgpio.gpio_write(chip, GPIO23, 1)
    lgpio.gpio_write(chip, GPIO24, 1)
    lgpio.gpio_write(chip, GPIO25, 1)
    lgpio.gpio_write(chip, GPIO16, 1)
    lgpio.gpio_write(chip, GPIO26, 1)
    lgpio.gpio_write(chip, GPIO6, 1)
    lgpio.gpio_write(chip, GPIO5, 1)
    
    # Increment counter
    counter += 1
    time.sleep(1)
    print(counter)

# After loop, set all pins low (turn off outputs)
lgpio.gpio_write(chip, GPIO17, 0)
lgpio.gpio_write(chip, GPIO23, 0)
lgpio.gpio_write(chip, GPIO24, 0)
lgpio.gpio_write(chip, GPIO25, 0)
lgpio.gpio_write(chip, GPIO16, 0)
lgpio.gpio_write(chip, GPIO26, 0)
lgpio.gpio_write(chip, GPIO6, 0)
lgpio.gpio_write(chip, GPIO5, 0)

