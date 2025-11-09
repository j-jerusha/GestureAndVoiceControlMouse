# Gesture Controlled Virtual Mouse with Voice Assistant

## Overview
This project allows you to **control your computer using hand gestures and voice commands**. You can perform mouse actions, control volume, adjust screen brightness, navigate browsers, and even control YouTube playback — all without touching the keyboard or mouse.

It leverages:
- **Mediapipe** for hand gesture detection
- **PyAutoGUI** for controlling mouse and keyboard
- **PyCaw** for audio control
- **SpeechRecognition** for voice commands
- **Screen Brightness Control** for adjusting display brightness

---

## Features

### Hand Gesture Control
- **Move cursor** with hand movement
- **Left click / Double click** with thumb–index pinch
- **Right click** with thumb–middle pinch
- **Close tab** with thumb–ring pinch
- **Scroll up/down** with index + middle fingers
- **Volume control** with index + middle + ring + pinky fingers
- **Brightness control** with index + middle + ring fingers
- **Mute/Unmute** with thumb + pinky pattern
- **Maximize/Minimize window** with all fingers folded + thumb up/down

### Voice Commands
- Mouse actions: `left click`, `right click`, `double click`, `scroll up`, `scroll down`
- Volume: `volume up`, `volume down`, `mute`, `unmute`
- Brightness: `brightness up`, `brightness down`
- Browser control: `open browser`, `close browser`, `open youtube`, `close youtube`
- YouTube: `play`, `pause`, `type <text>`, `search <text>`
- Screenshot: `screenshot`
- Gesture toggle: `enable gestures`, `disable gestures`
- Exit program: `stop`, `exit`, `quit`

---

## Requirements

- Python 3.8+
- Libraries:

```bash
pip install opencv-python mediapipe pyautogui pycaw comtypes SpeechRecognition pyaudio screen_brightness_control
