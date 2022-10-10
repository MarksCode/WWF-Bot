from PIL import Image, ImageDraw
import pytesseract
from . import image_utils as utils
from . import constants

path_to_tesseract = r'/opt/homebrew/Cellar/tesseract/5.2.0/bin/tesseract.exe'
pytesseract.tesseract_cmd = path_to_tesseract
tess_config = f'--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_text_from_image(pil_img):
    text = pytesseract.image_to_string(pil_img, lang='eng', config=tess_config)
    text = text.strip()
    if not text or text == 'L':
        if utils.detect_if_rectangle(pil_img):
            return 'I'
    return text


class TextExtractor:
    def __init__(self, image_url, debug_board=False, debug_pieces=False):
        self.img = Image.open(image_url)
        self.debug_board = debug_board
        self.debug_pieces = debug_pieces
        self.draw = ImageDraw.Draw(self.img)

    def extract_board(self):
        result = []

        tile_width = 44
        spacer = 3.9
        offset_x = 443.4
        offset_y = 395.2
        num_tiles = 15

        for y in range(num_tiles):
            top = y * tile_width + spacer * y + offset_y
            row = []
            for i in range(num_tiles):
                left = i * tile_width + spacer * i + offset_x
                right = left + tile_width
                bottom = top + tile_width
                if self.debug_board:
                    self.draw.rectangle((left, top, right, bottom), outline='red')
                cropped_img = self.img.crop((left, top, right, bottom))
                dom_color = utils.get_dominant_color(cropped_img)
                text = ' '
                if dom_color not in constants.special_colors:
                    text = get_text_from_image(cropped_img)
                row.append(text)
            result.append(row)
            print(row)
        if self.debug_board:
            self.img.show()

    def extract_pieces(self):
        result = []
        tile_width = 80
        tile_height = 64
        spacer = 13.5
        offset_x = 480
        offset_y = 1215
        for i in range(7):
            left = tile_width * i + spacer * i + offset_x
            top = offset_y
            right = left + tile_width
            bottom = top + tile_height
            if self.debug_pieces:
                self.draw.rectangle((left, top, right, bottom))
            cropped_img = self.img.crop((left, top, right, bottom))
            cv2_img = utils.mask_image(cropped_img)
            text = get_text_from_image(cv2_img)
            result.append(text)
        print(result)

        if self.debug_pieces:
            self.img.show()


