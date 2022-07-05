import fileinput
import os
import re
import subprocess
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter
from tkinter.ttk import Notebook
import socket
from PIL import Image, ImageTk
from time import sleep

root = Tk()
root.title("Config printing app")
root.geometry=("780x520")

# ============ Variables ============

range_prefix = tk.StringVar(None, "")
range_suffix = tk.StringVar(None, "")
range_start = tk.StringVar(None, "0")
range_end = tk.StringVar(None, "0")
printer_select = tk.StringVar(None, "LPT1")
tag_select = tk.IntVar(value=0)
asset_type = tk.StringVar(None, "Asset Tag :")
cust_quantity = tk.IntVar(None)
auto_1 = tk.StringVar(None)
auto_2 = tk.StringVar(None)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception: 
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ============ Printer Initial Setup ============

mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = str(printer_select.get())
port = 9100

# ============ Frames ============

frametop = tk.Frame(root,
                    height=100,
                    width=780)
frametop.pack(side=TOP, fill=X, expand=False)

frametop1 = tk.Frame(frametop,
                    height=80,
                    width=100)
frametop1.pack(side=LEFT, anchor=W)

frametop3 = tk.Frame(frametop,
                    height=80,
                    width=680)
frametop3.pack(side=RIGHT)

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

# ============ Tabs ============

tab1 = tk.Frame(frame2)
tab2 = tk.Frame(frame2)
tab2a = tk.Frame(tab2)
tab2b = tk.Frame(tab2)
tab3 = tk.Frame(frame2)
tab3a = tk.Frame(tab3)
tab4 = tk.Frame(frame2)
tab4a = tk.Frame(tab4)
tab4b = tk.Frame(tab4)
tab4c = tk.Frame(tab4)
tab5 = tk.Frame(frame2)
tab6 = tk.Frame(frame2)
frame2.add(tab1, text = "Singles")
frame2.add(tab2, text = "Groups")
frame2.add(tab3, text = "Range")
frame2.add(tab4, text = "Range (Auto)")
frame2.add(tab5, text = "Customer Labels")
frame2.add(tab6, text = "Reports")

tab2a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab2b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab3a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab4a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10, fill=BOTH)
tab4b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab4c.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10, fill=BOTH)
# ============ Side menu commands ============

def reset():
    root.destroy()
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

def set_tag():
    if tag_select.get() == 0:
        asset_type.set("Asset Tag :")
        frame2.tab(2, state="normal")
        frame2.tab(3, state="normal")
    elif tag_select.get() == 1:
        asset_type.set("Serial Number :")
        frame2.tab(2, state="disabled")
        frame2.tab(3, state="disabled")

def help_me():
    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 0:
        messagebox.showinfo("Singles","Enter a tag into the box and press enter.\nYour scanner should do this automatically")
    if tab_index == 1:
        messagebox.showinfo("Groups","Enter as many tags as you like into the box below. You can enter them directly or via the entry box. If you have a list of tags saved in a file you can load it directly from there")
    if tab_index == 2:
        messagebox.showinfo("Range","The prefix is the part of the tag which is the same for all of the tags and comes before the number. The suffix is the same but it comes after the number")
    if tab_index == 3:
        messagebox.showinfo("Range (Auto)","Simple scan the first and last tag and it will print those plus any in between")
    if tab_index == 4:
        messagebox.showinfo("Customer Labels","For printing labels that are unique to a customer")
    if tab_index == 5:
        messagebox.showinfo("Reports","Quickly and easily report one of the listed issues to the leadership team")

    # messagebox.showinfo("About", "Made by Dave Williams for the\nExclusive use of config in the\nCDW NDC located in Rugby")

def set_config():
    config_box = Toplevel(root)
    config_box.title("App Setup")
    config_box.geometry("300x500")

    editor = tkinter.Text(config_box, wrap=WORD, width=34, height=22)
    editor.pack(side=TOP, padx=5, pady=10)

    try:
        File1 = "Images/con_print.ini"
        File2 = open(File1, "r")
        editor.insert("1.0", File2.read())
        File2.close()
    except:
        File1 = "Images/con_print.ini"
        File2 = open(File1, "w")
        editor.insert("1.0", File2.read())
        File2.close()

    save_btn = tkinter.Button(config_box, text="Save Changes", command=save_edit)
    save_btn.pack(side=TOP)

    #Label(config_box, text="Boo, ya filthy animal").pack()
    Label(config_box, text="©Dave Williams 2022").pack(side=BOTTOM)
    Label(config_box, text="Created for the exclusive use in\nconfig at the NDC in Rugby").pack(side=BOTTOM)

