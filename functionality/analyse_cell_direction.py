import cv2
import numpy as np
import functionality.helpers.file_utils as file_utils
import functionality.helpers.image_analysis as image_analysis
import os
from typing import List

def run():
    files = file_utils.converted_files()
    for file in files:
        img = cv2.imread(file)
        centre = image_analysis.centre_of_img(img)
        print(f'{file} - {centre}')
        black_pixels = image_analysis.list_black_pixels(img)
        size = len(black_pixels)

        if size == 0:
            size = 1

        directions = {image_analysis.Direction.TOPRIGHT1 :0
                      , image_analysis.Direction.TOPRIGHT2 : 0
                      , image_analysis.Direction.TOPLEFT1 : 0
                      , image_analysis.Direction.TOPLEFT2 : 0
                      , image_analysis.Direction.BOTTOMRIGHT1 : 0
                      , image_analysis.Direction.BOTTOMRIGHT2 : 0
                      , image_analysis.Direction.BOTTOMLEFT1 : 0
                      , image_analysis.Direction.BOTTOMLEFT2 : 0}
        
        max_y, max_x, _ = img.shape

        for pixel in black_pixels:
            directions[get_direction(centre, image_analysis.PixelXY(max_x, max_y), pixel)] += 1

        directions_percentage_raw = {image_analysis.Direction.TOPRIGHT1 : round(((directions[image_analysis.Direction.TOPRIGHT1] / size) * 100), 4)
                                 , image_analysis.Direction.TOPRIGHT2 : round(((directions[image_analysis.Direction.TOPRIGHT2] / size) * 100), 4)
                                 , image_analysis.Direction.BOTTOMRIGHT1 : round(((directions[image_analysis.Direction.BOTTOMRIGHT1] / size) * 100), 4)
                                 , image_analysis.Direction.BOTTOMRIGHT2 : round(((directions[image_analysis.Direction.BOTTOMRIGHT2] / size) * 100), 4)
                                 , image_analysis.Direction.TOPLEFT1 : round(((directions[image_analysis.Direction.TOPLEFT1] / size) * 100), 4)
                                 , image_analysis.Direction.TOPLEFT2 : round(((directions[image_analysis.Direction.TOPLEFT2] / size) * 100), 4)
                                 , image_analysis.Direction.BOTTOMLEFT1 : round(((directions[image_analysis.Direction.BOTTOMLEFT1] / size) * 100), 4)
                                 , image_analysis.Direction.BOTTOMLEFT2 : round(((directions[image_analysis.Direction.BOTTOMLEFT2] / size) * 100), 4)}
        
        directions_percentage = format_dict_with_commas(directions_percentage_raw)
        filename = os.path.basename(file)
        analysis_path = file_utils.generate_analysis_file_location_csv(filename)

        with open(analysis_path, 'w') as f:
            f.write(f'{image_analysis.Direction.TOPRIGHT1.value};{image_analysis.Direction.TOPRIGHT2.value};{image_analysis.Direction.BOTTOMRIGHT1.value};{image_analysis.Direction.BOTTOMRIGHT2.value};{image_analysis.Direction.BOTTOMLEFT1.value};{image_analysis.Direction.BOTTOMLEFT2.value};{image_analysis.Direction.TOPLEFT1.value};{image_analysis.Direction.TOPLEFT2.value}\n')
            
            f.write(f'{directions_percentage[image_analysis.Direction.TOPRIGHT1]};{directions_percentage[image_analysis.Direction.TOPRIGHT2]};{directions_percentage[image_analysis.Direction.BOTTOMRIGHT1]};{directions_percentage[image_analysis.Direction.BOTTOMRIGHT2]};{directions_percentage[image_analysis.Direction.BOTTOMLEFT1]};{directions_percentage[image_analysis.Direction.BOTTOMLEFT2]};{directions_percentage[image_analysis.Direction.TOPLEFT1]};{directions_percentage[image_analysis.Direction.TOPLEFT2]}\n')
            
            f.write(f'{directions[image_analysis.Direction.TOPRIGHT1]};{directions[image_analysis.Direction.TOPRIGHT2]};{directions[image_analysis.Direction.BOTTOMRIGHT1]};{directions[image_analysis.Direction.BOTTOMRIGHT2]};{directions[image_analysis.Direction.BOTTOMLEFT1]};{directions[image_analysis.Direction.BOTTOMLEFT2]};{directions[image_analysis.Direction.TOPLEFT1]};{directions[image_analysis.Direction.TOPLEFT2]}\n')
        
        draw_red_lines(file, centre, image_analysis.PixelXY(max_x, max_y))
        

