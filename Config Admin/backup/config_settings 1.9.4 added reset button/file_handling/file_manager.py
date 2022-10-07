import os
from .config_file import Config_File
from .log import Log
import datetime

# TODO add refresh method (updates classes if files are externaly tampered with) 
# in config_settings but called through a list of them in _config_files.values().refresh()
# TODO create backup method

class File_Manager:
	
	# currently selected file
	currently_selected_file = None
	# currently selected section (string)
	currently_selected_section = None
	
	# dict of all config files {name: config_file} name is without .ini
	_config_files = {}

	def __init__(self):
		# populates the  _config_files
		self.refresh_entries()

# give a name and returns the config_file class
	def get_entry(self, name) -> Config_File:
		# true if file in file dictionary
		file_exists = name in self._config_files
		# if is in file dictionary ...
		if (file_exists):
			# return the config File class
			return self._config_files[name]
		# if is NOT in file dictionary ...
		else:
			# print and return false
			print("couldnt get entry")
			return None

	# saves all the files
	def save_all(self):
		# gets current date and time
		dt = datetime.datetime.now()
		date_stamp = f"{dt.year}-{dt.month}-{dt.day} {dt.hour}-{dt.minute}"
		# directory for the old files
		backup_directory = f"data/old/{date_stamp}/"
		# for every Config_File ... 
		for file in self._config_files.values():
			# call the save method
			file.save(backup_directory)

	# get a dict of all the files {name: config_file}
	def get_entries(self):
		return self._config_files

	# list of the {names: config_file} of .ini files
	def refresh_entries(self) -> dict:
		# list of the config files of .ini files
		config_files = []
		# list of the names of .ini files
		ini_files_names = []

		# gets the files to search
		folder_name = "data/"
		files_to_search = os.listdir(os.curdir + "/" + folder_name)


		# populates the lists: ini_files_names, config_files
		# for every file ...
		for file in files_to_search:
			# if it's not a .ini file check the next file
			if (not file.endswith(".ini")):
				continue
			# otherwise ... 
			else:
				full_path = folder_name + file
				# add to the config_file .ini config_file list
				config_files.append(Config_File(full_path))

				# get name by splitting at the "."
				file_name = file.split(".")[0].split("/")[-1]
				# add the name of the file to .ini file names list
				ini_files_names.append(file_name)

				
		# creates a dictionary to return
		entries = dict(zip(ini_files_names,  config_files))

		# raise an error if no files were found
		if entries == []:
			raise FileNotFoundError("no .ini files found")

		# set the entries file {names: config_file}
		self._config_files = entries