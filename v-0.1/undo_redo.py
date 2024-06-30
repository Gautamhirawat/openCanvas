import cv2
import numpy as np

undo_stack = []
redo_stack = []

def initialize_undo_redo(canvas):
    global undo_stack, redo_stack
    undo_stack = []
    redo_stack = []
    undo_stack.append(canvas.copy())

def add_to_undo_stack(canvas):
    global undo_stack
    undo_stack.append(canvas.copy())

def undo(canvas):
    global undo_stack, redo_stack
    if len(undo_stack) > 1:
        redo_stack.append(undo_stack.pop())
        canvas = undo_stack[-1].copy()
    return canvas

def redo(canvas):
    global undo_stack, redo_stack
    if redo_stack:
        canvas = redo_stack.pop().copy()
        undo_stack.append(canvas.copy())
    return canvas
