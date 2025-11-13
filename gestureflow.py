import os
import absl.logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'   # Hide TensorFlow INFO/WARNING
absl.logging.set_verbosity(absl.logging.ERROR)  # Only show ERRORs

# ------------------ Imports ------------------
import cv2
import mediapipe as mp
import pyautogui
import threading
import speech_recognition as sr
import time
import math
from util import move_cursor
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc


# ------------------ Gesture Control Variables ------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
click_times = []
last_click_time = 0
click_cooldown = 0.3

# ------------------ Global Gesture Toggle ------------------
gesture_enabled = True


# ------------------ Volume Control Setup ------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

pyautogui.FAILSAFE = False

# ------------------ Voice Assistant ------------------
def listen_for_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 0.8

    
    while True:
        recognized = False 


        try:
            with mic as source:
                print("🎤 Listening for voice commands...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, phrase_time_limit=5)

            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                # Mouse control
                if "left click" in command:
                    pyautogui.leftClick()
                    recognized = True
                    print("✅ Left click performed")

                elif "double click" in command:
                    pyautogui.doubleClick()
                    recognized = True
                    print("✅ Double click performed")

                elif "right click" in command:
                    pyautogui.rightClick()
                    recognized = True
                    print("✅ Right click performed")

                elif "scroll" in command:
                    if "up" in command:
                        pyautogui.scroll(500)
                        recognized = True
                        print("✅ Scrolled up")
                    elif "down" in command:
                        pyautogui.scroll(-500)
                        recognized = True
                        print("✅ Scrolled down")
                    else:
                        print("⚠️ Please say 'scroll up' or 'scroll down'")

                # Volume control
                elif "volume up" in command:
                    current_vol = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(min(current_vol+0.05,1.0),None)
                    recognized = True
                    print("🔊 Volume Up")
                elif "volume down" in command:
                    current_vol = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(max(current_vol-0.05,0.0),None)
                    recognized = True
                    print("🔊 Volume Down")


                # Brightness control
                elif "brightness up" in command:
                    sbc.set_brightness("+5")
                    recognized = True
                    print("💡 Brightness Up")
                elif "brightness down" in command:
                    sbc.set_brightness("-5")
                    recognized = True
                    print("💡 Brightness Down")

                # Browser control and youtube control
                elif "open browser" in command:
                    import webbrowser
                    webbrowser.open("https://www.google.com")
                    recognized = True
                    print("🌐 Browser opened")
                elif "close browser" in command:
                    # Closes currently active window (browser if active)
                    pyautogui.hotkey("alt", "f4")
                    recognized = True
                    print("❌ Browser closed")

                # Typing text
                elif command.startswith("type "):
                    text_to_type = command.replace("type ","")
                    pyautogui.write(text_to_type)
                    recognized = True
                    print(f"📝 Typed text: {text_to_type}")

                # Search command
                elif command.startswith("search "):
                    search_text = command.replace("search ","")
                    import webbrowser
                    webbrowser.open(f"https://www.google.com/search?q={search_text}")
                    recognized = True
                    print(f"🔎 Searched: {search_text}")


                # Flag to track YouTube mode
                youtube_mode = False

                # Activate YouTube Mode
                if "open youtube" in command:
                    import webbrowser
                    webbrowser.open("https://www.youtube.com")
                    youtube_mode = True
                    recognized = True
                    print("▶️🌐 Opened YouTube")

                elif "close youtube" in command:
                    pyautogui.hotkey("alt", "f4")
                    youtube_mode = False
                    recognized = True
                    print("❌📺 Closed YouTube")

                # Typing text on YouTube
                elif command.startswith("type "):
                    text_to_type = command.replace("type ","")
                    pyautogui.write(text_to_type)
                    pyautogui.press("enter")  # Press Enter to search
                    recognized = True
                    print(f"📝🔎 Typed and searched on YouTube: {text_to_type}")

                # Search command on YouTube
                elif command.startswith("search "):
                    search_text = command.replace("search ","")
                    pyautogui.write(search_text)
                    pyautogui.press("enter")  # Press Enter to search
                    recognized = True
                    print(f"🔎 Searched YouTube for: {search_text}")
                    
                elif "play" in command:
                    pyautogui.press("space")
                    recognized = True
                    print("▶️ Playing YouTube")

                elif "pause" in command:
                    pyautogui.press("space")
                    recognized = True
                    print("⏸️ Paused YouTube")


                # Screenshot
                elif "screenshot" in command:
                    screenshot = pyautogui.screenshot()
                    file_name = f"screenshot_{int(time.time())}.png"
                    screenshot.save(file_name)
                    recognized = True
                    print(f"📸 Screenshot saved as {file_name}")

                    

                # Enable or Disable Gesture Control
                elif "disable gestures" in command:
                    global gesture_enabled
                    gesture_enabled = False
                    recognized = True
                    print("🙌 Gesture control disabled")

                elif "enable gestures" in command:
                    gesture_enabled = True
                    recognized = True
                    print("🤖 Gesture control enabled")


                # Exit program
                elif "stop" in command or "exit" in command or "quit" in command:
                    print("🛑 Exiting program")
                    os._exit(0)

                if not recognized:
                    print("⚠️ Command not recognized")

            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            except sr.RequestError as e:
                print("❌ Could not request results;", e)

        except Exception as e:
            print(f"❌ Microphone error: {e}")
            time.sleep(1)


# Start voice assistant in parallel thread
threading.Thread(target=listen_for_voice, daemon=True).start()



# ------------------ Hand Gesture Control ------------------
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

        # Flip frame for natural mirror movement
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                if gesture_enabled: 
                    # Move cursor
                    move_cursor(hand_landmarks, frame)
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get fingertips
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]
                ring_tip = hand_landmarks.landmark[16]
                pinky_tip = hand_landmarks.landmark[20]
                thumb_ip = hand_landmarks.landmark[3]
                thumb_mcp = hand_landmarks.landmark[2]
                index_mcp = hand_landmarks.landmark[5]
                pinky_mcp = hand_landmarks.landmark[17]


                # Thumb Up/Down logic
                thumb_up = thumb_tip.y < thumb_ip.y and thumb_ip.y < thumb_mcp.y
                thumb_down = thumb_tip.y > thumb_ip.y and thumb_ip.y > thumb_mcp.y

                # Finger states (1=up, 0=down)
                fingers = [1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0 for tip in [8,12,16,20]]

                # Distances for gestures
                dist_thumb_index = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
                dist_thumb_middle = math.hypot(thumb_tip.x - middle_tip.x, thumb_tip.y - middle_tip.y)
                dist_thumb_ring = math.hypot(thumb_tip.x - ring_tip.x, thumb_tip.y - ring_tip.y)

                now = time.time()

                # ---- Left Click / Double Click ----
                if dist_thumb_index < 0.06 and now - last_click_time > click_cooldown:
                    click_times.append(now)
                    last_click_time = now

                    if len(click_times) >= 2 and click_times[-1] - click_times[-2] < 0.4:
                        pyautogui.doubleClick()
                        cv2.putText(frame, "Double Click", (10,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
                        click_times = []
                    else:
                        pyautogui.click()
                        cv2.putText(frame, "Single Click", (10,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)

                    if len(click_times) > 2:
                        click_times.pop(0)

                # ---- Right Click ----
                if dist_thumb_middle < 0.06:
                    pyautogui.rightClick()
                    cv2.putText(frame, "Right Click", (10,90), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)

                # ---- Close Tab ----
                if dist_thumb_ring < 0.06:
                    pyautogui.hotkey("ctrl","w")
                    cv2.putText(frame,"Close Tab",(10,130),cv2.FONT_HERSHEY_SIMPLEX,1,(0,128,255),2)

                # ---- Scroll Mode (index+middle fingers up) ----
                if fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0:
                    if index_tip.y<0.4:
                        pyautogui.scroll(80)
                        cv2.putText(frame,"Scroll Up",(10,170),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                    elif index_tip.y>0.6:
                        pyautogui.scroll(-80)
                        cv2.putText(frame,"Scroll Down",(10,170),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                # ---- Volume Control (Index + Middle + Ring + Pinky up) ----
                if fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1:
                    current_vol = volume.GetMasterVolumeLevelScalar()
                    if index_tip.y < 0.3:
                        volume.SetMasterVolumeLevelScalar(min(current_vol+0.05,1.0), None)
                        cv2.putText(frame,"Volume Up",(10,210),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                    elif index_tip.y > 0.7:
                        volume.SetMasterVolumeLevelScalar(max(current_vol-0.05,0.0), None)
                        cv2.putText(frame,"Volume Down",(10,210),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                # ---- Brightness Control (index+middle+ring fingers up) ----
                if fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0:
                    now = time.time()
                    if now - last_click_time > 0.5:  # add cooldown
                        if index_tip.y < 0.3:
                            sbc.set_brightness("+5")
                            cv2.putText(frame,"Brightness Up",(10,250),cv2.FONT_HERSHEY_SIMPLEX,1,(128,255,0),2)
                            last_click_time = now
                        elif index_tip.y > 0.55:
                            sbc.set_brightness("-5")
                            cv2.putText(frame,"Brightness Down",(10,250),cv2.FONT_HERSHEY_SIMPLEX,1,(128,0,255),2)
                            last_click_time = now


        cv2.imshow("Gesture Control",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()