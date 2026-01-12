import tkinter as tk

# ============ Global Variables ============

range_prefix = tk.StringVar(None, "")
range_suffix = tk.StringVar(None, "")
range_start = tk.StringVar(None, "0")
range_end = tk.StringVar(None, "0")
printer_select = tk.StringVar(None, "LPT1")
local_print = tk.StringVar(None, "127.0.0.1")
tag_select = tk.IntVar(value=0)
asset_type = tk.StringVar(None, "Asset Tag :")
cust_quantity = tk.IntVar(None, "1")
auto_1 = tk.StringVar(None)
auto_2 = tk.StringVar(None)
bg_col = str("white")
xyz = str(" ")
flag_1 = int(0)
flag_2 = str("0")
range_image = ""
qr_pos = 325 # default QR code position on the X axis
qr_mag = 2 # default QR magnification. range is 1-10
pCounter = 0
x_col = 0
y_row = 0

# ============ Printer Initial Selection ============

host = str(printer_select.get())
port = 9100