# ============ What to do when the enter key is pressed ============

def return_key(event = None):

    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 0:
        mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = str(printer_select.get())
        if single_entry.get() != "":
            try:
                tag_type = bytes(asset_type.get(), 'utf-8')
                zplMessage = bytes(single_entry.get(),'utf-8')  
                mysocket.connect((host, port)) #connecting to host
                mysocket.send(b"^XA^LH15,0^FO1,20^AsN,25,25^FDDevice " + tag_type + b"^FS^FO03,60^B3N,N,100,Y,N^FD" + zplMessage + b"^FS^XZ")#using bytes
                mysocket.close() #closing connection
                single_entry.delete(0, END)
                single_entry.focus()
            except:
                con_error()
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

def quit():
    sys.exit()

def con_error():
    answer = messagebox.askyesno("Question", "Connection error\nAttempt to map network printers?")
    if answer == True:
        subprocess.call(r'net use lpt1: /delete',shell=True)
        subprocess.call(r'net use lpt2: /delete',shell=True)
        subprocess.call(r'net use lpt3: /delete',shell=True)
        subprocess.call(r'net use lpt4: /delete',shell=True)
        subprocess.call(r'net use lpt6: /delete',shell=True)
        subprocess.call(r'net use lpt7: /delete',shell=True)
        subprocess.call(r'net use lpt1 \\10.151.53.22\rug-cfg-zebra-01 /persistent:yes /USER:config\config.engineer homebuild',shell=True)
        subprocess.call(r'net use lpt2 \\10.151.53.22\rug-cfg-zebra-02 /persistent:yes /USER:config\config.engineer homebuild',shell=True)
        subprocess.call(r'net use lpt3 \\10.151.53.22\rug-cfg-zebra-03 /persistent:yes /USER:config\config.engineer homebuild',shell=True)
        subprocess.call(r'net use lpt4 \\10.151.53.22\rug-cfg-zebra-04 /persistent:yes /USER:config\config.engineer homebuild',shell=True)
        subprocess.call(r'net use lpt6 \\10.151.53.22\rug-cfg-zebra-06 /persistent:yes /USER:config\config.engineer homebuild',shell=True)
        subprocess.call(r'net use lpt7 \\10.151.53.22\rug-cfg-zebra-07 /persistent:yes /USER:config\config.engineer homebuild',shell=True)
    else:
        return

def save_edit():
    print()

def Open():
    File1 = filedialog.askopenfilename()
    File2 = open(File1, "r")
    group_textbox.insert("1.0", File2.read())
    File2.close()  # Make sure you close the file when done

def clear_group_text():
    group_textbox.delete("1.0", END)

def print_group_text():
    if group_textbox.get("1.0", END) == "\n":
        return
    group_text = group_textbox.get("1.0", END)
    group_text = re.split(", |\n",group_text)
    try:
        while True:
            group_text.remove("")
    except ValueError:
        pass
    total_print = len(group_text)
    if total_print <= 0:
        messagebox.showerror("Error", "Nothing to print")
        return
    answer = messagebox.askyesno("Question","This will print " + str(total_print) + " labels.\nDo you wish to continue?")
    if answer == True:
        for x in (group_text):
            try:
                if x == "":
                    continue
                mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                host = str(printer_select.get())
                mysocket.connect((host, port)) #connecting to host
                tag_type = bytes(asset_type.get(), 'utf-8')
                y = bytes(x,'utf-8')
                mysocket.send(b"^XA^LH15,0^FO1,20^AsN,25,25^FDDevice " + tag_type + b"^FS^FO03,60^B3N,N,100,Y,N^FD" + y + b"^FS^XZ")#using bytes
                mysocket.close() #closing connection
            except:
                con_error()
                return
            sleep(0.5)
        clear_group_text()
        return
    else:
        messagebox.showinfo("","Printing has been aborted")


