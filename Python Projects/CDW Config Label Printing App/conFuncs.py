from random import randint
from playsound import playsound
import socket
import subprocess
import sys
from tkinter import messagebox
import tkinter as tk
import win32print
import win32ui
from PIL import Image, ImageWin

# ============ Command definitions ============
# miscellaneous defined commands

def ctrl_p(event):
    try:
        if cfg.pCounter == 0:
            messagebox.showinfo("Ctrl+P","I wouldn't do that if I were you")
            cfg.pCounter += 1
            return
        elif cfg.pCounter == 1:
            messagebox.showinfo("Ctrl+P","I'm warning you to not keep trying that!")
            cfg.pCounter += 1
            return
        elif cfg.pCounter == 2:
            messagebox.showinfo("Ctrl+P","Are you trying to upset me?")
            cfg.pCounter += 1
            return
        elif cfg.pCounter == 3:
            messagebox.showinfo("Ctrl+P","This is your last chance to turn back!")
            cfg.pCounter += 1
            return
        elif cfg.pCounter == 4:
            messagebox.showinfo("Ctrl+P","You're really doing this?")
            cfg.pCounter += 1
            return
        elif cfg.pCounter == 5:
            messagebox.showinfo("Ctrl+P","Fine, be that way. Don't say I didn't warn you")
            playsound("data/8dheowme.mp3")
            cfg.pCounter = 0
            return
    except Exception as e:
        print(e)

def quit(): # simple shutdown of program
    play = randint(0, 20)
    if play == 1:
        playsound('data/8d82b52.mp3')
    if play == 2:
        playsound('data/8d82b51.mp3')
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
# Label is 200 dots high (actually 208 but buffer for misaligned labels allows for less bad labels)

def txt_insert(ham):
    txt_length = len(ham)
    font_size = min(round(850/txt_length),140) + (int(cfg.textmod.get())*5)
    print(ham)
    print(font_size)
    txt_printing = ""
    txt_printing += "^A0N," + str(font_size)
    txt_printing += "^FO10," + str((100-(font_size/2)))
    txt_printing += "^FD"
    txt_printing += str(ham)
    return(txt_printing)

def txt_import(dud,more):

    # if str(more).startswith('('):
    #     more = str(more)
    #     more = more.split(',')
    #     print(type(more))
    # prints extra ("(' at start and ')") at end
    sub_total = len(more)
    if dud == 0:
        dud_length = 640
    elif dud == 1:
        dud_length = 850
    elif dud == 2:
        dud_length = 2000
        cfg.no_bc.set(False)
    if sub_total == 0:
        return ""
    index = 0
    try:
        font_size_max = max(more, key=len)
        txt_length = len(font_size_max)
        font_size = min(round(180/(sub_total)),round(dud_length/txt_length),60) + (int(cfg.textmod.get())*5)
    except:
        font_size = min(round(180/(sub_total)),100) + (int(cfg.textmod.get())*5)
    txt_printing = ""
    if cfg.no_bc.get() == True:
        quant = str(cfg.cust_quantity.get())
        for x in (more):
            txt_length = len(x)
            font_size = min(round(dud_length/txt_length),60) + (int(cfg.textmod.get())*5)
            txt_printing += "^XA" # Start of label
            txt_printing += "^LH" + str(15+(cfg.horz_label_mod.get() * 5)) + "," + str(10 + (cfg.label_mod.get() * 8))
            txt_printing += "^A0N," + str(font_size)
            # if sub_total== 1:
            txt_printing += "^FO10," + str((100-(font_size/2)))
            # else:
            #     txt_printing += "^FO10," + str((10+(font_size*index)))
            txt_printing += "^FD"
            txt_printing += str(x)
            txt_printing += "^FS"
            txt_printing += "^PQ"
            txt_printing += str(quant) # Selected quantity
            txt_printing += "^XZ" # End of label
    else:
        for x in (more):
            txt_printing += "^A0N," + str(font_size)
            if sub_total== 1:
                txt_printing += "^FO10," + str((100-(font_size/2)))
            else:
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
    printing += "^LH" + str(15+(cfg.horz_label_mod.get() * 5)) + "," + str(10 + (cfg.label_mod.get() * 8)) # Label Home | position of start of label
    try:
        printing += txt_import(0,*more)
    except:
        printing += txt_import(0,more)
    printing += "^FO" + str(cfg.qr_pos) +",10" # Position of QR code
    printing += "^BQN,2," + str(cfg.qr_mag) + ",L" # QR Initiator | last number is magnification/size
    # printing += "^BQN,2," + "3" + ",L" # QR Initiator | last number is magnification/size
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
    if cfg.no_bc.get() == True:
        printing = ""
        try:
            printing += txt_import(1,*more)
        except:
            printing += txt_import(1,more)

    else:
        printing = "^XA" # Start of label
        printing += "^LH" + str(15+(cfg.horz_label_mod.get() * 5)) + "," + str(10 + (cfg.label_mod.get() * 8)) # Label Home | position of start of label
        try:
            printing += txt_import(1,*more)
        except:
            printing += txt_import(1,more)
        printing += "^PQ"
        printing += str(quant) # Selected quantity
        printing += "^XZ" # End of label
    to_print(printing,hist)

# ========== BarCodePrint (BCPrint) ==========
# 4x parameters = (code)barcode + (quant)Quantity + (hist)log + (sa)serial or asset

