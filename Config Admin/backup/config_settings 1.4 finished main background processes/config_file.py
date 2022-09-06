from ast import Delete
from cgitb import html
import configparser
import os
from log import Log

# TODO allow sections inside sections
# TODO add are you sure you want to make these changes to save() method
# TODO update does_file_exist() method to check if file exists in a better way
# TODO handle key not found error
# TODO make the error() method call an event
# TODO make the save() method call an event if you want to override or create a new file
# TODO make errors more detailed
# TODO check typeing
# TODO add date time stamps to log files

# TODO handle empty files
# TODO handle empty sections
# TODO handle no files
# TODO handle sections inside sections

class Config_File:
	# name of the file
	name = None
	# a dictionary of the file used to edit and save the file
	config_dict = None
	# create a connfig parser that allows yo to read the .ini file
	config = None
	# the path of the file
	file_path = None
	# list of all edits made to the file
	edit_list = None

	def __init__(self, file_path: str):
		# instantiates the edit list
		self.edit_list = []
		# instantiates a config parser
		self.config = configparser.ConfigParser()
		# path of the file
		self.file_path = file_path
		# sets name by spliting up path
		self.name = file_path.split(".")[0].split("/")[-1]
		# read the file
		self.config.read(self.file_path)
		# converts the the config into a dict
		self.config_dict = self.config_to_dictionary(self.config)
		# checks file is real raises error if not valid
		if (not self.does_file_exist()):
			raise FileNotFoundError("config file does not exist")

	# saves file
	def save(self):
		# if file exists
		if (self.does_file_exist()):
			print(f"overwriting file at: {self.name}")
		# if file does NOT exist
		else:
			print("file not found, new file being created")

		# opens the file
		with open(self.file_path, "w") as file:
			# clears the memory of the config
			self.config.clear()
			# reads the dictionary object stored in this class
			print(self.config_dict)
			self.config.read_dict(self.config_dict)
			# writes the dictionary into the file in .ini format
			self.config.write(file)

	# returns name of the section
	def get_section_names(self) -> list:
		return list(self.config_dict.keys())

	# returns all the items in the section
	def get_section_items(self, section: str) -> dict:
		return dict(self.config_dict[section].items())

	# changes the name of the section
	def change_section_name(self, section: str, new_name: str):
		# if section does NOT exist ...
		if (not self.section_exists(section)):
			Log.error("can't change name section, it doesn't exist!")
			# stop the method
			return

		# duplicate section with a different name
		self.config_dict[new_name] = self.config_dict[section]
		Log.log_edit(self.name, f"section name changed from {section} to {new_name}")
		# delete the original
		del self.config_dict[section]

	# allows you to add a section
	def add_section(self, section: str):
		# if already key exists ...
		if (self.section_exists(section)):
			Log.error(self.name, "can't add section, it already exists!")
			# stop the method
			return

		# add the section
		self.config_dict[section] = {}
		Log.log_edit(self.name, f"{section} section added")

	# allows you to remove section
	def remove_section(self, section: str):
		# true if section exists
		section_exists = self.section_exists(section)

		# if section exists ...
		if (section_exists):
			# delete section
			del self.config_dict[section]
			# log the change
			Log.log_edit(self.name, f"{section} section deleted")
		# if section does NOT exists ...
		else:
			# log an error
			Log.error(self.name, "can't delete section, it dosn't exist")

	# allows you to add an entry to a section
	def add_entry(self, section: str, entry: dict):
		try:
			# adds entry to the config dict in the section given
			self.config_dict[section].update(entry)
		# if section not found
		except KeyError:
			# calls the error method
			Log.error(self.name, "section not found!")
		# if section is found
		else:
			print("ran")
			# logs the change
			Log.log_edit(self.name, f"{entry} added to [{section}] section")

	# allows you to delete an entry
	def delete_entry(self, section: str, key: str):
		# try delete the entry
		try:
			del self.config_dict[section][key]
		# if key or section doesnt exist 
		except KeyError:
			Log.error(self.name, "section or key not found!")
		else:
			# logs the change
			Log.log_edit(self.name, f"the field {key} in [{section}] section was deleted")

	# allows you to set the value of an entry
	def set_value(self, section: str, key: str, new_value: str):
		# true if selection exists
		section_exists = self.section_exists(section)
		# true if key exists
		key_exists = self.key_exists(section, key)

		# if section does NOT exist ...
		if (not section_exists):
			Log.error(self.name, "key not found!")
		# if key does NOT exist ...
		if (not key_exists):
			Log.error(self.name, "section not found!")
		# if one of them does NOT exist
		if (not (key_exists and section_exists)):
			# stop this method
			return

		# update the value
		self.config_dict[section][key] = new_value
		# log the change
		Log.log_edit(self.name, f"value of {key} changed to {new_value} in [{section}] section ")

	# checks if section exists returns true if found
	def section_exists(self, section: str) -> bool:
		# true if selection is in the config dict
		section_exists = section in self.config_dict
		# return value
		return section_exists
		
	# checks if key/field exists returns true if found
	def key_exists(self, section: str, key: str) -> bool:
		# if selection exists ...
		if (self.section_exists(section)):
			# true if key is in selection in the config dict
			key_exists = key in self.config_dict[section]
			# return value
			return key_exists
		# if selection does NOT exist ...
		else:
			return False

	# checks if file exists returns true if exists
	def does_file_exist(self) -> bool:
		# try tp read file
		try:
			with open(self.file_path, "r"): pass
		# if file not found ...
		except FileNotFoundError:
			return False
		# if file found ...
		else:
			return True

	# turns config into a dictionary
	def config_to_dictionary(self, config) -> dict:
		# turns data into a dictionary
		file_dictionary = dict(self.config)
		# for every section ...
		for section_key, section_value in file_dictionary.items():
			# creates a dictionary of all the values in the section
			section_items = {}
			# for items in section ...
			for key, value in self.config[section_key].items():
				# add item to section items dictionary
				section_items.update({key: value})
				
			# finaly ...
			# update them in the file dictionary class
			file_dictionary[section_key] = section_items

		# returns dictionary version of config
		return file_dictionary
