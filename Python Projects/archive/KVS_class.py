import tkinter as tk
import customtkinter

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("KVS BS Test")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        # initialise variables
        global kitchen_
        global kitchenplus_
        global collect_
        global oat_
        global beverage_
        global orb01_
        global orb02_
        kitchen_ = False
        kitchenplus_ = False
        collect_ = False
        oat_ = False
        beverage_ = False
        orb01_ = False
        orb02_ = False

        # initialise frame

        frame1 = customtkinter.CTkFrame(master=self,
                                        width=130,
                                        height=500)
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        frame2 = customtkinter.CTkFrame(master=self,
                                        width=130,
                                        height=500)
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        frame3 = customtkinter.CTkFrame(master=self,
                                        width=130,
                                        height=500)
        frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        frame4 = customtkinter.CTkFrame(master=self,
                                        width=130,
                                        height=500)
        frame4.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        frame5 = customtkinter.CTkFrame(master=self,
                                        width=130,
                                        height=500)
        frame5.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        frame6 = customtkinter.CTkFrame(master=self,
                                        width=130,
                                        height=500)
        frame6.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        parent_window = frame1
        parent_window2 = frame2
        parent_window3 = frame3
        parent_window4 = frame4
        parent_window5 = frame5
        parent_window6 = frame6

        # set button toggle commands

        def set_kitchen():
            global kitchen_
            if kitchen_ == False:
                KVS01.select()
                KVS02.select()
                KVS03.select()
                KVS04.select()
                KVS05.select()
                kitchen_ = True
            else:
                KVS01.deselect()
                KVS02.deselect()
                KVS03.deselect()
                KVS04.deselect()
                KVS05.deselect()
                kitchen_ = False

        def set_kitchenplus():
            global kitchenplus_
            if kitchenplus_ == False:
                KVS01.select()
                KVS02.select()
                KVS03.select()
                KVS04.select()
                KVS05.select()
                KVS39.select()
                KVS40.select()
                kitchenplus_ = True
            else:
                KVS01.deselect()
                KVS02.deselect()
                KVS03.deselect()
                KVS04.deselect()
                KVS05.deselect()
                KVS39.deselect()
                KVS40.deselect()
                kitchenplus_ = False

        def set_collection():
            global collect_
            if collect_ == False:
                KVS12.select()
                KVS13.select()
                collect_ = True
            else:
                KVS12.deselect()
                KVS13.deselect()
                collect_ = False

        def set_oat():
            global oat_
            if oat_ == False:
                KVS16.select()
                KVS17.select()
                oat_ = True
            else:
                KVS16.deselect()
                KVS17.deselect()
                oat_ = False

        def set_beverage():
            global beverage_
            if beverage_ == False:
                KVS20.select()
                KVS23.select()
                KVS26.select()
                beverage_ = True
            else:
                KVS20.deselect()
                KVS23.deselect()
                KVS26.deselect()
                beverage_ = False

        def set_orb01():
            global orb01_
            if orb01_ == False:
                ORB01.select()
                MiniORB01.select()
                orb01_ = True
            else:
                ORB01.deselect()
                MiniORB01.deselect()
                orb01_ = False

        def set_orb02():
            global orb02_
            if orb02_ == False:
                ORB02.select()
                MiniORB02.select()
                orb02_ = True
            else:
                ORB02.deselect()
                MiniORB02.deselect()
                orb02_ = False

        # set all checkboxes

        KVS01 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS01",
                                            onvalue="KVS01",
                                            offvalue="",
                                            sticky="w")
        KVS01.pack(padx=5, pady=5)

        KVS02 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS02",
                                            onvalue="KVS02",
                                            offvalue="")
        KVS02.pack(padx=5, pady=5)

        KVS03 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS03",
                                            onvalue="KVS03",
                                            offvalue="")
        KVS03.pack(padx=5, pady=5)

        KVS04 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS04",
                                            onvalue="KVS04",
                                            offvalue="")
        KVS04.pack(padx=5, pady=5)

        KVS05 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS05",
                                            onvalue="KVS05",
                                            offvalue="")
        KVS05.pack(padx=5, pady=5)

        KVS06 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS06",
                                            onvalue="KVS06",
                                            offvalue="")
        KVS06.pack(padx=5, pady=5)

        KVS07 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS07",
                                            onvalue="KVS07",
                                            offvalue="")
        KVS07.pack(padx=5, pady=5)

        KVS08 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS08",
                                            onvalue="KVS08",
                                            offvalue="")
        KVS08.pack(padx=5, pady=5)

        KVS09 = customtkinter.CTkCheckBox(master=parent_window,
                                            text="KVS09",
                                            onvalue="KVS09",
                                            offvalue="")
        KVS09.pack(padx=5, pady=5)

        KVS10 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS10",
                                            onvalue="KVS10",
                                            offvalue="")
        KVS10.pack(padx=5, pady=5)

        KVS11 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS11",
                                            onvalue="KVS11",
                                            offvalue="")
        KVS11.pack(padx=5, pady=5)

        KVS12 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS12",
                                            onvalue="KVS12",
                                            offvalue="")
        KVS12.pack(padx=5, pady=5)

        KVS13 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS13",
                                            onvalue="KVS13",
                                            offvalue="")
        KVS13.pack(padx=5, pady=5)

        KVS14 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS14",
                                            onvalue="KVS14",
                                            offvalue="")
        KVS14.pack(padx=5, pady=5)

        KVS15 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS15",
                                            onvalue="KVS15",
                                            offvalue="")
        KVS15.pack(padx=5, pady=5)

        KVS16 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS16",
                                            onvalue="KVS16",
                                            offvalue="")
        KVS16.pack(padx=5, pady=5)

        KVS17 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS17",
                                            onvalue="KVS17",
                                            offvalue="")
        KVS17.pack(padx=5, pady=5)

        KVS18 = customtkinter.CTkCheckBox(master=parent_window2,
                                            text="KVS18",
                                            onvalue="KVS18",
                                            offvalue="")
        KVS18.pack(padx=5, pady=5)

        KVS19 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS19",
                                            onvalue="KVS19",
                                            offvalue="")
        KVS19.pack(padx=5, pady=5)

        KVS20 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS20",
                                            onvalue="KVS20",
                                            offvalue="")
        KVS20.pack(padx=5, pady=5)

        KVS21 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS21",
                                            onvalue="KVS21",
                                            offvalue="")
        KVS21.pack(padx=5, pady=5)

        KVS22 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS22",
                                            onvalue="KVS22",
                                            offvalue="")
        KVS22.pack(padx=5, pady=5)

        KVS23 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS23",
                                            onvalue="KVS23",
                                            offvalue="")
        KVS23.pack(padx=5, pady=5)

        KVS24 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS24",
                                            onvalue="KVS24",
                                            offvalue="")
        KVS24.pack(padx=5, pady=5)

        KVS25 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS25",
                                            onvalue="KVS25",
                                            offvalue="")
        KVS25.pack(padx=5, pady=5)

        KVS26 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS26",
                                            onvalue="KVS26",
                                            offvalue="")
        KVS26.pack(padx=5, pady=5)

        KVS27 = customtkinter.CTkCheckBox(master=parent_window3,
                                            text="KVS27",
                                            onvalue="KVS27",
                                            offvalue="")
        KVS27.pack(padx=5, pady=5)

        KVS28 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS28",
                                            onvalue="KVS28",
                                            offvalue="")
        KVS28.pack(padx=5, pady=5)

        KVS29 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS29",
                                            onvalue="KVS29",
                                            offvalue="")
        KVS29.pack(padx=5, pady=5)

        KVS30 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS30",
                                            onvalue="KVS30",
                                            offvalue="")
        KVS30.pack(padx=5, pady=5)

        KVS31 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS31",
                                            onvalue="KVS31",
                                            offvalue="")
        KVS31.pack(padx=5, pady=5)

        KVS32 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS32",
                                            onvalue="KVS32",
                                            offvalue="")
        KVS32.pack(padx=5, pady=5)

        KVS33 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS33",
                                            onvalue="KVS33",
                                            offvalue="")
        KVS33.pack(padx=5, pady=5)

        KVS34 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS34",
                                            onvalue="KVS34",
                                            offvalue="")
        KVS34.pack(padx=5, pady=5)

        KVS35 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS35",
                                            onvalue="KVS35",
                                            offvalue="")
        KVS35.pack(padx=5, pady=5)

        KVS36 = customtkinter.CTkCheckBox(master=parent_window4,
                                            text="KVS36",
                                            onvalue="KVS36",
                                            offvalue="")
        KVS36.pack(padx=5, pady=5)

        KVS37 = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="KVS37",
                                            onvalue="KVS37",
                                            offvalue="")
        KVS37.pack(padx=5, pady=5)

        KVS39 = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="KVS39",
                                            onvalue="KVS39",
                                            offvalue="")
        KVS39.pack(padx=5, pady=5)

        KVS40 = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="KVS40",
                                            onvalue="KVS40",
                                            offvalue="")
        KVS40.pack(padx=5, pady=5)

        ORB01 = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="ORB01",
                                            onvalue="ORB01",
                                            offvalue="")
        ORB01.pack(padx=5, pady=5)

        MiniORB01 = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="MiniORB01",
                                            onvalue="MiniORB01",
                                            offvalue="")
        MiniORB01.pack(padx=5, pady=5)

        ORB02 = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="ORB02",
                                            onvalue="ORB02",
                                            offvalue="")
        ORB02.pack(padx=5, pady=5)

        MiniORB02 = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="MiniORB02",
                                            onvalue="MiniORB02",
                                            offvalue="")
        MiniORB02.pack(padx=5, pady=5)

        DriveThru = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="Drive-Thru",
                                            onvalue="Drive-Thru",
                                            offvalue="")
        DriveThru.pack(padx=5, pady=5)

        Spare = customtkinter.CTkCheckBox(master=parent_window5,
                                            text="Spare",
                                            onvalue="Spare",
                                            offvalue="")
        Spare.pack(padx=5, pady=5)

        kit_but = customtkinter.CTkButton(master=parent_window6,
                                            text="Kitchen",
                                            corner_radius=8,
                                            command=set_kitchen)
        kit_but.pack(padx=5, pady=5)

        kitplus_but = customtkinter.CTkButton(master=parent_window6,
                                            text="Kitchen Plus",
                                            corner_radius=8,
                                            command=set_kitchenplus)
        kitplus_but.pack(padx=5, pady=5)

        col_but = customtkinter.CTkButton(master=parent_window6,
                                            text="Collection",
                                            corner_radius=8,
                                            command=set_collection)
        col_but.pack(padx=5, pady=5)

        oat_but = customtkinter.CTkButton(master=parent_window6,
                                            text="OAT",
                                            corner_radius=8,
                                            command=set_oat)
        oat_but.pack(padx=5, pady=5)

        bev_but = customtkinter.CTkButton(master=parent_window6,
                                            text="Beverage",
                                            corner_radius=8,
                                            command=set_beverage)
        bev_but.pack(padx=5, pady=5)

        orb01_but = customtkinter.CTkButton(master=parent_window6,
                                            text="ORB01",
                                            corner_radius=8,
                                            command=set_orb01)
        orb01_but.pack(padx=5, pady=5)
        
        orb02_but = customtkinter.CTkButton(master=parent_window6,
                                            text="ORB02",
                                            corner_radius=8,
                                            command=set_orb02)
        orb02_but.pack(padx=5, pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()                                     