import os
import re
import subprocess
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Notebook
import socket
from PIL import Image, ImageTk
from time import sleep
from configparser import ConfigParser
import tkinter.scrolledtext as tkscrolled

root = tk.Tk()
root.title("Config printing app")
# root.tk_setPalette(background="#444", foreground="#eee")

w = 780 # width for the Tk root
h = 520 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# ============ Variables ============

range_prefix = tk.StringVar(None, "")
range_suffix = tk.StringVar(None, "")
range_start = tk.StringVar(None, "0")
range_end = tk.StringVar(None, "0")
printer_select = tk.StringVar(None, "LPT1")
local_print = tk.StringVar(None, "192.168.8.100")
tag_select = tk.IntVar(value=0)
asset_type = tk.StringVar(None, "Asset Tag :")
cust_quantity = tk.IntVar(None)
auto_1 = tk.StringVar(None)
auto_2 = tk.StringVar(None)
bg_col = str("white")
xyz = str(" ")
flag_1 = int(1)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception: 
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ============ Printer Initial Setup ============

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

frame1.grid_rowconfigure((0,1,2,5,6,7,9,10), weight=1)
frame1.grid_rowconfigure((3,4,8), weight=8)
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
    try:
        if flag_1 == 1:
            mezz_print_button.configure(state=DISABLED)
            config_print_button.configure(state=NORMAL)
            # print("Flag = 1")
        elif flag_1 == 2:
            config_print_button.configure(state=DISABLED)
            mezz_print_button.configure(state=NORMAL)
            # print("Flag = 2")
        elif flag_1 == 0:
            mezz_print_button.configure(state=NORMAL)
            config_print_button.configure(state=NORMAL)
            # print("Flag = 0")
    except:
        pass
    # print("Flag_1 is set to")
    # print(flag_1)
    con_update()

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
        messagebox.showinfo("Range (Auto)","Simply scan the first and last tag and it will print those plus any in between")
    if tab_index == 4:
        messagebox.showinfo("Customer Labels","For printing labels that are unique to a customer")
    if tab_index == 5:
        messagebox.showinfo("Reports","Quickly and easily report one of the listed issues to the leadership team")

    # messagebox.showinfo("About", "Made by Dave Williams for the\nExclusive use of config in the\nCDW NDC located in Rugby")

def set_config():
    config_box = Toplevel(root)
    config_box.title("Settings and about")

    def kill_me():
        config_box.destroy()

    w = 300 # width for the Tk root
    h = 500 # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) + (400)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    config_box.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Close config window on lose focus
    config_box.focus_force()
    config_box.bind('<FocusOut>', lambda x:kill_me())

    # Fill the config window with stuff
    label2 = tk.Label(config_box,
                    text="Settings saved in the config file")
    label2.pack(side=TOP)                    

    config_text = tk.Text(config_box, wrap=WORD, width=34, height=7, state=DISABLED)
    config_text.pack(side=TOP, padx=5, pady=(0,10))

    try: # If the file doesn't exist 
        File1 = "data/con_print.ini"
        File2 = open(File1, "r")
        config_text.config(state=NORMAL)
        config_text.insert("1.0", File2.read())
        config_text.config(state=DISABLED)
        File2.close()
    except: # create a fresh file and restart the config window in one smooth action
        File1 = "data/con_print.ini"
        File2 = open(File1, "w")
        File2.close()
        kill_me()
        set_config()
    label3 = tk.Label(config_box,
                    text="The last 1000 tags you printed")
    label3.pack(side=TOP)  

    log_text = tkscrolled.ScrolledText(config_box, wrap=WORD, width=32, height=15, state=DISABLED)
    log_text.pack(side=TOP, padx=5)

    try: # If the file doesn't exist 
        File1 = "data/logs.txt"
        File2 = open(File1, "r")
        log_text.config(state=NORMAL)
        log_text.insert("1.0", File2.read())
        log_text.config(state=DISABLED)
        File2.close()
    except: # create a fresh file and restart the config window in one smooth action
        File1 = "data/logs.txt"
        File2 = open(File1, "w")
        File2.close()
        kill_me()
        set_config()



    # exit_btn = tk.Button(config_box, text="Close window", command=kill_me)
    # exit_btn.pack(side=BOTTOM, pady=(30,20))

    
    Label(config_box, text="©Dave Williams 2022").pack(side=BOTTOM)
    Label(config_box, text="CDW Logo ©CDW 2022").pack(side=BOTTOM)
    Label(config_box, text="Created for the exclusive use in\nconfig at the NDC in Rugby").pack(side=BOTTOM)


# ============ What to do when the enter key is pressed ============

def return_key(event = None):

    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 0:
        if single_entry.get() != "":
            tag_type = asset_type.get()
            zplMessage = single_entry.get()
            xyz = ("^XA^LH15,0^FO1,20^AsN,25,25^FDDevice " + tag_type + "^FS^FO03,60^B3N,N,100,Y,N^FD" + zplMessage + "^FS^XZ")
            log = zplMessage
            to_print(xyz ,log)
            single_entry.delete(0, END)
            single_entry.focus()
            return
        else:
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
    print("Print error")

