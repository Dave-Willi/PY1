from tkinter import *
import tkinter as tk
from tkinter.ttk import Notebook
import os
import sys
import subprocess

root = Tk()
root.title("Config printing app")
root.geometry=("780x520")

frametop = tk.Frame(root, height=520,width=780)
frame1 = tk.Frame(root, height=470, width=200, bg="black")
frame2 = Notebook (root, height=470, width=680)
frametop.pack(side=TOP)
frame1.pack(padx=10,pady=10,side=LEFT,fill=Y, expand=False)
frame2.pack(padx=10,pady=10,side=RIGHT)
frame1a = tk.Frame(frame1, height=60, pady=40, bg="blue").pack(side=TOP,fill=y, expand=True)
frame1b = tk.Frame(frame1, height=80, pady=60, bg="green").pack(side=TOP,fill=y, expand=True)
frame1c = tk.Frame(frame1, height=80, pady=60).pack(side=TOP,fill=y, expand=True)
frame1d = tk.Frame(frame1).pack(side=BOTTOM,fill=y, expand=True)

app_title = tk.Label(frametop, text="Config General Printing Application", font="Helvetica").pack(side=TOP)

tab1 = tk.Frame(frame2)
tab1a = tk.Frame(tab1)
tab2 = tk.Frame(frame2)
tab2a = tk.Frame(tab2)
tab2b = tk.Frame(tab2)
tab3 = tk.Frame(frame2)
tab4 = tk.Frame(frame2)
frame2.add(tab1, text = "Singles")
frame2.add(tab2, text = "Groups")
frame2.add(tab3, text = "Range")
frame2.add(tab4, text = "Range-Auto")

tab1a.pack(padx=20, pady=20)
tab2a.pack(padx=20, pady=20)
tab2b.pack(padx=20, pady=20)

printer_select = tk.StringVar(None, "LPT1")
tag_select = tk.IntVar(value=0)
asset_type = tk.StringVar(None, "Asset Tag :")

def reset():
    root.destroy()
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

def set_tag():
    global asset_type
    global tag_select
    if tag_select.get() == 0:
        asset_type.set("Asset Tag :")
        frame2.tab(2, state="normal")
        frame2.tab(3, state="normal")
    elif tag_select.get() == 1:
        asset_type.set("Serial Number :")
        frame2.tab(2, state="disabled")
        frame2.tab(3, state="disabled")

def return_key(event = None):
    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 0:
        print("Singles")
    if tab_index == 1:
        print("Groups")
        if group_textbox == Null:
            group_textbox.insert(end, group_entry)
        else:
            group_textbox.insert(end, ("," + group_entry))
    if tab_index == 2:
        print("Range")
    if tab_index == 3:
        print("Range-Auto")

printer_label = tk.Label(master=frame1b,
                            text="Select printer:").pack(padx=10, side=TOP)

check_print_button = tk.Radiobutton(master=frame1b,
                    text="Config Printer",
                    variable=printer_select,
                    value="LPT1", anchor="nw").pack(padx=10, side=TOP)

set_print_button = tk.Radiobutton(master=frame1b,
                    text="MEZZ Printer",
                    variable=printer_select,
                    value="LPT7", anchor="nw").pack(padx=10, side=TOP)

set_asset_button = tk.Radiobutton(master=frame1c,
                    text="Asset tags",
                    variable=tag_select,
                    value=0, anchor="nw",
                    command=set_tag).pack(padx=10, side=TOP)

set_serial_button = tk.Radiobutton(master=frame1c,
                    text="Serial Numbers",
                    variable=tag_select,
                    value=1, anchor="nw",
                    command=set_tag).pack(padx=10, side=TOP) 

reset_button = tk.Button(master=frame1d,
                    text="Reset",
                    command=reset).pack()

exit_button = tk.Button(master=frame1d,
                    text="Quit",
                    command=exit).pack()              

# ============ Single Tab ============

single_label = tk.Label(master=tab1a,
                            textvariable=asset_type).pack(side=LEFT)

single_entry = tk.Entry(master=tab1a).pack(side=LEFT)

# ============ Groups Tab ============

group_label = tk.Label(master=tab2a,
                            textvariable=asset_type).pack(side=LEFT)

group_entry = tk.Entry(master=tab2a).pack(side=LEFT)

group_textbox = tk.Text(master=tab2b).pack(side=BOTTOM)

# ============ Range Tab ============

# ============ Range-Auto Tab ============

root.bind('<Return>', return_key)
root.mainloop()
