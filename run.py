import device
import sys

device = device.Device(sys.argv[1])

try:
    device.connect()
    device.screen.detect_images()
except Exception as e:
    print(e)
    device.disconnect()
finally:
    device.disconnect()
