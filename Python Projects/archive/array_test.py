from doctest import master
import tkinter
import customtkinter
from tkcalendar import DateEntry

customtkinter.set_appearance_mode("dark") # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue") # Themes: blue (default), dark-blue, green

screen_types = list()
root = "null"
class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520
    

    def __init__(self):
        super().__init__()

        global checked1
        global checked2
        global checked3
        global checked4
        global checked5
        global checked6
        global checked7
        global checked8
        checked1 = tkinter.StringVar(value="")
        checked2 = tkinter.StringVar(value="")
        checked3 = tkinter.StringVar(value="")
        checked4 = tkinter.StringVar(value="")
        checked5 = tkinter.StringVar(value="")
        checked6 = tkinter.StringVar(value="")
        checked7 = tkinter.StringVar(value="")
        checked8 = tkinter.StringVar(value="")

        self.title("McD Project label printing app")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        self.frame_middle = customtkinter.CTkFrame(master=self,
                                                   width=180,
                                                   corner_radius=0)
        self.frame_middle.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=2, sticky="nswe", padx=20, pady=20)

# configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(4, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(7, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="McD Project labels",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Check list",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command = self.screen_check)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear list",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command = self.clear_screens)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=9, column=0, pady=10, padx=20, sticky="w")
        self.switch_2.select()

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Exit",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=exit)
        self.button_3.grid(row=10, column=0, pady=10, padx=20)

        # ============ middle frame ============
        self.frame_middle.rowconfigure(10, weight=1)
        self.frame_middle.columnconfigure(0, weight=1)

        self.check1 = customtkinter.CTkCheckBox(master=self.frame_middle,
                                                text="Check1",
                                                variable=checked1,
                                                onvalue='random1',
                                                offvalue="")
        self.check1.grid(row=1, column=0, pady=10, padx=20, sticky="n")

        self.check1 = customtkinter.CTkCheckBox(master=self.frame_middle,
                                                text="Check2",
                                                variable=checked2,
                                                onvalue="random2",
                                                offvalue="")
        self.check1.grid(row=2, column=0, pady=10, padx=20, sticky="n")

        self.check1 = customtkinter.CTkCheckBox(master=self.frame_middle,
                                                text="Check3",
                                                variable=checked3,
                                                onvalue="random3",
                                                offvalue="")
        self.check1.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.check1 = customtkinter.CTkCheckBox(master=self.frame_middle,
                                                text="Check4",
                                                variable=checked4,
                                                onvalue="random4",
                                                offvalue="")
        self.check1.grid(row=4, column=0, pady=10, padx=20, sticky="n")

        self.check1 = customtkinter.CTkCheckBox(master=self.frame_middle,
                                                text="Check5",
                                                variable=checked5,
                                                onvalue="random5",
                                                offvalue="")
        self.check1.grid(row=5, column=0, pady=10, padx=20, sticky="n")

        self.check1 = customtkinter.CTkCheckBox(master=self.frame_middle,
                                                text="Check6",
                                                variable=checked6,
                                                onvalue="random6",
                                                offvalue="")
        self.check1.grid(row=6, column=0, pady=10, padx=20, sticky="n")

        self.check1 = customtkinter.CTkCheckBox(master=self.frame_middle,
                                                text="Check7",
                                                variable=checked7,
                                                onvalue="random7",
                                                offvalue="")
        self.check1.grid(row=7, column=0, pady=10, padx=20, sticky="n")

        self.check1 = customtkinter.CTkCheckBox(master=self.frame_middle,
                                                text="Check8",
                                                variable=checked8,
                                                onvalue="random8",
                                                offvalue="")
        self.check1.grid(row=8, column=0, pady=10, padx=20, sticky="n")

    # ============ define functions ============

    def button_event(self):
        print("Button pressed")

    def screen_check(self):
        screen_types.clear()
        print("List starts as -")
        print(screen_types)
        print("Checking Screens")
        screen_types.append(checked1.get())
        screen_types.append(checked2.get())
        screen_types.append(checked3.get())
        screen_types.append(checked4.get())
        screen_types.append(checked5.get())
        screen_types.append(checked6.get())
        screen_types.append(checked7.get())
        screen_types.append(checked8.get())
        screen_types[:] = (value for value in screen_types if value != "")
        print(screen_types)

    def clear_screens(self):
        screen_types.clear()

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        app.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
