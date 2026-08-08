import os
import sys
import json
import random
from platformdirs import user_data_dir
from kivy.app import App
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.effects.scroll import ScrollEffect
from kivy.graphics import Ellipse
from kivy.graphics import Line
from kivy.animation import Animation
from kivy.properties import NumericProperty

# ----- ДОСТИЖЕНИЯ -----
achivements = {
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

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def icon_path(icon_name):
    """
    Возвращает путь к иконке внутри папки guesswordgame-icons,
    которая лежит рядом с этим файлом с кодом (или рядом с exe/apk при сборке).
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "guesswordgame-icons", icon_name)

def font_path(font_name):
    """
    Возвращает путь к шрифту внутри папки guesswordgame-fonts,
    которая лежит рядом с этим файлом с кодом (или рядом с exe/apk при сборке).
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "guesswordgame-fonts", font_name)

try:
    game_save_dir = user_data_dir("GuessWordGame", "MGGamesStudio")
    if not os.path.exists(game_save_dir):
        os.makedirs(game_save_dir)
    SAVE_FILE_PATH = os.path.join(game_save_dir, "guess_word_save_file_guess_word_save_file.json")
except Exception:
    SAVE_FILE_PATH = "guess_word_save_file_guess_word_save_file.json"

def load_words_list():
    words = resource_path("guess_word_words_list.txt")
    if not os.path.exists(words):
        return ["ПТИЦА", "АРБУЗ", "ВЕСНА", "ЭКРАН", "СЛОВО", "КНИГА", "РУЧКА"]
    try:
        with open(words, "r", encoding="utf-8") as f:
            return [line.strip().upper() for line in f if line.strip()]
    except Exception as e:
        print(f"[MGGamesStudio] Ошибка чтения словаря: {e}")
        return ["СЛОВО"]

# ----- ГЕНЕРАЦИЯ СИДА -----
SEED_BASE = 33
SEED_LENGTH = 6
SEED_MODULUS = SEED_BASE ** SEED_LENGTH
SEED_ALPHABET = "ЙЧДЕЯФЩЪСЛЮРЖВАМПУХКЬЦГЫЗОТШИЭЁБН"
SEED_MULTIPLIER = 856495781
SEED_OFFSET = 419883757
SEED_MULTIPLIER_INV = pow(SEED_MULTIPLIER, -1, SEED_MODULUS)
SEED_CHAR_TO_DIGIT = {ch: i for i, ch in enumerate(SEED_ALPHABET)}

_SEED_WORD_LIST = None
_SEED_WORD_INDEX = None
_SEED_WORD_SOURCE_ID = None

def _get_seed_word_list():
    global _SEED_WORD_LIST, _SEED_WORD_INDEX, _SEED_WORD_SOURCE_ID
    words_source = globals().get("MOBILE_ALL_WORDS") or globals().get("ALL_WORDS") or []
    source_id = id(words_source)
    if _SEED_WORD_LIST is None or _SEED_WORD_SOURCE_ID != source_id:
        unique_words = {w.strip().upper() for w in words_source if len(w.strip()) == 5}
        _SEED_WORD_LIST = sorted(unique_words)
        _SEED_WORD_INDEX = {w: i for i, w in enumerate(_SEED_WORD_LIST)}
        _SEED_WORD_SOURCE_ID = source_id
    return _SEED_WORD_LIST, _SEED_WORD_INDEX

def encode_word_to_seed(word):
    word = (word or "").strip().upper()
    if len(word) != 5:
        return None
    _, word_index = _get_seed_word_list()
    idx = word_index.get(word)
    if idx is None:
        return None
    code = (idx * SEED_MULTIPLIER + SEED_OFFSET) % SEED_MODULUS
    digits = []
    for _ in range(SEED_LENGTH):
        digits.append(code % SEED_BASE)
        code //= SEED_BASE
    digits.reverse()
    return "".join(SEED_ALPHABET[d] for d in digits)

def decode_seed_to_word(seed):
    seed = (seed or "").strip().upper()
    if len(seed) != SEED_LENGTH:
        return None
    code = 0
    for ch in seed:
        digit = SEED_CHAR_TO_DIGIT.get(ch)
        if digit is None:
            return None
        code = code * SEED_BASE + digit
    idx = ((code - SEED_OFFSET) * SEED_MULTIPLIER_INV) % SEED_MODULUS
    word_list, _ = _get_seed_word_list()
    if 0 <= idx < len(word_list):
        return word_list[idx]
    return None

def get_default_stats():
    return {
        "player_coins": 0,
        "total_wins": 0,
        "total_losses": 0,
        "current_win_streak": 0,
        "max_win_streak": 0,
        "total_completed_quests": 0,
        "last_update_day": -1,
        "active_quests": {},
        "unlocked_themes": {"classic": True},
        "active_theme_name": "classic",
        "unlocked_achivements": {},
        "settings": {}
    }

def load_game_progress():
    if not os.path.exists(SAVE_FILE_PATH):
        print("[MGGamesStudio] Файл не найден. Автоматически разворачиваем структуру сохранения...")
        default_stats = get_default_stats()
        save_game_progress(default_stats)
        return default_stats
    try:
        with open(SAVE_FILE_PATH, "r", encoding="utf-8") as file:
            save_data = json.load(file)
        print("[MGGamesStudio] Системный файл сохранения успешно прочитан лаунчером!")
        return save_data
    except Exception:
        print("[MGGamesStudio] Файл поврежден. Автоматически разворачиваем структуру сохранения...")
        default_stats = get_default_stats()
        save_game_progress(default_stats)
        return default_stats

def save_game_progress(stats):
    try:
        with open(SAVE_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(stats, file, ensure_ascii=False, indent=4)
        print("[MGGamesStudio] Прогресс успешно сохранен лаунчером в скрытый системный файл!")
    except Exception as e:
        print(f"[MGGamesStudio] Ошибка сохранения данных: {e}")

TOP_SAFE_MARGIN = dp(32)
BOTTOM_SAFE_MARGIN = dp(28)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture

_ICON_TEXTURE_CACHE = {}

def load_white_icon_texture(path):
    """
    Loads a PNG icon and returns a Kivy Texture whose RGB channels are
    forced to pure white, keeping only the original alpha channel intact.

    This exists because Kivy's Image.color acts as a multiplicative tint
    (final_channel = pixel_channel * color_channel). A black-filled icon
    (0, 0, 0) multiplied by any tint color stays black (0 * x = 0), so
    recoloring never has any visible effect. Converting the icon to a
    white-based mask (255 * x = x) makes the tint actually work, without
    requiring the source .png files themselves to be edited.
    """
    if path in _ICON_TEXTURE_CACHE:
        return _ICON_TEXTURE_CACHE[path]

    core_img = CoreImage(path)
    src_tex = core_img.texture

    if src_tex.colorfmt != 'rgba':
        # No alpha channel to preserve shape by - nothing safe to do,
        # just reuse the texture as-is.
        _ICON_TEXTURE_CACHE[path] = src_tex
        return src_tex

    pixels = bytearray(src_tex.pixels)
    for i in range(0, len(pixels), 4):
        pixels[i] = 255      # R
        pixels[i + 1] = 255  # G
        pixels[i + 2] = 255  # B
        # alpha (pixels[i + 3]) stays untouched - keeps the glyph's shape

    new_tex = Texture.create(size=src_tex.size, colorfmt='rgba')
    new_tex.blit_buffer(bytes(pixels), colorfmt='rgba', bufferfmt='ubyte')
    new_tex.flip_vertical()
    _ICON_TEXTURE_CACHE[path] = new_tex
    return new_tex

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

MOBILE_ACHIVEMENTS = {}
MOBILE_QUESTS = {}

color_name = color_themes["classic"]["color_name"]
color_bg = color_themes["classic"]["color_bg"]
color_text = color_themes["classic"]["color_text"]
color_blank = color_themes["classic"]["color_blank"]
color_correct = color_themes["classic"]["color_correct"]
color_in_word = color_themes["classic"]["color_in_word"]
color_not_in_word = color_themes["classic"]["color_not_in_word"]
color_key = color_themes["classic"]["color_key"]

def fit_font_size(label, max_allowed_w, start_font_px):
    label.text_size = (None, None)
    current_font = max(int(start_font_px), 8)
    label.font_size = f"{current_font}px"
    label.texture_update()
    shrink_steps = 0
    while label.texture_size[0] > max_allowed_w and current_font > 8 and shrink_steps < 8:
        measured_w = label.texture_size[0]
        if measured_w <= 0:
            break
        ratio = max_allowed_w / measured_w
        estimated = int(current_font * ratio)
        current_font = max(8, min(current_font - 1, estimated))
        label.font_size = f"{current_font}px"
        label.texture_update()
        shrink_steps += 1
    while label.texture_size[0] > max_allowed_w and current_font > 8:
        current_font -= 1
        label.font_size = f"{current_font}px"
        label.texture_update()

def fit_font_size_wrapped(label, max_allowed_w, max_allowed_h, start_font_px):
    label.text_size = (max_allowed_w, None)
    current_font = max(int(start_font_px), 8)
    label.font_size = f"{current_font}px"
    label.texture_update()
    shrink_steps = 0
    while label.texture_size[1] > max_allowed_h and current_font > 8 and shrink_steps < 8:
        measured_h = label.texture_size[1]
        if measured_h <= 0:
            break
        ratio = min(max_allowed_h / measured_h, 0.95)
        estimated = int(current_font * ratio)
        current_font = max(8, min(current_font - 1, estimated))
        label.font_size = f"{current_font}px"
        label.texture_update()
        shrink_steps += 1

    while label.texture_size[1] > max_allowed_h and current_font > 8:
        current_font -= 1
        label.font_size = f"{current_font}px"
        label.texture_update()

def prepare_layout_for_dynamic_sizes(container, child_widgets):
    container.size_hint_y = None
    for widget in child_widgets:
        widget.size_hint_y = None
        if widget.parent is None:
            container.add_widget(widget)

def position_header(title_label, back_btn, win_w, win_h):
    back_w, back_h = dp(92), dp(48)
    back_btn_y = win_h - TOP_SAFE_MARGIN - back_h
    back_btn.size = (back_w, back_h)
    back_btn.pos = (win_w - back_w - dp(14), back_btn_y)
    fit_font_size(back_btn, back_w - dp(18), back_h * 0.42)
    title_box_w = max(win_w - back_w - dp(14) - dp(15) - dp(10), dp(60))
    title_h = min(win_h * 0.05, dp(32))
    title_label.pos = (dp(15), back_btn_y + (back_h - title_h) / 2.0 + dp(4))
    fit_font_size(title_label, title_box_w, title_h * 0.85)
    title_label.size = (title_box_w, title_h)
    title_label.text_size = (title_box_w, title_h)
    return back_btn_y - dp(12)

def choose_theme(theme):
    global color_name, color_bg, color_text, color_blank, color_correct, color_in_word, color_not_in_word, color_key
    new_theme = color_themes[theme]
    color_name = new_theme["color_name"]
    color_bg = new_theme["color_bg"]
    color_text = new_theme["color_text"]
    color_blank = new_theme["color_blank"]
    color_correct = new_theme["color_correct"]
    color_in_word = new_theme["color_in_word"]
    color_not_in_word = new_theme["color_not_in_word"]
    color_key = new_theme["color_key"]

    if 'MOBILE_PLAYER_STATS' in globals():
        MOBILE_PLAYER_STATS["active_theme_name"] = theme
        
    if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
        MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)

    redraw_all_screens()

_SCREEN_FACTORIES = {
    'main': lambda: MainScreen(name='main'),
    'menu': lambda: MenuScreen(name='menu'),
    'play': lambda: PlayScreen(name='play'),
    'options': lambda: OptionsScreen(name='options'),
    'about': lambda: AboutScreen(name='about'),
    'license': lambda: TextDocumentScreen(name='license', title_text="Лицензия", back_target='about', source_file="LICENSE.txt"),
    'third_party': lambda: TextDocumentScreen(name='third_party', title_text="Сторонние компоненты", back_target='about', source_file="THIRD-PARTY NOTICES.txt"),
    'about_game': lambda: TextDocumentScreen(name='about_game', title_text="О игре", back_target='about', source_file="README.txt"),
    'special_thanks': lambda: TextDocumentScreen(name='special_thanks', title_text="Особая благодарность", back_target='about', source_file="SPECIAL-THANKS.txt"),
    'how_to_play': lambda: HowToPlayScreen(name='how_to_play'),
    'achievements': lambda: AchievementsScreen(name='achievements'),
    'customization': lambda: CustomizationScreen(name='customization'),
    'quests': lambda: QuestsScreen(name='quests'),
    'one_player_game': lambda: OnePlayerGameScreen(name='one_player_game'),
    'two_player_game': lambda: TwoPlayerGameScreen(name='two_player_game'),
    'seed_generation': lambda: SeedGenerationScreen(name='seed_generation'),
    'seed_create': lambda: SeedCreateScreen(name='seed_create'),
    'seed_enter': lambda: SeedEnterScreen(name='seed_enter'),
}

_pending_screen_rebuild_event = None

def redraw_all_screens():
    global _pending_screen_rebuild_event
    from kivy.core.window import Window

    app = App.get_running_app()
    if not app or not app.root:
        return

    sm = app.root

    Window.clearcolor = color_bg

    if hasattr(sm, 'canvas'):
        if sm.canvas.before:
            for instr in sm.canvas.before.children:
                if instr.__class__.__name__ == 'Color':
                    instr.rgba = color_bg
        if sm.canvas.children:
            for instr in sm.canvas.children:
                if instr.__class__.__name__ == 'Color':
                    instr.rgba = color_bg

    if _pending_screen_rebuild_event is not None:
        _pending_screen_rebuild_event.cancel()
        _pending_screen_rebuild_event = None

    current_name = sm.current
    current_screen = sm.get_screen(current_name) if current_name else None

    if current_screen is None or not hasattr(current_screen, 'apply_theme_instant'):
        _redraw_all_screens_full_rebuild(sm)
        return

    current_screen.apply_theme_instant()
    pending_names = [name for name in _SCREEN_FACTORIES if name != current_name and sm.has_screen(name)]

    def rebuild_chunk(dt):
        global _pending_screen_rebuild_event
        BATCH_SIZE = 2
        for _ in range(BATCH_SIZE):
            if not pending_names:
                _pending_screen_rebuild_event = None
                return False
            name = pending_names.pop(0)
            factory = _SCREEN_FACTORIES.get(name)
            if factory is None or not sm.has_screen(name) or name == sm.current:
                continue
            old_scr = sm.get_screen(name)
            new_scr = factory()
            sm.remove_widget(old_scr)
            sm.add_widget(new_scr)
        return True

    _pending_screen_rebuild_event = Clock.schedule_interval(rebuild_chunk, 0)

def _redraw_all_screens_full_rebuild(sm):
    from kivy.uix.screenmanager import NoTransition

    old_transition = sm.transition
    sm.transition = NoTransition()
    sm.current = 'main'
    screens_to_recreate = [screen.name for screen in list(sm.screens)]

    for screen_name in screens_to_recreate:
        old_scr = sm.get_screen(screen_name)
        sm.remove_widget(old_scr)

    for name, factory in _SCREEN_FACTORIES.items():
        sm.add_widget(factory())

    sm.current = 'customization'
    sm.transition = old_transition

def apply_adaptive_fonts(screen_instance, cell_height, key_height):
    cell_pad_bottom = cell_height * 0.08
    for cell in screen_instance.cells:
        cell.font_size = f"{cell_height * 0.50}px"
        cell.text_size = cell.size
        cell.halign = 'center'
        cell.valign = 'middle'
        cell.padding = [0, 0, 0, cell_pad_bottom]

    key_width = screen_instance.keyboard_keys[0].width if screen_instance.keyboard_keys else 30
    safe_side_key = min(key_width, key_height)
    key_font_size_px = safe_side_key * 0.8
    key_pad_bottom = key_height * 0.08

    for key in screen_instance.keyboard_keys:
        key.font_size = f"{key_font_size_px}px"
        key.text_size = key.size
        key.halign = 'center'
        key.valign = 'middle'
        key.padding = [0, 0, 0, key_pad_bottom]

    sys_pad_bottom = key_height * 0.07

    for btn in screen_instance.system_buttons:
        btn.text_size = (None, None)
        fit_font_size(btn, btn.width * 0.88, key_font_size_px)
        btn.text_size = btn.size
        btn.halign = 'center'
        btn.valign = 'middle'
        btn.shorten = False
        btn.padding = [0, 0, 0, sys_pad_bottom]

class MenuButton(Button):
    def __init__(self, text="", pos_hint=None, size_hint=(0.93, None), height=84, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_name = font_path("ClearSans-Bold.ttf")
        self.font_size = '30sp'
        self.bold = True
        
        self.halign = 'center'
        self.valign = 'middle'
        self.padding = [0, -5, 0, 5]
        
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        
        self.size_hint = size_hint
        self.height = height
        
        if pos_hint:
            self.pos_hint = pos_hint
            
        self.base_color = color_key
        self.color = color_text

        with self.canvas.before:
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)

    def update_canvas(self, *args):
        if self.state == 'normal':
            self.bg_color_instr.rgba = self.base_color
        else:
            self.bg_color_instr.rgba = (self.base_color[0]*0.8, self.base_color[1]*0.8, self.base_color[2]*0.8, 1.0)
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class ModeButton(BoxLayout):
    def __init__(self, title_text="", description_text="", description_color=None, on_release=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [15, 28, 15, 6]
        self.spacing = 14
        
        self.on_release_func = on_release
        
        self.size_hint = (None, None)
        self.size = (350, 200)
        
        self.base_color = color_key
        self.current_bg = list(self.base_color)

        self.title_label = Label(
            text=title_text,
            font_name=font_path("ClearSans-Bold.ttf"),
            font_size='30sp',
            bold=True,
            color=color_text,
            halign='center',
            valign='bottom',
            size_hint=(1, None)
        )
        self.title_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        
        self.sub_label = Label(
            text=description_text,
            font_name=font_path("ClearSans-Bold.ttf"),
            font_size='14sp',
            color=description_color if description_color else color_text,
            halign='center',
            valign='top',
            size_hint=(1, None)
        )
        self.sub_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        
        self.add_widget(self.title_label)
        self.add_widget(self.sub_label)

        with self.canvas.before:
            self.bg_color_instr = Color(*self.current_bg)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_color_instr.rgba = self.current_bg
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.current_bg = [c * 0.8 for c in self.base_color[:3]] + [1.0]
            self.update_canvas()
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.current_bg = list(self.base_color)
            self.update_canvas()
            touch.ungrab(self)
            if self.collide_point(*touch.pos) and self.on_release_func:
                self.on_release_func(self)
            return True
        return super().on_touch_up(touch)

class GameCell(Label):
    def __init__(self, size=(74, 92), pos=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.text = ""
        self.font_name = font_path("ClearSans-Bold.ttf")
        self.font_size = '32sp'
        self.bold = True
        
        self.size_hint = (None, None)
        self.size = size
        self.pos = pos
        
        self.cell_status = "blank"
        self.base_color = color_blank
        self.text_color = color_text

        self.color = self.text_color

        with self.canvas.before:
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8])

        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def change_type(self, letter_type):
        self.cell_status = letter_type
        if letter_type == "blank":
            self.base_color = color_blank
            self.text_color = color_text
        elif letter_type == "correct":
            self.base_color = color_correct
            self.text_color = (1.0, 1.0, 1.0, 1.0)
        elif letter_type == "in_word":
            self.base_color = color_in_word
            self.text_color = (0.0, 0.0, 0.0, 1.0)
        elif letter_type == "not_in_word":
            self.base_color = color_not_in_word
            self.text_color = (1.0, 1.0, 1.0, 1.0)

        self.color = self.text_color
        self.update_canvas()

    def update_canvas(self, *args):
        corner_radius = min(min(self.width, self.height) * 0.12, 8)
        self.bg_color_instr.rgba = self.base_color
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.bg_rect.radius = [corner_radius]

class KeyButton(Button):
    def __init__(self, text="", size=(40, 85), **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_name = font_path("ClearSans-Bold.ttf")
        self.font_size = '16sp'
        self.bold = True
        self.halign = 'center'
        self.valign = 'middle'
        
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0.01)
        
        self.size_hint = (None, None)
        self.size = size
        
        self.base_color = color_key
        self.cell_status = "blank"
        self.color = color_text

        with self.canvas.before:
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[6])

        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)

    def update_canvas(self, *args):
        if self.state == 'normal':
            self.bg_color_instr.rgba = self.base_color
        else:
            self.bg_color_instr.rgba = (self.base_color[0]*0.8, self.base_color[1]*0.8, self.base_color[2]*0.8, 1.0)
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class IconKeyButton(KeyButton):
    def __init__(self, image_source="backspace.png", icon_ratio=0.5, size=(100, 50), **kwargs):
        super().__init__(text="", size=size, **kwargs)
        self._icon_ratio = icon_ratio
        self.icon = Image(
            size_hint=(None, None),
            fit_mode="contain",
            color=self.color,
        )
        self.icon.texture = load_white_icon_texture(icon_path(image_source))
        self.add_widget(self.icon)
        self.bind(pos=self._update_icon, size=self._update_icon)
        self._update_icon()

    def _update_icon(self, *args):
        side = min(self.width, self.height)
        icon_side = side * self._icon_ratio
        self.icon.size = (icon_side, icon_side)
        self.icon.center = self.center

    def update_canvas(self, *args):
        super().update_canvas(*args)
        self.icon.color = self.color

