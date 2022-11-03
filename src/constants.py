import os

player_A = 'mcnutty'
player_B = 'saul'

player_nums = {player_A: 0, player_B: 1}

profile_imgs = [
    'images/saul_photo.png',
    'images/mcnutty_photo.png'
]

user_ids = {
    'mcnutty': '261715683',
    'saul': '262145972',
}

players = [player_A, player_B]
opponents = [player_B, player_A]
opponent_user_names = ['saui_goodman', 'mcnuttyy']

player_user_ids = [user_ids[player_A], user_ids[player_B]]

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y', 'Z']

board_mac = {
    'tile_width': 54,
    'spacer': 8,
    'offset_x': 433,
    'offset_y': 400,
    'num_tiles': 15,
}

board_win = {
    'tile_width': 58,
    'spacer': 15.3,
    'offset_x': 26,
    'offset_y': 600,
    'num_tiles': 15,
}

pieces_mac = {
    'tile_width': 100,
    'tile_height': 100,
    'spacer': 21,
    'offset_x': 480,
    'offset_y': 1450,
    'num_tiles': 7,
}

pieces_win = {
    'tile_width': 60,
    'tile_height': 52,
    'spacer': 16.5,
    'offset_x': 308,
    'offset_y': 1912,
    'num_tiles': 7,
}

special_tile_colors = [
    # Blank
    (238, 236, 233),
    # DL
    (98, 164, 215),
    (73, 166, 220),
    # TL
    (172, 194, 113),
    (167, 195, 101),
    # DW
    (225, 119, 101),
    (241, 111, 95),
    # TW
    (240, 158, 104),
    (254, 153, 93),
]

# cv2 in B,G,R
text_colors = [
    (19, 35, 67),
    (23, 39, 73),
]

is_windows = os.name == 'nt'

scale_factor = 1 if is_windows else 2

platform = 'win' if is_windows else 'mac'
