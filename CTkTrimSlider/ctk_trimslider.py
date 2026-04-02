"""
CTkTrimSlider
Video trim slider for custom tkinter
Author: David Gingerich
Version 0.1.0
"""

from collections.abc import Callable
from typing import Any

from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.widgets.core_rendering import CTkCanvas
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

class CTkTrimSlider(CTkBaseClass):
   
  """ 
  The trim slider is a custom slider with two outer buttons for changing 
  the start and end times of a video, and a center button that will both 
  move as the video is playing, or be manually moved to seek a specific time stamp.
  
  Visual Representation of the trim slider:
  
  -----|=====•=====|----
  """   
    
  def __init__(self,
               master: Any,
               width: int | None = None,
               height: int | None = None,
               corner_radius: int | None = None,
               border_width: int | None = None,
               
               bg_color: str | tuple[str] = "Transparent",
               fg_color: str | tuple[str] | None = None,
               border_color: str | tuple[str] = "Transparent",
               progress_color: str | tuple[str] | None = None,
               
               from_: int = 0,
               to: int = 1,
               number_of_steps: int | None = None,
               state: str = "normal",
               hover: bool = True,
               orientation: str = "horizontal",
               
               **kwargs) -> None:
  
    # set default dimensions according to orientation
    if width is None:
      if orientation.lower() == "vertical":
        width = 20
      else:
        width = 200
    if height is None:
      if orientation.lower() == "vertical":
        height = 200
      else:
        height = 20
    
    # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
    super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

    # color
    self._border_color = self._check_color_type(border_color, transparency=True)
    self._fg_color = ThemeManager.theme["CTkSlider"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
    self._progress_color = ThemeManager.theme["CTkSlider"]["progress_color"] if progress_color is None else self._check_color_type(progress_color, transparency=True)
    
    self._orientation = orientation
    self._hover_state: bool = False
    self._hover = hover
    self._from_ = from_
    self._to = to
    
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self._canvas = CTkCanvas(master=self,
                             highlightthickness=0,
                             width=self._apply_widget_scaling(self._desired_width),
                             height=self._apply_widget_scaling(self._desired_height))
    
    self._canvas.grid(column=0, row=0, rowspan=1, columnspan=1, sticky="nswe")