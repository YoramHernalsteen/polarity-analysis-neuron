import cv2
import numpy as np
from dataclasses import dataclass
import functionality.helpers.file_utils as file_utils
from enum import Enum
import os

@dataclass
class Pixel:
    """Represents a pixel with x, y coordinates and R, G, B color values."""
    x: int
    y: int
    r: int
    g: int
    b: int

class Direction(Enum):
    TOPRIGHT = 'TOPRIGHT'
    TOPLEFT = 'TOPLEFT'
    BOTTOMRIGHT = 'BOTTOMRIGHT'
    BOTTOMLEFT = 'BOTTOMLEFT'

@dataclass
class PixelXY:
    """Represents a pixel with x, y values"""
    x: int
    y: int

def run():
    files = file_utils.converted_files()
    for file in files:
        print(file)
        img = cv2.imread(file)
        centre = centre_of_img(img)
        black_pixels = list_black_pixels(img)
        size = len(black_pixels)

        if size == 0:
            size = 1

        directions = {Direction.TOPRIGHT :0, Direction.TOPLEFT : 0, Direction.BOTTOMRIGHT : 0, Direction.BOTTOMLEFT : 0}
        for pixel in black_pixels:
            if(pixel.x >= centre.x and pixel.y >= centre.y):
                directions[Direction.BOTTOMRIGHT] += 1
            elif(pixel.x >= centre.x and pixel.y < centre.y):
                directions[Direction.TOPRIGHT] += 1
            elif(pixel.x < centre.x and pixel.y < centre.y):
                directions[Direction.TOPLEFT] += 1
            elif(pixel.x < centre.x and pixel.y >= centre.y):
                directions[Direction.BOTTOMLEFT] += 1

        directions_percentage = {Direction.TOPRIGHT : (directions[Direction.TOPRIGHT] / size) * 100
                                 , Direction.TOPLEFT : (directions[Direction.TOPLEFT] / size) * 100
                                 , Direction.BOTTOMRIGHT : (directions[Direction.BOTTOMRIGHT] / size) * 100
                                 , Direction.BOTTOMLEFT : (directions[Direction.BOTTOMLEFT] / size) * 100}
        
        filename = os.path.basename(file)
        analysis_path = file_utils.generate_analysis_file_location_csv(filename)

        with open(analysis_path, 'w') as f:
            f.write(f"{Direction.TOPRIGHT.value};{Direction.TOPLEFT.value};{Direction.BOTTOMRIGHT.value};{Direction.BOTTOMLEFT.value}\n")
            f.write(f"{directions_percentage[Direction.TOPRIGHT]};{directions_percentage[Direction.TOPLEFT]};{directions_percentage[Direction.BOTTOMRIGHT]};{directions_percentage[Direction.BOTTOMLEFT]}\n")
            f.write(f"{directions[Direction.TOPRIGHT]};{directions[Direction.TOPLEFT]};{directions[Direction.BOTTOMRIGHT]};{directions[Direction.BOTTOMLEFT]}\n")
        
        max_y, max_x, _ = img.shape
        draw_red_line(file, centre.x, centre.y, max_x, max_y)
        
def get_pixel(img, x, y):
    """Gets a Pixel object for the pixel at (x, y) in the image."""
    if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
        b, g, r = img[y, x]
        return Pixel(x, y, r, g, b)
    else:
        return None 

def centre_of_img(img) -> PixelXY:
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


def list_all_pixels(img):
    """Lists all Pixel objects in the image."""
    height, width, _ = img.shape
    all_pixels = []
    for y in range(height):
        for x in range(width):
            pixel = get_pixel(img, x, y)
            if pixel is not None:
                all_pixels.append(pixel)
    return all_pixels

def list_colored_pixels(img, color, threshold):
    """Filters Pixel objects based on color and threshold."""
    
    all_pixels = list_all_pixels(img=img)
    colored_pixels = []
    for pixel in all_pixels:
        if color == 'black' and np.all(np.array([pixel.b, pixel.g, pixel.r]) <= threshold):
            colored_pixels.append(pixel)
        elif color == 'blue' and pixel.b > threshold and pixel.g == 0 and pixel.r == 0:
            colored_pixels.append(pixel)
    return colored_pixels

def list_black_pixels(img):
    return list_colored_pixels(img=img, color='black', threshold=225)

def list_blue_pixels(img):
    return list_colored_pixels(img=img, color='blue', threshold=250)

def draw_red_line(img, x, y, max_x, max_y):
    print(img)
    image = cv2.imread(img)  # Replace with your image path

    if image is None:
        print("Could not read the image.")

    color = (255, 0, 0)  # Red color
    thickness = 1

    start_point = (0, y)
    end_point = (max_x, y)
    image = cv2.line(image, start_point, end_point, color, thickness)

    start_point = (x, 0)
    end_point = (x, max_y)
    image = cv2.line(image, start_point, end_point, color, thickness)

    file_name = os.path.basename(img)
    file_path = file_utils.generate_analysis_file_location(file_name)
    print(file_path)
    cv2.imwrite(file_path, image)
