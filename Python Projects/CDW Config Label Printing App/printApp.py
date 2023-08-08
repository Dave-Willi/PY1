############
# pip installs used by this script
############
# playsound 1.2.2 (newer versions are broken!)
# pillow
# pywin32
# configparser
# tkcalendar

# imports.... so many imports 

import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Notebook, Style
from PIL import Image, ImageTk
from configparser import ConfigParser
import tkinter.scrolledtext as tkscrolled
import re
# from tkcalendar import DateEntry

root = tk.Tk()
root.title("CDW Config Label Printer") # Title of app window

w = 1080 # width for the App
h = 720 # height for the App

# ==========================================
# ============ Position window =============
# ==========================================

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the app window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(False,False) # Disable resizing of window

# Set program icon in top right corner to image
try:
    root.iconphoto(False, tk.PhotoImage(file='data/CDW_icon.png'))
except:
    pass

# Set default font style for MOST widgets, does NOT effect notebook tabs. That requires a custom style
root.option_add( "*font", "aerial 14" )

# ***************************************************************
# cfg holds global variables. MUST import AFTER initiating window
# ***************************************************************
import cfg

# Set recource path for program, relative to exe location.
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception: 
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ==========================================
# ============ Primary Frames ==============
# ==========================================

# frametop = header
# header is further split into 3 sections = frametop1, frametop2, frametop3
# Body is split into 2x1 = frame1, frame2

frametop = tk.Frame(root,
                    height=120,
                    width=780)
frametop.pack(side=TOP, fill=X, expand=False)

frametop1 = tk.Frame(frametop,
                    height=80,
                    width=100)
frametop1.pack(side=LEFT, anchor=W)

frametop3 = tk.Frame(frametop, 
                    height=80,
                    width=680)
frametop3.pack(side=RIGHT) #frametop3 is packed before frametop2 to keep it on the right

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

# Creates a style for use on the notebook tabs
Mysky = "#DCF0F2"
Myyellow = "#F2C88B"
MyGrey = "#DADADA"
style = Style()
style.theme_create( "dummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": Mysky,
                            "font":("aerial",12)},
            "map":       {"background": [("selected", Myyellow),("disabled",MyGrey)],
                          "expand": [("selected", [1, 1, 1, 0])],}
                           } } )
style.theme_use("dummy")


# ==========================================
# ================= Tabs ===================
# ==========================================
# additional frames created inside tabs for formatting 

tab1 = tk.Frame(frame2) # singles
tab2 = tk.Frame(frame2) # groups
tab2a = tk.Frame(tab2)
tab2b = tk.Frame(tab2)
tab2c = tk.Frame(tab2, height=45)
tab2d = tk.Frame(tab2)
tab3 = tk.Frame(frame2) # range
tab3a = tk.Frame(tab3)
tab4 = tk.Frame(frame2) # range auto
tab4a = tk.Frame(tab4)
tab4b = tk.Frame(tab4)
tab4c = tk.Frame(tab4)
tab5 = tk.Frame(frame2) # customer labels
tab5a = tk.Frame(tab5)
tab5b = tk.Frame(tab5)
tab6 = tk.Frame(frame2) # reports
tab7 = tk.Frame(frame2) # custom labels
tab7a = tk.Frame(tab7)
tab7aa = tk.Frame(tab7)
tab7ab = tk.Frame(tab7)
tab7b = tk.Frame(tab7)
tab7c = tk.Frame(tab7)
frame2.add(tab1, text = "     Singles     ")
frame2.add(tab2, text = "     Groups      ")
#frame2.add(tab3, text = "  Range (Manual) ")
frame2.add(tab4, text = "      Range      ")
frame2.add(tab5, text = " Customer Labels ")
frame2.add(tab7, text = "  Custom Labels  ")

tab2a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab2b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab2c.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab2d.pack(anchor=CENTER, expand=False, side=BOTTOM, pady=(10,30), padx=10)
tab3a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab4a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10, fill=BOTH)
tab4b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab4c.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10, fill=BOTH)
tab5a.pack(anchor=CENTER, expand=False, side=TOP, pady=(10,0))
tab5b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10, fill=BOTH)
tab7a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab7aa.pack(anchor=CENTER, expand=False, side=TOP)
tab7ab.pack(anchor=CENTER, expand=False, side=TOP)
tab7b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab7c.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)

# *******************************************************
# explicit import conFuncs functions after setting frames
# *******************************************************
from conFuncs import cust_print, quit, BCPrint, to_print, txtPrint, QRPrint, ctrl_p, history, limit_print

# ==========================================
# =========== Side menu commands ===========
# ==========================================
# definitions required for the buttons on the left side menu to function

def reset(): # restarts app by closing it and then restarting
    root.destroy()
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

def set_tag(): # Change between asset tag and serial number. Sets colour of entry box as an added hint for which is selected. Disable range tabs in serial number mode.
    if cfg.tag_select.get() == 0:
        cfg.asset_type.set("Asset Tag :")
        frame2.tab(2, state="normal")
        frame2.tab(3, state="normal")
        bg_col = "#eef"
        cfg.device_label.set("Device")
        serial_radio2.configure(state=NORMAL)
        serial_radio3.configure(state=NORMAL)
        serial_radio2a.configure(state=NORMAL)
        serial_radio3a.configure(state=NORMAL)
    elif cfg.tag_select.get() == 1:
        cfg.asset_type.set("Serial Number :")
        frame2.tab(2, state="disabled")
        frame2.tab(3, state="disabled")
        bg_col = "#fee"
        serial_radio2.configure(state=NORMAL)
        serial_radio3.configure(state=NORMAL)
        serial_radio2a.configure(state=NORMAL)
        serial_radio3a.configure(state=NORMAL)
    try: # Disables printer selections based on config setting
        single_entry.config(bg=bg_col)
        group_entry.config(bg=bg_col)
        if cfg.flag_1 == 1:
            mezz_print_button.configure(state=DISABLED)
            config_print_button.configure(state=NORMAL)
            config_print_button2.configure(state=NORMAL)
        elif cfg.flag_1 == 2:
            config_print_button.configure(state=DISABLED)
            config_print_button2.configure(state=DISABLED)
            mezz_print_button.configure(state=NORMAL)
        elif cfg.flag_1 == 0:
            mezz_print_button.configure(state=NORMAL)
            config_print_button.configure(state=NORMAL)
            config_print_button2.configure(state=NORMAL)
    except:
        pass
    con_update()

def help_me(): # Set custom help dialog boxes for each page/tab
    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    set_config(tab_index)


def set_config(tab=""): # additional window with extra info such as print log
    omni_box = Toplevel(root)
    omni_box.title("Settings and about")
    omni_box.overrideredirect(True)

    def kill_me(): # closes the extra window
        omni_box.destroy()

    w = 350 # width for the Tk root
    h = 740 # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) + (550)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    omni_box.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Close config window on lose focus
    omni_box.focus_force()
    omni_box.bind('<FocusOut>', lambda x:kill_me())

    # Fill the config window with stuff
    if tab == "":
        
        # =======================================================
        # ===== Display last 100 tags printed from log file =====
        # =======================================================

        label3 = tk.Label(omni_box,
                        text="The last 1000 tags you printed")
        label3.pack(side=TOP)  

        log_text = tkscrolled.ScrolledText(omni_box, wrap=WORD, width=32, height=24, state=DISABLED)
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
    else:
        try:
            canvas = Canvas(omni_box, width = 300, height = 400)
            canvas.pack()
            if tab == 0: # singles tab
                cfg.range_image = ImageTk.PhotoImage(Image.open("data/single_helper.jpg").resize((300,400)))
            if tab == 1: # groups tab
                cfg.range_image = ImageTk.PhotoImage(Image.open("data/groups_helper.jpg").resize((300,400)))
            if tab == 2: # Range tab
                cfg.range_image = ImageTk.PhotoImage(Image.open("data/range_helper.jpg").resize((300,400)))
            if tab == 3: # Range (auto) tab
                cfg.range_image = ImageTk.PhotoImage(Image.open("data/range_auto_helper.jpg").resize((300,400)))
            if tab == 4: # customer labels tab
                cfg.range_image = ImageTk.PhotoImage(Image.open("data/cust_helper.jpg").resize((300,400)))
            if tab == 5: # reports tab
                cfg.range_image = ImageTk.PhotoImage(Image.open("data/reports_helper.jpg").resize((300,400)))
            if tab == 6: # custom labels tab
                cfg.range_image = ImageTk.PhotoImage(Image.open("data/custom_helper.jpg").resize((300,400)))
            canvas.create_image(0, 0, anchor=NW, image=cfg.range_image)
        except:
            logo_text = tk.Label(omni_box, text="Image is missing", font=("Helvetica",16))
            logo_text.pack(side=TOP)

    # ==========================================
    # =========== short about info =============
    # ==========================================

    # attaches to bottom of window, items placed here are bottom to top i.e. reverse order
    Label(omni_box, text="App ©Dave Williams 2022").pack(side=BOTTOM)
    Label(omni_box, text="CDW Logo ©CDW 2022").pack(side=BOTTOM)
    Label(omni_box, text="Created for the exclusive use in\nconfig at the NDC in Rugby").pack(side=BOTTOM)


