import cv2
import numpy as np
import mediapipe as mp
from undo_redo import initialize_undo_redo, add_to_undo_stack, undo, redo
# from dynamic_brush_size import change_brush_size
# from shape_drawing import draw_shape
from save_load import save_drawing, load_drawing
# from color_picker import get_color_from_palette
# from multi_finger_gestures import handle_zoom
# from multiple_colors import switch_color
from brush_textures import apply_brush_texture
# from background_image import set_background
# from gesture_eraser import detect_eraser_gesture
from drawing_layers import initialize_layers, add_layer, switch_layer

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Initialize variables for drawing
drawing = False
color = (0, 0, 255)  # Default color: Red
brush_size = 5
tool = "pen"  # Default tool
prev_x, prev_y = None, None

# Set the window size to a larger resolution
window_width = 1280
window_height = 720

# Open webcam and set resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)
ret, frame = cap.read()

if ret:
    frame_height, frame_width, _ = frame.shape
    # Initialize drawing layers
    initialize_layers(frame_height, frame_width)
    # Create a black image for drawing
    canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

# Initialize Undo/Redo
initialize_undo_redo(canvas)

def is_finger_on_button(x, y, button_x, button_y, button_width, button_height):
    """
    Checks if the finger tip coordinates (x, y) are within the button boundaries.

    Parameters:
        x, y (int): Coordinates of the finger tip.
        button_x, button_y (int): Top-left corner coordinates of the button.
        button_width, button_height (int): Width and height of the button.

    Returns:
        bool: True if the finger tip is on the button, False otherwise.
    """
    if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
        return True
    else:
        return False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Ensure the canvas matches the frame size
    if canvas.shape[0] != frame_height or canvas.shape[1] != frame_width:
        canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the tip of the index finger
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x_tip = int(index_finger_tip.x * frame_width)
            y_tip = int(index_finger_tip.y * frame_height)

            # Check for button clicks
            if is_finger_on_button(x_tip, y_tip, 20, 20, 50, 30):  # Red color button
                color = (0, 0, 255)
            elif is_finger_on_button(x_tip, y_tip, 90, 20, 50, 30):  # Green color button
                color = (0, 255, 0)
            elif is_finger_on_button(x_tip, y_tip, 160, 20, 50, 30):  # Blue color button
                color = (255, 0, 0)
            elif is_finger_on_button(x_tip, y_tip, 230, 20, 50, 30):  # Pen tool
                tool = "pen"
                brush_size = 5
                color = (0, 0, 255)  # Default pen color
            elif is_finger_on_button(x_tip, y_tip, 300, 20, 50, 30):  # Brush tool
                tool = "brush"
                brush_size = 15
                color = (0, 0, 255)  # Default brush color
            elif is_finger_on_button(x_tip, y_tip, 370, 20, 50, 30):  # Eraser tool
                tool = "eraser"
                brush_size = 20
                color = (0, 0, 0)  # Eraser color
            elif is_finger_on_button(x_tip, y_tip, 440, 20, 50, 30):  # Clear button
                canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)  # Clear the canvas
                initialize_undo_redo(canvas)  # Reinitialize Undo/Redo when the canvas is cleared
            elif is_finger_on_button(x_tip, y_tip, 510, 20, 50, 30):  # Undo button
                canvas = undo(canvas)
            elif is_finger_on_button(x_tip, y_tip, 580, 20, 50, 30):  # Redo button
                canvas = redo(canvas)
            elif is_finger_on_button(x_tip, y_tip, 850, 20, 50, 30):  # save drawing
                canvas = save_drawing(canvas)

            # Draw on the canvas if drawing is enabled
            if drawing:
                if prev_x is not None and prev_y is not None:
                    if tool == "pen" or tool == "brush":
                        canvas = apply_brush_texture(canvas, (prev_x, prev_y), (x_tip, y_tip), color, tool, brush_size)
                    elif tool == "eraser":
                        cv2.line(canvas, (prev_x, prev_y), (x_tip, y_tip), color, brush_size)
                prev_x, prev_y = x_tip, y_tip
            else:
                prev_x, prev_y = None, None

            # Toggle drawing when the finger is not on any button
            if not (is_finger_on_button(x_tip, y_tip, 20, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 90, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 160, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 230, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 300, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 370, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 440, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 510, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 580, 20, 50, 30) or
                    is_finger_on_button(x_tip, y_tip, 900, 20, 50, 30)):
                drawing = True
            else:
                drawing = False

    # Overlay the canvas on the frame
    frame = cv2.addWeighted(frame, 1, canvas, 0.5, 0)

    # Draw buttons
    cv2.rectangle(frame, (20, 20), (70, 50), (0, 0, 255), -1)  # Red button
    cv2.rectangle(frame, (90, 20), (140, 50), (0, 255, 0), -1)  # Green button
    cv2.rectangle(frame, (160, 20), (210, 50), (255, 0, 0), -1)  # Blue button
    cv2.rectangle(frame, (230, 20), (280, 50), (128, 128, 128), -1)  # Pen button
    cv2.rectangle(frame, (300, 20), (350, 50), (128, 128, 128), -1)  # Brush button
    cv2.rectangle(frame, (370, 20), (420, 50), (128, 128, 128), -1)  # Eraser button
    cv2.rectangle(frame, (440, 20), (490, 50), (128, 128, 128), -1)  # Clear button
    cv2.rectangle(frame, (510, 20), (560, 50), (128, 128, 128), -1)  # Undo button
    cv2.rectangle(frame, (580, 20), (630, 50), (128, 128, 128), -1)  # Redo button
    cv2.rectangle(frame, (900, 20), (820, 50), (128, 128, 128), -1)

    # Add text to buttons
    cv2.putText(frame, 'Red', (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Green', (95, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Blue', (165, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Pen', (235, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Brush', (305, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Eraser', (375, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Clear', (445, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Undo', (515, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Redo', (585, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, 'Save', (850, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


    # Display the frame
    cv2.imshow("Hand Tracking Drawing", frame)

    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
