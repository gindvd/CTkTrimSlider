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
               
               bg_color: str | tuple[str] = "Transparent",
               fg_color: str | tuple[str] | None = None,
               border_color: str | tuple[str] = "Transparent",
               progress_color: str | tuple[str] | None = None,

               outer_btn_color: str | tuple[str] | None = None,
               outer_btn_hover_color: str | tuple[str] | None = None,
               
               inner_btn_color: str | tuple[str] | None = None,
               inner_btn_hover_color: str | tuple[str] | None = None, 
               
               outer_btn_corner_radius: int | None = None,
               outer_btn_border_width: int | None = None,
               outer_btn_width: int | None = None,
               outer_btn_height: int | None = None,
               
               inner_btn_corner_radius: int | None = None,
               inner_btn_border_width: int | None = None,
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
               
               **kwargs) -> None:
  
    # set default dimensions according to orientation
    if width is None:
      if orientation.lower() == "vertical":
        width = 20
      elif orientation.lower() == "horizontal":
        width = 200
      else:
        raise AttributeError
    if height is None:
      if orientation.lower() == "vertical":
        height = 200
      elif orientation.lower() == "horizontal":
        width = 20
      else:
        raise AttributeError
    
    # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
    super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

    # color
    self._border_color = self._check_color_type(border_color, transparency=True)
    self._fg_color = ThemeManager.theme["CTkSlider"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
    self._progress_color = ThemeManager.theme["CTkSlider"]["progress_color"] if progress_color is None else self._check_color_type(progress_color, transparency=True)

    # shape
    self._corner_radius = ThemeManager.theme["CTkSlider"]["corner_radius"] if corner_radius is None else corner_radius
    self._border_width = ThemeManager.theme["CTkSlider"]["border_width"] if border_width is None else border_width

    # left trim button for changing video start time
    self._lslider_btn = TrimSliderButton(self, 
                                         width=outer_btn_width, 
                                         height=outer_btn_height,
                                         corner_radius=outer_btn_corner_radius,
                                         fg_color=outer_btn_color,
                                         hover_color=outer_btn_hover_color,
                                         value=to,
                                         state=state,
                                         hover=hover,
                                         orientation=orientation,
                                         command=lb_command)

    # right trim button for changing video end time
    self._rslider_btn = TrimSliderButton(self, 
                                         width=outer_btn_width, 
                                         height=outer_btn_height,
                                         corner_radius=outer_btn_corner_radius,
                                         fg_color=outer_btn_color,
                                         hover_color=outer_btn_hover_color,
                                         value=from_,
                                         state=state,
                                         hover=hover,
                                         orientation=orientation,
                                         command=rb_command)

    mb_offset = 1 + (to / number_of_steps)                               

    # middle seek button to  seek specific times inbetween the start and end times
    self._mslider_btn = TrimSliderButton(self, 
                                         width=inner_btn_width, 
                                         height=inner_btn_height,
                                         corner_radius=inner_btn_corner_radius,
                                         fg_color=inner_btn_color,
                                         hover_color=inner_btn_hover_color,
                                         shape="circular",
                                         value=mb_offset,
                                         state=state,
                                         hover=hover,
                                         orientation=orientation,
                                         command=mb_command)

    
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

    self._draw_engine = CustomDrawEngine(CTkCanvas)
  
  def _draw(self, no_color_updates: bool=False) -> None:
    super._draw(no_color_updates)

    requires_recoloring: bool = self._draw_engine.draw_rounded_slider_with_border_and_3_buttons(self._apply_widget_scaling(self._desired_width),
                                                                                                self._apply_widget_scaling(self._desired_height),
                                                                                                self._apply_widget_scaling(self._corner_radius),
                                                                                                self._apply_widget_scaling(self._border_width),

                                                                                                # outer button values, either _lsliber_button or _right_slider button can be used
                                                                                                self._apply_widget_scaling(self._lslider_btn._desired_width),
                                                                                                self._apply_widget_scaling(self._lslider_btn._desired_height),
                                                                                                self._apply_widget_scaling(self._lslider_btn._button_corner_radius),
                                                                                                                                                                                                
                                                                                                # center button values
                                                                                                self._apply_widget_scaling(self._mslider_btn._desired_width),
                                                                                                self._apply_widget_scaling(self._mslider_btn._desired_height),
                                                                                                self._apply_widget_scaling(self._mslider_btn._button_corner_radius),
                                                                                                                                                                                                
                                                                                                # button locations
                                                                                                self._lsliber_button._value,
                                                                                                self._rslider_btn._value,
                                                                                                self._mslider_btn._value,
                                                                                                self._orientation)

class TrimSliderButton(CTkBaseClass):
  def __init__(self,
               master: Any,
               width: int | None = None,
               height: int | None = None,
               corner_radius: int | None = None,
               
               shape: str = "rectangular",

               bg_color: str | tuple[str] = "Transparent",
               fg_color: str | tuple[str] | None = None,
               hover_color: str | tuple[str] | None = None,

               value: int | float | None = None, 
               state: str = "normal",
               hover: bool = True,
               orientation: str = "horizontal",
               command: Callable[[Any], int | float] | None = None,

               **kwargs):

    if width is None:
      if shape.lower() == "rectangular":
        if orientation.lower() == "vertical":
          width = 72
        elif orientation.lower() == "horizontal":
          width = 24

      elif shape.lower() == "circular":
        width = 28

      else:
          raise AttributeError("Not a valid attribute")

    if height is None:
      if shape.lower() == "rectangular":
        if orientation.lower() == "vertical":
          height = 24
        elif orientation.lower() == "horizontal":
          width = 72

      elif shape.lower() == "circular":
        width = 28

      else:
          raise AttributeError("Not a valid attribute")

    # transfer basic functionality (_bg_color, size, __appearance_mode, scaling to CTkBaseClass
    super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

    # use color themes for CTkButton
    self._fg_color: str | tuple[str] = ThemeManager.theme["CTkButton"]["fg_color"] if fg_color is None else self._check_color_type(fg_color, transparency=True)
    self._hover_color: str | tuple[str] = ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else self._check_color_type(hover_color)
    
    # use shape themes for CTkButton
    self._button_corner_radius: int = ThemeManager.theme["CTkSlider"]["button_corner_radius"] if button_corner_radius is None else button_corner_radius
   
    self._value = value