# ====================================================
# ===== What to do when the enter key is pressed =====
# ====================================================
# Currently only applies to single and group tags

def return_key(event = None):
    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 0: # single tags
        if single_entry.get() != "":
            tag_type = cfg.asset_type.get()
            zplMessage = (single_entry.get().upper())
            BCPrint(zplMessage,1,zplMessage,tag_type)
            single_entry.delete(0, END)
            single_entry.focus()
            return
        else:
            single_entry.focus()
            return
    if tab_index == 1: # group tags
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

def return_auto1(event = None):
    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 3: # auto range
        auto_entry2.focus()

def return_auto2(event = None):
    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 3: # auto range
        auto_entry1.focus()

# ==========================================
# ========= Command definitions ============
# ==========================================
# miscellaneous defined commands

def open_file1(): # opens selected file for group textbox insertion
    File1 = filedialog.askopenfilename()
    File2 = open(File1, "r")
    group_textbox.insert("1.0", File2.read())
    File2.close()  # Make sure you close the file when done

def open_file2(): # opens selected file for custom textbox insertion
    File1 = filedialog.askopenfilename()
    File2 = open(File1, "r")
    custom_textbox.insert("1.0", File2.read())
    File2.close()  # Make sure you close the file when done

def print_group_text(): # print the group text box
    if group_textbox.get("1.0", END) == "\n":
        return
    group_text = (group_textbox.get("1.0", END).upper())
    group_text = re.split(", |\n| ",group_text) # split and parse the text box into a list
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
        full_range = ""
        suf_label = "^FS^PQ1^XZ"
        pre_label = "^XA^LH" + str(15+(cfg.horz_label_mod.get() * 5)) + "," + str(10 + (cfg.label_mod.get() * 8)) + "^FO1,20^ASN,25,25^FD"+ cfg.device_label.get() + " " + cfg.asset_type.get() + "^FS^FO3,60^BCN,80,Y,N^FD"
        for x in (group_text):
            if x == "":
                continue
            history(x)
            y = pre_label + x + suf_label
            full_range += y
        limit_print(full_range)
        clear_all()
        return
    else:
        messagebox.showinfo("","Printing has been aborted")
    
def clear_all(): # resets all entry boxes and spinboxes to default (Empty) values
    clear_custom_qr()
    single_entry.delete(0, END)
    group_entry.delete(0, END)
    auto_entry1.delete(0, END)
    auto_entry2.delete(0, END)
    group_textbox.delete("1.0", END)
    custom_textbox.delete("1.0", END)
    range_entry2.delete(0, END)
    range_entry3.delete(0, END)
    cfg.range_start.set('')
    cfg.range_end.set('')
    cfg.cust_quantity.set(1)
    cfg.textmod.set(0)
    cfg.device_label.set("Device")

def clear_custom_qr(): # clears the QR code text box
    custom_qr.delete(0, END)
    # slide1.set(340)
    # slide2.set(2)

def print_range(): # Print from the legacy range tab using data entered into it
    total_print = 1 + int(cfg.range_end.get()) - int(cfg.range_start.get())
    if total_print <= 0:
        messagebox.showerror("Error", "Please sure you have the start and end numbers the correct way around")
        return
    answer = messagebox.askyesno("Question","This will print " + str(total_print) + " labels.\nDo you wish to continue?")
    if answer == True:
        lead_zeros = max(len(cfg.range_end.get()), len(cfg.range_start.get())) # Use the longer of the two number to determine leading zeros
        prefixed = str(cfg.range_prefix.get()).upper() # prefix entry, converted to upper case
        suffixed = str(cfg.range_suffix.get()).upper() # suffix entry, converted to lower case
        full_range = ""
        pre_label = "^XA^LH" + str(15+(cfg.horz_label_mod.get() * 5)) + "," + str(10 + (cfg.label_mod.get() * 8)) + "^FO1,20^ASN,25,25^FDDevice Asset Tag^FS^FO3,60^BCN,80,Y,N^FD"
        suf_label = "^FS^PQ1^XZ"
        for x in range(int(cfg.range_start.get()), int(cfg.range_end.get())+1):
            y = str(x).zfill(lead_zeros)
            log = prefixed + y + suffixed
            full_range += pre_label + log + suf_label
        # add to print log the range that was printed rather than the full list of labels
        history("To: " + prefixed + cfg.range_end.get() + suffixed) 
        history("From: " + prefixed + cfg.range_start.get() + suffixed)
        history("Printed range")
        limit_print(full_range)
        clear_all()
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

# ============ Auto Range (Experimental)============

def print_auto():
    if cfg.auto_1.get() == "" or cfg.auto_2.get() == "":
        return
    if cfg.auto_1.get() == cfg.auto_2.get():
        messagebox.showerror("Error", "Error, that's the same tag twice")
        return
    auto_prefix1 = ""
    auto_start = ""
    auto_suffix1 = "" 
    auto_prefix2 = ""
    auto_end = ""
    auto_suffix2 = ""
    auto_range_split1 = re.split("(\d+)", cfg.auto_1.get())
    auto_range_split2 = re.split("(\d+)", cfg.auto_2.get())
    if len(cfg.auto_1.get()) != len(cfg.auto_2.get()) or len(auto_range_split1) != len(auto_range_split2):
        messagebox.showerror("Error", "Error, tags don't match")
        return
    y = 0
    z = 0
    for x in auto_range_split1: #cycles through however many splits exist in the first split
        if auto_range_split1[y] != auto_range_split2[y]:
            z = y + 1
            auto_start = min(auto_range_split1[y],auto_range_split2[y]) # sets the lowest number entered into the start
            auto_end = max(auto_range_split2[y],auto_range_split1[y]) # sets the highest number entered into the end
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
            full_range = ""
            pre_label = "^XA^LH" + str(15+(cfg.horz_label_mod.get() * 5)) + "," + str(10 + (cfg.label_mod.get() * 8)) + "^FO1,20^ASN,25,25^FDDevice Asset Tag^FS^FO3,60^BCN,80,Y,N^FD"
            suf_label = "^FS^PQ1^XZ"
            for x in range(int(auto_start), int(auto_end)+1):
                y = str(x).zfill(lead_zeros)
                log = prefixed + y + suffixed
                full_range += pre_label + log + suf_label
            history("To: " + prefixed + auto_end + suffixed)
            history("From: " + prefixed + auto_start + suffixed)
            history("Printed range")
            limit_print(full_range)
        else:
            messagebox.showinfo("","Printing has been aborted")
            return
    clear_all()

def print_custom_one(): # print one custom label
    qr = custom_qr.get()
    txt = custom_textbox.get("1.0", END)
    if (qr == "") and (txt.isspace()):
        return
    print_custom(1,qr,txt)
    
def print_custom_many(): # print many custom labels
    quant = str(cfg.cust_quantity.get())
    qr = custom_qr.get()
    txt = custom_textbox.get("1.0", END)
    if (qr == "") and (txt.isspace()):
        return
    answer = messagebox.askyesno("Question","This will print " + quant + " labels.\nDo you wish to continue?")
    if answer == True:
        print_custom(quant,qr,txt)
        clear_all()
    else:
        messagebox.showinfo("","Printing has been aborted")

