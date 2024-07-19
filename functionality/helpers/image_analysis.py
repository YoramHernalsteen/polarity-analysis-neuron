from enum import Enum
from dataclasses import dataclass
import cv2
from typing import List
import numpy as np

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

def get_pixel(img: cv2.typing.MatLike, x: int, y: int) -> Pixel:
    """Gets a file_analysis.Pixel object for the pixel at (x, y) in the image."""
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
    """Lists all file_analysis.Pixel objects in the image."""
    height, width, _ = img.shape
    all_pixels = []
    for y in range(height):
        for x in range(width):
            pixel = get_pixel(img, x, y)
            if pixel is not None:
                all_pixels.append(pixel)
    return all_pixels

def list_colored_pixels(img: cv2.typing.MatLike, color: str, threshold: int) -> List[Pixel]:
    """Filters file_analysis.Pixel objects based on color and threshold."""
    
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