#############################
# List of required installs #
#############################
# python 3.10
# tkinter
# Pillow


###################
# List of imports #
###################

import tkinter as tk
# import tkinter.scrolledtext as tkscrolled

# from PrintAppFunctions import rangeToList
# from functools import partial
########################
# Initialising Program #
########################

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


# rangeLabel = tk.Label(text="Range test")
# rangeLabel.pack()

# rangeInput1 = tk.Entry()
# rangeInput1.pack()

# rangeInput2 = tk.Entry()
# rangeInput2.pack()

# rangeBtn = tk.Button(command=rangeToList(rangeInput1.get(),rangeInput2.get())
#                     ,text="Print")
# rangeBtn.pack()

# rangeList = tkscrolled.ScrolledText(height=12)
# rangeList.pack()


#################
# initiate loop #
#################
# if __name__ == '__main__':
#     main()