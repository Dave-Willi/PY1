# pip installs used by this script, incomplete
# playsound 1.2.2
# pillow
# pywin32
# configparser

# imports.... so many imports 
import os
import subprocess
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Notebook
from PIL import Image, ImageTk
from configparser import ConfigParser
import tkinter.scrolledtext as tkscrolled
import re
from time import sleep

self = tk.Tk()
self.title("Config printing app")

w = 780 # width for the Tk root
h = 520 # height for the Tk root

# ==========================================
# ============ Position window =============
# ==========================================

# get screen width and height
ws = self.winfo_screenwidth() # width of the screen
hs = self.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
self.geometry('%dx%d+%d+%d' % (w, h, x, y))
self.resizable(False,False)

# ***************************************************************
# cfg holds global variables. Must import AFTER initiating window
# ***************************************************************
import cfg

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

frametop = tk.Frame(self,
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
frametop3.pack(side=RIGHT) #frametop3 before frametop2 to keep it on the right

frametop2 = tk.Frame(frametop,
                    height=80,
                    width=680)
frametop2.pack(side=RIGHT)
frametop2.place(relx=0.25, y=15)

frame1 = tk.Frame(self,
                height=490,
                width=200)
frame1.pack(padx=10, pady=10, anchor=W, fill=Y, expand=False, side=LEFT)

frame2 = Notebook (self, 
                    height=470,
                    width=680,)
frame2.pack(padx=10,pady=10, anchor=E, fill=BOTH, expand=True, side=RIGHT)

frame1.grid_rowconfigure((0,1,2,5,6,7,9,10), weight=1)
frame1.grid_rowconfigure((3,4,8), weight=8)
frame1.grid_columnconfigure(0, weight=1)


# ==========================================
# ================= Tabs ===================
# ==========================================
# additional frames created inside tabs for formatting

tab1 = tk.Frame(frame2) # singles
tab2 = tk.Frame(frame2) # groups
tab2a = tk.Frame(tab2)
tab2b = tk.Frame(tab2)
tab3 = tk.Frame(frame2) # range
tab3a = tk.Frame(tab3)
tab4 = tk.Frame(frame2) # range auto
tab4a = tk.Frame(tab4)
tab4b = tk.Frame(tab4)
tab4c = tk.Frame(tab4)
tab5 = tk.Frame(frame2) # customer labels
tab6 = tk.Frame(frame2) # reports
tab7 = tk.Frame(frame2) # custom labels
tab7a = tk.Frame(tab7)
tab7aa = tk.Frame(tab7)
tab7ab = tk.Frame(tab7)
tab7b = tk.Frame(tab7)
tab7c = tk.Frame(tab7)
frame2.add(tab1, text = "Singles")
frame2.add(tab2, text = "Groups")
frame2.add(tab3, text = "Range")
frame2.add(tab4, text = "Range (Auto)")
frame2.add(tab5, text = "Customer Labels")
frame2.add(tab6, text = "Reports", state=DISABLED)
frame2.add(tab7, text = "Custom Labels")

tab2a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab2b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab3a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab4a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10, fill=BOTH)
tab4b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab4c.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10, fill=BOTH)
tab7a.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab7aa.pack(anchor=CENTER, expand=False, side=TOP)
tab7ab.pack(anchor=CENTER, expand=False, side=TOP)
tab7b.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)
tab7c.pack(anchor=CENTER, expand=False, side=TOP, pady=10, padx=10)

# **********************************************
# import external functions after setting frames
# **********************************************
from conFuncs import quit, set_print, BCPrint, print_auto, BBC, ebay_mac, ebay_PC, txtPrint, QRPrint


# ==========================================
# =========== Side menu commands ===========
# ==========================================
# definitions required for the buttons on the left side menu to function

def reset(): # stop and restart app. Can be disabled for final release
    self.destroy()
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

