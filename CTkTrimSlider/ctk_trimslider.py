"""
CTkTrimSlider
Video trim slider for custom tkinter
Author: David Gingerich
Version 0.1.0
"""

from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.widgets.core_rendering import CTkCanvas
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

class CTkTrimSlider(CTkBaseClass):
  def __init__(self,
               master: any,
               width: int | None = None,
               height: int | None = None,
               corner_radius: int | None = None,
               
               from_: int = 0,
               to: int = 1,
               number_of_steps: int | None = None,
               state = "normal",
               hover: bool = True,
               orientation: str = "horizontal",

               **kwargs
              ):
    
    