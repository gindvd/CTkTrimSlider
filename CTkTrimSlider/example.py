import tkinter
import customtkinter as ctk

from ctk_trimslider import CTkTrimSlider

def show_duration(value):
  duration = end_value.get() - start_value.get()
  duration_label.configure(text=str(duration))
  
def show_remaining(value):
  remaining = end_value.get() - current_value.get()
  remaining_label.configure(text=str(remaining))

root = ctk.CTk()

start_value = tkinter.DoubleVar(root, value=0)
end_value = tkinter.DoubleVar(root, value=1000)
current_value = tkinter.DoubleVar(root, value=500)

trim_slider = CTkTrimSlider(root, from_=0, to=1000, number_of_steps=1000,
                            start_variable=start_value, end_variable=end_value, center_variable=current_value,
                            lbutton_command=show_duration, rbutton_command=show_duration, cbutton_command=show_remaining)
trim_slider.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nswe")

ctk.CTkLabel(root, text="Start value:").grid(row=1,column=0, padx=5, pady=5)
start_label = ctk.CTkLabel(root, textvariable=start_value)
start_label.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="End value:").grid(row=2,column=0, padx=5, pady=5)
end_label = ctk.CTkLabel(root, textvariable=end_value)
end_label.grid(row=2, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="Current value:").grid(row=3,column=0, padx=5, pady=5)
current_label = ctk.CTkLabel(root, textvariable=current_value)
current_label.grid(row=3, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="Duration:").grid(row=4,column=0, padx=5, pady=5)
duration_label = ctk.CTkLabel(root, text="0")
duration_label.grid(row=4, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="Remaining:").grid(row=5,column=0, padx=5, pady=5)
remaining_label = ctk.CTkLabel(root, text=str(end_value.get() - current_value.get()))
remaining_label.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()