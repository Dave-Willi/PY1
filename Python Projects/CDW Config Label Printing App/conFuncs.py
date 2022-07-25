import cfg
import subprocess
import sys
from zplPrint import to_print
# from printApp import *
from tkinter import filedialog, messagebox

# ============ Side menu commands ============
# definitions required for the buttons on the left side menu to function

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

# ============ What to do when the enter key is pressed ============
# Currently only applies to single and group tags

def return_key(event = None):

    tab_name = frame2.select()
    tab_index = frame2.index(tab_name)
    if tab_index == 0: # single tags
        if single_entry.get() != "":
            tag_type = cfg.asset_type.get()
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

# ============ Command definitions ============
# miscellaneous defined commands

def quit(): # simple shutdown of program
    sys.exit()

def con_error(): # connection error
    print("Print error")

def set_print(): # attempt to map printers
    answer = messagebox.askyesno("Question", "Attempt to map network printers?")
    if answer == True:
        subprocess.call(r'net use lpt1: /delete',shell=True)
        subprocess.call(r'net use lpt7: /delete',shell=True)
        subprocess.call(r'net use lpt1 \\10.151.53.22\rug-cfg-zebra-01 /persistent:yes /USER:config\config.engineer homebuild',shell=True)
        subprocess.call(r'net use lpt7 \\10.151.53.22\rug-cfg-zebra-07 /persistent:yes /USER:config\config.engineer homebuild',shell=True)
    else:
        return

def history(log): # writes to history log file
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
        lead_zeros = max(len(cfg.range_end.get()), len(cfg.range_start.get()))
        prefixed = str(cfg.range_prefix.get()).upper()
        suffixed = str(cfg.range_suffix.get()).upper()
        for x in range(int(cfg.range_start.get()), int(cfg.range_end.get())+1):
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