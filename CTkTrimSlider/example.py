import tkinter
import customtkinter as ctk

from ctk_trimslider import CTkTrimSlider

def show_duration(value):
  duration = end_time.get() - start_time.get()
  duration_label.configure(text=str(duration))
  
def show_remaining(value):
  remaining = end_time.get() - current_time.get()
  remaining_label.configure(text=str(remaining))

root = ctk.CTk()

start_time = tkinter.DoubleVar(root, value=0)
end_time = tkinter.DoubleVar(root, value=1000)
current_time = tkinter.DoubleVar(root, value=10)

trim_slider = CTkTrimSlider(root, from_=0, to=1000, number_of_steps=1000,
                            start_variable=start_time, end_variable=end_time, center_variable=current_time,
                            lbutton_command=show_duration, rbutton_command=show_duration, cbutton_command=show_remaining)
trim_slider.pack(padx=5, pady=5, fill="x", expand=False)

start_label = ctk.CTkLabel(root, textvariable=start_time)
start_label.pack(padx=5, pady=5)

end_label = ctk.CTkLabel(root, textvariable=end_time)
end_label.pack(padx=5, pady=5)

current_label = ctk.CTkLabel(root, textvariable=current_time)
current_label.pack(padx=5, pady=5)

duration_label = ctk.CTkLabel(root, text="0")
duration_label.pack(padx=5, pady=5)

remaining_label = ctk.CTkLabel(root, text=str(end_time.get() - current_time.get()))
remaining_label.pack(padx=5, pady=5)

root.mainloop()