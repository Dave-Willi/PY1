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
from tkinter import ttk
import tkinter.font as tkFont
import tkinter.scrolledtext as tkscrolled
from PIL import Image, ImageTk

#################
# Create styles #
#################

### Set standardised colours to use throughout
backgroundColor = "#001F3F" # A dark blue                           #001F3F
controlsColor = "#083358"   # A less dark blue                      #083358
fontColor = "#9DB2BF"       # A light gray with a tint of blue      #9DB2BF
specialColor = "#FFD717"    # Bright yellow                         #FFD717

### Standard button style
# [buttonName] = tk.Button(LeftControlFrame, text = "buttonText", width = 15
#                                ,command = [buttonCommand]
#                                ,bg = controlsColor
#                                ,fg = specialColor
#                                ,relief = "flat")
# [buttonName].grid(row = y, column = x, padx = 15, pady = 10)

########################
# Initialising Program #
########################

class printApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        varappversion = tk.StringVar(None, 'Version 2.0.0')       # current app version #

        ################
        # Apply window #
        ################

        self.title("NDC Config Label Printing")
        appWidth = 1290 # App width in pixels
        appHeight = 860 # App height in pixels

        ### Font styles
        self.option_add("*Font", "aerial")
        fontHeaderH1 = tkFont.Font(size=28)

        # Get screen resolution
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # calculate x and y coordinates for the app window - A touch above centre position
        x = (ws/2) - (appWidth/2)
        y = (hs/2) - (appHeight/2) - 50

        # set the dimensions of the window and where it is placed
        self.geometry('%dx%d+%d+%d' % (appWidth, appHeight, x, y))
        self.resizable(False,False) # Disable resizing of window
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.configure(bg = backgroundColor)

        from PrintAppFunctions import rangeToList, backBtn, helpBtn, historyBtn, settingsBtn, addToList, printerSelect, printList, clearVars, clearInputs, idleTimer
        import settings

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

        # Primary container splits between Titlebar and lower
        PrimaryContainer = tk.Frame(self, bg = backgroundColor)
        PrimaryContainer.columnconfigure(0, weight = 1)
        PrimaryContainer.rowconfigure(0, weight = 0)
        PrimaryContainer.rowconfigure(1, weight = 1)
        PrimaryContainer.grid(row = 0, column = 0, sticky = "nsew")

        # Frame injected to split up Titlebar into 3
        TitleFrame = tk.Frame(PrimaryContainer, bg = controlsColor)
        TitleFrame.grid(row = 0, column = 0, sticky = "nsew")
        TitleFrame.columnconfigure(0, weight = 1)
        TitleFrame.columnconfigure(2, weight = 1, minsize = 144)
        TitleFrame.columnconfigure(1, weight = 8)

        # Frame to split lower section into two, the main space and the space for the control sidebar
        PageFrame = tk.Frame(PrimaryContainer, bg = backgroundColor)
        PageFrame.rowconfigure(0, weight = 1)
        PageFrame.columnconfigure(0, weight = 0)
        PageFrame.columnconfigure(1, weight = 10)
        PageFrame.grid(row = 1, column = 0, sticky = "nsew")

        # Frame for the controls sidebar
        LeftControlFrame = tk.Frame(PageFrame, bg = backgroundColor)
        LeftControlFrame.grid(row = 0, column = 0, sticky = "nsw")

        # Container Frame for the pages
        HomePage = tk.Frame(PageFrame, bg=backgroundColor)
        HomePage.rowconfigure((0,1,2,3,4,5), weight=1)
        HomePage.columnconfigure((0,1,2,3), weight=1)
        HomePage.grid(row=0, column=1, sticky="nsew")

        BarcodesPage = tk.Frame(PageFrame, bg=backgroundColor)
        BarcodesPage.columnconfigure((0,1,2,3,4), weight=1)
        BarcodesPage.rowconfigure((0,1,2,3,4,5), weight=1)
        BarcodesPage.grid(row=0, column=1, sticky="nsew")

        QRcodePage = tk.Frame(PageFrame, bg=backgroundColor)
        QRcodePage.columnconfigure((0,1,2,3,4), weight=1)
        QRcodePage.rowconfigure((0,1,2,3,4,5,6,7), weight=1)
        QRcodePage.grid(row=0, column=1, sticky="nsew")

        plainPage = tk.Frame(PageFrame, bg=backgroundColor)
        plainPage.columnconfigure((0,1,2,3,4), weight=1)
        plainPage.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        plainPage.grid(row=0, column=1, sticky="nsew")

        customerPage = tk.Frame(PageFrame, bg=backgroundColor)
        customerPage.columnconfigure((0,1,2,3,4,5), weight=1)
        customerPage.rowconfigure((0,1,2,3,4,5,6), weight=1)
        customerPage.grid(row=0, column=1, sticky="nsew")

        helpPage = tk.Frame(PageFrame, bg=backgroundColor)
        helpPage.rowconfigure((0,1,20,21,22), weight=1)
        helpPage.grid(row=0, column=1, sticky="nsew")

        historyPage = tk.Frame(PageFrame, bg=backgroundColor)
        historyPage.grid(row=0, column=1, sticky="nsew")

        settingsPage = tk.Frame(PageFrame, bg=backgroundColor)
        settingsPage.rowconfigure((0,1,20,21,22), weight=1)
        settingsPage.grid(row=0, column=1, sticky="nsew")
        
        HomePage.tkraise()

        #########################
        # Add content to frames #
        #########################

        # Image and text for titlebar
        try:
            TitleCompanyImage0 = Image.open('CDW.PNG')
            TitleCompanyImage1 = ImageTk.PhotoImage(TitleCompanyImage0.resize((144,80)))
            TitleImageWidth, TitleImageHeight = TitleCompanyImage1.width(), TitleCompanyImage1.height()
            TitleContentLabel0 = tk.Label(TitleFrame, image=TitleCompanyImage1,bg = controlsColor, width = TitleImageWidth, height = TitleImageHeight, bd = 0, highlightthickness = 0)
            TitleContentLabel0.grid(row = 0, column = 0, sticky = "ew", padx = 0, pady = 10)
            TitleContentLabel0.image = TitleCompanyImage1
        except:
            TitleCompanyLabel = tk.Label(TitleFrame, text="CDW", bg = backgroundColor, fg = "red", font=('aerial 48 bold'))
            TitleCompanyLabel.grid(row = 0, column = 0, sticky = "ew", padx = 15, pady = 10)

        TitleContentLabel1 = tk.Label(TitleFrame, text = "NDC Config Label Printing", bg = controlsColor, fg = specialColor, font = ('verdana 24 bold'))
        TitleContentLabel1.grid(row = 0, column = 1, sticky = "ew")

        # Controls for lefthand sidebar
        LeftControlBackBtn = tk.Button(LeftControlFrame, text = "Home", width = 15
                                    # ,command = lambda : self.screenSwap(HomePage)
                                    ,command = lambda:HomePage.tkraise() # temp command until genuine command is ready
                                    ,bg = controlsColor
                                    ,fg = specialColor
                                    ,relief = "flat")
        LeftControlBackBtn.grid(row = 0, column = 0, padx = 15, pady = 10)

        LeftControlHelpBtn = tk.Button(LeftControlFrame, text = "Help", width = 15
                                    ,command = lambda:helpPage.tkraise()
                                    ,bg = controlsColor
                                    ,fg = specialColor
                                    ,relief = "flat")
        LeftControlHelpBtn.grid(row = 10, column = 0, padx = 15, pady = (550,5))

        LeftControlHistoryBtn = tk.Button(LeftControlFrame, text = "Print History", width = 15
                                    ,command = lambda:historyPage.tkraise()
                                    ,bg = controlsColor
                                    ,fg = specialColor
                                    ,relief = "flat")
        LeftControlHistoryBtn.grid(row = 12, column = 0, padx = 15, pady = 5)

        LeftControlSettingsBtn = tk.Button(LeftControlFrame, text = "Settings", width = 15
                                    ,command = lambda:settingsPage.tkraise()
                                    ,bg = controlsColor
                                    ,fg = specialColor
                                    ,relief = "flat")
        LeftControlSettingsBtn.grid(row = 14, column = 0, padx = 15, pady = 5)

        VersionLabel = tk.Label(LeftControlFrame, textvariable=varappversion, bg = backgroundColor, fg = fontColor)
        VersionLabel.grid(row=15, column=0)

        # Home page
        barcodePageBtn = tk.Button(HomePage, command = lambda:BarcodesPage.tkraise(), text = "Barcodes")
        barcodePageBtn.grid(row = 0, column = 0)
        QRcodePageBtn = tk.Button(HomePage, command = lambda:QRcodePage.tkraise(), text = "QR Codes")
        QRcodePageBtn.grid(row = 0, column = 1)
        plainPageBtn = tk.Button(HomePage, command = lambda:plainPage.tkraise(), text = "Plain")
        plainPageBtn.grid(row = 1, column = 0)
        customerPageBtn = tk.Button(HomePage, command = lambda:customerPage.tkraise(), text = "Customer")
        customerPageBtn.grid(row = 1, column = 1)

        # Barcode page
        tk.Label(BarcodesPage, text="Barcoded Tags", bg=backgroundColor, fg=fontColor, font=fontHeaderH1).grid(row=0, columnspan=5, sticky="ew")


if __name__ == "__main__":
    app = printApp()
    app.mainloop()    
    