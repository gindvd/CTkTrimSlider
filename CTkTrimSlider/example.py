import customtkinter as ctk

from ctk_trimslider import CTkTrimSlider

def show_lvalue(value):
    print(value)

def show_rvalue(value):
    print(value)

def show_cvalue(value):
    print(value)

root = ctk.CTk()

trim_slider = CTkTrimSlider(root, to=100, from_=0, number_of_steps=1000, lbutton_command=show_lvalue, rbutton_command=show_rvalue, cbutton_command=show_cvalue)
trim_slider.pack(padx=30, pady=30, fill="both")

root.mainloop()