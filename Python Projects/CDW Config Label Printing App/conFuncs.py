from random import randint
import socket
import subprocess
import sys
from tkinter import messagebox
import re
from time import sleep
from playsound import playsound
import win32print
import win32ui
from PIL import Image, ImageWin

# ============ Command definitions ============
# miscellaneous defined commands

def quit(): # simple shutdown of program
    play = randint(0, 20)
    if play == 5:
        playsound('data/8d82b52.mp3')
    if play == 10:
        playsound('data/8d82b51.mp3')
    print(play)
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
        save = history_orig.read()
    with open("data\logs.txt", "w") as history_orig:
        history_orig.write(str(log))
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

# text formatting function
# Label is 200 dots high (actually larger but buffer for misaligned labels allows for less bad labels)

def txt_import(*more):
    if len(more) == 0:
        return ""
    sub_total = len(more)
    index = 0
    try:
        font_size_max = max(more, key=len)
        txt_length = len(font_size_max)
        font_size = min(round(180/(sub_total)),round(750/txt_length),60)
    except:
        font_size = min(round(180/(sub_total)),60)
    txt_printing = ""
    for x in (more):
        txt_printing += "^CF0," + str(font_size)
        txt_printing += "^FO10," + str((10+(font_size*index)))
        txt_printing += "^FD"
        txt_printing += str(x)
        txt_printing += "^FS"
        index += 1
    return(txt_printing)

# ========== QR Code Print (QRPrint) ==========
# x parameters = (code) QR code + (quant)Quantity + (hist)log + (*more) optional lines of text

def QRPrint(code,quant,hist,*more):
    printing = "^XA" # Start of label
    printing += "^LH15,0" # Label Home | position of start of label
    try:
        printing += txt_import(*more)
    except:
        printing += txt_import(more)
    printing += "^FO" + str(cfg.qr_pos) +",10" # Position of QR code
    printing += "^BQN,2," + str(cfg.qr_mag) # QR Initiator | last number is magnification/size
    printing += "^FDQA," # Field Initiator (QA is added for QR codes)
    printing += str(code) # QR Entry
    printing += "^FS" # end of field
    printing += "^PQ" # Print quantity
    printing += str(quant) # Selected quantity
    printing += "^XZ" # End of label
    to_print(printing,hist)

# ========== Simple text print (txtPrint) ==========
# x parameters = (quant)Quantity + (hist)log, (*more)1 or more lines of text

def txtPrint(quant,hist,*more):
    printing = "^XA" # Start of label
    printing += "^LH15,0" # Label Home | position of start of label
    try:
        printing += txt_import(*more)
    except:
        printing += txt_import(more)
    printing += str(quant) # Selected quantity
    printing += "^XZ" # End of label
    to_print(printing,hist)

# ========== BarCodePrint (BCPrint) ==========
# 4x parameters = (code)barcode + (quant)Quantity + (hist)log + (sa)serial or asset

def BCPrint(code,quant,hist,sa):
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
    printing += str(code) # Barcode Entry
    printing += "^FS" # end of field
    printing += "^PQ" # Print quantity
    printing += str(quant) # Selected quantity (normally 1 for barcodes)
    printing += "^XZ" # End of label
    to_print(printing,hist)

# ========== Image Print (imgPrint) ==========
# 3x parameters = (code)image filename + (quant)Quantity + (hist)log

def imgPrint(code,quant,hist):

    # read the image
    im = Image.open(code)
    # look at the dimensions
    size = im.size
    # calculate ratio x/y
    ratio = size[0] / size[1]
    # determine whether to apply ratio to height or width and do so
    if (180 * ratio) > 500:
        newsize = (500, round(500/ratio))
    else:
        newsize = (round(180*ratio),180)
    # rezise image to fit on label
    pic = im.resize(newsize)
    # show image
    pic.show()
    # figure out how to print it instead!!!!

    # the below sends 1 byte to the printer?! It's a zpl emulator so it might be ignoring it

    printer_name = win32print.GetDefaultPrinter ()
    
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)

    hDC.StartDoc (code)
    hDC.StartPage ()

    dib = ImageWin.Dib (pic)
    dib.draw (hDC.GetHandleOutput (), (0,0,newsize[0],newsize[1]))

    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()

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
                log = prefixed + y + suffixed
                BCPrint(log,1,log,"Asset Tag")
                sleep(0.7)
        else:
            messagebox.showinfo("","Printing has been aborted")
            return

def cust_print(type,hist,code,*txt):
    quant = str(cfg.cust_quantity.get())
    answer = messagebox.askyesno("Question","This will print " + hist + " labels.\nDo you wish to continue?")
    if answer == True:
        try:
            if type == 0:
                txtPrint(quant,hist,*txt)
            elif type == 1:
                QRPrint(code,quant,hist,*txt)
            elif type == 2:
                BCPrint(code,quant,hist,*txt)
            elif type == 3:
                imgPrint(code,quant,hist)
        except:
            return
    else:
        messagebox.showinfo("","Printing has been aborted")
        return

# ==========================================    
# ======= Customer label functions =========
# ==========================================
#
# cust_print = 4x parameters (label type, what to save in log, label code to print, optional text to print)
# label type = 0 plain text label e.g. (0,"plain tag","","Hello World")
# label type = 1 QR code label e.g. (1,"label","https://www.label.com","Hello Earth")
# label type = 2 BarCode label e.g. (2,"Stripes","F1355SV","Asset Tag")
# label type = 3 Image print e.g. (3,"Pretty picture","img.png")
# for barcode labels the 'txt' parameter needs either "Serial Number" or "Asset Tag"
#

def BBC():
    y = str(cfg.cust_quantity.get())
    log = ("*BBC Tag* x" + y)
    cust_print(3,log,"data/bbc.png")

def ebay_mac():
    y = str(cfg.cust_quantity.get())
    log = ("*Ebay MAC QR tag* x" + y)
    cust_print(1,log,"Hello world","eBay MAC","QR Code")

def ebay_PC():
    y = str(cfg.cust_quantity.get())
    log = ("*Ebay PC QR tag* x" + y)
    cust_print(1,log,"Bo Derek was here","eBay PC","QR Code")

# Import cfg last!!
import cfg