def draw_red_lines(img: cv2.typing.MatLike, centre: image_analysis.PixelXY, max: image_analysis.PixelXY) -> None:
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

    bottom_left = get_limit(centre, image_analysis.Limit.BOTTOMLEFT, max)
    top_right = get_limit(centre, image_analysis.Limit.TOPRIGHT, max)
    start_point = (bottom_left.x, bottom_left.y)
    end_point = (top_right.x, top_right.y)
    image = cv2.line(image, start_point, end_point, color, thickness)

    top_left = get_limit(centre, image_analysis.Limit.TOPLEFT, max)
    bottom_right = get_limit(centre, image_analysis.Limit.BOTTOMRIGHT, max)
    start_point = (top_left.x, top_left.y)
    end_point = (bottom_right.x, bottom_right.y)
    image = cv2.line(image, start_point, end_point, color, thickness)

    file_name = os.path.basename(img)
    file_path = file_utils.generate_analysis_file_location(file_name)
    cv2.imwrite(file_path, image)

def get_part():
    pass

def get_limit(centre: image_analysis.PixelXY, limit: image_analysis.Limit, max: image_analysis.PixelXY) -> image_analysis.PixelXY:
    #bypass mutability
    coordinate = image_analysis.PixelXY(centre.x, centre.y)

    if limit.value == image_analysis.Limit.TOPRIGHT.value:
        return search_limit(coordinate, max, 1, -1)
    elif limit.value == image_analysis.Limit.BOTTOMRIGHT.value:
        return search_limit(coordinate, max, 1, 1)
    elif limit.value == image_analysis.Limit.BOTTOMLEFT.value:
        return search_limit(coordinate, max, -1, 1)
    elif limit.value == image_analysis.Limit.TOPLEFT.value:
        return search_limit(coordinate, max, -1, -1)
    
    return image_analysis.PixelXY(0,0)

def search_limit(coordinate: image_analysis.PixelXY, max: image_analysis.PixelXY, x_move: int, y_move: int) -> image_analysis.PixelXY:
    while not(coordinate.x == 0 or coordinate.x == max.x or coordinate.y == 0 or coordinate.y == max.y):
        coordinate.x += x_move
        coordinate.y += y_move
    
    return image_analysis.PixelXY(coordinate.x, coordinate.y)

def get_direction(centre: image_analysis.PixelXY, max: image_analysis.PixelXY, pixel: image_analysis.PixelXY) -> image_analysis.Direction:

    coordinate = image_analysis.PixelXY(pixel.x, pixel.y)
    if(coordinate.x >= centre.x and coordinate.y >= centre.y):

        limit = get_limit(centre, image_analysis.Limit.BOTTOMRIGHT, max)
        coordinate = get_limit(coordinate, image_analysis.Limit.BOTTOMRIGHT, max)
        if coordinate.x < limit.x or coordinate.y > limit.y:
            return image_analysis.Direction.BOTTOMRIGHT2
        return image_analysis.Direction.BOTTOMRIGHT1
    
    elif(coordinate.x >= centre.x and coordinate.y <= centre.y):

        limit = get_limit(centre, image_analysis.Limit.TOPRIGHT, max)
        coordinate = get_limit(coordinate, image_analysis.Limit.TOPRIGHT, max)

        if coordinate.x > limit.x or coordinate.y > limit.y:
            return image_analysis.Direction.TOPRIGHT2
        return image_analysis.Direction.TOPRIGHT1
    
    elif(coordinate.x < centre.x and coordinate.y < centre.y):

        limit = get_limit(centre, image_analysis.Limit.TOPLEFT, max)
        coordinate = get_limit(coordinate, image_analysis.Limit.TOPLEFT, max)
         
        if coordinate.x > limit.x or coordinate.y < limit.y:
            return image_analysis.Direction.TOPLEFT2
        return image_analysis.Direction.TOPLEFT1
    elif(coordinate.x < centre.x and coordinate.y >= centre.y):

        limit = get_limit(centre, image_analysis.Limit.BOTTOMLEFT, max)
        coordinate = get_limit(coordinate, image_analysis.Limit.BOTTOMLEFT, max)

        if coordinate.x < limit.x or coordinate.y < limit.y:
            return image_analysis.Direction.BOTTOMLEFT2
        return image_analysis.Direction.BOTTOMLEFT1
    
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