def set_tag(): # Change between asset tag and serial number. Sets colour of entry box as an added hint for which is selected. Disable range tabs in serial number mode.
    if cfg.tag_select.get() == 0:
        cfg.asset_type.set("Asset Tag :")
        frame2.tab(2, state="normal")
        frame2.tab(3, state="normal")
        bg_col = "#eef"
    elif cfg.tag_select.get() == 1:
        cfg.asset_type.set("Serial Number :")
        frame2.tab(2, state="disabled")
        frame2.tab(3, state="disabled")
        bg_col = "#fee"
    try:
        single_entry.config(bg=bg_col)
        group_entry.config(bg=bg_col)
        if flag_1 == 1:
            mezz_print_button.configure(state=DISABLED)
            config_print_button.configure(state=NORMAL)
        elif flag_1 == 2:
            config_print_button.configure(state=DISABLED)
            mezz_print_button.configure(state=NORMAL)
        elif flag_1 == 0:
            mezz_print_button.configure(state=NORMAL)
            config_print_button.configure(state=NORMAL)
    except:
        pass
    con_update()

def help_me(): # Set custom help dialog boxes for each page/tab
    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    set_config(tab_index)


def set_config(tab=""): # additional window with extra info such as print log
    omni_box = Toplevel(self)
    omni_box.title("Settings and about")
    omni_box.overrideredirect(True)

    def kill_me(): # closes the extra window
        omni_box.destroy()

    w = 300 # width for the Tk root
    h = 500 # height for the Tk root

    # get screen width and height
    ws = self.winfo_screenwidth() # width of the screen
    hs = self.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) + (400)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    omni_box.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Close config window on lose focus
    omni_box.focus_force()
    omni_box.bind('<FocusOut>', lambda x:kill_me())

    # Fill the config window with stuff
    if tab == "":
        # ==========================================
        # ====== Display config file contents ======
        # ==========================================

        label2 = tk.Label(omni_box,
                        text="Settings saved in the config file")
        label2.pack(side=TOP)                    

        config_text = tk.Text(omni_box, wrap=WORD, width=34, height=7, state=DISABLED)
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

        # =======================================================
        # ===== Display last 100 tags printed from log file =====
        # =======================================================

        label3 = tk.Label(omni_box,
                        text="The last 1000 tags you printed")
        label3.pack(side=TOP)  

        log_text = tkscrolled.ScrolledText(omni_box, wrap=WORD, width=32, height=15, state=DISABLED)
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
    Label(omni_box, text="©Dave Williams 2022").pack(side=BOTTOM)
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
            zplMessage = single_entry.get()
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

# ==========================================
# ========= Command definitions ============
# ==========================================
# miscellaneous defined commands

def open_file(): # opens selected file for group textbox insertion
    File1 = filedialog.askopenfilename()
    File2 = open(File1, "r")
    group_textbox.insert("1.0", File2.read())
    File2.close()  # Make sure you close the file when done

def clear_group_text(): # clears the group tab text box
    group_textbox.delete("1.0", END)

def print_group_text(): # print the group text box
    if group_textbox.get("1.0", END) == "\n":
        return
    group_text = group_textbox.get("1.0", END)
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
        for x in (group_text):
            if x == "":
                continue
            tag_type = cfg.asset_type.get()
            y = x
            BCPrint(y,1,y,tag_type)
            sleep(0.7) # sending the commands too quickly will have some disappear.. probably
        clear_group_text()
        return
    else:
        messagebox.showinfo("","Printing has been aborted")

def clear_range():
    range_entry2.delete(0, END)
    range_entry3.delete(0, END)
    cfg.range_start.set(0)
    cfg.range_end.set(0)

def clear_auto():
    auto_entry1.delete(0, END)
    auto_entry2.delete(0, END)
    
def print_range():
    total_print = 1 + int(cfg.range_end.get()) - int(cfg.range_start.get())
    if total_print <= 0:
        messagebox.showerror("Error", "Please sure you have the start and end numbers the correct way around")
        return
    answer = messagebox.askyesno("Question","This will print " + str(total_print) + " labels.\nDo you wish to continue?")
    if answer == True:
        lead_zeros = max(len(cfg.range_end.get()), len(cfg.range_start.get())) # Use the longer of the two number to determine leading zeros
        prefixed = str(cfg.range_prefix.get()).upper() # prefix entry, converted to upper case
        suffixed = str(cfg.range_suffix.get()).upper() # suffix entry, converted to lower case
        for x in range(int(cfg.range_start.get()), int(cfg.range_end.get())+1):
            y = str(x).zfill(lead_zeros)
            log = prefixed + y + suffixed
            BCPrint(log,1,log,"Asset Tag")
            sleep(0.7)    
        clear_range()
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

