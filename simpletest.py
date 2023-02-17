# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
thruster_zero = 614  # Out of 4096, 15% duty cycle 
thruster_on = 696  # =Out of 4096, 17% duty cycle

# A 15% duty cycle at 100Hz refresh rate will have a pulse duration of 1500µs 
# (100Hz) * (15% duty cycle) = 1500µs   or 0.01s*0.15=0.0015s

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 100       # 100 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 100hz, works well with Blue Robotics ESC's and makes math easy
pwm.set_pwm_freq(100)

while True:
    # This should initialize the ESC, then turn on/turn off the ESC every 1 second. 
    # ESC initialization requires 1500µs, then some throttle value (Ex: 1700µs), then back to 1500µs
    
    pwm.set_pwm(0, 0, thruster_zero)
    time.sleep(1)
    pwm.set_pwm(0, 0, thruster_on)
    time.sleep(1)
