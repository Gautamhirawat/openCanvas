import cv2

def save_drawing(canvas):
    cv2.imwrite("canvas.png", canvas)  # Use a supported image format

def load_drawing(file_name):
    return cv2.imread(file_name)
