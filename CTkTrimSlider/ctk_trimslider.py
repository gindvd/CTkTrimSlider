"""
CTkTrimSlider
Video trim slider for custom tkinter
Author: David Gingerich
Version 0.1.0
"""

import tkinter

from collections.abc import Callable
from typing import Any

from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.widgets.core_rendering import CTkCanvas
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from custom_rendering import CustomDrawEngine

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
               
               outer_button_width: int | None = None,
               outer_button_height: int | None = None,
               outer_button_corner_radius: int | None = None,
               
               center_button_length: int | None = None,
               center_button_corner_radius: int | None = None,
               
               bg_color: str | tuple[str] = "transparent",
               fg_color: str | tuple[str] | None = None,
               border_color: str | tuple[str] = "transparent",
               progress_color: str | tuple[str] | None = None,
               button_color: str | tuple[str] | None = None,
               button_hover_color: str | tuple[str] | None = None,
               
               from_: int = 0,
               to: int = 1,
               number_of_steps: int | None = None,
               state: str = "normal",
               hover: bool = True,
               orientation: str = "horizontal",
               
               lbutton_variable: tkinter.Variable | None = None,
               rbutton_variable: tkinter.Variable | None = None,
               cbutton_variable: tkinter.Variable | None = None,
               
               **kwargs) -> None:
  
    # set default dimensions according to orientation
    if width is None:
      if orientation.lower() == "vertical":
        width = 20
      else:
        width = 500

    if height is None:
      if orientation.lower() == "vertical":
        height = 500
      else:
        height = 20
    
    # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
    super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

    # color
    self._border_color = self._check_color_type(border_color, transparency=True)
    self._fg_color = ThemeManager.theme["CTkSlider"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
    self._progress_color = ThemeManager.theme["CTkSlider"]["progress_color"] if progress_color is None else self._check_color_type(progress_color, transparency=True)
    
    self._button_color = ThemeManager.theme["CTkSlider"]["button_color"] if button_color is None else self._check_color_type(button_color)
    self._button_hover_color = ThemeManager.theme["CTkSlider"]["button_hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)

    # shape
    self._corner_radius = ThemeManager.theme["CTkSlider"]["corner_radius"] if corner_radius is None else corner_radius
    self._border_width = ThemeManager.theme["CTkSlider"]["border_width"] if border_width is None else border_width
    
    # center button shape
    self._center_button_corner_radius = ThemeManager.theme["CTkSlider"]["button_corner_radius"] if center_button_corner_radius is None else center_button_corner_radius
    self._center_button_length = ThemeManager.theme["CTkSlider"]["button_length"] if center_button_length is None else center_button_length
    
    # outer button shape parameters
    # set default dimensions according to orientation
    if outer_button_width is None:
      if orientation.lower() == "vertical":
        outer_button_width = 48
      else:
        outer_button_width = 12

    if outer_button_height is None:
      if orientation.lower() == "vertical":
       outer_button_height = 12
      else:
        outer_button_height = 48
    
    self._outer_button_width =  outer_button_width
    self._outer_button_height =  outer_button_height
    self._outer_button_corner_radius: int | float = ThemeManager.theme["CTkSlider"]["button_corner_radius"] if outer_button_corner_radius is None else outer_button_corner_radius
    
    self._from_:int = from_
    self._to: int = to
    self._number_of_steps: int | None = number_of_steps
    self._hover: bool = hover
    self._hover_state: bool = False
    self._orientation: str = orientation
    
    # set initial values of the 3 buttons
    self._lbutton_value: float = 0
    self._rbutton_value: float = 1
    self._cbutton_value: float = 0.5
    
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self._canvas = CTkCanvas(master=self,
                             highlightthickness=0,
                             width=self._apply_widget_scaling(self._desired_width),
                             height=self._apply_widget_scaling(self._desired_height))
    
    self._canvas.grid(column=0, row=0, rowspan=1, columnspan=1, sticky="nswe")

    self._draw_engine = CustomDrawEngine(self._canvas)
    self._draw()

  def _set_scaling(self, *args, **kwargs):
    super()._set_scaling(*args, **kwargs)

    self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                            height=self._apply_widget_scaling(self._desired_height))
    self._draw()

  def _set_dimensions(self, width=None, height=None):
    super()._set_dimensions(width, height)

    self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                          height=self._apply_widget_scaling(self._desired_height))
    self._draw()

  
  def _draw(self, no_color_updates: bool=False) -> None:
    super()._draw(no_color_updates)
    
    if self._orientation.lower() == "horizontal":
      orientation = "w"
    elif self._orientation.lower() == "vertical":
      orientation = "s"
    else:
      orientation = "w"

    requires_recoloring: bool = self._draw_engine.draw_rounded_slider_with_border_and_3_buttons(self._apply_widget_scaling(self._desired_width),
                                                                                                self._apply_widget_scaling(self._desired_height),
                                                                                                self._apply_widget_scaling(self._corner_radius),
                                                                                                self._apply_widget_scaling(self._border_width),
                                                                                                
                                                                                                self._apply_widget_scaling(self._outer_button_width),
                                                                                                self._apply_widget_scaling(self._outer_button_height),
                                                                                                self._apply_widget_scaling(self._outer_button_corner_radius),
                                                                                                
                                                                                                self._apply_widget_scaling(self._center_button_length),
                                                                                                self._apply_widget_scaling(self._center_button_corner_radius),

                                                                                                self._lbutton_value,
                                                                                                self._rbutton_value,
                                                                                                self._cbutton_value,
                                                                                                orientation)
    
    if no_color_updates is False or requires_recoloring:
      self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))

      if self._border_color == "transparent":
        self._canvas.itemconfig("border_parts", fill=self._apply_appearance_mode(self._bg_color),
                                outline=self._apply_appearance_mode(self._bg_color))
      else:
        self._canvas.itemconfig("border_parts", fill=self._apply_appearance_mode(self._border_color),
                                outline=self._apply_appearance_mode(self._border_color))

      self._canvas.itemconfig("inner_parts", fill=self._apply_appearance_mode(self._fg_color),
                              outline=self._apply_appearance_mode(self._fg_color))

      if self._progress_color == "transparent":
        self._canvas.itemconfig("progress_parts", fill=self._apply_appearance_mode(self._fg_color),
                                outline=self._apply_appearance_mode(self._fg_color))
      else:
        self._canvas.itemconfig("progress_parts", fill=self._apply_appearance_mode(self._progress_color),
                                outline=self._apply_appearance_mode(self._progress_color))
      
      if (self._hover_state and self._hover) is True:
        self._canvas.itemconfig("left_button_parts",
                                fill=self._apply_appearance_mode(self._button_hover_color),
                                outline=self._apply_appearance_mode(self._button_hover_color))
      else:
        self._canvas.itemconfig("left_button_parts",
                                fill=self._apply_appearance_mode(self._button_color),
                                outline=self._apply_appearance_mode(self._button_color))

      if (self._hover_state and self._hover) is True:
        self._canvas.itemconfig("right_button_parts",
                                fill=self._apply_appearance_mode(self._button_hover_color),
                                outline=self._apply_appearance_mode(self._button_hover_color))
      else:
        self._canvas.itemconfig("right_button_parts",
                                fill=self._apply_appearance_mode(self._button_color),
                                outline=self._apply_appearance_mode(self._button_color))

