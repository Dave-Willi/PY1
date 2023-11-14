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
import tkinter.scrolledtext as tkscrolled
# from PrintAppFunctions import rangeToList
from functools import partial
from tkinter import messagebox
import re


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






def rangeToList(range1,range2): # To take 2 points of a range and create a list going from one to the other
    print("This is not running")
    print(range1)
    print(range2)
    if range1 == "" or range2 =="" or len(range1) != len(range2): # error out of function if one or both range values are empty or they don't match length
        return -1
    rangePrefix1 = ""
    rangeStart = ""
    rangeSuffix1 = "" 
    rangePrefix2 = ""
    rangeEnd = ""
    rangeSuffix2 = ""
    rangeSplit1 = re.split("(\d+)", range1)
    rangeSplit2 = re.split("(\d+)", range2)
    y = 0
    z = 0
    for x in rangeSplit1: #cycles through however many splits exist in the first split
        if rangeSplit1[y] != rangeSplit2[y]:
            z = y + 1
            rangeStart = min(rangeSplit1[y],rangeSplit2[y]) # sets the lowest number entered into the start
            rangeEnd = max(rangeSplit2[y],rangeSplit1[y]) # sets the highest number entered into the end
            for x in rangeSplit1[z:]:
                try:
                    if rangeSplit1[z] == rangeSplit2[z]:
                        rangeSuffix1 += x
                        rangeSuffix2 += x
                        z+=1
                    else:
                        messagebox.showerror("Error", "Problem determining the suffix")
                        return
                except:
                    break
            break
        elif rangeSplit1[y] == rangeSplit2[y]:
            rangePrefix1 += x
            rangePrefix2 += x
        y+=1
    if rangePrefix1 != rangePrefix2:
        messagebox.showerror("Error", "Error detected in the prefix. \nPlease check and try again")
        return
    elif rangeSuffix1 != rangeSuffix2:
        messagebox.showerror("Error", "Error detected in the suffix. \nPlease check and try again")
        return
    else:
            lead_zeros = len(rangeEnd)
            prefixed = str(rangePrefix1).upper()
            suffixed = str(rangeSuffix1).upper()
            newlist = ""
            for x in range(int(rangeStart), int(rangeEnd)+1):
                y = str(x).zfill(lead_zeros)
                newlist += prefixed + y + suffixed
            # addToList(newlist)
            print(newlist)
            # clearInputs()
    return







rangeLabel = tk.Label(text="Range test")
rangeLabel.pack()

rangeInput1 = tk.Entry()
rangeInput1.pack()

rangeInput2 = tk.Entry()
rangeInput2.pack()

rangeBtn = tk.Button(command=rangeToList(rangeInput1.get(),rangeInput2.get())
                    ,text="Print")
rangeBtn.pack()

rangeList = tkscrolled.ScrolledText(height=12)
rangeList.pack()


#################
# initiate loop #
#################
# if __name__ == '__main__':
#     main()