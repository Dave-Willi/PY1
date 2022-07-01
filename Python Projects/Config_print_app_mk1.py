import os
import re
import subprocess
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook

from PIL import Image, ImageTk

root = Tk()
root.title("Config printing app")
root.geometry=("780x520")

# ============ Variables ============

range_prefix = tk.StringVar(None, "")
range_suffix = tk.StringVar(None, "")
range_start = tk.StringVar(None)
range_end = tk.StringVar(None)
printer_select = tk.StringVar(None, "LPT1")
tag_select = tk.IntVar(value=0)
asset_type = tk.StringVar(None, "Asset Tag :")
cust_quantity = tk.IntVar(None)
auto_1 = tk.StringVar(None)
auto_2 = tk.StringVar(None)
auto_prefix1 = ""
auto_start = ""
auto_suffix1 = "" 
auto_prefix2 = ""
auto_end = ""
auto_suffix2 = ""
# ============ Frames ============

frametop = tk.Frame(root,
                    height=100,
                    width=780)
frametop.pack(side=TOP, fill=X, expand=False)

frametop1 = tk.Frame(frametop,
                    height=80,
                    width=100)
frametop1.pack(side=LEFT, anchor=W)

frametop2 = tk.Frame(frametop,
                    height=80,
                    width=680)
frametop2.pack(side=RIGHT)
frametop2.place(relx=0.25, y=15)

frame1 = tk.Frame(root,
                height=490,
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

logo_img = ImageTk.PhotoImage(Image.open("Images/2560px-CDW_Logo.svg.png").resize((100, 60)))
logo = Label(frametop1, image=logo_img)
logo.image = "Images/2560px-CDW_Logo.svg.png"
logo.pack(side=LEFT, anchor=W, padx=10, pady=10)
app_title = tk.Label(frametop2, text="Config General Printing Application", font=("Helvetica",25)).pack(side=TOP)

# ============ Tabs ============

tab1 = tk.Frame(frame2)
tab2 = tk.Frame(frame2)
tab2a = tk.Frame(tab2)
tab2b = tk.Frame(tab2)
tab3 = tk.Frame(frame2)
tab4 = tk.Frame(frame2)
tab4a = tk.Frame(tab4)
tab5 = tk.Frame(frame2)
tab6 = tk.Frame(frame2)
frame2.add(tab1, text = "Singles")
frame2.add(tab2, text = "Groups")
frame2.add(tab3, text = "Range")
frame2.add(tab4, text = "Range-Auto")
frame2.add(tab5, text = "Customer Labels")
frame2.add(tab6, text = "Reports")

tab2a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab2b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab4a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10, fill=BOTH)
# ============ Side menu commands ============

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
        if single_entry.get() != "":
            print("Device " + str(asset_type.get()))
            print(single_entry.get().upper())
            single_entry.delete(0, END)
            single_entry.focus()
            return
        else:
            print("Not a tag")
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

# ============ Command definitions ============

def clear_group_text():
    group_textbox.delete("1.0", END)

def print_group_text():
    result = len(group_textbox.get("1.0", END).split(","))
    print("This will print " + str(result) + " tags.")
    print(group_textbox.get("1.0", END))
    group_textbox.delete("1.0", END)

def clear_range():
    range_entry2.delete(0, END)
    range_entry3.delete(0, END)
    range_start.delete(0, END)
    range_end.delete(0, END)

def clear_auto():
    auto_entry1.delete(0, END)
    auto_entry2.delete(0, END)
    
def print_range():
    total_print = 1 + int(range_end.get()) - int(range_start.get())
    if total_print <= 0:
        messagebox.showerror("Error", "Please sure you have the start and end numbers the correct way around")
        return
    answer = messagebox.askyesno("Question","This will print " + str(total_print) + " labels.\nDo you wish to continue?")
    if answer == True:
        lead_zeros = len(range_end.get())
        print("proceed to print range")
        for x in range(int(range_start.get()), int(range_end.get())+1):
            print(str(range_prefix.get()).upper() + str(x).zfill(lead_zeros) + str(range_suffix.get()).upper())
    else:
        messagebox.showinfo("","Printing has been aborted")


# ============ Auto Range (Experimental)============

def print_auto():
    auto_range_split1 = re.split("(\d+)", auto_1.get())
    auto_range_split2 = re.split("(\d+)", auto_2.get())
    auto_prefix1 = auto_range_split1[0]
    auto_start = auto_range_split1[1]
    auto_suffix1 = auto_range_split1[2]
    auto_prefix2 = auto_range_split2[0]
    auto_end = auto_range_split2[1]
    auto_suffix2 = auto_range_split2[2]
    if auto_prefix1 != auto_prefix2:
        messagebox.showerror("Error", "Error detected in the prefix. Please check and try again")
        return
    elif auto_suffix1 != auto_suffix2:
        messagebox.showerror("Error", "Error detected in the suffix. Please check and try again")
        return
    else:
        total_print = 1 + int(auto_end) - int(auto_start)
        if total_print <= 0:
            messagebox.showerror("Error", "Please sure you have the start and end numbers the correct way around")
            return
        answer = messagebox.askyesno("Question","This will print " + str(total_print) + " labels.\nDo you wish to continue?")
        if answer == True:
            lead_zeros = len(auto_end)
            for x in range(int(auto_start), int(auto_end)+1):
                print(str(auto_prefix1).upper() + str(x).zfill(lead_zeros) + str(auto_suffix1.upper()))
        else:
            messagebox.showinfo("","Printing has been aborted")

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

