from os import path
from PIL import Image, ImageDraw
import pytesseract
from . import image_utils as utils
import constants as consts
import config

path_to_tesseract_mac = r'/opt/homebrew/Cellar/tesseract/5.2.0/bin/tesseract.exe'
path_to_tesseract_win = r'C:\\Users\\osher\\OneDrive\\Desktop\\programming\\Tesseract-OCR\\tesseract.exe'
pytesseract.tesseract_cmd = path_to_tesseract_win
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract_win
tess_config = f'--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_text_from_image(pil_img):
    text = pytesseract.image_to_string(pil_img, lang='eng', config=tess_config)
    text = text.strip()
    if not text or text == 'L':
        if utils.detect_if_rectangle(pil_img):
            return 'I'
    return text


class TextExtractor:
    def __init__(self, image, debug_board=False, debug_pieces=False):
        if isinstance(image, str):
            image = Image.open(image)
        self.img = image.convert('RGB')
        self.debug_board = debug_board
        self.debug_pieces = debug_pieces
        self.draw = ImageDraw.Draw(self.img)

    def extract_board(self):
        result = []
        board = consts.board_mac

        for y in range(board['num_tiles']):
            top = y * board['tile_width'] + board['spacer'] * y + board['offset_y']
            row = []
            for i in range(board['num_tiles']):
                left = i * board['tile_width'] + board['spacer'] * i + board['offset_x']
                right = left + board['tile_width']
                bottom = top + board['tile_width']
                if self.debug_board:
                    self.draw.rectangle((left, top, right, bottom), outline='red')
                # cropped_img = self.img.crop((left, top, right, bottom))
                # tile_color = utils.get_key_pixel_color(cropped_img)
                # if tile_color not in consts.special_tile_colors:
                #     text = get_text_from_image(cropped_img)
                #     row.append(text)
                # else:
                #     row.append(' ')
            result.append(row)
        if self.debug_board:
            self.img.show()
        print(colors)
        return result

    def extract_pieces(self):
        result = []
        tile_images = []
        pieces = consts.pieces_mac

        for i in range(pieces['num_tiles']):
            left = pieces['tile_width'] * i + pieces['spacer'] * i + pieces['offset_x']
            top = pieces['offset_y']
            right = left + pieces['tile_width']
            bottom = top + pieces['tile_height']
            if self.debug_pieces:
                self.draw.rectangle((left, top, right, bottom), outline='red')
            cropped_img = self.img.crop((left, top, right, bottom))
            tile_images.append(cropped_img)
            tile_color = utils.get_key_pixel_color(cropped_img)
            if tile_color == (255, 255, 255):
                result.append(False)
            else:
                cv2_img = utils.mask_image(cropped_img)
                text = get_text_from_image(cv2_img)
                if not text:
                    text = '?'
                result.append(text)
        if self.debug_pieces:
            self.img.show()
        return [result, tile_images]


