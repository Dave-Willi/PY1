from PIL import Image, ImageTk
import tkinter as tk
from .custom_window import Custom_Window
from file_handling.file_manager import File_Manager


# holds data and widgets about the header frame
class Header(Custom_Window):
	# the logo path
	logo_image_path = "data/CDW_Logo.png"
	# label widget of logo (may be text if image not loaded)
	logo_header = None


	def __init__(self, master, file_manager: File_Manager, *args, **kwargs):
		Custom_Window.__init__(self, master, file_manager, *args, **kwargs)

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

