from scipy.fftpack import dct
from PIL import Image
from math import sqrt
import os


def evaluation_details(im):
    """get the percentage of zero coefficient values DCT"""
    coef = dct(im)
    e = 0.01
    k = 0
    for i in range(len(coef)):
        for j in range(len(coef.T)):
            if abs(coef[i][j]) < e:
                k += 1
    kol = len(coef) * len(coef.T)
    p = k/kol * 100
    return p


def analysis_all_files():
    """get dictionary sorted by frequency of files in data"""
    percent_null = []
    files = os.listdir('data')
    for s in files:
        im = Image.open('data/' + s)
        im = im.convert('L')
        percent_null.append(evaluation_details(im))
    result = dict(zip(files, percent_null))
    sorted_result = dict(sorted(result.items(), key=lambda item: item[1]))
    return sorted_result


def create_grid_of_images(sorted_result):
    """creating grid of sorted images"""
    img = Image.new('RGB', (1920, 1080))
    sorted_files = list(sorted_result)
    x = int(sqrt(len(sorted_files)))
    y = x
    if x * (y + 1) >= len(sorted_files):
        y += 1
    elif x * (y + 2) >= len(sorted_files):
        y += 2
    else:
        x += 1
        y += 1
    i = -1
    for w in range(0, x):
        for h in range(0, y):
            i += 1
            if i <= len(sorted_files) - 1:
                img_in = Image.open('data/' + sorted_files[i])
                img_in.thumbnail((1920 // y, 1080 // x))
                img.paste(img_in, (1920 // y * h, 1080 // x * w))
    img.save('sort_result.jpg')


if __name__ == "__main__":
    create_grid_of_images(analysis_all_files())
