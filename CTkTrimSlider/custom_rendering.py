import tkinter

import math

from customtkinter.windows.widgets.core_rendering import DrawEngine
from customtkinter.windows.widgets.core_rendering import CTkCanvas

class CustomDrawEngine(DrawEngine):
  """
  Custom Draw Engine to draw slider with 2 outer trim slider buttons,
  and an center seek button
  
   Visual Representation of the trim slider:
  
  -----|=====•=====|----
  """

  # Use circle_shapes on macOS to avoid rectangular slider heads, font_shapes elsewhere
  preferred_drawing_method: str = "font_shapes"

  def __init__(self, canvas: CTkCanvas) -> None:
    super().__init__(canvas)
    
  # function to start drawing slider bar and 3 buttons onto a canvas widget
  def draw_rounded_slider_with_border_and_3_buttons(self,
                                                    width: int | float,
                                                    height: int | float,
                                                    corner_radius: int | float,
                                                    border_width: int | float,
                                                    
                                                    outer_button_width: int | float,
                                                    outer_button_height: int | float,
                                                    outer_button_corner_radius: int | float,

                                                    center_button_width: int | float,
                                                    center_button_corner_radius: int | float,

                                                    lbutton_value: int | float,
                                                    rbutton_value: int | float,
                                                    mbutton_value: int | float,
                                                    
                                                    orientation: str) -> bool:
    
    # round _current_width and _current_height and restrict them to even values only
    if self._round_width_to_even_numbers:
      width = math.floor(width / 2) * 2 
    if self._round_height_to_even_numbers:
      height = math.floor(height / 2) * 2
    
    # restrict corner_radius if it's too larger
    if corner_radius > width / 2 or corner_radius > height / 2:  
      corner_radius = min(width / 2, height / 2)
    
    # restrict outer_button_corner_radius if too large
    if outer_button_corner_radius > outer_button_width / 2 or outer_button_corner_radius > outer_button_width / 2:  
      outer_button_corner_radius = min(outer_button_width / 2, outer_button_height / 2)
    
    # restrict center_button_corner_radius if too large
    if center_button_corner_radius > center_button_width / 2:  
      center_button_corner_radius = center_button_width / 2

    outer_button_width = round(outer_button_width)
    outer_button_height = round(outer_button_height)
    center_button_width = round(center_button_width)

    border_width = round(border_width)

    outer_button_corner_radius = round(outer_button_corner_radius)
    center_button_corner_radius = round(center_button_corner_radius)
    corner_radius = self._DrawEngine__calc_optimal_corner_radius(corner_radius)  # optimize corner_radius for different drawing methods (different rounding)

    if corner_radius >= border_width:
      inner_corner_radius = corner_radius - border_width
    else:
      inner_corner_radius = 0
    
    if self.preferred_drawing_method == "font_shapes":
      return self.__draw_rounded_slider_with_border_and_3_buttons_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                              outer_button_width, outer_button_height, outer_button_corner_radius,
                                                                              center_button_width, center_button_corner_radius,
                                                                              lbutton_value, rbutton_value, mbutton_value, orientation)
    
  def __draw_rounded_slider_with_border_and_3_buttons_font_shapes(self,
                                                    width: int | float,
                                                    height: int | float,
                                                    corner_radius: int | float,
                                                    border_width: int | float,
                                                    inner_corner_radius: int | float,
                                                    
                                                    outer_button_width: int | float,
                                                    outer_button_height: int | float,
                                                    outer_button_corner_radius: int | float,

                                                    center_button_width: int | float,
                                                    center_button_corner_radius: int | float,

                                                    lbutton_value: int | float,
                                                    rbutton_value: int | float,
                                                    mbutton_value: int | float,
                                                    
                                                    orientation: str) -> bool:
    
    # draw normal progressbar
    requires_recoloring = self._DrawEngine__draw_rounded_progress_bar_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                       lbutton_value, rbutton_value, orientation)  
    
    # create the left slider button as a rectangle with round corners
    # create 4 circles (if not needed, then less)
    if not self._canvas.find_withtag("button_oval_1_a"):
      self._canvas.create_aa_circle(0, 0, 0, tags=("button_oval_1_a", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("button_oval_1_b", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True
    
    if not self._canvas.find_withtag("button_oval_2_a") and outer_button_width > 0:
      self._canvas.create_aa_circle(0, 0, 0, tags=("button_oval_2_a", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("button_oval_2_b", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True

    elif self._canvas.find_withtag("button_oval_2_a") and not outer_button_width > 0:
      self._canvas.delete("button_oval_2_a", "button_oval_2_b")
    
    if not self._canvas.find_withtag("button_oval_4_a") and height > 2 * outer_button_corner_radius:
      self._canvas.create_aa_circle(0, 0, 0, tags=("button_oval_4_a", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("button_oval_4_b", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True

    elif self._canvas.find_withtag("button_oval_4_a") and not height > 2 * outer_button_corner_radius:
      self._canvas.delete("button_oval_4_a", "button_oval_4_b")

    if not self._canvas.find_withtag("button_oval_3_a") and outer_button_width > 0 and height > 2 * outer_button_corner_radius:
      self._canvas.create_aa_circle(0, 0, 0, tags=("button_oval_3_a", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("button_oval_3_b", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True

    elif self._canvas.find_withtag("button_oval_3_a") and not (outer_button_width > 0 and height > 2 * outer_button_corner_radius):
      self._canvas.delete("button_oval_3_a", "button_oval_3_b")
    
    # create the 2 rectangles (if needed)
    if not self._canvas.find_withtag("button_rectangle_1") and outer_button_width > 0:
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("button_rectangle_1", "button_rectangle_part", "button_parts", "left_button_parts"), width=0)
      requires_recoloring = True

    elif self._canvas.find_withtag("slider_rectangle_1") and not outer_button_width > 0:
      self._canvas.delete("button_rectangle_1")
    

    if not self._canvas.find_withtag("button_rectangle_2") and height > 2 * outer_button_corner_radius:
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("button_rectangle_2", "button_rectangle_part", "button_parts", "left_button_parts"), width=0)
      requires_recoloring = True

    elif self._canvas.find_withtag("button_rectangle_2") and not height > 2 * outer_button_corner_radius:
      self._canvas.delete("button_rectangle_2")

      
    # set positions of circles and rectangles
    # draws button on horizontal progress bar
    if orientation == "w":
      left_button_x_position = corner_radius + (outer_button_width / 2) + (width - 2 * corner_radius - outer_button_width) * lbutton_value
      self._canvas.coords("button_oval_1_a", left_button_x_position - (outer_button_width / 2), outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("button_oval_1_b", left_button_x_position - (outer_button_width / 2), outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("button_oval_2_a", left_button_x_position + (outer_button_width / 2), outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("button_oval_2_b", left_button_x_position + (outer_button_width / 2), outer_button_corner_radius, outer_button_corner_radius)      
      self._canvas.coords("button_oval_3_a", left_button_x_position + (outer_button_width / 2), height - outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("button_oval_3_b", left_button_x_position + (outer_button_width / 2), height - outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("button_oval_4_a", left_button_x_position - (outer_button_width / 2), height - outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("button_oval_4_b", left_button_x_position - (outer_button_width / 2), height - outer_button_corner_radius, outer_button_corner_radius)
      

      self._canvas.coords("button_rectangle_1",
                          left_button_x_position - (outer_button_width / 2), 0,
                          left_button_x_position + (outer_button_width / 2), height)
      self._canvas.coords("button_rectangle_2",
                          left_button_x_position - (outer_button_width / 2) - outer_button_corner_radius, outer_button_corner_radius,
                          left_button_x_position + (outer_button_width / 2) + outer_button_corner_radius, height - outer_button_corner_radius)
    
    # draws button on vertical progress bar
    elif orientation == "s":
      left_button_y_position = corner_radius + (outer_button_width / 2) + (height - 2 * corner_radius - outer_button_width) * (1 - lbutton_value)
      self._canvas.coords("button_oval_1_a", outer_button_corner_radius, left_button_y_position - (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("button_oval_1_b", outer_button_corner_radius, left_button_y_position - (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("button_oval_2_a", outer_button_corner_radius, left_button_y_position + (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("button_oval_2_b", outer_button_corner_radius, left_button_y_position + (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("button_oval_3_a", width - outer_button_corner_radius, left_button_y_position + (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("button_oval_3_b", width - outer_button_corner_radius, left_button_y_position + (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("button_oval_4_a", width - outer_button_corner_radius, left_button_y_position - (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("button_oval_4_b", width - outer_button_corner_radius, left_button_y_position - (outer_button_width / 2), outer_button_corner_radius)

      self._canvas.coords("button_rectangle_1",
                          0, left_button_y_position - (outer_button_width / 2),
                          width, left_button_y_position + (outer_button_width / 2))
      self._canvas.coords("button_rectangle_2",
                          outer_button_corner_radius, left_button_y_position - (outer_button_width / 2) - outer_button_corner_radius,
                          width - outer_button_corner_radius, left_button_y_position + (outer_button_width / 2) + outer_button_corner_radius)

    if requires_recoloring:  # new parts were added -> manage z-order
      self._canvas.tag_raise("button_parts")
    
    return requires_recoloring