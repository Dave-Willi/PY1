########################################################
# The purpose of this is to test importing an xml file #
# and generating clickable buttons along with commands #
# and definitions associated with said button          #
########################################################

import tkinter as tk
from tkinter import *
from configparser import ConfigParser

root = tk.Tk()
root.title("XML Import Test")

class button:
    def __init__(self, name, frame, history, type, code, *text):
        self.name = name
        self.frame = frame
        self.history = history
        self.type = type
        self.code = code
        self.text = text

ConfigParser

root.mainloop()