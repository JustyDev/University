import os

import cv2


def save_progress(image, filename):
    if not os.path.exists('progress'):
        os.makedirs('progress')

    path = os.path.join('progress', filename)
    cv2.imwrite(path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))