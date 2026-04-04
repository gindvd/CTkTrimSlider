import customtkinter as ctk

from ctk_trimslider import CTkTrimSlider

root = customtkinter.CTk()


range_slider = CTkRangeSlider(root)
range_slider.pack(padx=30, pady=30, fill="both")

root.mainloop()