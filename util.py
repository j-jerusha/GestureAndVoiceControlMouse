# util.py
import pyautogui
import mediapipe as mp

# Screen size
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

def move_cursor(hand_landmarks, frame, smoothing=7):
    """
    Moves the mouse cursor based on the index fingertip position.

    Args:
        hand_landmarks: mediapipe hand landmarks
        frame: OpenCV frame (to get width/height)
        smoothing: int, higher = smoother but slower cursor
    """
    # Index fingertip
    index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]

    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape

    # Convert normalized coordinates to pixel coordinates
    x = int(index_tip.x * frame_width)
    y = int(index_tip.y * frame_height)

    # Map to screen coordinates
    screen_x = int(x * SCREEN_WIDTH / frame_width)
    screen_y = int(y * SCREEN_HEIGHT / frame_height)

    # Get current mouse position
    curr_x, curr_y = pyautogui.position()

    # Smooth the cursor movement
    new_x = curr_x + (screen_x - curr_x) / smoothing
    new_y = curr_y + (screen_y - curr_y) / smoothing

    pyautogui.moveTo(new_x, new_y)