class ThemeCard(ButtonBehavior, FloatLayout):
    def __init__(self, theme_id="classic", theme_name="Классика", theme_data=None, on_click_callback=None, **kwargs):
        self.is_active = False 
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.theme_id = theme_id
        self.on_click_callback = on_click_callback
        
        if theme_data:
            self.c_bg = theme_data.get('color_bg', color_bg)
            self.c_text = theme_data.get('color_text', color_text)
            self.c_correct = theme_data.get('color_correct', color_correct)
            self.c_in_word = theme_data.get('color_in_word', color_in_word)
            self.c_not_in_word = theme_data.get('color_not_in_word', color_not_in_word)
            self.c_blank = theme_data.get('color_blank', color_blank)
            self.c_key = theme_data.get('color_key', color_key)
        else:
            self.c_bg, self.c_text = color_bg, color_text
            self.c_correct, self.c_in_word = color_correct, color_in_word
            self.c_not_in_word, self.c_blank = color_not_in_word, color_blank
            self.c_key = color_key

        self.block_colors = [self.c_blank, self.c_correct, self.c_in_word, self.c_not_in_word, self.c_blank]
        self.text_colors  = [self.c_text, (1, 1, 1, 1), (0, 0, 0, 1), (1, 1, 1, 1), self.c_text]

        super().__init__(**kwargs)
        self.size_hint = (None, None)

        with self.canvas.before:
            Color(*self.c_bg)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
            
            self.active_circle_color = Color(*self.c_correct)
            self.active_circle = Ellipse(pos=(0, 0), size=(0, 0))

        self.lbl_name = Label(
            text=theme_name,
            font_name=font_path("ClearSans-Bold.ttf"),
            font_size='18sp',
            color=self.c_text,
            bold=True,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.lbl_name.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.add_widget(self.lbl_name)

        self.tiles = []
        self.tile_rects = []
        self.tile_colors = []

        for i in range(5):
            lbl_a = Label(
                text="A",
                font_name=font_path("ClearSans-Bold.ttf"),
                font_size='22sp',
                color=self.text_colors[i],
                bold=True,
                size_hint=(None, None),
                halign='center',
                valign='middle'
            )
            with self.canvas:
                c_inst = Color(*self.block_colors[i])
                rect = RoundedRectangle(pos=(0,0), size=(0,0), radius=[6])
                self.tile_colors.append(c_inst)
                self.tile_rects.append(rect)
                
            self.tiles.append(lbl_a)
            self.add_widget(lbl_a)

        self.kb_rects = []
        self.kb_colors = []
        with self.canvas:
            for _ in range(20):
                c_inst = Color(*self.c_key)
                rect = RoundedRectangle(pos=(0,0), size=(0,0), radius=[3])
                self.kb_colors.append(c_inst)
                self.kb_rects.append(rect)
            
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.is_selected = False

        with self.canvas.after:
            self.select_line_color = Color(*color_in_word)
            self.select_line = Line(width=2)

    def update_graphics(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
        self.lbl_name.size = (self.width, dp(28))
        self.lbl_name.pos = (self.x, self.y + 5)
        self.lbl_name.text_size = (None, None)
        fit_font_size(self.lbl_name, self.width - dp(20), dp(18))
        self.lbl_name.size = self.lbl_name.texture_size
        self.lbl_name.center_x = self.x + self.width / 2
        self.lbl_name.y = self.y + 5

        spacing = dp(8)
        tile_size_by_h = self.height * 0.33
        tile_size_by_w = (self.width - dp(20) - spacing * 4) / 5
        tile_size = max(min(tile_size_by_h, tile_size_by_w), dp(16))
        total_grid_w = (tile_size * 5) + (spacing * 4)
        start_x = self.x + (self.width - total_grid_w) / 2
        tile_y = self.y + self.height - tile_size - dp(10)
        
        for i, lbl_a in enumerate(self.tiles):
            current_x = start_x + i * (tile_size + spacing)
            lbl_a.size = (tile_size, tile_size)
            lbl_a.pos = (current_x, tile_y + tile_size * 0.04)
            lbl_a.text_size = (tile_size, tile_size)
            fit_font_size(lbl_a, tile_size * 0.8, tile_size * 0.7)
            lbl_a.text_size = (tile_size, tile_size)
            
            self.tile_colors[i].rgba = self.block_colors[i]
            self.tile_rects[i].pos = (current_x, tile_y)
            self.tile_rects[i].size = (tile_size, tile_size)

        kb_size = tile_size * 0.38  
        kb_spacing_x = dp(4)
        kb_spacing_y = dp(4)
        total_kb_w = (kb_size * 10) + (kb_spacing_x * 9)
        start_kb_x = self.x + (self.width - total_kb_w) / 2
        start_kb_y = tile_y - (kb_size * 2 + kb_spacing_y) - dp(8)
        
        for index in range(20):
            row = index // 10  
            col = index % 10   
            kx = start_kb_x + col * (kb_size + kb_spacing_x)
            ky = start_kb_y + (1 - row) * (kb_size + kb_spacing_y)
            
            self.kb_colors[index].rgba = self.c_key
            self.kb_rects[index].pos = (kx, ky)
            self.kb_rects[index].size = (kb_size, kb_size)

        self.update_indicators()

    def update_indicators(self, *args):
        if self.is_active:
            circle_size = 16
            cx = self.x + self.width - circle_size - 15
            cy = self.y + self.height - circle_size - 15

            self.active_circle_color.rgba = self.c_correct
            self.active_circle.pos = (cx, cy)
            self.active_circle.size = (circle_size, circle_size)
        else:
            self.active_circle.size = (0, 0)
            self.active_circle_color.rgba = (0, 0, 0, 0)

        if self.is_selected:
            self.select_line_color.rgba = color_in_word
            self.select_line.rounded_rectangle = (self.x, self.y, self.width, self.height, 12, 12, 12, 12)
        else:
            self.select_line.rounded_rectangle = (0, 0, 0, 0, 0)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not touch.is_mouse_scrolling:
                if self.on_click_callback:
                    self.on_click_callback(self.theme_id)
                return True
        return super().on_touch_down(touch)

# ----- ИГРА ----
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.title_label = Label(
            text="Угадай слово", 
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True, 
            color=color_text,
            size_hint=(None, None), 
            halign='center', 
            valign='middle'
        )

        self.buttons_container = BoxLayout(
            orientation='vertical', 
            size_hint=(None, None)
        )

        self.buttons = [
            MenuButton(text="Играть"),
            MenuButton(text="Меню"),
            MenuButton(text="Настройки")
        ]
        for btn in self.buttons:
            btn.font_name = font_path("ClearSans-Bold.ttf")

        self.buttons[0].base_color = color_correct
        self.buttons[0].color = (1.0, 1.0, 1.0, 1.0)

        self.buttons[0].bind(on_release=lambda x: setattr(self.manager, 'current', 'play'))
        self.buttons[1].bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.buttons[2].bind(on_release=lambda x: setattr(self.manager, 'current', 'options'))

        for btn in self.buttons:
            btn.size_hint = (1, None)
            self.buttons_container.add_widget(btn)

        self.copy_label = Label(
            text="Угадай слово by MGGamesStudio. v.1.1.0", 
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_not_in_word,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.buttons_container)
        self.layout.add_widget(self.copy_label)
        self.add_widget(self.layout)
        
        self.bind(size=self.reposition_menu_elements)
        self.reposition_menu_elements()
        Clock.schedule_once(lambda dt: self.reposition_menu_elements(), 0)

    def reposition_menu_elements(self, *args):
        win_w, win_h = self.width, self.height
        top_limit = win_h - TOP_SAFE_MARGIN
        bottom_limit = BOTTOM_SAFE_MARGIN
        copy_h = dp(16)
        self.copy_label.text_size = (None, None)
        fit_font_size(self.copy_label, win_w * 0.92, copy_h)
        self.copy_label.size = self.copy_label.texture_size
        self.copy_label.center_x = win_w / 2
        self.copy_label.y = bottom_limit
        available_h = top_limit - bottom_limit - self.copy_label.height - dp(12)
        container_w = win_w * 0.9
        total_elements = 3
        spacing_h = dp(14)
        max_btn_h = dp(84)

        btn_h = (available_h * 0.55 - spacing_h * (total_elements - 1)) / total_elements
        btn_h = max(min(btn_h, max_btn_h), dp(48))
        container_h = btn_h * total_elements + spacing_h * (total_elements - 1)

        self.buttons_container.size = (container_w, container_h)
        self.buttons_container.spacing = spacing_h
        self.buttons_container.center_x = win_w / 2
        self.buttons_container.center_y = win_h / 2

        for btn in self.buttons:
            btn.height = btn_h
            fit_font_size(btn, container_w - dp(36), btn_h * 0.42)

        distance_to_top = top_limit - self.buttons_container.top
        title_h = min(distance_to_top * 0.6, dp(60))
        self.title_label.size = (win_w * 0.9, title_h)
        self.title_label.center_x = win_w / 2
        self.title_label.y = self.buttons_container.top + (distance_to_top - title_h) / 2
        fit_font_size(self.title_label, win_w * 0.9, title_h * 0.85)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        self.btn_back.font_name = font_path("ClearSans-Bold.ttf")
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        self.layout.add_widget(self.btn_back)

        self.title_label = Label(
            text="Меню",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )
        self.layout.add_widget(self.title_label)

        self.buttons_container = BoxLayout(orientation='vertical', size_hint=(None, None))

        self.buttons = [
            MenuButton(text="Как играть"),
            MenuButton(text="Достижения"),
            MenuButton(text="Кастомизация"),
            MenuButton(text="Квесты")
        ]
        for btn in self.buttons:
            btn.font_name = font_path("ClearSans-Bold.ttf")
            btn.size_hint = (1, None)
            self.buttons_container.add_widget(btn)

        self.buttons[0].bind(on_release=lambda x: setattr(self.manager, 'current', 'how_to_play'))
        self.buttons[1].bind(on_release=lambda x: setattr(self.manager, 'current', 'achievements'))
        self.buttons[2].bind(on_release=lambda x: setattr(self.manager, 'current', 'customization'))
        self.buttons[3].bind(on_release=lambda x: setattr(self.manager, 'current', 'quests'))

        self.layout.add_widget(self.buttons_container)
        self.add_widget(self.layout)

        self.bind(size=self.reposition_elements)
        self.reposition_elements()
        Clock.schedule_once(lambda dt: self.reposition_elements(), 0)

    def on_pre_leave(self):
        self.opacity = 0

    def on_pre_enter(self):
        self.opacity = 1

    def reposition_elements(self, *args):
        win_w, win_h = self.width, self.height

        content_top = position_header(self.title_label, self.btn_back, win_w, win_h)

        bottom_limit = BOTTOM_SAFE_MARGIN
        available_h = content_top - bottom_limit

        container_w = win_w * 0.9
        total_elements = 4
        spacing_h = dp(12)
        max_btn_h = dp(76)

        btn_h = (available_h - spacing_h * (total_elements - 1)) / total_elements
        btn_h = max(min(btn_h, max_btn_h), dp(44))
        container_h = btn_h * total_elements + spacing_h * (total_elements - 1)

        self.buttons_container.size = (container_w, container_h)
        self.buttons_container.spacing = spacing_h
        self.buttons_container.center_x = win_w / 2
        self.buttons_container.center_y = bottom_limit + available_h * 0.5

        for btn in self.buttons:
            btn.height = btn_h
            fit_font_size(btn, container_w - dp(36), btn_h * 0.4)

class ToggleSwitch(ButtonBehavior, FloatLayout):
    progress = NumericProperty(0.0)

    def __init__(self, active=False, on_toggle=None, **kwargs):
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(56), dp(31)))
        super().__init__(**kwargs)

        self.on_toggle_callback = on_toggle
        self.active = active
        self.progress = 1.0 if active else 0.0

        with self.canvas.before:
            self.track_color_instr = Color(*color_not_in_word)
            self.track_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height / 2])

        with self.canvas:
            self.knob_color_instr = Color(*self._knob_color(self.progress))
            self.knob_ellipse = Ellipse(pos=(0, 0), size=(0, 0))

        self.bind(pos=self._update_graphics, size=self._update_graphics, progress=self._update_graphics)
        self._update_graphics()

    @staticmethod
    def _knob_color(progress):
        c1, c2 = color_key, color_bg
        return [c1[i] + (c2[i] - c1[i]) * progress for i in range(4)]

    def _update_graphics(self, *args):
        radius = self.height / 2
        self.track_rect.pos = self.pos
        self.track_rect.size = self.size
        self.track_rect.radius = [radius]
        self.track_color_instr.rgba = color_not_in_word

        margin = dp(3)
        knob_d = max(self.height - margin * 2, 1)
        travel = max(self.width - knob_d - margin * 2, 0)
        knob_x = self.x + margin + travel * self.progress
        knob_y = self.y + margin
        self.knob_ellipse.pos = (knob_x, knob_y)
        self.knob_ellipse.size = (knob_d, knob_d)
        self.knob_color_instr.rgba = self._knob_color(self.progress)

    def on_release(self):
        self.set_active(not self.active)

    def set_active(self, active, animate=True, fire_callback=True):
        self.active = active
        target = 1.0 if active else 0.0
        Animation.cancel_all(self, 'progress')
        if animate:
            Animation(progress=target, duration=0.18, t='out_quad').start(self)
        else:
            self.progress = target
        if fire_callback and self.on_toggle_callback:
            self.on_toggle_callback(active)

class SettingToggleRow(FloatLayout):
    def __init__(self, text, active=False, on_toggle=None, **kwargs):
        kwargs.setdefault('size_hint', (1, None))
        super().__init__(**kwargs)

        self.v_pad = dp(14)
        self.h_gap = dp(14)
        self.base_font_px = dp(26)

        self.switch = ToggleSwitch(active=active, on_toggle=on_toggle)
        self.add_widget(self.switch)

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_text,
            halign='left',
            valign='top',
            size_hint=(None, None)
        )
        self.add_widget(self.label)

        self.height = dp(60)
        self.bind(pos=self._relayout, size=self._relayout)
        Clock.schedule_once(lambda dt: self._relayout(), 0)

    def _relayout(self, *args):
        if self.width <= 0:
            return

        label_w = max(self.width - self.switch.width - self.h_gap, dp(10))
        fit_font_size_wrapped(self.label, label_w, dp(300), self.base_font_px)
        # Важно: text_size и size у Label должны совпадать (как у заголовка
        # экрана), иначе текстура рисуется с нецелым субпиксельным смещением
        # и буквы выглядят размытыми.
        real_h = self.label.texture_size[1]
        self.label.text_size = (label_w, real_h)
        self.label.size = (label_w, real_h)

        content_h = max(self.label.height, self.switch.height)
        new_height = content_h + self.v_pad * 2
        if abs(new_height - self.height) > 0.5:
            self.height = new_height
            return

        self.label.pos = (round(self.x), round(self.y + self.height - self.v_pad - self.label.height))
        self.switch.pos = (round(self.x + self.width - self.switch.width), round(self.y + (self.height - self.switch.height) / 2))

class SettingLinkRow(ButtonBehavior, FloatLayout):
    def __init__(self, text, on_press_callback=None, **kwargs):
        kwargs.setdefault('size_hint', (1, None))
        super().__init__(**kwargs)

        self.v_pad = dp(10)
        self.base_font_px = dp(26)
        self.on_press_callback = on_press_callback

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_correct,
            halign='left',
            valign='top',
            size_hint=(None, None)
        )
        self.add_widget(self.label)

        self.height = dp(40)
        self.bind(pos=self._relayout, size=self._relayout)
        Clock.schedule_once(lambda dt: self._relayout(), 0)

    def _relayout(self, *args):
        if self.width <= 0:
            return

        fit_font_size(self.label, self.width, self.base_font_px)
        real_w, real_h = self.label.texture_size
        self.label.text_size = (real_w, real_h)
        self.label.size = (real_w, real_h)

        new_height = self.label.height + self.v_pad * 2
        if abs(new_height - self.height) > 0.5:
            self.height = new_height
            return

        self.label.pos = (round(self.x), round(self.y + self.height - self.v_pad - self.label.height))

    def on_release(self):
        if self.on_press_callback:
            self.on_press_callback()

class SettingInfoRow(FloatLayout):
    def __init__(self, text, value="", **kwargs):
        kwargs.setdefault('size_hint', (1, None))
        super().__init__(**kwargs)

        self.v_pad = dp(14)
        self.h_gap = dp(14)
        self.base_font_px = dp(26)

        self.value_label = Label(
            text=value,
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_not_in_word,
            halign='right',
            valign='top',
            size_hint=(None, None)
        )
        self.add_widget(self.value_label)

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_text,
            halign='left',
            valign='top',
            size_hint=(None, None)
        )
        self.add_widget(self.label)

        self.height = dp(60)
        self.bind(pos=self._relayout, size=self._relayout)
        Clock.schedule_once(lambda dt: self._relayout(), 0)

    def _relayout(self, *args):
        if self.width <= 0:
            return

        max_value_w = max(self.width * 0.5, dp(10))
        fit_font_size(self.value_label, max_value_w, self.base_font_px)
        real_vw, real_vh = self.value_label.texture_size
        self.value_label.text_size = (real_vw, real_vh)
        self.value_label.size = (real_vw, real_vh)

        label_w = max(self.width - self.value_label.width - self.h_gap, dp(10))
        fit_font_size_wrapped(self.label, label_w, dp(300), self.base_font_px)
        real_h = self.label.texture_size[1]
        self.label.text_size = (label_w, real_h)
        self.label.size = (label_w, real_h)

        content_h = max(self.label.height, self.value_label.height)
        new_height = content_h + self.v_pad * 2
        if abs(new_height - self.height) > 0.5:
            self.height = new_height
            return

        self.label.pos = (round(self.x), round(self.y + self.height - self.v_pad - self.label.height))
        self.value_label.pos = (round(self.x + self.width - self.value_label.width), round(self.y + self.height - self.v_pad - self.value_label.height))

class OptionsScreen(Screen):
    settings_definitions = [
        {"type": "toggle", "key": "confirm_exit", "text": "Спрашивать повторно при выходе из игры", "default": False},
        {"type": "link", "text": "О программе", "target": "about"}
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        self.btn_back.font_name = font_path("ClearSans-Bold.ttf")
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        self.layout.add_widget(self.btn_back)

        self.title_label = Label(
            text="Настройки",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )
        self.layout.add_widget(self.title_label)

        self.settings_scroll = ScrollView(size_hint=(None, None), do_scroll_x=False, do_scroll_y=True, bar_width=0)
        self.settings_scroll.effect_cls = ScrollEffect

        self.settings_list_layout = GridLayout(cols=1, spacing=dp(4), size_hint=(1, None), padding=[0, 0, 0, dp(20)])
        self.settings_list_layout.bind(minimum_height=self.settings_list_layout.setter('height'))

        self.settings_scroll.add_widget(self.settings_list_layout)
        self.layout.add_widget(self.settings_scroll)

        self.add_widget(self.layout)
        self.build_settings_list()

        self.bind(size=self.reposition_elements)
        self.reposition_elements()
        Clock.schedule_once(lambda dt: self.reposition_elements(), 0)

    def build_settings_list(self):
        self.settings_list_layout.clear_widgets()

        stats = MOBILE_PLAYER_STATS if ('MOBILE_PLAYER_STATS' in globals() and MOBILE_PLAYER_STATS) else {}
        saved_settings = stats.get("settings", {})

        for item in self.settings_definitions:
            if item["type"] == "toggle":
                current_value = saved_settings.get(item["key"], item.get("default", False))
                row = SettingToggleRow(
                    text=item["text"],
                    active=current_value,
                    on_toggle=self._make_toggle_handler(item["key"])
                )
                self.settings_list_layout.add_widget(row)
            elif item["type"] == "link":
                row = SettingLinkRow(
                    text=item["text"],
                    on_press_callback=self._make_link_handler(item["target"])
                )
                self.settings_list_layout.add_widget(row)

    def _make_toggle_handler(self, key):
        def _handler(value):
            if 'MOBILE_PLAYER_STATS' in globals() and MOBILE_PLAYER_STATS is not None:
                MOBILE_PLAYER_STATS.setdefault("settings", {})[key] = value
                if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
                    MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)
        return _handler

    def _make_link_handler(self, target_screen):
        def _handler():
            setattr(self.manager, 'current', target_screen)
        return _handler

    def reposition_elements(self, *args):
        win_w, win_h = self.width, self.height
        if win_w <= 0 or win_h <= 0:
            return

        content_top = position_header(self.title_label, self.btn_back, win_w, win_h)
        bottom_limit = int(round(BOTTOM_SAFE_MARGIN))
        side_margin = int(round(dp(15)))

        scroll_w = int(round(win_w - side_margin * 2))
        scroll_h = int(round(max(content_top - bottom_limit, dp(10))))

        self.settings_scroll.pos = (side_margin, bottom_limit)
        self.settings_scroll.size = (scroll_w, scroll_h)
        self.settings_list_layout.width = scroll_w

class AboutScreen(Screen):
    about_definitions = [
        {"type": "info", "text": "Версия игры", "value": "v.1.1.0"},
        {"type": "info", "text": "Автор", "value": "MGGamesStudio"},
        {"type": "link", "text": "Особая благодарность", "target": "special_thanks"},
        {"type": "link", "text": "Лицензия", "target": "license"},
        {"type": "link", "text": "Сторонние компоненты", "target": "third_party"},
        {"type": "link", "text": "О игре", "target": "about_game"}
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        self.btn_back.font_name = font_path("ClearSans-Bold.ttf")
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'options'))
        self.layout.add_widget(self.btn_back)

        self.title_label = Label(
            text="О программе",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )
        self.layout.add_widget(self.title_label)

        self.about_scroll = ScrollView(size_hint=(None, None), do_scroll_x=False, do_scroll_y=True, bar_width=0)
        self.about_scroll.effect_cls = ScrollEffect

        self.about_list_layout = GridLayout(cols=1, spacing=dp(4), size_hint=(1, None), padding=[0, 0, 0, dp(20)])
        self.about_list_layout.bind(minimum_height=self.about_list_layout.setter('height'))

        self.about_scroll.add_widget(self.about_list_layout)
        self.layout.add_widget(self.about_scroll)

        self.add_widget(self.layout)
        self.build_about_list()

        self.bind(size=self.reposition_elements)
        self.reposition_elements()
        Clock.schedule_once(lambda dt: self.reposition_elements(), 0)

    def build_about_list(self):
        self.about_list_layout.clear_widgets()

        for item in self.about_definitions:
            if item["type"] == "info":
                row = SettingInfoRow(text=item["text"], value=item.get("value", ""))
                self.about_list_layout.add_widget(row)
            elif item["type"] == "link":
                row = SettingLinkRow(
                    text=item["text"],
                    on_press_callback=self._make_link_handler(item["target"])
                )
                self.about_list_layout.add_widget(row)

    def _make_link_handler(self, target_screen):
        def _handler():
            setattr(self.manager, 'current', target_screen)
        return _handler

    def reposition_elements(self, *args):
        win_w, win_h = self.width, self.height
        if win_w <= 0 or win_h <= 0:
            return

        content_top = position_header(self.title_label, self.btn_back, win_w, win_h)
        bottom_limit = int(round(BOTTOM_SAFE_MARGIN))
        side_margin = int(round(dp(15)))

        scroll_w = int(round(win_w - side_margin * 2))
        scroll_h = int(round(max(content_top - bottom_limit, dp(10))))

        self.about_scroll.pos = (side_margin, bottom_limit)
        self.about_scroll.size = (scroll_w, scroll_h)
        self.about_list_layout.width = scroll_w

