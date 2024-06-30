# import cv2

# def get_color_from_palette(x_tip, y_tip):
#     # Define coordinates and colors for the palette buttons
#     palette_buttons = {
#         (20, 80): (0, 0, 255),   # Red button
#         (90, 80): (0, 255, 0),   # Green button
#         (160, 80): (255, 0, 0),  # Blue button
#         # Add more colors as needed
#     }
    
#     for (button_x, button_y), color in palette_buttons.items():
#         button_width, button_height = 50, 30
#         if button_x <= x_tip <= button_x + button_width and button_y <= y_tip <= button_y + button_height:
#             return color
    
#     return None  # Return None if no color is selected
