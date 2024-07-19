import cv2
import numpy as np
from dataclasses import dataclass
import functionality.helpers.file_utils as file_utils
from enum import Enum
import os
from typing import List

@dataclass
class Pixel:
    """Represents a pixel with x, y coordinates and R, G, B color values."""
    x: int
    y: int
    r: int
    g: int
    b: int

class Direction(Enum):
    TOPRIGHT1 = 'TOPRIGHT1'
    TOPRIGHT2 = 'TOPRIGHT2'
    BOTTOMRIGHT1 = 'BOTTOMRIGHT1'
    BOTTOMRIGHT2 = 'BOTTOMRIGHT2'
    BOTTOMLEFT1 = 'BOTTOMLEFT1'
    BOTTOMLEFT2 = 'BOTTOMLEFT2'
    TOPLEFT1 = 'TOPLEFT1'
    TOPLEFT2 = 'TOPLEFT2'

class Limit(Enum):
    TOPRIGHT = 'TOPRIGHT'
    BOTTOMLEFT = 'BOTTOMLEFT'
    BOTTOMRIGHT = 'BOTTOMRIGHT'
    TOPLEFT = 'TOPLEFT'

@dataclass
class PixelXY:
    """Represents a pixel with x, y values"""
    x: int
    y: int

def run():
    files = file_utils.converted_files()
    for file in files:
        img = cv2.imread(file)
        centre = centre_of_img(img)
        black_pixels = list_black_pixels(img)
        size = len(black_pixels)

        if size == 0:
            size = 1

        directions = {Direction.TOPRIGHT1 :0
                      , Direction.TOPRIGHT2 : 0
                      , Direction.TOPLEFT1 : 0
                      , Direction.TOPLEFT2 : 0
                      , Direction.BOTTOMRIGHT1 : 0
                      , Direction.BOTTOMRIGHT2 : 0
                      , Direction.BOTTOMLEFT1 : 0
                      , Direction.BOTTOMLEFT2 : 0}
        
        max_y, max_x, _ = img.shape

        for pixel in black_pixels:
            directions[get_direction(centre, PixelXY(max_x, max_y), pixel)] += 1

        directions_percentage_raw = {Direction.TOPRIGHT1 : round(((directions[Direction.TOPRIGHT1] / size) * 100), 4)
                                 , Direction.TOPRIGHT2 : round(((directions[Direction.TOPRIGHT2] / size) * 100), 4)
                                 , Direction.BOTTOMRIGHT1 : round(((directions[Direction.BOTTOMRIGHT1] / size) * 100), 4)
                                 , Direction.BOTTOMRIGHT2 : round(((directions[Direction.BOTTOMRIGHT2] / size) * 100), 4)
                                 , Direction.TOPLEFT1 : round(((directions[Direction.TOPLEFT1] / size) * 100), 4)
                                 , Direction.TOPLEFT2 : round(((directions[Direction.TOPLEFT2] / size) * 100), 4)
                                 , Direction.BOTTOMLEFT1 : round(((directions[Direction.BOTTOMLEFT1] / size) * 100), 4)
                                 , Direction.BOTTOMLEFT2 : round(((directions[Direction.BOTTOMLEFT2] / size) * 100), 4)}
        
        directions_percentage = format_dict_with_commas(directions_percentage_raw)
        filename = os.path.basename(file)
        analysis_path = file_utils.generate_analysis_file_location_csv(filename)

        with open(analysis_path, 'w') as f:
            f.write(f'{Direction.TOPRIGHT1.value};{Direction.TOPRIGHT2.value};{Direction.BOTTOMRIGHT1.value};{Direction.BOTTOMRIGHT2.value};{Direction.BOTTOMLEFT1.value};{Direction.BOTTOMLEFT2.value};{Direction.TOPLEFT1.value};{Direction.TOPLEFT2.value}\n')
            
            f.write(f'{directions_percentage[Direction.TOPRIGHT1]};{directions_percentage[Direction.TOPRIGHT2]};{directions_percentage[Direction.BOTTOMRIGHT1]};{directions_percentage[Direction.BOTTOMRIGHT2]};{directions_percentage[Direction.BOTTOMLEFT1]};{directions_percentage[Direction.BOTTOMLEFT2]};{directions_percentage[Direction.TOPLEFT1]};{directions_percentage[Direction.TOPLEFT2]}\n')
            
            f.write(f'{directions[Direction.TOPRIGHT1]};{directions[Direction.TOPRIGHT2]};{directions[Direction.BOTTOMRIGHT1]};{directions[Direction.BOTTOMRIGHT2]};{directions[Direction.BOTTOMLEFT1]};{directions[Direction.BOTTOMLEFT2]};{directions[Direction.TOPLEFT1]};{directions[Direction.TOPLEFT2]}\n')
        
        draw_red_lines(file, centre, PixelXY(max_x, max_y))
        
def get_pixel(img: cv2.typing.MatLike, x: int, y: int) -> Pixel:
    """Gets a Pixel object for the pixel at (x, y) in the image."""
    if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
        b, g, r = img[y, x]
        return Pixel(x, y, r, g, b)
    else:
        return None 

def centre_of_img(img: cv2.typing.MatLike) -> PixelXY:
    centre_pixels = list_blue_pixels(img)
    
    mean_x = 0 
    mean_y  = 0
    size = len(centre_pixels)

    for pixel in centre_pixels:
        mean_x += pixel.x
        mean_y += pixel.y
    
    if size == 0:
        size = 1

    mean_y/= size
    mean_x/=size
    return PixelXY(x=int(mean_x), y=int(mean_y))