def print_custom(quant,qr,txt): # 1 step print function for custom labels
    cfg.qr_pos = 325
    cfg.qr_mag = 2
    customtxt = list()
    txt = re.split("\n",txt)
    for x in (txt):
        if x == "":
            continue
        customtxt.append(x)
    if qr == "":
        txtPrint(quant,"*custom text label*",tuple(customtxt))
    else:
        QRPrint(qr,quant,"*custom QR label*",tuple(customtxt))

def con_update():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("data/con_print.ini")
    #Get the PRINTER section
    printer = config_object["PRINTER"]
    #Update the printer
    printer["printer_select"] = cfg.printer_select.get()
    #Get the TAG-TYPE section
    tag = config_object["TAG-TYPE"]
    #Update the tag
    tag["tag_select"] = str(cfg.tag_select.get())
    flag = config_object["FLAGS"]
    flag["flag_1"] = str(cfg.flag_1)
    flag["flag_2"] = str(cfg.flag_2)

    #Write changes back to file
    with open('data/con_print.ini', 'w') as conf:
        config_object.write(conf)

# ==========================================
# ============== Config Parser =============
# ==========================================

try:
    os.makedirs("data", exist_ok=True)
    #Get the configparser object and read file
    config_object = ConfigParser()
    config_object.read("data/con_print.ini")
    # Get the settings
    printer = config_object["PRINTER"]
    tag = config_object["TAG-TYPE"]
    flag = config_object["FLAGS"]
    # parse the settings
    print_1 = str(format(printer["printer_select"]))
    cfg.printer_select.set(print_1)
    local_1 = str(format(printer["local_print"]))
    cfg.local_print.set(local_1)
    tag_1 = int(tag["tag_select"])
    cfg.tag_select.set(tag_1)
    flag_1a = int(flag["flag_1"]) # 1 = Config printer, 2 = Mezz Printer, 0 = All printers
    cfg.flag_1 = flag_1a
    flag_2a = str(flag["flag_2"]) # 0 = No dev tools, homebuild = dev tools
    cfg.flag_2 = flag_2a

except:
    #Get the configparser object and create file
    config_object = ConfigParser()
    config_object["PRINTER"] = {
        "printer_select": cfg.printer_select.get(),
        "local_print": cfg.local_print.get()}
    config_object["TAG-TYPE"] = {
        "tag_select": cfg.tag_select.get()}
    config_object["FLAGS"] = {
        "flag_1": cfg.flag_1,
        "flag_2": cfg.flag_2}
    with open('data/con_print.ini', 'w') as conf:
        config_object.write(conf)

# # ==========================================
# # ================= Classes ================
# # ==========================================

class Dominos(tk.Tk):
    # enter store number
    # each has a unique ip address
    # 2x VM Hosts
    # 8x Thin Clients
    # 2x Label Printer
    # 1x Receipt printer
    # 1x Office Printer
    # 1x Cash Drawer
    def __init__(self, y):
        self.setupDom = y
        self.bname = tk.Button(master=tab5b,
                        text="Dominos",
                        command=self.bfunc,
                        width=20)
        self.bname.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
        if cfg.x_col >= 2:
            cfg.y_row += 1
            cfg.x_col = 0
        else:
            cfg.x_col += 1
        return

    def bfunc(self):
        def entry_window():
            cfg.dom_col = 0
            cfg.dom_row = 2
            store = tk.StringVar(None,"")
            enter_box = tk.Toplevel()
            enter_box.title("Dominos")
            enter_frame1 = tk.Frame(master=enter_box)
            enter_frame1.grid(row=4, column=0, columnspan=8, sticky=EW, pady=20, padx=20)
            border = ttk.Separator(master=enter_box,orient='horizontal')
            border.grid(row=3, column=0, columnspan=20, sticky=EW)
            
            def printDom():
                try:
                    storeid = store.get()
                    if (int(storeid) < 4999 or int(storeid) > 100000):
                        messagebox.showinfo("Dominos","Store ID is required and\nshould be 5 digits long")
                    else:
                        print(storeid)
                        for widget in enter_frame1.winfo_children():
                            if isinstance(widget, tk.Label):
                                print("1")
                                xy = (widget.cget("text"))
                                if xy.startswith("HOST"):
                                    xyz = ("VM " + storeid + " " + xy)
                                elif xy.startswith("CL"):
                                    try:
                                        abc = re.split("(\d+)", xy)
                                        xyz = (abc[0] + storeid + abc[1])
                                    except Exception as e:
                                        print(e)
                                else:
                                    xyz = xy
                            print("2")
                            if isinstance(widget, tk.Entry):
                                if widget.get() != "":
                                    zyx = widget.get()
                                    newText = (xyz,zyx)
                                    txtPrint(1,"Dominos Labels",newText)
                                    print("3")
                except Exception as e:
                    print(e)

            def selectDom():
                try:
                    for widget in enter_frame1.winfo_children():
                        if isinstance(widget, tk.Checkbutton):
                            widget.select()
                except:
                    pass

            def clearDom():
                try:
                    for widget in enter_box.winfo_children():
                        if isinstance(widget, tk.Entry):
                            widget.delete(0, END)
                    for widget in enter_frame1.winfo_children():
                        if isinstance(widget, tk.Entry):
                            widget.delete(0, END)
                        elif isinstance(widget, tk.Checkbutton):
                            widget.deselect()
                except:
                    pass

            store_label = tk.Label(master=enter_box,
                                    text="Enter store number",
                                    font=("calibri", 14))
            store_label.grid(row=0, column=0, pady=(10,0))
            store_entry = tk.Entry(master=enter_box,
                                    textvariable=store,
                                    width=15)
            store_entry.grid(row=1, column=0, pady=(0,10), padx=10)

            ip_label = tk.Label(master=enter_box,
                                text="Enter IP addresses below",
                                font=("calibri", 14))
            ip_label.grid(row=1, column=1, pady=10, padx=15)

            dom_select = tk.Button(master=enter_box,
                                text="Select all",
                                command=selectDom,
                                width=15)
            dom_select.grid(row=0, column=1, padx=10)

            dom_clear = tk.Button(master=enter_box,
                                text="Clear all",
                                command=clearDom,
                                width=15)
            dom_clear.grid(row=0, column=2, padx=10)

            dom_print = tk.Button(master=enter_box,
                                text="Print Labels",
                                command=printDom,
                                width=15)
            dom_print.grid(row=1, column=2, padx=10)

            class host():
                def __init__(self,x) -> None:
                    domlabel = tk.Label(master=enter_frame1,
                                            text=x)
                    domlabel.grid(column=cfg.dom_col, row=cfg.dom_row, sticky=E, padx=5, pady=(10,0))
                    self.cb = IntVar(value=1)
                    domenter = tk.Checkbutton(master=enter_frame1, variable=self.cb)
                    domenter.grid(column=cfg.dom_col+1, row=cfg.dom_row, padx=5, pady=(0,10), sticky=W)
                    cfg.dom_row += 1

            class client():
                def __init__(self,x) -> None:
                    domlabel = tk.Label(master=enter_frame1,
                                            text=x)
                    domlabel.grid(column=cfg.dom_col, row=cfg.dom_row, sticky=E, padx=5, pady=(10,0))
                    self.x = 1
                    domenter = tk.Checkbutton(master=enter_frame1)
                    domenter.grid(column=cfg.dom_col+1, row=cfg.dom_row, padx=5,pady=(0,10), sticky=W)
                    cfg.dom_row += 1

            class label():
                def __init__(self,x) -> None:
                    domlabel = tk.Label(master=enter_frame1,
                                            text=x)
                    domlabel.grid(column=cfg.dom_col, row=cfg.dom_row, sticky=E, padx=5, pady=(10,0))
                    self.x = 1
                    domenter = tk.Checkbutton(master=enter_frame1)
                    domenter.grid(column=cfg.dom_col+1, row=cfg.dom_row, padx=5,pady=(0,10), sticky=W)
                    cfg.dom_row += 1

            class receipt():
                def __init__(self,x) -> None:
                    domlabel = tk.Label(master=enter_frame1,
                                            text=x)
                    domlabel.grid(column=cfg.dom_col, row=cfg.dom_row, sticky=E, padx=5, pady=(10,0))
                    if cfg.receiptCount == 0:
                        domenter = tk.Entry(master=enter_frame1, width=15)
                        domenter.grid(column=cfg.dom_col+1, row=cfg.dom_row, padx=5,pady=(0,10), sticky=W)
                        cfg.receiptCount += 1
                    else:
                        self.x = 1
                        domenter = tk.Checkbutton(master=enter_frame1)
                        domenter.grid(column=cfg.dom_col+1, row=cfg.dom_row, padx=5,pady=(0,10), sticky=W)
                    cfg.dom_row += 1

            class office():
                def __init__(self,x) -> None:
                    domlabel = tk.Label(master=enter_frame1,
                                            text=x)
                    domlabel.grid(column=cfg.dom_col, row=cfg.dom_row, sticky=E, padx=5, pady=(10,0))
                    if cfg.officeCount == 0:
                        domenter = tk.Entry(master=enter_frame1, width=15)
                        domenter.grid(column=cfg.dom_col+1, row=cfg.dom_row, padx=5,pady=(0,10), sticky=W)
                        cfg.officeCount += 1
                    else:
                        self.x = 1
                        domenter = tk.Checkbutton(master=enter_frame1)
                        domenter.grid(column=cfg.dom_col+1, row=cfg.dom_row, padx=5,pady=(0,10), sticky=W)
                    cfg.dom_row += 1

            class cash():
                def __init__(self,x) -> None:
                    domlabel = tk.Label(master=enter_frame1,
                                            text=x)
                    domlabel.grid(column=cfg.dom_col, row=cfg.dom_row, sticky=E, padx=5, pady=(10,0))
                    self.x = 1
                    domenter = tk.Checkbutton(master=enter_frame1)
                    domenter.grid(column=cfg.dom_col+1, row=cfg.dom_row, padx=5,pady=(0,10), sticky=W)
                    cfg.dom_row += 1

            for x in self.setupDom:
                if cfg.dom_row >= 11:
                    cfg.dom_col += 2
                    cfg.dom_row = 2
                y = self.setupDom[x]
                if x.startswith("host"):
                    host(y)
                elif x.startswith("client"):
                    client(y)
                elif x.startswith("label"):
                    label(y)
                elif x.startswith("receipt"):
                    receipt(y)
                elif x.startswith("office"):
                    office(y)
                elif x.startswith("cash"):
                    cash(y)

            selectDom()

        try:
            for widget in root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
        except:
            pass
        entry_window()

