# Release v1.0.0

First tagged release of **Android Automation**, a Python prototype that mirrors Android devices with **scrcpy**, drives simple **ADB** swipe automation, and performs **OpenCV** motion detection on the mirrored window. A standalone **mss** + OpenCV sample (`test.py`) demonstrates quadrant motion detection on the host screen.

## Highlights

- **Device workflow** — Network `adb connect`, configurable IPs per device index (`device.conf`), `run.py` entry point with multiprocessing for screen capture and controller loop.
- **Screen module** — Launches scrcpy with a stable window title, captures the window region, frame differencing and contour-based motion feedback, idle timeout, and basic error handling.
- **Controller module** — Movement commands loaded from `controller.conf` (ADB shell swipes and similar).
- **Host quadrant demo** — `test.py` for fourth-quadrant motion detection without a device.
- **Documentation** — Root `README.md` with setup, configuration, layout, usage, and limitations.
- **Vendored tooling** — scrcpy-related assets under `modules/` for local execution on Windows-oriented paths.

## Requirements

- Python 3.x with OpenCV, NumPy, mss, PyAutoGUI, and pygetwindow
- ADB and USB debugging / TCP connectivity to target devices
- scrcpy available where `screen.py` expects it (see README)

## Install

```bash
pip install opencv-python numpy mss pyautogui pygetwindow
```

Configure `device.conf` and `controller.conf` before running.

## Usage (quick reference)

```bash
python run.py 1
python test.py
```

See `README.md` for full instructions and platform notes.

## Known limitations

- Windows-centric scrcpy launcher paths; other OS users must adjust.
- No checked-in `requirements.txt`; pin dependencies for reproducible installs.
- Prototype-grade error handling and automation scope.

## History

This release corresponds to the repository state after conventional commit message cleanup and the expanded project readme. For a line-by-line history, use `git log` on the `master` branch.
