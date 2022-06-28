from tkinter import *
import tkinter as tk
from tkinter.ttk import Notebook
import os
import sys
import subprocess

root = Tk()
root.title("Config printing app")
root.geometry=("780x520")

# ============ Frames ============

frametop = tk.Frame(root,
                    height=520,
                    width=780)
frametop.pack(side=TOP)
frame1 = tk.Frame(root,
                    height=470,
                    width=200)
frame1.pack(padx=10, pady=10, anchor=W, fill=Y, expand=False, side=LEFT)
frame2 = Notebook (root, 
                    height=470,
                    width=680,)
frame2.pack(padx=10,pady=10, anchor=E, fill=BOTH, expand=True, side=RIGHT)
frame1.grid_rowconfigure((0,1,2,4,5,6,8,9), weight=1)
frame1.grid_rowconfigure((3,7), weight=8)
frame1.grid_columnconfigure(0, weight=1)

# ============ Title piece ============

app_title = tk.Label(frametop, text="Config General Printing Application", font=("Helvetica",25)).pack(side=TOP)

# ============ Tabs ============

tab1 = tk.Frame(frame2)
tab2 = tk.Frame(frame2)
tab3 = tk.Frame(frame2)
tab4 = tk.Frame(frame2)
frame2.add(tab1, text = "Singles")
frame2.add(tab2, text = "Groups")
frame2.add(tab3, text = "Range")
frame2.add(tab4, text = "Range-Auto")

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

# ============ What to do when the enter key is pressed ============

def return_key(event = None):
    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 0:
        print(single_entry.get().upper())
        single_entry.delete(0, END)
        single_entry.focus()
        return
    if tab_index == 1:
        if group_entry.get() == "":
            return
        if len(group_textbox.get("1.0",END)) == 1:
            group_textbox.insert("end", group_entry.get().upper())
            group_entry.delete(0, END)
            group_entry.focus()
        else:
            group_textbox.insert("end", (", " + group_entry.get().upper()))
            group_entry.delete(0, END)
            group_entry.focus()
    if tab_index == 2:
        print("Range")
    if tab_index == 3:
        print("Range-Auto")

def clear_group_text():
    group_textbox.delete("1.0", END)

# ============ Settings panel (frame1a) ============

printer_label = tk.Label(master=frame1,
                            text="Select printer:")
printer_label.grid(row=0, sticky=EW)

check_print_button = tk.Radiobutton(master=frame1,
                    text="Config Printer",
                    variable=printer_select,
                    value="LPT1")
check_print_button.grid(row=1, sticky=W)

set_print_button = tk.Radiobutton(master=frame1,
                    text="MEZZ Printer",
                    variable=printer_select,
                    value="LPT7")
set_print_button.grid(row=2, sticky=W)

asset_label = tk.Label(master=frame1,
                            text="Asset or serial?")
asset_label.grid(row=4, sticky=EW)

set_asset_button = tk.Radiobutton(master=frame1,
                    text="Asset tags",
                    variable=tag_select,
                    value=0,
                    command=set_tag)
set_asset_button.grid(row=5, sticky=W)

set_serial_button = tk.Radiobutton(master=frame1,
                    text="Serial Numbers",
                    variable=tag_select,
                    value=1,
                    command=set_tag)
set_serial_button.grid(row=6, sticky=W)

reset_button = tk.Button(master=frame1,
                    text="Restart App",
                    command=reset)
reset_button.grid(row=8, sticky=EW)

exit_button = tk.Button(master=frame1,
                    text="Quit",
                    command=exit)
exit_button.grid(row=9, sticky=EW)

# ============ Single Tab (tab1) ============

tab1.grid_columnconfigure((0,1,2,3),weight=1)
tab1.grid_rowconfigure((0,1,2,3),weight=1)

single_label = tk.Label(master=tab1,
                        textvariable=asset_type)
single_label.grid(row=0, column=1, sticky=E)

single_entry = tk.Entry(master=tab1)
single_entry.grid(row=0, column=2, sticky=W)

single_descript = tk.Label(master=tab1,
                        text="This will print a single label")
single_descript.grid(row=1, column=1, columnspan=2, sticky=N)

# ============ Groups Tab (tab2) ============

group_label = tk.Label(master=tab2,
                        textvariable=asset_type)
group_label.grid(row=0, column=1)

group_entry = tk.Entry(master=tab2)
group_entry.grid(row=0, column=2)

group_clear = tk.Button(master=tab2,
                        text="Clear",
                        command=clear_group_text)
group_clear.grid(row=1, columnspan=4)

group_textbox = Text(master=tab2, wrap=WORD)
group_textbox.grid(row=2, columnspan=4, rowspan=2, sticky=NSEW)

# ============ Range Tab (tab3) ============

# ============ Range-Auto Tab (tab4) ============

# ============ Start up the routine ============

root.bind('<Return>', return_key)
root.mainloop()
