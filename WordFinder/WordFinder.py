import requests
from . import constants


class WordFinder:
    def __init__(self):
        pass

    def find_word(self):
        response = requests.post('http://www.wordswithfriendscheat.io/resources/api/solve-board.php', cookies=constants.cookies, headers=constants.headers, json=constants.json_data)
        print(response)
