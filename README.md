# Gesture and Voice Controlled Virtual Mouse System

## Overview
This project enables **hands-free control of your computer** using **hand gestures** and **voice commands**. Perform mouse actions, control volume and brightness, navigate browsers, and control YouTube playback — all without touching a physical keyboard or mouse.

It leverages:  
- **Mediapipe** – hand gesture detection  
- **PyAutoGUI** – mouse and keyboard control  
- **PyCaw** – system volume control  
- **SpeechRecognition** – voice command processing  
- **Screen Brightness Control** – adjust display brightness  
- **FastAPI** – backend API handling  
- **HTML, CSS, JavaScript** – web interface  

---

## Features

### Hand Gesture Control
- **Move cursor** with hand movement  
- **Left click / Double click** – thumb–index pinch  
- **Right click** – thumb–middle pinch  
- **Close tab** – thumb–ring pinch  
- **Scroll up/down** – index + middle fingers  
- **Volume control** – index + middle + ring + pinky fingers  
- **Brightness control** – index + middle + ring fingers  
- **Mute/Unmute** – thumb + pinky  
- **Maximize/Minimize window** – all fingers folded + thumb up/down  

### Voice Commands
- Mouse actions: `left click`, `right click`, `double click`, `scroll up`, `scroll down`  
- Volume: `volume up`, `volume down`, `mute`, `unmute`  
- Brightness: `brightness up`, `brightness down`  
- Browser control: `open browser`, `close browser`, `open youtube`, `close youtube`  
- YouTube control: `play`, `pause`, `type <text>`, `search <text>`  
- Screenshot: `screenshot`  
- Gesture toggle: `enable gestures`, `disable gestures`  
- Exit program: `stop`, `exit`, `quit`  

### Web Interface
- Start gesture control from browser  
- Start voice control from browser  
- Clean UI built with HTML, CSS, and JavaScript  
- Backend communication via FastAPI  

---

## Requirements

- **Python** 3.8+  
- Libraries:  
  `opencv-python`, `mediapipe`, `pyautogui`, `pycaw`, `comtypes`, `SpeechRecognition`, `pyaudio`, `screen_brightness_control`, `fastapi`, `uvicorn`  

---

## Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the FastAPI backend
uvicorn main:app --reload

# 5. Open the browser and visit
http://127.0.0.1:8000
