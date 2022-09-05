import configparser

class Config_File:
	# name of the file
	name = None
	# a dictionary of the file
	config_dict = None
	# create a connfig parser that allows yo to read the .ini file
	config = configparser.ConfigParser()
	# the path of the file
	file_path = None

	def __init__(self, file_path):
		# path of the file
		self.file_path = file_path
		# sets name 
		self.name = file_path.split(".")[0]
		# read the file
		self.config.read(self.file_path)
		# converts the the config into a dict
		self.config_dict = self.config_to_dictionary(self.config)
		print(self.config.read(self.file_path))


	def save(self):
		with open(self.file_path, "w") as file:
			self.config.write(file)

	# returns name of the section
	def get_section_names(self) -> list:
		return list(self.config_dict.keys())

	# returns all the items in the section
	def get_section_items(self, section: str) -> dict:
		return dict(self.config_dict[section].items())

	# allows you to add an entry to a section with a dict perameter
	def add_entry(self, section, entry: dict):
		self.config_dict[section].update(entry)


	# turns config into a dictionary
	def config_to_dictionary(self, config) -> dict:
		# turns data into a dictionary
		file_dictionary = dict(self.config)

		# for every section ...
		for section_key in file_dictionary:
			# creates a dictionary of all the values in the section
			section_items = {}
			# for items in section ...
			for key, value in self.config[section_key].items():
				# add item to section items dictionary
				section_items.update({key: value})
			# finaly ...
			else:
				# update them in the file dictionary class
				file_dictionary[section_key] = section_items
		# returns dictionary version of config
		return file_dictionary