def clear_range():
    range_entry2.delete(0, END)
    range_entry3.delete(0, END)
    range_start.set(0)
    range_end.set(0)

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
        prefixed = bytes(str(range_prefix.get()).upper(), 'utf-8')
        suffixed = bytes(str(range_suffix.get()).upper(), 'utf-8')
        for x in range(int(range_start.get()), int(range_end.get())+1):
            try:
                mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                host = str(printer_select.get())
                mysocket.connect((host, port)) #connecting to host
                y = bytes(str(x).zfill(lead_zeros), 'utf-8')
                mysocket.send(b"^XA^LH15,0^FO1,20^AsN,25,25^FDDevice Asset Tag^FS^FO03,60^B3N,N,100,Y,N^FD" + prefixed + y + suffixed + b"^FS^XZ")#using bytes
                mysocket.close() #closing connection
            except:
                con_error()
                return
            sleep(0.5)    
        clear_range()
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

# ============ Auto Range (Experimental)============

def print_auto():
    if auto_1.get() == "" or auto_2.get() == "":
        return
    if auto_1.get() == auto_2.get():
        messagebox.showerror("Error", "Error, that's the same tag twice")
        return
    auto_prefix1 = ""
    auto_start = ""
    auto_suffix1 = "" 
    auto_prefix2 = ""
    auto_end = ""
    auto_suffix2 = ""
    auto_range_split1 = re.split("(\d+)", auto_1.get())
    auto_range_split2 = re.split("(\d+)", auto_2.get())
    if len(auto_1.get()) != len(auto_2.get()) or len(auto_range_split1) != len(auto_range_split2):
        messagebox.showerror("Error", "Error, tags don't match")
        return
    y = 0
    z = 0
    for x in auto_range_split1: #cycles through however many splits exist in the first split
        if auto_range_split1[y] != auto_range_split2[y]:
            z = y + 1
            auto_start = auto_range_split1[y]
            auto_end = auto_range_split2[y]
            for x in auto_range_split1[z:]:
                try:
                    if auto_range_split1[z] == auto_range_split2[z]:
                        auto_suffix1 += x
                        auto_suffix2 += x
                        z+=1
                    else:
                        messagebox.showerror("Error", "Problem determining the suffix")
                        return
                except:
                    break
            break
        elif auto_range_split1[y] == auto_range_split2[y]:
            auto_prefix1 += x
            auto_prefix2 += x
        y+=1
    if auto_prefix1 != auto_prefix2:
        messagebox.showerror("Error", "Error detected in the prefix. \nPlease check and try again")
        return
    elif auto_suffix1 != auto_suffix2:
        messagebox.showerror("Error", "Error detected in the suffix. \nPlease check and try again")
        return
    else:
        total_print = 1 + int(auto_end) - int(auto_start)
        if total_print <= 0:
            messagebox.showerror("Error", "Please sure you have the first and last tags the correct way around")
            return
        answer = messagebox.askyesno("Question","This will print " + str(total_print) + " labels.\nDo you wish to continue?")
        if answer == True:
            lead_zeros = len(auto_end)
            prefixed = bytes(str(auto_prefix1).upper(), 'utf-8')
            suffixed = bytes(str(auto_suffix1).upper(), 'utf-8')
            for x in range(int(auto_start), int(auto_end)+1):
                try:
                    mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    host = str(printer_select.get())
                    mysocket.connect((host, port)) #connecting to host
                    y = bytes(str(x).zfill(lead_zeros), 'utf-8')
                    mysocket.send(b"^XA^LH15,0^FO1,20^AsN,25,25^FDDevice Asset Tag^FS^FO03,60^B3N,N,100,Y,N^FD" + prefixed + y + suffixed + b"^FS^XZ")#using bytes
                    mysocket.close() #closing connection
                except:
                    con_error()
                    return
                sleep(0.5)    
            clear_auto()
        else:
            messagebox.showinfo("","Printing has been aborted")
            return

# ============ Customer label codes ============

