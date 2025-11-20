import os
import absl.logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
absl.logging.set_verbosity(absl.logging.ERROR)

# ------------------ Imports ------------------
import cv2
import mediapipe as mp
import pyautogui
import threading
import speech_recognition as sr
import time
import math
from util import move_cursor
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL, CoCreateInstance
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IMMDeviceEnumerator, EDataFlow, ERole
from pycaw.constants import CLSID_MMDeviceEnumerator
import screen_brightness_control as sbc

# ------------------ Gesture Control Variables ------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
click_times = []
last_click_time = 0
click_cooldown = 0.3

# ------------------ Global Gesture Toggle ------------------
gesture_enabled = True

# ------------------ Volume Control Setup (FIXED) ------------------
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
except AttributeError:
    # Fallback method for newer pycaw versions
    deviceEnumerator = CoCreateInstance(
        CLSID_MMDeviceEnumerator,
        IMMDeviceEnumerator,
        CLSCTX_ALL
    )
    speakers = deviceEnumerator.GetDefaultAudioEndpoint(EDataFlow.eRender.value, ERole.eMultimedia.value)
    interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

pyautogui.FAILSAFE = False


# ------------------ Voice Assistant ------------------
def listen_for_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 0.8

    youtube_mode = False  # global YouTube flag

    while True:
        recognized = False

        try:
            with mic as source:
                print("🎤 Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, phrase_time_limit=5)

            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                # ------------- MOUSE CONTROL -------------
                if "left click" in command:
                    pyautogui.leftClick()
                    print("Left click")
                    recognized = True

                elif "double click" in command:
                    pyautogui.doubleClick()
                    print("Double click")
                    recognized = True

                elif "right click" in command:
                    pyautogui.rightClick()
                    print("Right click")
                    recognized = True

                elif "scroll up" in command:
                    pyautogui.scroll(500)
                    recognized = True

                elif "scroll down" in command:
                    pyautogui.scroll(-500)
                    recognized = True

                # ------------- VOLUME -------------
                elif "volume up" in command:
                    v = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(min(v + 0.05, 1.0), None)
                    print("Volume up")
                    recognized = True

                elif "volume down" in command:
                    v = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(max(v - 0.05, 0.0), None)
                    print("Volume down")
                    recognized = True

                # ------------- BRIGHTNESS -------------
                elif "brightness up" in command:
                    sbc.set_brightness("+5")
                    print("Brightness up")
                    recognized = True

                elif "brightness down" in command:
                    sbc.set_brightness("-5")
                    print("Brightness down")
                    recognized = True

                # ------------- BROWSER -------------
                elif "open browser" in command:
                    import webbrowser
                    webbrowser.open("https://www.google.com")
                    print("Browser opened")
                    recognized = True

                elif "close browser" in command:
                    pyautogui.hotkey("alt", "f4")
                    print("Browser closed")
                    recognized = True

                # ------------- YOUTUBE MODE -------------
                elif "open youtube" in command:
                    import webbrowser
                    webbrowser.open("https://www.youtube.com")
                    youtube_mode = True
                    print("YouTube opened")
                    recognized = True

                elif "close youtube" in command:
                    youtube_mode = False
                    pyautogui.hotkey("alt", "f4")
                    print("YouTube closed")
                    recognized = True

                elif youtube_mode and command.startswith("search "):
                    text = command.replace("search ", "")
                    pyautogui.write(text)
                    pyautogui.press("enter")
                    print(f"Searched YouTube for: {text}")
                    recognized = True

                elif youtube_mode and command.startswith("type "):
                    text = command.replace("type ", "")
                    pyautogui.write(text)
                    pyautogui.press("enter")
                    print(f"YouTube typed: {text}")
                    recognized = True

                elif youtube_mode and "play" in command:
                    pyautogui.press("space")
                    print("YouTube play")
                    recognized = True

                elif youtube_mode and "pause" in command:
                    pyautogui.press("space")
                    print("YouTube pause")
                    recognized = True

                # ------------- GLOBAL TYPE / SEARCH -------------
                elif command.startswith("type "):
                    text = command.replace("type ", "")
                    pyautogui.write(text)
                    print("Typed:", text)
                    recognized = True

                elif command.startswith("search "):
                    text = command.replace("search ", "")
                    import webbrowser
                    webbrowser.open(f"https://www.google.com/search?q={text}")
                    print("Searched Google:", text)
                    recognized = True

                # ------------- SCREENSHOT -------------
                elif "screenshot" in command:
                    name = f"screenshot_{int(time.time())}.png"
                    pyautogui.screenshot().save(name)
                    print("Screenshot saved:", name)
                    recognized = True

                # ------------- GESTURE TOGGLE -------------
                elif "disable gestures" in command:
                    global gesture_enabled
                    gesture_enabled = False
                    print("Gestures disabled")
                    recognized = True

                elif "enable gestures" in command:
                    gesture_enabled = True
                    print("Gestures enabled")
                    recognized = True

                # ------------- EXIT -------------
                elif "stop" in command or "exit" in command:
                    print("Exiting program...")
                    os._exit(0)

                if not recognized:
                    print("⚠️ Command not recognized")

            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            except sr.RequestError as e:
                print("❌ Speech API error:", e)

        except Exception as e:
            print("❌ Microphone error:", e)
            time.sleep(1)


# Start voice assistant thread
threading.Thread(target=listen_for_voice, daemon=True).start()


# ------------------ HAND GESTURE CONTROL ------------------
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    print("Hand gesture control running... Press 'q' to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                if gesture_enabled:
                    move_cursor(hand_landmarks, frame)
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Fingertip indices
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]
                ring_tip = hand_landmarks.landmark[16]

                now = time.time()

                # ----------------- Finger Distance -----------------
                dist_index = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
                dist_middle = math.hypot(thumb_tip.x - middle_tip.x, thumb_tip.y - middle_tip.y)
                dist_ring = math.hypot(thumb_tip.x - ring_tip.x, thumb_tip.y - ring_tip.y)

                # ----------------- Single / Double Click -----------------
                if dist_index < 0.06 and now - last_click_time > click_cooldown:
                    click_times.append(now)
                    last_click_time = now

                    if len(click_times) >= 2 and click_times[-1] - click_times[-2] < 0.4:
                        pyautogui.doubleClick()
                        cv2.putText(frame, "Double Click", (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        click_times = []
                    else:
                        pyautogui.click()
                        cv2.putText(frame, "Single Click", (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

                # ----------------- Right Click -----------------
                if dist_middle < 0.06:
                    pyautogui.rightClick()
                    cv2.putText(frame, "Right Click", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

                # ----------------- Close Tab -----------------
                if dist_ring < 0.06:
                    pyautogui.hotkey("ctrl", "w")
                    cv2.putText(frame, "Close Tab", (10, 130),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 128, 255), 2)

        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()