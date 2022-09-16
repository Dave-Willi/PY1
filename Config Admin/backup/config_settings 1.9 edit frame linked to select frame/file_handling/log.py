class Log:
	edit_list = []
	# updates the edit_list about change made
	@staticmethod
	def log_edit(sender: str, message: str):
		Log.edit_list.append(f"{sender}: {message}")	

	# called when an error occurs
	@staticmethod
	def error(sender, message: str):
		# print message
		print(message)
		# the whole log file
		original_text = ""	
		# try open the log file
		try:
			with open("data/error_log.txt", "r") as f:
				# save the text
				original_text = f.read()
		# if log file not found (allow it, because it will one be created)
		except FileNotFoundError:
			# print to console
			print("log file not found, creaying a new one")	
		# create/overite ne
		with open("data/error_log.txt", "w") as f:
			f.write(f"{sender}: {message}\n")
			f.write(original_text)