def BBC():
    answer = messagebox.askyesno("Question","This will print " + str(cust_quantity.get()) + " BBC labels.\nDo you wish to continue?")
    if answer == True:
        try:
            mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            host = str(printer_select.get())
            mysocket.connect((host, port)) #connecting to host
            y = bytes(str(cust_quantity.get()), 'utf-8')
            mysocket.send(b"^XA^LRY^FO10,10^GB195,203,195^FS^FO225,10^GB195,203,195^FS^FO440,10^GB195,203,195^FS^FO50,37^CFG,180^FDB^FS^FO260,37^FDB^FS^FO470,37^FDC^PQ" + y + b"^FS^XZ")#using bytes
            mysocket.close() #closing connection
        except:
            con_error()
            return
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

def UOB_mac():
    answer = messagebox.askyesno("Question","This will print " + str(cust_quantity.get()) + " MAC QR Code labels.\n for University of Birmingham (UOB)\nDo you wish to continue?")
    if answer == True:
        try:
            mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            host = str(printer_select.get())
            mysocket.connect((host, port)) #connecting to host
            y = bytes(str(cust_quantity.get()), 'utf-8')
            mysocket.send(b"^XA^FX^CF0,60^FO10,10^FDUniversity of^FS^FO10,75^FDBirmingham^FS^FO420,5^BQN,2,3^FDhttps://www.youtube.com/watch?v=dQw4w9WgXcQ&ab^PQ" + y + b"^FS^XZ")#using bytes
            mysocket.close() #closing connection
        except:
            con_error()
            return
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

def UOB_PC():
    print()

# ============ Title piece ============
try:
    logo_img = ImageTk.PhotoImage(Image.open("Images/2560px-CDW_Logo.svg.png").resize((100, 60)))
    logo = Label(frametop1, image=logo_img)
    logo.pack(side=LEFT, anchor=W, padx=10, pady=10)
except:
    logo_text = tk.Label(frametop1, text="CDW", font=("Helvetica",20))
    logo_text.pack(side=LEFT, anchor=W, padx=10, pady=10)
app_title = tk.Label(frametop2, text="Config General Printing Application", font=("Helvetica",25)).pack(side=TOP)
help_button = tk.Button(master=frametop3, text="?", font=('Helvetica',20), command=help_me).pack(padx=(0,10))
try:
    cog_icon = ImageTk.PhotoImage(Image.open("Images/cogwheel.png").resize((25, 25)))
    cog = tk.Button(master=frametop3, image=cog_icon, borderwidth=0, command=set_config)
    cog.pack(padx=(0,8), pady=(5,0))    
except:
    cog = tk.Button(master=frametop3, text="...", font=("Helvetica",14), command=set_config).pack()
# ============ Settings panel (frame1a) ============

printer_label = tk.Label(master=frame1,
                            text="Select printer:")
printer_label.grid(row=0, sticky=EW)

config_print_button = tk.Radiobutton(master=frame1,
                    text="Config Printer",
                    variable=printer_select,
                    value="LPT1")
config_print_button.grid(row=1, sticky=W)

mezz_print_button = tk.Radiobutton(master=frame1,
                    text="MEZZ Printer",
                    variable=printer_select,
                    value="LPT7")
mezz_print_button.grid(row=2, sticky=W)

test_print_button = tk.Radiobutton(master=frame1,
                    text="Test Printer",
                    variable=printer_select,
                    value="192.168.8.100")
test_print_button.grid(row=3, sticky=W)

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
                    command=quit)
exit_button.grid(row=9, sticky=EW)

# ============ Single Tab (tab1) ============

tab1.grid_columnconfigure((0,1,2,3),weight=1)
tab1.grid_rowconfigure((0,1,2,3),weight=1)

single_label = tk.Label(master=tab1,
                        textvariable=asset_type)
single_label.grid(row=0, column=1, sticky=E)

single_entry = tk.Entry(master=tab1)
single_entry.grid(row=0, column=2, sticky=W, padx=10)

single_descript = tk.Label(master=tab1,
                        text="This will print a single label",
                        font=12,
                        fg="blue")
single_descript.grid(row=1, column=1, columnspan=2, sticky=N)

# ============ Groups Tab (tab2) ============

group_label1 = tk.Label(master=tab2,
                        font=12,
                        fg="blue",
                        text="Print the tags below:")
group_label1.pack()