def set_print():
    answer = messagebox.askyesno("Question", "Attempt to map network printers?")
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

def history(log):
    file = open("data\logs.txt", "a")
    file.close()
    with open("data\logs.txt", "r") as history_orig:
        save = history_orig.read().upper()
    with open("data\logs.txt", "w") as history_orig:
        history_orig.write(str(log).upper())
        history_orig.write("\n")
        history_orig.write(save)
    N = 1000 # number of lines you want to keep
    with open("data\logs.txt","r+") as f:
        data = f.readlines()
        if len(data) > N: data = data[0:N]
        f.seek(0)
        f.writelines(data)
        f.truncate()
    return
    

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
    group_text = re.split(", |\n| ",group_text)
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
            if x == "":
                continue
            tag_type = asset_type.get()
            y = x
            xyz = ("^XA^LH15,0^FO1,20^AsN,25,25^FDDevice " + tag_type + "^FS^FO03,60^B3N,N,100,Y,N^FD" + y + "^FS^XZ")
            log = y
            to_print(xyz ,log)
            sleep(0.7)
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
        lead_zeros = max(len(range_end.get()), len(range_start.get()))
        prefixed = str(range_prefix.get()).upper()
        suffixed = str(range_suffix.get()).upper()
        for x in range(int(range_start.get()), int(range_end.get())+1):
            y = str(x).zfill(lead_zeros)
            xyz = ("^XA^LH15,0^FO1,20^AsN,25,25^FDDevice Asset Tag^FS^FO03,60^B3N,N,100,Y,N^FD" + prefixed + y + suffixed + "^FS^XZ")
            log = prefixed + y + suffixed
            to_print(xyz, log)
            sleep(0.7)    
        clear_range()
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

def clear_all():
    clear_auto()
    clear_group_text()
    clear_range()

def con_update():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("data/con_print.ini")
    #Get the PRINTER section
    printer = config_object["PRINTER"]
    #Update the printer
    printer["printer_select"] = printer_select.get()
    printer["local_print"] = local_print.get()
    #Get the TAG-TYPE section
    tag = config_object["TAG-TYPE"]
    #Update the tag
    tag["tag_select"] = str(tag_select.get())
    flag = config_object["FLAGS"]
    flag["flag_1"] = str(flag_1)

    #Write changes back to file
    with open('data/con_print.ini', 'w') as conf:
        config_object.write(conf)

def to_print(zyx, log):
    host = str(printer_select.get())
    if host == "local":
        host = str(local_print.get())
    print_me = bytes(zyx, 'utf-8')
    try:
        if "LPT" in host:
            sys.stdout = open(host, 'a')
            print(print_me)
            sys.stdout = sys.__stdout__
            history(log)
            clear_all()
            return
        else:
            mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            mysocket.connect((host, port)) #connecting to host
            mysocket.send(print_me)
            mysocket.close() #closing connection
            history(log)
            return
    except:
        con_error()
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
            prefixed = str(auto_prefix1).upper()
            suffixed = str(auto_suffix1).upper()
            for x in range(int(auto_start), int(auto_end)+1):
                y = str(x).zfill(lead_zeros)
                xyz = ("^XA^LH15,0^FO1,20^AsN,25,25^FDDevice Asset Tag^FS^FO03,60^B3N,N,100,Y,N^FD" + prefixed + y + suffixed + "^FS^XZ")
                log = prefixed + y + suffixed
                to_print(xyz ,log)
                sleep(0.7)    
            clear_auto()
        else:
            messagebox.showinfo("","Printing has been aborted")
            return

# ============ Config Parser ============

try:
    # os.makedirs("data", exist_ok=True)
    #Get the configparser object and read file
    config_object = ConfigParser()
    config_object.read("data/con_print.ini")
    #Get the settings
    printer = config_object["PRINTER"]
    tag = config_object["TAG-TYPE"]
    flag = config_object["FLAGS"]
    # printer_select.set = tk.StringVar(format(printer["printer_select"]))
    print_1 = str(format(printer["printer_select"]))
    printer_select.set(print_1)
    local_1 = str(format(printer["local_print"]))
    local_print.set(local_1)
    tag_1 = int(tag["tag_select"])
    tag_select.set(tag_1)
    flag_1a = int(flag["flag_1"]) # 1 = Config, 2 = Mezz, 0 = Technician
    flag_1 = flag_1a
    
except:
    #Get the configparser object and create file
    config_object = ConfigParser()
    config_object["PRINTER"] = {
        "printer_select": printer_select.get(),
        "local_print": local_print.get()}
    config_object["TAG-TYPE"] = {
        "tag_select": tag_select.get()}
    config_object["FLAGS"] = {
        "flag_1": flag_1}
    with open('data/con_print.ini', 'w') as conf:
        config_object.write(conf)
    
# ============ Customer label codes ============

