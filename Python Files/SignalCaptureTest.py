import lgpio
import time

# Define the GPIO pin numbers
OUTPUT_PIN = 17

# Set up the GPIO interface
chip = lgpio.gpiochip_open(0)  # Open the first GPIO chip

# Set the pins as output and input
lgpio.gpio_claim_output(chip, OUTPUT_PIN)

COUNTER = 0
# Blink the LED 10 times
try:
    while (COUNTER < 10):
        # Turn the LED on (set the output pin to HIGH)
        lgpio.gpio_write(chip, OUTPUT_PIN, 1)
        time.sleep(1)  # Wait for 1 second

        # Turn the LED off (set the output pin to LOW)
        lgpio.gpio_write(chip, OUTPUT_PIN, 0)
        time.sleep(1)  # Wait for 1 second

	# Increment Counter By 1
        COUNTER += 1
except KeyboardInterrupt:
    pass  # Handle a keyboard interrupt (Ctrl+C) to stop the program

# Cleanup
lgpio.gpiochip_close(chip)

