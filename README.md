# CTkTrimSlider
**A video trim slider widget made for [customtkinter](https://github.com/TomSchimansky/CustomTkinter)**


Download the source code, paste the `CTkTrimSlider` folder in the directory where your program is present.

## Example
```python
import customtkinter as ctk

from CTkTrimSlider.ctk_trimslider import CTkTrimSlider

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

trim_slider = CTkTrimSlider(root, 
                           from_=0, 
                           to=100, 
                           number_of_steps=100,
                           start_variable=start_value, 
                           end_variable=end_value, 
                           center_variable=current_value,
                           lbutton_command=show_duration, 
                           rbutton_command=show_duration, 
                           cbutton_command=show_remaining)

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
```

## Arguments
| Parameters | Details |
|--------|----------|
|master	| root window, can be _tkinter.Frame_ or _CTkFrame_|
|command	| callback function, receives slider value as argument, two separate commands can be given by `command=(cmd1, cmd2)`|
|variables	| tuple: set two tkinter.IntVar or tkinter.DoubleVar objects |
|width	| slider width in px|
|height | slider height in px|
|corner_radius| corner roundness of the slider |
|border_width	| space around the slider rail in px |
|from_	| lower slider value |
|to	| upper slider value |
|number_of_steps |	number of steps in which the sliders can be positioned |
|fg_color	| foreground color, tuple: (light_color, dark_color) or single color |
|progress_color	| tuple: (light_color, dark_color) or single color or "transparent", color of the slider line before the button |
|border_color	| slider border color, tuple: (light_color, dark_color) or single color or "transparent", default is "transparent"|
|button_color |	color of the slider buttons, tuple: (light_color, dark_color) or single color or **((light_color_1, dark_color_1), (light_color_2, light_color_2)) for separate button colors** |
|button_hover_color |	hover color, tuple: (light_color, dark_color) or single color|
|button_width | width of the buttons in px |
|button_length | length of the buttons in px|
|button_corner_radius | corner roundness of the buttons |
|orientation | "horizontal" (standard) or "vertical" |
|state	| "normal" or "disabled" (not clickable) |
|hover | bool, enable/disable hover effect, default is True |

## Methods:
- **.configure(attribute=value, ...)**

    All attributes can be configured and updated.
    ```python
     range_slider.configure(fg_color=..., progress_color=..., button_color=..., ...)
    ```
- **.set([value, value])**

   Set sliders to specific float value.

- **.get()**

   Get current values of slider.
   
- **.cget("attribute_name")**

   Get any attribute value.
   
### More Details
This widget works just like the normal customtkinter slider widget, but it has dual slider-heads instead of one. A special thanks to [EN20M](https://github.com/EN20M) for providing the custom DrawEngine for rangeslider. 
Follow me for more stuff like this: [`Akascape`](https://github.com/Akascape/)
### That's all, hope it will help!