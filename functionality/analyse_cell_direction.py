import cv2
import numpy as np
from dataclasses import dataclass

@dataclass
class Pixel:
    """Represents a pixel with x, y coordinates and R, G, B color values."""
    x: int
    y: int
    r: int
    g: int
    b: int

def get_pixel(img, x, y):
    """Gets a Pixel object for the pixel at (x, y) in the image."""
    if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
        b, g, r = img[y, x]
        return Pixel(x, y, r, g, b)
    else:
        return None 


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


# Example usage
image_path = "C:\\Users\\yoram\\Documents\\Programmeren\\python\\cell_analyser\\data\\output\\cel2_070923.png"  # Replace with your image path
output_file = "C:\\Users\\yoram\\Documents\\Programmeren\\python\\cell_analyser\\data\\output\\analyse.csv"  # Replace with your image path
img = cv2.imread(image_path)

# List all pixels
#pixels = list_all_pixels(img)
#print(f"All pixels (first 5): {pixels[:5]}")  # Print a few for demonstration

# List black pixels
pixels = list_black_pixels(img)
print(f"black pixel coordinates {len(pixels)} of {len(list_all_pixels(img))}")  # Print a few

# List blue pixels
pixels = list_blue_pixels(img)
print(f"Blue pixel coordinates {len(pixels)} of {len(list_all_pixels(img))}")  # Print a few

def write_pixels_to_file(img, filename):
    """Writes Pixel objects to a file in dataclass format."""
    pixels = list_all_pixels(img)
    with open(filename, 'w') as f:
        f.write(f"x;y;r;g;b\n")
        for pixel in pixels:
            f.write(f"{pixel.x};{pixel.y};{pixel.r};{pixel.g};{pixel.b}\n")

write_pixels_to_file(img, output_file)