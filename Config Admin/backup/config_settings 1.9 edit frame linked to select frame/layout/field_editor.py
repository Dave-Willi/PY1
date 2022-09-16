import tkinter as tk
from file_handling.config_file import Config_File


# alows you to edit the fields in the .ini files
class Field_Editor(tk.Frame):
	# reference to the file object
	file = None
	# section name string
	section = None
	# key name
	key = None
	# value
	value = None

	def __init__(self, master, file: Config_File, section: str, key: str, value: str, *args, **kwargs):
		tk.Frame.__init__(self, master=master, *args, **kwargs)
		# set the variables
		self.file = file
		self.section = section 
		self.key = key
		self.value = value

		# render the widgets
		tk.Label(self, text=self.key).pack(side=tk.LEFT, padx=30)
		tk.Label(self, text=self.value).pack(side=tk.RIGHT, padx=30)

