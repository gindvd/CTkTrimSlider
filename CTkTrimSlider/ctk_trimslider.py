"""
CTkTrimSlider
Video trim slider for custom tkinter
Author: David Gingerich
Version 0.1.1
"""

import tkinter
import sys
from collections.abc import Callable
from typing import Any

from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.widgets.core_rendering import CTkCanvas
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from CTkTrimSlider.custom_rendering import CustomDrawEngine

class CTkTrimSlider(CTkBaseClass):
  
  """ 
  The trim slider is a custom slider with two outer buttons for changing 
  the start and end times of a video, and a center button that will both 
  move as the video is playing, or be manually moved to seek a specific time stamp.
  
  Visual Representation of the trim slider:
  
  -----|=====•=====|----
  
  """   

  def __init__(self,
               master: object,
               width: int | None = None,
               height: int | None = None,
               corner_radius: int | None = None,
               border_width: int | None = None,
               
               outer_button_length: int | None = None,
               outer_button_corner_radius: int | None = None,
               center_button_corner_radius: int | None = None,
               
               bg_color: str | tuple[str] = "transparent",
               fg_color: str | tuple[str] | None = None,
               border_color: str | tuple[str] = "transparent",
               progress_color: str | tuple[str] | None = None,
               button_color: str | tuple[str] | None = None,
               button_hover_color: str | tuple[str] | None = None,
               
               from_: int = 0,
               to: int = 1,
               number_of_steps: int = 1000,
               state: str = "normal",
               hover: bool = True,
               orientation: str = "horizontal",
               
               left_button_command: Callable[[float], None] | None = None,
               right_button_command: Callable[[float], None] | None = None,
               center_button_command: Callable[[float], None] | None = None,
               
               left_button_var: tkinter.Variable | None = None,
               right_button_var: tkinter.Variable | None = None,
               center_button_var: tkinter.Variable | None = None,
               
               button_blocking: bool = False,
               **kwargs) -> None:
  
     # set default dimensions according to orientation
    if width is None:
      if orientation.lower() == "vertical":
        width = 24
      else:
        width = 500

    if height is None:
      if orientation.lower() == "vertical":
        height = 500
      else:
        height = 24
    
    if outer_button_length is None:
      self._outer_button_length: int = 12
    else:
      self._outer_button_length = outer_button_length
    
    super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

    # color
    self._border_color: str = self._check_color_type(border_color, transparency=True)
    self._fg_color: str = ThemeManager.theme["CTkSlider"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
    self._progress_color: str = ThemeManager.theme["CTkSlider"]["progress_color"] if progress_color is None else self._check_color_type(progress_color, transparency=True)
    
    self._button_color: str = ThemeManager.theme["CTkSlider"]["button_color"] if button_color is None else self._check_color_type(button_color)
    self._button_hover_color: str = ThemeManager.theme["CTkSlider"]["button_hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)

    # shape
    self._corner_radius: int | float = ThemeManager.theme["CTkSlider"]["corner_radius"] if corner_radius is None else corner_radius
    self._border_width: int | float = ThemeManager.theme["CTkSlider"]["border_width"] if border_width is None else border_width
    
    # corner radius
    self._center_button_corner_radius: int | float = ThemeManager.theme["CTkSlider"]["button_corner_radius"] if center_button_corner_radius is None else center_button_corner_radius
    self._outer_button_corner_radius: int | float = ThemeManager.theme["CTkSlider"]["button_corner_radius"] if outer_button_corner_radius is None else outer_button_corner_radius
    
    if from_ >= to:
      raise ValueError("from_ value cannot be greater than or equal to to value!")
    
    # input and output values
    self._from_:int = from_
    self._to: int = to

    # values under 1 causes button values to be neegative which leads to draw errors
    # also doesn't make sense to have 1 step
    if number_of_steps <= 1:
      raise ValueError("number_of_steps must be any value above 1")
    
    self._number_of_steps: int  = number_of_steps
    self._step_size: float = (self._to - self._from_) / self._number_of_steps
    
    # output values
    self._left_output_value: int| float = from_
    self._right_output_value: int | float = to
    self._center_output_value: float = from_ + (to - from_) / 2
    
    # states 
    self._state: str = state
    self._hover: bool = hover
    self._hover_state: bool = False
    self._orientation: str = orientation.lower()
    
    # set initial left, right, and center button values, must be between 0 and 1
    self._lbutton_value: float = 0
    self._rbutton_value: float = 1
    self._cbutton_value: float = 0.5
    
    # commands fro each button
    self._left_button_command: Callable[[float], None] | None = left_button_command
    self._right_button_command: Callable[[float], None] | None = right_button_command
    self._center_button_command: Callable[[float], None] | None = center_button_command
    
    # initialize tkinter variables
    self._left_button_var: tkinter.Variable | None = left_button_var
    self._right_button_var: tkinter.Variable | None = right_button_var
    self._center_button_var: tkinter.Variable | None = center_button_var

    self._variable_callback_blocked: bool = False
    self._variable_callback_name: list[str | None] = [None, None, None]
    
    # when button blocking is true, right and left buttons cannot move past the center buttons position
    # when false, moving left and right button can chenge the position and values of the center button
    self._button_blocking: bool = button_blocking 
    
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self._canvas = CTkCanvas(master=self,
                             highlightthickness=0,
                             width=self._apply_widget_scaling(self._current_width),
                             height=self._apply_widget_scaling(self._current_height))
    
    self._canvas.grid(column=0, row=0, rowspan=1, columnspan=1, sticky="nswe")

    self._draw_engine = CustomDrawEngine(self._canvas)
    
    # change variable individually
    if self._left_button_var is not None:
      self._variable_callback_name[0] = self._left_button_var.trace_add("write", lambda *args: self._on_left_button_var_change())
      self.set("start_time", self._left_button_var.get(), from_variable_callback=True)

    if self._right_button_var is not None:
      self._variable_callback_name[1] = self._right_button_var.trace_add("write", lambda *args: self._on_right_button_var_change())
      self.set("end_time", self._right_button_var.get(), from_variable_callback=True)
    
    if self._center_button_var is not None:
      self._variable_callback_name[2] = self._center_button_var.trace_add("write", lambda *args: self._on_center_button_var_change())
      self.set("current_time", self._center_button_var.get(), from_variable_callback=True)
    
    self._draw()
    
    self._set_cursor()
    self._create_bindings()

  def _set_scaling(self, *args, **kwargs) -> None:
    super()._set_scaling(*args, **kwargs)

    self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                            height=self._apply_widget_scaling(self._desired_height))
    self._draw(no_color_updates=True)

  def _set_dimensions(self, width=None, height=None) -> None:
    super()._set_dimensions(width, height)

    self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                          height=self._apply_widget_scaling(self._desired_height))
    self._draw()
  
  def _set_cursor(self):
    if self._state == "normal" and self._cursor_manipulation_enabled:
      if sys.platform == "darwin":
        self.configure(cursor="pointinghand")
      elif sys.platform.startswith("win"):
        self.configure(cursor="hand2")
      elif sys.platform == "linux":
        self.configure(cursor="hand2")

    elif self._state == "disabled" and self._cursor_manipulation_enabled:
      if sys.platform == "darwin":
        self.configure(cursor="arrow")
      elif sys.platform.startswith("win"):
        self.configure(cursor="arrow")
      elif sys.platform == "linux":
        self.configure(cursor="arrow")
  
  def _draw(self, no_color_updates: bool=False) -> None:
    super()._draw(no_color_updates)
    
    if self._orientation == "horizontal":
      orientation = "w"
    elif self._orientation == "vertical":
      orientation = "s"
    else:
      orientation = "w"

    requires_recoloring: bool = self._draw_engine.draw_rounded_slider_with_border_and_3_buttons(
                                                          width = self._apply_widget_scaling(self._current_width), 
                                                          height = self._apply_widget_scaling(self._current_height),
                                                          corner_radius = self._apply_widget_scaling(self._corner_radius),
                                                          border_width = self._apply_widget_scaling(self._border_width),
                                                          
                                                          outer_button_length = self._apply_widget_scaling(self._outer_button_length),
                                                          outer_button_corner_radius = self._apply_widget_scaling(self._outer_button_corner_radius),
                                                          center_button_corner_radius = self._apply_widget_scaling(self._center_button_corner_radius),

                                                          lbutton_value = self._lbutton_value,
                                                          rbutton_value = self._rbutton_value,
                                                          cbutton_value = self._cbutton_value,
                                                          orientation = orientation
                                                      )
    
    if no_color_updates or requires_recoloring is False:
      return
    
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
      
    if (self._hover_state and self._hover) is True:
      self._canvas.itemconfig("center_button_parts",
                              fill=self._apply_appearance_mode(self._button_hover_color),
                              outline=self._apply_appearance_mode(self._button_hover_color))
    else:
      self._canvas.itemconfig("center_button_parts",
                              fill=self._apply_appearance_mode(self._button_color),
                              outline=self._apply_appearance_mode(self._button_color))
  
  def _create_bindings(self, sequence: str | None = None) -> None:
    if sequence is None or sequence == "<Enter>":
      self._canvas.tag_bind("left_button_parts", "<Enter>", self._lbutton_on_enter)
      self._canvas.tag_bind("right_button_parts", "<Enter>", self._rbutton_on_enter)
      self._canvas.tag_bind("center_button_parts", "<Enter>", self._cbutton_on_enter)
    if sequence is None or sequence == "<Leave>":
      self._canvas.tag_bind("left_button_parts", "<Leave>", self._lbutton_on_leave)
      self._canvas.tag_bind("right_button_parts", "<Leave>", self._rbutton_on_leave)
      self._canvas.tag_bind("center_button_parts", "<Leave>", self._cbutton_on_leave)
    if sequence is None or sequence == "<Button-1>":
      self._canvas.bind("<Button-1>", self._clicked)
    if sequence is None or sequence == "<B1-Motion>":
      self._canvas.bind("<B1-Motion>", self._clicked)

  def _lbutton_on_enter(self, event=0) -> None:
    if self._state != "normal":
      return
    
    if self._hover is False:
      return
    
    self._hover_state = True
    self._canvas.itemconfig("left_button_parts",
                            fill=self._apply_appearance_mode(self._button_hover_color),
                            outline=self._apply_appearance_mode(self._button_hover_color))
  
  def _rbutton_on_enter(self, event=0) -> None:
    if self._state != "normal":
      return
    
    if self._hover is False:
      return
    
    self._hover_state = True
    self._canvas.itemconfig("right_button_parts",
                            fill=self._apply_appearance_mode(self._button_hover_color),
                            outline=self._apply_appearance_mode(self._button_hover_color))
  
  def _cbutton_on_enter(self, event=0) -> None:
    if self._state != "normal":
      return
    
    if self._hover is False:
      return
    
    self._hover_state = True
    self._canvas.itemconfig("center_button_parts",
                            fill=self._apply_appearance_mode(self._button_hover_color),
                            outline=self._apply_appearance_mode(self._button_hover_color))
  
  def _lbutton_on_leave(self, event=0) -> None:
    self._hover_state = False
    self._canvas.itemconfig("left_button_parts",
                            fill=self._apply_appearance_mode(self._button_color),
                            outline=self._apply_appearance_mode(self._button_color))
  
  def _rbutton_on_leave(self, event=0) -> None:
    self._hover_state = False
    self._canvas.itemconfig("right_button_parts",
                            fill=self._apply_appearance_mode(self._button_color),
                            outline=self._apply_appearance_mode(self._button_color))
  
  def _cbutton_on_leave(self, event=0) -> None:
    self._hover_state = False
    self._canvas.itemconfig("center_button_parts",
                            fill=self._apply_appearance_mode(self._button_color),
                            outline=self._apply_appearance_mode(self._button_color))

  def _clicked(self, event=0) -> None:
    if self._state != "normal":
      return

    tags = self._canvas.gettags("current")
    
    if "left_button_parts" in tags:
      self._left_button_move_handler(event)
    elif "center_button_parts" in tags:
      self._center_button_move_handler(event)
    elif "right_button_parts" in tags:
      self._right_button_move_handler(event)
  
  def _left_button_move_handler(self, event=0) -> None:
    # handles the calculations to move the left button
    move_cbutton = False

    if self._orientation == "horizontal":
      self._lbutton_value = self._reverse_widget_scaling(event.x / self._canvas.winfo_width())
    else:
      self._lbutton_value = 1 - self._reverse_widget_scaling(event.y / self._canvas.winfo_height())
    
    if self._lbutton_value < 0:
      self._lbutton_value = 0

    if not self._button_blocking:
      if self._lbutton_value > self._rbutton_value:
        self._lbutton_value = self._rbutton_value
      
      if self._lbutton_value > self._cbutton_value:
        move_cbutton = True
      
    # left button cannot move center button if button blocking true
    else:
      if self._lbutton_value > self._cbutton_value:
        self._lbutton_value = self._cbutton_value
      
    self._left_output_value = self._round_to_step_size(self._from_ + (self._lbutton_value * (self._to - self._from_)))
    self._lbutton_value = (self._left_output_value - self._from_) / (self._to - self._from_)
    
    if move_cbutton:
      self._center_output_value = self._left_output_value
      self._cbutton_value = self._lbutton_value

    # run command associated with left button
    if self._left_button_command is not None:
      self._left_button_command(self._left_output_value)
    
    # set left varaibles
    if self._left_button_var is not None:
      self._variable_callback_blocked = True
      self._left_button_var.set(self._left_output_value)
      self._variable_callback_blocked = False
    
    if self._center_button_var is not None and move_cbutton:
      self._variable_callback_blocked = True
      self._center_button_var.set(self._center_output_value)
      self._variable_callback_blocked = False

    
    self._draw(no_color_updates=False)

  def _right_button_move_handler(self, event=0) -> None:
    # handles the calculations to move the right button
    move_cbutton = False
    
    if self._orientation == "horizontal":
        self._rbutton_value = self._reverse_widget_scaling(event.x / self._canvas.winfo_width())
    else:
      self._rbutton_value = 1 - self._reverse_widget_scaling(event.y / self._canvas.winfo_height())

    if self._rbutton_value >= 1:
        self._rbutton_value = 1

    if not self._button_blocking:
      if self._rbutton_value < self._lbutton_value:
        self._rbutton_value = self._lbutton_value

      if self._rbutton_value < self._cbutton_value:
        move_cbutton = True  

    # right button cannot move center button if button blocking true
    else:    
      if self._rbutton_value < self._cbutton_value:
        self._rbutton_value = self._cbutton_value 
        
    self._right_output_value = self._round_to_step_size(self._from_ + (self._rbutton_value * (self._to - self._from_)))
    self._rbutton_value = (self._right_output_value - self._from_) / (self._to - self._from_)
      
    # run command associated with rightr button
    if self._right_button_command is not None:
      self._right_button_command(self._right_output_value)

    if move_cbutton:
      self._center_output_value = self._right_output_value
      self._cbutton_value = self._rbutton_value
        
    # set right varaibles
    if self._right_button_var is not None:
      self._variable_callback_blocked = True
      self._right_button_var.set(self._right_output_value)
      self._variable_callback_blocked = False
    
    if self._center_button_var is not None and move_cbutton:
      self._variable_callback_blocked = True
      self._center_button_var.set(self._center_output_value)
      self._variable_callback_blocked = False
    
    self._draw(no_color_updates=False)
  
  def _center_button_move_handler(self, event=0) -> None:
    # change the center buttons location on the bar and set output values
    if self._orientation == "horizontal":
      self._cbutton_value = self._reverse_widget_scaling(event.x / self._canvas.winfo_width())
    else:
      self._cbutton_value = 1 - self._reverse_widget_scaling(event.y / self._canvas.winfo_height())
    
    if self._cbutton_value < self._lbutton_value:
      self._cbutton_value = self._lbutton_value 
    elif self._cbutton_value > self._rbutton_value:
      self._cbutton_value = self._rbutton_value 
      
    self._center_output_value = self._round_to_step_size(self._from_ + (self._cbutton_value * (self._to - self._from_)))
    self._cbutton_value = (self._center_output_value - self._from_) / (self._to - self._from_)
    
    # run command associated with center button
    if self._center_button_command is not None:
      self._center_button_command(self._center_output_value)
    
    # set center varaibles
    if self._center_button_var is not None:
      self._variable_callback_blocked = True
      self._center_button_var.set(self._center_output_value)
      self._variable_callback_blocked = False
    
    self._draw(no_color_updates=False)
  
  def _round_to_step_size(self, value) -> float:
    step_index = round((value - self._from_) / self._step_size)
    value = self._from_ + step_index * self._step_size
    return value

  def _destroy(self) -> None:
    # remove variable_callback from variable callbacks if variable exists
    if self._left_button_var is not None and self._variable_callback_name[0] is not None:
      self._left_button_var.trace_remove("write", self._variable_callback_name[0])
    
    if self._right_button_var is not None and self._variable_callback_name[1] is not None:
      self._right_button_var.trace_remove("write", self._variable_callback_name[1])
    
    if self._center_button_var is not None and self._variable_callback_name[2] is not None:
      self._center_button_var.trace_remove("write", self._variable_callback_name[2])

    super().destroy()

  def bind(self, sequence: str | None= None, command: Callable[[Any], int | float] | None = None, add: str | bool = True) -> None:
    """ called on the tkinter.Canvas """
    if not (add == "+" or add is True):
      add = "+"
    self._canvas.bind(sequence, command, add=add)

  def unbind(self, sequence: str | None = None, funcid: str | None = None) -> None:
    """ called on the tkinter.Label and tkinter.Canvas """
    if funcid is not None:
      raise ValueError("'funcid' argument can only be None, because there is a bug in" +
                       " tkinter and its not clear whether the internal callbacks will be unbinded or not")

    self._canvas.unbind(sequence, None)
    self._create_bindings(sequence=sequence)  # restore internal callbacks for sequence
  
  def configure(self, require_redraw=False, **kwargs) -> None:
    if "corner_radius" in kwargs:
      self._corner_radius = kwargs.pop("corner_radius")
      require_redraw = True

    if "outer_button_corner_radius" in kwargs:
      self._outer_button_corner_radius = kwargs.pop("outer_button_corner_radius")
      require_redraw = True
  
    if "center_button_corner_radius" in kwargs:
      self._center_button_corner_radius = kwargs.pop("center_button_corner_radius")
      require_redraw = True

    if "border_width" in kwargs:
      self._border_width = kwargs.pop("border_width")
      require_redraw = True

    if "outer_button_length" in kwargs:
      self._outer_button_length = kwargs.pop("outer_button_length")
      require_redraw = True

    if "fg_color" in kwargs:
      self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
      require_redraw = True

    if "border_color" in kwargs:
      self._border_color = self._check_color_type(kwargs.pop("border_color"), transparency=True)
      require_redraw = True

    if "progress_color" in kwargs:
      self._progress_color = self._check_color_type(kwargs.pop("progress_color"), transparency=True)
      require_redraw = True

    if "button_color" in kwargs:
      self._button_color = self._check_color_type(kwargs.pop("button_color"))
      require_redraw = True

    if "button_hover_color" in kwargs:
      self._button_hover_color = self._check_color_type(kwargs.pop("button_hover_color"))
      require_redraw = True

    if "from_" in kwargs:
      new_from = kwargs.pop("from_")
      if new_from >= self._to:
        raise ValueError("from_ value cannot be greater thet to value")
      
      self._from_ = new_from

    if "to" in kwargs:
      new_to = kwargs.pop("to")
      if new_to <= self._from_:
        raise ValueError("to value cannot be less than current from_ value")
      
      self._to = new_to

    if "state" in kwargs:
      self._state = kwargs.pop("state")
      self._set_cursor()
      require_redraw = True

    if "number_of_steps" in kwargs:
      new_steps = kwargs.pop("number_of_steps")
      if new_steps <= 1:
        raise ValueError("number_of_steps must be any value above 1")
      
      self._number_of_steps = new_steps
      self._step_size = (self._to - self._from_) / self._number_of_steps
      
    if "hover" in kwargs:
      self._hover = kwargs.pop("hover")
    
    if "left_button_command" in kwargs:
      self._left_button_command = kwargs.pop("left_button_command")
    
    if "right_button_command" in kwargs:
      self._right_button_command = kwargs.pop("right_button_command")
    
    if "center_button_command" in kwargs:
      self._center_button_command = kwargs.pop("center_button_command")

    if "orientation" in kwargs:
      self._orientation = kwargs.pop("orientation").lower()
      require_redraw = True

    super().configure(require_redraw=require_redraw, **kwargs)
  
  def cget(self, attribute_name: str) -> Any:
    if attribute_name == "corner_radius":
      return self._corner_radius
    elif attribute_name == "outer_button_corner_radius":
      return self._outer_button_corner_radius
    elif attribute_name == "center_button_corner_radius":
      return self._center_button_corner_radius
    elif attribute_name == "border_width":
      return self._border_width
    elif attribute_name == "outer_button_length":
      return self._outer_button_length

    elif attribute_name == "fg_color":
      return self._fg_color
    elif attribute_name == "border_color":
      return self._border_color
    elif attribute_name == "progress_color":
      return self._progress_color
    elif attribute_name == "button_color":
      return self._button_color
    elif attribute_name == "button_hover_color":
      return self._button_hover_color

    elif attribute_name == "from_":
      return self._from_
    elif attribute_name == "to":
      return self._to
    elif attribute_name == "state":
      return self._state
    elif attribute_name == "number_of_steps":
      return self._number_of_steps
    elif attribute_name == "hover":
      return self._hover
    elif attribute_name == "left_button_command":
      return self._left_button_command
    elif attribute_name == "right_button_command":
      return self._right_button_command
    elif attribute_name == "center_button_command":
      return self._center_button_command
    elif attribute_name == "orientation":
      return self._orientation

    else:
      return super().cget(attribute_name)
  
  def get(self, attribute_name: str) -> float:
    if attribute_name == "start_time":
      return self._left_output_value
    elif attribute_name == "end_time":
      return self._right_output_value
    elif attribute_name == "current_time":
      return self._center_output_value
    
    else:
      raise AttributeError(f"{attribute_name} is not attribute of CTkTrimSlider. Cannot retrieve any values.")
  
  def set(self, attribute_name, input_value, from_variable_callback=False) -> None:
    if attribute_name == "start_time":
      if input_value > self._center_output_value:
        input_value = self._center_output_value 
      elif input_value < self._from_:
        input_value = self._from_
      
      self._left_output_value = self._round_to_step_size(input_value)
      self._lbutton_value = (self._left_output_value - self._from_) / (self._to - self._from_)
      
    elif attribute_name == "current_time":
      if input_value > self._right_output_value:
        input_value = self._right_output_value 
      elif input_value < self._left_output_value:
        input_value = self._left_output_value 
      
      self._center_output_value = self._round_to_step_size(input_value)
      self._cbutton_value = (self._center_output_value - self._from_) / (self._to - self._from_)
      
    elif attribute_name == "end_time":
      if input_value > self._to :
        input_value = self._to
      elif input_value < self._center_output_value:
        input_value = self._center_output_value
      
      self._right_output_value = self._round_to_step_size(input_value)
      self._rbutton_value = (self._right_output_value - self._from_) / (self._to - self._from_)
      
    if not from_variable_callback:
      self._variable_callback_blocked = True

      if attribute_name == "start_time" and self._left_button_var is not None:
        self._left_button_var.set(self._left_output_value)

      elif attribute_name == "current_time" and self._center_button_var is not None:
        self._center_button_var.set(self._center_output_value)

      elif attribute_name == "end_time" and self._right_button_var is not None:
        self._right_button_var.set(self._right_output_value)

      self._variable_callback_blocked = False
    
    self._draw(no_color_updates=False)

  def _on_left_button_var_change(self) -> None:
    if self._variable_callback_blocked:
      return
    
    if self._left_button_var is None:
      return

    self._variable_callback_blocked = True
    self.set("start_time", self._left_button_var.get(), from_variable_callback=True)
    self._variable_callback_blocked = False
  
  def _on_center_button_var_change(self) -> None:
    if self._variable_callback_blocked:
      return

    if self._center_button_var is None:
      return
    
    self._variable_callback_blocked = True
    self.set("current_time", self._center_button_var.get(), from_variable_callback=True)
    self._variable_callback_blocked = False
  
  def _on_right_button_var_change(self) -> None:
    if self._variable_callback_blocked:
      return
    
    if self._right_button_var is None:
      return
    
    self._variable_callback_blocked = True
    self.set("end_time", self._right_button_var.get(), from_variable_callback=True)
    self._variable_callback_blocked = False

  def focus(self) -> Any:
    return self._canvas.focus()

  def focus_set(self) -> Any:
    return self._canvas.focus_set()

  def focus_force(self) -> Any:
    return self._canvas.focus_force()