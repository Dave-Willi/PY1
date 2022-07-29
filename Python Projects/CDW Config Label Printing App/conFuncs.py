import socket
import cfg
import subprocess
import sys
from tkinter import messagebox
import re
from time import sleep

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

# +++++++++++++++ ZPL PRINT FUNCTIONS +++++++++++++++

# ========== QR Code Print (QRPrint) ==========
# 3x parameter = (qr)Just QR code + (z)Quantity + (hl)log
# 4x parameters = (qr)QR code + (z)Quantity + (hl)log + (a)1 line of text
# 5x parameters = (qr)QR code + (z)Quantity + (hl)log + (a,b)2 lines of text

def QRPrint(qr,z,hl,*more):
    try:
        a = more[0]
    except:
        a = ""
    try:
        b = more[1]
    except:
        b = ""
    printing = "^XA" # Start of label
    printing += "^LH15,0" # Label Home | position of start of label
    printing += "^CF0,60" # Fontname and height and width
    printing += "^FO10,10" # Poisition of text
    printing += "^FD" # Field Initiator
    printing += a # text line 1
    printing += "^FS" # end of field
    printing += "^FO10,75" # Poisition of text
    printing += "^FD" # Field Initiator
    printing += b # text line 2
    printing += "^FS" # end of field
    printing += "^FO400,10" # Position of QR code
    printing += "^BQN,2,4" # QR Initiator | last number is magnification/size
    printing += "^FDQA" # Field Initiator (QA is added for QR codes)
    printing += str(qr) # QR Entry
    printing += "^FS" # end of field
    printing += "^PQ" # Print quantity
    printing += str(z) # Selected quantity
    printing += "^XZ" # End of label
    print(printing)
    to_print(printing,hl)

# ========== Simple text print (txtPrint) ==========
# 3x parameter = (a)1 line of text + (z)Quantity + (hl)log
# 4x parameters = (a,b)2 lines of text + (z)Quantity + (hl)log

def txtPrint(z,hl,*more):
    try:
        a = more[0]
    except:
        a = ""
    try:
        b = more[1]
    except:
        b = ""
    printing = "^XA" # Start of label
    printing += "^LH15,0" # Label Home | position of start of label
    printing += "^CF0,60" # Fontname and height and width
    printing += "^FO10,10" # Poisition of text
    printing += "^FD" # Field Initiator
    printing += a # text line 1
    printing += "^FS" # end of field
    printing += "^FO10,80" # Poisition of text
    printing += "^FD" # Field Initiator
    printing += b # text line 2
    printing += "^FS" # end of field
    printing += "^PQ" # Print quantity
    printing += str(z) # Selected quantity
    printing += "^XZ" # End of label
    to_print(printing,hl)

# ========== BarCodePrint (BCPrint) ==========
# 4x parameters = (sa)serial or asset + (bc)barcode + (z)Quantity + (hl)log

def BCPrint(sa,bc,z,hl):
    printing = "^XA" # Start of label
    printing += "^LH15,0" # Label Home | position of start of label
    printing += "^FO1,20" # Field position
    printing += "^AsN,25,25" # Font to use for this field | font, orientation, height, width
    printing += "^FD" # Field initiator
    printing += "Device "
    printing += sa # Serial or asset tag
    printing += "^FS" # end of field
    printing += "^FO3,60" # Position of Barcode code
    printing += "^B3N,N,100,Y,N" # Barcode Initiator | orientation, checkDigit, height, line, lineAbove
    printing += "^FD" # Field Initiator
    printing += str(bc) # Barcode Entry
    printing += "^FS" # end of field
    printing += "^PQ" # Print quantity
    printing += str(z) # Selected quantity (normally 1 for barcodes)
    printing += "^XZ" # End of label
    to_print(printing,hl)

# ========== to_print ==========
# 2x parameters = zpl code + log

def to_print(zyx, log):
    host = str(cfg.printer_select.get())
    if host == "local":
        host = str(cfg.local_print.get())
    print_me = bytes(zyx, 'utf-8')
    try:
        if "LPT" in host:
            sys.stdout = open(host, 'a')
            sys.stdout = sys.__stdout__
            history(log)
            return
        else:
            mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            mysocket.connect((host, cfg.port)) #connecting to host
            mysocket.send(print_me)
            mysocket.close() #closing connection
            history(log)
            return
    except:
        con_error()
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
                # xyz = ("^XA^LH15,0^FO1,20^AsN,25,25^FDDevice Asset Tag^FS^FO03,60^B3N,N,100,Y,N^FD" + prefixed + y + suffixed + "^FS^XZ")
                log = prefixed + y + suffixed
                BCPrint("Asset Tag",log,1,log)
                # to_print(xyz ,log)
                sleep(0.7)
        else:
            messagebox.showinfo("","Printing has been aborted")
            return