import tkinter as tk
from tkinter import ttk
import settings
from functions import *

class PrintApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Print Application")
        self.configure(bg=settings.backgroundColor)
        self.setup_UI()

    def setup_UI(self):
        # Add your UI setup code here
        pass
