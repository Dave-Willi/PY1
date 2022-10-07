import tkinter as tk

# has "<<TextModified>>" event
# has a charichter limit
# from stack overflow
# https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
class CustomText(tk.Text):
	# the width of the widget in charichters
	width_in_characters = 38

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
			# if value is new line (enter key pressed) ...
			if (args[-1] == "\n"):
				self.event_generate("<<RemoveFocus>>")
				return

			# if value is tab (tab key pressed) ...
			if (args[-1] == "\t"):
				self.event_generate("<<NextFocus>>")
				return
				

			# remove any new lines
			new_args = list(args)
			new_args[-1] = new_args[-1].replace("\n", "")
			args = tuple(new_args)
			cmd = (self._orig, command) + args

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
				# try ...
				try:
				# call custom event
					self.event_generate("<<TextModified>>")
				# catches tkinter error
				except Exception as e: pass


		elif (command == "delete"):
			#try
			try:
				result = self.tk.call(cmd)
				# call custom event
				self.event_generate("<<TextModified>>")
			# catches tkinter error
			except Exception as e: pass


		# if not "replace", "insert", "delete" command
		else:
				result = self.tk.call(cmd)

    # for background calls to use
		return result