class McDonald(tk.Tk):
    # store = tk.StringVar(None,"")
    # sord = tk.StringVar(None,"")
    # shipDate = tk.StringVar(None,"")
    def __init__(self, y):
        self.setupMcD = y
        
        self.bname = tk.Button(master=tab5b,
                        text="McDonalds",
                        command=self.bfunc,
                        width=20)
        self.bname.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
        if cfg.x_col >= 2:
            cfg.y_row += 1
            cfg.x_col = 0
        else:
            cfg.x_col += 1
        return


    def bfunc(self):
        def entry_window():
            cfg.screen_row = 2
            cfg.soc_row = 2
            cfg.kvs_row = 2
            cfg.group_row = 2
            store = tk.StringVar(None,"")
            sord = tk.StringVar(None,"")
            shipDate = tk.StringVar(None,"")
            enter_box = tk.Toplevel()
            # enter_box.geometry('750x600')
            enter_box.title("McDonalds Project Labels")
            enter_frame1 = tk.Frame(master=enter_box)
            enter_frame1.grid(row=2, column=0, columnspan=3)
            border = ttk.Separator(master=enter_frame1,orient='horizontal')
            border.grid(row=1, column=0, columnspan=4, sticky=EW)
            mcdlabel1 = tk.Label(master=enter_frame1, text="Screens")
            mcdlabel1.grid(row=0, column=0)
            mcdlabel2 = tk.Label(master=enter_frame1, text="SoCs")
            mcdlabel2.grid(row=0, column=1)
            mcdlabel3 = tk.Label(master=enter_frame1, text="KVS")
            mcdlabel3.grid(row=0, column=2)
            mcdlabel4 = tk.Label(master=enter_frame1, text="Groups")
            mcdlabel4.grid(row=0, column=3)
            # Enter Store number
            # Enter SORD
            # Enter ship date
            # Select MPs
            # Select SoCs
            # or select from defaults (ODMB, COTF etc)
            # Print 25mm labels
            # Print 65mm labels
            """
            config parse the custom_buttons.ini
            [McD]/[SBucks] will be used to initiate the button in the main app
            then the variables will define the screens and socs
            groups will need more consideration but should be doable all the same
            screen1 = BackOfBar 1
            screen2 = DailyOrderBoard 1
            soc1 = BackOfBar 1 SOC
            soc2 = DailyOrderBoard 1 SOC
            group1 = ODmB
            group1a = screen1, screen2, soc1, soc2
            """
            def an_print():
                print(store.get())
                print(sord.get())
                print(date_entry.get_date())
            
            class mcdscreen():
                def __init__(self,x) -> None:
                    mcdlabel = tk.Checkbutton(master=enter_frame1,
                                            text=x)
                    mcdlabel.grid(column=0, row=cfg.screen_row, sticky=W, padx=5)
                    cfg.screen_row += 1
            
            class mcdsoc():
                def __init__(self,x) -> None:
                    mcdlabel = tk.Checkbutton(master=enter_frame1,
                                            text=x)
                    mcdlabel.grid(column=1, row=cfg.soc_row, sticky=W, padx=5)
                    cfg.soc_row += 1
                
            class mcdkvs():
                def __init__(self,x) -> None:
                    mcdlabel = tk.Checkbutton(master=enter_frame1,
                                            text=x)
                    mcdlabel.grid(column=2, row=cfg.kvs_row, sticky=W, padx=5)
                    cfg.kvs_row += 1
                
            class mcdgroup():
                def __init__(self,x) -> None:
                    mcdlabel = tk.Button(master=enter_frame1,
                                            text=x,
                                            width=20)
                    mcdlabel.grid(column=3, row=cfg.group_row, sticky=W, padx=5)
                    cfg.group_row += 1
                
            store_label = tk.Label(master=enter_box,
                                    text="Enter store number",
                                    font=("calibri", 14))
            store_label.grid(row=0, column=0, pady=10)
            store_entry = tk.Entry(master=enter_box,
                                    textvariable=store,
                                    width=15)
            store_entry.grid(row=1, column=0)

            sord_label = tk.Label(master=enter_box,
                                    text="Enter SORD number",
                                    font=("calibri", 14))
            sord_label.grid(row=0, column=1, pady=10)
            sord_entry = tk.Entry(master=enter_box,
                                    textvariable=sord,
                                    width=15)
            sord_entry.grid(row=1, column=1)

            date_label = tk.Label(master=enter_box,
                                    text="Enter ship date",
                                    font=("calibri", 14))
            date_label.grid(row=0, column=2, pady=10)
            date_entry = DateEntry(master=enter_box,
                                    selectmode='day',
                                    date_pattern='dd/mm/y')
            date_entry.grid(row=1, column=2)

            for x in self.setupMcD:
                y = self.setupMcD[x]
                if x.startswith("screen"):
                    mcdscreen(y)
                elif x.startswith("soc"):
                    mcdsoc(y)
                elif x.startswith("kvs"):
                    mcdkvs(y)
                elif x.startswith("group"):
                    mcdgroup(y)

            enter_print = tk.Button(master=enter_box,
                                    text="Print",
                                    command=an_print)
            enter_print.grid(row=3, column=0)
        
        try:
            for widget in root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
        except Exception as e:
            print(e)
        entry_window()

class button(tk.Tk):
    def __init__(self, y):
        self.bname = y["button_name"]
        self.bhistory = y["history"]
        self.btype = y["btn_type"]
        self.bcode = y["code"]
        self.btext = y["text"]

        self.bname = tk.Button(master=tab5b,
                        text=self.bname,
                        command=self.bfunc,
                        width=20)
        self.bname.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
        if cfg.x_col >= 2:
            cfg.y_row += 1
            cfg.x_col = 0
        else:
            cfg.x_col += 1
        return

    def bfunc(self):
        if int(self.btype) != 2:
            self.newText = tuple(self.btext.split('$2'))
        else:
            self.newText = str(self.btext)
        cust_print(int(self.btype),str(self.bhistory),self.bcode,self.newText)

