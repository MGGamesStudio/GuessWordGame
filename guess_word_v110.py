import os
import sys
import json
import random
import time
import copy
from platformdirs import user_data_dir
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line

# ----- ДОСТИЖЕНИЯ -----
achievements = {
    "ach_1": {"type": "rare", "name": "5 побед", "description": "Выиграйте 5 раз.", "got": False, "date": ""},
    "ach_2": {"type": "rare", "name": "10 побед", "description": "Выиграйте 10 раз.", "got": False, "date": ""},
    "ach_3": {"type": "rare", "name": "15 побед", "description": "Выиграйте 15 раз.", "got": False, "date": ""},
    "ach_4": {"type": "rare", "name": "20 побед", "description": "Выиграйте 20 раз.", "got": False, "date": ""},
    "ach_5": {"type": "rare", "name": "25 побед", "description": "Выиграйте 25 раз.", "got": False, "date": ""},
    "ach_6": {"type": "common", "name": "5 поражений", "description": "Проиграйте 5 раз.", "got": False, "date": ""},
    "ach_7": {"type": "common", "name": "10 поражений", "description": "Проиграйте 10 раз.", "got": False, "date": ""},
    "ach_8": {"type": "common", "name": "15 поражений", "description": "Проиграйте 15 раз.", "got": False, "date": ""},
    "ach_9": {"type": "common", "name": "20 поражений", "description": "Проиграйте 20 раз.", "got": False, "date": ""},
    "ach_10": {"type": "common", "name": "25 поражений", "description": "Проиграйте 25 раз.", "got": False, "date": ""},
    "ach_11": {"type": "epic", "name": "Гений", "description": "Выиграйте с 1 попытки.", "got": False, "date": ""},
    "ach_12": {"type": "epic", "name": "Академик", "description": "Выиграйте с 2 попытки.", "got": False, "date": ""},
    "ach_13": {"type": "rare", "name": "Гроссмейстер", "description": "Выиграйте с 3 попытки.", "got": False, "date": ""},
    "ach_14": {"type": "rare", "name": "Эрудит", "description": "Выиграйте с 4 попытки.", "got": False, "date": ""},
    "ach_15": {"type": "common", "name": "Логик", "description": "Выиграйте с 5 попытки.", "got": False, "date": ""},
    "ach_16": {"type": "common", "name": "В последний вагон", "description": "Выиграйте с 6 попытки.", "got": False, "date": ""}
}
# ----- КВЕСТЫ -----
all_quests = {
    "q1": {"type": "common", "name": "РАЗМИНКА", "description": "Сыграйте 3 игры в одиночном режиме.", "reward": 50, "goal": 3, "progress": 0, "done": False},
    "q2": {"type": "common", "name": "ТОЧНОЕ ПОПАДАНИЕ", "description": "Найдите хотя бы 3 зелёные буквы за одну игру.", "reward": 50, "goal": 1, "progress": 0, "done": False},
    "q3": {"type": "common", "name": "В ПОИСКАХ ИСТИНЫ", "description": "Найдите хотя бы 3 жёлтые буквы за одну игру.", "reward": 50, "goal": 1, "progress": 0, "done": False},
    "q4": {"type": "common", "name": "РАЗВЕДКА БОЕМ", "description": "Введите слово, которого нет в словаре.", "reward": 50, "goal": 1, "progress": 0, "done": False},
    "q5": {"type": "rare", "name": "СТАБИЛЬНЫЙ РЕЗУЛЬТАТ", "description": "Одержите 2 победы подряд в одиночном режиме.", "reward": 150, "goal": 2, "progress": 0, "done": False},
    "q6": {"type": "rare", "name": "ПО ТОНКОМУ ЛЕДУ", "description": "Выиграйте игру строго на 5 или 6 попытке.", "reward": 150, "goal": 1, "progress": 0, "done": False},
    "q7": {"type": "rare", "name": "ЭКОНОМНЫЙ ЭРУДИТ", "description": "Выиграйте игру, потратив не более 4 попыток.", "reward": 150, "goal": 1, "progress": 0, "done": False},
    "q8": {"type": "rare", "name": "БУКВЕННЫЙ ПОСТ", "description": "Покрасьте на клавиатуре 10 букв в серый цвет за игру.", "reward": 150, "goal": 1, "progress": 0, "done": False},
    "q9": {"type": "epic", "name": "ИНТУИЦИЯ ГЕНИЯ", "description": "Угадайте слово со 2-й или 3-й попытки.", "reward": 350, "goal": 1, "progress": 0, "done": False},
    "q10": {"type": "epic", "name": "ЧИСТАЯ ПОБЕДА", "description": "Выиграйте игру без единой жёлтой буквы.", "reward": 350, "goal": 1, "progress": 0, "done": False},
    "q11": {"type": "epic", "name": "ЛИНГВИСТ-МАРАФОН", "description": "Одержите 5 побед за день.", "reward": 350, "goal": 5, "progress": 0, "done": False},
    "q12": {"type": "epic", "name": "ЮВЕЛИРНАЯ РАБОТА", "description": "Выиграйте игру, ни разу не нажав 'СТЕРЕТЬ'.", "reward": 350, "goal": 1, "progress": 0, "done": False}
}
# ----- ЦВЕТА -----
color_themes = {
    "classic": {"color_name": "Классика", "price": 0, "unlocked": True, "color_bg": (255/255, 255/255, 255/255, 1.0), "color_text": (31/255, 41/255, 55/255, 1.0), "color_blank": (229/255, 231/255, 235/255, 1.0), "color_correct": (34/255, 197/255, 94/255, 1.0), "color_in_word": (250/255, 204/255, 21/255, 1.0), "color_not_in_word": (148/255, 163/255, 184/255, 1.0), "color_key": (226/255, 232/255, 240/255, 1.0)},
    "night": {"color_name": "Ночь", "price": 0, "unlocked": True, "color_bg": (15/255, 23/255, 42/255, 1.0), "color_text": (248/255, 250/255, 252/255, 1.0), "color_blank": (30/255, 41/255, 59/255, 1.0), "color_correct": (34/255, 197/255, 94/255, 1.0), "color_in_word": (234/255, 179/255, 8/255, 1.0), "color_not_in_word": (71/255, 85/255, 105/255, 1.0), "color_key": (51/255, 65/255, 85/255, 1.0)},
    "ocean": {"color_name": "Океан", "price": 1000, "unlocked": False, "color_bg": (224/255, 242/255, 254/255, 1.0), "color_text": (15/255, 23/255, 42/255, 1.0), "color_blank": (186/255, 230/255, 253/255, 1.0), "color_correct": (2/255, 132/255, 199/255, 1.0), "color_in_word": (56/255, 189/255, 248/255, 1.0), "color_not_in_word": (148/255, 163/255, 184/255, 1.0), "color_key": (125/255, 211/255, 252/255, 1.0)},
    "sunset": {"color_name": "Закат", "price": 1000, "unlocked": False, "color_bg": (255/255, 247/255, 237/255, 1.0), "color_text": (67/255, 20/255, 7/255, 1.0), "color_blank": (254/255, 215/255, 170/255, 1.0), "color_correct": (234/255, 88/255, 12/255, 1.0), "color_in_word": (251/255, 191/255, 36/255, 1.0), "color_not_in_word": (168/255, 162/255, 158/255, 1.0), "color_key": (253/255, 186/255, 116/255, 1.0)},
    "sakura": {"color_name": "Сакура", "price": 1000, "unlocked": False, "color_bg": (255/255, 241/255, 242/255, 1.0), "color_text": (74/255, 4/255, 78/255, 1.0), "color_blank": (251/255, 207/255, 232/255, 1.0), "color_correct": (236/255, 72/255, 153/255, 1.0), "color_in_word": (244/255, 114/255, 182/255, 1.0), "color_not_in_word": (203/255, 213/255, 225/255, 1.0), "color_key": (253/255, 164/255, 175/255, 1.0)},
    "forest": {"color_name": "Лес", "price": 1000, "unlocked": False, "color_bg": (240/255, 253/255, 244/255, 1.0), "color_text": (5/255, 46/255, 22/255, 1.0), "color_blank": (187/255, 247/255, 208/255, 1.0), "color_correct": (21/255, 128/255, 61/255, 1.0), "color_in_word": (101/255, 163/255, 13/255, 1.0), "color_not_in_word": (148/255, 163/255, 184/255, 1.0), "color_key": (134/255, 239/255, 172/255, 1.0)},
    "royal": {"color_name": "Король", "price": 1000, "unlocked": False, "color_bg": (245/255, 243/255, 255/255, 1.0), "color_text": (46/255, 16/255, 101/255, 1.0), "color_blank": (221/255, 214/255, 254/255, 1.0), "color_correct": (124/255, 58/255, 237/255, 1.0), "color_in_word": (168/255, 85/255, 247/255, 1.0), "color_not_in_word": (148/255, 163/255, 184/255, 1.0), "color_key": (196/255, 181/255, 253/255, 1.0)},
    "lava": {"color_name": "Лава", "price": 1000, "unlocked": False, "color_bg": (254/255, 242/255, 242/255, 1.0), "color_text": (69/255, 10/255, 10/255, 1.0), "color_blank": (254/255, 202/255, 202/255, 1.0), "color_correct": (220/255, 38/255, 38/255, 1.0), "color_in_word": (251/255, 146/255, 60/255, 1.0), "color_not_in_word": (156/255, 163/255, 175/255, 1.0), "color_key": (248/255, 113/255, 113/255, 1.0)},
    "emerald": {"color_name": "Изумруд", "price": 1000, "unlocked": False, "color_bg": (236/255, 253/255, 245/255, 1.0), "color_text": (2/255, 44/255, 34/255, 1.0), "color_blank": (167/255, 243/255, 208/255, 1.0), "color_correct": (5/255, 150/255, 105/255, 1.0), "color_in_word": (16/255, 185/255, 129/255, 1.0), "color_not_in_word": (148/255, 163/255, 184/255, 1.0), "color_key": (110/255, 231/255, 183/255, 1.0)},
    "candy": {"color_name": "Конфета", "price": 1000, "unlocked": False, "color_bg": (255/255, 247/255, 251/255, 1.0), "color_text": (131/255, 24/255, 67/255, 1.0), "color_blank": (249/255, 168/255, 212/255, 1.0), "color_correct": (236/255, 72/255, 153/255, 1.0), "color_in_word": (244/255, 114/255, 182/255, 1.0), "color_not_in_word": (203/255, 213/255, 225/255, 1.0), "color_key": (253/255, 164/255, 175/255, 1.0)},
    "neon": {"color_name": "Неон", "price": 1000, "unlocked": False, "color_bg": (15/255, 23/255, 42/255, 1.0), "color_text": (255/255, 255/255, 255/255, 1.0), "color_blank": (51/255, 65/255, 85/255, 1.0), "color_correct": (0/255, 255/255, 136/255, 1.0), "color_in_word": (255/255, 230/255, 0/255, 1.0), "color_not_in_word": (100/255, 116/255, 139/255, 1.0), "color_key": (0/255, 217/255, 255/255, 1.0)},
    "gold": {"color_name": "Золото", "price": 1000, "unlocked": False, "color_bg": (255/255, 251/255, 235/255, 1.0), "color_text": (120/255, 53/255, 15/255, 1.0), "color_blank": (253/255, 230/255, 138/255, 1.0), "color_correct": (217/255, 119/255, 6/255, 1.0), "color_in_word": (250/255, 204/255, 21/255, 1.0), "color_not_in_word": (168/255, 162/255, 158/255, 1.0), "color_key": (251/255, 191/255, 36/255, 1.0)}}

color_name = color_themes["classic"]["color_name"]
color_bg = color_themes["classic"]["color_bg"]
color_text = color_themes["classic"]["color_text"]
color_blank = color_themes["classic"]["color_blank"]
color_correct = color_themes["classic"]["color_correct"]
color_in_word = color_themes["classic"]["color_in_word"]
color_not_in_word = color_themes["classic"]["color_not_in_word"]
color_key = color_themes["classic"]["color_key"]

MOBILE_ACHIVEMENTS = achievements
MOBILE_QUESTS = all_quests

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    game_save_dir = user_data_dir("GuessWordGame", "MGGamesStudio")
    if not os.path.exists(game_save_dir):
        os.makedirs(game_save_dir)
    SAVE_FILE_PATH = os.path.join(game_save_dir, "guess_word_save_file_guess_word_save_file.json")
except Exception:
    SAVE_FILE_PATH = "guess_word_save_file_guess_word_save_file.json"
