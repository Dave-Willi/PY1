#############################
# List of required installs #
#############################



###################
# List of imports #
###################

import os, sys
import win32print
from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.title("NDC Config Label Printing") # App title, appears in title bar of app window
appWidth = 1290 # App width in pixels
appHeight = 860 # App height in pixels

# Get screen resolution
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the app window - A touch above centre position
x = (ws/2) - (appWidth/2)
y = (hs/2) - (appHeight/2) - 50

# set the dimensions of the window and where it is placed
root.geometry('%dx%d+%d+%d' % (appWidth, appHeight, x, y))
root.resizable(False,False) # Disable resizing of window



root.mainloop()