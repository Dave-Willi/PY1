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
import tkinter.ttk as ttk
import tkinter.scrolledtext as tkscrolled
from tkinter import PhotoImage, ttk, Frame
from PIL import Image, ImageTk



########################
# Initialising Program #
########################

root = tk.Tk()
root.title("NDC Config Label Printing") # App title, appears in title bar of app window
root.configure(bg = "#27374D")
root.option_add("*Font", "aerial")
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
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
#############################
# Import additional scripts #
#############################

import PrintAppFunctions
from PrintAppFunctions import rangeToList, screenSwap, backBtn, helpBtn, historyBtn, settingsBtn, addToList, printerSelect, printList, clearVars, clearInputs, idleTimer
import settings
currentPage = settings.currentPage
currentList = settings.currentList
tagQty = tk.StringVar(None,0)

#################
# Create styles #
#################

style = ttk.Style()
style.configure('W.TButton', font = ('calibri', 10, 'bold'),
                foreground = 'black', background = 'green', relief = 'flat')


##########################
# Assign frames to pages #
##########################

### Primary frame / grid ###
# 2x rows
# 1x column
# top row for title bar and header, static and consistent throughout the whole app
# 2nd row has embedded gui for all the pages in the app
#   Takes the bulk of the app
#   All pages use this row to place their widgets etc
#   Contents changes to suit page
#   Attempt to keep all widgets fitted into a 8x10 subgrid within 2nd row in primary grid
#
#   Backgrounds = #001F3F
#   Control colours = #083358
#   Fonts/foreground = #9DB2BF
#   Special Highlights = #FFD717

backgroundColor = "#001F3F"
controlsColor = "#083358"
fontColor = "#9DB2BF"
specialColor = "#FFD717"

PrimaryContainer = tk.Frame(root, bg = backgroundColor)
PrimaryContainer.columnconfigure(0, weight = 1)
PrimaryContainer.rowconfigure(0, weight = 0)
PrimaryContainer.rowconfigure(1, weight = 1)
PrimaryContainer.grid(row = 0, column = 0, sticky = "nsew")

TitleFrame = tk.Frame(PrimaryContainer, bg = controlsColor)
TitleFrame.grid(row = 0, column = 0, sticky = "nsew")
TitleFrame.columnconfigure(0, weight = 1)
TitleFrame.columnconfigure(2, weight = 1, minsize = 144)
TitleFrame.columnconfigure(1, weight = 8)

TitleContentImage0 = Image.open('CDW.PNG')
TitleContentImage1 = ImageTk.PhotoImage(TitleContentImage0.resize((144,80)))
TitleImageWidth, TitleImageHeight = TitleContentImage1.width(), TitleContentImage1.height()
TitleContentLabel0 = tk.Canvas(TitleFrame, bg = controlsColor, width = TitleImageWidth, height = TitleImageHeight, bd = 0, highlightthickness = 0)
TitleContentLabel0.grid(row = 0, column = 0, sticky = "ew", padx = 15, pady = 10)
TitleContentLabel0.create_image(0, 0, image = TitleContentImage1, anchor = tk.NW)

TitleContentLabel1 = tk.Label(TitleFrame, text = "NDC Config Label Printer", bg = controlsColor, fg = specialColor, font = 'verdana 32 bold')
TitleContentLabel1.grid(row = 0, column = 1, sticky = "ew")



PageFrame = tk.Frame(PrimaryContainer, bg = backgroundColor)
PageFrame.rowconfigure(0, weight = 1)
PageFrame.columnconfigure(0, weight = 1)
PageFrame.columnconfigure(1, weight = 10)
PageFrame.grid(row = 1, column = 0, sticky = "nsew")

TitleContentLabel2 = tk.Label(PageFrame, text = "Tulips are for kissing", bg = backgroundColor, fg = fontColor)
TitleContentLabel2.grid(row = 0, columnspan = 2, sticky = "ew")

LeftControlFrame = tk.Frame(PageFrame, bg = backgroundColor)
LeftControlFrame.grid(row = 0, column = 0, sticky = "nsw")

LeftControlBackBtn = tk.Button(LeftControlFrame, text = "Back", width = 15
                            #    ,command = backBtn()
                               ,command = root.destroy
                               ,bg = controlsColor
                               ,fg = specialColor
                               ,relief = "flat")
LeftControlBackBtn.grid(row = 0, column = 0, padx = 15, pady = 10)

LeftControlHelpBtn = tk.Button(LeftControlFrame, text = "Help", width = 15
                               ,command = helpBtn()
                               ,bg = controlsColor
                               ,fg = specialColor
                               ,relief = "flat")
LeftControlHelpBtn.grid(row = 10, column = 0, padx = 15, pady = (580,5))

LeftControlHistoryBtn = tk.Button(LeftControlFrame, text = "Print History", width = 15
                               ,command = historyBtn()
                               ,bg = controlsColor
                               ,fg = specialColor
                               ,relief = "flat")
LeftControlHistoryBtn.grid(row = 12, column = 0, padx = 15, pady = 5)

LeftControlSettingsBtn = tk.Button(LeftControlFrame, text = "Settings", width = 15
                               ,command = settingsBtn()
                               ,bg = controlsColor
                               ,fg = specialColor
                               ,relief = "flat")
LeftControlSettingsBtn.grid(row = 14, column = 0, padx = 15, pady = 5)

# Pagelabel = tk.Label(PageFrame, text = "Tulips are for kissing", bg = "#27374D", fg = "gray90")
# Pagelabel.grid(row = 0, column = 0, sticky = "ew")
"""

###############
# Run Program #
###############

def updateLabels(): # Adds range to list and updates tag count
    rangeList.insert(tk.END, settings.currentList.get())    # Add current range to list
    settings.currentList.set('')                            # clears stored list from variables
    counter = 0
    for x in (rangeList.get('1.0', tk.END).split('\n')):    # split the list into lines
        if x:                                               # only count lines with something in them
            counter + =  1
    tagQty.set(counter)



rangeLabel = tk.Label(text = "Range test")
rangeLabel.pack()

rangeInput1 = tk.Entry()
rangeInput1.pack()

rangeInput2 = tk.Entry()
rangeInput2.pack()

rangeBtn = tk.Button(command = lambda: [rangeToList(rangeInput1.get(),rangeInput2.get()),updateLabels()]
                    ,text = "Add to List")
rangeBtn.pack()

# rangeList = tk.Label(textvariable = currentList)
rangeList = tkscrolled.ScrolledText(height = 12)
rangeList.pack()

qty = tk.Label(text = "Number of tags:")
qty.pack()
rangeQty = tk.Label(textvariable = str(tagQty))
rangeQty.pack()
qtyRefresh = tk.Button(command = updateLabels, text = "Refresh")
qtyRefresh.pack()



def upperswitch():
     
    # Determine is on or off
    if settings.is_on:
        uppercase1.config(image = upperOff)
        settings.is_on = False
    else:
        uppercase1.config(image = upperOn)
        settings.is_on = True

upperOnIMG = Image.open('on.png')
upperOffIMG = Image.open('off.png')
upperOnRes = upperOnIMG.resize((40,20))
upperOffRes = upperOffIMG.resize((40,20))
upperOn = ImageTk.PhotoImage(upperOnRes)
upperOff = ImageTk.PhotoImage(upperOffRes)

uppercase1Label = tk.Label(text = "Caps Lock?")
uppercase1Label.pack()

uppercase1 = tk.Button(root, image = upperOn, bd = 0, command = upperswitch)
uppercase1.pack()

"""

#################
# initiate loop #
#################
if __name__ == '__main__': root.mainloop()
#     main()