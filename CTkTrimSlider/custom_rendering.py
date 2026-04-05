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

  def __init__(self, canvas: CTkCanvas) -> None:
    super().__init__(canvas)

  # custom renderer render the progress bar background and border, wnetered in the center of the canvas widget
  def __draw_rounded_rect_with_border_font_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int,
                                                  x_offset: int, y_offset: int, exclude_parts: tuple) -> bool:
        
    requires_recoloring = False

    # create border button parts
    if border_width > 0:
      if corner_radius > 0:
        # create canvas border corner parts if not already created, but only if needed, and delete if not needed
        if not self._canvas.find_withtag("border_oval_1_a") and "border_oval_1" not in exclude_parts:
          self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_1_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
          self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_1_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
          requires_recoloring = True
        
        elif self._canvas.find_withtag("border_oval_1_a") and "border_oval_1" in exclude_parts:
            self._canvas.delete("border_oval_1_a", "border_oval_1_b")

        if not self._canvas.find_withtag("border_oval_2_a") and width > 2 * corner_radius and "border_oval_2" not in exclude_parts:
          self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_2_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
          self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_2_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
          requires_recoloring = True

        elif self._canvas.find_withtag("border_oval_2_a") and (not width > 2 * corner_radius or "border_oval_2" in exclude_parts):
          self._canvas.delete("border_oval_2_a", "border_oval_2_b")

        if not self._canvas.find_withtag("border_oval_3_a") and height > 2 * corner_radius \
                                                                    and width > 2 * corner_radius and "border_oval_3" not in exclude_parts:
          self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_3_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
          self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_3_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
          requires_recoloring = True

        elif self._canvas.find_withtag("border_oval_3_a") and (not (height > 2 * corner_radius
                                                                    and width > 2 * corner_radius) or "border_oval_3" in exclude_parts):
          self._canvas.delete("border_oval_3_a", "border_oval_3_b")

        if not self._canvas.find_withtag("border_oval_4_a") and height > 2 * corner_radius and "border_oval_4" not in exclude_parts:
          self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_4_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
          self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_4_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
          requires_recoloring = True
        elif self._canvas.find_withtag("border_oval_4_a") and (not height > 2 * corner_radius or "border_oval_4" in exclude_parts):
          self._canvas.delete("border_oval_4_a", "border_oval_4_b")

        # change position of border corner parts
        self._canvas.coords("border_oval_1_a", x_offset + corner_radius, y_offset + corner_radius, corner_radius)
        self._canvas.coords("border_oval_1_b", x_offset + corner_radius, y_offset + corner_radius, corner_radius)
        self._canvas.coords("border_oval_2_a", x_offset + width - corner_radius, y_offset + corner_radius, corner_radius)
        self._canvas.coords("border_oval_2_b", x_offset + width - corner_radius, y_offset + corner_radius, corner_radius)
        self._canvas.coords("border_oval_3_a", x_offset + width - corner_radius, y_offset + height - corner_radius, corner_radius)
        self._canvas.coords("border_oval_3_b", x_offset + width - corner_radius, y_offset + height - corner_radius, corner_radius)
        self._canvas.coords("border_oval_4_a", x_offset + corner_radius, y_offset + height - corner_radius, corner_radius)
        self._canvas.coords("border_oval_4_b", x_offset + corner_radius, y_offset + height - corner_radius, corner_radius)

      else:
        self._canvas.delete("border_corner_part")  # delete border corner parts if not needed

      # create canvas border rectangle parts if not already created
      if not self._canvas.find_withtag("border_rectangle_1"):
        self._canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_1", "border_rectangle_part", "border_parts"), width=0)
        self._canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_2", "border_rectangle_part", "border_parts"), width=0)
        requires_recoloring = True

      # change position of border rectangle parts
      self._canvas.coords("border_rectangle_1", (x_offset + corner_radius, y_offset, x_offset + width - corner_radius, y_offset + height))
      self._canvas.coords("border_rectangle_2", (x_offset, y_offset + corner_radius, x_offset + width, y_offset + height - corner_radius))

    else:
      self._canvas.delete("border_parts")

    # create inner button parts
    if inner_corner_radius > 0:

      # create canvas border corner parts if not already created, but only if they're needed and delete if not needed
      if not self._canvas.find_withtag("inner_oval_1_a") and "inner_oval_1" not in exclude_parts:
        self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_1_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
        self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_1_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
        requires_recoloring = True

      elif self._canvas.find_withtag("inner_oval_1_a") and "inner_oval_1" in exclude_parts:
        self._canvas.delete("inner_oval_1_a", "inner_oval_1_b")

      if not self._canvas.find_withtag("inner_oval_2_a") and width - (2 * border_width) > 2 * inner_corner_radius and "inner_oval_2" not in exclude_parts:
        self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_2_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
        self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_2_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
        requires_recoloring = True
        
      elif self._canvas.find_withtag("inner_oval_2_a") and (not width - (2 * border_width) > 2 * inner_corner_radius or "inner_oval_2" in exclude_parts):
          self._canvas.delete("inner_oval_2_a", "inner_oval_2_b")

      if not self._canvas.find_withtag("inner_oval_3_a") and height - (2 * border_width) > 2 * inner_corner_radius \
                                                            and width - (2 * border_width) > 2 * inner_corner_radius and "inner_oval_3" not in exclude_parts:
        self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_3_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
        self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_3_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
        requires_recoloring = True

      elif self._canvas.find_withtag("inner_oval_3_a") and (not (height - (2 * border_width) > 2 * inner_corner_radius
                                                              and width - (2 * border_width) > 2 * inner_corner_radius) or "inner_oval_3" in exclude_parts):
        self._canvas.delete("inner_oval_3_a", "inner_oval_3_b")

      if not self._canvas.find_withtag("inner_oval_4_a") and height - (2 * border_width) > 2 * inner_corner_radius and "inner_oval_4" not in exclude_parts:
        self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_4_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
        self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_4_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
        requires_recoloring = True

      elif self._canvas.find_withtag("inner_oval_4_a") and (not height - (2 * border_width) > 2 * inner_corner_radius or "inner_oval_4" in exclude_parts):
        self._canvas.delete("inner_oval_4_a", "inner_oval_4_b")

      # change position of border corner parts
      self._canvas.coords("inner_oval_1_a", x_offset + border_width + inner_corner_radius, y_offset + border_width + inner_corner_radius, inner_corner_radius)
      self._canvas.coords("inner_oval_1_b", x_offset + border_width + inner_corner_radius, y_offset + border_width + inner_corner_radius, inner_corner_radius)
      self._canvas.coords("inner_oval_2_a", x_offset + width - border_width - inner_corner_radius, y_offset + border_width + inner_corner_radius, inner_corner_radius)
      self._canvas.coords("inner_oval_2_b", x_offset + width - border_width - inner_corner_radius, y_offset + border_width + inner_corner_radius, inner_corner_radius)
      self._canvas.coords("inner_oval_3_a", x_offset + width - border_width - inner_corner_radius, y_offset + height - border_width - inner_corner_radius, inner_corner_radius)
      self._canvas.coords("inner_oval_3_b", x_offset + width - border_width - inner_corner_radius, y_offset + height - border_width - inner_corner_radius, inner_corner_radius)
      self._canvas.coords("inner_oval_4_a", x_offset + border_width + inner_corner_radius, y_offset + height - border_width - inner_corner_radius, inner_corner_radius)
      self._canvas.coords("inner_oval_4_b", x_offset + border_width + inner_corner_radius, y_offset + height - border_width - inner_corner_radius, inner_corner_radius)
    else:
      self._canvas.delete("inner_corner_part")  # delete inner corner parts if not needed

    # create canvas inner rectangle parts if not already created
    if not self._canvas.find_withtag("inner_rectangle_1"):
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_1", "inner_rectangle_part", "inner_parts"), width=0)
      requires_recoloring = True

    if not self._canvas.find_withtag("inner_rectangle_2") and inner_corner_radius * 2 < height - (border_width * 2):
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_2", "inner_rectangle_part", "inner_parts"), width=0)
      requires_recoloring = True

    elif self._canvas.find_withtag("inner_rectangle_2") and not inner_corner_radius * 2 < height - (border_width * 2):
      self._canvas.delete("inner_rectangle_2")

    # change position of inner rectangle parts
    self._canvas.coords("inner_rectangle_1", (x_offset + inner_corner_radius + border_width, 
                                              y_offset + border_width, 
                                              x_offset + width - inner_corner_radius - border_width, 
                                              y_offset + height - border_width))
    self._canvas.coords("inner_rectangle_2", (x_offset + border_width, 
                                              y_offset + inner_corner_radius + border_width, 
                                              x_offset + width - border_width, 
                                              y_offset + height - inner_corner_radius - border_width))

    if requires_recoloring:  # new parts were added -> manage z-order
      self._canvas.tag_lower("inner_parts")
      self._canvas.tag_lower("border_parts")
      self._canvas.tag_lower("background_parts")

    return requires_recoloring

  # Custom renderer for progress bar foreground, lowering the height of the bar in side the canvas widget
  def __draw_rounded_progress_bar_with_border_font_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int,
                                                          x_offset: int, y_offset: int, progress_value_1: float, progress_value_2: float, orientation: str) -> bool:

    requires_recoloring, requires_recoloring_2 = False, False

    if inner_corner_radius > 0:
      # create canvas border corner parts if not already created
      if not self._canvas.find_withtag("progress_oval_1_a"):
        self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_1_a", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER)
        self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_1_b", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER, angle=180)
        self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_2_a", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER)
        self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_2_b", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER, angle=180)
        requires_recoloring = True

      if not self._canvas.find_withtag("progress_oval_3_a") and round(inner_corner_radius) * 2 < height - 2 * border_width:
        self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_3_a", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER)
        self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_3_b", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER, angle=180)
        self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_4_a", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER)
        self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_4_b", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER, angle=180)
        requires_recoloring = True

      elif self._canvas.find_withtag("progress_oval_3_a") and not round(inner_corner_radius) * 2 < height - 2 * border_width:
          self._canvas.delete("progress_oval_3_a", "progress_oval_3_b", "progress_oval_4_a", "progress_oval_4_b")

    if not self._canvas.find_withtag("progress_rectangle_1"):
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("progress_rectangle_1", "progress_rectangle_part", "progress_parts"), width=0)
      requires_recoloring = True

    if not self._canvas.find_withtag("progress_rectangle_2") and inner_corner_radius * 2 < height - (border_width * 2):
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("progress_rectangle_2", "progress_rectangle_part", "progress_parts"), width=0)
      requires_recoloring = True

    elif self._canvas.find_withtag("progress_rectangle_2") and not inner_corner_radius * 2 < height - (border_width * 2):
      self._canvas.delete("progress_rectangle_2")

    # horizontal orientation from the bottom
    if orientation == "w":
      requires_recoloring_2 = self.__draw_rounded_rect_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                x_offset, y_offset, ())

      
      # set positions of progress corner parts 
      self._canvas.coords("progress_oval_1_a", 
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_1 + x_offset,
                          border_width + inner_corner_radius + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_1_b", 
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_1 + x_offset,
                          border_width + inner_corner_radius + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_2_a", 
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_2 + x_offset,
                          border_width + inner_corner_radius + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_2_b", 
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_2 + x_offset,
                          border_width + inner_corner_radius + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_3_a", 
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_2 + x_offset,
                          height - border_width - inner_corner_radius + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_3_b", 
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_2 + x_offset,
                          height - border_width - inner_corner_radius + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_4_a", 
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_1 + x_offset,
                          height - border_width - inner_corner_radius + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_4_b", 
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_1 + x_offset,
                          height - border_width - inner_corner_radius + y_offset, inner_corner_radius)

      # set positions of progress rect parts
      self._canvas.coords("progress_rectangle_1",
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_1 + x_offset,
                          border_width + y_offset,
                          border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value_2 + x_offset,
                          height - border_width + y_offset)
      self._canvas.coords("progress_rectangle_2",
                          border_width + 2 * inner_corner_radius + (width - 2 * inner_corner_radius - 2 * border_width) * progress_value_1 + x_offset,
                          border_width + inner_corner_radius + y_offset,
                          border_width + 2 * inner_corner_radius + (width - 2 * inner_corner_radius - 2 * border_width) * progress_value_2 + x_offset,
                          height - inner_corner_radius - border_width + y_offset)
    
    # vertical orientation from the bottom
    if orientation == "s":
      requires_recoloring_2 = self.__draw_rounded_rect_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                x_offset, y_offset, ())
      
      # set positions of progress corner parts
      self._canvas.coords("progress_oval_1_a", 
                          border_width + inner_corner_radius + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_2) + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_1_b", 
                          border_width + inner_corner_radius + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_2) + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_2_a", 
                          width - border_width - inner_corner_radius + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_2) + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_2_b", 
                          width - border_width - inner_corner_radius + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_2) + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_3_a", 
                          width - border_width - inner_corner_radius + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_1) + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_3_b", 
                          width - border_width - inner_corner_radius + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_1) + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_4_a", 
                          border_width + inner_corner_radius + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_1) + y_offset, inner_corner_radius)
      self._canvas.coords("progress_oval_4_b", 
                          border_width + inner_corner_radius + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_1) + y_offset, inner_corner_radius)

      # set positions of progress rect parts
      self._canvas.coords("progress_rectangle_1",
                          border_width + inner_corner_radius + x_offset,
                          border_width + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_2) + y_offset,
                          width - border_width - inner_corner_radius + x_offset,
                          border_width + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_1) + y_offset)
      self._canvas.coords("progress_rectangle_2",
                          border_width + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_2) + y_offset,
                          width - border_width + x_offset,
                          border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value_1) + y_offset)
      
    
    return requires_recoloring or requires_recoloring_2
    
  # function to start drawing slider bar and 3 buttons onto a canvas widget
  def draw_rounded_slider_with_border_and_3_buttons(self,
                                                    canvas_width: int | float,
                                                    canvas_height: int | float,

                                                    bar_width: int | float,
                                                    bar_height: int | float,
                                                    bar_corner_radius: int | float,
                                                    bar_border_width: int | float,
                                                    
                                                    outer_button_width: int | float,
                                                    outer_button_height: int | float,
                                                    outer_button_corner_radius: int | float,

                                                    center_button_width: int | float,
                                                    center_button_corner_radius: int | float,

                                                    lbutton_value: int | float,
                                                    rbutton_value: int | float,
                                                    cbutton_value: int | float,
                                                    
                                                    orientation: str) -> bool:
    
    # round _current_width and _current_height and restrict them to even values only
    if self._round_width_to_even_numbers:
      bar_width = math.floor(bar_width / 2) * 2 
    if self._round_height_to_even_numbers:
      bar_height = math.floor(bar_height / 2) * 2
    
    # restrict corner_radius if it's too larger
    if bar_corner_radius > bar_width / 2 or bar_corner_radius > bar_height / 2:  
      bar_corner_radius = min(bar_width / 2, bar_height / 2)

    bar_corner_radius = self._DrawEngine__calc_optimal_corner_radius(bar_corner_radius)  # optimize corner_radius for different drawing methods (different rounding)
    
    # restrict outer_button_corner_radius if too large
    if outer_button_corner_radius > outer_button_width / 2 or outer_button_corner_radius > outer_button_width / 2:  
      outer_button_corner_radius = min(outer_button_width / 2, outer_button_height / 2)
    
    outer_button_corner_radius = round(outer_button_corner_radius)

    # restrict center_button_corner_radius if too large
    if center_button_corner_radius > center_button_width / 2:  
      center_button_corner_radius = center_button_width / 2
    
    center_button_corner_radius = round(center_button_corner_radius)

    bar_border_width = round(bar_border_width)
    
    outer_button_width = round(outer_button_width)
    outer_button_height = round(outer_button_height)
    center_button_width = round(center_button_width)    

    if bar_corner_radius >= bar_border_width:
      bar_inner_corner_radius = bar_corner_radius - bar_border_width
    else:
      bar_inner_corner_radius = 0

    if orientation == "w":
      x_offset = round(canvas_width - bar_width - outer_button_width)
      y_offset = round((canvas_height / 2) - (bar_height / 2)) 
    elif orientation == "s":
      x_offset = round((canvas_width / 2) - (bar_width / 2))
      y_offset = round(canvas_height - bar_height - outer_button_height)
    
    return self.__draw_rounded_slider_with_border_and_3_buttons_font_shapes(bar_width, bar_height, bar_corner_radius, bar_border_width, bar_inner_corner_radius,
                                                                            x_offset, y_offset,
                                                                            outer_button_width, outer_button_height, outer_button_corner_radius,
                                                                            center_button_width, center_button_corner_radius,
                                                                            lbutton_value, rbutton_value, cbutton_value, orientation)
    
  def __draw_rounded_slider_with_border_and_3_buttons_font_shapes(self,
                                                    bar_width: int | float,
                                                    bar_height: int | float,
                                                    bar_corner_radius: int | float,
                                                    bar_border_width: int | float,
                                                    bar_inner_corner_radius: int | float,

                                                    x_offset: int,
                                                    y_offset: int,
                                                    
                                                    outer_button_width: int | float,
                                                    outer_button_height: int | float,
                                                    outer_button_corner_radius: int | float,

                                                    center_button_width: int | float,
                                                    center_button_corner_radius: int | float,

                                                    lbutton_value: int | float,
                                                    rbutton_value: int | float,
                                                    cbutton_value: int | float,
                                                    
                                                    orientation: str) -> bool:
    # need offset to move proress bar down (or down right if vertical) to align with the elongated outer buttons
    # without the buttons getting cutoff
    
    # draw normal progressbar
    requires_recoloring = self.__draw_rounded_progress_bar_with_border_font_shapes(bar_width, bar_height, bar_corner_radius, bar_border_width, bar_inner_corner_radius,
                                                                                       x_offset, y_offset, lbutton_value, rbutton_value, orientation)  
    
    """
    # create the left slider button as a rectangle with round corners
    # create 4 circles (if not needed, then less)
    if not self._canvas.find_withtag("lbutton_oval_2_a"):
      self._canvas.create_aa_circle(0, 0, 0, tags=("lbutton_oval_1_a", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("lbutton_oval_1_b", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True
    
    if not self._canvas.find_withtag("lbutton_oval_2_a") and height > 2 * outer_button_corner_radius:
      self._canvas.create_aa_circle(0, 0, 0, tags=("lbutton_oval_2_a", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER)
      self._canvas.create_aa_circle(0, 0, 0, tags=("lbutton_oval_2_b", "button_corner_part", "button_parts", "left_button_parts"), anchor=tkinter.CENTER, angle=180)
      requires_recoloring = True

    elif self._canvas.find_withtag("lbutton_oval_2_a") and not height > 2 * outer_button_corner_radius:
      self._canvas.delete("lbutton_oval_4_a", "lbutton_oval_2_b")

    # create the 2 rectangles (if needed)
    if not self._canvas.find_withtag("lbutton_rectangle_1") and outer_button_width > 0:
      self._canvas.create_rectangle(0, 0, 0, 0, tags=("lbutton_rectangle_1", "button_rectangle_part", "button_parts", "left_button_parts"), width=0)
      requires_recoloring = True

    elif self._canvas.find_withtag("lbutton_rectangle_1") and not outer_button_width > 0:
      self._canvas.delete("lbutton_rectangle_1")

    
    # set positions of circles and rectangles
    # draws button on horizontal progress bar
    if orientation == "w":
      left_button_x_position = corner_radius + (outer_button_width / 2) + (width - 2 * corner_radius - outer_button_width) * lbutton_value

      self._canvas.coords("lbutton_oval_1_a", left_button_x_position - (outer_button_width / 2), outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_1_b", left_button_x_position - (outer_button_width / 2), outer_button_corner_radius, outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_2_a", left_button_x_position - (outer_button_width / 2), outer_button_height - (outer_button_corner_radius * 2), outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_2_b", left_button_x_position - (outer_button_width / 2), outer_button_height - (outer_button_corner_radius * 2), outer_button_corner_radius)
      

      self._canvas.coords("lbutton_rectangle_1",
                          left_button_x_position , 
                          outer_button_corner_radius,
                          left_button_x_position - outer_button_width, 
                          outer_button_height - (outer_button_corner_radius * 2))
    
    
    # draws button on vertical progress bar
    elif orientation == "s":
      left_button_y_position = corner_radius + (outer_button_width / 2) + (height - 2 * corner_radius - outer_button_width) * (1 - lbutton_value)
      self._canvas.coords("lbutton_oval_1_a", outer_button_corner_radius, left_button_y_position - (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_1_b", outer_button_corner_radius, left_button_y_position - (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_4_a", width - outer_button_corner_radius, left_button_y_position - (outer_button_width / 2), outer_button_corner_radius)
      self._canvas.coords("lbutton_oval_4_b", width - outer_button_corner_radius, left_button_y_position - (outer_button_width / 2), outer_button_corner_radius)

      self._canvas.coords("lbutton_rectangle_1",
                          0, left_button_y_position - (outer_button_width / 2),
                          width, left_button_y_position + (outer_button_width / 2))
    """
    

    
    if requires_recoloring:  # new parts were added -> manage z-order
      self._canvas.tag_raise("button_parts")
    
    return requires_recoloring