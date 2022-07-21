import tkinter as tk
import customtkinter

class App(customtkinter.CTk):

    WIDTH = 600
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        text1 = tk.StringVar()
        text1.set("")
        
        def say_hi():
            print(say_what.get())
            text1.set(say_what.get())

        self.title("Bullshit testing app")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame1 = customtkinter.CTkFrame(self)
        frame2 = customtkinter.CTkFrame(self)
        frame3 = customtkinter.CTkFrame(self)

        label1 = customtkinter.CTkLabel(master=frame1,
                                        textvariable=text1,
                                        text=text1,
                                        width=120,
                                        height=25,
                                        fg_color=("white", "gray75"),
                                        bg_color=("black", "white"),
                                        corner_radius=8).pack()

        say_what = customtkinter.CTkEntry(master=frame2)
        say_what.pack()

        hi_there = customtkinter.CTkButton(master=frame3,text="say something",command=say_hi)
        hi_there.pack()

        frame1.pack(padx=1,pady=1)
        frame2.pack(padx=10,pady=10)
        frame3.pack(padx=10,pady=10)

    

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()