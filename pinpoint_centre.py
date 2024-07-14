import cv2
import file_utils
#import numpy as np
from typing import Any

def draw_circle(event: int, x: int, y: int, flags: int, params: Any) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image, (x, y), 5, (255, 0, 0), -1)  # Blue circle, -1 fills it7

def run() -> None:
    image_path = 'C:\\Users\\yoram\\Documents\\Programmeren\\python\\cell_analyser\\data\\input\\cel2_070923.png'  # Replace with your image path
    global image 
    image = cv2.imread(image_path)

    # Function for handling mouse clicks

    # Create a window and set the mouse callback function
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_circle)

    # Display the image and wait for user interactions
    output_path = file_utils.generate_output_file_location('data.png')

    file_utils.verify_output_folder()

    while True:
        cv2.imshow('Image', image)
        print(file_utils.current_path())
        key = cv2.waitKey(1) & 0xFF  # Wait for a key press
        if key == ord('q'):  # Quit when 'q' is pressed
            break
        elif key == ord('s'):  # Save the image when 's' is pressed
            cv2.imwrite(output_path, image)
            break  

    cv2.destroyAllWindows() 
