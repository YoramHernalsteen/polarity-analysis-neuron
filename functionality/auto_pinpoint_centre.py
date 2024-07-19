import functionality.helpers.image_analysis as image_analysis
import functionality.helpers.file_utils as file_utils
import numpy as np
import cv2
from collections import Counter
from typing import List
import os

def run():
    files = file_utils.input_files()
    # delete all auto_recognition files
    files_to_delete = file_utils.converted_files()

    for f_delete in files_to_delete:
        if 'auto_recognition' in f_delete:
            try:
                os.remove(f_delete)
                print(f'deleted {f_delete}')
            except OSError as e:
                print(f"Error deleting {f_delete}: {e}")

    max_distance = 10

    for file in files: 
        img = cv2.imread(file)
        black_pixels = image_analysis.list_black_pixels(img)
        first_round_pixels = most_close_neighbours(black_pixels, 100, 8)
        second_round_pixels = most_close_neighbours(first_round_pixels, 50, 4)
        third_round_pixels = most_close_neighbours(second_round_pixels, 10, 4)
        x = 0
        y = 0
        size = len(third_round_pixels)
        if size == 0:
            size = 1
        for pixel in third_round_pixels:
            x += pixel.x
            y += pixel.y

        x = round(x/size)
        y = round(y / size)
        cv2.circle(img, (x, y), 3, (255, 0, 0), -1)

        filename = file_utils.base_filename(file)
        output_path = file_utils.generate_output_file_location('auto_recognition_' + filename)
        cv2.imwrite(output_path, img)


def most_close_neighbours(pixels: image_analysis.Pixel, limit: int, max_distance: int) -> List[image_analysis.Pixel]:
    amount_of_neighbours = {}
    for pixel in pixels:

        pixel_key = f'{pixel.x}-{pixel.y}'

        for neighbour_pixel in pixels:
            if abs(abs(pixel.x) - abs(neighbour_pixel.x)) > (max_distance * 2):
                continue
            if (abs(pixel.y) - abs(neighbour_pixel.y)) > (max_distance * 2):
                continue

            distance = np.linalg.norm(np.array([pixel.x, pixel.y]) - np.array([neighbour_pixel.x, neighbour_pixel.y]))

            if distance <= max_distance:
                if pixel_key in amount_of_neighbours:
                    amount_of_neighbours[pixel_key] += 1
                else:
                    amount_of_neighbours[pixel_key] = 1
    
    counter = Counter(amount_of_neighbours)
    neighbours = []
    i = 0
    for key, value in counter.most_common():
        if(i >= limit):
            break
        x = int(key.split('-')[0])
        y = int(key.split('-')[1])
        neighbours.append(image_analysis.Pixel(x=x, y=y,r=0,g=0, b=0))
        i+=1
    return neighbours

