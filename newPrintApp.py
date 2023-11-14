#############################
# List of required installs #
#############################
# python 3.10
# tkinter
# Pillow
# qrcode https://pypi.org/project/qrcode/


###################
# List of imports #
###################

import tkinter as tk
import tkinter.scrolledtext as tkscrolled

from tkinter import PhotoImage



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

#############################
# Import additional scripts #
#############################

from PrintAppFunctions import rangeToList, screenSwap
import settings
currentList=settings.currentList
tagQty = tk.StringVar(None,0)
###############
# Run Program #
###############

def updateLabels(): # Adds range to list and updates tag count
    rangeList.insert(tk.END, settings.currentList.get())    # Add current range to list
    settings.currentList.set('')                            # clears stored list from variables
    counter = 0
    for x in (rangeList.get('1.0', tk.END).split('\n')):    # split the list into lines
        print(x)
        if x:                                               # only count lines with something in them
            counter += 1
            print(counter)
    tagQty.set(counter)

    

rangeLabel = tk.Label(text="Range test")
rangeLabel.pack()

rangeInput1 = tk.Entry()
rangeInput1.pack()

rangeInput2 = tk.Entry()
rangeInput2.pack()

rangeBtn = tk.Button(command=lambda: [rangeToList(rangeInput1.get(),rangeInput2.get()),updateLabels()]
                    ,text="Add to List")
rangeBtn.pack()

# rangeList = tk.Label(textvariable=currentList)
rangeList = tkscrolled.ScrolledText(height=12)
rangeList.pack()

qty = tk.Label(text="Number of tags:")
qty.pack()
rangeQty = tk.Label(textvariable=str(tagQty))
rangeQty.pack()
qtyRefresh = tk.Button(command=updateLabels, text="Refresh")
qtyRefresh.pack()



def upperswitch():
     
    # Determine is on or off
    if settings.is_on:
        uppercase1.config(image = upperOff)
        settings.is_on = False
    else:
       
        uppercase1.config(image = upperOn)
        settings.is_on = True

upperOn = PhotoImage(file = "on.png")
upperOff = PhotoImage(file = "off.png")

uppercase1Label = tk.Label(text="Caps Lock?")
uppercase1Label.pack()

uppercase1 = tk.Button(root, image = upperOn, bd = 0, command = upperswitch)
uppercase1.pack()


#################
# initiate loop #
#################
if __name__ == '__main__': root.mainloop()
#     main()