def list_all_pixels(img: cv2.typing.MatLike) -> List[Pixel]:
    """Lists all Pixel objects in the image."""
    height, width, _ = img.shape
    all_pixels = []
    for y in range(height):
        for x in range(width):
            pixel = get_pixel(img, x, y)
            if pixel is not None:
                all_pixels.append(pixel)
    return all_pixels

def list_colored_pixels(img: cv2.typing.MatLike, color: str, threshold: int) -> List[Pixel]:
    """Filters Pixel objects based on color and threshold."""
    
    all_pixels = list_all_pixels(img=img)
    colored_pixels = []
    for pixel in all_pixels:
        if color == 'black' and np.all(np.array([pixel.b, pixel.g, pixel.r]) <= threshold):
            colored_pixels.append(pixel)
        elif color == 'blue' and pixel.b > threshold and pixel.g == 0 and pixel.r == 0:
            colored_pixels.append(pixel)
    return colored_pixels

def list_black_pixels(img: cv2.typing.MatLike) -> List[Pixel]:
    return list_colored_pixels(img=img, color='black', threshold=225)

def list_blue_pixels(img: cv2.typing.MatLike) -> List[Pixel]:
    return list_colored_pixels(img=img, color='blue', threshold=250)

def draw_red_lines(img: cv2.typing.MatLike, centre: PixelXY, max: PixelXY) -> None:
    image = cv2.imread(img)

    if image is None:
        print("Could not read the image.")

    color = (0, 0, 255)  # Red color - uses not rgb but bgr
    thickness = 1

    start_point = (0, centre.y)
    end_point = (max.x, centre.y)
    image = cv2.line(image, start_point, end_point, color, thickness)

    start_point = (centre.x, 0)
    end_point = (centre.x, max.y)
    image = cv2.line(image, start_point, end_point, color, thickness)

    bottom_left = get_limit(centre, Limit.BOTTOMLEFT, max)
    top_right = get_limit(centre, Limit.TOPRIGHT, max)
    start_point = (bottom_left.x, bottom_left.y)
    end_point = (top_right.x, top_right.y)
    image = cv2.line(image, start_point, end_point, color, thickness)

    top_left = get_limit(centre, Limit.TOPLEFT, max)
    bottom_right = get_limit(centre, Limit.BOTTOMRIGHT, max)
    start_point = (top_left.x, top_left.y)
    end_point = (bottom_right.x, bottom_right.y)
    image = cv2.line(image, start_point, end_point, color, thickness)

    file_name = os.path.basename(img)
    file_path = file_utils.generate_analysis_file_location(file_name)
    cv2.imwrite(file_path, image)

def get_part():
    pass

def get_limit(centre: PixelXY, limit: Limit, max: PixelXY) -> PixelXY:
    #bypass mutability
    coordinate = PixelXY(centre.x, centre.y)

    if limit.value == Limit.TOPRIGHT.value:
        return search_limit(coordinate, max, 1, -1)
    elif limit.value == Limit.BOTTOMRIGHT.value:
        return search_limit(coordinate, max, 1, 1)
    elif limit.value == Limit.BOTTOMLEFT.value:
        return search_limit(coordinate, max, -1, 1)
    elif limit.value == Limit.TOPLEFT.value:
        return search_limit(coordinate, max, -1, -1)
    
    return PixelXY(0,0)

def search_limit(coordinate: PixelXY, max: PixelXY, x_move: int, y_move: int) -> PixelXY:
    while not(coordinate.x == 0 or coordinate.x == max.x or coordinate.y == 0 or coordinate.y == max.y):
        coordinate.x += x_move
        coordinate.y += y_move
    
    return PixelXY(coordinate.x, coordinate.y)

def get_direction(centre: PixelXY, max: PixelXY, pixel: PixelXY) -> Direction:

    coordinate = PixelXY(pixel.x, pixel.y)
    if(coordinate.x >= centre.x and coordinate.y >= centre.y):

        limit = get_limit(centre, Limit.BOTTOMRIGHT, max)
        coordinate = get_limit(coordinate, Limit.BOTTOMRIGHT, max)
        if coordinate.x < limit.x or coordinate.y > limit.y:
            return Direction.BOTTOMRIGHT2
        return Direction.BOTTOMRIGHT1
    
    elif(coordinate.x >= centre.x and coordinate.y <= centre.y):

        limit = get_limit(centre, Limit.TOPRIGHT, max)
        coordinate = get_limit(coordinate, Limit.TOPRIGHT, max)

        if coordinate.x > limit.x or coordinate.y > limit.y:
            return Direction.TOPRIGHT2
        return Direction.TOPRIGHT1
    
    elif(coordinate.x < centre.x and coordinate.y < centre.y):

        limit = get_limit(centre, Limit.TOPLEFT, max)
        coordinate = get_limit(coordinate, Limit.TOPLEFT, max)
         
        if coordinate.x > limit.x or coordinate.y < limit.y:
            return Direction.TOPLEFT2
        return Direction.TOPLEFT1
    elif(coordinate.x < centre.x and coordinate.y >= centre.y):

        limit = get_limit(centre, Limit.BOTTOMLEFT, max)
        coordinate = get_limit(coordinate, Limit.BOTTOMLEFT, max)

        if coordinate.x < limit.x or coordinate.y < limit.y:
            return Direction.BOTTOMLEFT2
        return Direction.BOTTOMLEFT1
    
    return None

def format_dict_with_commas(data_dict: dict) -> dict:
    """Converts numeric values in a dictionary to comma-separated decimal strings.

    Args:
        data_dict: The input dictionary with numeric values.

    Returns:
        A new dictionary with the values formatted as comma-separated decimal strings.
    """
    formatted_dict = {}
    for key, value in data_dict.items():
        if isinstance(value, (int, float)):
            number = f"{value:4f}"
            formatted_dict[key] = number.replace('.', ',')
        else:
            formatted_dict[key] = value 
    return formatted_dict