group_label = tk.Label(master=tab2a,
                        textvariable=asset_type)
group_label.pack(side=LEFT, pady=(20,0))

group_entry = tk.Entry(master=tab2a,)
group_entry.pack(side=LEFT, padx=10, pady=(20,0))

group_clear = tk.Button(master=tab2b,
                        text="Clear",
                        command=clear_group_text)
group_clear.pack(side=LEFT)

group_print = tk.Button(master=tab2b,
                        text="Print",
                        command=print_group_text)
group_print.pack(side=LEFT, padx=100)

group_load = tk.Button(master=tab2b,
                        text="Load from file",
                        command=Open)
group_load.pack(side=LEFT, padx=(0,100))

group_textbox = Text(master=tab2, wrap=WORD)
group_textbox.pack(side=BOTTOM, fill=BOTH, expand=True, padx=5, pady=5)

# ============ Range Tab (tab3) ============

range_label1 = tk.Label(master=tab3a,
                        font=12,
                        fg="blue",
                        text="Print a range of asset tags")
range_label1.grid(row=0, column=0, columnspan=2)

range_label2 = tk.Label(master=tab3a,
                        text="Enter the Prefix of the tag")
range_label2.grid(row=1, column=0, pady=(20,0))

range_entry2 = tk.Entry(master=tab3a,
                        textvariable=range_prefix)
range_entry2.grid(row=2, column=0)

range_label3 = tk.Label(master=tab3a,
                        text="Enter the Suffix of the tag")
range_label3.grid(row=1, column=1, pady=(20,0))

range_entry3 = tk.Entry(master=tab3a,
                        textvariable=range_suffix)
range_entry3.grid(row=2, column=1)

range_label4 = tk.Label(master=tab3a,
                        text="Enter the starting number of the range")
range_label4.grid(row=3, column=0, pady=(20,0), padx=10)

range_entry4 = tk.Entry(master=tab3a,
                        textvariable=range_start)
range_entry4.grid(row=4, column=0)

range_label5 = tk.Label(master=tab3a,
                        text="Enter the ending number of the range")
range_label5.grid(row=3, column=1, pady=(20,0), padx=10)

range_entry5 = tk.Entry(master=tab3a,
                        textvariable=range_end)
range_entry5.grid(row=4, column=1)

range_clear = tk.Button(master=tab3a,
                        text="Clear",
                        command=clear_range)
range_clear.grid(row=5, column=0, pady=(20,0), padx=40, sticky=E)

range_print = tk.Button(master=tab3a,
                        text="Print",
                        command=print_range)
range_print.grid(row=5, column=1, pady=(20,0), padx=40, sticky=W)

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

auto_clear = tk.Button(master=tab4b,
                        text="Clear",
                        command=clear_auto)
auto_clear.grid(row=0, column=1, padx=10)

auto_print = tk.Button(master=tab4b,
                        text="Print",
                        command=print_auto)
auto_print.grid(row=0, column=2, padx=10)

warn_label = tk.Label(master=tab4c,
                        text="New Feature\nCheck number of tags\n is correct\nbefore printing",
                        font=("Helvetica",14),
                        fg="dark red")
warn_label.pack(side=TOP, padx=40, pady=40)

# ============ Customer label Tab (tab5) ============

print_quantity_label = tk.Label(master=tab5,
                            font=12,
                            fg="blue",
                            text="Enter quantity of labels required")
print_quantity_label.grid(row=0, column=0, pady=20, padx= 10)

print_quantity = tk.Spinbox(master=tab5, from_=1, to=9999,
                            textvariable=cust_quantity)
print_quantity.grid(row=0, column=1, pady=10, padx= 10)

bbc_button = tk.Button(master=tab5,
                        text="BBC",
                        command=BBC)
bbc_button.grid(row=2, column=0, pady=10, padx= 10)

bbc_button = tk.Button(master=tab5,
                        text="eBay Mac QR Code",
                        command=UOB_mac)
bbc_button.grid(row=3, column=0, pady=10, padx= 10)

bbc_button = tk.Button(master=tab5,
                        text="eBay PC QR Code",
                        command=UOB_PC)
bbc_button.grid(row=4, column=0, pady=10, padx= 10)

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
