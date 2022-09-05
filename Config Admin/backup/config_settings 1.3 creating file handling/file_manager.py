import configparser
import os
from config_file import Config_File

# TODO handle empty files
# TODO handle empty sections
# TODO handle no files
# TODO handle sections inside sections
# TODO create an entry class



class File_Manager:
	
	# dict of all config files {name: config_file} name is without .ini
	_config_files = {}

	def __init__(self):
		# list of the {names: paths} of .ini files
		self._config_files = self.get_entries()
		# for value (file path) in entry
		for key, value in self._config_files.items():
			# add a new instance of config files list
			self._config_files.update( {key: Config_File(value)} )

	def get_entry(self, name) -> Config_File:
		return self._config_files[name]

	# list of the {names: paths} of .ini files
	def get_entries(self) -> dict:
		# list of the paths of .ini files
		ini_files_paths = []
		# list of the names of .ini files
		ini_files_names = []

		# gets the files to search
		folder_name = "/data/"
		files_to_search = os.listdir(os.curdir + folder_name)

		# for every file ...
		for file in files_to_search:
			# if it's not a .ini file check the next file
			if (not file.endswith(".ini")):
				continue
			# otherwise ...
			else:
				full_path = folder_name + file
				# add to the path .ini file path list
				ini_files_paths.append(full_path)

				# get name by splitting at the "."
				file_name = file.split(".")[0]
				# add the name of the file to .ini file names list
				ini_files_names.append(file_name)
				
		# creates a dictionary to return
		entries = dict(zip(ini_files_names,  ini_files_paths))

		# raise an error if no files were found
		if entries == []:
			raise FileNotFoundError("no .ini files found")

		return entries

file_manager = File_Manager()
file_manager.get_entry("dummy2").add_entry("settings2", {"hello": 1234})
file_manager.get_entry("dummy2").save()