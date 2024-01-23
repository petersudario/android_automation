# Android Automation

Prototype tooling that combines **ADB**, **scrcpy**, **OpenCV**, and **Python** to mirror one or more Android devices on a desktop, run simple swipe-based automation, and detect on-screen motion inside the mirrored window. A separate script demonstrates quadrant-based motion detection on the host display using **mss**.

This repository is aimed at experimentation and local workflows rather than production orchestration.

## Overview

The project has two main ideas:

1. **Device workflow** — Connect to a phone or emulator over the network, launch **scrcpy** with a predictable window title, capture that window with **PyAutoGUI**, and apply frame differencing to highlight motion. While detection runs, a background loop can issue **ADB input** commands defined in a config file (for example repeated upward swipes).

2. **Screen-quadrant prototype** — `test.py` grabs a fixed quadrant of the host monitor with **mss**, compares consecutive frames with OpenCV, and draws rectangles where motion exceeds a size threshold. This path does not talk to ADB; it is useful for validating motion logic in isolation.

Bundled under `modules/` are vendored or local copies of **scrcpy** and **ADB**-related assets used by the Windows-oriented launcher paths in the code. Paths in `screen.py` assume a Windows layout for launching scrcpy.

## Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy
- **mss** (for `test.py`)
- **PyAutoGUI** and **pygetwindow** (for `screen.py` / `run.py`)
- **ADB** on the host `PATH`, with devices reachable over TCP/IP (`adb connect`)
- **scrcpy** available where `screen.py` expects it (see `modules/scrcpy` and the launcher script referenced below)

Install Python dependencies (example):

```bash
pip install opencv-python numpy mss pyautogui pygetwindow
```

Adjust versions to match your environment.

## Configuration

### `device.conf`

Maps logical device indices to IP addresses used by `adb connect` / `adb disconnect`:

```ini
[connection]
device_ip_1 = 192.168.0.119
device_ip_2 = 192.168.0.119
...
```

Pass the device index as the first argument to `run.py` (see below). The code resolves `device_ip_{n}` for that index.

### `controller.conf`

Defines shell commands for named movements. Values are executed with `os.system`; example entries use `adb shell input swipe ...`:

```ini
[controller]
UP = "adb shell input swipe 500 1200 500 300 500"
DOWN = "adb shell input swipe 500 500 500 1500 500"
```

Extend this file with additional keys if you add new movement types in `controller.py`.

## Project layout

| Path | Role |
|------|------|
| `run.py` | Entry point: connect ADB, start motion detection in a subprocess, call controller movements in a loop. |
| `device.py` | Loads configs, runs `adb connect` / `disconnect`, resolves device model from `adb devices -l`, constructs `Screen` and `Controller`. |
| `screen.py` | Starts scrcpy with a titled window, grabs that region, detects motion vs a baseline frame, optional idle timeout, OpenCV display. |
| `controller.py` | Reads `controller.conf` and runs the configured command for a movement name. |
| `test.py` | Standalone quadrant motion demo on the host screen (mss + OpenCV). |
| `modules/` | scrcpy and related binaries/scripts for mirroring. |

## Usage

### Motion detection on the scrcpy window

1. Edit `device.conf` with your device IP(s).
2. Ensure the device accepts `adb connect` over the network (USB debugging authorized).
3. From the project root:

```bash
python run.py 1
```

Use `1`, `2`, … matching `device_ip_1`, `device_ip_2`, etc.

`run.py` connects, starts `Screen.image_detection()` in another process, and repeatedly invokes `perform_movement("UP")` from `controller.conf`. Press **q** in the OpenCV window to quit the motion view when focused.

### Quadrant-only prototype (`test.py`)

```bash
python test.py
```

This uses monitor index `3` in **mss** for the capture region; adjust `monitor = sct.monitors[3]` if your setup differs. Press **q** to exit.

## Behavior notes

- **Window title** — `screen.py` builds `"{device_number}:{model}"` and passes it to scrcpy so **pygetwindow** can find the window. If the window is missing, the script logs and returns.
- **Motion idle timeout** — If no motion is detected for a configured duration, the loop in `screen.py` exits.
- **Platform assumptions** — Scrcpy is invoked via a Windows path (`.\\modules\\scrcpy\\scrcpy-noconsole.vbs`). Running on macOS or Linux requires path and launcher changes.
- **Security** — Config files may contain LAN IPs; avoid committing secrets or exposing ADB on untrusted networks.

## Limitations

- No packaged dependency manifest is checked in; pin libraries for reproducibility if you need it.
- Error handling is minimal outside the screen capture path.
- Automation commands are fixed swipe strings; there is no higher-level scenario DSL.

## License

Refer to upstream components under `modules/` (for example scrcpy) for their respective licenses. Add a root-level license file if you publish this project formally.