def clear_all():
    clear_auto()
    clear_group_text()
    clear_range()

def clear_custom_qr(): # clears the group tab text box
    custom_qr.delete(0, END)
    slide1.set(340)
    slide2.set(2)

def clear_custom():
    clear_custom_qr()
    custom_textbox.delete("1.0", END)

def print_custom_one(): # print one custom label
    qr = custom_qr.get()
    txt = custom_textbox.get("1.0", END)
    if (qr == "") and (txt.isspace()):
        return
    print_custom(1,qr,txt)
    
def print_custom_many(): # print many custom labels
    quant = str(cfg.custom_quantity.get())
    qr = custom_qr.get()
    txt = custom_textbox.get("1.0", END)
    if (qr == "") and (txt.isspace()):
        return
    answer = messagebox.askyesno("Question","This will print " + quant + " labels.\nDo you wish to continue?")
    if answer == True:
        print_custom(quant,qr,txt)
    else:
        messagebox.showinfo("","Printing has been aborted")

def print_custom(quant,qr,txt):
    cfg.qr_pos = slide1.get()
    cfg.qr_mag = slide2.get()
    customtxt = ()
    # txt = custom_textbox.get("1.0", END)
    txt = re.split(", |\n",txt)
    for x in (txt):
        if x == "":
            continue
        customtxt += (x,)
    # qr = custom_qr.get()
    if qr == "":
        txtPrint(quant,"*custom text label*",*customtxt)
    else:
        QRPrint(qr,quant,"*custom QR label*",*customtxt)

def con_update():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("data/con_print.ini")
    #Get the PRINTER section
    printer = config_object["PRINTER"]
    #Update the printer
    printer["printer_select"] = cfg.printer_select.get()
    printer["local_print"] = cfg.local_print.get()
    #Get the TAG-TYPE section
    tag = config_object["TAG-TYPE"]
    #Update the tag
    tag["tag_select"] = str(cfg.tag_select.get())
    flag = config_object["FLAGS"]
    flag["flag_1"] = str(flag_1)

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
    flag_1a = int(flag["flag_1"]) # 1 = Config, 2 = Mezz, 0 = Technician
    flag_1 = flag_1a
    
except:
    #Get the configparser object and create file
    config_object = ConfigParser()
    config_object["PRINTER"] = {
        "printer_select": cfg.printer_select.get(),
        "local_print": cfg.local_print.get()}
    config_object["TAG-TYPE"] = {
        "tag_select": cfg.tag_select.get()}
    config_object["FLAGS"] = {
        "flag_1": cfg.flag_1}
    with open('data/con_print.ini', 'w') as conf:
        config_object.write(conf)

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
app_title = tk.Label(frametop2, text="Config General Printing Application", font=("Helvetica",25)).pack(side=TOP)
help_button = tk.Button(master=frametop3, text="?", font=('Helvetica',20), command=help_me).pack(padx=(0,10))
try:
    cog_icon = ImageTk.PhotoImage(Image.open("data/cogwheel.png").resize((25, 25)))
    cog = tk.Button(master=frametop3, image=cog_icon, borderwidth=0, command=set_config)
    cog.pack(padx=(0,8), pady=(5,0))    
except:
    cog = tk.Button(master=frametop3, text="...", font=("Helvetica",14), command=set_config).pack()

# ==========================================
# ======= Settings panel (frame1a) =========
# ==========================================

printer_label = tk.Label(master=frame1,
                            text="Select printer:")
printer_label.grid(row=0, sticky=EW)

config_print_button = tk.Radiobutton(master=frame1,
                    text="Config Printer",
                    variable=cfg.printer_select,
                    value="LPT1",
                    command=con_update)
config_print_button.grid(row=1, sticky=W)

mezz_print_button = tk.Radiobutton(master=frame1,
                    text="MEZZ Printer",
                    variable=cfg.printer_select,
                    value="LPT7",
                    command=con_update)
mezz_print_button.grid(row=2, sticky=W)

test_print_button = tk.Radiobutton(master=frame1, # test print button. Remove for final release
                    text="Test Printer",
                    value="local",
                    variable=cfg.printer_select,
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
                    variable=cfg.tag_select,
                    value=0,
                    command=set_tag)
set_asset_button.grid(row=6, sticky=W)

