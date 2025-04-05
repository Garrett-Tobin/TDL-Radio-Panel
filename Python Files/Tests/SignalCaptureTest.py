import lgpio
import time

# Define the GPIO pin numbers
LED_PIN = 17
LDR_PIN = 27

# Set up the GPIO interface
chip = lgpio.gpiochip_open(0)  # Open the first GPIO chip

# Set the pins as output and input
lgpio.gpio_claim_output(chip, LED_PIN)
lgpio.gpio_claim_input(chip, LDR_PIN)

COUNTER = 0
# Turn on LED when Light Level is high
try:
    while True:
        ldr_value = lgpio.gpio_read(chip, LDR_PIN)
        print(ldr_value)
        time.sleep(1)

        if(ldr_value > 0):
           lgpio.gpio_write(chip, LED_PIN, 1)
        else:
           lgpio.gpio_write(chip, LED_PIN, 0)

        time.sleep(1)

except KeyboardInterrupt:
    pass  # Handle a keyboard interrupt (Ctrl+C) to stop the program

# Cleanup
lgpio.gpiochip_close(chip)

