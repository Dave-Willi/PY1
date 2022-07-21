import cfg
import sys
import socket
import conFuncs

# ========== QRPrint ==========
# 1x parameter = Just QR code
# 2x parameters = 1 line of text + QR code
# 3x parameters = 2 lines of text + QR code

def QRPrint(a):
    pass

def QRPrint(a,b):
    pass

def QRPrint(a,b,c):
    pass

# ========== txtPrint ==========
# 1x parameter = 1 line of text
# 2x parameters = 2 lines of text

def txtPrint(a):
    pass

def txtPrint(a,b):
    pass

# ========== BCPrint ==========
# 2x parameters = Asset or serial + Code to print as barcode

def BCPrint(a,b):
    pass

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
            print(print_me)
            sys.stdout = sys.__stdout__
            conFuncs.history(log)
            conFuncs.clear_all()
            return
        else:
            mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            mysocket.connect((host, cfg.port)) #connecting to host
            mysocket.send(print_me)
            mysocket.close() #closing connection
            conFuncs.history(log)
            return
    except:
        conFuncs.con_error()
        return