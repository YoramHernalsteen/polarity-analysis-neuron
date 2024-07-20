import functionality.helpers.image_analysis as image_analysis
import functionality.helpers.file_utils as file_utils
import numpy as np
import cv2
from collections import Counter
from typing import List, Dict
import os
import time

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


    for file in files: 
        start_time = time.perf_counter()
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
        end_time = time.perf_counter()
        elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"Function execution time: {elapsed_time_ms:.2f} ms")


def most_close_neighbours(pixels: image_analysis.Pixel, limit: int, max_distance: int) -> List[image_analysis.Pixel]:
    pixels_np = np.array([[pixel.x, pixel.y] for pixel in pixels])

    neighbours = count_neighbors_within_distance_np(pixels_np, max_distance)
    neighbours_sorted_desc = dict(sorted(neighbours.items(), key=lambda item: item[1], reverse=True))

    i = 0

    closest_neighbours = []
    for key in neighbours_sorted_desc:
        if(i >= limit):
            break
        x = int(key.split('-')[0])
        y = int(key.split('-')[1])
        closest_neighbours.append(image_analysis.Pixel(x=x, y=y,r=0,g=0, b=0))
        i+=1
    return closest_neighbours

def count_neighbors_within_distance_np(coords: np.array, distance_threshold: int) -> Dict[str, int]:
    """
    Counts the number of coordinates within a specified Euclidean distance for each coordinate
    and returns a dictionary with keys "x_y" and matched coordinates as the count.

    Args:
        coords: A NumPy array of shape (N, 2) where each row represents an (x, y) coordinate.
        distance_threshold: The maximum Euclidean distance to consider as a neighbor.

    Returns:
        A dictionary where keys are strings "x-y" representing coordinates and values are the
        number of neighbors within the threshold for each coordinate.
    """
    distances = np.sqrt(np.sum((coords[:, np.newaxis, :] - coords[np.newaxis, :, :]) ** 2, axis=-1))
    within_threshold = distances <= distance_threshold
    np.fill_diagonal(within_threshold, False)
    neighbor_counts = np.sum(within_threshold, axis=1)

    neighbor_counts_dict = {}

    for (x, y), count in zip(coords, neighbor_counts):
        neighbor_counts_dict[f"{x}-{y}"] = count

    return neighbor_counts_dict

