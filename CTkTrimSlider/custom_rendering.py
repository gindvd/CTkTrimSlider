"""
Custom Draw Engine
Custom draw engine to draw trim slider components on a canvas
Author: David Gingerich
Version 1.0.6
"""

import tkinter

from customtkinter.windows.widgets.core_rendering import DrawEngine
from customtkinter.windows.widgets.core_rendering import CTkCanvas

class CustomDrawEngine(DrawEngine):
  """
  Custom Draw Engine to draw slider with 2 outer trim slider buttons,
  and an center seek button
  
   Visual Representation of the trim slider:
  
  -----|=====•=====|----
  """

  def __init__(self, canvas: CTkCanvas) -> None:
    super().__init__(canvas)

  # function to start drawing slider bar and 3 buttons onto a canvas widget
  def draw_rounded_slider_with_border_and_3_buttons(self,
                                                    width: int | float,
                                                    height: int | float,
                                                    corner_radius: int | float,
                                                    border_width: int | float,

                                                    outer_button_length: int | float,
                                                    outer_button_corner_radius: int | float,
                                                    
                                                    center_button_corner_radius: int | float,

                                                    lbutton_value: int | float,
                                                    rbutton_value: int | float,
                                                    cbutton_value: int | float,
                                                    
                                                    orientation: str) -> bool:
    
    # restrict corner_radius if it's too larger
    if border_width > width / 2 or border_width > height / 2:  
      border_width = min(width / 2, height / 2)
    
    if corner_radius > width / 2 or corner_radius > height / 2:
      corner_radius = min(width / 2, height / 2)

    corner_radius = round(corner_radius)
    border_width = round(border_width)
    
    # restrict outer_button_corner_radius if too large or too small
    outer_button_length = round(outer_button_length)
    center_button_corner_radius = round(center_button_corner_radius /  2.5)

    # scale outer_button_length and center_button_corner_radius proportionally to the cross-axis
    # so buttons resize correctly when the widget is stretched by layout managers
    if orientation == "w":
      cross_axis = height
    else:
      cross_axis = width
    outer_button_length = round(max(outer_button_length, cross_axis * 0.5))
    center_button_corner_radius = round(max(center_button_corner_radius, cross_axis * 0.35))

    # compute corner radius after scaling so it matches the final button length
    outer_button_corner_radius = round(outer_button_length / 2)

    border_width = round(border_width + min(width / border_width, height / border_width))

    if corner_radius >= border_width:
      inner_corner_radius = round(corner_radius - border_width)
    else:
      inner_corner_radius = 0

    
    return self.__draw_rounded_slider_with_border_and_3_buttons_font_shapes(width=width, height=height, border_width=border_width, corner_radius=corner_radius,  
                                                                            inner_corner_radius=inner_corner_radius, outer_button_length=outer_button_length, 
                                                                            outer_button_corner_radius=outer_button_corner_radius, center_button_corner_radius=center_button_corner_radius,  
                                                                            lbutton_value=lbutton_value, rbutton_value=rbutton_value, cbutton_value=cbutton_value, orientation=orientation)
    
  def __draw_rounded_slider_with_border_and_3_buttons_font_shapes(self,
                                                    width: int | float,
                                                    height: int | float,

                                                    border_width: int | float,
                                                    corner_radius: int | float,
                                                    inner_corner_radius: int | float,

                                                    outer_button_length: int | float,
                                                    outer_button_corner_radius: int | float,

                                                    center_button_corner_radius: int | float,

                                                    lbutton_value: int | float,
                                                    rbutton_value: int | float,
                                                    cbutton_value: int | float,
                                                    
                                                    orientation: str) -> bool:
   
    # draw normal progressbar
    requires_recoloring: bool = self._DrawEngine__draw_rounded_progress_bar_with_border_font_shapes(width=width, height=height, border_width=border_width, corner_radius=corner_radius, 
                                                                                                    inner_corner_radius=inner_corner_radius,  progress_value_1=lbutton_value, 
                                                                                                    progress_value_2=rbutton_value, orientation=orientation)

    # New calculations to keep the buttons from occupying the same space when there values are the same
    # does so by changing the distance they can travel and then moving each otf the buttons to the right slightly
    if orientation == "w":
      offset = outer_button_length + center_button_corner_radius
      max_button_range = width - (offset * 2)

      lbutton_x_pos = max_button_range * lbutton_value
      cbutton_x_pos = (max_button_range * cbutton_value) + offset
      rbutton_x_pos = (max_button_range * rbutton_value) + (offset * 2)

    elif orientation == "s":
      offset = outer_button_length + center_button_corner_radius
      max_button_range = height - (offset * 2)

      rbutton_y_pos = max_button_range * (1 - rbutton_value)
      cbutton_y_pos = (max_button_range * (1 - cbutton_value)) + offset
      lbutton_y_pos = (max_button_range * (1 - lbutton_value)) + (offset * 2)
    
    # create the left slider button as a rectangle with round corners  
    if not self._canvas.find_withtag("lbutton_oval_1_a"):
      self._canvas.create_aa_circle(0, 0, 0, tags=("lbutton_oval_1_a", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("lbutton_oval_1_b", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True
    
    if not self._canvas.find_withtag("lbutton_oval_2_a"):
      self._canvas.create_aa_circle(0, 0, 0, tags=("lbutton_oval_2_a", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("lbutton_oval_2_b", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True

    # create the 2 rectangles (if needed)
    if not self._canvas.find_withtag("lbutton_rectangle_1") and outer_button_length > 0:
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("lbutton_rectangle_1", "button_rectangle_part", "button_parts", "left_button_parts"), width=0)
      requires_recoloring = True

    elif self._canvas.find_withtag("lbutton_rectangle_1") and not outer_button_length > 0:
      self._canvas.delete("lbutton_rectangle_1")

    # set positions of circles and rectangles
    # draws button on horizontal progress bar
    if orientation == "w":
      self._canvas.coords("lbutton_oval_1_a", lbutton_x_pos + outer_button_corner_radius, outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_1_b", lbutton_x_pos + outer_button_corner_radius, outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_2_a", lbutton_x_pos + outer_button_corner_radius, height - outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_2_b", lbutton_x_pos + outer_button_corner_radius, height - outer_button_corner_radius, outer_button_corner_radius)

      self._canvas.coords("lbutton_rectangle_1",
                          lbutton_x_pos,
                          outer_button_corner_radius,
                          lbutton_x_pos + outer_button_length,
                          height - outer_button_corner_radius)

    # draws button on vertical progress bar
    elif orientation == "s":
      self._canvas.coords("lbutton_oval_1_a", outer_button_corner_radius, lbutton_y_pos - outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_1_b", outer_button_corner_radius, lbutton_y_pos - outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_2_a", width - outer_button_corner_radius, lbutton_y_pos - outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_2_b", width - outer_button_corner_radius, lbutton_y_pos - outer_button_corner_radius, outer_button_corner_radius)

      self._canvas.coords("lbutton_rectangle_1",
                          outer_button_corner_radius,
                          lbutton_y_pos - outer_button_length,
                          width - outer_button_corner_radius,
                          lbutton_y_pos)
   
   # create the right slider button as a rectangle with round corners  
    if not self._canvas.find_withtag("rbutton_oval_1_a"):
      self._canvas.create_aa_circle(0, 0, 0, tags=("rbutton_oval_1_a", "button_corner_part", "button_parts", "right_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("rbutton_oval_1_b", "button_corner_part", "button_parts", "right_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True
    
    if not self._canvas.find_withtag("rbutton_oval_2_a"):
      self._canvas.create_aa_circle(0, 0, 0, tags=("rbutton_oval_2_a", "button_corner_part", "button_parts", "right_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("rbutton_oval_2_b", "button_corner_part", "button_parts", "right_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True

    # create the 2 rectangles (if needed)
    if not self._canvas.find_withtag("rbutton_rectangle_1") and outer_button_length > 0:
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("rbutton_rectangle_1", "button_rectangle_part", "button_parts", "right_button_parts"), width=0)
      requires_recoloring = True

    elif self._canvas.find_withtag("rbutton_rectangle_1") and not outer_button_length > 0:
      self._canvas.delete("rbutton_rectangle_1")

    # set positions of circles and rectangles
    # draws button on horizontal progress bar
    if orientation == "w":
      self._canvas.coords("rbutton_oval_1_a", rbutton_x_pos - outer_button_corner_radius, outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("rbutton_oval_1_b", rbutton_x_pos - outer_button_corner_radius, outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("rbutton_oval_2_a", rbutton_x_pos - outer_button_corner_radius, height - outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("rbutton_oval_2_b", rbutton_x_pos - outer_button_corner_radius, height - outer_button_corner_radius, outer_button_corner_radius)

      self._canvas.coords("rbutton_rectangle_1",
                          rbutton_x_pos - outer_button_length,
                          outer_button_corner_radius,
                          rbutton_x_pos,
                          height - outer_button_corner_radius)

    # draws button on vertical progress bar
    elif orientation == "s":      
      self._canvas.coords("rbutton_oval_1_a", outer_button_corner_radius, rbutton_y_pos + outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("rbutton_oval_1_b", outer_button_corner_radius, rbutton_y_pos + outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("rbutton_oval_2_a", width - outer_button_corner_radius, rbutton_y_pos + outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("rbutton_oval_2_b", width - outer_button_corner_radius, rbutton_y_pos + outer_button_corner_radius, outer_button_corner_radius)

      self._canvas.coords("rbutton_rectangle_1",
                          outer_button_corner_radius,
                          rbutton_y_pos,
                          width - outer_button_corner_radius,
                          rbutton_y_pos + outer_button_length)
    
    # create the center slider button as a rectangle with round corners  
    if not self._canvas.find_withtag("cbutton_oval_1_a"):
      self._canvas.create_aa_circle(0, 0, 0, tags=("cbutton_oval_1_a", "button_corner_part", "button_parts", "center_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("cbutton_oval_1_b", "button_corner_part", "button_parts", "center_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True

    # set positions of circles and rectangles
    # draws button on horizontal progress bar
    if orientation == "w":
      self._canvas.coords("cbutton_oval_1_a", cbutton_x_pos, height / 2, center_button_corner_radius)
      self._canvas.coords("cbutton_oval_1_b", cbutton_x_pos, height / 2, center_button_corner_radius)

    # draws button on vertical progress bar
    elif orientation == "s":      
      self._canvas.coords("cbutton_oval_1_a", width / 2, cbutton_y_pos, center_button_corner_radius)
      self._canvas.coords("cbutton_oval_1_b", width / 2, cbutton_y_pos, center_button_corner_radius)
    
    if requires_recoloring:  # new parts were added -> manage z-order
      self._canvas.tag_raise("button_parts")
    
    return requires_recoloring