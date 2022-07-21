from contextlib import nullcontext
import random
import tkinter
import customtkinter
import string

customtkinter.set_appearance_mode("dark") # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue") # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):

    WIDTH = 1000
    HEIGHT = 850
    
    def __init__(self):
        super().__init__()

        global asset_var
        global asset_tags
        global printer_select
        asset_var=tkinter.StringVar(value="on")
        asset_tags=["as32df4d15","q34ta","ateg4","aerta","e45ta"]
        printer_select=tkinter.StringVar(value="lpt6")
        
        self.title("McD Project label printing app")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(6, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(7, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Duplicate Printer",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set printers",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command = self.set_printers)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Exit",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=exit)
        self.button_3.grid(row=10, column=0, pady=10, padx=20)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=9, column=0, pady=10, padx=20, sticky="w")
        self.switch_2.select()

        self.radio1 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                    text="Asset Tags",
                                                    variable= asset_var,
                                                    value="on")
        self.radio1.grid(row=4, column=0, pady=10, padx=20, sticky="w")

        self.radio2 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                    text="Serial Numbers",
                                                    variable= asset_var,
                                                    value="off")
        self.radio2.grid(row=5, column=0, pady=10, padx=20, sticky="w")

        self.radio3 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                    text="Config",
                                                    variable= printer_select,
                                                    value="lpt6")
        self.radio3.grid(row=7, column=0, pady=10, padx=20, sticky="w")

        self.radio4 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                    text="Mezz",
                                                    variable= printer_select,
                                                    value="lpt7")
        self.radio4.grid(row=8, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (6x5)
        self.frame_right.rowconfigure((0, 1, 3), weight=1)
        self.frame_right.rowconfigure((2, 4), weight=3, minsize=50)
        self.frame_right.columnconfigure((1, 2, 3, 4), weight=1)
        self.frame_right.columnconfigure((0, 5), weight=1, minsize=20)

        # ============ Tab buttons in frame_right ============

        self.tab_1 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Singles",
                                                command=self.single_event)
        self.tab_1.grid(row=0, column=1, pady=10 ,sticky="n")

        self.tab_2 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Groups",
                                                command=self.button_event)
        self.tab_2.grid(row=0, column=2, pady=10, sticky="n")

        self.tab_3 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Range",
                                                command=self.button_event)
        self.tab_3.grid(row=0, column=3, pady=10, sticky="n")

        self.tab_4 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Range (Auto)",
                                                command=self.asset_tags_clear)
        self.tab_4.grid(row=0, column=4, pady=10, sticky="n")

        # ============ frame_tags ============
        # ============ Where to put the input classes ============

        self.frame_tags = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_tags.grid(row=2, column=0, columnspan=6, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============
        # ============ List tags to be printed ============

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=4, column=0, columnspan=6,  pady=20, padx=20, sticky="nsew")

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    textvariable=asset_tags,
                                                    height=100,
                                                    fg_color=("white", "gray38"),
                                                    justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, columnspan=6, sticky="nwe", padx=15, pady=15)

        


    # ============ define functions ============

    def button_event(self):
        print("Button pressed")

    def single_event(self):
        print(nullcontext)

    def asset_tags_clear(self):
        asset_tags.clear()

    def add_rando(self):
        frog1 = ( ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)))
        asset_tags.append(frog1)

    def set_printers(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x300")
        frame_deets = customtkinter.CTkFrame(master=window,
                                            width=350,
                                            corner_radius=5)
        frame_deets.pack()
        asset_string  = customtkinter.StringVar()
        asset_string.set(''.join(asset_tags))
        label = customtkinter.CTkLabel(master=frame_deets, text="Your Asset tags are")
        label.pack(side="top", fill="both", expand=True)
        label2 = customtkinter.CTkLabel(master=frame_deets, textvariable=asset_var)
        label2.pack(side="top", fill="both", expand=True)
        label3 = customtkinter.CTkLabel(master=frame_deets, text="Your printer is")
        label3.pack(side="top", fill="both", expand=True)
        label4 = customtkinter.CTkLabel(master=frame_deets, textvariable=printer_select)
        label4.pack(side="top", fill="both", expand=True)
        label5 = customtkinter.CTkLabel(master=frame_deets, text="Asset tags are")
        label5.pack(side="top", fill="both", expand=True)
        label6 = customtkinter.CTkLabel(master=frame_deets, textvariable=self.asset_string)
        label6.pack(side="top", fill="both", expand=True)
        button_2q = customtkinter.CTkButton(master=frame_deets, text="Exit", command=window.destroy)
        button_2q.pack(side="bottom", fill="both", expand=False)

    

        

    def change_theme(self):
        switch_1_thing = str(self.switch_1.get())
        print("theme toggled " + switch_1_thing)
        if self.switch_1.get() == 1:
            customtkinter.set_default_color_theme("blue")
            print("theme set blue")
            
        else:
            customtkinter.set_default_color_theme("green")
            print("theme set green")
    
    def theme_check(self):
        print(customtkinter.get_appearance_mode())

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        app.destroy()

class single_tag(customtkinter.CTk):
    print(nullcontext)

class individual_tags(customtkinter.CTk):
    print(nullcontext)    

class range(customtkinter.CTk):
    print(nullcontext)

class range_auto(customtkinter.CTk):
    print(nullcontext)


if __name__ == "__main__":
    app = App()
    app.mainloop()