class TextDocumentScreen(Screen):
    def __init__(self, title_text="", back_target="about", source_file=None, **kwargs):
        super().__init__(**kwargs)
        self.back_target = back_target
        self.layout = FloatLayout()

        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        self.btn_back.font_name = font_path("ClearSans-Bold.ttf")
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', self.back_target))
        self.layout.add_widget(self.btn_back)

        self.title_label = Label(
            text=title_text,
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )
        self.layout.add_widget(self.title_label)

        self.doc_scroll = ScrollView(size_hint=(None, None), do_scroll_x=False, do_scroll_y=True, bar_width=0)
        self.doc_scroll.effect_cls = ScrollEffect
        if self.doc_scroll.effect_cls:
            self.doc_scroll.effect_cls.bounces = False

        self.content_box = BoxLayout(orientation='vertical', size_hint_y=None, padding=[0, 0, 0, dp(20)])
        self.content_box.bind(minimum_height=self.content_box.setter('height'))

        self.text_label = Label(
            text=self._load_document_text(source_file),
            font_name=font_path("ClearSans-Bold.ttf"),
            font_size='14sp',
            color=color_text,
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.text_label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
        self.content_box.add_widget(self.text_label)

        self.doc_scroll.add_widget(self.content_box)
        self.layout.add_widget(self.doc_scroll)

        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)
        self.reposition_elements()
        Clock.schedule_once(lambda dt: self.reposition_elements(), 0)

    def _load_document_text(self, source_file):
        if not source_file:
            return "Здесь пока что ничего нет."
        try:
            file_path = resource_path(source_file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            return content if content else "Здесь пока что ничего нет."
        except Exception as e:
            print(f"[MGGamesStudio] Ошибка чтения документа {source_file}: {e}")
            return "Не удалось загрузить файл."

    def reposition_elements(self, *args):
        win_w, win_h = self.width, self.height
        if win_w <= 0 or win_h <= 0:
            return

        content_top = position_header(self.title_label, self.btn_back, win_w, win_h)
        bottom_limit = int(round(BOTTOM_SAFE_MARGIN))
        side_margin = int(round(dp(15)))

        scroll_w = int(round(win_w - side_margin * 2))
        scroll_h = int(round(max(content_top - bottom_limit, dp(10))))

        self.doc_scroll.pos = (side_margin, bottom_limit)
        self.doc_scroll.size = (scroll_w, scroll_h)
        self.content_box.width = scroll_w
        self.text_label.text_size = (scroll_w, None)

class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        self.btn_back.font_name = font_path("ClearSans-Bold.ttf")
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        self.layout.add_widget(self.btn_back)

        self.title_label = Label(
            text="ВЫБЕРИТЕ РЕЖИМ ИГРЫ",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.layout.add_widget(self.title_label)

        self.category_label = Label(
            text="Оффлайн",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.layout.add_widget(self.category_label)

        self.mode_container = BoxLayout(
            orientation='vertical',
            size_hint=(None, None)
        )

        self.offline_modes = [
            {
                "title": "Одиночная игра",
                "description": "Одиночная оффлайн игра с монетами, достижениями и квестами.",
                "description_color": color_correct,
                "target_screen": "one_player_game",
            },
            {
                "title": "Игра вдвоём",
                "description": "Игра вдвоём за одним устройством без монет, квестов и достижений.",
                "description_color": color_correct,
                "target_screen": "two_player_game",
            },
            {
                "title": "Генерация сида",
                "description": "Введите сид или создайте сид, чтобы друг смог поиграть на другом устройстве.",
                "description_color": color_correct,
                "target_screen": "seed_generation",
            },
        ]

        self.mode_buttons = []
        for mode in self.offline_modes:
            card = ModeButton(
                title_text=mode["title"],
                description_text=mode["description"],
                description_color=mode["description_color"],
                on_release=self._make_mode_opener(mode["target_screen"])
            )
            self.mode_buttons.append(card)
            self.mode_container.add_widget(card)

        self.layout.add_widget(self.mode_container)
        self.footer_label = Label(
            text="Больше режимов нет.",
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_not_in_word,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.layout.add_widget(self.footer_label)

        self.add_widget(self.layout)

        self.bind(size=self.reposition_elements)
        self.reposition_elements()
        Clock.schedule_once(lambda dt: self.reposition_elements(), 0)

    def _make_mode_opener(self, target_screen):
        def _open(*args):
            setattr(self.manager, 'current', target_screen)
        return _open

    def reposition_elements(self, *args):
        win_w, win_h = self.width, self.height

        back_w, back_h = dp(92), dp(48)
        self.btn_back.size = (back_w, back_h)
        self.btn_back.pos = (win_w - back_w - dp(14), win_h - TOP_SAFE_MARGIN - back_h)
        fit_font_size(self.btn_back, back_w - dp(18), back_h * 0.42)

        header_line_h = min(win_h * 0.035, dp(26))
        title_gap_below_button = dp(32)

        self.title_label.size = (win_w * 0.9, header_line_h)
        self.title_label.center_x = win_w / 2
        self.title_label.y = win_h - TOP_SAFE_MARGIN - back_h - title_gap_below_button - header_line_h
        fit_font_size(self.title_label, win_w * 0.9, header_line_h * 0.72)
        self.title_label.text_size = (win_w * 0.9, header_line_h)

        category_gap = dp(10)
        self.category_label.size = (win_w * 0.9, header_line_h)
        self.category_label.center_x = win_w / 2
        self.category_label.y = self.title_label.y - category_gap - header_line_h
        fit_font_size(self.category_label, win_w * 0.9, header_line_h * 0.72)
        self.category_label.text_size = (win_w * 0.9, header_line_h)

        content_top = self.category_label.y - dp(12)
        bottom_limit = BOTTOM_SAFE_MARGIN
        desc_font_start = min(win_h * 0.02, dp(40))
        TITLE_TO_DESC_RATIO = 2
        desc_h_cap = min(win_h * 0.16, dp(120))
        footer_gap = dp(14)
        footer_h_reserved = desc_font_start
        count = len(self.mode_buttons)
        card_w = win_w * 0.93
        card_pad_h = dp(13)
        card_pad_top, card_pad_bottom = dp(15), dp(14)
        card_inner_gap = dp(11)
        cards_spacing = dp(8)
        desc_max_w = card_w - card_pad_h * 2
        title_max_w = card_w - card_pad_h * 2

        def layout_cards(font_scale):
            total_h = 0.0
            for card in self.mode_buttons:
                fit_font_size_wrapped(card.sub_label, desc_max_w, desc_h_cap, desc_font_start * font_scale)
                desc_real_h = card.sub_label.texture_size[1]
                card.sub_label.height = desc_real_h
                card.sub_label.text_size = (desc_max_w, desc_real_h)
                title_target_font = card.sub_label.font_size * TITLE_TO_DESC_RATIO
                fit_font_size(card.title_label, title_max_w, title_target_font)
                title_real_h = card.title_label.texture_size[1]
                card.title_label.height = title_real_h
                card.title_label.text_size = (title_max_w, title_real_h)
                this_card_h = card_pad_top + title_real_h + card_inner_gap + desc_real_h + card_pad_bottom
                card.padding = [card_pad_h, card_pad_top, card_pad_h, card_pad_bottom]
                card.spacing = card_inner_gap
                card.size = (card_w, this_card_h)
                total_h += this_card_h

            total_h += cards_spacing * max(count - 1, 0)
            return total_h

        total_cards_h = layout_cards(1.0)

        available_for_cards = content_top - bottom_limit - footer_h_reserved - footer_gap
        if count > 0 and total_cards_h > 0 and total_cards_h > available_for_cards:
            scale = max(available_for_cards / total_cards_h, 0.55)
            total_cards_h = layout_cards(scale)

        self.mode_container.size = (card_w, max(total_cards_h, 0))
        self.mode_container.spacing = cards_spacing
        self.mode_container.center_x = win_w / 2
        self.mode_container.top = content_top

        desc_final_font_px = self.mode_buttons[0].sub_label.font_size if self.mode_buttons else desc_font_start
        self.footer_label.text_size = (None, None)
        fit_font_size(self.footer_label, win_w * 0.85, desc_final_font_px)
        self.footer_label.size = self.footer_label.texture_size
        self.footer_label.center_x = win_w / 2
        self.footer_label.top = self.mode_container.y - footer_gap

class OnePlayerGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.cells = []
        for _ in range(30):
            cell = GameCell(size=(74, 92))
            cell.base_color = color_blank
            self.cells.append(cell)
            self.layout.add_widget(cell)

        self.pending_match_coins = 0

        self.keyboard_keys = []

        self.btn_erase = IconKeyButton(image_source="backspace.png", size=(100, 50))
        self.btn_erase.bind(on_release=self.press_erase_key)

        self.btn_enter = IconKeyButton(image_source="corner-down-left.png", size=(100, 50))
        self.btn_enter.bind(on_release=self.press_enter_key)

        self.system_buttons = [self.btn_erase, self.btn_enter]
        
        self.layout.add_widget(self.btn_erase)
        self.layout.add_widget(self.btn_enter)

        self.btn_exit_top = MenuButton(text="Назад", size_hint=(None, None), size=(dp(92), dp(48)))
        self.btn_exit_top.bind(on_release=self.press_exit_key)
        self.layout.add_widget(self.btn_exit_top)

        self.lines = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮЁ"]
        self.letter_buttons = []
        for line in self.lines:
            row_buttons = []
            for char in line:
                key = KeyButton(text=char, size=(40, 85))
                key.font_size = '22sp'

                key.bind(on_release=self.press_letter_key)

                self.keyboard_keys.append(key)
                self.layout.add_widget(key)
                row_buttons.append(key)
            self.letter_buttons.append(row_buttons)
                
        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)
        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

        self.current_word = ""
        self.current_attempt = 0
        self.secret_word = ""

        self.reset_game()

    def reposition_elements(self, instance, size):
        win_w = self.width
        win_h = self.height
        self.bg_rect.size = (win_w, win_h)
        self.bg_rect.pos = (0, 0)

        GRID_GAP = dp(6)
        top_reserved = TOP_SAFE_MARGIN + dp(48) + GRID_GAP
        bottom_reserved = BOTTOM_SAFE_MARGIN

        self.btn_exit_top.size = (dp(92), dp(48))
        self.btn_exit_top.pos = (win_w - dp(92) - dp(14), win_h - TOP_SAFE_MARGIN - dp(48))
        fit_font_size(self.btn_exit_top, self.btn_exit_top.width - dp(18), self.btn_exit_top.height * 0.42)

        # ----- КЛАВИАТУРА: фиксированная высота (доля от высоты экрана), не зависит от
        # того, сколько места осталось под сеткой — высота клавиатуры всегда одинаковая. -----
        KEY_SPACING_X = 4
        KEY_SPACING_Y = 4
        KEY_HEIGHT_FRACTION = 0.0786
        avail_w = win_w - 16 - 44
        KEY_WIDTH = avail_w / 12
        KEY_HEIGHT = win_h * KEY_HEIGHT_FRACTION
        keyboard_total_height = (3 * KEY_HEIGHT) + (2 * KEY_SPACING_Y)
        keyboard_top_y = bottom_reserved + keyboard_total_height

        for key in self.keyboard_keys:
            key.size = (KEY_WIDTH, KEY_HEIGHT)

        row_heights = [
            bottom_reserved,
            bottom_reserved + (KEY_HEIGHT + KEY_SPACING_Y),
            bottom_reserved + 2 * (KEY_HEIGHT + KEY_SPACING_Y)
        ]

        self.btn_enter.size = (KEY_WIDTH, KEY_HEIGHT)
        self.btn_erase.size = (KEY_WIDTH, KEY_HEIGHT)

        line_to_height_idx = {0: 2, 1: 1, 2: 0}
        for i, line_keys in enumerate(self.letter_buttons):
            h_idx = line_to_height_idx[i]
            extra_slots = 2 if i == 2 else 0
            total_w = (len(line_keys) + extra_slots) * KEY_WIDTH + (len(line_keys) + extra_slots - 1) * KEY_SPACING_X
            start_l_x = (win_w - total_w) / 2

            if i == 2:
                self.btn_enter.pos = (start_l_x, row_heights[h_idx])
                self.btn_enter.update_canvas()
                start_l_x += KEY_WIDTH + KEY_SPACING_X

            for idx, key in enumerate(line_keys):
                key.pos = (start_l_x + idx * (KEY_WIDTH + KEY_SPACING_X), row_heights[h_idx])
                key.update_canvas()

            if i == 2:
                erase_x = start_l_x + len(line_keys) * (KEY_WIDTH + KEY_SPACING_X)
                self.btn_erase.pos = (erase_x, row_heights[h_idx])
                self.btn_erase.update_canvas()

        # ----- СЕТКА 5×6: ширина клеток — от ширины экрана (как раньше). Высота
        # ограничена так, чтобы сетка не наезжала на клавиатуру, и ЦЕНТРИРУЕТСЯ по
        # вертикали в промежутке между кнопкой "Назад" и клавиатурой — сверху и снизу
        # от сетки остаётся поровну свободного места. -----
        CELL_SPACING_X = 5
        CELL_SPACING_Y = 5

        side_margin = win_w * 0.11

        avail_cell_w = win_w - (2 * side_margin) - 20
        CELL_WIDTH = avail_cell_w / 5  
        CELL_HEIGHT = CELL_WIDTH  

        total_blanks_height = (6 * CELL_HEIGHT) + (5 * CELL_SPACING_Y)

        top_boundary = win_h - top_reserved
        avail_for_grid_space = top_boundary - keyboard_top_y - GRID_GAP
        max_allowed_height = avail_for_grid_space * 0.68

        if total_blanks_height > max_allowed_height:

            total_blanks_height = max_allowed_height
            CELL_HEIGHT = (total_blanks_height - (5 * CELL_SPACING_Y)) / 6
            CELL_WIDTH = CELL_HEIGHT
            side_margin = (win_w - (5 * CELL_WIDTH) - 20) / 2

        for cell in self.cells:
            cell.size = (CELL_WIDTH, CELL_HEIGHT)

        free_space_y = avail_for_grid_space - total_blanks_height
        block_bottom_y = keyboard_top_y + GRID_GAP + (free_space_y / 2)

        start_blank_x = side_margin
        start_blank_y = block_bottom_y + total_blanks_height - CELL_HEIGHT

        cell_idx = 0
        for row in range(6):
            for col in range(5):
                if cell_idx < len(self.cells):
                    self.cells[cell_idx].pos = (start_blank_x + col * (CELL_WIDTH + CELL_SPACING_X), start_blank_y - row * (CELL_HEIGHT + CELL_SPACING_Y))
                    self.cells[cell_idx].update_canvas()
                    cell_idx += 1

        apply_adaptive_fonts(self, CELL_HEIGHT, KEY_HEIGHT)

    def press_letter_key(self, instance):
        letter = instance.text

        if len(self.current_word) < 5:
            cell_idx = (self.current_attempt * 5) + len(self.current_word)

            if cell_idx < len(self.cells):
                self.cells[cell_idx].text = letter

                self.current_word += letter

    def press_erase_key(self, instance):
        if len(self.current_word) > 0:
            cell_idx = (self.current_attempt * 5) + len(self.current_word) - 1

            if cell_idx < len(self.cells):

                self.cells[cell_idx].text = ""

                self.current_word = self.current_word[:-1]

    def press_enter_key(self, instance):

        global MOBILE_PLAYER_STATS, MOBILE_QUESTS

        if len(self.current_word) == 5:
            check_word = self.current_word.upper()

            if 'MOBILE_ALL_WORDS' in globals() and MOBILE_ALL_WORDS and check_word in MOBILE_ALL_WORDS:
                print(f"[MGGamesStudio] Слово найдено в словаре: {check_word}")
                self.evaluate_word_colors_mobile(check_word)
            else:
                self.check_and_advance_mobile_quest("q4", amount=1)

                if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
                    MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)

                self.show_game_popup("Такого слова нет в словаре", "Введите другое слово.", color_text, is_end_game=False)
        else:
            self.show_game_popup("Слово не из 5 букв", "Заполните все 5 ячеек перед вводом.", color_text, is_end_game=False)

    def evaluate_word_colors_mobile(self, check_word):
        global MOBILE_PLAYER_STATS, MOBILE_QUESTS

        row_statuses = ["not_in_word"] * 5
        sec_chars = list(self.secret_word)
        g_chars = list(check_word)

        greens = 0
        for i in range(5):
            if g_chars[i] == sec_chars[i]:
                row_statuses[i] = "correct"
                sec_chars[i] = None
                g_chars[i] = " "
                greens += 1

        yellows = 0
        for i in range(5):
            if g_chars[i] != " " and g_chars[i] in sec_chars:
                row_statuses[i] = "in_word"
                idx = sec_chars.index(g_chars[i])
                sec_chars[idx] = None
                yellows += 1

        start_idx = self.current_attempt * 5
        for i in range(5):
            cell_idx = start_idx + i
            if cell_idx < len(self.cells):
                self.cells[cell_idx].change_type(row_statuses[i])

        for i in range(5):
            char = self.current_word[i].upper()
            status = row_statuses[i]
            for btn in self.keyboard_keys:
                if btn.text == char:
                    if btn.cell_status == "correct": continue
                    if btn.cell_status == "in_word" and status != "correct": continue
                    
                    if status == "correct":
                        btn.base_color = color_correct
                        btn.color = (1.0, 1.0, 1.0, 1.0)
                    elif status == "in_word":
                        btn.base_color = color_in_word
                        btn.color = (0.0, 0.0, 0.0, 1.0)
                    elif status == "not_in_word":
                        btn.base_color = color_not_in_word
                        btn.color = (1.0, 1.0, 1.0, 1.0)
                    btn.cell_status = status
                    btn.update_canvas()

        coins = sum(5 if s == "correct" else (2 if s == "in_word" else 1) for s in row_statuses)

        if check_word == self.secret_word: coins += 10
        self.pending_match_coins += coins
        if greens >= 3: self.check_and_advance_mobile_quest("q2", 1)
        if greens < 5 and (greens + yellows) >= 3: self.check_and_advance_mobile_quest("q3", 1)

        self.process_end_game_logic_mobile(check_word, yellows)

    def check_mobile_achievements(self, last_win_attempt=None):

        global MOBILE_PLAYER_STATS
        import time
        
        stats = MOBILE_PLAYER_STATS
        ach_base = stats.get("achivements_dict", {})
        if not ach_base:
            return

        def give_mobile_reward(ach_id):
            if ach_id in ach_base and not ach_base[ach_id].get("got", False):
                ach_base[ach_id]["got"] = True
                ach_base[ach_id]["date"] = time.strftime("%d.%m.%Y")
                
                rewards = {"common": 30, "rare": 50, "epic": 500}
                reward = rewards.get(ach_base[ach_id].get("type", "common"), 0)
                    
                stats["player_coins"] = stats.get("player_coins", 0) + reward
                print(f"[MGGamesStudio] Достижение: {ach_base[ach_id]['name']}. +{reward} монет!")

        t_wins, t_losses = stats.get("total_wins", 0), stats.get("total_losses", 0)
        win_cond = {5: "ach_1", 10: "ach_2", 15: "ach_3", 20: "ach_4", 25: "ach_5"}
        loss_cond = {5: "ach_6", 10: "ach_7", 15: "ach_8", 20: "ach_9", 25: "ach_10"}
        
        if t_wins in win_cond: give_mobile_reward(win_cond[t_wins])
        if t_losses in loss_cond: give_mobile_reward(loss_cond[t_losses])

        if last_win_attempt is not None:
            attempt_cond = {i: f"ach_{i+10}" for i in range(1, 7)}
            if last_win_attempt in attempt_cond:
                give_mobile_reward(attempt_cond[last_win_attempt])

        stats["unlocked_achivements"] = {k: {"got": v["got"], "date": v["date"]} for k, v in ach_base.items()}

    def check_and_advance_mobile_quest(self, quest_id, amount=1):
        global MOBILE_PLAYER_STATS, MOBILE_QUESTS
        
        if quest_id in MOBILE_QUESTS:
            q = MOBILE_QUESTS[quest_id]
            if q.get("done", False):
                return
                
            q["progress"] = q.get("progress", 0) + amount
            goal = q.get("goal", 1)
            
            if q["progress"] >= goal:
                q["progress"] = goal
                q["done"] = True

                reward = q.get("reward", 50)
                MOBILE_PLAYER_STATS["player_coins"] = MOBILE_PLAYER_STATS.get("player_coins", 0) + reward
                MOBILE_PLAYER_STATS["total_completed_quests"] = MOBILE_PLAYER_STATS.get("total_completed_quests", 0) + 1
                print(f"[MGGamesStudio] Квест выполнен: {q['name']}. +{reward} монет!")

            if "active_quests" in MOBILE_PLAYER_STATS:
                if quest_id in MOBILE_PLAYER_STATS["active_quests"]:
                    MOBILE_PLAYER_STATS["active_quests"][quest_id]["progress"] = q["progress"]
                    MOBILE_PLAYER_STATS["active_quests"][quest_id]["done"] = q["done"]

    def handle_mobile_win(self):
        global MOBILE_PLAYER_STATS, MOBILE_QUESTS
        stats = MOBILE_PLAYER_STATS

        remaining_start = (self.current_attempt + 1) * 5
        remaining_cells_count = len(self.cells[remaining_start:])
        self.pending_match_coins += remaining_cells_count * 5

        stats["player_coins"] = stats.get("player_coins", 0) + self.pending_match_coins
        self.pending_match_coins = 0

        stats["total_wins"] = stats.get("total_wins", 0) + 1
        stats["current_win_streak"] = stats.get("current_win_streak", 0) + 1

        if stats["current_win_streak"] > stats.get("max_win_streak", 0):
            stats["max_win_streak"] = stats["current_win_streak"]

        self.check_mobile_achievements(last_win_attempt=self.current_attempt + 1)

        self.check_and_advance_mobile_quest("q1", 1)
        self.check_and_advance_mobile_quest("q5", 1)
        self.check_and_advance_mobile_quest("q11", 1)

        if self.current_attempt in (4, 5):
            self.check_and_advance_mobile_quest("q6", 1)
        if self.current_attempt <= 3:
            self.check_and_advance_mobile_quest("q7", 1)
        if self.current_attempt in (1, 2):
            self.check_and_advance_mobile_quest("q9", 1)

        if not getattr(self, "used_delete_key", False):
            self.check_and_advance_mobile_quest("q12", 1)

        if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
            MOBILE_SAVE_FUNC(stats)

        self.show_game_popup("ПОБЕДА!", f"Было загадано слово: {self.secret_word}", color_correct, is_end_game=True)

    def handle_mobile_loss(self):
        global MOBILE_PLAYER_STATS, MOBILE_QUESTS
        stats = MOBILE_PLAYER_STATS

        stats["player_coins"] = stats.get("player_coins", 0) + self.pending_match_coins
        self.pending_match_coins = 0

        stats["total_losses"] = stats.get("total_losses", 0) + 1
        stats["current_win_streak"] = 0

        if "active_quests" in stats and "q5" in stats["active_quests"]:
            stats["active_quests"]["q5"]["progress"] = 0
            if "q5" in MOBILE_QUESTS:
                MOBILE_QUESTS["q5"]["progress"] = 0
                
        self.check_mobile_achievements(last_win_attempt=None)
        self.check_and_advance_mobile_quest("q1", 1)
        
        if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
            MOBILE_SAVE_FUNC(stats)
            
        self.show_game_popup("ИГРА ОКОНЧЕНА", f"Загаданное слово было: {self.secret_word}", color_not_in_word, is_end_game=True)

    def process_end_game_logic_mobile(self, check_word, current_match_yellows):
        global MOBILE_PLAYER_STATS, MOBILE_QUESTS
        
        grey_keys = sum(1 for btn in self.keyboard_keys if btn.cell_status == "not_in_word")
        if grey_keys >= 10:
            self.check_and_advance_mobile_quest("q8", 1)
            
        if check_word == self.secret_word:
            self.handle_mobile_win()
            return
            
        self.current_attempt += 1
        self.current_word = ""
        
        if self.current_attempt >= 6:
            self.handle_mobile_loss()

    def press_exit_key(self, instance):
        self.reset_game()
        self.manager.current = 'play'

    def reset_game(self):
        for cell in self.cells:
            cell.text = ""
            cell.base_color = color_blank
            cell.color = color_text
            cell.update_canvas()

        for key_btn in self.keyboard_keys:
            key_btn.base_color = color_key
            key_btn.color = color_text
            key_btn.cell_status = "blank"
            key_btn.update_canvas()

        for btn in self.system_buttons:
            btn.base_color = color_key
            btn.color = color_text
            btn.update_canvas()
            
        self.current_word = ""
        self.current_attempt = 0
        self.pending_match_coins = 0

        if 'MOBILE_ALL_WORDS' in globals() and MOBILE_ALL_WORDS:
            self.secret_word = random.choice(MOBILE_ALL_WORDS).upper()
            print(f"[MGGamesStudio] Загадано новое секретное слово: {self.secret_word}")
        else:
            self.secret_word = "СЛОВО"

    def show_game_popup(self, title_text, msg_text, title_color, is_end_game=False):
        win_w = Window.width
        win_h = Window.height
        safe_screen_side = min(win_w, win_h)
        popup_height = win_h * 0.30

        from kivy.graphics.texture import Texture
        transparent_texture = Texture.create(size=(1, 1), colorfmt='rgba')
        transparent_texture.blit_buffer(b'\x00\x00\x00\x00', colorfmt='rgba', bufferfmt='ubyte')

        view = ModalView(size_hint=(0.8, None), height=popup_height, auto_dismiss=True)
        view.background_image = transparent_texture
        view.overlay_color = (0, 0, 0, 0.5)

        box = FloatLayout()
        with box.canvas.before:
            Color(*color_bg)
            self.popup_rect = RoundedRectangle(pos=view.pos, size=view.size, radius=[12])
            
        def update_popup_bg(inst, value):
            self.popup_rect.pos = view.pos
            self.popup_rect.size = view.size
        view.bind(pos=update_popup_bg, size=update_popup_bg)

        title_font_size = safe_screen_side * 0.06
        msg_font_size = safe_screen_side * 0.04
        tip_font_size = safe_screen_side * 0.03

        lbl_title = Label(text=title_text, font_name=font_path("ClearSans-Bold.ttf"),
                          font_size=f"{title_font_size}px", color=title_color, bold=True,
                          size_hint=(1, None), height=popup_height * 0.25, 
                          pos_hint={'center_x': 0.5, 'top': 0.9})

        lbl_msg = Label(text=msg_text, font_name=font_path("ClearSans-Bold.ttf"),
                        font_size=f"{msg_font_size}px", color=color_text, bold=True,
                        size_hint=(1, None), height=popup_height * 0.25, 
                        pos_hint={'center_x': 0.5, 'center_y': 0.45})

        tip_text = "Кликните в любое место для выхода в меню" if is_end_game else "Кликните в любое место, чтобы скрыть"
        lbl_tip = Label(text=tip_text, font_name=font_path("ClearSans-Bold.ttf"),
                        font_size=f"{tip_font_size}px", color=(100/255, 116/255, 139/255, 1.0), bold=True,
                        size_hint=(1, None), height=popup_height * 0.15, 
                        pos_hint={'center_x': 0.5, 'y': 0.08})

        box.add_widget(lbl_title)
        box.add_widget(lbl_msg)
        box.add_widget(lbl_tip)
        view.add_widget(box)
        
        def self_dismiss(instance, touch):
            instance.dismiss()
            return True
            
        view.bind(on_touch_down=self_dismiss)
        
        if is_end_game:
            view.bind(on_dismiss=lambda x: self.press_exit_key(None))
            
        view.open()

class TwoPlayerGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.lbl_title = Label(text="ЗАГАДАЙТЕ СЛОВО", font_name=font_path("ClearSans-Bold.ttf"),
                               font_size='32sp', color=color_text, bold=True, size_hint=(None, None))
        self.lbl_subtitle = Label(text="Второй игрок должен отвернуться от экрана!", font_name=font_path("ClearSans-Bold.ttf"),
                                  font_size='14sp', color=color_not_in_word, bold=True, size_hint=(None, None))
        self.lbl_error = Label(text="", font_name=font_path("ClearSans-Bold.ttf"),
                               font_size='15sp', color=color_in_word, bold=True, size_hint=(None, None))
        self.layout.add_widget(self.lbl_error)
        self.layout.add_widget(self.lbl_title)
        self.layout.add_widget(self.lbl_subtitle)

        self.cells = []
        for _ in range(30):
            cell = GameCell(size=(74, 92))
            cell.base_color = color_blank
            self.cells.append(cell)
            self.layout.add_widget(cell)

        self.keyboard_keys = []

        self.btn_erase = IconKeyButton(image_source="backspace.png", size=(100, 50))
        self.btn_erase.bind(on_release=self.press_erase_key)

        self.btn_enter = IconKeyButton(image_source="corner-down-left.png", size=(100, 50))
        self.btn_enter.bind(on_release=self.press_enter_key)

        self.system_buttons = [self.btn_erase, self.btn_enter]
        
        self.layout.add_widget(self.btn_erase)
        self.layout.add_widget(self.btn_enter)

        self.btn_exit_top = MenuButton(text="Назад", size_hint=(None, None), size=(dp(92), dp(48)))
        self.btn_exit_top.bind(on_release=self.press_exit_key)
        self.layout.add_widget(self.btn_exit_top)

        self.lines = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮЁ"]
        self.letter_buttons = []
        for line in self.lines:
            row_buttons = []
            for char in line:
                key = KeyButton(text=char, size=(40, 85))
                key.font_size = '22sp'

                key.bind(on_release=self.press_letter_key)
                
                self.keyboard_keys.append(key)
                self.layout.add_widget(key)
                row_buttons.append(key)
            self.letter_buttons.append(row_buttons)
                
        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        self.current_word = ""
        self.current_attempt = 0
        self.secret_word = ""
        self.stage = "setup"

        self.reset_game()
        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def reposition_elements(self, instance, size):
        win_w = self.width
        win_h = self.height
        self.bg_rect.size = (win_w, win_h)
        self.bg_rect.pos = (0, 0)

        GRID_GAP = dp(6)
        top_reserved = TOP_SAFE_MARGIN + dp(48) + GRID_GAP
        bottom_reserved = BOTTOM_SAFE_MARGIN

        self.btn_exit_top.size = (dp(92), dp(48))
        self.btn_exit_top.pos = (win_w - dp(92) - dp(14), win_h - TOP_SAFE_MARGIN - dp(48))
        fit_font_size(self.btn_exit_top, self.btn_exit_top.width - dp(18), self.btn_exit_top.height * 0.42)

        # ----- КЛАВИАТУРА: фиксированная высота (доля от высоты экрана), как и на
        # остальных экранах игры — не зависит от того, сколько места осталось под сеткой. -----
        KEY_SPACING_X = 4
        KEY_SPACING_Y = 4
        KEY_HEIGHT_FRACTION = 0.0786
        avail_w = win_w - 16 - 44
        KEY_WIDTH = avail_w / 12
        KEY_HEIGHT = win_h * KEY_HEIGHT_FRACTION
        keyboard_total_height = (3 * KEY_HEIGHT) + (2 * KEY_SPACING_Y)
        keyboard_top_y = bottom_reserved + keyboard_total_height

        row_heights = [
            bottom_reserved,
            bottom_reserved + (KEY_HEIGHT + KEY_SPACING_Y),
            bottom_reserved + 2 * (KEY_HEIGHT + KEY_SPACING_Y)
        ]

        CELL_SPACING_X = 5
        CELL_SPACING_Y = 5
        side_margin = win_w * 0.11
        avail_cell_w = win_w - (2 * side_margin) - 20
        CELL_WIDTH = avail_cell_w / 5  
        CELL_HEIGHT = CELL_WIDTH  

        total_blanks_height = (6 * CELL_HEIGHT) + (5 * CELL_SPACING_Y)

        top_boundary = win_h - top_reserved
        avail_for_grid_space = top_boundary - keyboard_top_y - GRID_GAP
        max_allowed_height = avail_for_grid_space * 0.68

        if total_blanks_height > max_allowed_height:
            total_blanks_height = max_allowed_height
            CELL_HEIGHT = (total_blanks_height - (5 * CELL_SPACING_Y)) / 6
            CELL_WIDTH = CELL_HEIGHT
            side_margin = (win_w - (5 * CELL_WIDTH) - 20) / 2

        for cell in self.cells:
            cell.size = (CELL_WIDTH, CELL_HEIGHT)

        start_blank_x = side_margin
        
        if self.stage == "setup":
            kbd_top_y = keyboard_top_y

            total_free_space_y = top_boundary - kbd_top_y
            start_blank_y = kbd_top_y + (total_free_space_y - CELL_HEIGHT) // 2

            space_above_cells = top_boundary - (start_blank_y + CELL_HEIGHT)
            center_above_y = (start_blank_y + CELL_HEIGHT) + (space_above_cells // 2)

            fit_font_size(self.lbl_title, win_w * 0.9, dp(24))
            self.lbl_title.text_size = (None, None)
            self.lbl_title.size = self.lbl_title.texture_size

            fit_font_size(self.lbl_subtitle, win_w * 0.85, dp(14))
            self.lbl_subtitle.text_size = (None, None)
            self.lbl_subtitle.size = self.lbl_subtitle.texture_size

            block_gap = dp(4)
            block_h = self.lbl_title.height + block_gap + self.lbl_subtitle.height

            block_center = min(center_above_y, top_boundary - block_h / 2 - dp(6))
            block_center = max(block_center, kbd_top_y + block_h / 2 + dp(6))

            block_top_y = block_center + block_h / 2
            self.lbl_title.pos = (win_w / 2 - self.lbl_title.width / 2, block_top_y - self.lbl_title.height)
            self.lbl_subtitle.pos = (win_w / 2 - self.lbl_subtitle.width / 2, block_top_y - self.lbl_title.height - block_gap - self.lbl_subtitle.height)

            space_below_cells = start_blank_y - kbd_top_y
            center_below_y = kbd_top_y + (space_below_cells // 2)

            fit_font_size(self.lbl_error, win_w * 0.85, dp(16))
            self.lbl_error.text_size = (None, None)
            self.lbl_error.size = self.lbl_error.texture_size
            self.lbl_error.pos = (win_w // 2 - self.lbl_error.width // 2, center_below_y - self.lbl_error.height // 2)
        else:
            # ----- СЕТКА 5×6 центрируется по вертикали между кнопкой "Назад" и
            # клавиатурой — сверху и снизу от сетки остаётся поровну свободного места. -----
            free_space_y = avail_for_grid_space - total_blanks_height
            block_bottom_y = keyboard_top_y + GRID_GAP + (free_space_y / 2)
            start_blank_y = block_bottom_y + total_blanks_height - CELL_HEIGHT

        cell_idx = 0
        for row in range(6):
            for col in range(5):
                if cell_idx < len(self.cells):
                    if self.stage == "setup" and row > 0:
                        self.cells[cell_idx].pos = (-1000, -1000)
                    else:
                        self.cells[cell_idx].pos = (start_blank_x + col * (CELL_WIDTH + CELL_SPACING_X), start_blank_y - row * (CELL_HEIGHT + CELL_SPACING_Y))
                    self.cells[cell_idx].update_canvas()
                    cell_idx += 1

        for key in self.keyboard_keys:
            key.size = (KEY_WIDTH, KEY_HEIGHT)

        for btn in self.system_buttons:
            btn.size = (KEY_WIDTH, KEY_HEIGHT)

        line_to_height_idx = {0: 2, 1: 1, 2: 0}
        for i, line_keys in enumerate(self.letter_buttons):
            h_idx = line_to_height_idx[i]
            extra_slots = 2 if i == 2 else 0
            total_w = (len(line_keys) + extra_slots) * KEY_WIDTH + (len(line_keys) + extra_slots - 1) * KEY_SPACING_X
            start_l_x = (win_w - total_w) / 2

            if i == 2:
                self.btn_enter.pos = (start_l_x, row_heights[h_idx])
                self.btn_enter.update_canvas()
                start_l_x += KEY_WIDTH + KEY_SPACING_X

            for idx, key in enumerate(line_keys):
                key.pos = (start_l_x + idx * (KEY_WIDTH + KEY_SPACING_X), row_heights[h_idx])
                key.update_canvas()

            if i == 2:
                erase_x = start_l_x + len(line_keys) * (KEY_WIDTH + KEY_SPACING_X)
                self.btn_erase.pos = (erase_x, row_heights[h_idx])
                self.btn_erase.update_canvas()

        apply_adaptive_fonts(self, CELL_HEIGHT, KEY_HEIGHT)

    def press_letter_key(self, instance):
        self.lbl_error.text = ""
        letter = instance.text

        if len(self.current_word) < 5:
            cell_idx = (self.current_attempt * 5) + len(self.current_word)

            if cell_idx < len(self.cells):
                self.cells[cell_idx].text = letter

                self.current_word += letter

    def press_erase_key(self, instance):
        self.lbl_error.text = ""
        if len(self.current_word) > 0:
            cell_idx = (self.current_attempt * 5) + len(self.current_word) - 1

            if cell_idx < len(self.cells):
                self.cells[cell_idx].text = ""
                self.current_word = self.current_word[:-1]

    def press_enter_key(self, instance):
        if len(self.current_word) != 5:
            if self.stage == "setup":
                self.lbl_error.color = color_in_word
                self.lbl_error.text = "Слово не из 5 букв!"
                self.reposition_elements(None, None)
            else:
                self.show_game_popup("Слово не из 5 букв", "Заполните все 5 ячеек перед вводом.", color_text, is_end_game=False)
            return

        check_word = self.current_word.upper()

        if 'MOBILE_ALL_WORDS' in globals() and MOBILE_ALL_WORDS and check_word in MOBILE_ALL_WORDS:

            if self.stage == "setup":
                self.secret_word = check_word
                self.stage = "playing"
                self.current_word = ""

                self.lbl_title.text = ""
                self.lbl_subtitle.text = ""
                self.lbl_error.text = ""

                for cell in self.cells:
                    cell.text = ""

                self.reposition_elements(None, None)
                return

            row_statuses = ["not_in_word"] * 5
            secret_chars = list(self.secret_word)
            guess_chars = list(check_word)

            for i in range(5):
                if guess_chars[i] == secret_chars[i]:
                    row_statuses[i] = "correct"
                    secret_chars[i] = None
                    guess_chars[i] = b" "

            for i in range(5):
                if guess_chars[i] != b" " and guess_chars[i] in secret_chars:
                    row_statuses[i] = "in_word"
                    idx = secret_chars.index(guess_chars[i])
                    secret_chars[idx] = None

            start_idx = self.current_attempt * 5
            for i in range(5):
                cell_idx = start_idx + i
                if cell_idx < len(self.cells):
                    self.cells[cell_idx].change_type(row_statuses[i])

            for i in range(5):
                char_in_guess = self.current_word[i].upper()
                status_for_char = row_statuses[i]
                for key_btn in self.keyboard_keys:
                    if key_btn.text == char_in_guess:
                        if key_btn.cell_status == "correct": continue
                        elif key_btn.cell_status == "in_word" and status_for_char != "correct": continue
                        if status_for_char == "correct":
                            key_btn.base_color = color_correct
                            key_btn.color = (1.0, 1.0, 1.0, 1.0)
                        elif status_for_char == "in_word":
                            key_btn.base_color = color_in_word
                            key_btn.color = (0.0, 0.0, 0.0, 1.0)
                        elif status_for_char == "not_in_word":
                            key_btn.base_color = color_not_in_word
                            key_btn.color = (1.0, 1.0, 1.0, 1.0)
                        key_btn.cell_status = status_for_char
                        key_btn.update_canvas()

            if check_word == self.secret_word:
                self.show_game_popup(
                    "ПОБЕДА!", 
                    f"Второй игрок угадал слово: {self.secret_word}",
                    color_correct,
                    is_end_game=True
                )
                return

            self.current_attempt += 1
            self.current_word = ""

            if self.current_attempt >= 6:
                self.show_game_popup(
                    "ИГРА ОКОНЧЕНА", 
                    f"Загаданное слово было: {self.secret_word}",
                    color_not_in_word,
                    is_end_game=True
                )
        else:
            if self.stage == "setup":
                self.lbl_error.color = color_in_word
                self.lbl_error.text = "Такого слова нет в словаре!"
                self.reposition_elements(None, None)
            else:
                self.show_game_popup("Такого слова нет в словаре", "Введите другое слово.", color_text, is_end_game=False)

    def press_exit_key(self, instance):
        self.reset_game()
        self.manager.current = 'play'

    def reset_game(self):
        self.stage = "setup"
        self.current_word = ""
        self.current_attempt = 0
        self.secret_word = ""
        self.lbl_title.text = "ЗАГАДАЙТЕ СЛОВО"
        self.lbl_subtitle.text = "Второй игрок должен отвернуться от экрана!"
        self.lbl_error.text = ""

        for cell in self.cells:
            cell.text = ""
            cell.base_color = color_blank
            cell.color = color_text
            cell.update_canvas()

        for key_btn in self.keyboard_keys:
            key_btn.base_color = color_key
            key_btn.color = color_text
            key_btn.cell_status = "blank"
            key_btn.update_canvas()

        for btn in self.system_buttons:
            btn.base_color = color_key
            btn.color = color_text
            btn.update_canvas()

        self.reposition_elements(None, None)

    def show_game_popup(self, title_text, msg_text, title_color, is_end_game=False):
        win_w = Window.width
        win_h = Window.height

        safe_screen_side = min(win_w, win_h)

        popup_height = win_h * 0.30

        from kivy.graphics.texture import Texture
        transparent_texture = Texture.create(size=(1, 1), colorfmt='rgba')
        transparent_texture.blit_buffer(b'\x00\x00\x00\x00', colorfmt='rgba', bufferfmt='ubyte')

        view = ModalView(size_hint=(0.8, None), height=popup_height, auto_dismiss=True)
        view.background_image = transparent_texture
        view.overlay_color = (0, 0, 0, 0.5)

        box = FloatLayout()
        with box.canvas.before:
            Color(*color_bg)
            self.popup_rect = RoundedRectangle(pos=view.pos, size=view.size, radius=[12])

        def update_popup_bg(inst, value):
            self.popup_rect.pos = view.pos
            self.popup_rect.size = view.size
        view.bind(pos=update_popup_bg, size=update_popup_bg)

        title_font_size = safe_screen_side * 0.06
        msg_font_size = safe_screen_side * 0.04
        tip_font_size = safe_screen_side * 0.03

        lbl_title = Label(text=title_text, font_name=font_path("ClearSans-Bold.ttf"),
                          font_size=f"{title_font_size}px", color=title_color, bold=True,
                          size_hint=(1, None), height=popup_height * 0.25, 
                          pos_hint={'center_x': 0.5, 'top': 0.9})

        lbl_msg = Label(text=msg_text, font_name=font_path("ClearSans-Bold.ttf"),
                        font_size=f"{msg_font_size}px", color=color_text, bold=True,
                        size_hint=(1, None), height=popup_height * 0.25, 
                        pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        tip_text = "Кликните в любое место для выхода в меню" if is_end_game else "Кликните в любое место, чтобы скрыть"
        lbl_tip = Label(text=tip_text, font_name=font_path("ClearSans-Bold.ttf"),
                        font_size=f"{tip_font_size}px", color=color_not_in_word, bold=True,
                        size_hint=(1, None), height=popup_height * 0.15, 
                        pos_hint={'center_x': 0.5, 'y': 0.08})
        
        box.add_widget(lbl_title)
        box.add_widget(lbl_msg)
        box.add_widget(lbl_tip)
        view.add_widget(box)
        
        def self_dismiss(instance, touch):
            instance.dismiss()
            return True
            
        view.bind(on_touch_down=self_dismiss)
        
        if is_end_game:
            view.bind(on_dismiss=lambda x: self.press_exit_key(None))
            
        view.open()

class SeedGenerationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(dp(92), dp(48)))
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'play'))
        self.layout.add_widget(self.btn_back)

        self.title_label = Label(
            text="ГЕНЕРАЦИЯ СИДА",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.layout.add_widget(self.title_label)

        self.lbl_stub = Label(
            text="Создайте сид из своего слова и отправьте его другу,\nили введите сид, который вам прислали, чтобы отгадать слово.",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_not_in_word,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.layout.add_widget(self.lbl_stub)

        self.buttons_container = BoxLayout(
            orientation='vertical',
            size_hint=(None, None)
        )

        self.btn_create_seed = MenuButton(text="Создать сид")
        self.btn_create_seed.font_name = font_path("ClearSans-Bold.ttf")
        self.btn_create_seed.base_color = color_correct
        self.btn_create_seed.color = (1.0, 1.0, 1.0, 1.0)
        self.btn_create_seed.bind(on_release=lambda x: setattr(self.manager, 'current', 'seed_create'))

        self.btn_enter_seed = MenuButton(text="Ввести сид")
        self.btn_enter_seed.font_name = font_path("ClearSans-Bold.ttf")
        self.btn_enter_seed.bind(on_release=lambda x: setattr(self.manager, 'current', 'seed_enter'))

        self.mode_buttons = [self.btn_create_seed, self.btn_enter_seed]
        for btn in self.mode_buttons:
            btn.size_hint = (1, None)
            self.buttons_container.add_widget(btn)

        self.layout.add_widget(self.buttons_container)

        self.add_widget(self.layout)

        self.bind(size=self.reposition_elements)
        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def reposition_elements(self, instance, size):
        win_w, win_h = self.width, self.height
        self.bg_rect.size = (win_w, win_h)
        self.bg_rect.pos = (0, 0)

        back_w, back_h = dp(92), dp(48)
        self.btn_back.size = (back_w, back_h)
        self.btn_back.pos = (win_w - back_w - dp(14), win_h - TOP_SAFE_MARGIN - back_h)
        fit_font_size(self.btn_back, back_w - dp(18), back_h * 0.42)

        fit_font_size(self.title_label, win_w * 0.85, dp(26))
        self.title_label.text_size = (None, None)
        self.title_label.size = self.title_label.texture_size
        self.title_label.center_x = win_w / 2
        self.title_label.top = win_h - TOP_SAFE_MARGIN - back_h - dp(24)

        container_w = win_w * 0.86
        total_buttons = len(self.mode_buttons)
        spacing_h = dp(16)
        max_btn_h = dp(84)

        available_h = win_h * 0.5
        btn_h = (available_h * 0.5 - spacing_h * (total_buttons - 1)) / total_buttons
        btn_h = max(min(btn_h, max_btn_h), dp(52))
        container_h = btn_h * total_buttons + spacing_h * (total_buttons - 1)

        self.buttons_container.size = (container_w, container_h)
        self.buttons_container.spacing = spacing_h
        self.buttons_container.center_x = win_w / 2
        self.buttons_container.center_y = win_h / 2

        for btn in self.mode_buttons:
            btn.height = btn_h
            fit_font_size(btn, container_w - dp(36), btn_h * 0.4)

        stub_gap = self.title_label.y - self.buttons_container.top
        max_stub_h = max(min(stub_gap - dp(16), win_h * 0.22), dp(30))
        fit_font_size_wrapped(self.lbl_stub, win_w * 0.8, max_stub_h, dp(15))
        self.lbl_stub.text_size = (win_w * 0.8, None)
        self.lbl_stub.size = self.lbl_stub.texture_size
        self.lbl_stub.center_x = win_w / 2
        self.lbl_stub.center_y = (self.title_label.y + self.buttons_container.top) / 2

class SeedCreateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.lbl_title = Label(text="СОЗДАЙТЕ СИД", font_name=font_path("ClearSans-Bold.ttf"),
                               font_size='32sp', color=color_text, bold=True, size_hint=(None, None))
        self.lbl_subtitle = Label(text="Введите загаданное слово, чтобы получить его сид", font_name=font_path("ClearSans-Bold.ttf"),
                                  font_size='14sp', color=color_not_in_word, bold=True, size_hint=(None, None))
        self.lbl_error = Label(text="", font_name=font_path("ClearSans-Bold.ttf"),
                               font_size='15sp', color=color_in_word, bold=True, size_hint=(None, None))
        self.lbl_seed = Label(text="", font_name=font_path("ClearSans-Bold.ttf"),
                              font_size='20sp', color=color_correct, bold=True, size_hint=(None, None))
        self.layout.add_widget(self.lbl_error)
        self.layout.add_widget(self.lbl_seed)
        self.layout.add_widget(self.lbl_title)
        self.layout.add_widget(self.lbl_subtitle)

        self.cells = []
        for _ in range(5):
            cell = GameCell(size=(74, 92))
            cell.base_color = color_blank
            self.cells.append(cell)
            self.layout.add_widget(cell)

        self.keyboard_keys = []

        self.btn_erase = IconKeyButton(image_source="backspace.png", size=(100, 50))
        self.btn_erase.bind(on_release=self.press_erase_key)

        self.btn_enter = IconKeyButton(image_source="corner-down-left.png", size=(100, 50))
        self.btn_enter.bind(on_release=self.press_enter_key)

        self.system_buttons = [self.btn_erase, self.btn_enter]

        self.layout.add_widget(self.btn_erase)
        self.layout.add_widget(self.btn_enter)

        self.btn_exit_top = MenuButton(text="Назад", size_hint=(None, None), size=(dp(92), dp(48)))
        self.btn_exit_top.bind(on_release=self.press_exit_key)
        self.layout.add_widget(self.btn_exit_top)

        self.lines = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮЁ"]
        self.letter_buttons = []
        for line in self.lines:
            row_buttons = []
            for char in line:
                key = KeyButton(text=char, size=(40, 85))
                key.font_size = '22sp'

                key.bind(on_release=self.press_letter_key)

                self.keyboard_keys.append(key)
                self.layout.add_widget(key)
                row_buttons.append(key)
            self.letter_buttons.append(row_buttons)

        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        self.current_word = ""

        self.reset_game()
        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def reposition_elements(self, instance, size):
        win_w = self.width
        win_h = self.height
        self.bg_rect.size = (win_w, win_h)
        self.bg_rect.pos = (0, 0)

        GRID_GAP = dp(6)
        top_reserved = TOP_SAFE_MARGIN + dp(48) + GRID_GAP
        bottom_reserved = BOTTOM_SAFE_MARGIN

        self.btn_exit_top.size = (dp(92), dp(48))
        self.btn_exit_top.pos = (win_w - dp(92) - dp(14), win_h - TOP_SAFE_MARGIN - dp(48))
        fit_font_size(self.btn_exit_top, self.btn_exit_top.width - dp(18), self.btn_exit_top.height * 0.42)

        CELL_SPACING_X = 5
        CELL_SPACING_Y = 5
        side_margin = win_w * 0.11
        avail_cell_w = win_w - (2 * side_margin) - 20
        CELL_WIDTH = avail_cell_w / 5
        CELL_HEIGHT = CELL_WIDTH

        total_blanks_height = (6 * CELL_HEIGHT) + (5 * CELL_SPACING_Y)
        max_allowed_height = (win_h - top_reserved - bottom_reserved) * 0.68
        if total_blanks_height > max_allowed_height:
            total_blanks_height = max_allowed_height
            CELL_HEIGHT = (total_blanks_height - (5 * CELL_SPACING_Y)) / 6
            CELL_WIDTH = CELL_HEIGHT
            side_margin = (win_w - (5 * CELL_WIDTH) - 20) / 2

        for cell in self.cells:
            cell.size = (CELL_WIDTH, CELL_HEIGHT)

        kbd_top_y = self._layout_keyboard(win_w, win_h, bottom_reserved, top_reserved, CELL_HEIGHT)
        top_boundary = win_h - top_reserved

        start_blank_x = side_margin
        total_free_space_y = top_boundary - kbd_top_y
        start_blank_y = kbd_top_y + (total_free_space_y - CELL_HEIGHT) // 2

        for idx, cell in enumerate(self.cells):
            cell.pos = (start_blank_x + idx * (CELL_WIDTH + CELL_SPACING_X), start_blank_y)
            cell.update_canvas()

        fit_font_size(self.lbl_title, win_w * 0.9, dp(24))
        self.lbl_title.text_size = (None, None)
        self.lbl_title.size = self.lbl_title.texture_size

        fit_font_size(self.lbl_subtitle, win_w * 0.85, dp(14))
        self.lbl_subtitle.text_size = (None, None)
        self.lbl_subtitle.size = self.lbl_subtitle.texture_size

        space_above_cells = top_boundary - (start_blank_y + CELL_HEIGHT)
        center_above_y = (start_blank_y + CELL_HEIGHT) + (space_above_cells // 2)

        block_gap = dp(4)
        block_h = self.lbl_title.height + block_gap + self.lbl_subtitle.height
        block_center = min(center_above_y, top_boundary - block_h / 2 - dp(6))
        block_center = max(block_center, kbd_top_y + block_h / 2 + dp(6))

        block_top_y = block_center + block_h / 2
        self.lbl_title.pos = (win_w / 2 - self.lbl_title.width / 2, block_top_y - self.lbl_title.height)
        self.lbl_subtitle.pos = (win_w / 2 - self.lbl_subtitle.width / 2, block_top_y - self.lbl_title.height - block_gap - self.lbl_subtitle.height)

        space_below_cells = start_blank_y - kbd_top_y
        center_below_y = kbd_top_y + (space_below_cells // 2)

        fit_font_size_wrapped(self.lbl_seed, win_w * 0.85, space_below_cells * 0.6, dp(20))
        self.lbl_seed.text_size = (None, None)
        self.lbl_seed.size = self.lbl_seed.texture_size

        fit_font_size(self.lbl_error, win_w * 0.85, dp(16))
        self.lbl_error.text_size = (None, None)
        self.lbl_error.size = self.lbl_error.texture_size

        if self.lbl_seed.text:
            self.lbl_seed.pos = (win_w // 2 - self.lbl_seed.width // 2, center_below_y - self.lbl_seed.height // 2)
            self.lbl_error.pos = (win_w // 2 - self.lbl_error.width // 2, -1000)
        else:
            self.lbl_error.pos = (win_w // 2 - self.lbl_error.width // 2, center_below_y - self.lbl_error.height // 2)
            self.lbl_seed.pos = (win_w // 2 - self.lbl_seed.width // 2, -1000)

        apply_adaptive_fonts(self, CELL_HEIGHT, self.keyboard_keys[0].height if self.keyboard_keys else dp(50))

    def _layout_keyboard(self, win_w, win_h, bottom_reserved, top_reserved, cell_height):
        # ----- КЛАВИАТУРА: та же фиксированная высота (доля от высоты экрана), что и
        # на игровых экранах, чтобы клавиатура выглядела одинаково на всех экранах. -----
        KEY_SPACING_X = 4
        KEY_SPACING_Y = 4
        KEY_HEIGHT_FRACTION = 0.0786
        avail_w = win_w - 16 - 44
        KEY_WIDTH = avail_w / 12
        KEY_HEIGHT = win_h * KEY_HEIGHT_FRACTION

        row_heights = [
            bottom_reserved,
            bottom_reserved + (KEY_HEIGHT + KEY_SPACING_Y),
            bottom_reserved + 2 * (KEY_HEIGHT + KEY_SPACING_Y)
        ]

        for key in self.keyboard_keys:
            key.size = (KEY_WIDTH, KEY_HEIGHT)

        for btn in self.system_buttons:
            btn.size = (KEY_WIDTH, KEY_HEIGHT)

        line_to_height_idx = {0: 2, 1: 1, 2: 0}
        for i, line_keys in enumerate(self.letter_buttons):
            h_idx = line_to_height_idx[i]
            extra_slots = 2 if i == 2 else 0
            total_w = (len(line_keys) + extra_slots) * KEY_WIDTH + (len(line_keys) + extra_slots - 1) * KEY_SPACING_X
            start_l_x = (win_w - total_w) / 2

            if i == 2:
                self.btn_enter.pos = (start_l_x, row_heights[h_idx])
                self.btn_enter.update_canvas()
                start_l_x += KEY_WIDTH + KEY_SPACING_X

            for idx, key in enumerate(line_keys):
                key.pos = (start_l_x + idx * (KEY_WIDTH + KEY_SPACING_X), row_heights[h_idx])
                key.update_canvas()

            if i == 2:
                erase_x = start_l_x + len(line_keys) * (KEY_WIDTH + KEY_SPACING_X)
                self.btn_erase.pos = (erase_x, row_heights[h_idx])
                self.btn_erase.update_canvas()

        return row_heights[2] + KEY_HEIGHT

    def press_letter_key(self, instance):
        self.lbl_error.text = ""
        letter = instance.text

        if len(self.current_word) < 5:
            cell_idx = len(self.current_word)
            if cell_idx < len(self.cells):
                self.cells[cell_idx].text = letter
                self.current_word += letter

    def press_erase_key(self, instance):
        self.lbl_error.text = ""
        if len(self.current_word) > 0:
            cell_idx = len(self.current_word) - 1
            if cell_idx < len(self.cells):
                self.cells[cell_idx].text = ""
                self.current_word = self.current_word[:-1]

    def press_enter_key(self, instance):
        if len(self.current_word) != 5:
            self.lbl_seed.text = ""
            self.lbl_error.color = color_in_word
            self.lbl_error.text = "Слово не из 5 букв!"
            self.reposition_elements(None, None)
            return

        check_word = self.current_word.upper()
        seed = encode_word_to_seed(check_word)

        if seed is None:
            self.lbl_seed.text = ""
            self.lbl_error.color = color_in_word
            self.lbl_error.text = "Такого слова нет в словаре!"
            self.reposition_elements(None, None)
            return

        self.lbl_error.text = ""
        self.lbl_seed.text = f"Сид: {seed}"
        self.lbl_subtitle.text = "Нажмите на сид, чтобы скопировать его"
        self.current_word = ""
        for cell in self.cells:
            cell.text = ""
        self.reposition_elements(None, None)

    def on_touch_down(self, touch):
        if self.lbl_seed.text and self.lbl_seed.collide_point(*touch.pos):
            seed_part = self.lbl_seed.text.split(": ", 1)[-1].strip()
            try:
                Clipboard.copy(seed_part)
            except Exception:
                pass
            self.lbl_error.color = color_correct
            self.lbl_error.text = "Сид скопирован в буфер обмена!"
            self.reposition_elements(None, None)
            Clock.schedule_once(self._clear_copy_notice, 1.4)
            return True
        return super().on_touch_down(touch)

    def _clear_copy_notice(self, dt):
        self.lbl_error.text = ""
        self.lbl_error.color = color_in_word
        self.reposition_elements(None, None)

    def press_exit_key(self, instance):
        self.reset_game()
        self.manager.current = 'seed_generation'

    def reset_game(self):
        self.current_word = ""
        self.lbl_error.text = ""
        self.lbl_error.color = color_in_word
        self.lbl_seed.text = ""
        self.lbl_subtitle.text = "Введите загаданное слово, чтобы получить его сид"

        for cell in self.cells:
            cell.text = ""
            cell.base_color = color_blank
            cell.color = color_text
            cell.update_canvas()

        for key_btn in self.keyboard_keys:
            key_btn.base_color = color_key
            key_btn.color = color_text
            key_btn.cell_status = "blank"
            key_btn.update_canvas()

        for btn in self.system_buttons:
            btn.base_color = color_key
            btn.color = color_text
            btn.update_canvas()

        self.reposition_elements(None, None)

class SeedEnterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.lbl_title = Label(text="ВВЕДИТЕ СИД", font_name=font_path("ClearSans-Bold.ttf"),
                               font_size='32sp', color=color_text, bold=True, size_hint=(None, None))
        self.lbl_subtitle = Label(text="Введите сид, который вам прислал друг", font_name=font_path("ClearSans-Bold.ttf"),
                                  font_size='14sp', color=color_not_in_word, bold=True, size_hint=(None, None))
        self.lbl_error = Label(text="", font_name=font_path("ClearSans-Bold.ttf"),
                               font_size='15sp', color=color_in_word, bold=True, size_hint=(None, None))
        self.layout.add_widget(self.lbl_error)
        self.layout.add_widget(self.lbl_title)
        self.layout.add_widget(self.lbl_subtitle)

        self.cells = []
        for _ in range(SEED_LENGTH):
            cell = GameCell(size=(60, 74))
            cell.base_color = color_blank
            self.cells.append(cell)
            self.layout.add_widget(cell)

        self.keyboard_keys = []

        self.btn_erase = IconKeyButton(image_source="backspace.png", size=(100, 50))
        self.btn_erase.bind(on_release=self.press_erase_key)

        self.btn_enter = IconKeyButton(image_source="corner-down-left.png", size=(100, 50))
        self.btn_enter.bind(on_release=self.press_enter_key)

        self.system_buttons = [self.btn_erase, self.btn_enter]

        self.layout.add_widget(self.btn_erase)
        self.layout.add_widget(self.btn_enter)

        self.btn_exit_top = MenuButton(text="Назад", size_hint=(None, None), size=(dp(92), dp(48)))
        self.btn_exit_top.bind(on_release=self.press_exit_key)
        self.layout.add_widget(self.btn_exit_top)

        self.lines = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮЁ"]
        self.letter_buttons = []
        for line in self.lines:
            row_buttons = []
            for char in line:
                key = KeyButton(text=char, size=(40, 85))
                key.font_size = '22sp'

                key.bind(on_release=self.press_letter_key)

                self.keyboard_keys.append(key)
                self.layout.add_widget(key)
                row_buttons.append(key)
            self.letter_buttons.append(row_buttons)

        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        self.current_word = ""

        self.reset_game()
        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def reposition_elements(self, instance, size):
        win_w = self.width
        win_h = self.height
        self.bg_rect.size = (win_w, win_h)
        self.bg_rect.pos = (0, 0)

        GRID_GAP = dp(6)
        top_reserved = TOP_SAFE_MARGIN + dp(48) + GRID_GAP
        bottom_reserved = BOTTOM_SAFE_MARGIN

        self.btn_exit_top.size = (dp(92), dp(48))
        self.btn_exit_top.pos = (win_w - dp(92) - dp(14), win_h - TOP_SAFE_MARGIN - dp(48))
        fit_font_size(self.btn_exit_top, self.btn_exit_top.width - dp(18), self.btn_exit_top.height * 0.42)

        CELL_SPACING_X = 5
        CELL_SPACING_Y = 5

        ref_side_margin = win_w * 0.11
        ref_avail_cell_w = win_w - (2 * ref_side_margin) - 20
        REF_CELL_WIDTH = ref_avail_cell_w / 5
        REF_CELL_HEIGHT = REF_CELL_WIDTH

        total_blanks_height = (6 * REF_CELL_HEIGHT) + (5 * CELL_SPACING_Y)
        max_allowed_height = (win_h - top_reserved - bottom_reserved) * 0.68
        if total_blanks_height > max_allowed_height:
            total_blanks_height = max_allowed_height
            REF_CELL_HEIGHT = (total_blanks_height - (5 * CELL_SPACING_Y)) / 6

        CELL_HEIGHT = REF_CELL_HEIGHT
        CELL_WIDTH = CELL_HEIGHT
        side_margin = (win_w - (SEED_LENGTH * CELL_WIDTH) - (5 * CELL_SPACING_X)) / 2

        for cell in self.cells:
            cell.size = (CELL_WIDTH, CELL_HEIGHT)

        kbd_top_y = self._layout_keyboard(win_w, win_h, bottom_reserved, top_reserved, CELL_HEIGHT)

        top_boundary = win_h - top_reserved

        start_blank_x = side_margin
        total_free_space_y = top_boundary - kbd_top_y
        start_blank_y = kbd_top_y + (total_free_space_y - CELL_HEIGHT) // 2

        for idx, cell in enumerate(self.cells):
            cell.pos = (start_blank_x + idx * (CELL_WIDTH + CELL_SPACING_X), start_blank_y)
            cell.update_canvas()

        fit_font_size(self.lbl_title, win_w * 0.9, dp(24))
        self.lbl_title.text_size = (None, None)
        self.lbl_title.size = self.lbl_title.texture_size

        fit_font_size(self.lbl_subtitle, win_w * 0.85, dp(14))
        self.lbl_subtitle.text_size = (None, None)
        self.lbl_subtitle.size = self.lbl_subtitle.texture_size

        space_above_cells = top_boundary - (start_blank_y + CELL_HEIGHT)
        center_above_y = (start_blank_y + CELL_HEIGHT) + (space_above_cells // 2)

        block_gap = dp(4)
        block_h = self.lbl_title.height + block_gap + self.lbl_subtitle.height
        block_center = min(center_above_y, top_boundary - block_h / 2 - dp(6))
        block_center = max(block_center, kbd_top_y + block_h / 2 + dp(6))

        block_top_y = block_center + block_h / 2
        self.lbl_title.pos = (win_w / 2 - self.lbl_title.width / 2, block_top_y - self.lbl_title.height)
        self.lbl_subtitle.pos = (win_w / 2 - self.lbl_subtitle.width / 2, block_top_y - self.lbl_title.height - block_gap - self.lbl_subtitle.height)

        space_below_cells = start_blank_y - kbd_top_y
        center_below_y = kbd_top_y + (space_below_cells // 2)

        fit_font_size(self.lbl_error, win_w * 0.85, dp(16))
        self.lbl_error.text_size = (None, None)
        self.lbl_error.size = self.lbl_error.texture_size
        self.lbl_error.pos = (win_w // 2 - self.lbl_error.width // 2, center_below_y - self.lbl_error.height // 2)

        apply_adaptive_fonts(self, CELL_HEIGHT, self.keyboard_keys[0].height if self.keyboard_keys else dp(50))

    def _layout_keyboard(self, win_w, win_h, bottom_reserved, top_reserved, cell_height):
        # ----- КЛАВИАТУРА: та же фиксированная высота (доля от высоты экрана), что и
        # на игровых экранах, чтобы клавиатура выглядела одинаково на всех экранах. -----
        KEY_SPACING_X = 4
        KEY_SPACING_Y = 4
        KEY_HEIGHT_FRACTION = 0.0786
        avail_w = win_w - 16 - 44
        KEY_WIDTH = avail_w / 12
        KEY_HEIGHT = win_h * KEY_HEIGHT_FRACTION

        row_heights = [
            bottom_reserved,
            bottom_reserved + (KEY_HEIGHT + KEY_SPACING_Y),
            bottom_reserved + 2 * (KEY_HEIGHT + KEY_SPACING_Y)
        ]

        for key in self.keyboard_keys:
            key.size = (KEY_WIDTH, KEY_HEIGHT)

        for btn in self.system_buttons:
            btn.size = (KEY_WIDTH, KEY_HEIGHT)

        line_to_height_idx = {0: 2, 1: 1, 2: 0}
        for i, line_keys in enumerate(self.letter_buttons):
            h_idx = line_to_height_idx[i]
            extra_slots = 2 if i == 2 else 0
            total_w = (len(line_keys) + extra_slots) * KEY_WIDTH + (len(line_keys) + extra_slots - 1) * KEY_SPACING_X
            start_l_x = (win_w - total_w) / 2

            if i == 2:
                self.btn_enter.pos = (start_l_x, row_heights[h_idx])
                self.btn_enter.update_canvas()
                start_l_x += KEY_WIDTH + KEY_SPACING_X

            for idx, key in enumerate(line_keys):
                key.pos = (start_l_x + idx * (KEY_WIDTH + KEY_SPACING_X), row_heights[h_idx])
                key.update_canvas()

            if i == 2:
                erase_x = start_l_x + len(line_keys) * (KEY_WIDTH + KEY_SPACING_X)
                self.btn_erase.pos = (erase_x, row_heights[h_idx])
                self.btn_erase.update_canvas()

        return row_heights[2] + KEY_HEIGHT

    def press_letter_key(self, instance):
        self.lbl_error.text = ""
        letter = instance.text

        if len(self.current_word) < SEED_LENGTH:
            cell_idx = len(self.current_word)
            if cell_idx < len(self.cells):
                self.cells[cell_idx].text = letter
                self.current_word += letter

    def press_erase_key(self, instance):
        self.lbl_error.text = ""
        if len(self.current_word) > 0:
            cell_idx = len(self.current_word) - 1
            if cell_idx < len(self.cells):
                self.cells[cell_idx].text = ""
                self.current_word = self.current_word[:-1]

    def press_enter_key(self, instance):
        if len(self.current_word) != SEED_LENGTH:
            self.lbl_error.text = "Введите 6 букв!"
            self.reposition_elements(None, None)
            return

        entered_seed = self.current_word.upper()
        found_word = decode_seed_to_word(entered_seed)

        if found_word is None:
            self.lbl_error.text = "Неверно введёный сид."
            self.reposition_elements(None, None)
            return

        self.lbl_error.text = ""
        self._send_to_two_player_screen(found_word)

    def _send_to_two_player_screen(self, secret_word):
        tp_screen = self.manager.get_screen('two_player_game')
        tp_screen.reset_game()
        tp_screen.secret_word = secret_word
        tp_screen.stage = "playing"
        tp_screen.current_word = ""
        tp_screen.current_attempt = 0
        tp_screen.lbl_title.text = ""
        tp_screen.lbl_subtitle.text = ""
        tp_screen.lbl_error.text = ""

        for cell in tp_screen.cells:
            cell.text = ""

        tp_screen.reposition_elements(None, None)

        self.reset_game()
        self.manager.current = 'two_player_game'

    def press_exit_key(self, instance):
        self.reset_game()
        self.manager.current = 'seed_generation'

    def reset_game(self):
        self.current_word = ""
        self.lbl_error.text = ""

        for cell in self.cells:
            cell.text = ""
            cell.base_color = color_blank
            cell.color = color_text
            cell.update_canvas()

        for key_btn in self.keyboard_keys:
            key_btn.base_color = color_key
            key_btn.color = color_text
            key_btn.cell_status = "blank"
            key_btn.update_canvas()

        for btn in self.system_buttons:
            btn.base_color = color_key
            btn.color = color_text
            btn.update_canvas()

        self.reposition_elements(None, None)

class HowToPlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(self.btn_back)
        self.title_label = Label(
            text="Как играть",
            font_name=font_path("ClearSans-Bold.ttf"),
            font_size='28sp',
            bold=True,
            color=color_text,
            size_hint=(None, None)
        )
        self.layout.add_widget(self.title_label)
        self.scroll_view = ScrollView(size_hint=(None, None), do_scroll_x=False, do_scroll_y=True)
        self.content_box = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None, padding=[20, 10, 20, 20])
        self.content_box.bind(minimum_height=self.content_box.setter('height'))

        self.title_labels = []
        self.text_labels = []
        self.row_labels = []

        def add_title(text):
            lbl = Label(text=text, font_name=font_path("ClearSans-Bold.ttf"), font_size='18sp', 
                        bold=True, color=color_in_word, size_hint_y=None, halign='left', valign='middle')
            lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
            self.title_labels.append(lbl)
            self.content_box.add_widget(lbl)
            
        def add_text(text, custom_color=None):
            lbl = Label(text=text, font_name=font_path("ClearSans-Bold.ttf"), font_size='14sp', 
                        color=custom_color if custom_color else color_text, size_hint_y=None, halign='left', valign='top')
            lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
            self.text_labels.append(lbl)
            self.content_box.add_widget(lbl)
            
        def add_row(letter, status, description, text_col=None):
            row = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=dp(32))

            cell = GameCell(size=(dp(32), dp(32)))
            cell.text = letter
            cell.change_type(status)
            cell.text_size = cell.size
            cell.font_size = '22sp'
            cell.halign = 'center'
            cell.valign = 'middle'
            cell.padding = [0, 0, 0, 4]
            
            desc = Label(text=description, font_name=font_path("ClearSans-Bold.ttf"), font_size='14sp', 
                        color=text_col if text_col else color_text, size_hint_y=None, halign='left', valign='top')

            desc.bind(texture_size=lambda inst, val: [
                setattr(inst, 'height', val[1]), 
                setattr(row, 'height', max(dp(32), val[1]))
            ])
            
            row.add_widget(cell)
            row.add_widget(desc)
            self.row_labels.append(desc)
            self.content_box.add_widget(row)

        add_title("О ЧЕМ ЭТА ИГРА?")
        add_text("Игра является цифровой головоломкой на логику и эрудицию.")
        add_text("Ваша главная цель - за 6 попыток вычислить секретное слово.")
        add_text("Загаданное слово всегда состоит строго из 5 букв.")
        add_text("Вводите ваши варианты слов и следите за изменением цветов ячеек!")
        add_text("Если вы потратите все 6 попыток и не угадаете - раунд завершится.", color_not_in_word)
        
        add_title("РАСШИФРОВКА ЦВЕТОВ ЯЧЕЕК:")
        add_row("А", "blank", "- Цвет пустой клетки. Буква введена, но еще не подтверждена клавишей ВВОД.")
        add_row("А", "not_in_word", "- Такой буквы нет в загаданном слове. На клавиатуре клавиша станет серой.")
        add_row("А", "in_word", "- Буква есть в слове, но в данный момент она стоит на другом месте.")
        add_row("А", "correct", "- Буква угадана идеально и стоит на своем правильном месте!", color_correct)
        add_text("Если все 5 букв в ряду загорелись зелёным - ВЫ ВЫИГРАЛИ!", color_correct)
        add_text("Тратьте монеты в магазине Кастомизации, чтобы разблокировать новые цветовые палитры интерфейса.", color_not_in_word)
        
        add_title("ЭКОНОМИКА И ЗАРАБОТОК МОНЕТ:")
        add_text("Каждая проверенная буква в раунде прибавляет монеты в ваш кошелёк:")
        add_text("Зелёная ячейка (Точное попадание) - +5 монет", color_correct)
        add_text("Жёлтая ячейка (Буква есть в слове) - +2 монеты", color_in_word)
        add_text("Серая ячейка (Буквы нет в слове) - +1 монета", color_not_in_word)
        add_text("Успешная полная победа в матче - +10 монет", color_correct)
        
        add_title("СИСТЕМА ДОСТИЖЕНИЙ:")
        add_text("За выполнение особых условий во время игры вы получаете Достижения.")
        add_text("При получении достижения оно показывается на экране.")
        add_text("В зависимости от сложности, достижения выдают крупные бонусы:")
        add_text("Лёгкие карточки наград - +30 монет")
        add_text("Средние карточки наград - +50 монет", color_in_word)
        add_text("Эпические карточки наград - +500 монет", color_correct)
        
        add_title("ЕЖЕДНЕВНЫЕ ЗАДАНИЯ И СЕРИИ:")
        add_text("Каждые новые сутки строго в 00:00 игра выдаёт 5 случайных квестов.")
        add_text("Выполняйте их в Одиночном режиме, чтобы забирать награды.")
        add_text("Текст наград выполненных квестов на карточках становится серым.")
        add_text("Копите непрерывные серии побед, чтобы увеличивать Серию побед.")
        add_text("Внимание: ЛЮБОЕ поражение полностью сбрасывает Серию побед!", color_not_in_word)

        self.scroll_view.add_widget(self.content_box)
        self.layout.add_widget(self.scroll_view)
        self.add_widget(self.layout)

        self.bind(size=self.reposition_elements)
        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def reposition_elements(self, instance, size):
        win_w, win_h = self.width, self.height

        back_w, back_h = dp(92), dp(48)
        btn_y = win_h - TOP_SAFE_MARGIN - back_h
        self.btn_back.size = (back_w, back_h)
        self.btn_back.pos = (win_w - back_w - dp(14), btn_y)
        fit_font_size(self.btn_back, back_w - dp(18), back_h * 0.42)

        title_max_w = max(win_w - back_w - dp(14) - dp(15) - dp(10), dp(60))
        title_h = min(win_h * 0.05, dp(32))
        fit_font_size(self.title_label, title_max_w, title_h * 0.85)
        self.title_label.text_size = (None, None)
        self.title_label.size = self.title_label.texture_size
        self.title_label.x = dp(15)
        self.title_label.y = btn_y + (back_h - self.title_label.height) / 2 + dp(4)

        self.scroll_view.size = (win_w, btn_y - BOTTOM_SAFE_MARGIN)
        self.scroll_view.pos = (0, BOTTOM_SAFE_MARGIN)

        self.scroll_view.effect_cls = ScrollEffect
        if self.scroll_view.effect_cls:
            self.scroll_view.effect_cls.bounces = False
        self.scroll_view.bar_width = 0

        text_width = int(win_w - 40)
        row_text_width = int(win_w - 40 - 54 - 30)

        for lbl in self.title_labels:
            lbl.text_size = (text_width, None)
        for lbl in self.text_labels:
            lbl.text_size = (text_width, None)
        for lbl in self.row_labels:
            lbl.text_size = (row_text_width, None)

class AchievementsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.stub_layout = create_stub_layout(self, "")
        self.layout.add_widget(self.stub_layout)

        self.top_overlay = FloatLayout(size_hint=(1, None))
        with self.top_overlay.canvas.before:
            Color(*color_bg)
            self.overlay_rect = RoundedRectangle(pos=(0, 0), size=(360, 200), radius=[12])
        self.layout.add_widget(self.top_overlay)

        if self.stub_layout.children:

            btn = [child for child in self.stub_layout.children if isinstance(child, MenuButton)][0]
            self.stub_layout.remove_widget(btn)
            self.layout.add_widget(btn)

        self.lbl_main_title = Label(
            text="Достижения", 
            font_name=font_path("ClearSans-Bold.ttf"), 
            bold=True, 
            color=color_text,
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )
        self.layout.add_widget(self.lbl_main_title)

        self.stats_scroll = ScrollView(size_hint=(1, None), do_scroll_x=True, do_scroll_y=False, bar_width=0)

        from kivy.effects.scroll import ScrollEffect
        self.stats_scroll.effect_cls = ScrollEffect
        
        self.stats_container = BoxLayout(orientation='vertical', spacing=8, size_hint=(None, None))
        self.stats_row1 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None))
        self.stats_row2 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None))
        
        self.stats_container.add_widget(self.stats_row1)
        self.stats_container.add_widget(self.stats_row2)
        self.stats_scroll.add_widget(self.stats_container)
        self.layout.add_widget(self.stats_scroll)
        
        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        self.scroll_view = ScrollView(size_hint=(1, None), do_scroll_x=False, do_scroll_y=True, bar_width=0)

        from kivy.effects.scroll import ScrollEffect
        self.scroll_view.effect_cls = ScrollEffect

        self.ach_list_layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[0, 0, 0, dp(20)])
        self.ach_list_layout.bind(minimum_height=self.ach_list_layout.setter('height'))

        self.scroll_view.add_widget(self.ach_list_layout)

        self.layout.add_widget(self.scroll_view)

        if hasattr(self, 'top_overlay'):
            self.layout.remove_widget(self.scroll_view)
            self.layout.add_widget(self.scroll_view, index=len(self.layout.children))
        self._ach_last_signature = None
        self._ach_build_event = None

        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def on_enter(self):
        self.refresh_stats_and_achievements()

    def reposition_elements(self, instance, size):
        win_w = self.width
        win_h = self.height
        overlay_height = min(win_h * 0.32, dp(230))

        self.top_overlay.height = overlay_height
        self.top_overlay.pos = (0, win_h - overlay_height)

        self.overlay_rect.size = (win_w, overlay_height)
        self.overlay_rect.pos = (0, win_h - overlay_height)

        back_w, back_h = dp(92), dp(48)
        back_btn = None
        for child in self.layout.children:
            if isinstance(child, MenuButton):
                back_btn = child
                break
        if back_btn is not None:
            back_btn.size = (back_w, back_h)
            back_btn.pos = (win_w - back_w - dp(14), win_h - TOP_SAFE_MARGIN - back_h)
            fit_font_size(back_btn, back_w - dp(18), back_h * 0.42)

        title_h = min(win_h * 0.05, dp(34))
        self.lbl_main_title.size = (win_w - back_w - dp(45), title_h)
        self.lbl_main_title.text_size = (None, None)
        fit_font_size(self.lbl_main_title, win_w - back_w - dp(45), title_h * 0.85)
        self.lbl_main_title.text_size = self.lbl_main_title.size
        self.lbl_main_title.y = win_h - TOP_SAFE_MARGIN - back_h / 2 - title_h / 2 + dp(4)
        self.lbl_main_title.x = dp(15)

        stats_h = dp(70) * 2 + dp(8)
        self.stats_scroll.height = stats_h
        self.stats_scroll.size_hint_x = 1
        self.stats_scroll.do_scroll_x = False

        header_bottom = (back_btn.y if back_btn is not None else win_h - TOP_SAFE_MARGIN - back_h) - dp(10)
        self.stats_scroll.pos = (0, header_bottom - stats_h)
        self.stats_container.size = (win_w, stats_h)
        self.stats_container.padding = [dp(12), 0, dp(12), 0]
        self.stats_container.spacing = dp(8)

        row_w = win_w - dp(24)
        self.stats_row1.size = (row_w, dp(70))
        self.stats_row2.size = (row_w, dp(70))
        self.stats_row1.spacing = dp(8)
        self.stats_row2.spacing = dp(8)

        for row in (self.stats_row1, self.stats_row2):
            for card in row.children:
                if hasattr(card, 'label_ref'):
                    fit_font_size(card.label_ref, row_w / 3 * 0.85, dp(15))
                    fit_font_size(card.value_ref, row_w / 3 * 0.85, dp(22))

        list_top = self.stats_scroll.y - dp(10)
        self.scroll_view.size = (win_w, list_top - BOTTOM_SAFE_MARGIN)
        self.scroll_view.pos = (0, BOTTOM_SAFE_MARGIN)

        self.ach_list_layout.width = win_w

    def create_card(self, label_text, val_text, val_color):
        card = FloatLayout(size_hint=(1, 1))

        with card.canvas.before:
            Color(*color_blank)
            r_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
        card.bind(pos=lambda inst, v: setattr(r_rect, 'pos', inst.pos), size=lambda inst, v: setattr(r_rect, 'size', inst.size))
        
        lbl_lbl = Label(
            text=label_text, 
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_not_in_word,
            size_hint=(1, 0.45),
            pos_hint={'x': 0, 'y': 0.48},
            halign='center', 
            valign='middle'
        )
        card.add_widget(lbl_lbl)
        
        lbl_val = Label(
            text=val_text, 
            font_name=font_path("ClearSans-Bold.ttf"),
            color=val_color, 
            bold=True, 
            size_hint=(1, 0.5),
            pos_hint={'x': 0, 'y': 0.02},
            halign='center', 
            valign='middle'
        )
        card.add_widget(lbl_val)

        card.label_ref = lbl_lbl
        card.value_ref = lbl_val
        return card
    
    def create_achievement_row(self, name, description, ach_data, got, date_str):
        row = FloatLayout(size_hint_y=None, height=110)

        def lerp_color(c1, c2, factor):
            return (
                c1[0] + (c2[0] - c1[0]) * factor,
                c1[1] + (c2[1] - c1[1]) * factor,
                c1[2] + (c2[2] - c1[2]) * factor,
                1.0
            )

        r_type = "common"
        if isinstance(ach_data, dict):
            r_type = ach_data.get("type", "common").lower().strip()

        if r_type == "rare":
            rare_color = lerp_color(color_text, color_in_word, 0.5)
            type_text = "Редкое"
        elif r_type == "epic":
            rare_color = lerp_color(color_text, color_correct, 0.6)
            type_text = "Эпическое"
        else:
            rare_color = lerp_color(color_text, color_bg, 0.3)
            type_text = "Обычное"

        if got:
            bg_color = color_blank
            text_color = color_text
            status_color = color_correct
        else:
            bg_color = lerp_color(color_blank, color_bg, 0.5)
            text_color = lerp_color(color_text, color_bg, 0.4)
            rare_color = lerp_color(rare_color, color_bg, 0.3)
            status_color = color_not_in_word

        with row.canvas.before:
            Color(*bg_color)
            bg_rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[12])
            
            Color(*rare_color)
            ribbon_rect = RoundedRectangle(pos=row.pos, size=(10, 110), radius=[(12, 12), (0, 0), (0, 0), (12, 12)])
            
        def sync_graphics(instance, value):
            bg_rect.pos = (instance.x + 15, instance.y)
            bg_rect.size = (instance.width - 30, instance.height)
            ribbon_rect.pos = (instance.x + 15, instance.y)
            ribbon_rect.size = (10, instance.height)
        row.bind(pos=sync_graphics, size=sync_graphics)

        return self.fill_achievement_widgets(row, name, description, got, date_str, type_text, rare_color, text_color, status_color, bg_rect, ribbon_rect)

    def fill_achievement_widgets(self, row, name, description, got, date_str, type_text, rarity_color, text_color, status_color, bg_rect, ribbon_rect):
        text_w = self.width - 45
        font_path = font_path("ClearSans-Bold.ttf")
        name_lbl = Label(
            text=name.upper(), font_name=font_path,
            font_size='18sp', color=text_color, bold=True,
            size_hint=(None, None), width=text_w, text_size=(text_w, None),
            halign='left', valign='top'
        )
        name_lbl.texture_update()
        name_lbl.height = name_lbl.texture_size[1]
        name_lbl.bind(texture_size=lambda inst, sz: setattr(inst, 'height', sz[1]))
        desc_lbl = Label(
            text=description, font_name=font_path,
            font_size='13sp', color=text_color,
            size_hint=(None, None), width=text_w, text_size=(text_w, None),
            halign='left', valign='top'
        )
        desc_lbl.texture_update()
        desc_lbl.height = desc_lbl.texture_size[1]
        desc_lbl.bind(texture_size=lambda inst, sz: setattr(inst, 'height', sz[1]))
        info_h = dp(30)
        info_line = FloatLayout(size_hint=(1, None), height=info_h)
        seg_w = max((self.width - dp(24)) / 3, dp(60))
        lbl_rare = Label(
            text=type_text, font_name=font_path, color=rarity_color, bold=True,
            size_hint=(None, None), size=(seg_w, info_h),
            pos_hint={'x': 0.06, 'center_y': 0.5}, halign='left', valign='middle'
        )
        fit_font_size(lbl_rare, seg_w - dp(8), dp(13))
        lbl_rare.text_size = (seg_w, info_h)
        lbl_date = Label(
            text=f"Дата: {date_str}" if (got and date_str) else "",
            font_name=font_path, color=color_not_in_word, bold=True,
            size_hint=(None, None), size=(seg_w, info_h),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, halign='center', valign='middle'
        )
        fit_font_size(lbl_date, seg_w - dp(8), dp(12))
        lbl_date.text_size = (seg_w, info_h)
        lbl_stat = Label(
            text="ПОЛУЧЕНО" if got else "НЕ ПОЛУЧЕНО", font_name=font_path, color=status_color, bold=True,
            size_hint=(None, None), size=(seg_w, info_h),
            pos_hint={'right': 0.97, 'center_y': 0.5}, halign='right', valign='middle'
        )
        fit_font_size(lbl_stat, seg_w - dp(8), dp(13))
        lbl_stat.text_size = (seg_w, info_h)
        
        info_line.add_widget(lbl_rare)
        info_line.add_widget(lbl_date)
        info_line.add_widget(lbl_stat)

        text_group = FloatLayout(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        text_group.add_widget(name_lbl)
        text_group.add_widget(desc_lbl)
        text_group.add_widget(info_line)

        def sync_row_height(*args):
            name_lbl.height = name_lbl.texture_size[1]
            desc_lbl.height = desc_lbl.texture_size[1]
            total_h = 4 + name_lbl.height + 2 + desc_lbl.height + 8 + info_line.height + 4

            row.height = max(75, total_h)
            ribbon_rect.size = (10, row.height)

            name_lbl.pos_hint = {'x': 0.06, 'top': 1.0 - (4 / row.height)}
            desc_lbl.pos_hint = {'x': 0.06, 'top': name_lbl.pos_hint['top'] - (name_lbl.height / row.height) - (2 / row.height)}
            info_line.pos_hint = {'x': 0, 'y': 4 / row.height}

        desc_lbl.bind(texture_size=sync_row_height)
        name_lbl.bind(texture_size=sync_row_height)
        row.bind(size=sync_row_height)
        sync_row_height()

        row.add_widget(text_group)
        return row
    
    def build_achievements_list(self, launcher_achievements):
        if self._ach_build_event is not None:
            self._ach_build_event.cancel()
            self._ach_build_event = None

        self.ach_list_layout.clear_widgets()

        if not launcher_achievements:
            return

        all_keys = list(launcher_achievements.keys())
        sorted_keys = sorted(all_keys, key=lambda k: launcher_achievements[k].get("got", False), reverse=True)
        remaining = list(sorted_keys)

        def build_chunk(dt):
            ROWS_PER_FRAME = 4
            for _ in range(ROWS_PER_FRAME):
                if not remaining:
                    self._ach_build_event = None
                    return False
                ach_key = remaining.pop(0)
                ach_data = launcher_achievements[ach_key]

                name = ach_data.get("name", "Секретное достижение")
                description = ach_data.get("description", "")
                got = ach_data.get("got", False)
                date_str = ach_data.get("date", "")

                row_widget = self.create_achievement_row(name, description, ach_data, got, date_str)
                self.ach_list_layout.add_widget(row_widget)
            return True

        if build_chunk(0):
            self._ach_build_event = Clock.schedule_interval(build_chunk, 0)

    def refresh_stats_and_achievements(self):
        stats = MOBILE_PLAYER_STATS if ('MOBILE_PLAYER_STATS' in globals() and MOBILE_PLAYER_STATS) else {}
        launcher_ach = MOBILE_ACHIVEMENTS if ('MOBILE_ACHIVEMENTS' in globals() and MOBILE_ACHIVEMENTS) else {}
        
        coins = stats.get("player_coins", 0)
        wins = stats.get("total_wins", 0)
        losses = stats.get("total_losses", 0)
        streak = f"{stats.get('current_win_streak', 0)}/{stats.get('max_win_streak', 0)}"
        quests = stats.get("total_completed_quests", 0)
        
        got_count = sum(1 for ach in launcher_ach.values() if ach.get("got", False))
        ach_ratio = f"{got_count}/{len(launcher_ach)}" if launcher_ach else "0/16"
        signature = (
            coins, wins, losses, streak, quests, ach_ratio,
            tuple(sorted((k, v.get("got", False), v.get("date", "")) for k, v in launcher_ach.items()))
        )
        if (signature == self._ach_last_signature
                and self.ach_list_layout.children
                and self._ach_build_event is None):
            return
        self._ach_last_signature = signature

        self.stats_row1.clear_widgets()
        self.stats_row2.clear_widgets()

        row1_data = [
            ("Монеты", str(coins), color_in_word),
            ("Победы", str(wins), color_correct),
            ("Поражения", str(losses), color_text)
        ]
        
        row2_data = [
            ("Серия побед", streak, color_text),
            ("Достижения", ach_ratio, color_text),
            ("Квесты", str(quests), color_text)
        ]

        for item in row1_data:
            self.stats_row1.add_widget(self.create_card(*item))
            
        for item in row2_data:
            self.stats_row2.add_widget(self.create_card(*item))

        self.reposition_elements(None, None)

        self.build_achievements_list(launcher_ach)

class CustomizationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            self.bg_color_instr = Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

            self.pad_color_instr = Color(*color_bg)
            self.top_pad_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[0])
            self.bottom_pad_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[0])

            self.top_coins_color = Color(*color_key)
            self.block_coins_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[12])
            
            self.top_theme_color = Color(*color_key)
            self.block_theme_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[12])
            
            self.top_status_color = Color(*color_key)
            self.block_status_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[12])

        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        
        self.lbl_title = Label(
            text="Кастомизация", 
            font_name=font_path("ClearSans-Bold.ttf"),
            font_size='32sp', 
            color=color_text, 
            bold=True, 
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )

        self.lbl_coins_title = Label(text="Монеты:", font_name=font_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')
        self.lbl_theme_title = Label(text="Тема:", font_name=font_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')
        self.lbl_status_title = Label(text="Статус:", font_name=font_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')
        self.lbl_coins_val = Label(text="0",font_name=font_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_in_word,size_hint=(None, None), halign='center', valign='middle')
        self.lbl_theme_val = Label(text="Классика", font_name=font_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')
        self.lbl_status_val = Label(text="Применено", font_name=font_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')

        for lbl in [self.lbl_coins_title, self.lbl_theme_title, self.lbl_status_title, self.lbl_coins_val, self.lbl_theme_val, self.lbl_status_val]:
            lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

        self.btn_action = MenuButton(text="КУПИТЬ", size_hint=(None, None))
        self.btn_action.background_normal = 'atlas://data/images/defaulttheme/button_pressed'
        self.btn_action.background_color = (0, 0, 0, 0)
        self.btn_action.color = color_text
        self.btn_action.font_size = '18sp'
        self.btn_action.disabled_color = color_text 

        with self.btn_action.canvas.before:
            self.btn_action_color = Color(*color_key)
            self.rect_action = RoundedRectangle(pos=self.btn_action.pos, size=self.btn_action.size, radius=[12])

        self.btn_sell = MenuButton(text="ПРОДАТЬ ЗА 900", size_hint=(None, None))
        self.btn_sell.background_normal = 'atlas://data/images/defaulttheme/button_pressed'
        self.btn_sell.background_color = (0, 0, 0, 0)
        self.btn_sell.color = color_text
        self.btn_sell.font_size = '18sp'
        self.btn_sell.disabled_color = color_not_in_word

        with self.btn_sell.canvas.before:
            self.btn_sell_color = Color(*color_key)
            self.rect_sell = RoundedRectangle(pos=self.btn_sell.pos, size=self.btn_sell.size, radius=[12])

        self.layout.add_widget(self.btn_action)
        self.layout.add_widget(self.btn_sell)

        self.btn_action.bind(on_release=self.process_theme_action)
        self.btn_sell.bind(on_release=self.process_theme_sell)

        self.layout.add_widget(self.lbl_title)
        self.layout.add_widget(self.btn_back)
        
        self.layout.add_widget(self.lbl_coins_title)
        self.layout.add_widget(self.lbl_theme_title)
        self.layout.add_widget(self.lbl_status_title)
        self.layout.add_widget(self.lbl_coins_val)
        self.layout.add_widget(self.lbl_theme_val)
        self.layout.add_widget(self.lbl_status_val)
        
        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        self.scroll_view = ScrollView(
            size_hint=(None, None), 
            do_scroll_x=False, 
            do_scroll_y=True, 
            bar_width=0,
            effect_cls=ScrollEffect
        )

        self.scroll_content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=(15, 10))
        self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))
        
        self.scroll_view.add_widget(self.scroll_content)
        self.layout.add_widget(self.scroll_view)

        global MOBILE_PLAYER_STATS
        self.theme_cards = {} 
        
        active_theme_id = MOBILE_PLAYER_STATS.get("active_theme_name", "classic")
        self.selected_theme_id = active_theme_id 
        
        for t_id, t_data in color_themes.items():
            t_title = t_data.get("color_name", t_id.capitalize())

            card = ThemeCard(
                theme_id=t_id, 
                theme_name=t_title, 
                theme_data=t_data, 
                on_click_callback=self.select_theme
            )
            
            if t_id == active_theme_id:
                card.is_active = True
                card.update_graphics(card, card.size)
                
            self.theme_cards[t_id] = card
            self.scroll_content.add_widget(card)

        self.select_theme(self.selected_theme_id)
        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def on_enter(self):
        self.refresh_coins_display()

    def apply_theme_instant(self):
        self.bg_color_instr.rgba = color_bg
        self.pad_color_instr.rgba = color_bg
        self.top_coins_color.rgba = color_key
        self.top_theme_color.rgba = color_key
        self.top_status_color.rgba = color_key

        self.lbl_title.color = color_text
        self.lbl_coins_title.color = color_text
        self.lbl_theme_title.color = color_text
        self.lbl_status_title.color = color_text
        self.lbl_coins_val.color = color_in_word
        self.lbl_theme_val.color = color_text

        self.btn_back.base_color = color_key
        self.btn_back.color = color_text
        self.btn_back.update_canvas()

        self.btn_action.base_color = color_key
        self.btn_action.color = color_text
        self.btn_action.disabled_color = color_text
        self.btn_action.update_canvas()
        self.btn_action_color.rgba = color_key

        self.btn_sell.base_color = color_key
        self.btn_sell.color = color_text
        self.btn_sell.disabled_color = color_not_in_word
        self.btn_sell.update_canvas()
        self.btn_sell_color.rgba = color_key

        for card in self.theme_cards.values():
            card.update_indicators()
        self.select_theme(self.selected_theme_id)

    def refresh_coins_display(self):
        global MOBILE_PLAYER_STATS
        if 'MOBILE_PLAYER_STATS' in globals() and isinstance(MOBILE_PLAYER_STATS, dict) and 'player_coins' in MOBILE_PLAYER_STATS:
            self.lbl_coins_val.text = str(MOBILE_PLAYER_STATS['player_coins'])
        else:
            self.lbl_coins_val.text = "0"

    def reposition_elements(self, instance, size):
        self.refresh_coins_display()
        win_w = self.width
        win_h = self.height
        
        self.bg_rect.size = (win_w, win_h)

        back_w, back_h = dp(92), dp(48)
        self.btn_back.size = (back_w, back_h)
        self.btn_back.pos = (win_w - back_w - dp(14), win_h - TOP_SAFE_MARGIN - back_h)
        fit_font_size(self.btn_back, back_w - dp(18), back_h * 0.42)

        title_h = min(win_h * 0.05, dp(34))
        fit_font_size(self.lbl_title, win_w - back_w - dp(45), title_h * 0.85)
        self.lbl_title.size = (win_w - back_w - dp(45), title_h)
        self.lbl_title.text_size = self.lbl_title.size
        self.lbl_title.pos = (dp(15), win_h - TOP_SAFE_MARGIN - back_h / 2 - title_h / 2 + dp(4))
        
        top_pad_h = win_h * 0.12
        header_bottom = self.btn_back.y - dp(10)
        top_pad_y = header_bottom - top_pad_h
        self.top_pad_rect.size = (win_w, top_pad_h)
        self.top_pad_rect.pos = (0, top_pad_y)
        
        bottom_pad_h = win_h * 0.12
        self.bottom_pad_rect.size = (win_w, bottom_pad_h)
        self.bottom_pad_rect.pos = (0, BOTTOM_SAFE_MARGIN)
        
        block_w = (win_w - 40) / 3
        block_h = top_pad_h - 20
        block_y = top_pad_y + 10
        
        x_coins = 10
        x_theme = 10 + block_w + 10
        x_status = 10 + block_w + 10 + block_w + 10
        
        self.block_coins_rect.size = (block_w, block_h)
        self.block_coins_rect.pos = (x_coins, block_y)
        
        self.block_theme_rect.size = (block_w, block_h)
        self.block_theme_rect.pos = (x_theme, block_y)
        
        self.block_status_rect.size = (block_w, block_h)
        self.block_status_rect.pos = (x_status, block_y)
        
        row_h = block_h / 2
        lbl_size = (block_w, row_h)
        
        y_titles = block_y + row_h
        self.lbl_coins_title.size = lbl_size
        self.lbl_coins_title.pos = (x_coins, y_titles)
        self.lbl_theme_title.size = lbl_size
        self.lbl_theme_title.pos = (x_theme, y_titles)
        self.lbl_status_title.size = lbl_size
        self.lbl_status_title.pos = (x_status, y_titles)
        
        y_vals = block_y
        self.lbl_coins_val.size = lbl_size
        self.lbl_coins_val.pos = (x_coins, y_vals)
        self.lbl_theme_val.size = lbl_size
        self.lbl_theme_val.pos = (x_theme, y_vals)
        self.lbl_status_val.size = lbl_size
        self.lbl_status_val.pos = (x_status, y_vals)

        btn_w = (win_w - 30) / 2
        btn_h = bottom_pad_h - 20
        btn_y = BOTTOM_SAFE_MARGIN + dp(10)

        self.btn_action.size = (btn_w, btn_h)
        self.btn_action.pos = (10, btn_y)
        fit_font_size(self.btn_action, btn_w - dp(20), btn_h * 0.36)

        self.btn_sell.size = (btn_w, btn_h)
        self.btn_sell.pos = (10 + btn_w + 10, btn_y)
        fit_font_size(self.btn_sell, btn_w - dp(20), btn_h * 0.36)

        self.rect_action.pos = self.btn_action.pos
        self.rect_action.size = self.btn_action.size

        self.rect_sell.pos = self.btn_sell.pos
        self.rect_sell.size = self.btn_sell.size

        scroll_top = top_pad_y - 15
        scroll_bottom = bottom_pad_h + BOTTOM_SAFE_MARGIN + dp(15)
        scroll_h = scroll_top - scroll_bottom
        self.scroll_view.size = (win_w, scroll_h)
        self.scroll_view.pos = (0, scroll_bottom)

        for card in self.scroll_content.children:
            card.size = (win_w - 30, min(win_w * 0.42, dp(150)))

    def select_theme(self, theme_id):
        global MOBILE_PLAYER_STATS
        self.selected_theme_id = theme_id

        for t_id, card in self.theme_cards.items():
            new_selected = (t_id == theme_id)
            if card.is_selected != new_selected:
                card.is_selected = new_selected
                card.update_indicators()

        theme_data = color_themes[theme_id]
        self.lbl_theme_val.text = theme_data.get("color_name", theme_id.capitalize())

        unlocked_themes = MOBILE_PLAYER_STATS.get("unlocked_themes", {"classic": True})
        is_unlocked = unlocked_themes.get(theme_id, False)

        if theme_id in ['classic', 'night'] or theme_data.get("price", 0) == 0:
            is_unlocked = True

        if is_unlocked:
            if self.theme_cards[theme_id].is_active:
                self.lbl_status_val.text = "Применено"
                self.lbl_status_val.color = color_correct
            else:
                self.lbl_status_val.text = "Куплено"
                self.lbl_status_val.color = color_text
        else:
            price = theme_data.get('price', 1000)
            self.lbl_status_val.text = f"{price} мон."
            self.lbl_status_val.color = color_in_word

        if is_unlocked:
            if self.theme_cards[theme_id].is_active:
                self.btn_action.text = "ПРИМЕНЕНО"
                self.btn_action.disabled = True
            else:
                self.btn_action.text = "ПРИМЕНИТЬ"
                self.btn_action.disabled = False
        else:
            self.btn_action.text = "КУПИТЬ"
            self.btn_action.disabled = False

        if theme_id in ['classic', 'night']:
            self.btn_sell.disabled = True
        else:
            self.btn_sell.disabled = not is_unlocked

    def process_theme_action(self, instance):
        global MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC
        global color_bg, color_text, color_correct, color_in_word, color_not_in_word, color_blank, color_key
        
        theme_id = self.selected_theme_id
        theme_data = color_themes[theme_id]
        
        unlocked_themes = MOBILE_PLAYER_STATS.get("unlocked_themes", {"classic": True})
        is_unlocked = unlocked_themes.get(theme_id, False)
        
        if theme_id in ['classic', 'night'] or theme_data.get("price", 0) == 0:
            is_unlocked = True
            
        if is_unlocked:
            if self.theme_cards[theme_id].is_active:
                return  

            for t_id, card in self.theme_cards.items():
                if card.is_active:
                    card.is_active = False
                    card.update_indicators()
            self.theme_cards[theme_id].is_active = True
            self.theme_cards[theme_id].update_indicators()

            choose_theme(theme_id)

            color_bg = theme_data.get("color_bg", color_bg)
            color_text = theme_data.get("color_text", color_text)
            color_correct = theme_data.get("color_correct", color_correct)
            color_in_word = theme_data.get("color_in_word", color_in_word)
            color_not_in_word = theme_data.get("color_not_in_word", color_not_in_word)
            color_blank = theme_data.get("color_blank", color_blank)
            color_key = theme_data.get("color_key", color_key)

            self.reposition_elements(self, self.size)
            self.scroll_content.do_layout()
            
            if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
                MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)
            
            self.select_theme(theme_id)
            print(f"[MGGamesStudio] Тема {theme_id} успешно применена!")
        else:
            price = theme_data.get('price', 1000)
            current_coins = MOBILE_PLAYER_STATS.get('player_coins', 0)
            
            if current_coins >= price:
                MOBILE_PLAYER_STATS['player_coins'] = current_coins - price
                MOBILE_PLAYER_STATS['unlocked_themes'][theme_id] = True
                self.lbl_coins_val.text = str(MOBILE_PLAYER_STATS['player_coins'])
                
                for t_id, card in self.theme_cards.items():
                    if card.is_active:
                        card.is_active = False
                        card.update_indicators()

                self.theme_cards[theme_id].is_active = True
                self.theme_cards[theme_id].update_indicators()

                choose_theme(theme_id)

                color_bg = theme_data.get("color_bg", color_bg)
                color_text = theme_data.get("color_text", color_text)
                color_correct = theme_data.get("color_correct", color_correct)
                color_in_word = theme_data.get("color_in_word", color_in_word)
                color_not_in_word = theme_data.get("color_not_in_word", color_not_in_word)
                color_blank = theme_data.get("color_blank", color_blank)
                color_key = theme_data.get("color_key", color_key)

                self.btn_action.color = color_text
                self.btn_sell.color = color_text

                self.reposition_elements(self, self.size)
                self.scroll_content.do_layout()
                
                if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
                    MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)
                
                self.select_theme(theme_id)
                print(f"[MGGamesStudio] Тема {theme_id} успешно куплена, применена и сохранена!")

    def process_theme_sell(self, instance):
        global MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC
        global color_bg, color_text, color_correct, color_in_word, color_not_in_word, color_blank, color_key
        
        theme_id = self.selected_theme_id

        if theme_id in ['classic', 'night']:
            return
            
        current_coins = MOBILE_PLAYER_STATS.get('player_coins', 0)
        MOBILE_PLAYER_STATS['player_coins'] = current_coins + 900
        MOBILE_PLAYER_STATS['unlocked_themes'][theme_id] = False
        self.lbl_coins_val.text = str(MOBILE_PLAYER_STATS['player_coins'])

        if self.theme_cards[theme_id].is_active:
            self.theme_cards[theme_id].is_active = False
            self.theme_cards[theme_id].update_indicators()
            self.theme_cards['classic'].is_active = True
            self.theme_cards['classic'].update_indicators()

            choose_theme('classic')

            classic_data = color_themes['classic']
            color_bg = classic_data.get("color_bg")
            color_text = classic_data.get("color_text")
            color_correct = classic_data.get("color_correct")
            color_in_word = classic_data.get("color_in_word")
            color_not_in_word = classic_data.get("color_not_in_word")
            color_blank = classic_data.get("color_blank")
            color_key = classic_data.get("color_key")

            self.reposition_elements(self, self.size)
            self.scroll_content.do_layout()
            
        if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
            MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)
            
        self.select_theme(theme_id)
        print(f"[MGGamesStudio] Тема {theme_id} успешно продана за 900 монет и заблокирована!")

class QuestsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        self.stub_layout = create_stub_layout(self, "")
        self.layout.add_widget(self.stub_layout)
        
        self.lbl_main_title = Label(
            text="Квесты", 
            font_name=font_path("ClearSans-Bold.ttf"), 
            bold=True, 
            color=color_text,
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )
        self.layout.add_widget(self.lbl_main_title)
        
        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        self.top_overlay = FloatLayout(size_hint=(1, None))
        with self.top_overlay.canvas.before:
            Color(*color_bg)
            self.overlay_rect = RoundedRectangle(pos=(0, 0), size=(360, 200), radius=[0])
        self.layout.add_widget(self.top_overlay)

        if self.stub_layout.children:
            btn_list = [child for child in self.stub_layout.children if isinstance(child, MenuButton)]
            if btn_list:
                btn = btn_list[0]
                self.stub_layout.remove_widget(btn)
                self.layout.add_widget(btn)

        self.stats_scroll = ScrollView(size_hint=(1, None), do_scroll_x=True, do_scroll_y=False, bar_width=0)
        
        from kivy.effects.scroll import ScrollEffect
        self.stats_scroll.effect_cls = ScrollEffect

        self.stats_container = BoxLayout(orientation='vertical', spacing=8, size_hint=(None, None))

        self.stats_row1 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None))
        self.stats_row2 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None))

        self.stats_container.add_widget(self.stats_row1)
        self.stats_container.add_widget(self.stats_row2)
        self.stats_scroll.add_widget(self.stats_container)
        self.layout.add_widget(self.stats_scroll)

        self.scroll_view = ScrollView(size_hint=(1, None), do_scroll_x=False, do_scroll_y=True, bar_width=0)

        from kivy.effects.scroll import ScrollEffect
        self.scroll_view.effect_cls = ScrollEffect

        self.quests_list_layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[0, 10, 0, dp(20)])
        self.quests_list_layout.bind(minimum_height=self.quests_list_layout.setter('height'))

        self.scroll_view.add_widget(self.quests_list_layout)
        self.layout.add_widget(self.scroll_view)

        if hasattr(self, 'top_overlay'):
            self.layout.remove_widget(self.scroll_view)
            self.layout.add_widget(self.scroll_view, index=len(self.layout.children))

        self._quests_last_signature = None
        self._quests_build_event = None

        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def on_enter(self):
        self.refresh_quests_data()

    def refresh_quests_data(self):
        stats = MOBILE_PLAYER_STATS if ('MOBILE_PLAYER_STATS' in globals() and MOBILE_PLAYER_STATS) else {}
        launcher_quests = MOBILE_QUESTS if ('MOBILE_QUESTS' in globals() and MOBILE_QUESTS) else {}
        
        coins = stats.get("player_coins", 0)
        wins = stats.get("total_wins", 0)
        losses = stats.get("total_losses", 0)
        streak = f"{stats.get('current_win_streak', 0)}/{stats.get('max_win_streak', 0)}"
        
        done_count = sum(1 for q in launcher_quests.values() if q.get("done", False))
        quests_ratio = f"{done_count}/{len(launcher_quests)}" if launcher_quests else "0/5"
        signature = (
            coins, wins, losses, streak, quests_ratio,
            tuple(sorted((k, v.get("done", False), v.get("progress", 0)) for k, v in launcher_quests.items()))
        )
        if (signature == self._quests_last_signature
                and self.quests_list_layout.children
                and self._quests_build_event is None):
            return
        self._quests_last_signature = signature

        self.stats_row1.clear_widgets()
        self.stats_row2.clear_widgets()
        
        row1_data = [
            ("Монеты", str(coins), color_in_word),
            ("Победы", str(wins), color_correct),
            ("Поражения", str(losses), color_text)
        ]
        
        row2_data = [
            ("Серия побед", streak, color_text),
            ("Выполнено", quests_ratio, color_text)
        ]

        for item in row1_data:
            self.stats_row1.add_widget(self.create_card(*item))
            
        for item in row2_data:
            self.stats_row2.add_widget(self.create_card(*item))

        self.reposition_elements(None, None)
        self.build_quests_list(launcher_quests)

    def reposition_elements(self, instance, size):
        win_w = self.width
        win_h = self.height

        self.lbl_main_title.text = "Квесты"

        back_w, back_h = dp(92), dp(48)
        back_btn = None
        for child in self.layout.children:
            if isinstance(child, MenuButton):
                back_btn = child
                break
        if back_btn is not None:
            back_btn.size = (back_w, back_h)
            back_btn.pos = (win_w - back_w - dp(14), win_h - TOP_SAFE_MARGIN - back_h)
            fit_font_size(back_btn, back_w - dp(18), back_h * 0.42)

        title_h = min(win_h * 0.05, dp(34))
        self.lbl_main_title.text_size = (None, None)
        fit_font_size(self.lbl_main_title, win_w - back_w - dp(45), title_h * 0.85)
        self.lbl_main_title.size = (win_w - back_w - dp(45), title_h)
        self.lbl_main_title.text_size = self.lbl_main_title.size
        self.lbl_main_title.y = win_h - TOP_SAFE_MARGIN - back_h / 2 - title_h / 2 + dp(4)
        self.lbl_main_title.x = dp(15)

        overlay_height = min(win_h * 0.32, dp(230))
        if hasattr(self, 'top_overlay'):
            self.top_overlay.height = overlay_height
            self.top_overlay.pos = (0, win_h - overlay_height)
            self.overlay_rect.size = (win_w, overlay_height)
            self.overlay_rect.pos = (0, win_h - overlay_height)

        stats_h = dp(70) * 2 + dp(8)
        if hasattr(self, 'stats_scroll'):
            self.stats_scroll.height = stats_h
            self.stats_scroll.do_scroll_x = False
            header_bottom = (back_btn.y if back_btn is not None else win_h - TOP_SAFE_MARGIN - back_h) - dp(10)
            self.stats_scroll.pos = (0, header_bottom - stats_h)
            self.stats_container.size = (win_w, stats_h)
            self.stats_container.padding = [dp(12), 0, dp(12), 0]
            self.stats_container.spacing = dp(8)

            row_w = win_w - dp(24)
            self.stats_row1.size = (row_w, dp(70))
            self.stats_row2.size = (row_w, dp(70))
            self.stats_row1.spacing = dp(8)
            self.stats_row2.spacing = dp(8)

            for row in (self.stats_row1, self.stats_row2):
                n = max(len(row.children), 1)
                for card in row.children:
                    if hasattr(card, 'label_ref'):
                        fit_font_size(card.label_ref, row_w / n * 0.85, dp(15))
                        fit_font_size(card.value_ref, row_w / n * 0.85, dp(22))

        if hasattr(self, 'scroll_view'):
            list_top = self.stats_scroll.y - dp(10) if hasattr(self, 'stats_scroll') else win_h - overlay_height
            self.scroll_view.size = (win_w, list_top - BOTTOM_SAFE_MARGIN)
            self.scroll_view.pos = (0, BOTTOM_SAFE_MARGIN)
            self.quests_list_layout.width = win_w

        if hasattr(self, 'lbl_main_title') and self.lbl_main_title in self.layout.children:
            self.layout.remove_widget(self.lbl_main_title)
            self.layout.add_widget(self.lbl_main_title, index=0)

    def create_card(self, label_text, val_text, val_color):
        card = FloatLayout(size_hint=(1, 1))
        
        with card.canvas.before:
            Color(*color_blank)
            r_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
        card.bind(pos=lambda inst, v: setattr(r_rect, 'pos', inst.pos), 
                  size=lambda inst, v: setattr(r_rect, 'size', inst.size))
        
        lbl_lbl = Label(
            text=label_text, 
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_not_in_word,
            size_hint=(1, 0.45),
            pos_hint={'x': 0, 'y': 0.48},
            halign='center', 
            valign='middle'
        )
        card.add_widget(lbl_lbl)
        
        lbl_val = Label(
            text=val_text, 
            font_name=font_path("ClearSans-Bold.ttf"),
            color=val_color, 
            bold=True, 
            size_hint=(1, 0.5),
            pos_hint={'x': 0, 'y': 0.02},
            halign='center', 
            valign='middle'
        )
        card.add_widget(lbl_val)

        card.label_ref = lbl_lbl
        card.value_ref = lbl_val
        return card
    
    def create_quest_row(self, name, description, progress, goal, reward, is_done, quest_type="common"):
        row = FloatLayout(size_hint_y=None, height=110)
        
        def lerp_color(c1, c2, factor):
            return (
                c1[0] + (c2[0] - c1[0]) * factor,
                c1[1] + (c2[1] - c1[1]) * factor,
                c1[2] + (c2[2] - c1[2]) * factor,
                1.0
            )

        qt = quest_type.lower().strip()
        if qt == "common":
            rare_color = lerp_color(color_text, color_bg, 0.3)
            type_text = "Обычное"
        elif qt == "rare":
            rare_color = lerp_color(color_text, color_in_word, 0.5)
            type_text = "Редкое"
        elif qt == "epic":
            rare_color = lerp_color(color_text, color_correct, 0.6)
            type_text = "Эпическое"
        else:
            rare_color = lerp_color(color_text, color_bg, 0.3)
            type_text = "Обычное"

        if is_done:
            bg_color = color_blank
            text_color = color_text
            progress_color = color_correct
        else:
            bg_color = lerp_color(color_blank, color_bg, 0.5)
            text_color = lerp_color(color_text, color_bg, 0.4)
            rare_color = lerp_color(rare_color, color_bg, 0.3)
            progress_color = color_not_in_word

        with row.canvas.before:
            Color(*bg_color)
            bg_rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[12])
            Color(*rare_color)
            ribbon_rect = RoundedRectangle(pos=row.pos, size=(10, 110), radius=[(12, 12), (0, 0), (0, 0), (12, 12)])
            
        def sync_graphics(instance, value):
            bg_rect.pos = (instance.x + 15, instance.y)
            bg_rect.size = (instance.width - 30, instance.height)
            ribbon_rect.pos = (instance.x + 15, instance.y)
            ribbon_rect.size = (10, instance.height)
        row.bind(pos=sync_graphics, size=sync_graphics)

        return self.fill_quest_row_widgets(row, name, description, progress, goal, reward, text_color, progress_color, is_done, type_text, rare_color, bg_rect, ribbon_rect)

    def fill_quest_row_widgets(self, row, name, description, progress, goal, reward, text_color, progress_color, is_done, type_text, rarity_color, bg_rect, ribbon_rect):
        text_w = self.width - 45
        name_lbl = Label(
            text=name.upper(), font_name=font_path("ClearSans-Bold.ttf"),
            font_size='18sp', color=text_color, bold=True,
            size_hint=(None, None), width=text_w, text_size=(text_w, None),
            halign='left', valign='top'
        )
        desc_lbl = Label(
            text=description, font_name=font_path("ClearSans-Bold.ttf"),
            font_size='13sp', color=text_color,
            size_hint=(None, None), width=text_w, text_size=(text_w, None),
            halign='left', valign='top'
        )
        name_lbl.texture_update()
        desc_lbl.texture_update()
        info_h = dp(30)
        info_line = FloatLayout(size_hint=(1, None), height=info_h)
        seg_w = max((self.width - dp(24)) / 3, dp(60))
        lbl_rare = Label(
            text=type_text, font_name=font_path("ClearSans-Bold.ttf"),
            color=rarity_color, bold=True, size_hint=(None, None),
            size=(seg_w, info_h), pos_hint={'x': 0.06, 'center_y': 0.5},
            halign='left', valign='middle'
        )
        fit_font_size(lbl_rare, seg_w - dp(8), dp(13))
        lbl_rare.text_size = (seg_w, info_h)
        lbl_rew = Label(
            text=f"Награда: {reward}", font_name=font_path("ClearSans-Bold.ttf"),
            color=color_in_word, bold=True, size_hint=(None, None),
            size=(seg_w, info_h), pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center', valign='middle'
        )
        fit_font_size(lbl_rew, seg_w - dp(8), dp(13))
        lbl_rew.text_size = (seg_w, info_h)
        status_txt = "ВЫПОЛНЕНО" if is_done else f"{progress}/{goal}"
        lbl_stat = Label(
            text=status_txt, font_name=font_path("ClearSans-Bold.ttf"),
            color=progress_color, bold=True, size_hint=(None, None),
            size=(seg_w, info_h), pos_hint={'right': 0.97, 'center_y': 0.5},
            halign='right', valign='middle'
        )
        fit_font_size(lbl_stat, seg_w - dp(8), dp(14))
        lbl_stat.text_size = (seg_w, info_h)

        info_line.add_widget(lbl_rare)
        info_line.add_widget(lbl_rew)
        info_line.add_widget(lbl_stat)

        text_group = FloatLayout(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        text_group.add_widget(name_lbl)
        text_group.add_widget(desc_lbl)
        text_group.add_widget(info_line)

        def sync_row_height(*args):
            name_lbl.height = name_lbl.texture_size[1]
            desc_lbl.height = desc_lbl.texture_size[1]
            
            total_h = 4 + name_lbl.height + 2 + desc_lbl.height + 8 + info_line.height + 4
            
            row.height = max(75, total_h)
            ribbon_rect.size = (10, row.height)

            name_lbl.pos_hint = {'x': 0.06, 'top': 1.0 - (4 / row.height)}
            desc_lbl.pos_hint = {'x': 0.06, 'top': name_lbl.pos_hint['top'] - (name_lbl.height / row.height) - (2 / row.height)}
            info_line.pos_hint = {'x': 0, 'y': 4 / row.height}

        name_lbl.bind(texture_size=sync_row_height)
        desc_lbl.bind(texture_size=sync_row_height)
        row.bind(size=sync_row_height)
        sync_row_height()

        row.add_widget(text_group)
        return row

    def build_quests_list(self, launcher_quests):
        if self._quests_build_event is not None:
            self._quests_build_event.cancel()
            self._quests_build_event = None

        self.quests_list_layout.clear_widgets()

        if not launcher_quests:
            return

        all_keys = list(launcher_quests.keys())
        sorted_keys = sorted(all_keys, key=lambda k: launcher_quests[k].get("done", False), reverse=False)
        remaining = list(sorted_keys)

        def build_chunk(dt):
            ROWS_PER_FRAME = 4
            for _ in range(ROWS_PER_FRAME):
                if not remaining:
                    self._quests_build_event = None
                    return False
                q_key = remaining.pop(0)
                q_data = launcher_quests[q_key]
                quest_row_widget = self.create_quest_row(
                    q_data.get("name", "Секретное задание"),
                    q_data.get("description", ""),
                    q_data.get("progress", 0),
                    q_data.get("goal", 1),
                    q_data.get("reward", 50),
                    q_data.get("done", False),
                    q_data.get("type", "common")
                )
                self.quests_list_layout.add_widget(quest_row_widget)
            return True
        if build_chunk(0):
            self._quests_build_event = Clock.schedule_interval(build_chunk, 0)

    def update_daily_quests_mobile(self):
        global MOBILE_PLAYER_STATS, MOBILE_QUESTS
        import time
        import copy

        current_time_struct = time.localtime()
        current_day = current_time_struct.tm_mday

        last_update_day = MOBILE_PLAYER_STATS.get("last_update_day", -1)

        if current_day == last_update_day and MOBILE_PLAYER_STATS.get("active_quests"):
            MOBILE_QUESTS = MOBILE_PLAYER_STATS["active_quests"]
            return

        print("[MGGamesStudio] Новый день по местному времени! Выбираем 5 случайных квестов...")

        full_base_quests = MOBILE_PLAYER_STATS.get("quests_dict", {})
        if not full_base_quests:
            return

        commons = [k for k, v in full_base_quests.items() if v.get("type", "common") == "common"]
        rares = [k for k, v in full_base_quests.items() if v.get("type", "common") == "rare"]
        epics = [k for k, v in full_base_quests.items() if v.get("type", "common") == "epic"]

        chosen_keys = random.sample(commons, 2) + random.sample(rares, 2) + random.sample(epics, 1)

        new_active_quests = {}
        for key in chosen_keys:
            new_active_quests[key] = copy.deepcopy(full_base_quests[key])
            new_active_quests[key]["progress"] = 0
            new_active_quests[key]["done"] = False

        MOBILE_PLAYER_STATS["active_quests"] = new_active_quests
        MOBILE_PLAYER_STATS["last_update_day"] = current_day
        MOBILE_QUESTS = new_active_quests

        if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
            MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)

