import tkinter

from customtkinter.windows.widgets.core_rendering import DrawEngine
from customtkinter.windows.widgets.core_rendering import CTkCanvas

class CustomDrawEngine:
  """
  Custom Draw Engine to draw slider with 2 outer trim slider buttons,
  and an inner seek button
  """

  # Use circle_shapes on macOS to avoid rectangular slider heads, font_shapes elsewhere
  preferred_drawing_method: str = "circle_shapes" if sys.platform == "darwin" else "font_shapes"

  def __init__(self, canvas: CTkCanvas):
    self._canvas = canvas
  
  def set_round_to_even_numbers(self, round_width_to_even_numbers: bool = True, round_height_to_even_numbers: bool = True):
    self._round_width_to_even_numbers: bool = round_width_to_even_numbers
    self._round_height_to_even_numbers: bool = round_height_to_even_numbers
    
  def __calc_optimal_corner_radius(self, user_corner_radius: Union[float, int]) -> Union[float, int]:
    # optimize for drawing with polygon shapes
    if self.preferred_drawing_method == "polygon_shapes":
      if sys.platform == "darwin":
        return user_corner_radius
      else:
        return round(user_corner_radius)

    # optimize for drawing with antialiased font shapes
    elif self.preferred_drawing_method == "font_shapes":
      return round(user_corner_radius)

    # optimize for drawing with circles and rects
    elif self.preferred_drawing_method == "circle_shapes":
      user_corner_radius = 0.5 * round(user_corner_radius / 0.5)  # round to 0.5 steps

      # make sure the value is always with .5 at the end for smoother corners
      if user_corner_radius == 0:
        return 0
      elif user_corner_radius % 1 == 0:
        return user_corner_radius + 0.5
      else:
        return user_corner_radius
  
  # function to start drawing slider bar and 3 buttons onto a canvas widget
  def draw_rounded_slider_with_border_and_3_buttons(self,
                                                    width: int | float,
                                                    height: int | float,
                                                    corner_radius: int | float,
                                                    border_width : int | float,
                                                    
                                                    outer_button_height: int | float,
                                                    outer_button_width: int | float,
                                                    outer_button_corner_radius: int | float,
                                                    outer_button_border_width: int | float,
                                                    
                                                    inner_button_height: int | float,
                                                    inner_button_width: int | float,
                                                    inner_button_corner_radius: int | float,
                                                    inner_button_border_width: int | float,
                                                    
                                                    lslider_button_pos: int | float,
                                                    rslider_button_pos: int | float,
                                                    mslider_button_pos: int | float,
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
    
    # restrict inner_button_corner_radius if too large
    if inner_button_corner_radius > inner_button_width / 2 or inner_button_corner_radius > inner_button_width / 2:  
      inner_button_corner_radius = min(inner_button_width / 2, inner_button_height / 2)
    
    corner_radius = self.__calc_optimal_corner_radius(corner_radius)
    outer_button_corner_radius = self.__calc_optimal_corner_radius(outer_button_corner_radius)
    inner_button_corner_radius = self.__calc_optimal_corner_radius(inner_button_corner_radius)