set_serial_button = tk.Radiobutton(master=frame1,
                    text="Serial Numbers",
                    variable=cfg.tag_select,
                    value=1,
                    command=set_tag)
set_serial_button.grid(row=7, sticky=W)

reset_button = tk.Button(master=frame1, # restart app button, can be removed for final release
                    text="Restart App",
                    command=reset)
reset_button.grid(row=9, sticky=EW)

exit_button = tk.Button(master=frame1,
                    text="Quit",
                    command=quit)
exit_button.grid(row=10, sticky=EW)

# ==========================================
# =========== Single Tab (tab1) ============
# ==========================================

tab1.grid_columnconfigure((0,1,2,3),weight=1)
tab1.grid_rowconfigure((0,1,2),weight=1)
tab1.grid_rowconfigure((3),weight=3)

single_label = tk.Label(master=tab1,
                        textvariable=cfg.asset_type)
single_label.grid(row=0, column=1, sticky=E)

single_entry = tk.Entry(master=tab1, bg=cfg.bg_col)
single_entry.grid(row=0, column=2, sticky=W, padx=10)

single_btn = tk.Button(master=tab1, text="Print", width=10, command=return_key)
single_btn.grid(row=1, column=1, columnspan=2, sticky=N)

single_descript = tk.Label(master=tab1,
                        text="This will print a single label",
                        font=12,
                        fg="blue")
single_descript.grid(row=2, column=1, columnspan=2, sticky=N)

# ==========================================
# =========== Groups Tab (tab2) ============
# ==========================================

group_label1 = tk.Label(master=tab2,
                        font=12,
                        fg="blue",
                        text="Print the tags below:")
group_label1.pack()

group_label = tk.Label(master=tab2a,
                        textvariable=cfg.asset_type)
group_label.pack(side=LEFT, pady=(20,0))

group_entry = tk.Entry(master=tab2a, bg=cfg.bg_col)
group_entry.pack(side=LEFT, padx=10, pady=(20,0))

group_clear = tk.Button(master=tab2b,
                        text="Clear",
                        command=clear_group_text,
                        width=10)
group_clear.pack(side=LEFT)

group_print = tk.Button(master=tab2b,
                        text="Print",
                        command=print_group_text,
                        width=10)
group_print.pack(side=LEFT, padx=100)

group_load = tk.Button(master=tab2b,
                        text="Load from file",
                        command=open_file)
group_load.pack(side=LEFT, padx=(0,100))



group_textbox = tkscrolled.ScrolledText(master=tab2, wrap=WORD)
group_textbox.pack(side=BOTTOM, fill=BOTH, expand=True, padx=30, pady=(5,20))

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
                        command=clear_range,
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

auto_label1 = tk.Label(master=tab4a,
                        text="Scan the first tag in the range")
auto_label1.pack()

auto_entry1 = tk.Entry(master=tab4a,
                        textvariable=cfg.auto_1)
auto_entry1.pack()

auto_label2 = tk.Label(master=tab4a,
                        text="Scan the last tag in the range")
auto_label2.pack()

auto_entry2 = tk.Entry(master=tab4a,
                        textvariable=cfg.auto_2)
auto_entry2.pack()

auto_clear = tk.Button(master=tab4b,
                        text="Clear",
                        command=clear_auto,
                        width=10)
auto_clear.grid(row=0, column=1, padx=10)

auto_print = tk.Button(master=tab4b,
                        text="Print",
                        command=print_auto,
                        width=10)
auto_print.grid(row=0, column=2, padx=10)

warn_label = tk.Label(master=tab4c,
                        text="New Feature\nCheck number of tags\n is correct\nbefore printing",
                        font=("Helvetica",14),
                        fg="dark red")
warn_label.pack(side=TOP, padx=40, pady=40)

# ==========================================
# ======== Customer label Tab (tab5) =======
# ==========================================

print_quantity_label = tk.Label(master=tab5,
                            font=12,
                            fg="blue",
                            text="Enter quantity of labels required")
print_quantity_label.grid(row=0, column=0, pady=20, padx= 10)

print_quantity = tk.Spinbox(master=tab5, from_=1, to=9999,
                            textvariable=cfg.cust_quantity)
print_quantity.grid(row=0, column=1, pady=10, padx= 10)

bbc_button = tk.Button(master=tab5,
                        text="BBC",
                        command=BBC,
                        width=15)
