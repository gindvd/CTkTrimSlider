import tkinter
import customtkinter as ctk

from ctk_trimslider import CTkTrimSlider

def show_duration():
  duration = end_time - start_time
  duration_label.configure(text=str(duration))
  
def show_remaining():
  remaining = end_time - current_time
  remaining_label.configure(text=str(remaining))

root = ctk.CTk()

start_time = tkinter.DoubleVar(root, value=0)
end_time = tkinter.DoubleVar(root, value=50)
current_time = tkinter.DoubleVar(root, value=0)

trim_slider = CTkTrimSlider(root, from_=0, to=1000, number_of_steps=1000, 
                            start_variable=start_time, end_variable=end_time, center_variable=current_time,
                            lbutton_command=show_duration, rbutton_command=show_duration, cbutton_command=show_remaining)
trim_slider.pack(padx=30, pady=30, fill="both")

start_label = ctk.CTkLabel(root, textvariable=start_time)
start_label.pack(padx=30, pady=30)

end_label = ctk.CTkLabel(root, textvariable=end_time)
end_label.pack(padx=30, pady=30)

current_label = ctk.CTkLabel(root, textvariable=current_time)
current_label.pack(padx=30, pady=30)

duration_label = ctk.CTkLabel(root, text="0")
duration.pack(padx=30, pady=30)

remaining_label = ctk.CTkLabel(root, text=str(end_time - current_time))
remaining.pack(padx=30, pady=30)

root.mainloop()