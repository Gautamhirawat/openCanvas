# import cv2
# import numpy as np
# import mediapipe as mp


# def detect_eraser_gesture(hand_landmarks):
#     # Example: If a fist is detected (all fingers are bent), enable eraser
#     fist_detected = all(hand_landmarks.landmark[i].y < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y for i in range(5, 21))
#     return fist_detected

# def detect_eraser_gesture(hand_landmarks):
#     # Implement gesture detection logic for eraser tool
#     # Example: Recognize when fingers are clenched to activate eraser
#     pass