def BCPrint(code,quant,hist,sa):
    printing = "^XA" # Start of label
    printing += "^LH" + str(15+(cfg.horz_label_mod.get() * 5)) + "," + str(10 + (cfg.label_mod.get() * 8)) # Label Home | position of start of label
    printing += "^FO1,20" # Field position
    printing += "^ASN,25,25" # Font to use for this field | font, orientation, height, width
    printing += "^FD" # Field initiator
    printing += cfg.device_label.get() + " "
    printing += str(sa) # Serial or asset tag
    printing += "^FS" # end of field
    printing += "^FO3,60" # Position of Barcode code
    printing += "^BCN,80,Y,N" # Barcode 'Code 128 Type' Initiator | orientation, height, line, lineAbove
    # printing += "^B3N,N,80,Y,N" # Barcode 'Code 39 Type' Initiator | orientation, checkDigit, height, line, lineAbove
    printing += "^FD" # Field Initiator
    printing += str(code).upper() # Barcode Entry
    printing += "^FS" # end of field
    printing += "^PQ" # Print quantity
    printing += str(quant) # Selected quantity (normally 1 for barcodes)
    printing += "^XZ" # End of label
    to_print(printing,hist)

# ========== Image Print (imgPrint) ==========
# 3x parameters = (code)image filename + (quant)Quantity + (hist)log

def imgPrint(code,quant,hist):
    downer = int(cfg.label_mod.get() * 6)
    # read the image
    im = Image.open(code)
    # look at the dimensions
    size = im.size
    sidex = size[0]
    sidey = size[1]
    target = 9000 # 500 default
    scale = 220 # 220 = LPT2, 180 = LPT1
    if sidex < sidey:
        im = im.rotate(270, expand=True)
        size = im.size
        sidex = size[0]
        sidey = size[1]
        ratio = sidey / sidex
        if (scale * ratio) > target:
            newsize = (round(target/ratio) , round(target))
        else:
            newsize = (round(scale), round(scale*ratio))
    else:
        ratio = sidex / sidey
        if (scale * ratio) > target:
            newsize = (round(target), round(target/ratio))
        else:
            newsize = (round(scale*ratio),round(scale))

    pic = im.resize(newsize)

    # the below sends 1 byte to the printer?! It's a zpl emulator so it might be ignoring it?

    # pic.show()

    printer_name = win32print.GetDefaultPrinter ()
    
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    y = int(quant)
    x = 0
    hDC.StartDoc (code)
    while x < y: # Loop the print to match the quantity.
        hDC.StartPage ()
        dib = ImageWin.Dib (pic)
        dib.draw (hDC.GetHandleOutput (), (10,0 + downer,10 + newsize[0],10 + newsize[1] + downer))
        hDC.EndPage ()
        x += 1
    hDC.EndDoc ()
    hDC.DeleteDC ()
    history(hist)

# ========== to_print ==========
# 2x parameters = zpl code + log

def to_print(zyx, log):
    host = str(cfg.printer_select.get())
    print_me = zyx
    try:
        if host == "local":
            host = str(cfg.local_print.get())
            print_me = bytes(zyx, 'utf-8')
            mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            mysocket.connect((host, cfg.port)) #connecting to host
            mysocket.send(print_me)
            mysocket.close() #closing connection
            history(log)
            return
        else:
            try:
                chisel = open(host, "w")
                chisel.write(zyx)
                chisel.close()
                history(log)
            except Exception as e:
                print(e)
            return
    except:
        con_error()
        return

def limit_print(zyx):
    host = str(cfg.printer_select.get())
    print_me = zyx
    try:
        if host == "local":
            print("1")
            # host = str(cfg.local_print.get())
            # print_me = bytes(zyx, 'utf-8')
            print("2")
            # mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            # mysocket.connect((host, cfg.port)) #connecting to host
            # mysocket.send(print_me)
            # mysocket.close() #closing connection
            toSaveHere = "printed.txt"
            print("3")
            FileSave = open(toSaveHere, "w")
            print("4")
            FileSave.write(zyx)
            print("5")
            FileSave.close()
            print("Saved")
            return
        else:
            try:
                chisel = open(host, "w")
                chisel.write(zyx)
                chisel.close()
            except Exception as e:
                print(e)
            return
    except:
        con_error()
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
        messagebox.showinfo("Cancelled","Printing has been aborted")
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


def BBC():
    y = str(cfg.cust_quantity.get())
    log = ("*BBC Tag* x" + y)
    cust_print(3,log,"data/bbc.png")
    cfg.cust_quantity.set(1)

def ebay_mac():
    y = str(cfg.cust_quantity.get())
    log = ("*Ebay MAC QR tag* x" + y)
    cfg.qr_pos = 325
    cfg.qr_mag = 2
    qrcode = "https://azwusenduserguidestorage.blob.core.windows.net/slef-setup-guide/Setup%20Assistant%20-%20Mac.pdf?sp=r&st=2021-07-21T20:03:19Z&se=2022-07-22T04:03:19Z&spr=https&sv=2020-08-04&sr=b&sig=asYaBWQoH1%2FpMQx348TdCyRw6A%2BU8LvqWObiQXSkK4I%3D"
    cust_print(1,log,qrcode,"eBay MAC","QR Code")
    cfg.cust_quantity.set(1)

def ebay_PC():
    y = str(cfg.cust_quantity.get())
    log = ("*Ebay Windows QR tag* x" + y)
    cfg.qr_pos = 325
    cfg.qr_mag = 2
    qrcode = "https://azwusenduserguidestorage.blob.core.windows.net/slef-setup-guide/Setup%20Assistant%20-%20Windows%20PC.pdf?sp=r&st=2021-07-21T20:04:59Z&se=2022-07-22T04:04:59Z&spr=https&sv=2020-08-04&sr=b&sig=UPuaJt%2BZmcqrG%2BqEx5WNPpGp7BInx0gdsaXQlg%2Be4c8%3D"
    cust_print(1,log,qrcode,"eBay Windows","QR Code")
    cfg.cust_quantity.set(1)

# Import cfg last!!
import cfg