# import cv2

# def set_background(canvas, background_image_path):
#     background = cv2.imread(background_image_path)
#     background = cv2.resize(background, (canvas.shape[1], canvas.shape[0]))
#     canvas = cv2.addWeighted(canvas, 0.5, background, 0.5, 0)
#     return canvas
