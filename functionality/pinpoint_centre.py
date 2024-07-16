import cv2
import functionality.helpers.file_utils as file_utils
import os
from typing import Any

def draw_circle(event: int, x: int, y: int, image: cv2.typing.MatLike, flags: int) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image, (x, y), 3, (255, 0, 0), -1)

def run() -> None:
    files = file_utils.files_not_converted()
    for file in files:
        filename = os.path.basename(file)
        
        image = cv2.imread(file)
        
        cv2.namedWindow(filename)
        cv2.setMouseCallback(filename, lambda event, x, y, flags, _: draw_circle(event=event, x=x, y=y, flags=flags, image=image))

        output_path = file_utils.generate_output_file_location(filename)
        file_utils.verify_output_folder()

        while True:
            cv2.imshow(filename, image)
            key = cv2.waitKey(1) & 0xFF 
            if key == ord('q'):
                break
            elif key == ord('s'):
                cv2.imwrite(output_path, image)
                break  

        cv2.destroyAllWindows() 
