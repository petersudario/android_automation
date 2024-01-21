import device
import sys

device = device.Device(sys.argv[1])

try:
    device.connect()
    device.screen.detect_images()
except:
    device.disconnect()
finally:
    device.disconnect()
