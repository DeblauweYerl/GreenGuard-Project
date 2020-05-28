from RPi import GPIO
import time

class SolenoidValve:

    def __init__(self, pin, sleep=2):
        self.pin = pin
        self.sleep = sleep

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def apply_water(self):
        GPIO.output(self.pin, 1)
        time.sleep(self.sleep)
        GPIO.output(self.pin, 0)
        print("water applied!!!")