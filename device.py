import os
import re
import subprocess
import configparser
from screen import Screen


class Device(object):

    def __init__(self, device_number):
        self.device_number = device_number
        self.screen = Screen(self, device_number)

    def connect(self):

        config = configparser.ConfigParser()
        config.read("device.conf")

        ip = config.get("connection", f"device_ip_{self.device_number}")
        os.system("adb connect " + ip)

    def disconnect(self):
        config = configparser.ConfigParser()
        config.read("device.conf")

        ip = config.get("connection", f"device_ip_{self.device_number}")
        os.system("adb disconnect " + ip)

    # Should run after connecting to a device
    def get_model(self, device_number):

        command = "adb devices -l"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            command_output = result.stdout.strip()

            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

            match_ip = re.search(ip_pattern, command_output)

            if match_ip:
                config = configparser.ConfigParser()
                config.read("device.conf")

                ip_address = match_ip.group(0)
                print("IP Address from Command Output:", ip_address)

                real_ip = config.get("connection", f"device_ip_{device_number}")

                if ip_address == real_ip:
                    print("IP Matched.")

                    model_pattern = r'model:(\S+)'
                    match_model = re.search(model_pattern, command_output)

                    if match_model:
                        device_model = match_model.group(1)
                        print("Device Model:", device_model)

                        return device_model
                    else:
                        print("Model could not be found")
                else:
                    print("IP is not matching. Please try again after checking the device.conf file.")
            else:
                print("IP Pattern not matched. Please try again")
        else:
            print("Error:", result.stderr)
