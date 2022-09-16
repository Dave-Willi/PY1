from queue import Empty
from layout.field_editor import Field_Editor
from .custom_window import Custom_Window
import tkinter as tk
from file_handling.file_manager import File_Manager
from file_handling.config_file import Config_File

# holds data and widgets about the select frame
class Edit_Frame(Custom_Window):

	# file this class is based on
	file_manager = None

	# section this class is based on
	section = None

	# reference to all the field_editer frames instances
	field_editors = []

	def __init__(self, master, file_manager: File_Manager, *args, **kwargs):
		Custom_Window.__init__(self, master, file_manager, *args, **kwargs)
		self.file_manager = file_manager

		# resets the frame
		self.refresh()


	# resets the frame and populates it with field editors
	def refresh(self):
		# gets name of currently selected file
		file_name = self.file_manager.currently_selected_file
		# uses name to get the currently selected file instance
		self.file = self.file_manager.get_entry(file_name)
		# gets the currently selected selected section
		self.section = self.file_manager.currently_selected_section

		# clears all of the field_editors off the frame
		self.clear()

		# stops method if no section is selected
		if (self.section == None):
			return
		# stops method if no file is selected
		if (self.file == None):
			return

		# all the key value pairs of data to be edited
		fields = self.file.get_section_items(self.section)


		# stops method if there are no fields
		if (len(fields) <= 0):
			print("empty")
			return

		# for every key value pair in the fields class ...
		for key, value in fields.items():
			# create a new field editor to represent the field
			field_editor = Field_Editor(self, self.file, self.section, key, value)
			# create a field editor class and add it to the list
			self.field_editors.append(field_editor)
			# render it on the this frame
			field_editor.pack()

	# clears all of the field_editors off the frame
	def clear(self):
		# for each field editor that already exists ...
		for field_editor in self.field_editors:
			# destroy that field_editor
			field_editor.destroy()

