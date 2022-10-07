from cgitb import reset
from doctest import master
import tkinter as tk
from file_handling.config_file import Config_File
from layout.custom_text import CustomText
from typing import List

# TODO disable double click on entry widgets


# allows you to edit the fields in the .ini files
class Field_Editor(tk.Frame):
	# reference to the file object
	file = None
	# section name string
	section = None
	# key name
	key = None
	# text entry to edit the field
	text_entry = None
	# reset button reference
	reset_button = None
	# all field editors
	field_editors = []

	# value in file
	@property
	def value_in_file(self): 
		return self.file.get_section_items(self.section)[self.key]

	@property
	def has_value_been_edited(self):
		return not (self.value_in_file == self.text_entry.get(1.0, "end-1c"))

	def __init__(self, master, file: Config_File, section: str, key: str, *args, **kwargs):
		tk.Frame.__init__(self, master=master, *args, **kwargs)
		self.configure(background="black") # DEBUG

		# set the variables
		self.file = file
		self.section = section 
		self.key = key

		# label to show the name of the field
		field_label = tk.Label(self, text=self.key)

		# text entry to edit the field
		self.text_entry = CustomText(self, height=1)
		self.text_entry.bind("<<TextModified>>", lambda dummy: self.on_entry_value_changed())
		self.text_entry.bind("<<NextFocus>>", lambda dummy: self.change_focus())
		self.text_entry.bind("<<RemoveFocus>>", lambda dummy: self.remove_focus())

		# create button
		self.reset_button = tk.Button(self, text="Reset", command=self.reset)

		# places the value of field into the text entry
		self.reset()

		# renders the widgets
		field_label.pack(side=tk.LEFT, padx=(10,0))
		self.reset_button.pack(side=tk.RIGHT, padx=(0,10), pady=(2, 2))
		self.text_entry.pack(side=tk.RIGHT, padx=(0,10))

		# ref to all field editors
		self.field_editors.append(self)

	# remove this instance from list and destroys
	def destroy(self):
		self.field_editors.remove(self)
		super().destroy()


	# removes focus from custom_text
	def remove_focus(self):
		self.master.focus_set()


	# sets focus to the text widget (rather than the frame)
	def change_focus(self):
		# True: go to next tab index
		# False: remove focus
		# get focused element
		focused_element = self.focus_get()

		# loop through the field editors
		for field_editor in Field_Editor.field_editors:
			# if one of the text entrys match the selected element ...
			if (field_editor.text_entry == focused_element):
				# get the focused field editer
				focused_field_editor = field_editor
				# break from loop
				break
		# if one of the text entrys match the selected element ...
		else:
			# log error
			print("Error: no focus found found")
			# stop script
			return

		# tab index of current selected field editor
		tab_index =  Field_Editor.field_editors.index(focused_field_editor)
		# get the next tab index 
		new_tab_index = tab_index + 1
		# check if i can get the next index ...
		try:
			next_field_editor = Field_Editor.field_editors[new_tab_index]
		# if there is no next index ...
		except IndexError:
			# go back to the first in the tab index
			next_field_editor = Field_Editor.field_editors[0]
		# change focus
		# used after() method to sto it from interfering with other commands
		self.after(50, lambda:  next_field_editor.text_entry.focus_set())


	# every time a value is changed in the entry widget
	def on_entry_value_changed(self):
		if(self.has_value_been_edited):
			self.reset_button.configure(state=tk.NORMAL)
			self.text_entry.configure(background="#DBFAFF")
		else:
			self.reset_button.configure(state=tk.DISABLED)
			self.text_entry.configure(background="White")


	# saves the value to the .ini file
	def save(self):
		# get value from entry
		new_value = self.text_entry.get(1.0, "end-1c")
		# makes change in file
		self.file.set_value(self.section, self.key, new_value)
		# refreshes the text box
		self.reset()


	# sets the text back to the value in the .ini file 
	def reset(self):
		# sets to value in the .ini file
		self.text_entry.replace(1.0, tk.END, self.value_in_file)
		# update what happens when the value is changed
		self.on_entry_value_changed()