class button2(tk.Tk):
    def __init__(self, y):
        self.btnData = y
        self.bname = self.btnData["button_name"]
        self.bname2 = str(self.bname)
        self.bhistory = self.btnData["history"]
        self.btype = self.btnData["btn_type"]
        self.tags = []
        self.bname = tk.Button(master=tab5b,
                        text=self.bname,
                        command=self.bfunc,
                        width=20)
        self.bname.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
        if cfg.x_col >= 2:
            cfg.y_row += 1
            cfg.x_col = 0
        else:
            cfg.x_col += 1
        return

    def bfunc(self):
        def entry_window():
            cfg.btnCol = 0
            cfg.btnRow = 2
            uid = tk.StringVar(None,"")
            enter_box = tk.Toplevel()
            # enter_box.geometry('350x500')
            enter_box.title(str(self.bname2))
            enter_frame1 = tk.Frame(master=enter_box)
            enter_frame1.grid(row=4)
            if self.btnData.get("UID"):
                uid_label = tk.Label(master=enter_box,
                                    text=self.btnData["UID"],
                                    font=("calibri", 14))
                uid_label.grid(column=0, row=0)
                uid_entry = tk.Entry(master=enter_box,
                                        textvariable=uid,
                                        width=15)
                uid_entry.grid(row=1, column=0, pady=(0,10), padx=10)

            def selectAll():
                try:
                    for widget in enter_frame1.winfo_children():
                        if isinstance(widget, tk.Checkbutton):
                            widget.select()
                except:
                    pass

            def clearAll():
                try:
                    for widget in enter_box.winfo_children():
                        if isinstance(widget, tk.Entry):
                            widget.delete(0, END)
                    for widget in enter_frame1.winfo_children():
                        if isinstance(widget, tk.Entry):
                            widget.delete(0, END)
                        elif isinstance(widget, tk.Checkbutton):
                            widget.deselect()
                except:
                    pass

            allSelect = tk.Button(master=enter_box,
                                text="Select all",
                                command=selectAll,
                                width=15)
            allSelect.grid(row=0, column=1, padx=10)

            allClear = tk.Button(master=enter_box,
                                text="Clear all",
                                command=clearAll,
                                width=15)
            allClear.grid(row=0, column=2, padx=10)

            class btnCheckBox():
                def __init__(self,x) -> None:
                    named = x[:]
                    if "{}" in named:
                        named = named.format(uid.get())
                    btnCheck = tk.Checkbutton(master=enter_frame1,
                                            text=named)
                    btnCheck.grid(column=cfg.btnCol, row=cfg.btnRow, sticky=W, padx=5)
                    cfg.btnRow += 1

            class btnEntryBox():
                def __init__(self,x) -> None:
                    named = x[:]
                    if "{}" in named:
                        named = named.format(uid.get())
                    btnLabel = tk.Label(master=enter_frame1,
                                        text=named)
                    btnLabel.grid(column=cfg.btnCol, row=cfg.btnRow, padx=5, pady=(10,0))
                    self.x = 1
                    btnEnter = tk.Entry(master=enter_frame1)
                    btnEnter.grid(column=cfg.btnCol+1, row=cfg.btnRow, padx=5,pady=(0,10), sticky=W)
                    cfg.btnRow += 1

            for x in self.btnData:
                z = str(x)
                if z.startswith("check"):
                    btnCheckBox(self.btnData[z])
                elif z.startswith("enter"):
                    btnEntryBox(self.btnData[z])

            def an_print():
                pass

            entry_quant_label = tk.Label(master=enter_box, text="Enter number of labels to print")
            entry_quant_label.grid(column=0, row=5, pady=(35,0), padx=30)
            entry_quantities = tk.Spinbox(master=enter_box, from_=1, to=999,
                                        textvariable=cfg.cust_quantity)
            entry_quantities.grid(column=0, row=6, pady=(10,20))

            enter_print = tk.Button(master=enter_box,
                                    text="Print",
                                    command=an_print)
            enter_print.grid(column=1, row=6)
        
        try:
            for widget in root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
        except:
            pass
        entry_window()

class button3(tk.Tk):
    def __init__(self, y):
        self.qt = y
        self.bname = self.qt["button_name"]
        self.bname2 = str(self.bname)
        self.bhistory = self.qt["history"]
        self.btype = self.qt["btn_type"]
        self.tags = []
        self.bname = tk.Button(master=tab5b,
                        text=self.bname,
                        command=self.bfunc,
                        width=20)
        self.bname.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
        if cfg.x_col >= 2:
            cfg.y_row += 1
            cfg.x_col = 0
        else:
            cfg.x_col += 1
        return


    def bfunc(self):
        def entry_window():
            enter_box = tk.Toplevel()
            enter_box.geometry('350x500')
            enter_box.title(str(self.bname2))
            enter_frame1 = tk.Frame(master=enter_box)
            enter_frame1.pack()
            self.tags = []
            self.checks = []
            for x in self.qt:
                z = str(x)
                if z.startswith("enter"):
                    self.tags.append(self.qt[z])
                elif z.startswith("check"):
                    self.checks.append(self.qt[z])
                else:
                    pass
            for i in self.tags:
                enter = tk.Label(master=enter_frame1,text=i)
                enter.pack()
                dataEntry = tk.Entry(master=enter_frame1)
                dataEntry.pack()
                pass
            for i in self.checks:
                checkVar= tk.IntVar()
                check = tk.Checkbutton(master=enter_frame1,text=i,variable=checkVar)
                check.pack()

            def an_print():
                entries = []
                try:
                    for widget in enter_frame1.winfo_children():
                        if isinstance(widget, tk.Entry):
                            entries.append(widget.get())
                        elif isinstance(widget, tk.Checkbutton):
                            if checkVar.get() == 1:
                                print("Checkbox for ", widget)
                except Exception as e:
                    print(e)
                    print("Couldn't collate answers")
                
                try:
                    qty = cfg.cust_quantity.get()
                    newText = ()
                    checkText = ()
                    for x in range(len(self.tags)):
                        print(entries[x])
                        if entries[x] != "":
                            newText = (self.tags[x],entries[x])
                            
                            txtPrint(qty,str(self.bhistory),newText)
                        else:
                            pass
                except Exception as e:
                    print(e)

            entry_quant_label = tk.Label(master=enter_frame1, text="Enter number of labels to print")
            entry_quant_label.pack(pady=(35,0))
            entry_quantities = tk.Spinbox(master=enter_frame1, from_=1, to=999,
                                        textvariable=cfg.cust_quantity)
            entry_quantities.pack(pady=10)

            enter_print = tk.Button(master=enter_frame1,
                                    text="Print",
                                    command=an_print)
            enter_print.pack()
        
        try:
            for widget in root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
        except:
            pass
        entry_window()