group_label = tk.Label(master=tab2a,
                        textvariable=asset_type)
group_label.pack(side=LEFT)

group_entry = tk.Entry(master=tab2a,)
group_entry.pack(side=LEFT, padx=10)

group_clear = tk.Button(master=tab2b,
                        text="Clear",
                        command=clear_group_text)
group_clear.pack(side=LEFT)

group_print = tk.Button(master=tab2b,
                        text="Print",
                        command=print_group_text)
group_print.pack(side=LEFT, padx=100)

group_textbox = Text(master=tab2, wrap=WORD)
group_textbox.pack(side=BOTTOM, fill=BOTH, expand=True, padx=5, pady=5)

# ============ Range Tab (tab3) ============

range_label1 = tk.Label(master=tab3,
                        text="For printing a range of asset tags")
range_label1.pack()

range_label2 = tk.Label(master=tab3,
                        text="Enter the Prefix of the tag")
range_label2.pack()

range_entry2 = tk.Entry(master=tab3,
                        textvariable=range_prefix)
range_entry2.pack()

range_label3 = tk.Label(master=tab3,
                        text="Enter the Suffix of the tag")
range_label3.pack()

range_entry3 = tk.Entry(master=tab3,
                        textvariable=range_suffix)
range_entry3.pack()

range_label4 = tk.Label(master=tab3,
                        text="Enter the starting number of the range")
range_label4.pack()

range_entry4 = tk.Entry(master=tab3,
                        textvariable=range_start)
range_entry4.pack()

range_label5 = tk.Label(master=tab3,
                        text="Enter the ending number of the range")
range_label5.pack()

range_entry5 = tk.Entry(master=tab3,
                        textvariable=range_end)
range_entry5.pack()

range_clear = tk.Button(master=tab3,
                        text="Clear",
                        command=clear_range)
range_clear.pack(side=LEFT)

range_print = tk.Button(master=tab3,
                        text="Print",
                        command=print_range)
range_print.pack(side=LEFT, padx=100)

# ============ Range-Auto Tab (tab4) ============

auto_label1 = tk.Label(master=tab4a,
                        text="Scan the first tag in the range")
auto_label1.pack()

auto_entry1 = tk.Entry(master=tab4a,
                        textvariable=auto_1)
auto_entry1.pack()

auto_label2 = tk.Label(master=tab4a,
                        text="Scan the last tag in the range")
auto_label2.pack()

auto_entry2 = tk.Entry(master=tab4a,
                        textvariable=auto_2)
auto_entry2.pack()

auto_clear = tk.Button(master=tab4a,
                        text="Clear",
                        command=clear_auto)
auto_clear.pack(side=LEFT, padx=40)

auto_print = tk.Button(master=tab4a,
                        text="Print",
                        command=print_auto)
auto_print.pack(side=LEFT, padx=40)

warn_label = tk.Label(master=tab4a,
                        text="Experimental\nUse caution",
                        font=("Helvetica",18),
                        fg="red")
warn_label.pack(side=TOP, padx=40, pady=40)

# ============ Customer label Tab (tab5) ============

print_quantity_label = tk.Label(master=tab5,
                                text="Enter quantity of labels required")
print_quantity_label.pack()

print_quantity = tk.Spinbox(master=tab5, from_=0, to=9999,
                            textvariable=cust_quantity)
print_quantity.pack(padx=5, pady=5)

bbc_button = tk.Button(master=tab5,
                        text="BBC")
bbc_button.pack(padx=5, pady=5)

bbc_button = tk.Button(master=tab5,
                        text="UOB Mac QR Code")
bbc_button.pack(padx=5, pady=5)

bbc_button = tk.Button(master=tab5,
                        text="UOB PC QR Code")
bbc_button.pack(padx=5, pady=5)

# ============ Reports Tab (tab6) ============

tab6a = tk.Frame(master=tab6)
tab6a.pack(pady=20)
tab6b = tk.Frame(master=tab6)
tab6b.pack(pady=20)

label_6a = tk.Label(master=tab6a,
                    text="Less than 5 rolls of labels remaining?")
label_6a.grid(row=0, column=0)

labels_ribbon = tk.Checkbutton(master=tab6a, text="Also ribbons?")
labels_ribbon.grid(row=1, column=1)

labels_remain = tk.Spinbox(master=tab6a, from_=0, to=5, wrap=True)
labels_remain.grid(row=0, column=1)

labels_alert = tk.Button(master=tab6a,
                        text="Report labels")
labels_alert.grid(row=1, column=0)

label_6b = tk.Label(master=tab6b,
                    text="Faulty Network port:")
label_6b.grid(row=1, column=0)

label_6bb = tk.Label(master=tab6b,
                    text="enter switch number and full port number (i.e. SW5 Gi2/0/4)")
label_6bb.grid(row=0, column=0, columnspan=3)

port_entry = tk.Entry(master=tab6b)
port_entry.grid(row=1, column=2)

ports_alert = tk.Button(master=tab6b,
                        text="Report port")
ports_alert.grid(row=2, column=2)

# ============ Start up the routine ============

root.bind('<Return>', return_key)
root.mainloop()
