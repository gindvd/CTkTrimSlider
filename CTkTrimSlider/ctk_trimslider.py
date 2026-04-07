
import tkinter
import sys
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
               number_of_steps: int | None = None,
               state: str = "normal",
               hover: bool = True,
               orientation: str = "horizontal",
               
               lbutton_command: Callable[[Any], int | float] | None = None,
               rbutton_command: Callable[[Any], int | float] | None = None,
               cbutton_command: Callable[[Any], int | float] | None = None,
               
               lbutton_variable: tkinter.Variable | None = None,
               rbutton_variable: tkinter.Variable | None = None,
               cbutton_variable: tkinter.Variable | None = None,
               
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
    
    # center button shape
    self._center_button_corner_radius: int | float = ThemeManager.theme["CTkSlider"]["button_corner_radius"] if center_button_corner_radius is None else center_button_corner_radius
    
    self._outer_button_corner_radius: int | float = ThemeManager.theme["CTkSlider"]["button_corner_radius"] if outer_button_corner_radius is None else outer_button_corner_radius
    
    if from_ >= to:
      raise IndexError
    
    self._from_:int = from_
    self._to: int = to
    self._number_of_steps: int  = width if number_of_steps is None else number_of_steps
    self._starttime_output_value: int| float = 0
    self._currenttime_output_value: int | float = 0
    self._endtime_output_value: int | float = 0
    
    self._state: str = state
    self._hover: bool = hover
    self._hover_state: bool = False
    self._orientation: str = orientation
    
    # set initial left, right, and center button values
    self._starttime_value: float = 0
    self._endtime_value: float = 1
    self._currenttime_value: float = 0.5
    
    self._lbutton_command = lbutton_command
    self._rbutton_command = rbutton_command
    self._cbutton_command = cbutton_command
    
    self._active = None
    
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self._canvas = CTkCanvas(master=self,
                             highlightthickness=0,
                             width=self._apply_widget_scaling(self._current_width),
                             height=self._apply_widget_scaling(self._current_height))
    
    self._canvas.grid(column=0, row=0, rowspan=1, columnspan=1, sticky="nswe")

    self._draw_engine = CustomDrawEngine(self._canvas)
    self._draw()
    
    self._set_cursor()
    self._create_bindings()

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
  
  def _set_cursor(self):
    if self._state == "normal" and self._cursor_manipulation_enabled:
      if sys.platform == "darwin":
        self.configure(cursor="pointinghand")
      elif sys.platform.startswith("win"):
        self.configure(cursor="hand2")

    elif self._state == "disabled" and self._cursor_manipulation_enabled:
      if sys.platform == "darwin":
        self.configure(cursor="arrow")
      elif sys.platform.startswith("win"):
        self.configure(cursor="arrow")
  
  def _draw(self, no_color_updates: bool=False) -> None:
    super()._draw(no_color_updates)
    
    if self._orientation.lower() == "horizontal":
      orientation = "w"
    elif self._orientation.lower() == "vertical":
      orientation = "s"
    else:
      orientation = "w"

    requires_recoloring: bool = self._draw_engine.draw_rounded_slider_with_border_and_3_buttons(
                                                width = self._apply_widget_scaling(self._desired_width), 
                                                height = self._apply_widget_scaling(self._desired_height),
                                                corner_radius = self._apply_widget_scaling(self._corner_radius),
                                                border_width = self._apply_widget_scaling(self._border_width),
                                                
                                                outer_button_length = self._apply_widget_scaling(self._outer_button_length),
                                                outer_button_corner_radius = self._apply_widget_scaling(self._outer_button_corner_radius),

                                                center_button_corner_radius = self._apply_widget_scaling(self._center_button_corner_radius),

                                                lbutton_value = self._starttime_value,
                                                rbutton_value = self._endtime_value,
                                                cbutton_value = self._currenttime_value,
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
  
  def _create_bindings(self, sequence: str | None = None):
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
    if sequence is None or sequence == "ButtonRelease-1":
      self._canvas.bind("<ButtonRelease-1>", lambda x: setattr(self, "_active", None))
  
  def _lbutton_on_enter(self, event=0):
    if self._state != "normal":
      return
    
    if self._hover is False:
      return
    
    self._hover_state = True
    self._canvas.itemconfig("left_button_parts",
                            fill=self._apply_appearance_mode(self._button_hover_color),
                            outline=self._apply_appearance_mode(self._button_hover_color))
  
  def _rbutton_on_enter(self, event=0):
    if self._state != "normal":
      return
    
    if self._hover is False:
      return
    
    self._hover_state = True
    self._canvas.itemconfig("right_button_parts",
                            fill=self._apply_appearance_mode(self._button_hover_color),
                            outline=self._apply_appearance_mode(self._button_hover_color))
  
  def _cbutton_on_enter(self, event=0):
    if self._state != "normal":
      return
    
    if self._hover is False:
      return
    
    self._hover_state = True
    self._canvas.itemconfig("center_button_parts",
                            fill=self._apply_appearance_mode(self._button_hover_color),
                            outline=self._apply_appearance_mode(self._button_hover_color))
  
  def _lbutton_on_leave(self, event=0):
    self._hover_state = False
    self._canvas.itemconfig("left_button_parts",
                            fill=self._apply_appearance_mode(self._button_color),
                            outline=self._apply_appearance_mode(self._button_color))
  
  def _rbutton_on_leave(self, event=0):
    self._hover_state = False
    self._canvas.itemconfig("right_button_parts",
                            fill=self._apply_appearance_mode(self._button_color),
                            outline=self._apply_appearance_mode(self._button_color))
  
  def _cbutton_on_leave(self, event=0):
    self._hover_state = False
    self._canvas.itemconfig("center_button_parts",
                            fill=self._apply_appearance_mode(self._button_color),
                            outline=self._apply_appearance_mode(self._button_color))

  def _clicked(self, event=0):
    if self._state != "normal":
      return
    
    tags = self._canvas.find_withtag("current")

    if "left_button_parts" in tags:
      self._active = "left"
    elif "center_button_parts" in tags:
      self._active = "center"
    elif "right_button_parts" in tags:
      self._active = "right"

    self._move_handle(event)
    
  def _move_handle(self, event):
    if self._active == "left":
      if self._orientation.lower() == "horizontal":
        self._starttime_value = self._reverse_widget_scaling(event.x / self._current_width)
      else:
        self._starttime_value = 1 - self._reverse_widget_scaling(event.y / self._current_height)
      
      if self._starttime_value < 0:
        self._starttime_value = 0
      elif self._starttime_value >= self._currenttime_value:
        self._starttime_value = self._currenttime_value - ((self._to - self._from_) / self._number_of_steps)
        
      self._starttime_output_value = self._round_to_step_size(self._from_ + (self._starttime_value * (self._to - self._from_)))
      self._starttime_value = (self._starttime_output_value - self._from_) / (self._to - self._from_)
      
      if self._lbutton_command is not None:
        self._lbutton_command(self._starttime_output_value)
    
    elif self._active == "center":
      if self._orientation.lower() == "horizontal":
        self._currenttime_value = self._reverse_widget_scaling(event.x / self._current_width)
      else:
        self._currenttime_value = 1 - self._reverse_widget_scaling(event.y / self._current_height)
      
      if self._currenttime_value <= self._starttime_value:
        self._currenttime_value = self._starttime_value + ((self._to - self._from_) / self._number_of_steps)
      elif self._currenttime_value >= self._endtime_value:
        self._currenttime_value = self._endtime_value - ((self._to - self._from_) / self._number_of_steps)
        
      self._currenttime_output_value = self._round_to_step_size(self._from_ + (self._currenttime_value * (self._to - self._from_)))
      self._currenttime_value = (self._currenttime_output_value - self._from_) / (self._to - self._from_)
      
      if self._cbutton_command is not None:
        self._cbutton_command(self._currenttime_output_value)
    
    elif self._active == "right":
      if self._orientation.lower() == "horizontal":
        self._endtime_value = self._reverse_widget_scaling(event.x / self._current_width)
      else:
        self._endtime_value = 1 - self._reverse_widget_scaling(event.y / self._current_height)
      
      if self._endtime_value >= 1:
        self._endtime_value = 1
      elif self._endtime_value <= self._currenttime_value:
        self._endtime_value = self._currenttime_value + ((self._to - self._from_) / self._number_of_steps)
        
      self._endtime_output_value = self._round_to_step_size(self._from_ + (self._endtime_value * (self._to - self._from_)))
      self._endtime_value = (self._endtime_output_value - self._from_) / (self._to - self._from_)
      
      if self._rbutton_command is not None:
        self._rbutton_command(self._endtime_output_value)
    
    # redraws the slider with the click button moved to it's new value
    self._draw(no_color_updates=False)
  
  def _round_to_step_size(self, value) -> float:
    if self._number_of_steps is not None:
      step_size = (self._to - self._from_) / self._number_of_steps
      value = self._to - (round((self._to - value) / step_size) * step_size)
      return value
    else:
      return value
    
  def bind(self, sequence: str | None= None, command: Callable[[Any], int | float] | None = None, add: str | bool = True):
    """ called on the tkinter.Canvas """
    if not (add == "+" or add is True):
      raise ValueError("'add' argument can only be '+' or True to preserve internal callbacks")
    self._canvas.bind(sequence, command, add=True)

  def unbind(self, sequence: str | None = None, funcid: str | None = None):
    """ called on the tkinter.Label and tkinter.Canvas """
    if funcid is not None:
      raise ValueError("'funcid' argument can only be None, because there is a bug in" +
                       " tkinter and its not clear whether the internal callbacks will be unbinded or not")

    self._canvas.unbind(sequence, None)
    self._create_bindings(sequence=sequence)  # restore internal callbacks for sequence
    
  def configure(self, require_redraw=False, **kwargs):
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
      self._from_ = kwargs.pop("from_")

    if "to" in kwargs:
      self._to = kwargs.pop("to")

    if "state" in kwargs:
      self._state = kwargs.pop("state")
      self._set_cursor()
      require_redraw = True

    if "number_of_steps" in kwargs:
      self._number_of_steps = kwargs.pop("number_of_steps")

    if "hover" in kwargs:
      self._hover = kwargs.pop("hover")
    
    if "lbutton_command" in kwargs:
      self._lbutton_command = kwargs.pop("lbutton_command")
    
    if "rbutton_command" in kwargs:
      self._rbutton_command = kwargs.pop("rbutton_command")
    
    if "cbutton_command" in kwargs:
      self._cbutton_command = kwargs.pop("cbutton_command")

    if "orientation" in kwargs:
      self._orientation = kwargs.pop("orientation")
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
    elif attribute_name == "lbutton_command":
      return self._lbutton_command
    elif attribute_name == "rbutton_command":
      return self._rbutton_command
    elif attribute_name == "cbutton_command":
      return self._cbutton_command
    elif attribute_name == "orientation":
      return self._orientation

    else:
      return super().cget(attribute_name)
  
  def get(self, value_name: str) -> None:
    if value_name == "start_time":
      return self._starttime_output_value
    elif value_name == "end_time":
      return self._endtime_output_value
    elif value_name == "current_time":
      return self._currenttime_output_value
    
    else:
      raise AttributeError
  
  def set(self, value_name, input_value):
    if value_name == "start_time":
      if input_value > self._currenttime_output_value:
        input_value = self._currenttime_output_value
      elif input_value < self._from_:
        input_value = self._from_
      
      self._starttime_output_value = self._round_to_step_size(input_value)
      self._starttime_value = (self._starttime_output_value - self._from_) / (self._to - self._from_)
    
    elif value_name == "current_time":
      if input_value > self._endtime_output_value:
        input_value = self._endtime_output_value
      elif input_value < self._starttime_output_value:
        input_value = self._starttime_output_value
      
      self._currenttime_output_value = self._round_to_step_size(input_value)
      self._currenttime_value = (self._currenttime_output_value - self._from_) / (self._to - self._from_)
    
    elif value_name == "end_time":
      if input_value > self._to:
        self._endtime_output_value = self._to
      elif input_value < self._currenttime_output_value:
        input_value = self._currenttime_output_value
      
      self._endtime_output_value = self._round_to_step_size(input_value)
      self._endtime_value = (self._endtime_output_value - self._from_) / (self._to - self._from_)
      
    self._draw(no_color_updates=False)
  
  def _destroy(self):
    super().destroy()

  def focus(self):
    return self._canvas.focus()

  def focus_set(self):
    return self._canvas.focus_set()

  def focus_force(self):
    return self._canvas.focus_force()