class btn_bcu(tk.Tk): # special class just for BCU labels
    def __init__(self):
        self.bname = tk.Button(master=tab5b,
                        text="BCU",
                        command=self.bfunc,
                        width=20)
        self.bname.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
        if cfg.x_col >= 2:
            cfg.y_row += 1
            cfg.x_col = 0
        else:
            cfg.x_col += 1
        return

    def bfunc(self):
        def entry_window():
            enter_box = tk.Toplevel()
            enter_box.geometry('450x500')
            enter_box.title("BCU Labels")
            enter_frame1 = tk.Frame(master=enter_box)
            enter_frame1.pack()
            
            BCU_ID = tk.StringVar(None, "BCUL1-")
            BCU_ID.set("BCUL1-")

            def an_print():
                BCU_print = ""
                BCU_print += "^XA"
                BCU_print += "^LH5,5"
                BCU_print += "^FO10,30"
                BCU_print += "^A0N,40,40"
                BCU_print += "^FD"
                BCU_print += str(BCU_ID.get())
                BCU_print += bcu_asset_enter.get()
                BCU_print += "^FS"
                BCU_print += "^FO15,70,^BY2.1"
                BCU_print += "^B3N,N,60,Y,N" 
                BCU_print += "^FD"
                BCU_print += str(BCU_ID.get())
                BCU_print += bcu_asset_enter.get()
                BCU_print += "^FS"
                BCU_print += "^FO10,160"
                BCU_print += "^A0N,40,40"
                BCU_print += "^FD"
                BCU_print += "BCUPO:"
                BCU_print += bcu_po_enter.get()
                BCU_print += "^FS"
                BCU_print += "^FD"
                BCU_print += "^FS"
                BCU_print += "^FO10,220"
                BCU_print += "^A0N,40,40"
                BCU_print += "^FD"
                BCU_print += "SORD:"
                BCU_print += bcu_sord_enter.get()
                BCU_print += "^FS"
                BCU_print += "^FD"
                BCU_print += "^FS"
                BCU_print += "^FO10,270"
                BCU_print += "^A0N,40,40"
                BCU_print += "^FD"
                BCU_print += "ASSET TAG"
                BCU_print += "^FS"
                BCU_print += "^FO10,310,^BY2.1"
                BCU_print += "^B3N,N,60,Y,N"
                BCU_print += "^FD"
                BCU_print += bcu_asset_enter.get()
                BCU_print += "^PQ1"
                BCU_print += "^FS"
                BCU_print += "^XZ"
                bcu_asset_enter.delete(0, END)
                try:
                    chisel = open("LPT4", "w")
                    chisel.write(BCU_print)
                    chisel.close()
                    history("BCU Tag " + str(bcu_asset_enter.get()))
                except Exception as e:
                    print(e)
                print("BCU Tag " + bcu_asset_enter.get())

            bcu_head_label = tk.Label(master=enter_frame1,
                                    text="Please select your unit type")
            bcu_head_label.grid(row=0, column=0, columnspan=3)

            bcu_radio1 = tk.Radiobutton(master=enter_frame1,
                                        text="Staff Laptop (L1)",
                                        variable=BCU_ID,
                                        value="BCUL1-",
                                        font=("calibri", 14))
            bcu_radio1.grid(row=1, column=0, sticky=W)

            bcu_radio2 = tk.Radiobutton(master=enter_frame1,
                                        text="Staff Desktop (D1)",
                                        variable=BCU_ID,
                                        value="BCUD1-",
                                        font=("calibri", 14))
            bcu_radio2.grid(row=2, column=0, sticky=W)

            bcu_radio3 = tk.Radiobutton(master=enter_frame1,
                                        text="Staff Tablet (T1)",
                                        variable=BCU_ID,
                                        value="BCUT1-",
                                        font=("calibri", 14))
            bcu_radio3.grid(row=3, column=0, sticky=W)

            bcu_radio4 = tk.Radiobutton(master=enter_frame1,
                                        text="Student Laptop (L2)",
                                        variable=BCU_ID,
                                        value="BCUL2-",
                                        font=("calibri", 14))
            bcu_radio4.grid(row=1, column=1, sticky=W)

            bcu_radio5 = tk.Radiobutton(master=enter_frame1,
                                        text="Student Desktop (D2)",
                                        variable=BCU_ID,
                                        value="BCUD2-",
                                        font=("calibri", 14))
            bcu_radio5.grid(row=2, column=1, sticky=W)

            bcu_radio6 = tk.Radiobutton(master=enter_frame1,
                                        text="Student Tablet (T2)",
                                        variable=BCU_ID,
                                        value="BCUT2-",
                                        font=("calibri", 14))
            bcu_radio6.grid(row=3, column=1, sticky=W)

            bcu_radio7 = tk.Radiobutton(master=enter_frame1,
                                        text="Lecturn Desktop (D4)",
                                        variable=BCU_ID,
                                        value="BCUD4-",
                                        font=("calibri", 14))
            bcu_radio7.grid(row=4, column=0, columnspan=2)

            bcu_po_label = tk.Label(master=enter_frame1,
                                    text="Enter the order PO")
            bcu_po_label.grid(row=5, column=0, columnspan=2, pady=(20,0))

            bcu_po_enter = tk.Entry(master=enter_frame1)
            bcu_po_enter.grid(row=6, column=0, columnspan=2, pady=(0,20))

            bcu_sord_label = tk.Label(master=enter_frame1,
                                    text="Enter the SORD# (numbers only)")
            bcu_sord_label.grid(row=7, column=0, columnspan=2, pady=0)

            bcu_sord_enter = tk.Entry(master=enter_frame1)
            bcu_sord_enter.grid(row=8, column=0, columnspan=2, pady=(0,20))

            bcu_asset_label = tk.Label(master=enter_frame1,
                                    text="Enter the asset tag")
            bcu_asset_label.grid(row=9, column=0, columnspan=2, pady=0)

            bcu_asset_enter = tk.Entry(master=enter_frame1)
            bcu_asset_enter.grid(row=10, column=0, columnspan=2, pady=(0,20))

            enter_print = tk.Button(master=enter_frame1,
                                    text="Print",
                                    command=an_print)
            enter_print.grid(row=11, column=0, columnspan=2)

        try:
            for widget in root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
        except:
            pass
        entry_window()   

class new_date_test():
    def __init__(self):
        self.bname = tk.Button(master=tab5b,
                        text="Day of week",
                        command=self.bfunc,
                        width=20)
        self.bname.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
        if cfg.x_col >= 2:
            cfg.y_row += 1
            cfg.x_col = 0
        else:
            cfg.x_col += 1
        return
        
    def bfunc(self):
        from datetime import date
        from calendar import day_name
        qty = cfg.cust_quantity.get()
        day = (date.today().weekday())
        thisWeekday = day_name[day]
        print_me = []
        print_me.append(thisWeekday)
        txtPrint(qty,"Date",print_me)

trial = ConfigParser()
trial.read("data/custom_buttons.ini")
for x in trial:
    if x == "DEFAULT":
        continue
    elif x == "date":
        new_date_test()
        continue
    elif x == "McD":
        McDonald(trial[x])
        continue
    # elif x == "Dominos":
    #     Dominos(trial[x])
    #     continue
    y = trial[x]
    btype = y["btn_type"]
    if btype == "5":
        button3(y)
        # button2(y)
        continue
    elif btype == "6":
        btn_bcu()
        continue
    else:
        button(y)


tryout = ConfigParser()
tryout.read("data/custom_buttons.ini")

# ==========================================
# =============== Title header =============
# ==========================================

try:
    logo_img = ImageTk.PhotoImage(Image.open("data/CDW_Logo.png").resize((100, 60)))
    logo = Label(frametop1, image=logo_img)
    logo.pack(side=LEFT, anchor=W, padx=15, pady=10)
except:
    logo_text = tk.Label(frametop1, text="CDW", font=("Helvetica",20))
    logo_text.pack(side=LEFT, anchor=W, padx=10, pady=10)
app_title = tk.Label(frametop2, text="Config General Printing Application", font=("Helvetica",30)).pack(side=TOP)
help_button = tk.Button(master=frametop3, text="?", font=('Helvetica',20), command=help_me).pack(padx=(0,10))
try:
    # cog_icon = ImageTk.PhotoImage(Image.open("data/cogwheel.png").resize((25, 25)))
    cog_icon = ImageTk.PhotoImage(Image.open("data/print_history.png").resize((25, 25)))
    cog = tk.Button(master=frametop3, image=cog_icon, borderwidth=0, command=set_config)
    cog.pack(padx=(0,8), pady=(5,0))    
except:
    cog = tk.Button(master=frametop3, text="...", font=("Helvetica",14), command=set_config).pack()

# ==========================================
# ======= Settings panel (frame1a) =========
# ==========================================

frame1.grid_rowconfigure((0,1,2,3,5,7,9,12), weight=1)
frame1.grid_rowconfigure((4,8,11), weight=8)
frame1.grid_columnconfigure(0, weight=1)

printer_label = tk.Label(master=frame1,
                            text="Select printer:")
printer_label.grid(row=0, sticky=W, column=0, columnspan=2)

config_print_button = tk.Radiobutton(master=frame1,
                    text="Config Printer",
                    variable=cfg.printer_select,
                    value="LPT1",
                    command=con_update)
config_print_button.grid(row=1, sticky=W, column=0, columnspan=2)

config_print_button2 = tk.Radiobutton(master=frame1,
                    text="Config Alt Printer",
                    variable=cfg.printer_select,
                    value="LPT2",
                    command=con_update)
config_print_button2.grid(row=2, sticky=W, column=0, columnspan=2)

mezz_print_button = tk.Radiobutton(master=frame1,
                    text="MEZZ Printer",
                    variable=cfg.printer_select,
                    value="LPT7",
                    command=con_update)
mezz_print_button.grid(row=3, sticky=W, column=0, columnspan=2)

#row=4 is reserved for test printer

def reset_print():
    res = str("^MNY")
    to_print(res,"")

