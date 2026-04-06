import customtkinter as ctk

from ctk_trimslider import CTkTrimSlider

root = ctk.CTk()


range_slider = CTkTrimSlider(root)
range_slider.pack(padx=30, pady=30, fill="both")

root.mainloop()