bbc_button.grid(row=2, column=0, pady=10, padx= 10)

ebay_mac_button = tk.Button(master=tab5,
                        text="eBay Mac QR Code",
                        command=ebay_mac,
                        width=15)
ebay_mac_button.grid(row=3, column=0, pady=10, padx= 10)

ebay_pc_button = tk.Button(master=tab5,
                        text="eBay PC QR Code",
                        command=ebay_PC,
                        width=15)
ebay_pc_button.grid(row=4, column=0, pady=10, padx= 10)

# ==========================================
# ========== Reports Tab (tab6) ============
# ==========================================

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

label_6b = tk.Label(master=tab6b,
                    text="Nothing works on this page yet so don't waste your time",
                    font=38,
                    fg="red")
label_6b.grid(row=5, column=0, columnspan=4, rowspan=2)

# ==========================================
# =========== Custom Tab (tab7) ============
# ==========================================

custom_label1 = tk.Label(master=tab7a,
                        font=12,
                        fg="blue",
                        text="Print the label below:")
custom_label1.pack(side=TOP)

custom_label = tk.Label(master=tab7a,
                        text="QR Code: ")
custom_label.pack(side=LEFT, pady=(10,0))

custom_qr = tk.Entry(master=tab7a,
                    width=70)
custom_qr.pack(side=LEFT, padx=10, pady=(10,0))

slide1_label = tk.Label(master=tab7aa,
                        text="QR position: ")
slide1_label.pack(side=LEFT)

slide1 = Scale(tab7aa, from_=200, to=400, orient=HORIZONTAL, length=250)
slide1.set(cfg.qr_pos)
slide1.pack(side=LEFT)

slide2 = Scale(tab7aa, from_=1, to=10, orient=HORIZONTAL)
slide2.set(cfg.qr_mag)
slide2.pack(side=RIGHT)

slide2_label = tk.Label(master=tab7aa,
                        text="QR size: ")
slide2_label.pack(side=RIGHT)

custom_clear = tk.Button(master=tab7b,
                        text="Clear QR Code",
                        command=clear_custom_qr,
                        width=15)
custom_clear.pack(side=LEFT, padx=(40,0))

custom_print = tk.Button(master=tab7b,
                        text="Print one",
                        command=print_custom_one,
                        width=10)
custom_print.pack(side=LEFT, padx=40)

custom_print_many = tk.Button(master=tab7b,
                        text="Print many",
                        command=print_custom_many,
                        width=10)
custom_print_many.pack(side=LEFT, padx=0)

custom_load = tk.Button(master=tab7b,
                        text="Clear all",
                        command=clear_custom,
                        width=10)
custom_load.pack(side=LEFT, padx=40)

custom_quantity_label = tk.Label(master=tab7c,
                            text="Print quantity")
custom_quantity_label.pack(padx=10, side=LEFT)

custom_quantity = tk.Spinbox(master=tab7c, from_=1, to=9999,
                            textvariable=cfg.custom_quantity)
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
files += "data/8d82b51.mp3           # misc audio file\n"
files += "data/8d82b52.mp3           # misc audio file\n"
files += "data/bbc.png               # to print the BBC logo\n"
files += "data/CDW_Logo.png          # display CDW logo in app\n"
files += "data/cogwheel.png          # settings icon in app\n"
files += "data/custom_helper.jpg     # Help image for custom tab (300x400)\n"
files += "data/groups_helper.jpg     # Help image for groups tab (300x400)\n"
files += "data/range_auto_helper.jpg # Help image for range auto tab (300x400)\n"
files += "data/range_helper.jpg      # Help image for range tab (300x400)\n"
files += "data/single_helper.jpg     # Help image for singles tab (300x400)\n"
files += "data/cust_helper.jpg       # Help image for customer tab (300x400)\n"
files += "data/reports_helper.jpg    # Help image for reports tab (300x400)\n"
# Step 2, name your file
file_list = "data/filelist.txt"
# Step 3, Open file. "w" sets file to be freshly overwritten
File1 = open(file_list, "w")
# Step 4, Save list of files to newly opened file
File1.write(files)
# Step 5, close file
File1.close()

# ==========================================
# ========= Start up the routine ===========
# ==========================================

try:
    set_tag()
except:
    pass
self.bind('<Return>', return_key)
self.mainloop()
