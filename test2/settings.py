import tkinter as tk

# Colors
backgroundColor = "#FFFFFF"
controlsColor = "#000000"
fontColor = "#000000"
specialColor = "#FF0000"
activeBGcolor = "#00FF00"

# Variables
is_on = True
currentList = tk.StringVar(None, '')
currentTextList = tk.StringVar(None, '')
inputList = ["rangeInput1,rangeInput2"]
currentPage = tk.StringVar(None, '0')
qrTextSize = tk.StringVar(None, "30")
qrCodeSize = tk.StringVar(None, "4")
labelHomeVertical = tk.IntVar(None, "0")
labelHomeHorizontal = tk.IntVar(None, "0")
tagQty = tk.StringVar(None, "No tags")
tagQtytxt = tk.StringVar(None, "No tags")
varBarcodeSelection = tk.StringVar(None, "Asset")
varQRSideSelection = tk.StringVar(None, "right")
varTextSelection = tk.StringVar(None, "Small")