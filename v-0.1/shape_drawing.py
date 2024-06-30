def draw_shape(canvas, shape, start_point, end_point, color, brush_size):
    if shape == "circle":
        center = start_point
        radius = int(((start_point[0] - end_point[0]) ** 2 + (start_point[1] - end_point[1]) ** 2) ** 0.5)
        cv2.circle(canvas, center, radius, color, brush_size)
    elif shape == "rectangle":
        cv2.rectangle(canvas, start_point, end_point, color, brush_size)
    elif shape == "line":
        cv2.line(canvas, start_point, end_point, color, brush_size)
    return canvas
