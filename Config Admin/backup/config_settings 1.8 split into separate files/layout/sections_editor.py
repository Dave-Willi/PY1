import tkinter as tk
import tkinter.ttk as tkk
from tkinter import  messagebox
from tkinter.simpledialog import askstring
from .custom_window import Custom_Window
from file_handling.file_manager import File_Manager

"""			Select_Frame class			"""


# holds data and widgets about the select frame
class Select_Frame(Custom_Window):


	# file combobox (allows you to select the .ini file you want to configure)
	select_file_dropdown_menu = None

	# list of sections (combobox)
	sections_selection_list = None

	def __init__(self, master, file_manager: File_Manager, *args, **kwargs):
		Custom_Window.__init__(self, master, file_manager, *args, **kwargs)


		# create drop down menu (combobox)
		self.select_file_dropdown_menu = tkk.Combobox(self, state="readonly")
		self.select_file_dropdown_menu.bind('<<ComboboxSelected>>', self.on_file_changed)
		# create add and remove buttons
		button_frame = tk.Frame(self)
		self.add_sections_button = tk.Button(button_frame, text="add", width=6, command=self.on_button_add)
		self.remove_sections_button = tk.Button(button_frame, text="remove", width=6)
		self.remove_sections_button.config(command=lambda :self.on_button_remove())

		# main part of the program

		main_frame = tk.Frame(self)
		# create the section selection box (listbox)
		self.sections_selection_list = Sections_Listbox(main_frame, file_manager, selectmode=tk.SINGLE)
		# create scroll bar
		self.scrollbar_sections = tk.Scrollbar(main_frame, orient=tk.VERTICAL)


		# refreshes parts of the program
		self.refresh_dropdown_entry_keys()
		self.sections_selection_list.refresh_listbox_entrys()

		# render widgets
		self.sections_selection_list.pack(side="left")
		self.scrollbar_sections.pack(side="right", fill=tk.Y)

		self.select_file_dropdown_menu.pack()
		main_frame.pack()

		button_frame.pack()
		self.add_sections_button.pack(side="left")
		self.remove_sections_button.pack(side="right")

	# what to do when the dropdown menu item is changed (update listbox)
	def on_file_changed(self, event):
		# gets file name from dropdown menu
		file_name = self.select_file_dropdown_menu.get()
		# changes the currently selected file
		self.file_manager.currently_selected_file = file_name
		# refreshes the listbox
		self.sections_selection_list.refresh_listbox_entrys()


	# adds sections
	def on_button_add(self):
		# get string input (what the section needs to be named)
		new_section_name = askstring("", "Enter the name of the section you would like to create")

		# if close button pressed ...
		if (new_section_name == None):
			# end method
			return
		# if nothing is typed in ...
		elif (new_section_name == ""):
			# show an error message
			messagebox.showerror("Invalid input!")
			return

		# gets the name of the current file
		current_file_name = self.file_manager.currently_selected_file
		# gets the class of the current file
		current_file = self.file_manager.get_entry(current_file_name)
		# adds the file
		# returns false if an error ocurred
		ran_successfully = current_file.add_section(new_section_name)
		# if ran successfully ...
		if (ran_successfully):
			# save file
			current_file.save()
			# refresh the listbox
			self.sections_selection_list.refresh_listbox_entrys()
			# select the entry
			self.sections_selection_list.select_set(tk.END)
			# call method
			self.sections_selection_list.on_selection_changed(None)
		else:
			# show an error message
			messagebox.showerror("", "Failed to input! \nCheck section doesn't already exist")
		
	# removes sections
	def on_button_remove(self):
		# get the file selected
		current_file = self.file_manager.get_entry(self.file_manager.currently_selected_file)

		# get all sections in the file
		section_names = current_file.get_section_names()
		# get the currently selected section
		current_section_name = self.file_manager.currently_selected_section

		choice_confirmed = False
		# if section NOT in the file ...
		if (current_section_name not in section_names):
			messagebox.showerror("", "Section not found!")
			return

		# ask user if there sure
		choice_confirmed = messagebox.askquestion("", f"Are you sure you want to delete \"{current_section_name}\" section?")
		# if choice is no, return
		if not ( choice_confirmed  == "yes"):
			return

		# remove the section
		current_file.remove_section(current_section_name)
		# save the changes
		current_file.save()

		# gets the index of the currently selected listbox item
		current_file_index = self.sections_selection_list.get_listbox_selected_index()
		# deletes index from combobox
		self.sections_selection_list.delete(current_file_index)
		# sets combobox selected index back to 0
		self.refresh_dropdown_entry_keys()

	# populates the values of the combobox widget and sets it to currently selected file
	# resets the listbox
	def refresh_dropdown_entry_keys(self):
		# dict of entries {name: Config_File}
		select_file_dropdown_entries = self.file_manager.get_entries()
		# list of only the keys (names)
		file_names = list(select_file_dropdown_entries.keys())
		# update the widgets values (sets the values to the list of names)
		self.select_file_dropdown_menu.configure(values=file_names)

		# if current file is in file names ...
		if (self.file_manager.currently_selected_file in file_names):
			# get the index
			index_of_curent_file = file_names.index(self.file_manager.currently_selected_file)
			# update the dropdown menu
			self.select_file_dropdown_menu.current(index_of_curent_file)
		# if current file is NOT in file names ...
		else:
			# return the first index
			self.select_file_dropdown_menu.current(0)
			# the name of the file that has been switched
			new_file_name = self.select_file_dropdown_menu.get()
			# calls method 
			self.on_file_changed(None)





"""			Sections_Listbox			"""


# the listbox on the left side
class Sections_Listbox(tk.Listbox):
	# reference to the file manager
	file_manager = None

	def __init__(self, master, file_manager: File_Manager, *args, **kwargs):
		tk.Listbox.__init__(self, master, *args, **kwargs)

		# creating file_manager reference
		self.file_manager = file_manager
		# only allow single selection
		self.configure(selectmode=tk.SINGLE)
		# what to do when selection changes
		self.bind('<<ListboxSelect>>', self.on_selection_changed)

	
	# what to do when selection changes (change variable in the file_manager)
	def on_selection_changed(self, event):
		# get section name
		currently_selected_section = self.get_listbox_selected_name()
		# update the file_manager variable
		self.file_manager.currently_selected_section = currently_selected_section

	# gets the name of the currently selected listbox item
	def get_listbox_selected_name(self) -> str:
		# gets the index of the selected file
		index = self.get_listbox_selected_index()
		# gets name of selecten file
		file_name = self.get(index)
		# returns name
		return file_name


	# gets the index of the currently selected listbox item
	def get_listbox_selected_index(self):
		# gets all the values selected in the listbox (only one can be selected)
		selected_tuple = self.curselection()
		
		# if empty tuple ...
		if (selected_tuple == ()):
			# print and return None
			print("nothing is selected")
			return None
		# if tuple is NOT empty 
		else:
			# get the first idex of selected_tuple
			selected_index = selected_tuple[0]
			# return value
			return selected_index

	# refreshes the listbox
	def refresh_listbox_entrys(self):
		# the name of the file
		file_name = self.file_manager.currently_selected_file
		# list of all the names of the sections
		section_names = self.file_manager.get_entry(file_name).get_section_names()


		# clears the listbox
		self.delete(0, tk.END)

		# add items to the listbox
		# for each section ...
		for section in section_names:
			# add section to the end of thr listbox
			self.insert(tk.END, section)


