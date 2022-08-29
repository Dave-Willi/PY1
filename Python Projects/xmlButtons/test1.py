########################################################
# The purpose of this is to test importing an xml file #
# and generating clickable buttons along with commands #
# and definitions associated with said button          #
########################################################

import tkinter as tk
from tkinter import *
from configparser import ConfigParser
import tkinter

root = tk.Tk()
root.title("XML Import Test")
root.geometry("800x600")

tab5 = tk.Frame(root)
tab5.pack()

global x_col
global y_row
x_col = 0
y_row = 0

class button:
    def __init__(self, name, place, history, type, code, *text):
        global x_col
        global y_row
        self.name = name
        place = place
        self.history = history
        self.type = type
        self.code = code
        self.text = text
        name = tkinter.Button(master=tab5,
                        text=self.name,
                        command=self.func,
                        width=20)
        name.grid(pady=(0,10), padx=(0,10),row=y_row, column=x_col)
        if y_row > 10:
            x_col += 1
            y_row = 0
        else:
            y_row += 1

    def func(self):
        print(int(self.type),self.history,self.code,self.text)

trial = ConfigParser()
trial.read("Python Projects/xmlButtons/custom_buttons.xml")
for x in trial:
    if x == "DEFAULT":
        continue
    y = trial[x]
    name = str(y["button_name"])
    place = str(y["frame"])
    history = str(y["history"])
    type = str(y["type"])
    code = str(y["code"])
    text = str(y["text"])
    button(name, place, history, type, code, text)

root.mainloop()