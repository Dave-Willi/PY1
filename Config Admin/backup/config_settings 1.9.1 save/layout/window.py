import tkinter as tk
from layout.custom_window import Custom_Window
from file_handling.file_manager import File_Manager
from layout.header_frame import Header
from .sections_editor import Select_Frame
from .edit_frame import Edit_Frame

# holds data about the window
class Window(tk.Tk):

	# window width
	width = 780
	# window height
	height = 520

	file_manager = None

	
	#			layout frames
	

	# has cdw logo and admin settings label
	header_frame = None
	header_frame_height = 90

	# holds the main_left_frame and main_right_frame
	main_frame = None

	# left partition of the main frame
	select_frame = None
	# main partition of the right frame
	edit_frame = None

	# ratio between the left and right side
	left_to_right_frame_ratio = 0.4

	
	#			constructer
	

	# creates a window but dosnt run it
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creates new file manager
		self.file_manager = File_Manager() 
		# sets current file
		self.file_manager.currently_selected_file = list(self.file_manager.get_entries().keys())[0]

		# TODO delete and make edit frame reset automaticly when section is updated
		self.file_manager.currently_selected_section = self.file_manager.get_entry(self.file_manager.currently_selected_file).get_section_names()[1]
		
		# gives the window a title
		self.title("Admin Settings")
		# sets window width and position
		self.geometry(("%dx%d") % (self.width, self.height))
		# stops resizing
		self.resizable(False,False)
		# centers window
		self.center_window()
		# initializes the frames
		self.create_frames()
		
		# runs the window
		self.mainloop()

	
	#			methods
	
	
	# initializes the frames
	def create_frames(self):
		
		# set height and width of the main frame
		main_frame_height = self.height - (self.header_frame_height)
		main_frame_width = self.width - 60

		main_left_frame_width = main_frame_width * self.left_to_right_frame_ratio


		# creates the main frames
		self.header_frame = Header(self,
										self.file_manager,
										width=self.width, 
										height=self.header_frame_height, 
										bg="green")

		self.main_frame = tk.Frame(self, 
										width=main_frame_width,
										height=main_frame_height,
										bg="purple")

		self.edit_frame = Edit_Frame(self.main_frame,
										self.file_manager, 
										width=main_frame_width * (1 - self.left_to_right_frame_ratio),
										height=main_frame_height,
										bg="red")

		self.select_frame = Select_Frame(self.main_frame, 
										self.file_manager,
										self.edit_frame,
										width=main_left_frame_width, 
										height=main_frame_height, 
										bg="yellow")

		# stops shrinking of frame
		self.header_frame.pack_propagate(False)
		self.main_frame.pack_propagate(False)
		self.select_frame.pack_propagate(False)
		self.edit_frame.pack_propagate(False)


		# renders all frames

		self.header_frame.pack()
		self.main_frame.pack()

		# pushes them onto the left and right side of the main frame
		self.select_frame.pack(side="left")
		self.edit_frame.pack(side="right")


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
