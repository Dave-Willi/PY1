########################################################
# The purpose of this is to test importing an xml file #
# and generating clickable buttons along with commands #
# and definitions associated with said button          #
########################################################

# testing with pip install pytomlpp

# import pytomlpp as toml


from tkinter import *
import tkinter as tk
from configparser import ConfigParser

root = tk.Tk()
root.title("XML Import Test")
root.geometry("800x600")

# tab5 = tk.Frame(root)
# tab5.pack()

import cfg

global x_col
global y_row
x_col = 0
y_row = 0

# class button:
#     def __init__(self, name, place, history, type, code, *text):
#         global x_col
#         global y_row
#         self.name = name
#         place = place
#         self.history = history
#         self.type = type
#         self.code = code
#         self.text = text
#         name = tkinter.Button(master=tab5,
#                         text=self.name,
#                         command=self.func,
#                         width=20)
#         name.grid(pady=(0,10), padx=(0,10),row=y_row, column=x_col)
#         if y_row > 10:
#             x_col += 1
#             y_row = 0
#         else:
#             y_row += 1

#     def func(self):
#         print(int(self.type),self.history,self.code,self.text)

# trial2 = toml()
# toml.load('test/custom_buttons2.ini')
# print(toml)

class button(tk.Tk):
    def __init__(self, bname, bhistory, btype, bcode, btext):
        self.bname = bname
        self.bhistory = bhistory
        self.btype = btype
        self.bcode = bcode
        self.btext = btext

        name = tk.Button(master=root,
                        text=self.bname,
                        command=self.bfunc,
                        width=20)
        name.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
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
        print(int(self.btype),str(self.bhistory),self.bcode,self.newText)

class button2(tk.Tk):
    def __init__(self, bname, bhistory, bline1, bentry1, bline2, bentry2):
        self.bname = bname
        self.bhistory = bhistory
        self.btype = 0
        self.bline1 = bline1
        self.bentry1 = bentry1
        self.bline2 = bline2
        self.bentry2 = bentry2
        name = tk.Button(master=root,
                        text=self.bname,
                        command=self.bfunc,
                        width=20)
        name.grid(pady=(0,10), padx=(0,10),row=cfg.y_row, column=cfg.x_col)
        if cfg.x_col >= 2:
            cfg.y_row += 1
            cfg.x_col = 0
        else:
            cfg.x_col += 1
        return

    

    def bfunc(self):
        def entry_window(bline1,bentry1,bline2,bentry2):
            enter_box = tk.Toplevel()
            enter_box.geometry('350x500')
            enter_box.title(self.bname)
            def kill_me(): # closes the extra window
                enter_box.destroy()
            # enter_box.focus_force()
            # enter_box.bind('<FocusOut>', lambda x:kill_me())
            # enter_box.overrideredirect(True)
            enter_frame1 = tk.Frame(master=enter_box)
            enter_frame1.pack()
            entry1_label = tk.Label(master=enter_frame1,
                                    text=bline1)
            entry1_label.pack(pady=(15,0))
            enter1_entry = tk.Entry(master=enter_frame1, textvariable=bentry1, text=bentry1)
            enter1_entry.pack(pady=(0,15))
            enter1_entry.focus()
            entry2_label = tk.Label(master=enter_frame1,
                                    text=bline2)
            entry2_label.pack()
            enter2_entry = tk.Entry(master=enter_frame1, textvariable=bentry2)
            enter2_entry.pack(pady=(0,15))
            enter_print = tk.Button(master=enter_frame1,
                                    text="Print",
                                    command=an_print)
            enter_print.pack()
            display1 = tk.Label(master=enter_frame1, textvariable=bentry1, text=bentry1)
            display1.pack()
            return
        
        def an_print():
            # bentry1 = enter1_entry.get()
            print(bentry1)
            print(type(bentry1))
            print(bentry2)
            print(type(bentry2))
            pass

        entry_window(self.bline1,self.bentry1,self.bline2,self.bentry2)
        
        self.newText1 = (self.bline1,bentry1)
        self.newText2 = (self.bline2,bentry2)
        # cust_print(int(self.btype),str(self.bhistory),"",self.newText1)
        # cust_print(int(self.btype),str(self.bhistory),"",self.newText2)

trial = ConfigParser()
trial.read("data/custom_buttons.xml")
for x in trial:
    if x == "DEFAULT":
        continue
    y = trial[x]
    bname = y["button_name"]
    bhistory = y["history"]
    btype = y["btn_type"]
    if btype == "5":
        bline1 = y["line1"]
        bentry1 = y["entry1"]
        bline2 = y["line2"]
        bentry2 = y["entry2"]
        button2(bname, bhistory, bline1, bentry1, bline2, bentry2)
    else:
        bcode = y["code"]
        btext = y["text"]
        button(bname, bhistory, btype, bcode, btext)


#############################

# trial = ConfigParser()
# trial.read("Python Projects/xmlButtons/custom_buttons.xml")
# for x in trial:
#     if x == "DEFAULT":
#         continue
#     y = trial[x]
#     name = str(y["button_name"])
#     place = str(y["frame"])
#     history = str(y["history"])
#     type = str(y["type"])
#     code = str(y["code"])
#     text = str(y["text"])
#     button(name, place, history, type, code, text)

root.mainloop()