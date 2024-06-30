import cv2
import numpy as np


def apply_brush_texture(canvas, start_point, end_point, color, texture, brush_size):
    if texture == "spray":
        for _ in range(brush_size * 10):
            offset_x = np.random.randint(-brush_size, brush_size)
            offset_y = np.random.randint(-brush_size, brush_size)
            if 0 <= start_point[0] + offset_x < canvas.shape[1] and 0 <= start_point[1] + offset_y < canvas.shape[0]:
                canvas[start_point[1] + offset_y, start_point[0] + offset_x] = color
    else:
        cv2.line(canvas, start_point, end_point, color, brush_size)
    return canvas


def apply_paintbrush_texture(canvas, start_point, end_point, color, brush_size):
    # Implement paintbrush texture logic
    cv2.line(canvas, start_point, end_point, color, brush_size)
    return canvas

def apply_spray_paint_texture(canvas, center, color, brush_size):
    # Implement spray paint texture logic
    cv2.circle(canvas, center, brush_size, color, -1)
    return canvas
