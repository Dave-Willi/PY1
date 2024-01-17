############################
# List of printApp.keep indexs #
############################
#
# [0] = QR preview image
# [1] = Text preview image
# [2] = Capslock Image

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
from tkinter import PhotoImage, messagebox, filedialog
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.scrolledtext as tkscrolled
from PIL import Image, ImageTk
import re
import docx2txt
import xlrd
import requests

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
        style = ttk.Style(self)
        appWidth = 1290 # App width in pixels
        appHeight = 860 # App height in pixels

        ### Font styles
        self.option_add("*Font", "aerial")
        fontHeaderH1 = tkFont.Font(size=28)
        fontLabelH1 = tkFont.Font(size=16, weight='normal')
        fontLabelSub = tkFont.Font(size=9, weight='normal')

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

        style.configure('IndicatorOff.TRadiobutton',
                        indicatorrelief=tk.FLAT,
                        indicatormargin=-1,
                        indicatordiameter=-1,
                        relief=tk.RAISED,
                        focusthickness=0, highlightthickness=0, padding=5)

        ####################
        # Create variables #
        ####################

        import settings     # Most settings kept here

        printApp.keep = []      # For long term storage of images so they aren't thrown out with garbage
        qrPreviewDefault = Image.open("Images/QRCodedLabelsPageImg.PNG")
        qrPreviewDefaultImg = qrPreviewDefault.resize((504,200))
        qrPreviewImg = ImageTk.PhotoImage(qrPreviewDefaultImg)
        printApp.keep.insert(0, qrPreviewImg) # Index 0 for this file to be easily replaced as image is updated
        textPreviewDefault = Image.open("Images/PlainTextLabelsPageImg.PNG")
        textPreviewDefaultImg = textPreviewDefault.resize((504,200))
        textPreviewImg = ImageTk.PhotoImage(textPreviewDefaultImg)
        printApp.keep.insert(1, textPreviewImg) # Index 1 for this file to be easily replaced as image is updated
        upperOnIMG = Image.open('Images/on.png')
        printApp.keep.append(upperOnIMG)
        upperOffIMG = Image.open('Images/off.png')
        printApp.keep.append(upperOffIMG)
        global upperSet
        upperSet = ImageTk.PhotoImage(upperOnIMG)
        upperSetOff = ImageTk.PhotoImage(upperOffIMG)
        printApp.keep.insert(2, upperSet) # Index 2 for this file to be easily replaced as image is updated
        printApp.keep.insert(3, upperSetOff)
        printApp.keep.append(upperOnIMG)
        printApp.keep.append(upperOffIMG)

        ##################
        # Custom Widgets #
        ##################

        class newButton(tk.Frame):
            def __init__(self, parent, newText, newCommand, width=15):
                tk.Frame.__init__(self, parent)
                self.label = tk.Button(self,
                                    text=newText,
                                    command=newCommand,
                                    bg=controlsColor,
                                    fg=specialColor,
                                    width=width,
                                    relief="flat")
                self.label.pack()

        class allCaps(tk.Frame):
            # create set and get!!!!!!!!!!!
            is_on = tk.BooleanVar(None, True)
            def __init__(self, parent, text):
                tk.Frame.__init__(self, parent)
                tk.Frame.configure(self, bg=backgroundColor)
                tk.Label(self, text="All Caps",bg=backgroundColor, fg=fontColor, font=("aerial 14 bold")).grid(row=0, column=0)
                self.upperCaseBtn = tk.Button(self, image=upperSet, bd=0, command=self.upperswitch, relief="flat")
                self.upperCaseBtn.grid(row=1, column=0)
                tk.Label(self, text=text,bg=backgroundColor, fg=fontColor, font=("aerial 8 bold")).grid(row=2, column=0)
            def upperswitch(self):
                if self.is_on:
                    self.upperCaseBtn.configure(image = upperSetOff)
                    self.is_on = False
                else:
                    self.upperCaseBtn.configure(image = upperSet)
                    self.is_on = True

        #################
        # Create Frames #
        #################

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

        ### List of frames
        # PrimaryContainer - Division between TitleBar and Main window content. Will hold only additional frames
        # TitleFrame - 3 column frame to split up the titlebar between the logo and title text with space for future addition in corner
        # PageFrame - Splits lower section, beneath titlebar, into 2 columns. Left one is intended for static left side controls which will be housed in another frame
        # LeftControlFrame - Frame for static controls on left of app. Lots of room for additions. Currently holds 4 navigation buttons and program version
        ### Further frames are switched between like pages | command = "lambda:PAGENAME.tkraise()"
        # HomePage - Opening page. Should default to this page on opening and when left idle. Offers navigation to label types for printing
        # BarcodesPage - Navigated to from HomePage | Offers options to print labels which are barcode based.
        # QRcodePage - Navigated to from HomePage | Offers options to print labels which are QR Code based.
        # plainPage - Navigated to from HomePage | Offers options to print labels which are plain text only.
        # customerPage - Navigated to from HomePage | Offers options to print labels which are customer specific. Many of these may require an additional page creating for them.
        # helpPage - Navigated to from Sidebar | Gives generalised or specific context help. Unsure of exact use as yet. May go with general as context help can be handled via 'tooltips'
        # historyPage - Navigated to from Sidebar | Shows labels that have previously been printed. Will be basic to begin with, may add additional information to the history with time, such as who printed it and when
        # settingsPage - Navigated to from Sidebar | Settings page, will include such things as printer selection positioning adjustment. Can be locked behind a password

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
        BarcodesPage.columnconfigure((0,1,2,3,4,5), weight=1)
        BarcodesPage.columnconfigure((4), weight=0)
        BarcodesPage.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        BarcodesPage.grid(row=0, column=1, sticky="nsew")

        QRcodePage = tk.Frame(PageFrame, bg=backgroundColor)
        QRcodePage.columnconfigure((0,1,2,3), weight=1)
        QRcodePage.columnconfigure(4, weight=2)
        QRcodePage.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14), weight=1)
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
        settingsPage.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22), weight=1)
        settingsPage.columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        settingsPage.grid(row=0, column=1, sticky="nsew")
        
        HomePage.tkraise() # Start with the HomePage

        ###################
        # Define commands #
        ###################

        ### Add caplock control commands and images

        # def upperswitch():
        #     def refreshUpperSwitch(): # Updates all caplock buttons in app
        #         upperCaseBarcodedBtn.updateImage()
        #         # upperCaseBarcodedBtn.upperCaseQRBtn.config(image = upperSet)
        #         # upperCaseQRBtn.upperCaseQRBtn.config(image = upperSet)
        #     # Determine is on or off
        #     if settings.is_on:
        #         global upperSet
        #         upperSet = ImageTk.PhotoImage(upperOffIMG)
        #         printApp.keep[2] = upperSet
        #         refreshUpperSwitch()
        #         # upperCaseBarcodedBtn.config(image = upperSet)
        #         settings.is_on = False
        #     else:
        #         upperSet = ImageTk.PhotoImage(upperOnIMG)
        #         printApp.keep[2] = upperSet
        #         refreshUpperSwitch()
        #         # upperCaseBarcodedBtn.config(image = upperSet)
        #         settings.is_on = True

        # upperOnIMG = Image.open('Images/on.png')
        # upperOffIMG = Image.open('Images/off.png')
        # upperSet = ImageTk.PhotoImage(upperOnIMG)
        # printApp.keep.insert(2, upperSet)
        # printApp.keep.append(upperOnIMG, upperOffIMG)
        # upperOn = ImageTk.PhotoImage(upperOnIMG)
        # printApp.keep.append(upperOn)
        # upperOff = ImageTk.PhotoImage(upperOffIMG)
        # printApp.keep.append(upperOff)

        ### Return key definitions - each element is individually bound and passes an identifier

        def ReturnKeyPress(event):
            if event == "singleBarcode":
                if len(addTagsBarcodeEntry.get()) == 0:
                    pass
                else:
                    addedTagsBarcodedList.insert(tk.END, addTagsBarcodeEntry.get()) # Add barcode
                    addedTagsBarcodedList.insert(tk.END, "\n")                      # Add line break
                    addTagsBarcodeEntry.delete(0, 'end')                            # Clear entrybox
                    updateLabels()
            elif event == "rangeBarcode1":
                addRangeBarcodeEntry2.focus_set()
            elif event == "rangeBarcode2":
                addRangeBarcodeEntry1.focus_set()
        
        ### Page selection command - to include primary element to have focus

        def pageSelect(selection):
            if selection == BarcodesPage:
                BarcodesPage.tkraise()
                addTagsBarcodeEntry.focus_set()
            elif selection == HomePage:
                HomePage.tkraise()
                clearAll()
            elif selection == QRcodePage:
                QRcodePage.tkraise()
                qrEntry1.focus_set()
            elif selection == settingsPage:
                settingsPage.tkraise()
            elif selection == helpPage:
                helpPage.tkraise()
            elif selection == historyPage:
                historyPage.tkraise()
            elif selection == plainPage:
                plainPage.tkraise()
            elif selection == customerPage:
                customerPage.tkraise()


        ### Barcode Range creation command
                
        def rangeToList(range1,range2): # To take 2 points of a range and create a list going from one to the other
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
                        newlist += prefixed + y + suffixed + "\n"
                    addToList(newlist)
                    addRangeBarcodeEntry1.delete(0, 'end')
                    addRangeBarcodeEntry2.delete(0, 'end')

            return
        
        def addToList(itemsForList): # To add labels to the currently active list
            settings.currentList.set(itemsForList)

        ### Tag number counter update command
            
        def updateLabels(*event): # Adds range to list and updates tag count
            addedTagsBarcodedList.insert(tk.END, settings.currentList.get())    # Add current range to list
            settings.currentList.set('')                            # clears stored list from variables
            counter = 0
            for x in (addedTagsBarcodedList.get('1.0', tk.END).split('\n')):    # split the list into lines
                if x:                                               # only count lines with something in them
                    counter += 1
            settings.tagQty.set("Number of tags: " + str(counter))

        ### Changes selection of barcode type

        def barcodeLabelSelection(choice):
            choice.config(fg=specialColor)
            for x in barcodeRadioButtons:
                if x != choice:
                    x.config(fg=fontColor)

        ### Various commands to clear various sections

        def clearBarcodesPage():
            barcodeLabelSelection(BarcodeAssetSelectionBtn)
            addedTagsBarcodedList.delete('1.0', tk.END)
            addTagsBarcodeEntry.delete(0, tk.END)
            addRangeBarcodeEntry1.delete(0, tk.END)
            addRangeBarcodeEntry2.delete(0, tk.END)
            updateLabels()

        def clearQRcodePage():
            qrEntry1.delete(0, 'end')
            qrEntry2.delete(0, 'end')
            qrDefaultPreview()

        def clearPlainTextPage():
            pass

        def clearAll():
            clearBarcodesPage()
            clearQRcodePage()
            clearPlainTextPage()

        ### File open dialog
            
        def fileOpener(location):
            pre_file_content = ""
            file_content = ""
            file_path = filedialog.askopenfilename(filetypes=[("Supported Files", ".xlsx .docx .csv .txt .pdf")])
            if file_path.endswith('.docx'):
                file_content = docx2txt.process(file_path)
            elif file_path.endswith('.doc'): ### still to do ###
                print("Document")
            elif file_path.endswith('.xlsx'):
                pre_file_content = xlrd.open_workbook(file_path)
                new_pre_file_content = pre_file_content.sheet_by_index(0)
                for rownum in range(new_pre_file_content.nrows):
                    for colnum in range(new_pre_file_content.ncols):
                        file_content += new_pre_file_content.cell_value(rownum, colnum)
                        file_content = file_content + '\n'
            elif file_path.endswith('.csv'):
                pre_file_content = open(file_path, "r")
                file_content = pre_file_content.read().replace(',','\n')
            elif file_path.endswith('.txt'):
                pre_file_content = open(file_path, "r")
                file_content = pre_file_content.read()
            elif file_path.endswith('.pdf'): ### still to do ###
                print("Acrobat file")
            else:
                print("text file?")
            if file_content == "":
                print("empty or cancelled")
            elif location == "barcode": # Add to relevant page
                file_content = file_content + '\n'
                addedTagsBarcodedList.insert(tk.END, file_content)
                updateLabels()
            elif location == "plainText":
                pass
            pre_file_content = ""
            file_content = ""

        ### QR Preview Image generator/refresh command
        def qrPreviewRefresh():
            if qrEntry1.get() == "" and qrEntry2.get() == "":
                qrDefaultPreview()
            else:
                zpl = genQRcodeZPL()
                url = 'http://api.labelary.com/v1/printers/8dpmm/labels/2.48x0.98/0/' # 8dpmm = dots per mm (Printer Specific) | 2.48x0.98 = Inch measurement of label (63mmx25mm)(Label Specific)
                files = {'file' : zpl}
                response = requests.post(url, files = files, stream = True)
                eatme = response.content
                qrPreviewImg = ImageTk.PhotoImage(data=eatme)
                qrPreviewImage.configure(image=qrPreviewImg)
                printApp.keep[0] = qrPreviewImg

        def qrDefaultPreview():
            qrPreviewDefault = Image.open("Images/QRCodedLabelsPageImg.PNG")
            qrPreviewDefaultImg = qrPreviewDefault.resize((504,200))
            qrPreviewImg = ImageTk.PhotoImage(qrPreviewDefaultImg)
            qrPreviewImage.configure(image=qrPreviewImg)
            printApp.keep[0] = qrPreviewImg

        ### Generate QR coded ZPL
        def genQRcodeZPL():
            zpl = "^XA"             # Start of label
            zpl += "^LH" + "0,0"    # Label home, set by settings
            zpl += "^CF" + "0," + settings.qrTextSize.get()   # Default text, set by amount of text entered approximating it to fit the label
            if settings.varQRSideSelection.get() == "right":
                zpl += "^FO" + "5,5"    # First text placement
                zpl += "^TB,304,190^FD" + qrEntry2.get() + "^FS" # Wrapped text from single line
                zpl += "^FO" + "309,0"
            else:
                zpl += "^FO" + "200,5"    # First text placement
                zpl += "^TB,304,190^FD" + qrEntry2.get() + "^FS" # Wrapped text from single line
                zpl += "^FO" + "5,0"
            zpl += "^BQ,," + settings.qrCodeSize.get()    # Set QR magnification
            zpl += "^FD" + qrEntry1.get() + "^FS" # QR code input
            zpl += "^XZ"            # End of label
            return(zpl)
            
        def moveLabelHomeX():
            labelSettingCanvas.moveto(objectxline1, x=labelSettingHorizontalSlider.get()*3, y=labelSettingVerticalSlider.get()*2)
            labelSettingCanvas.moveto(objectxline2, x=labelSettingHorizontalSlider.get()*3, y=labelSettingVerticalSlider.get()*2)
        ### File open handler

        # def WordFileOpenHandler(filing):
        #     returnFile = docx2txt.process(filing)
        #     return(returnFile)

        self.bind('<Escape>', lambda x: pageSelect(HomePage)) # Press escape to return to homepage

        #########################
        # Add content to frames #
        #########################

        # Image and text for titlebar
        try:
            TitleCompanyImage0 = Image.open('Images\CDW.PNG')
            TitleCompanyImage1 = ImageTk.PhotoImage(TitleCompanyImage0.resize((144,80)))
            TitleImageWidth, TitleImageHeight = TitleCompanyImage1.width(), TitleCompanyImage1.height()
            TitleContentLabel0 = tk.Label(TitleFrame, image=TitleCompanyImage1,bg = controlsColor, width = TitleImageWidth, height = TitleImageHeight, bd = 0, highlightthickness = 0)
            TitleContentLabel0.grid(row = 0, column = 0, sticky = "ew", padx = 0, pady = 10)
            TitleContentLabel0.image = TitleCompanyImage1
            printApp.keep.append(TitleCompanyImage1)
        except:
            TitleCompanyLabel = tk.Label(TitleFrame, text="CDW", bg = backgroundColor, fg = "red", font=('aerial 48 bold'))
            TitleCompanyLabel.grid(row = 0, column = 0, sticky = "ew", padx = (0,TitleImageWidth), pady = 10)

        TitleContentLabel1 = tk.Label(TitleFrame, text = "NDC Config Label Printing", bg = controlsColor, fg = specialColor, font = ('verdana 24 bold'))
        TitleContentLabel1.grid(row = 0, column = 1, sticky = "ew")

        # Controls for lefthand sidebar
        LeftControlBackBtn = newButton(LeftControlFrame,
                                       "Home",
                                       lambda:pageSelect(HomePage))
        LeftControlBackBtn.grid(row = 0, column = 0, padx = 15, pady = 10)

        LeftControlHelpBtn = newButton(LeftControlFrame, 
                                       "Help",
                                       lambda:pageSelect(helpPage))
        LeftControlHelpBtn.grid(row = 10, column = 0, padx = 15, pady = (550,5))

        LeftControlHistoryBtn = newButton(LeftControlFrame, 
                                          "Print History", 
                                          lambda:pageSelect(historyPage))
        LeftControlHistoryBtn.grid(row = 12, column = 0, padx = 15, pady = 5)

        LeftControlSettingsBtn = newButton(LeftControlFrame,
                                           "Settings",
                                           lambda:pageSelect(settingsPage))
        LeftControlSettingsBtn.grid(row = 14, column = 0, padx = 15, pady = 5)

        VersionLabel = tk.Label(LeftControlFrame, textvariable=varappversion, bg = backgroundColor, fg = fontColor)
        VersionLabel.grid(row=15, column=0)

        ### Home page ###

        # Images
        BarcodedLabelsPageImg = PhotoImage(file = "Images/BarcodedLabelsPageImg.PNG")
        BarcodedLabelsPageImg.image = BarcodedLabelsPageImg
        printApp.keep.append(BarcodedLabelsPageImg)
        QRCodedLabelsPageImg = PhotoImage(file = "Images/QRCodedLabelsPageImg.PNG")
        QRCodedLabelsPageImg.image = QRCodedLabelsPageImg
        printApp.keep.append(QRCodedLabelsPageImg)
        PlainTextLabelsPageImg = PhotoImage(file = "Images/PlainTextLabelsPageImg.PNG")
        PlainTextLabelsPageImg.image = PlainTextLabelsPageImg
        printApp.keep.append(PlainTextLabelsPageImg)
        customerLabelsPageImg = PhotoImage(file = "Images/PlainTextLabelsPageImg.PNG")
        customerLabelsPageImg.image = customerLabelsPageImg
        printApp.keep.append(customerLabelsPageImg)
        
        
        # Buttons
        barcodePageBtn = tk.Button(HomePage, 
                                   command = lambda:pageSelect(BarcodesPage), 
                                   text = "Barcoded Labels ", 
                                   image = BarcodedLabelsPageImg, 
                                   compound="top", 
                                   bg=backgroundColor, 
                                   fg=fontColor,
                                   relief="flat", 
                                   activebackground=controlsColor, 
                                   activeforeground=specialColor,
                                   font=fontLabelH1)
        barcodePageBtn.grid(row = 1, column = 1)

        QRcodePageBtn = tk.Button(HomePage, 
                                  command = lambda:pageSelect(QRcodePage), 
                                  text = "QR coded Labels ", 
                                  image = QRCodedLabelsPageImg, 
                                  compound="top", 
                                  bg=backgroundColor, 
                                  fg=fontColor,
                                  relief="flat", 
                                  activebackground=controlsColor, 
                                  activeforeground=specialColor,
                                  font=fontLabelH1)
        QRcodePageBtn.grid(row = 1, column = 2)

        plainPageBtn = tk.Button(HomePage, 
                                 command = lambda:plainPage.tkraise(), 
                                 text = "Plain Text Labels ", 
                                 image = PlainTextLabelsPageImg, 
                                 compound="top", 
                                 bg=backgroundColor, 
                                 fg=fontColor,
                                 relief="flat", 
                                 activebackground=controlsColor, 
                                 activeforeground=specialColor,
                                 font=fontLabelH1)
        plainPageBtn.grid(row = 2, column = 1)

        customerPageBtn = tk.Button(HomePage, 
                                    command = lambda:customerPage.tkraise(), 
                                    text = "Customer Labels ", 
                                    image = customerLabelsPageImg, 
                                    compound="top", 
                                    bg=backgroundColor, 
                                    fg=fontColor,
                                    relief="flat", 
                                    activebackground=controlsColor, 
                                    activeforeground=specialColor,
                                    font=fontLabelH1)
        customerPageBtn.grid(row = 2, column = 2)

        # Labels

        tk.Label(HomePage,
                                       text = "Select your label type",
                                       font = fontHeaderH1,
                                       bg = backgroundColor, 
                                       fg = fontColor).grid(row=0, 
                                                               columnspan=8,
                                                               sticky="ew")

        ### Barcode page ###

        # Images
        BarcodedLabelsPageImg_serial = PhotoImage(file = "Images/BarcodedLabelsPageImg_serial.PNG")
        BarcodedLabelsPageImg_serial.image = BarcodedLabelsPageImg_serial
        printApp.keep.append(BarcodedLabelsPageImg_serial)
        BarcodedLabelsPageImg_mac = PhotoImage(file = "Images/BarcodedLabelsPageImg_mac.PNG")
        BarcodedLabelsPageImg_mac.image = BarcodedLabelsPageImg_mac
        printApp.keep.append(BarcodedLabelsPageImg_mac)
        
        # Labels
        tk.Label(BarcodesPage,
                 text="Barcoded Labels",
                 bg=backgroundColor,
                 fg=fontColor,
                 font=fontHeaderH1).grid(row=0, 
                                         columnspan=6, 
                                         sticky="ew")
        
        tk.Label(BarcodesPage,
                 text="Add range to tags",
                 bg=backgroundColor,
                 fg=fontColor).grid(row=1, column=5)
        
        tk.Label(BarcodesPage,
                 textvariable=settings.tagQty,
                 bg=backgroundColor,
                 fg=specialColor).grid(row=7, column=0)


        # RadioButtons
        BarcodeAssetSelectionBtn = tk.Radiobutton(BarcodesPage,
                    image=BarcodedLabelsPageImg, 
                    text="Asset Tag", 
                    compound="top", 
                    bg=backgroundColor,
                    fg=fontColor,
                    relief="flat", 
                    activebackground=controlsColor, 
                    activeforeground=specialColor,
                    font=fontLabelH1,
                    variable=settings.varBarcodeSelection,
                    indicatoron=False,
                    selectcolor=controlsColor,
                    bd=0,
                    offrelief="flat",
                    value="Asset Tag")
        BarcodeAssetSelectionBtn.config(command = lambda arg=BarcodeAssetSelectionBtn: barcodeLabelSelection(arg))
        BarcodeAssetSelectionBtn.grid(row=2, column=2, rowspan=2, columnspan=2)
        
        BarcodeSerialSelectionBtn = tk.Radiobutton(BarcodesPage,
                    image=BarcodedLabelsPageImg_serial, 
                    text="Serial Number",
                    compound="top", 
                    bg=backgroundColor, 
                    fg=fontColor,
                    relief="flat", 
                    activebackground=controlsColor, 
                    activeforeground=specialColor,
                    font=fontLabelH1,
                    variable=settings.varBarcodeSelection,
                    indicatoron=False,
                    selectcolor=controlsColor,
                    bd=0,
                    offrelief="flat",
                    value="Serial Number")
        BarcodeSerialSelectionBtn.config(command = lambda arg=BarcodeSerialSelectionBtn: barcodeLabelSelection(arg))
        BarcodeSerialSelectionBtn.grid(row=4, column=2, rowspan=2, columnspan=2)
        
        BarcodMACSelectionBtn = tk.Radiobutton(BarcodesPage,
                    image=BarcodedLabelsPageImg_mac, 
                    text="MAC Address",
                    compound="top", 
                    bg=backgroundColor, 
                    fg=fontColor,
                    relief="flat", 
                    activebackground=controlsColor, 
                    activeforeground=specialColor,
                    font=fontLabelH1,
                    variable=settings.varBarcodeSelection,
                    indicatoron=False,
                    selectcolor=controlsColor,
                    bd=0,
                    offrelief="flat",
                    value="MAC Address")
        BarcodMACSelectionBtn.config(command = lambda arg=BarcodMACSelectionBtn: barcodeLabelSelection(arg))
        BarcodMACSelectionBtn.grid(row=6, column=2, rowspan=2, columnspan=2)

        # List of radioButtons
        barcodeRadioButtons = [BarcodeAssetSelectionBtn,BarcodeSerialSelectionBtn,BarcodMACSelectionBtn]
        barcodeLabelSelection(BarcodeAssetSelectionBtn) # Set default button

        # Buttons
        # printBarcodedBtn = tk.Button(BarcodesPage,
        #             text="Add to Queue",
        #             bg=controlsColor, 
        #             fg=fontColor,
        #             relief="flat", 
        #             activebackground=controlsColor, 
        #             activeforeground=specialColor,
        #             font=fontLabelH1,
        #             # command=lambda: print(varBarcodeSelection.get()),
        #             width=15)
        # printBarcodedBtn.grid(row=9, column=2, columnspan=2)

        printBarcodedBtn = tk.Button(BarcodesPage,
                    text="Print Now",
                    bg=controlsColor, 
                    fg=fontColor,
                    relief="flat", 
                    activebackground=controlsColor, 
                    activeforeground=specialColor,
                    font=fontLabelH1,
                    # command=lambda: print(varBarcodeSelection.get()),
                    width=15)
        printBarcodedBtn.grid(row=8, column=2)

        clearBarcodedBtn = tk.Button(BarcodesPage,
                    text="Clear",
                    bg=controlsColor, 
                    fg=fontColor,
                    relief="flat", 
                    activebackground=controlsColor, 
                    activeforeground=specialColor,
                    font=fontLabelH1,
                    command= lambda: clearBarcodesPage(),
                    width=15)
        clearBarcodedBtn.grid(row=8, column=3)

        addFileBarcodedBtn = tk.Button(BarcodesPage,
                    text="Add from file",
                    bg=controlsColor, 
                    fg=fontColor,
                    relief="flat", 
                    activebackground=controlsColor, 
                    activeforeground=specialColor,
                    font=fontLabelH1,
                    command=lambda: fileOpener("barcode"),
                    width=15)
        addFileBarcodedBtn.grid(row=1, column=3)

        addRangeBarcodedBtn = tk.Button(BarcodesPage,
                    text="Add range",
                    bg=controlsColor, 
                    fg=fontColor,
                    relief="flat", 
                    activebackground=controlsColor, 
                    activeforeground=specialColor,
                    font=fontLabelH1,
                    width=15,
                    command = lambda: [rangeToList(addRangeBarcodeEntry1.get(),addRangeBarcodeEntry2.get()),updateLabels()])
        addRangeBarcodedBtn.grid(row=4, column=5)


        #Seperator
        ttk.Separator(BarcodesPage, orient="vertical").grid(row=1, column=4, rowspan=7, sticky="ns")

        # Entry boxes
        addTagsBarcodeEntry = tk.Entry(BarcodesPage)
        addTagsBarcodeEntry.grid(row=1, column=2)
        addTagsBarcodeEntry.bind('<Return>', lambda x: ReturnKeyPress("singleBarcode"))

        addRangeBarcodeEntry1 = tk.Entry(BarcodesPage)
        addRangeBarcodeEntry1.grid(row=2, column=5)
        addRangeBarcodeEntry1.bind('<Return>', lambda x: ReturnKeyPress("rangeBarcode1"))

        addRangeBarcodeEntry2 = tk.Entry(BarcodesPage)
        addRangeBarcodeEntry2.grid(row=3, column=5)
        addRangeBarcodeEntry2.bind('<Return>', lambda x: ReturnKeyPress("rangeBarcode2"))

        # List box
        addedTagsBarcodedList = tkscrolled.ScrolledText(BarcodesPage, width=20)
        addedTagsBarcodedList.grid(row=1, column=0, rowspan=6, padx=(30,0), pady=(30,0), sticky="nsew")
        addedTagsBarcodedList.bind('<Key>', updateLabels)

        # Capslock control
        upperCaseBarcodedBtn = allCaps(BarcodesPage, "All caps with show when\nlabels are printed.\nOnly affects BARCODES")
        upperCaseBarcodedBtn.grid(row=9, column=0)

        ### QR Code Page ###
        
        # Radio Button
        qrLeftSelect = tk.Radiobutton(QRcodePage,
                                      text="Left",
                                      bg=backgroundColor,
                                      fg="white",
                                      variable=settings.varQRSideSelection,
                                      activebackground=backgroundColor,
                                      activeforeground=specialColor,
                                      selectcolor="#000000",
                                      value="left",
                                      command=lambda:qrPreviewRefresh()
                                      )
        qrLeftSelect.grid(row=0, column=2)
        qrRightSelect = tk.Radiobutton(QRcodePage,
                                       text="Right",
                                       bg=backgroundColor,
                                       fg="white",
                                       variable=settings.varQRSideSelection,
                                       activebackground=backgroundColor,
                                       activeforeground=specialColor,
                                       selectcolor="#000000",
                                       value="right",
                                       command=lambda:qrPreviewRefresh()
                                       )
        qrRightSelect.grid(row=0, column=3)

        # Labels
        tk.Label(QRcodePage, text = "Select QR position", bg=backgroundColor, fg=fontColor).grid(row=0, column=1, sticky='e')
        tk.Label(QRcodePage, text = "QR encoded data", bg=backgroundColor, fg=specialColor).grid(row=1, column=1, sticky='w')
        tk.Label(QRcodePage, text = "Plain Text", bg=backgroundColor, fg=specialColor).grid(row=4, column=1, sticky='w')
        tk.Label(QRcodePage, text = "Text Size", bg=backgroundColor, fg=fontColor).grid(row=4, column=2, sticky='e')
        tk.Label(QRcodePage, text = "QR Code Size", bg=backgroundColor, fg=fontColor).grid(row=1, column=2, sticky='e')

        # Text Entry
        qrEntry1 = tk.Entry(QRcodePage, width=90)
        qrEntry1.grid(row=2, column=0, columnspan=6)

        qrEntry2 = tk.Entry(QRcodePage, width=90)
        qrEntry2.grid(row=5, column=0, columnspan=6)

        # Capslock control

        upperCaseQRBtn = allCaps(QRcodePage, "All caps with show when\nlabels are printed.\nDoes NOT affect QR code")
        upperCaseQRBtn.grid(row=13, column=0)

        # tk.Label(QRcodePage, text="All Caps",bg=backgroundColor, fg=fontColor, font=("aerial 14 bold")).grid(row=12, column=0)
        # upperCaseQRBtn = tk.Button(QRcodePage, image=upperSet, bd=0, command=upperswitch, relief="flat")
        # upperCaseQRBtn.grid(row=13, column=0)
        # tk.Label(QRcodePage, text="All caps with show when\nlabels are printed.\nDoes NOT affect QR code",bg=backgroundColor, fg=fontColor, font=("aerial 8 bold")).grid(row=14, column=0)

        # Buttons
        qrPreviewRefreshBtn = tk.Button(QRcodePage,
                                     text="Refresh Preview",
                                     bg=controlsColor,
                                     fg=fontColor,
                                     relief="flat", 
                                     activebackground=controlsColor, 
                                     activeforeground=specialColor,
                                     font=fontLabelH1,
                                     command= lambda:qrPreviewRefresh(),
                                     width=15)
        qrPreviewRefreshBtn.grid(row=11, column=1)

        qrPrintLabelBtn = tk.Button(QRcodePage,
                                     text="Print",
                                     bg=controlsColor,
                                     fg=fontColor,
                                     relief="flat", 
                                     activebackground=controlsColor, 
                                     activeforeground=specialColor,
                                     font=fontLabelH1,
                                     width=15)
        qrPrintLabelBtn.grid(row=12, column=2)

        qrClearBtn = tk.Button(QRcodePage,
                                     text="Clear",
                                     bg=controlsColor,
                                     fg=fontColor,
                                     relief="flat", 
                                     activebackground=controlsColor, 
                                     activeforeground=specialColor,
                                     font=fontLabelH1,
                                     command = lambda: clearQRcodePage(),
                                     width=15)
        qrClearBtn.grid(row=12, column=3)

        # Image - Preview image generated using Labelary API
        qrPreviewImage = tk.Label(QRcodePage, text="Imagery", image=qrPreviewImg)
        qrPreviewImage.grid(row=10, column=2, columnspan=3, rowspan=2)
        printApp.keep.append(qrPreviewImg)

        # Tickers
        qrTextSizeTicker = ttk.Spinbox(QRcodePage, textvariable=settings.qrTextSize, from_=10, to=80, width=5)
        qrTextSizeTicker.grid(row=4, column=3, sticky='w', padx=(10,0))

        qrCodeSizeTicker = ttk.Spinbox(QRcodePage, textvariable=settings.qrCodeSize, from_=1, to=10, width=5)
        qrCodeSizeTicker.grid(row=1, column=3, sticky='w', padx=(10,0))

        ### Settings Page ###
        
        # Labels
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, text="Created for use within the configuration department within the NDC of CDW UK Ltd.").grid(row=20, column=1, columnspan=3)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, text="Program: ©Dave Williams 2024").grid(row=21, column=1, columnspan=3)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, text="CDW logo: ©CDW UK Ltd.").grid(row=22, column=1, columnspan=3)

        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, text="Label Position Adjustment").grid(row=3, column=1, columnspan=2)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, font=fontLabelSub, text="Not to scale").grid(row=4, column=1, columnspan=2)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, font=fontLabelSub, text="N.B. Position Adjustment will not affect some customer labels").grid(row=11, column=1, columnspan=2)

        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, text="Select Printers").grid(row=3, column=7, columnspan=2)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, font=fontLabelSub, text="Default Printer:").grid(row=4, column=7, columnspan=2)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, font=fontLabelSub, text="Barcodes Printer:").grid(row=5, column=7, columnspan=2)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, font=fontLabelSub, text="QR Printer:").grid(row=6, column=7, columnspan=2)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, font=fontLabelSub, text="Barcodes Alt Printer:").grid(row=7, column=7, columnspan=2)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, font=fontLabelSub, text="Text Printer (Small):").grid(row=8, column=7, columnspan=2)
        tk.Label(settingsPage, bg=backgroundColor, fg=fontColor, font=fontLabelSub, text="Text Printer (Large):").grid(row=9, column=7, columnspan=2)

        # Sliders
        labelSettingVerticalSlider = tk.Scale(settingsPage, 
                                              from_=0, 
                                              to=25, 
                                              bg=backgroundColor, 
                                              fg=fontColor,
                                              troughcolor=controlsColor,
                                              bd=0,
                                              activebackground=fontColor,
                                              highlightbackground=backgroundColor,
                                              highlightcolor=specialColor,
                                              command=lambda x:moveLabelHomeX(),
                                              variable=settings.labelHomeVertical)
        labelSettingVerticalSlider.grid(row=5, column=3, sticky='nsw', rowspan=3)
        labelSettingHorizontalSlider = tk.Scale(settingsPage, 
                                                from_=0, 
                                                to=25, 
                                                orient="horizontal", 
                                                bg=backgroundColor, 
                                                fg=fontColor,
                                                troughcolor=controlsColor,
                                                bd=0,
                                                activebackground=fontColor,
                                                highlightbackground=backgroundColor,
                                                highlightcolor=specialColor,
                                                command=lambda x:moveLabelHomeX(),
                                                variable=settings.labelHomeHorizontal)
        labelSettingHorizontalSlider.grid(row=8, column=1, columnspan=2, sticky='new')

        # Canvas
        labelSettingCanvasHeight = 150
        labelSettingCanvasWidth = 400
        labelSettingCanvas = tk.Canvas(settingsPage,
                                       height=labelSettingCanvasHeight,
                                       width=labelSettingCanvasWidth,
                                       bd=0, 
                                       highlightthickness=0, 
                                       relief='ridge')
        labelSettingCanvas.grid(row=5, column=1, rowspan=3, columnspan=2)

        labelSettingCanvas.create_rectangle(5,5,395,145, outline="#ff0000")
        labelSettingCanvas.create_polygon(6,0,0,6,6,6, outline="#0000ff", fill="#0000ff")
        labelSettingCanvas.create_polygon(394,0,400,6,394,6, outline="#0000ff", fill="#0000ff")
        labelSettingCanvas.create_polygon(0,144,6,144,6,150, outline="#0000ff", fill="#0000ff")
        labelSettingCanvas.create_polygon(394,144,400,144,394,150, outline="#0000ff", fill="#0000ff")
        
        positionx = 0
        positiony = 0
        objectxline1 = labelSettingCanvas.create_line(positionx,positiony,positionx+9,positiony+9)
        objectxline2 = labelSettingCanvas.create_line(positionx,positiony+9,positionx+9,positiony)

if __name__ == "__main__":
    root = printApp()
    root.mainloop()
    