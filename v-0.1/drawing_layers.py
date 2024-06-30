import numpy as np

def initialize_layers(height, width):
    global layers, current_layer_index
    layers = [np.zeros((height, width, 3), dtype=np.uint8)]
    current_layer_index = 0

def add_layer(height, width):
    global layers, current_layer_index
    layers.append(np.zeros((height, width, 3), dtype=np.uint8))
    current_layer_index = len(layers) - 1

# def switch_layer(index):
#     global current_layer_index
#     if 0 <= index < len(layers):
#         current_layer_index = index
#     return layers[current_layer_index]


def switch_layer(layer_index):
    # Switch to a different layer for drawing
    global layers
    if 0 <= layer_index < len(layers):
        return layers[layer_index]
    else:
        return layers[0] 