import tkinter as tk
from tkinter import messagebox
import settings as _set
import re

def barcodeLabelSelection(button):
    # Your function implementation
    pass

def updateTextLabels(event=None):
    # Your function implementation
    pass

def addToList(itemsForList): # To add labels to the currently active list
    _set.currentList.set(itemsForList)

def rangeToList(range1,range2, split): # To take 2 points of a range and create a list going from one to the other
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
            prefixed = str(rangePrefix1)
            suffixed = str(rangeSuffix1)
            newlist = ""
            for x in range(int(rangeStart), int(rangeEnd)+1):
                y = str(x).zfill(lead_zeros)
                newlist += prefixed + y + suffixed + split
            addToList(newlist)
            addRangeBarcodeEntry1.delete(0, 'end')
            addRangeBarcodeEntry2.delete(0, 'end')

    return

def ReturnKeyPress(event_type):
    # Your function implementation
    pass

def newButton2(parent, text, command):
    # Your function implementation
    pass

def allCaps(parent, text):
    # Your function implementation
    pass
