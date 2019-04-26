import time
from grove.gpio import GPIO

led = GPIO(12, GPIO.OUT)

print("connect an LED to pin #12\nPress CTRL + c to quit")

try:
    while True:
        led.write(not led.read())
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Done!")
    led.write(False)
    quit()


