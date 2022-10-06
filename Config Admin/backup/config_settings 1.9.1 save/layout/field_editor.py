from cgitb import reset
import tkinter as tk
from file_handling.config_file import Config_File

# TODO disable double click on entry widgets


# alows you to edit the fields in the .ini files
class Field_Editor(tk.Frame):
	# reference to the file object
	file = None
	# section name string
	section = None
	# key name
	key = None
	# text entry to edit the field
	text_entry = None

	# value in file
	@property
	def value_in_file(self): 
		return self.file.get_section_items(self.section)[self.key]

	def __init__(self, master, file: Config_File, section: str, key: str, *args, **kwargs):
		tk.Frame.__init__(self, master=master, *args, **kwargs)
		# set the variables
		self.file = file
		self.section = section 
		self.key = key

		# label to show the name of the field
		field_label = tk.Label(self, text=self.key)

		# text entry to edit the field
		self.text_entry = CustomText(self, height=1)
		self.text_entry.bind("<<TextModified>>", lambda dummy: self.on_entry_value_changed())
		# places the value of field into the text entry

		self.reset()

		# renders the widgets
		field_label.pack(side=tk.LEFT, padx=30)
		self.text_entry.pack(side=tk.RIGHT, padx=30)

	
	# every time a value is changed in the entry widget
	def on_entry_value_changed(self):
		has_value_been_edited = not (self.value_in_file == self.text_entry.get(1.0, "end-1c"))
		if(has_value_been_edited):
			self.text_entry.configure(background="#DBFAFF")
		else:
			self.text_entry.configure(background="White")


	# saves the value to the .ini file
	def save(self):
		# get value from entry
		new_value = self.text_entry.get(1.0, "end-1c")
		# makes change in file
		self.file.set_value(self.section, self.key, new_value)
		# refreshes the text box
		self.reset()


# TODO allow to pass
	# sets the text back to the value in the .ini file 
	def reset(self):
		# sets to value in the .ini file
		self.text_entry.replace(1.0, tk.END, self.value_in_file)



# has "<<TextModified>>" event
# has a charichter limit
# from stack overflow
# https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
class CustomText(tk.Text):
	# the width of the widget in charichters
	width_in_characters = 20

	def __init__(self, *args, **kwargs):
		"""A text widget that report on internal widget commands"""
		tk.Text.__init__(self, width=self.width_in_characters, *args, **kwargs)

		# create a proxy for the underlying widget
		self._orig = self._w + "_orig"
		self.tk.call("rename", self._w, self._orig)
		self.tk.createcommand(self._w, self._proxy)


	def _proxy(self, command, *args):
		cmd = (self._orig, command) + args
		# resunt of the command
		result = None

		# if user is trying to add text ...
		if (command == "insert"):
			# get length of input text
			input_text = self.get(1.0, "end-1c")
			# the length of the input text
			length_of_text_inputed = 0 if (input_text == "None") else len(input_text)
			# length of charachters to add
			length_of_characters_to_add = len(cmd[3])
			# the length that the text would be after the update
			new_length = length_of_text_inputed + length_of_characters_to_add
			# if new length is less then the max length ...
			if (new_length <= self.width_in_characters):
				# complete the function call
				result = self.tk.call(cmd)
				# call custom event
				try:
				# call custom event
					self.event_generate("<<TextModified>>")
				# catches tkinter error
				except Exception as e: pass
			# if new length is less then the max length ...
			else:
				# print an error
				print("Error: Max charichter size reached")
				return


		# TODO test
		# if user is trying to replace text ...
		elif (command == "replace"):
			# the original value in the entry
			original_value = self.get(1.0, "end-1c")
			# if empty text widget, then set to empty string
			if (original_value == "None"):
				original_value = ""
			# do replace command
			result = self.tk.call(cmd)
			# the length that the text would be after the update
			new_length = len(self.get(1.0, "end-1c"))
			# if over characher limit ...
			if (new_length > self.width_in_characters):
				# revert back to normal
				# clears text
				self.delete(1.0, tk.END)
				# sets to value in the .ini file
				self.insert(1.0, original_value)
				# print an error
				print("Error: Max charichter size reached")
				return
			else:
				try:
				# call custom event
					self.event_generate("<<TextModified>>")
				# catches tkinter error
				except Exception as e: pass


		elif (command == "delete"):
			try:
				result = self.tk.call(cmd)
				# call custom event
				self.event_generate("<<TextModified>>")
			# catches tkinter error
			except Exception as e: pass


		# if not "replace", "insert", "delete" call command
		else:
				result = self.tk.call(cmd)


		return result