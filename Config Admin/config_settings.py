from cProfile import label
import tkinter as tk

# TODO make files automaticly go into select_frame_files
# TODO update check_everything_loaded_correctly() method
# TODO create a check load for window

# holds data about the window
class Window:
	# window width
	width = 780
	# window height
	height = 520
	# root element
	root = None

	# creates a window but dosnt run it
	def __init__(self):
		# creates a new window called root
		self.root = tk.Tk()
		# gives the window a title
		self.root.title("Admin Settings")
		# sets window width and position
		self.root.geometry(("%dx%d") % (self.width, self.height))
		# stops resizing
		self.root.resizable(False,False)
		# centers window
		self.center_window()

	# centers window
	def center_window(self):
		# gets screen width
		screen_width = self.root.winfo_screenwidth()
		# gets screen height
		screen_height = self.root.winfo_screenheight()
		# gets x co-ordinate
		screen_x_pos = (screen_width - self.width) / 2
		# gets y coordinate
		Screen_y_pos = (screen_height - self.height) / 2
		# sets position
		self.root.geometry("+%d+%d" % (screen_x_pos, Screen_y_pos))

# holds data about all wigits
class Window_Items:
	#
	#    ***when creating a widget add it to widget in get_widgets_that_couldnt_load method***
	#

	# has cdw logo and admin settings label
	header_frame = None
	header_frame_height = 50

	# holds the select frame and edit frame, and the add/remove/cancel/save/button
	main_frame = None

	# left partition of the main frame
	main_left_frame = None
	# main partition of the right frame
	main_right_frame = None

	# (part of main frame) takes the file from memory and allows you to select wich class to edit
	select_frame = None

	# (part of main frame) allows you to edit values of the classes
	edit_frame = None

	# ratio between the left and right side
	left_to_right_frame_ratio = 0.4



	# takes in a window object
	# instantiates all wigets
	# runs the window
	def __init__(self, window: Window):
		# initializes the frames
		self.create_frames(window)

		# renders all frames
		self.header_frame.grid(row = 0, columnspan = 1)
		self.main_frame.grid(row = 2)

		# pushes them onto the left and right side of the main frame
		self.main_left_frame.pack(side = "left")
		self.main_right_frame.pack(side = "right")

		# runs the window
		window.root.mainloop()

		# makes sure everything is loaded
		if (len(self.get_widgets_that_couldnt_load()) >= 1):
			raise AttributeError(f"error code 1: Window_Items, __init__ couldnt load: {self.get_widgets_that_couldnt_load()}")

	# initializes the frames
	def create_frames(self, window: Window):
		
		# set height and width of the main frame
		main_frame_height = window.height - (self.header_frame_height)
		main_frame_width = window.width - 60

		
		# initiates all frames
		self.header_frame = tk.Frame(window.root, 
									width = window.width, 
									height = self.header_frame_height, 
									bg = "green")

		self.main_frame = tk.Frame(window.root, 
									width = window.width,
									height = main_frame_width,
									bg = "purple")

		self.main_left_frame = tk.Frame(self.main_frame,
									width = main_frame_width * self.left_to_right_frame_ratio,
									height = main_frame_height,
									bg = "yellow")
		# stops srinking of frame
		self.main_left_frame.pack_propagate(False)

		self.main_right_frame = tk.Frame(self.main_frame, 
									width = main_frame_width * (1 - self.left_to_right_frame_ratio),
									height = main_frame_height,
									bg = "red")
		# stops srinking of frame
		self.main_right_frame.pack_propagate(False)

		

	# returns a list of the widgets that didn't load
	def get_widgets_that_couldnt_load(self) -> list:
		# list of all widgets
		widgets   = [self.main_frame,
					self.main_right_frame,
					self.header_frame,
					self.main_left_frame]
		# a list of all the widgets that couldnt load
		widgets_that_couldnt_load = []
		# for each widget in this class...
		for i in range(len(widgets)):
			# if the widget is not defined...
			if (i == None):
				# apends to list
				widgets_that_couldnt_load.append()

		# returns the list
		return widgets_that_couldnt_load





main_window = Window()
window_items = Window_Items(main_window)

