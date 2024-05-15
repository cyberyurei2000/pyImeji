# Copyright (c) cyberyurei2000 2022
# Released under the BSD 3-Clause License
# https://opensource.org/license/bsd-3-clause

import os
import cv2
import yaml
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from cv2.typing import MatLike

mpl.rcParams['toolbar'] = "None"


def histogram(image1: MatLike, image2: MatLike, title: str, original: bool) -> None:
    """Show image histogram"""
    if original:
        image1_gry = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        histr1 = cv2.calcHist([image1_gry], [0], None, [256], [0, 256])
        plt.subplot(121)
        plt.plot(histr1)
        plt.title("Original Histogram")

        plt.subplot(122)

    image2_gry = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    histr2 = cv2.calcHist([image2_gry], [0], None, [256], [0, 256])
    plt.plot(histr2)
    plt.title(f"{title} Histogram")
    plt.show()


def save_image(image: MatLike, path: str) -> None:
    """Save image with filter applied"""
    file_name, file_ext = os.path.splitext(path)
    cv2.imwrite(f"output{file_ext}", image)


def show(image1: MatLike, image2: MatLike, title: str, histr: bool, original: bool) -> None:
    """Show image"""
    if original:
        plt.subplot(121)
        plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        plt.title("Original")

        plt.subplot(122)

    plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.show()

    if histr:
        histogram(image1, image2, title, original)


def low_pass(path: str, histr: bool, original: bool, save: bool) -> None:
    """Apply Low-pass filter to the image"""
    image = cv2.imread(path)
    gblur_image = cv2.GaussianBlur(image, (5, 5), 0)
    if save:
        save_image(gblur_image, path)
    show(image, gblur_image, "Low-pass", histr, original)


def high_pass(path: str, histr: bool, original: bool, save: bool) -> None:
    "Apply High-pass filter to the image"
    image = cv2.imread(path)

    filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpen_image = cv2.filter2D(src=image, ddepth=-1, kernel=filter)
    if save:
        save_image(sharpen_image, path)
    show(image, sharpen_image, "High-pass", histr, original)


def median(path: str, histr: bool, original: bool, save: bool) -> None:
    """Apply Median filter to the image"""
    image = cv2.imread(path)
    median_image = cv2.medianBlur(image, 5)
    if save:
        save_image(median_image, path)
    show(image, median_image, "Median", histr, original)


def main():
    with open("./config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
            filter = config["filter"]
            path = config["imagePath"]
            show_histr = config["showHistogram"]
            original = config["showOriginal"]
            save = config["save"]

            match filter:
                case "lowpass":
                    low_pass(path, show_histr, original, save)
                case "highpass":
                    high_pass(path, show_histr, original, save)
                case "median":
                    median(path, show_histr, original, save)
        except yaml.YAMLError as err:
            print(err)


if __name__ == "__main__":
    main()
