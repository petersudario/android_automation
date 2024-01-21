import time
import multiprocessing
import device
import sys

device = device.Device(sys.argv[1])

if __name__ == "__main__":
    try:
        device.connect()
        process = multiprocessing.Process(target=device.screen.image_detection)
        process.start()
        while True:
            device.controller.perform_movement("UP")
    except Exception as e:
        print(e)
        process.join()
        device.disconnect()
    finally:
        process.join()
        device.disconnect()
