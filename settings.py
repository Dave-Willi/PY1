import tkinter as tk

# Colors
backgroundColor = "#001F3F" # A dark blue                           #001F3F
controlsColor = "#083358"   # A less dark blue                      #083358
fontColor = "#9DB2BF"       # A light gray with a tint of blue      #9DB2BF
specialColor = "#FFD717"    # Bright yellow                         #FFD717
activeBGcolor = "#255075"
brightRedColor = "#FF0000"

# Fonts
fontType2 = ("Arial", 16, "bold")

# Variables
is_on = True
currentList = tk.StringVar(None,'')
currentTextList = tk.StringVar(None,'')
inputList = ["rangeInput1,rangeInput2"]
currentPage = tk.StringVar(None,'0')
qrTextSize = tk.StringVar(None, "30")
qrCodeSize = tk.StringVar(None, "4")
labelHomeVertical = tk.IntVar(None, "5")
labelHomeHorizontal = tk.IntVar(None, "5")
tagQty = tk.StringVar(None,"No tags")
tagQtytxt = tk.StringVar(None,"No tags")
varBarcodeSelection = tk.StringVar(None,"Device Asset Tag")
varQRSideSelection = tk.StringVar(None, "right")
varTextSelection = tk.StringVar(None, "Small")