from os import path
from PIL import Image, ImageDraw
import pytesseract
import src.ImageProcessor.image_utils as utils
import constants as consts
import config

path_to_tesseract_mac = r'/opt/homebrew/Cellar/tesseract/5.2.0/bin/tesseract.exe'
path_to_tesseract_win = r'C:\Users\sendm\Projects\Tesseract-OCR\tesseract.exe'

if consts.is_windows:
    pytesseract.tesseract_cmd = path_to_tesseract_win
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract_win
else:
    pytesseract.tesseract_cmd = path_to_tesseract_mac
tess_config = f'--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_text_from_image(pil_img):
    text = pytesseract.image_to_string(pil_img, lang='eng', config=tess_config)
    text = text.strip()
    if not text or text == 'L':
        if utils.detect_if_rectangle(pil_img):
            return 'I'
    return text


def extract_board(img, debug=False):
    result = []
    board = consts.board_win if consts.is_windows else consts.board_mac

    for y in range(board['num_tiles']):
        top = y * board['tile_width'] + board['spacer'] * y + board['offset_y']
        row = []
        for i in range(board['num_tiles']):
            left = i * board['tile_width'] + board['spacer'] * i + board['offset_x']
            right = left + board['tile_width']
            bottom = top + board['tile_width']
            if debug:
                draw = ImageDraw.Draw(img)
                draw.rectangle((left, top, right, bottom), outline='red')
            # cropped_img = self.img.crop((left, top, right, bottom))
            # tile_color = utils.get_key_pixel_color(cropped_img)
            # if tile_color not in consts.special_tile_colors:
            #     text = get_text_from_image(cropped_img)
            #     row.append(text)
            # else:
            #     row.append(' ')
        result.append(row)
    if debug:
        img.show()
    return result


def extract_pieces(img, debug=False):
    result = []
    tile_images = []
    pieces = consts.pieces_win if consts.is_windows else consts.pieces_mac

    for i in range(pieces['num_tiles']):
        left = pieces['tile_width'] * i + pieces['spacer'] * i + pieces['offset_x']
        top = pieces['offset_y']
        right = left + pieces['tile_width']
        bottom = top + pieces['tile_height']
        if debug:
            draw = ImageDraw.Draw(img)
            draw.rectangle((left, top, right, bottom), outline='red')
        cropped_img = img.crop((left, top, right, bottom))
        tile_color = utils.get_key_pixel_color(cropped_img)
        if tile_color == (255, 255, 255):
            continue
        else:
            tile_images.append(cropped_img)
            # cv2_img, is_blank = utils.mask_image(cropped_img)
            # if i == 0:
            #     utils.show_cv2(cv2_img)
            # if is_blank:
            #     result.append('?')
            # else:
            #     text = get_text_from_image(cv2_img)
            #     result.append('L')
    if debug:
        img.show()
    return tile_images


