import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkscrolled
import settings
from functions import *

class PrintApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Print Application")
        self.configure(bg=settings.backgroundColor)
        self.setup_UI()

    def setup_UI(self):
        plainPage = tk.Frame(self, bg=settings.backgroundColor)
        plainPage.grid(row=0, column=0, sticky="nsew")

        addRangeTextBtn = newButton2(plainPage, "Add range", lambda: [rangeToList(addRangeTextEntry1.get(), addRangeTextEntry2.get(), "\n\n"), updateTextLabels()])
        addRangeTextBtn.grid(row=4, column=5)

        ttk.Separator(plainPage, orient="vertical").grid(row=1, column=4, rowspan=7, sticky="ns")

        addTagsTextEntry = tk.Entry(plainPage)
        addTagsTextEntry.grid(row=1, column=2)
        addTagsTextEntry.bind('<Return>', lambda x: ReturnKeyPress("singleText"))

        addRangeTextEntry1 = tk.Entry(plainPage)
        addRangeTextEntry1.grid(row=2, column=5)
        addRangeTextEntry1.bind('<Return>', lambda x: ReturnKeyPress("rangeText1"))

        addRangeTextEntry2 = tk.Entry(plainPage)
        addRangeTextEntry2.grid(row=3, column=5)
        addRangeTextEntry2.bind('<Return>', lambda x: ReturnKeyPress("rangeText2"))

        addedTagsTextList = tkscrolled.ScrolledText(plainPage, width=20)
        addedTagsTextList.grid(row=1, column=0, rowspan=6, padx=(30,0), pady=(30,0), sticky="nsew")
        addedTagsTextList.bind('<Key>', updateTextLabels)

        upperCaseTextBtn = allCaps(plainPage, "All caps with show when\nlabels are printed.")
        upperCaseTextBtn.grid(row=9, column=0)
