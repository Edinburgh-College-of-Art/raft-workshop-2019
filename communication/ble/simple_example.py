from bluepy import btle

# Scan and print devices
devs = list(btle.Scanner().scan())

for dev in devs:
    print(dev.addr)
    print(dev.rssi)
    print(dev.connectable)
    print("\n")
