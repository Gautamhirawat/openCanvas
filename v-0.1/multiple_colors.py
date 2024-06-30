# def switch_color(current_color):
#     # Define a list of colors to cycle through
#     colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # Example: Red, Green, Blue
    
#     # Find the index of the current color in the list
#     try:
#         index = colors.index(current_color)
#     except ValueError:
#         index = 0  # Default to the first color if current_color is not found
    
#     # Cycle to the next color
#     next_index = (index + 1) % len(colors)
#     return colors[next_index]