label_mod_label = tk.Label(master=frame1,
                            text="Printed position\noffset",
                            anchor="w",
                            justify=LEFT,
                            font=("calibri", 12))
label_mod_label.grid(row=5, column=0, sticky=W, pady=0)

label_mod_select = tk.Spinbox(master=frame1,
                                from_=-10,
                                to=10,
                                textvariable=cfg.label_mod,
                                increment=-1,
                                width=3)
label_mod_select.grid(row=5, column=1, pady=0)

label_mod_horizontal = tk.Scale(master=frame1,
                                from_=-10, to=20,
                                orient=HORIZONTAL,
                                variable=cfg.horz_label_mod)
label_mod_horizontal.grid(row=6, column=0, columnspan=2, pady=0)

textmod_label = tk.Label(master=frame1,
                                anchor="w",
                                justify=LEFT,
                                font=("calibri", 12),
                                text="Text size\nmodifier: ")
textmod_label.grid(row=7, column=0, pady=(0,20), padx= 10)

textmod = tk.Spinbox(master=frame1,
                            from_=-10,
                            to=10,
                            textvariable=cfg.textmod,
                            width=3)
textmod.grid(row=7, column=1, pady=(0,10), padx= 10)

asset_label = tk.Label(master=frame1,
                            text="Asset or serial?")
asset_label.grid(row=8, sticky=W, column=0, columnspan=2)

set_asset_button = tk.Radiobutton(master=frame1,
                    text="Asset tags",
                    variable=cfg.tag_select,
                    value=0,
                    command=set_tag)
set_asset_button.grid(row=9, sticky=W, column=0, columnspan=2)

set_serial_button = tk.Radiobutton(master=frame1,
                    text="Serial Numbers",
                    variable=cfg.tag_select,
                    value=1,
                    command=set_tag)
set_serial_button.grid(row=10, sticky=W, column=0, columnspan=2)

# row=11 reserved for dev reset button

# row=12 reserved for current version number

exit_button = tk.Button(master=frame1,
                    text="Quit",
                    command=quit,
                    width=12)
exit_button.grid(row=13, sticky=EW, column=0, columnspan=2)

# ==========================================
# =========== Singles Tab (tab1) ===========
# ==========================================

tab1.grid_columnconfigure((0,1),weight=1)
tab1.grid_rowconfigure((0,1,2,3,4),weight=1)
tab1.grid_rowconfigure((5),weight=9)

single_descript = tk.Label(master=tab1,
                        text="To print a single label",
                        font=12,
                        fg="blue")
single_descript.grid(row=0, column=0, columnspan=2)

single_label = tk.Label(master=tab1,
                        textvariable=cfg.asset_type)
single_label.grid(row=1, column=0, sticky=E)

single_entry = tk.Entry(master=tab1,
                        bg=cfg.bg_col)
single_entry.grid(row=1, column=1, sticky=W, padx=10)

single_btn = tk.Button(master=tab1,
                        text="Print",
                        width=10,
                        command=return_key)
single_btn.grid(row=2, column=0, columnspan=2, sticky=N)

serial_radio2 = tk.Label(master=tab1,
                        text="Device or custom serial number")
serial_radio2.grid(row=3, column=0, columnspan=2)

serial_radio1 = tk.Radiobutton(master=tab1,
                                text="Device (default)",
                                variable=cfg.device_label,
                                value="Device")
serial_radio1.grid(row=4, column=0, sticky=E)           

serial_radio3 = tk.Entry(master=tab1,
                        textvariable=cfg.device_label)
serial_radio3.grid(row=4, column=1, stick=W, padx=40)


# ==========================================
# =========== Groups Tab (tab2) ============
# ==========================================

group_label1 = tk.Label(master=tab2a,
                        font=12,
                        fg="blue",
                        text="Print a selection of labels")
group_label1.pack(side=TOP)

group_label = tk.Label(master=tab2a,
                        textvariable=cfg.asset_type)
group_label.pack(side=LEFT, pady=(20,0))

group_entry = tk.Entry(master=tab2a,
                        bg=cfg.bg_col)
group_entry.pack(side=LEFT, padx=10, pady=(20,0))

group_clear = tk.Button(master=tab2b,
                        text="Clear",
                        command=clear_all,
                        width=10)
group_clear.pack(side=LEFT)

group_print = tk.Button(master=tab2b,
                        text="Print",
                        command=print_group_text,
                        width=10)
group_print.pack(side=LEFT, padx=100)

group_load = tk.Button(master=tab2b,
                        text="Load from file",
                        command=open_file1)
group_load.pack(side=LEFT, padx=(0,100))

group_textbox = tkscrolled.ScrolledText(master=tab2c,
                                        wrap=WORD,
                                        height=12)
group_textbox.pack(fill=BOTH, expand=True, padx=30, pady=(5,20))

serial_radio2a = tk.Label(master=tab2d,
                        text="Device or custom serial number")
serial_radio2a.grid(row=1, column=0, columnspan=2)

serial_radio1a = tk.Radiobutton(master=tab2d,
                                text="Device (default)",
                                variable=cfg.device_label,
                                value="Device")
serial_radio1a.grid(row=2, column=0, sticky=E)           

serial_radio3a = tk.Entry(master=tab2d,
                        textvariable=cfg.device_label)
serial_radio3a.grid(row=2, column=1, stick=W, padx=40)

# ==========================================
# ============ Range Tab (tab3) ============
# ==========================================

range_label1 = tk.Label(master=tab3a,
                        font=12,
                        fg="blue",
                        text="Print a range of asset tags")
range_label1.grid(row=0, column=0, columnspan=2)

range_label2 = tk.Label(master=tab3a,
                        text="Enter the Prefix of the tag")
range_label2.grid(row=1, column=0, pady=(20,0))

range_entry2 = tk.Entry(master=tab3a,
                        textvariable=cfg.range_prefix)
range_entry2.grid(row=2, column=0)

range_label3 = tk.Label(master=tab3a,
                        text="Enter the Suffix of the tag")
range_label3.grid(row=1, column=1, pady=(20,0))

range_entry3 = tk.Entry(master=tab3a,
                        textvariable=cfg.range_suffix)
range_entry3.grid(row=2, column=1)

range_label4 = tk.Label(master=tab3a,
                        text="Enter the starting number of the range")
range_label4.grid(row=3, column=0, pady=(20,0), padx=10)

range_entry4 = tk.Entry(master=tab3a,
                        textvariable=cfg.range_start)
range_entry4.grid(row=4, column=0)

range_label5 = tk.Label(master=tab3a,
                        text="Enter the ending number of the range")
range_label5.grid(row=3, column=1, pady=(20,0), padx=10)

range_entry5 = tk.Entry(master=tab3a,
                        textvariable=cfg.range_end)
range_entry5.grid(row=4, column=1)

range_clear = tk.Button(master=tab3a,
                        text="Clear",
                        command=clear_all,
                        width=10)
range_clear.grid(row=5, column=0, pady=(20,0), padx=40, sticky=E)

range_print = tk.Button(master=tab3a,
                        text="Print",
                        command=print_range,
                        width=10)
range_print.grid(row=5, column=1, pady=(20,0), padx=40, sticky=W)

# ==========================================
# ========= Range-Auto Tab (tab4) ==========
# ==========================================

auto_label1a = tk.Label(master=tab4a,
                        font=12,
                        fg="blue",
                        text="Print a range of asset tags")
auto_label1a.pack(pady=(5,20))

auto_label1 = tk.Label(master=tab4a,
                        text="Scan the first and last tag in your range into the 2 boxes provided\nYou must use both boxes to enter your range\nDon't worry about what goes where, they both work the same")
auto_label1.pack()

auto_entry1 = tk.Entry(master=tab4a,
                        textvariable=cfg.auto_1)
auto_entry1.pack(pady=15)

auto_entry2 = tk.Entry(master=tab4a,
                        textvariable=cfg.auto_2)
auto_entry2.pack()

auto_clear = tk.Button(master=tab4b,
                        text="Clear",
                        command=clear_all,
                        width=10)
auto_clear.grid(row=0, column=1, padx=10)

auto_print = tk.Button(master=tab4b,
                        text="Print",
                        command=print_auto,
                        width=10)
auto_print.grid(row=0, column=2, padx=10)

warn_label = tk.Label(master=tab4c,
                        text="Check number of tags\n is correct before printing",
                        font=("Helvetica",14),
                        fg="dark red")