def create_stub_layout(screen_instance, text):
    layout = FloatLayout()
    btn_back = MenuButton(
        text="Назад", 
        size_hint=(None, None), 
        size=(dp(92), dp(48))
    )
    btn_back.pos = (Window.width - dp(92) - dp(14), Window.height - TOP_SAFE_MARGIN - dp(48))
    btn_back.font_size = '20sp' 
    btn_back.bind(on_release=lambda x: setattr(screen_instance.manager, 'current', 'menu'))
    layout.add_widget(btn_back)
    layout.add_widget(Label(
        text=text, 
        font_name=font_path("ClearSans-Bold.ttf"), 
        font_size='32sp', 
        bold=True, 
        color=color_text,
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    ))
    return layout

class LoadingScreen(Screen):
    progress = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.icon_image = Image(
            source=resource_path("app_icon.png"),
            fit_mode="contain",
            size_hint=(None, None)
        )

        self.title_label = Label(
            text="Угадай Слово",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.subtitle_label = Label(
            text="от MGGamesStudio",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_correct,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.status_label = Label(
            text="Загрузка...",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_not_in_word,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )

        self.bar_bg = FloatLayout(size_hint=(None, None))
        with self.bar_bg.canvas.before:
            self.bar_bg_color = Color(*color_blank)
            self.bar_bg_rect = Rectangle()
        with self.bar_bg.canvas.after:
            self.bar_fill_color = Color(*color_not_in_word)
            self.bar_fill_rect = Rectangle()

        self.layout.add_widget(self.icon_image)
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.subtitle_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.bar_bg)
        self.add_widget(self.layout)

        self.bind(size=self.reposition_loading_elements, progress=self._update_bar_fill)
        self.reposition_loading_elements()
        Clock.schedule_once(lambda dt: self.reposition_loading_elements(), 0)

    def apply_theme_colors(self):
        self.title_label.color = color_text
        self.subtitle_label.color = color_correct
        self.status_label.color = color_not_in_word
        self.bar_bg_color.rgba = color_blank
        self.bar_fill_color.rgba = color_not_in_word

    def reposition_loading_elements(self, *args):
        win_w, win_h = self.width, self.height
        if win_w <= 0 or win_h <= 0:
            return

        icon_size = min(win_w * 0.32, dp(140))
        self.icon_image.size = (icon_size, icon_size)
        self.icon_image.center_x = win_w / 2
        self.icon_image.center_y = win_h * 0.58

        self.title_label.size = (win_w * 0.9, dp(50))
        self.title_label.center_x = win_w / 2
        self.title_label.y = self.icon_image.y - dp(56)
        fit_font_size(self.title_label, win_w * 0.88, dp(38))

        self.subtitle_label.size = (win_w * 0.9, dp(32))
        self.subtitle_label.center_x = win_w / 2
        self.subtitle_label.y = self.title_label.y - dp(38)
        fit_font_size(self.subtitle_label, win_w * 0.8, dp(22))

        bar_w = win_w * 0.86
        bar_h = dp(8)
        self.status_label.size = (win_w * 0.9, dp(30))
        self.status_label.center_x = win_w / 2
        self.status_label.y = BOTTOM_SAFE_MARGIN + dp(40)
        fit_font_size(self.status_label, win_w * 0.8, dp(24))

        self.bar_bg.size = (bar_w, bar_h)
        self.bar_bg.center_x = win_w / 2
        self.bar_bg.y = BOTTOM_SAFE_MARGIN + dp(16)
        self.bar_bg_rect.pos = self.bar_bg.pos
        self.bar_bg_rect.size = self.bar_bg.size

        self._update_bar_fill()

    def _update_bar_fill(self, *args):
        bar_w, bar_h = self.bar_bg.size
        self.bar_fill_rect.pos = self.bar_bg.pos
        self.bar_fill_rect.size = (bar_w * self.progress, bar_h)

    def set_progress(self, fraction, animate=True):
        fraction = max(0.0, min(1.0, fraction))
        Animation.cancel_all(self, 'progress')
        if animate:
            Animation(progress=fraction, duration=0.18, t='out_quad').start(self)
        else:
            self.progress = fraction

class MobileApp(App):
    def build(self):
        self.title = "Угадай Слово"
        self.icon = resource_path("app_icon.png")
        self.words_list = MOBILE_ALL_WORDS
        saved_theme = MOBILE_PLAYER_STATS.get("active_theme_name", "classic")
        theme_translator = {"классика": "classic", "ночь": "night", "океан": "ocean", "закат": "sunset", "сакура": "sakura", "лес": "forest", "король": "royal", "лава": "lava", "изумруд": "emerald", "конфета": "candy", "неон": "neon", "золото": "gold"}
        
        if isinstance(saved_theme, str):
            saved_theme = theme_translator.get(saved_theme.lower(), saved_theme.lower())

        choose_theme(saved_theme)
        Window.clearcolor = color_bg

        sm = ScreenManager(transition=NoTransition())

        self.loading_screen = LoadingScreen(name='loading')
        sm.add_widget(self.loading_screen)
        sm.current = 'loading'

        self._sm_ref = sm
        self._screens_to_build = list(_SCREEN_FACTORIES.items())
        self._screens_total = len(self._screens_to_build)
        Clock.schedule_once(self._build_next_screens, 0)

        return sm

    def _build_next_screens(self, dt):
        chunk_size = 2
        for _ in range(chunk_size):
            if not self._screens_to_build:
                break
            name, factory = self._screens_to_build.pop(0)
            self._sm_ref.add_widget(factory())

        done = self._screens_total - len(self._screens_to_build)
        self.loading_screen.set_progress(done / self._screens_total)

        if self._screens_to_build:
            Clock.schedule_once(self._build_next_screens, 0)
        else:
            self._sm_ref.current = 'main'
            Clock.schedule_once(lambda dt: self._sm_ref.remove_widget(self.loading_screen), 0)

def start_mobile_game(words_list, player_stats, save_function):
    global MOBILE_ALL_WORDS, MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC, MOBILE_ACHIVEMENTS, MOBILE_QUESTS
    MOBILE_ALL_WORDS = words_list
    MOBILE_PLAYER_STATS = player_stats
    MOBILE_SAVE_FUNC = save_function

    if "achivements_dict" in player_stats and player_stats["achivements_dict"]:
        MOBILE_ACHIVEMENTS = player_stats["achivements_dict"]
    else:
        MOBILE_ACHIVEMENTS = player_stats.get("unlocked_achivements", {})
        
    if "quests_dict" in player_stats and player_stats["quests_dict"]:
        MOBILE_QUESTS = player_stats["quests_dict"]
    else:
        MOBILE_QUESTS = player_stats.get("active_quests", {})
        
    print(f"[MGGamesStudio] Достижений {len(MOBILE_ACHIVEMENTS)}, квестов {len(MOBILE_QUESTS)}.")
    MobileApp().run()

ALL_WORDS = load_words_list()
PLAYER_STATS = load_game_progress()

print(f"[MGGamesStudio] Успешно загружено уникальных слов: {len(ALL_WORDS)}")

START_MOBILE = True

if START_MOBILE:
    os.environ["MGGAMES_MODE"] = "mobile"
    print("[MGGamesStudio] ЗАПУСК МОБИЛЬНОЙ ВЕРСИИ ИГРЫ")
    
    try:
        saved_ach = PLAYER_STATS.get("unlocked_achivements", {})
        if saved_ach:
            for ach_key, saved_data in saved_ach.items():
                if ach_key in achivements:
                    achivements[ach_key]["got"] = saved_data.get("got", False)
                    achivements[ach_key]["date"] = saved_data.get("date", "")

        import time
        import copy
        
        current_time_struct = time.localtime()
        current_day = current_time_struct.tm_mday
        
        last_update_day = PLAYER_STATS.get("last_update_day", -1)
        saved_quests = PLAYER_STATS.get("active_quests", {})

        if current_day != last_update_day or not saved_quests:
            print("[MGGamesStudio] Чистый старт или новый день! Генерируем 5 квестов...")
            
            commons = [k for k, v in all_quests.items() if v.get("type", "common") == "common"]
            rares = [k for k, v in all_quests.items() if v.get("type", "common") == "rare"]
            epics = [k for k, v in all_quests.items() if v.get("type", "common") == "epic"]

            if len(commons) >= 2 and len(rares) >= 2 and len(epics) >= 1:
                chosen_keys = random.sample(commons, 2) + random.sample(rares, 2) + random.sample(epics, 1)
            else:
                chosen_keys = list(all_quests.keys())[:5]
            
            new_active_quests = {}
            for key in chosen_keys:
                new_active_quests[key] = copy.deepcopy(all_quests[key])
                new_active_quests[key]["progress"] = 0
                new_active_quests[key]["done"] = False
                
            PLAYER_STATS["active_quests"] = new_active_quests
            PLAYER_STATS["last_update_day"] = current_day
            save_game_progress(PLAYER_STATS)
            saved_quests = new_active_quests
        else:
            for q_key, saved_data in saved_quests.items():
                if q_key in all_quests:
                    all_quests[q_key]["progress"] = saved_data.get("progress", 0)
                    all_quests[q_key]["done"] = saved_data.get("done", False)

        filtered_mobile_quests = {}
        for q_key, q_val in all_quests.items():
            if q_key in saved_quests:
                filtered_mobile_quests[q_key] = q_val

        PLAYER_STATS["achivements_dict"] = achivements
        PLAYER_STATS["quests_dict"] = filtered_mobile_quests
        
        start_mobile_game(ALL_WORDS, PLAYER_STATS, save_game_progress)
    except Exception as e:
        print(f"[MGGamesStudio] Ошибка при запуске мобильной версии игры: {e}")
else:
    pass