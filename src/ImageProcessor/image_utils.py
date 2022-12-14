import numpy as np
import cv2
from PIL import Image
from colorthief import ColorThief
import io
import constants as consts


def is_cv2(img):
    return isinstance(img, np.ndarray)


def show_cv2(cv2_img):
    cv2.imshow('image', cv2_img)
    cv2.waitKey(0)


def convert_pil_to_cv2(pil_img):
    numpy_img = np.array(pil_img)
    cv2_img = cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR)
    return cv2_img


def convert_cv2_to_pil(cv2_img):
    color_converted = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_converted)
    return pil_image


def get_key_pixel_color(pil_img):
    width, _ = pil_img.size
    x = round(width / 2)
    y = 6
    return pil_img.getpixel((x, y))


def get_palette(pil_img):
    with io.BytesIO() as file_object:
        pil_img.save(file_object, "PNG")
        cf = ColorThief(file_object)
        colors = cf.get_palette(color_count=5, quality=3)
        return colors


def is_light_letter(cv2_img: np.ndarray):
    shape = cv2_img.shape
    h = shape[0]
    w = shape[1]
    num_white_pixels = 0
    for i in range(h):
        for y in range(w):
            color = cv2_img[i][y]
            if color > 240:
                num_white_pixels += 1
                if num_white_pixels > 40:
                    return True
    return False


def add_padding(pil_img):
    padding = 100
    width, height = pil_img.size
    new_width = width + 2 * padding
    new_height = height + 2 * padding
    result = Image.new(pil_img.mode, (new_width, new_height), '#fff')
    result.paste(pil_img, (padding, padding))
    return result


def erase_number(cv2_img):
    shape = cv2_img.shape
    w = shape[1]
    for y in range(0, 14):
        for x in range(w - 13, w - 1):
            cv2_img[y][x] = cv2_img[y][2]
    return cv2_img


def mask_image(img, debug=False):
    if not is_cv2(img):
        img = convert_pil_to_cv2(img)
    lower = (19, 31, 70) if consts.is_windows else (19, 31, 64)
    upper = (25, 45, 86) if consts.is_windows else (22, 33, 70)
    if consts.is_windows:
        img = cv2.resize(img, None, fx=1.5, fy=1.5)
    if debug:
        for i in range(len(img)):
            print(img[i])
    mask = cv2.inRange(img, lower, upper)
    is_blank = not mask.any()
    result = img.copy()
    result[mask != 255] = (255, 255, 255)
    result[mask == 255] = (0, 0, 0)
    erase_number(result)
    return result, is_blank


def detect_shape(cv2_img):
    img = erase_number(cv2_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if not is_light_letter(img):
        img = cv2.bitwise_not(img)
    _, thresh = cv2.threshold(img, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(thresh, contours, len(contours) - 1, (0, 255, 0), 3)
    if len(contours) == 0:
        return 'none'
    contour = contours[-1]

    epsilon = 0.03 * cv2.arcLength(contour, True)
    approximations = cv2.approxPolyDP(contour, epsilon, True)
    if len(approximations) == 3:
        return "triangle"
    elif len(approximations) == 4:
        return "rectangle"
    elif len(approximations) == 5:
        return "pentagon"
    elif 6 < len(approximations) < 15:
        return "ellipse"
    else:
        return "circle"


def detect_if_rectangle(img):
    if is_cv2(img):
        shape = detect_shape(img)
    else:
        shape = detect_shape(convert_pil_to_cv2(img))
    return shape == "rectangle"
