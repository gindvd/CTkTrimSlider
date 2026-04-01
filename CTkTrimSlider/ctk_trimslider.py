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
               
               outer_btn_color: str | tuple[str] | None = None,
               outer_btn_hover_color: str | tuple[str] | None = None,
               
               inner_btn_color: str | tuple[str] | None = None,
               inner_btn_hover_color: str | tuple[str] | None = None, 
               
               outer_btn_corner_radius: int | None = None,
               outer_btn_width: int | None = None,
               outer_btn_height: int | None = None,
               
               inner_btn_corner_radius: int | None = None,
               inner_btn_width: int | None = None,
               inner_btn_height: int | None = None,
               
               lb_command: Callable[[Any], int | float] | None = None,
               rb_command: Callable[[Any], int | float] | None = None,
               mb_command: Callable[[Any], int | float] | None = None,
               
               from_: int = 0,
               to: int = 1,
               number_of_steps: int | None = None,
               state: str = "normal",
               hover: bool = True,
               orientation: str = "horizontal",
               
               **kwargs):
  
    # set default dimensions according to orientation
    if width is None:
      if orientation.lower() == "vertical":
        width = 24
      else:
        width = 240
    if height is None:
      if orientation.lower() == "vertical":
        height = 240
      else:
        height = 24
      
    # transfer basic functionality (_bg_color, size, __appearance_mode, scaling) to CTkBaseClass
    super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)
  
    # set themes of slider bar
    self._border_color: str | tuple[str]= self._check_color_type(border_color, transparency=True)
    self._fg_color: str | tuple[str] = ThemeManager.theme["CTkSlider"]["fg_color"] if fg_color is None else self._check_color_type(progress_color, transparency=True)
  
    # slider bar shape
    self._corner_radius: int = ThemeManager.theme["CTkSlider"]["corner_radius"] if corner_radius is None else corner_radius
    self._border_width: int = ThemeManager.theme["CTkSlider"]["border_width"] if border_width is None else border_width
  
    # slider bar vlaues
    self._from_: int = from_
    self._to: int = to
    self._number_of_steps = number_of_steps
  
class TrimSliderButton(CTkBaseClass):
  def __init__(self,
               master: Any,
               width: int | None = None,
               height: int | None = None,
               corner_radius: int | None = None,
               border_width: int | None = None,
               
               shape: str = "rectangular",
               
               bg_color: str | tuple[str] = "Transparent",
               fg_color: str | tuple[str] | None = None,
               border_color: str | tuple[str] = "Transparent",
               hover_color: str | tuple[str] | None = None,
               
               state: str = "normal",
               hover: bool = True,
               orientation: str = "horizontal",
               command: Callable[[Any], int | float] | None = None,
               
               **kwargs):

    if width is None:
      if shape.lower() == "rectangular":
        if orientation.lower() == "vertical":
          width = 72
        else:
          width = 24
      else:
        width = 24
    
    if height is None:
      if shape.lower() == "rectangular":
        if orientation.lower() == "vertical":
          height = int(width / 3)
        else:
          height = int(width * 3)
      else:
        height = width
  
    # transfer basic functionality (_bg_color, size, __appearance_mode, scaling) to CTkBaseClass
    super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)
  
    # use color themes for CTkButton
    self._fg_color: str | tuple[str] = ThemeManager.theme["CTkButton"]["fg_color"] if fg_color is None else self._check_color_type(fg_color, transparency=True)
    self._hover_color: str | tuple[str] = ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else self._check_color_type(hover_color)
    self._border_color: str | tuple[str] = ThemeManager.theme["CTkButton"]["border_color"] if border_color is None else self._check_color_type(border_color, transparency=True)
  
    # use shape themes for CTkButton
    self._corner_radius: int = ThemeManager.theme["CTkButton"]["corner_radius"] if corner_radius is None else corner_radius
    self._corner_radius = min(self._corner_radius, round(self._current_height / 2))
    self._border_width: int = ThemeManager.theme["CTkButton"]["border_width"] if border_width is None else border_width
  