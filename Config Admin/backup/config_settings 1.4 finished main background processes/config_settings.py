from cProfile import label
from msilib.schema import ComboBox
import os
import tkinter as tk
import tkinter.ttk as tkk
from PIL import Image, ImageTk
from file_manager import File_Manager

# TODO add a popup to filenot found error in dropdown_entries method
# TODO handle what happens if theres no ini files
# TODO make files automaticly go into select_frame_files
# TODO update check_everything_loaded_correctly() method
# TODO create a check load for window
# TODO create a class/ method for creating images with alts e.g. alt text
# TODO create a help button
# TODO remove layout frames

# holds data about the window
class Window(tk.Tk):

	
	"""			fields			"""
	


	# window width
	width = 780
	# window height
	height = 520

	
	"""			layout frames			"""
	

	# has cdw logo and admin settings label
	header_frame = None
	header_frame_height = 90

	# holds the main_left_frame and main_right_frame
	main_frame = None

	# left partition of the main frame
	select_frame = None
	# main partition of the right frame
	main_right_frame = None

	# ratio between the left and right side
	left_to_right_frame_ratio = 0.4

	
	"""			methods			"""
	

	# creates a window but dosnt run it
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# gives the window a title
		self.title("Admin Settings")
		# initializes the frames
		self.create_frames()
		# sets window width and position
		self.geometry(("%dx%d") % (self.width, self.height))
		# stops resizing
		self.resizable(False,False)
		# centers window
		self.center_window()
		
		# runs the window
		self.mainloop()

	
	# initializes the frames
	def create_frames(self):
		
		# set height and width of the main frame
		main_frame_height = self.height - (self.header_frame_height)
		main_frame_width = self.width - 60

		main_left_frame_width = main_frame_width * self.left_to_right_frame_ratio


		# creates the main frames
		self.header_frame = Header_Frame(width=self.width, height=self.header_frame_height, bg="green")

		self.main_frame = tk.Frame(self, 
									width = main_frame_width,
									height = main_frame_height,
									bg = "purple")
		self.select_frame = Select_Frame(self.main_frame, width=main_left_frame_width, height=main_frame_height, bg="yellow")

		self.main_right_frame = tk.Frame(self.main_frame, 
									width = main_frame_width * (1 - self.left_to_right_frame_ratio),
									height = main_frame_height,
									bg = "red")

		# stops shrinking of frame
		self.header_frame.pack_propagate(False)
		self.main_frame.pack_propagate(False)
		self.select_frame.pack_propagate(False)
		self.main_right_frame.pack_propagate(False)


		# renders all frames

		self.header_frame.grid(row=0, columnspan=1)
		self.main_frame.grid(row=2)

		# pushes them onto the left and right side of the main frame
		self.select_frame.pack(side="left")
		self.main_right_frame.pack(side="right")


	# centers window
	def center_window(self):
		# gets screen width
		screen_width = self.winfo_screenwidth()
		# gets screen height
		screen_height = self.winfo_screenheight()
		# gets x co-ordinate
		screen_x_pos = (screen_width - self.width) / 2
		# gets y coordinate
		Screen_y_pos = (screen_height - self.height) / 2
		# sets position
		self.geometry("+%d+%d" % (screen_x_pos, Screen_y_pos))




# holds data and widgets about the header frame
class Header_Frame(tk.Frame):
	# the logo path
	logo_image_path = "data/CDW_Logo.png"
	# label widget of logo (may be text if image not loaded)
	logo_header = None


	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)

		# configure this frame
		#self.configure(width=width, height=height, bg=bg)
		# try and load the image ...
		try:
			# the image loaded
			logo_image = ImageTk.PhotoImage(Image.open(self.logo_image_path).resize((100, 60)))
		# if file is NOT found ...
		except FileNotFoundError:
			# set to alt text
			self.logo_header = tk.Label(self, text="CDW", font=("Helvetica",20), bg="green")
		# if image is found ...
		else:
			# the image in a label
			self.logo_header = tk.Label(self, image=logo_image, bg="green")
			# PATCH: to stop image showing up white (garbage collection)
			self.logo_header.image = logo_image
		# always ...
		finally:
			# renders the image/text logo
			self.logo_header.pack(side=tk.LEFT, anchor=tk.W, padx=10)

		# title for the app
		app_title = tk.Label(self, 
							text="Config Printing Admin Settings", 
							font=("Helvetica", 25),
							bg="green")

		# render title in the center 
		app_title.place(relx=0.5, rely=0.5, anchor="c")

# holds data and widgets about the select frame
class Select_Frame(tk.Frame):

	file_manager = File_Manager()
	# file combobox (allows you to select the .ini file you want to configure)
	select_file_dropdown_menu = None

	select_file_dropdown_entries = None

	# classes listbox (allows you to select the class in an .ini file to configure)
	classes_to_edit_listbox = None
	# scrollbar for the listbox
	scrollbar_classes_to_edit_listbox = None
	# add button (allows you to create another class in an .ini file)
	add_class_button = None
	# remove button (allows you to remove a class from an .ini file)
	remove_class_button = None

	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		label = tk.Label(self, text="hello World")
		label.pack()

		# dict of entries
		# key is the name value is the file path
		self.select_file_dropdown_entries = self.file_manager.get_entries()
		# list of only the keys
		dropdown_entry_keys = list(self.select_file_dropdown_entries.keys())

		self.select_file_dropdown_menu = tkk.Combobox(self, 
														state="readonly", 
														values=dropdown_entry_keys)
		self.select_file_dropdown_menu.pack()
		self.select_file_dropdown_menu.current(0)

		




main_window = Window()


