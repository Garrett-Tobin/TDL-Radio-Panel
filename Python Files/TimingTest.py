# Test Used for Testing capturing a signal for a designated Time and outputting afterwards


import lgpio # Used for Raspberry Pi 5 GPIO Handeling 
import time

DURATION = 10

# Pin Numbers
LED_PIN = 17
LDR_PIN = 27

# Open GPIO Chip and get a handle
chip = lgpio.gpiochip_open(0)

# Set Pin Outputs and Inputs
lgpio.gpio_claim_input(chip, LDR_PIN)
lgpio.gpio_claim_output(chip, LED_PIN)

# list to store captured data (timestamp, signal state)
captured_data = []

start_time = time.time() # Record Start Time
previous_state = lgpio.gpio_read(chip, LDR_PIN)

try:
    while time.time() - start_time < DURATION: # Run For a Given Duration
        current_state = lgpio.gpio_read(chip, LDR_PIN) # Read GPIO State
        
        timestamp = time.time()- start_time
        captured_data.append((timestamp, current_state)) # Append the Data to a list
        
        time.sleep(0.001)
except KeyboardInterrupt:
    print("\nInterrupted By User")
    
finally:
    print("\n Capture Complete. Replaying signal to LED \n")
    
    replay_start_time = time.time()
    for timestamp, state in captured_data:
        # Wait until the correct replay time
        while time.time() - replay_start_time < timestamp:
            time.sleep(0.001)
            
        # Output stored signal to LED
        lgpio.gpio_write(chip, LED_PIN, state)
        state_str = "ON" if state else "OFF"
        print(f"Replayed: Time {timestamp:.3f}s | LED {state_str}")
        
    # Ensure LED is turned off at the end
    lgpio.gpio_write(chip, LED_PIN, 0)
    
    lgpio.gpiochip_close(chip) # Clean up GPIO
    print("\nReplay Complete and Program Finished. GPIO Closed. Exiting.")
    