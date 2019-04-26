import time
from grove.gpio import GPIO

led = GPIO(12, GPIO.OUT)

while True:
    led.write(not led.read())
    time.sleep(0.5)