def BBC():
    answer = messagebox.askyesno("Question","This will print " + str(cust_quantity.get()) + " BBC labels.\nDo you wish to continue?")
    if answer == True:
        y = str(cust_quantity.get())
        xyz = ("^XA^LRY^FO10,10^GB195,203,195^FS^FO225,10^GB195,203,195^FS^FO440,10^GB195,203,195^FS^FO50,37^CFG,180^FDB^FS^FO260,37^FDB^FS^FO470,37^FDC^PQ" + y + "^FS^XZ")
        log = ("**BBC Tag** x" + y)
        to_print(xyz ,log)
        return
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

def ebay_mac():
    answer = messagebox.askyesno("Question","This will print " + str(cust_quantity.get()) + " MAC QR\nCode label for eBay\nDo you wish to continue?")
    if answer == True:
        y = str(cust_quantity.get())
        xyz = ("^XA^FX^CF0,60^FO10,10^FDeBay QR Code^FS^FO10,75^FDfor MAC^FS^FO420,5^BQN,2,4^FDQA,www.youtube.com/watch?v=dQw4w9WgXcQ^PQ" + y + "^FS^XZ")
        log = ("**Ebay MAC QR tag** x" + y)
        to_print(xyz ,log)
        return
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

def ebay_PC():
    answer = messagebox.askyesno("Question","This will print " + str(cust_quantity.get()) + " MAC QR\nCode label for eBay\nDo you wish to continue?")
    if answer == True:
        y = str(cust_quantity.get())
        xyz = ("^XA^FX^CF0,60^FO10,10^FDeBay QR Code^FS^FO10,75^FDfor PC^FS^FO420,5^BQN,2,4^FDQA,www.youtube.com/watch?v=KMYN4djSq7o^PQ" + y + "^FS^XZ")
        log = ("**Ebay PC QR tag** x" + y)
        to_print(xyz ,log)
        return
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

# ============ Title piece ============

try:
    logo_img = ImageTk.PhotoImage(Image.open("data/CDW_Logo.png").resize((100, 60)))
    logo = Label(frametop1, image=logo_img)
    logo.pack(side=LEFT, anchor=W, padx=15, pady=10)
except:
    logo_text = tk.Label(frametop1, text="CDW", font=("Helvetica",20))
    logo_text.pack(side=LEFT, anchor=W, padx=10, pady=10)
app_title = tk.Label(frametop2, text="Config General Printing Application", font=("Helvetica",25)).pack(side=TOP)
help_button = tk.Button(master=frametop3, text="?", font=('Helvetica',20), command=help_me).pack(padx=(0,10))
try:
    cog_icon = ImageTk.PhotoImage(Image.open("data/cogwheel.png").resize((25, 25)))
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
                    value="LPT1",
                    command=con_update)
config_print_button.grid(row=1, sticky=W)

mezz_print_button = tk.Radiobutton(master=frame1,
                    text="MEZZ Printer",
                    variable=printer_select,
                    value="LPT7",
                    command=con_update)
mezz_print_button.grid(row=2, sticky=W)

test_print_button = tk.Radiobutton(master=frame1,
                    text="Test Printer",
                    value="local",
                    variable=printer_select,
                    command=con_update)
test_print_button.grid(row=3, sticky=W)

set_printer_btn = tk.Button(master=frame1,
                    text="Map Printers",
                    command=set_print)
set_printer_btn.grid(row=4, sticky=EW)

asset_label = tk.Label(master=frame1,
                            text="Asset or serial?")
asset_label.grid(row=5, sticky=EW)

set_asset_button = tk.Radiobutton(master=frame1,
                    text="Asset tags",
                    variable=tag_select,
                    value=0,
                    command=set_tag)
set_asset_button.grid(row=6, sticky=W)

set_serial_button = tk.Radiobutton(master=frame1,
                    text="Serial Numbers",
                    variable=tag_select,
                    value=1,
                    command=set_tag)
set_serial_button.grid(row=7, sticky=W)

reset_button = tk.Button(master=frame1,
                    text="Restart App",
                    command=reset)
reset_button.grid(row=9, sticky=EW)

exit_button = tk.Button(master=frame1,
                    text="Quit",
                    command=quit)
exit_button.grid(row=10, sticky=EW)

# ============ Single Tab (tab1) ============

tab1.grid_columnconfigure((0,1,2,3),weight=1)
tab1.grid_rowconfigure((0,1,2,3),weight=1)

single_label = tk.Label(master=tab1,
                        textvariable=asset_type)
single_label.grid(row=0, column=1, sticky=E)

single_entry = tk.Entry(master=tab1, bg=bg_col)
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

group_entry = tk.Entry(master=tab2a, bg=bg_col)
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



group_textbox = tkscrolled.ScrolledText(master=tab2, wrap=WORD)
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

ebay_mac_button = tk.Button(master=tab5,
                        text="eBay Mac QR Code",
                        command=ebay_mac)
ebay_mac_button.grid(row=3, column=0, pady=10, padx= 10)

ebay_pc_button = tk.Button(master=tab5,
                        text="eBay PC QR Code",
                        command=ebay_PC)
ebay_pc_button.grid(row=4, column=0, pady=10, padx= 10)

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

try:
    set_tag()
except:
    pass
root.bind('<Return>', return_key)
root.mainloop()
