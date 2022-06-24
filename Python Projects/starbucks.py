# ============ frame_right ============

def starbucks():

    # configure grid layout (1x1)
    App.self.frame_info.rowconfigure(0, weight=1)
    self.frame_info.columnconfigure(0, weight=1)

    self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                text="CTkLabel: Lorem ipsum dolor sit,\n" +
                                                    "amet consetetur sadipscing elitr,\n" +
                                                    "sed diam nonumy eirmod tempor" ,
                                                height=100,
                                                fg_color=("white", "gray38"),  # <- custom tuple-color
                                                justify=tkinter.LEFT)
    self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

    self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
    self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

    # ============ frame_right ============

    self.radio_var = tkinter.IntVar(value=0)

    self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                    text="CTkRadioButton Group:")
    self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

    self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                        variable=self.radio_var,
                                                        value=0)
    self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

    self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                        variable=self.radio_var,
                                                        value=1)
    self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

    self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                        variable=self.radio_var,
                                                        value=2)
    self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

    self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                            from_=0,
                                            to=1,
                                            number_of_steps=3,
                                            command=self.progressbar.set)
    self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

    self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
                                            command=self.progressbar.set)
    self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

    self.slider_button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                    height=25,
                                                    text="CTkButton",
                                                    command=self.button_event)
    self.slider_button_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

    self.slider_button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                    height=25,
                                                    text="CTkButton",
                                                    command=self.button_event)
    self.slider_button_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

    self.checkbox_button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                        height=25,
                                                        text="CTkButton",
                                                        border_width=3,   # <- custom border_width
                                                        fg_color=None,   # <- no fg_color
                                                        command=self.button_event)
    self.checkbox_button_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

    self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                    text="CTkCheckBox")
    self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

    self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                    text="CTkCheckBox")
    self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

    self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                        width=120,
                                        placeholder_text="CTkEntry")
    self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

    self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                            text="CTkButton",
                                            command=self.button_event)
    self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

    # set default values
    self.radio_button_1.select()
    self.switch_2.select()
    self.slider_1.set(0.2)
    self.slider_2.set(0.7)
    self.progressbar.set(0.5)
    self.slider_button_1.configure(state=tkinter.DISABLED, text="Disabled Button")
    self.radio_button_3.configure(state=tkinter.DISABLED)
    self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
    self.check_box_2.select()