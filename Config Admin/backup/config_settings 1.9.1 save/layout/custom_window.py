import tkinter as tk
from file_handling.file_manager import File_Manager

# what all custom frames inherit from
# spreads functionality that all custom frames should have
class Custom_Window(tk.Frame):
	file_manager = None

	def __init__(self, master, file_manager: File_Manager, *args, **kwargs):
		tk.Frame.__init__(self, master=master, *args, **kwargs)

		# create reference to the window
		self.file_manager = file_manager
