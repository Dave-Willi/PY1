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

	# main part of the frame that holds the field_editor frames
	field_editor_section = None

	# reference to all the field_editer frames instances
	widgets_on_this_frame = []

	def __init__(self, master, file_manager: File_Manager, *args, **kwargs):
		Custom_Window.__init__(self, master, file_manager, *args, **kwargs)
		self.file_manager = file_manager

		

		# creates new frame
		# main part of the frame that holds the field_editor frames
		self.field_editor_section = tk.Frame(self, height=200)
		self.field_editor_section.pack_propagate(False)

		# resets the frame
		self.refresh_field_editors()

		# save button 
		# (saves the changes to all the fiels)
		save_button = tk.Button(self, text="save", width=6, command=self.save_all)

		# reset button 
		# (go back to the values in the .ini file)

		# renders widgets
		self.field_editor_section.pack(fill="x", padx=20)
		save_button.pack()


	# resets the frame and populates it with field editors
	def refresh_field_editors(self):
		# gets name of currently selected file
		file_name = self.file_manager.currently_selected_file
		# uses name to get the currently selected file instance
		self.file = self.file_manager.get_entry(file_name)
		# gets the currently selected selected section
		self.section = self.file_manager.currently_selected_section

		# clears all of the widgets off the frame
		self.clear_all()

		# TODO test method

		# if there is no file selected ...
		# (stops method if no file is selected)
		if (self.file == None):
			# create message
			section_is_empty_label = tk.Label(self.field_editor_section, text="No file selected")
			please_select_a_file_label = tk.Label(self.field_editor_section, text="please select a file")
			# render message
			section_is_empty_label.pack()
			please_select_a_file_label.pack()
			# add to the list of widgets
			self.widgets_on_this_frame.append(section_is_empty_label)
			self.widgets_on_this_frame.append(please_select_a_file_label)
			# stop this method
			return


		# if thers no section selected ...
		# (stops method if no section is selected)
		if (self.section == None):
			# create message
			section_is_empty_label = tk.Label(self.field_editor_section, text="No section selected")
			please_select_a_file_label = tk.Label(self.field_editor_section, text="please select a selection")
			# render the message
			section_is_empty_label.pack()
			please_select_a_file_label.pack()
			# add to the list of widgets
			self.widgets_on_this_frame.append(section_is_empty_label)
			self.widgets_on_this_frame.append(please_select_a_file_label)
			return


		# all the key value pairs of data to be edited
		fields = self.file.get_section_items(self.section)


		# if there are 0 fields in the section ...
		# (stops method if there are no fields/section is empty)
		if (len(fields) <= 0):
			# create message
			section_is_empty_label = tk.Label(self.field_editor_section, text="This section is empty")
			# render the message
			section_is_empty_label.pack()
			# add to the list of widgets
			self.widgets_on_this_frame.append(section_is_empty_label)
			return

		# for every key value pair in the fields class ...
		for key, value in fields.items():
			# create a new field editor to represent the field
			field_editor = Field_Editor(self.field_editor_section, self.file, self.section, key)
			# create a field editor class and add it to the list
			self.widgets_on_this_frame.append(field_editor)
			# render it on the this frame
			field_editor.pack(fill="x")

	# clears all of the field_editors off the frame
	def clear_all(self):
		# for each field editor that already exists ...
		for widget in self.widgets_on_this_frame:
			# destroy that field_editor
			widget.destroy()

		# clear the widgets on frame list
		self.widgets_on_this_frame = []


	# saves all edits onto the .ini file
	def save_all(self):
		# loops through all the field editors
		for field_editor in self.widgets_on_this_frame:
			# if a field editor is selected
			if (type(field_editor) == Field_Editor):
				# call the save method
				field_editor.save()

		# self.file.save()
		self.file_manager.save_all()