warn_label.pack(side=TOP, padx=40, pady=40)

# ==========================================
# ======== Customer label Tab (tab5) =======
# ==========================================

print_quantity_label = tk.Label(master=tab5a,
                            font=12,
                            fg="blue",
                            text="Enter quantity of labels required")
print_quantity_label.grid(row=0, column=1, pady=20, padx= 10)

print_quantity = tk.Spinbox(master=tab5a, from_=1, to=9999,
                            textvariable=cfg.cust_quantity,
                            width=4)
print_quantity.grid(row=0, column=2, pady=10, padx= 10)

# ==========================================
# ========== Reports Tab (tab6) ============
# ==========================================

# tab6a = tk.Frame(master=tab6)
# tab6a.pack(pady=20)
# tab6b = tk.Frame(master=tab6)
# tab6b.pack(pady=20)

# label_6a = tk.Label(master=tab6a,
#                     text="Less than 5 rolls of labels remaining?")
# label_6a.grid(row=0, column=0)

# labels_ribbon = tk.Checkbutton(master=tab6a,
#                             text="Also ribbons?")
# labels_ribbon.grid(row=1, column=1)

# labels_remain = tk.Spinbox(master=tab6a,
#                             from_=0,
#                             to=5,
#                             wrap=True)
# labels_remain.grid(row=0, column=1)

# labels_alert = tk.Button(master=tab6a,
#                         text="Report labels")
# labels_alert.grid(row=1, column=0)

# label_6b = tk.Label(master=tab6b,
#                     text="Faulty Network port:")
# label_6b.grid(row=1, column=0)

# label_6bb = tk.Label(master=tab6b,
#                     text="enter switch number and full port number (i.e. SW5 Gi2/0/4)")
# label_6bb.grid(row=0, column=0, columnspan=3)

# port_entry = tk.Entry(master=tab6b)
# port_entry.grid(row=1, column=2)

# ports_alert = tk.Button(master=tab6b,
#                         text="Report port")
# ports_alert.grid(row=2, column=2)

# label_6b = tk.Label(master=tab6b,
#                     text="Nothing works on this page yet so don't waste your time",
#                     font=38,
#                     fg="red")
# label_6b.grid(row=5, column=0, columnspan=4, rowspan=2)


# ==========================================
# =========== Custom Tab (tab7) ============
# ==========================================

custom_label1 = tk.Label(master=tab7a,
                        font=12,
                        fg="blue",
                        text="To print plain text and/or QR codes")
custom_label1.pack(side=TOP)

custom_label = tk.Label(master=tab7a,
                        text="QR Code: ")
custom_label.pack(side=LEFT, pady=(10,0))

custom_qr = tk.Entry(master=tab7a,
                    width=70)
custom_qr.pack(side=LEFT, padx=10, pady=(10,0))

custom_clear = tk.Button(master=tab7b,
                        text="Clear QR Code",
                        command=clear_custom_qr,
                        width=15)
custom_clear.pack(side=LEFT, padx=(20,0))

custom_print = tk.Button(master=tab7b,
                        text="Print one",
                        command=print_custom_one,
                        width=10)
custom_print.pack(side=LEFT, padx=20)

custom_print_many = tk.Button(master=tab7b,
                        text="Print many",
                        command=print_custom_many,
                        width=10)
custom_print_many.pack(side=LEFT, padx=0)

custom_load = tk.Button(master=tab7b,
                        text="Clear all",
                        command=clear_all,
                        width=10)
custom_load.pack(side=LEFT, padx=20)

custom_load = tk.Button(master=tab7b,
                        text="Load from file",
                        command=open_file2)
custom_load.pack(side=LEFT, padx=(0,20))

def on_tab_change(event): # Reset text and QR printing when moving away from custom prints
    # tab_name = frame2.select()
    # tab_index = frame2.index(tab_name)
    # if tab_index != 5:
    cfg.textmod.set(0)
    custom_no_bc.config(text="Text&QR: All on 1 label", bg="#555555")
    cfg.no_bc.set(False)
    clear_all()

def no_bc_toggle():
    if custom_no_bc.config('text')[-1] == "Text&QR: All on 1 label":
        custom_no_bc.config(text="Text: 1 line per label",bg="#DD0033")
        cfg.no_bc.set(True)
    else:
        custom_no_bc.config(text="Text&QR: All on 1 label", bg="#555555")
        cfg.no_bc.set(False)

custom_no_bc = tk.Button(master=tab7c,
                            text="Text&QR: All on 1 label",
                            command=no_bc_toggle,
                            width=20,
                            bg="#555555",
                            fg="#f0f0f0")
custom_no_bc.pack(side=LEFT, pady=5)

custom_quantity_label = tk.Label(master=tab7c,
                            text="Print quantity")
custom_quantity_label.pack(padx=10, side=LEFT)

custom_quantity = tk.Spinbox(master=tab7c,
                            from_=1,
                            to=9999,
                            textvariable=cfg.cust_quantity,
                            width=4)
custom_quantity.pack(padx=10, side=LEFT)

custom_textbox = tkscrolled.ScrolledText(master=tab7,
                                        wrap=WORD,
                                        width=60,
                                        height=10)
custom_textbox.pack(side=TOP, padx=5, pady=(10,30))


# =====================================
# ==== Generate external file list ====
# =====================================
# Step 1, add list of files, include short description, '\n' on end to input new line
files = ""
files += "data/8dheowme.mp3           # misc audio file\n"
files += "data/8d82b51.mp3            # misc audio file\n"
files += "data/8d82b52.mp3            # misc audio file\n"
files += "data/bbc.png                # to print the BBC logo\n"
files += "data/CDW_icon.png           # CDW icon for top left corner of app\n"
files += "data/CDW_Logo.png           # display CDW logo in app\n"
files += "data/con_print.ini          # holds ini settings for program\n"
files += "data/cogwheel.png           # settings icon in app\n"
files += "data/cust_helper.jpg        # Help image for customer tab (320x600)\n"
files += "data/custom_buttons.ini     # hold customer button information\n"
files += "data/custom_buttons_read.me # guide to write customer_button.xml\n"
files += "data/custom_helper.jpg      # Help image for custom tab (320x600)\n"
files += "data/groups_helper.jpg      # Help image for groups tab (320x600)\n"
files += "data/logs.txt               # list of previously printed labels\n"
files += "data/range_auto_helper.jpg  # Help image for range auto tab (320x600)\n"
files += "data/range_helper.jpg       # Help image for range tab (320x600)\n"
files += "data/reports_helper.jpg     # Help image for reports tab (320x600)\n"
files += "data/single_helper.jpg      # Help image for singles tab (320x600)\n"

# Step 2, name your file
file_list = "data/filelist.txt"
# Step 3, Open file. "w" sets file to be freshly overwritten
File1 = open(file_list, "w")
# Step 4, Save list of files to newly opened file
File1.write(files)
# Step 5, close file
File1.close()

# ===============================
# ========== Tooltips ===========
# ===============================

# from idlelib.tooltip import Hovertip
    
# myTip = Hovertip(tab3,'This is \na multiline tooltip.')



# ===============================
# ========= Dev Tools ===========
# ===============================

if flag_2a == "homebuild":
    reset_button = tk.Button(master=frame1,
                        text="Restart App",
                        command=reset,
                        width=12)
    reset_button.grid(row=11, sticky=EW, column=0, columnspan=2)

    test_print_button = tk.Radiobutton(master=frame1,
                        text="Test Printer",
                        value="local",
                        variable=cfg.printer_select,
                        command=con_update)
    test_print_button.grid(row=4, sticky=W, column=0, columnspan=2)

# ==========================================
# ======== Current version number ==========
# ==========================================

version_label = tk.Label(master=frame1,
                            text="Version 1.1.19",
                            font=("courier new", 10))
version_label.grid(row=12, sticky=EW, column=0, columnspan=2)

# ==========================================
# ========= Start up the routine ===========
# ==========================================

try:
    set_tag()
except:
    pass
root.bind('<Return>', return_key)
root.bind('<Control-p>', ctrl_p)
root.bind('<Control-P>', ctrl_p)
frame2.bind('<<NotebookTabChanged>>',on_tab_change)
auto_entry1.bind('<Return>', return_auto1)
auto_entry2.bind('<Return>', return_auto2)

root.mainloop()
