import os
import sys
import json
import random
import re
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


class SharpScrollView(ScrollView):
    """
    Обычный ScrollView сдвигает своё содержимое через self.g_translate -
    отдельный Translate в canvas, а не через смену pos у детей (в исходниках
    Kivy это буквально `self.g_translate.xy = x, y`, БЕЗ округления). x и y -
    это scroll_x/scroll_y * размер прокручиваемой области, то есть почти
    всегда нецелые пиксели. GPU в итоге рисует уже готовый (целочисленно
    отрисованный) текст со сдвигом на дробную долю пикселя - отсюда
    размытие текста при прокрутке/перелистывании, даже если позиции самих
    лейблов внутри уже округлены.
    Здесь после стандартного пересчёта просто округляем сам сдвиг - тот же
    приём, что и в других местах этого файла (round() на финальных
    пиксельных координатах), только на уровне ScrollView, а не лейбла.
    """
    def update_from_scroll(self, *largs):
        super().update_from_scroll(*largs)
        x, y = self.g_translate.xy
        self.g_translate.xy = (round(x), round(y))


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

try:
    from kivy.graphics import Color, RoundedRectangle, Rectangle, BoxShadow
    _BOX_SHADOW_AVAILABLE = True
except ImportError:
    # BoxShadow появился в Kivy 2.2.0 - на более старой версии просто
    # отключаем настоящую тень вместо падения всего приложения при старте.
    from kivy.graphics import Color, RoundedRectangle, Rectangle
    BoxShadow = None
    _BOX_SHADOW_AVAILABLE = False
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture

_ICON_TEXTURE_CACHE = {}
_MISSING_ICON_TEXTURE = None

def _get_missing_icon_texture():
    """1x1 прозрачная текстура-заглушка, чтобы отсутствующая/битая иконка
    просто не отображалась, а не роняла всё приложение."""
    global _MISSING_ICON_TEXTURE
    if _MISSING_ICON_TEXTURE is None:
        _MISSING_ICON_TEXTURE = Texture.create(size=(1, 1), colorfmt='rgba')
        _MISSING_ICON_TEXTURE.blit_buffer(bytes([0, 0, 0, 0]), colorfmt='rgba', bufferfmt='ubyte')
    return _MISSING_ICON_TEXTURE

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

    ВАЖНО: если файл иконки отсутствует, не читается или имя не совпадает
    по регистру (частая причина падений именно на Android, где файловая
    система чувствительна к регистру, в отличие от Windows) - функция
    больше НЕ роняет всё приложение, а возвращает прозрачную заглушку и
    печатает путь к проблемному файлу в лог, чтобы его было легко найти.
    """
    if path in _ICON_TEXTURE_CACHE:
        return _ICON_TEXTURE_CACHE[path]

    try:
        core_img = CoreImage(path)
        src_tex = core_img.texture

        if src_tex.colorfmt != 'rgba':
            # No alpha channel to preserve shape by - nothing safe to do,
            # just reuse the texture as-is.
            _ICON_TEXTURE_CACHE[path] = src_tex
            return src_tex

        pixels = bytearray(src_tex.pixels)
        # Раньше тут был питоновский цикл по каждому пикселю (на большой иконке
        # это сотни тысяч итераций на старте). Срезы с шагом 4 делают то же в C.
        _n = len(pixels) // 4
        _white = b'\xff' * _n
        pixels[0::4] = _white  # R
        pixels[1::4] = _white  # G
        pixels[2::4] = _white  # B
        # alpha остаётся нетронутой - сохраняет форму глифа

        new_tex = Texture.create(size=src_tex.size, colorfmt='rgba')
        new_tex.blit_buffer(bytes(pixels), colorfmt='rgba', bufferfmt='ubyte')
        new_tex.flip_vertical()
        _ICON_TEXTURE_CACHE[path] = new_tex
        return new_tex
    except Exception as e:
        print(f"[MGGamesStudio] НЕ УДАЛОСЬ ЗАГРУЗИТЬ ИКОНКУ: {path} ({e})")
        fallback = _get_missing_icon_texture()
        _ICON_TEXTURE_CACHE[path] = fallback
        return fallback

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

# ======================================================================
# СВОЯ ТЕМА: данные
# Тема "custom" - обычная запись в color_themes, поэтому choose_theme,
# сохранение active_theme_name и перекраска экранов работают без изменений.
# Владение хранится там же, где у остальных тем: unlocked_themes["custom"].
# Цвета и название игрока: MOBILE_PLAYER_STATS["custom_theme"] =
#   {"name": "...", "colors": {"color_bg": "#RRGGBB", ...}}
# ======================================================================
CUSTOM_THEME_ID = "custom"
CUSTOM_THEME_PRICE = 10000
CUSTOM_NAME_MAX = 16
CUSTOM_DEFAULT_NAME = "Моя тема"
CUSTOM_SLOTS = [
    ("color_bg", "Фон"),
    ("color_text", "Текст"),
    ("color_blank", "Пустая клетка"),
    ("color_correct", "Верная буква"),
    ("color_in_word", "Не на месте"),
    ("color_not_in_word", "Нет в слове"),
    ("color_key", "Клавиши"),
]
CUSTOM_DEFAULT_HEX = {
    "color_bg": "#F5F3FF",
    "color_text": "#2E1065",
    "color_blank": "#DDD6FE",
    "color_correct": "#7C3AED",
    "color_in_word": "#F59E0B",
    "color_not_in_word": "#94A3B8",
    "color_key": "#C4B5FD",
}


def hex_to_rgba(value):
    value = value.lstrip('#')
    return (int(value[0:2], 16) / 255.0, int(value[2:4], 16) / 255.0, int(value[4:6], 16) / 255.0, 1.0)


def rgba_to_hex(color):
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, int(round(c * 255)))) for c in color[:3]))


def _valid_hex(value):
    if not (isinstance(value, str) and len(value) == 7 and value[0] == '#'):
        return False
    try:
        int(value[1:], 16)
        return True
    except ValueError:
        return False


def get_custom_theme_data():
    """(название, {ключ: '#RRGGBB'}) из сохранения; недостающее/битое - значения по умолчанию."""
    stats = globals().get('MOBILE_PLAYER_STATS') or {}
    saved = stats.get("custom_theme") or {}
    saved_colors = saved.get("colors") or {}
    colors = {}
    for key, default in CUSTOM_DEFAULT_HEX.items():
        value = saved_colors.get(key)
        colors[key] = value.upper() if _valid_hex(value) else default
    name = saved.get("name")
    if not isinstance(name, str) or not name.strip():
        name = CUSTOM_DEFAULT_NAME
    return name.strip()[:CUSTOM_NAME_MAX], colors


def sync_custom_theme():
    """Пересобирает color_themes["custom"] из сохранения."""
    name, colors = get_custom_theme_data()
    entry = {"color_name": name, "price": CUSTOM_THEME_PRICE, "unlocked": False}
    for key, value in colors.items():
        entry[key] = hex_to_rgba(value)
    color_themes[CUSTOM_THEME_ID] = entry


def _rel_luminance(color):
    def lin(x):
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(color[0]) + 0.7152 * lin(color[1]) + 0.0722 * lin(color[2])


def contrast_ratio(c1, c2):
    l1, l2 = _rel_luminance(c1), _rel_luminance(c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


sync_custom_theme()

class BaseScreen(Screen):
    """
    Экран с НЕПРОЗРАЧНЫМ фоном (color_bg) под всем содержимым.

    Причина бага "снизу остаётся старый экран": ScreenManager с NoTransition
    убирает уходящий экран не мгновенно, а на СЛЕДУЮЩЕМ кадре. Пока кадр
    тяжёлый (на телефоне), старый экран просвечивает сквозь новый, потому что
    у большинства экранов не было собственного фона (фон давал только
    Window.clearcolor). Теперь каждый экран сам закрашивает себя полностью.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._base_bg_color = Color(*color_bg)
            self._base_bg_rect = Rectangle(pos=(0, 0), size=self.size)
        self.bind(size=self._sync_base_bg)

    def _sync_base_bg(self, *args):
        self._base_bg_rect.pos = (0, 0)
        self._base_bg_rect.size = self.size

    def refresh_base_bg(self):
        self._base_bg_color.rgba = color_bg


# Кэш подбора размера шрифта: (текст, шрифт, ширина, старт) -> итоговый размер.
# Без него каждый reposition заново по несколько раз рендерил текстуру в цикле.
_FIT_CACHE = {}

def fit_font_size(label, max_allowed_w, start_font_px):
    key = (label.text, label.font_name, bool(label.bold), round(float(max_allowed_w), 1), int(start_font_px))
    cached = _FIT_CACHE.get(key)
    if cached is not None:
        if (getattr(label, '_fit_done', None) == key
                and label.text_size == [None, None]
                and abs(label.font_size - cached) < 0.01):
            return
        label.text_size = (None, None)
        label.font_size = f"{cached}px"
        label.texture_update()
        label._fit_done = key
        return

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

    if len(_FIT_CACHE) > 3000:
        _FIT_CACHE.clear()
    _FIT_CACHE[key] = current_font
    label._fit_done = key

# ----- Центрирование глифа по реальным границам букв -----
# Label рисует текстуру строки целиком, вместе с запасом под выносные элементы
# (ascent/descent). Заглавные кириллические буквы стоят на базовой линии и не
# имеют выносных элементов, поэтому «середина текстуры» оказывается заметно
# ниже середины самой буквы (на скриншоте ~4% высоты плитки), а асимметричные
# буквы вроде «Л» ещё и немного съезжают по горизонтали. Чтобы поставить букву
# точно в центр плитки, мы находим реальные границы непрозрачных пикселей
# текстуры и выравниваем по ним.
_INK_CENTER_CACHE = {}
_ROWS_BOTTOM_FIRST = None


def _scan_ink(texture, threshold=24):
    """Границы непрозрачных пикселей текстуры: (x0, x1, row0, row1, h).
    x - колонки слева направо, row - индексы строк в порядке буфера
    texture.pixels (какая строка идёт первой - см. _rows_bottom_first)."""
    w, h = texture.size
    pix = texture.pixels
    if not pix or len(pix) < w * h * 4:
        return None
    alpha = pix[3::4]
    rows = [r for r in range(h) if max(alpha[r * w:(r + 1) * w]) > threshold]
    if not rows:
        return None
    cols = [c for c in range(w) if max(alpha[c::w]) > threshold]
    if not cols:
        return None
    return cols[0], cols[-1] + 1, rows[0], rows[-1] + 1, h


def _rows_bottom_first():
    """True, если первая строка texture.pixels - нижняя (как на экране).
    Порядок строк определяем на лету по точке: она стоит на базовой линии,
    то есть всегда в нижней половине текстуры строки."""
    global _ROWS_BOTTOM_FIRST
    if _ROWS_BOTTOM_FIRST is None:
        _ROWS_BOTTOM_FIRST = True
        try:
            probe = Label(text=".", font_name=font_path("ClearSans-Bold.ttf"),
                          font_size="48px", bold=True)
            probe.texture_update()
            scan = _scan_ink(probe.texture)
            if scan:
                _x0, _x1, r0, r1, h = scan
                _ROWS_BOTTOM_FIRST = ((r0 + r1) / 2.0) < (h / 2.0)
        except Exception:
            pass
    return _ROWS_BOTTOM_FIRST


def glyph_ink_center(label):
    """Центр видимой части текста лейбла в координатах его текстуры
    (от левого нижнего угла, как на экране). None - если измерить не вышло."""
    key = (label.text, label.font_name, label.font_size)
    if key in _INK_CENTER_CACHE:
        return _INK_CENTER_CACHE[key]
    result = None
    try:
        scan = _scan_ink(label.texture)
        if scan:
            x0, x1, r0, r1, h = scan
            if _rows_bottom_first():
                y0, y1 = r0, r1
            else:
                y0, y1 = h - r1, h - r0
            result = ((x0 + x1) / 2.0, (y0 + y1) / 2.0)
    except Exception:
        result = None
    if len(_INK_CENTER_CACHE) > 200:
        _INK_CENTER_CACHE.clear()
    _INK_CENTER_CACHE[key] = result
    return result


_CAP_OFFSET_CACHE = {}


def cap_ink_offset_y(font_px):
    """Насколько центр ЗАГЛАВНОЙ буквы выше центра строки лейбла (px).
    Заглавные буквы и цифры стоят на базовой линии без выносных элементов, поэтому
    при valign='middle' они выглядят смещёнными вниз. Меряем по эталону "Н" того же
    шрифта и размера - так все надписи (ПРОДАТЬ, КУПИТЬ, +900 ...) стоят на одной
    высоте, независимо от того, есть ли в слове буквы с хвостиками (Д, Р, у)."""
    key = round(float(font_px), 1)
    cached = _CAP_OFFSET_CACHE.get(key)
    if cached is not None:
        return cached
    off = 0.0
    try:
        probe = Label(text="Н", font_name=font_path("ClearSans-Bold.ttf"),
                      font_size=f"{key}px", bold=True)
        probe.texture_update()
        center = glyph_ink_center(probe)
        if center is not None:
            off = center[1] - probe.texture_size[1] / 2.0
    except Exception:
        off = 0.0
    if len(_CAP_OFFSET_CACHE) > 200:
        _CAP_OFFSET_CACHE.clear()
    _CAP_OFFSET_CACHE[key] = off
    return off


_FIT_WRAP_CACHE = {}

def fit_font_size_wrapped(label, max_allowed_w, max_allowed_h, start_font_px):
    key = (label.text, label.font_name, bool(label.bold), round(float(max_allowed_w), 1),
           round(float(max_allowed_h), 1), int(start_font_px))
    cached = _FIT_WRAP_CACHE.get(key)
    if cached is not None:
        label.text_size = (max_allowed_w, None)
        label.font_size = f"{cached}px"
        label.texture_update()
        return

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

    if len(_FIT_WRAP_CACHE) > 3000:
        _FIT_WRAP_CACHE.clear()
    _FIT_WRAP_CACHE[key] = current_font

def lerp_color(c1, c2, factor):
    """Плавная линейная интерполяция между двумя RGBA-цветами (0..1 каждый канал)."""
    return tuple(c1[i] + (c2[i] - c1[i]) * factor for i in range(4))

def prepare_layout_for_dynamic_sizes(container, child_widgets):
    container.size_hint_y = None
    for widget in child_widgets:
        widget.size_hint_y = None
        if widget.parent is None:
            container.add_widget(widget)

def position_header(title_label, back_btn, win_w, win_h):
    back_w, back_h = dp(48), dp(48)
    back_btn_y = win_h - TOP_SAFE_MARGIN - back_h
    back_btn.size = (back_w, back_h)
    back_btn.pos = (win_w - back_w - dp(14), back_btn_y)
    fit_font_size(back_btn, back_w - dp(18), back_h * 0.42)
    title_box_w = max(win_w - back_w - dp(14) - dp(15) - dp(10), dp(1))
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
    'whats_new': lambda: TextDocumentScreen(name='whats_new', title_text="Что нового", back_target='options', source_file="WHATS-NEW.txt"),
    'license': lambda: TextDocumentScreen(name='license', title_text="Лицензия", back_target='about', source_file="LICENSE.txt"),
    'third_party': lambda: TextDocumentScreen(name='third_party', title_text="Сторонние компоненты", back_target='about', source_file="THIRD-PARTY NOTICES.txt"),
    'about_game': lambda: TextDocumentScreen(name='about_game', title_text="О игре", back_target='about', source_file="README.txt"),
    'special_thanks': lambda: TextDocumentScreen(name='special_thanks', title_text="Особая благодарность", back_target='about', source_file="SPECIAL-THANKS.txt"),
    'how_to_play': lambda: HowToPlayScreen(name='how_to_play'),
    'achievements': lambda: AchievementsScreen(name='achievements'),
    'customization': lambda: CustomizationScreen(name='customization'),
    'theme_editor': lambda: ThemeEditorScreen(name='theme_editor'),
    'quests': lambda: QuestsScreen(name='quests'),
    'one_player_game': lambda: OnePlayerGameScreen(name='one_player_game'),
    'two_player_game': lambda: TwoPlayerGameScreen(name='two_player_game'),
    'seed_generation': lambda: SeedGenerationScreen(name='seed_generation'),
    'seed_create': lambda: SeedCreateScreen(name='seed_create'),
    'seed_enter': lambda: SeedEnterScreen(name='seed_enter'),
}

_THEME_VERSION = 0
_bg_rebuild_event = None
# экраны, на которых нельзя занимать кадры фоновой пересборкой
_BUSY_SCREENS = {'one_player_game', 'two_player_game', 'seed_create', 'seed_enter'}

def make_screen(name):
    """Создаёт экран и ставит на него метку текущей версии темы."""
    scr = _SCREEN_FACTORIES[name]()
    scr._theme_version = _THEME_VERSION
    return scr

def is_screen_stale(scr):
    return getattr(scr, '_theme_version', -1) != _THEME_VERSION

def refresh_screen_if_stale(sm, name):
    """Пересобирает экран, если он создан под старую тему. Текущий экран не трогает."""
    if name not in _SCREEN_FACTORIES or not sm.has_screen(name):
        return False
    old = sm.get_screen(name)
    if old is sm.current_screen or not is_screen_stale(old):
        return False
    new = make_screen(name)
    sm.remove_widget(old)
    sm.add_widget(new)
    return True

def _schedule_bg_rebuild(sm, delay=0.35):
    global _bg_rebuild_event
    if _bg_rebuild_event is not None:
        _bg_rebuild_event.cancel()
    _bg_rebuild_event = Clock.schedule_once(lambda dt: _bg_rebuild_step(sm), delay)

def _bg_rebuild_step(sm):
    """Один устаревший экран за шаг, с паузой между шагами."""
    global _bg_rebuild_event
    _bg_rebuild_event = None
    stale = [n for n in _SCREEN_FACTORIES
             if sm.has_screen(n)
             and sm.get_screen(n) is not sm.current_screen
             and is_screen_stale(sm.get_screen(n))]
    if not stale:
        return
    if sm.current in _BUSY_SCREENS:
        _schedule_bg_rebuild(sm, 1.0)   # не мешаем игре, подождём
        return
    if refresh_screen_if_stale(sm, stale[0]):
        # свежепересобранному экрану сразу готовим данные (списки), пока его никто не видит
        scr = sm.get_screen(stale[0])
        if hasattr(scr, 'prepare_in_background'):
            scr.prepare_in_background()
    _schedule_bg_rebuild(sm)

class ThemedScreenManager(ScreenManager):
    """
    1) Если пользователь перешёл на экран, который ещё не успел пересобраться
       в фоне после смены темы - пересобираем его прямо перед показом.
    2) Скрытые экраны сразу получают размер окна. Раньше экран, которого ещё
       ни разу не показывали, имел размер по умолчанию (100x100), и ВСЯ его
       раскладка (шрифты, карточки, текстуры) считалась в момент первого
       перехода на него - отсюда задержки при открытии экранов. Теперь это
       делается заранее (на загрузке или в фоне).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._presize_hidden_screens)

    def add_widget(self, widget, *args, **kwargs):
        super().add_widget(widget, *args, **kwargs)
        self._presize(widget)

    def _presize(self, scr):
        if scr.parent is not None:      # показанный экран раскладывает сам ScreenManager
            return
        w, h = self.size
        if w <= 1 or h <= 1:
            return
        if scr.width != w or scr.height != h:
            scr.size = (w, h)

    def _presize_hidden_screens(self, *args):
        for scr in list(self.screens):
            self._presize(scr)

    def on_current(self, instance, value):
        refresh_screen_if_stale(self, value)
        super().on_current(instance, value)


# ----- обновление статистики Достижений/Квестов в фоне -----
_stats_dirty_event = None

def mark_stats_dirty():
    """Вызывается при каждом сохранении прогресса: данные Достижений/Квестов
    изменились, значит их экраны надо обновить заранее, в фоне."""
    global _stats_dirty_event
    if _stats_dirty_event is not None:
        _stats_dirty_event.cancel()
    _stats_dirty_event = Clock.schedule_once(_refresh_stats_screens, 0.6)

def _refresh_stats_screens(dt):
    global _stats_dirty_event
    _stats_dirty_event = None
    app = App.get_running_app()
    if not app or not app.root:
        return
    sm = app.root
    if sm.current in _BUSY_SCREENS:
        # идёт игра - не отнимаем кадры, подождём
        _stats_dirty_event = Clock.schedule_once(_refresh_stats_screens, 1.0)
        return
    for name in ('achievements', 'quests'):
        if not sm.has_screen(name):
            continue
        scr = sm.get_screen(name)
        if scr is sm.current_screen or is_screen_stale(scr):
            continue
        if hasattr(scr, 'prepare_in_background'):
            scr.prepare_in_background()

def redraw_all_screens():
    global _THEME_VERSION
    from kivy.core.window import Window

    app = App.get_running_app()
    if not app or not app.root:
        return
    sm = app.root
    _THEME_VERSION += 1

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

    cur = sm.current_screen
    if cur is None or not hasattr(cur, 'apply_theme_instant'):
        _redraw_all_screens_full_rebuild(sm)
        return

    cur.apply_theme_instant()            # мгновенно, на месте
    if hasattr(cur, 'refresh_base_bg'):
        cur.refresh_base_bg()
    cur._theme_version = _THEME_VERSION  # этот экран уже актуален
    _schedule_bg_rebuild(sm, 0.6)        # остальные - потом, по одному

def _redraw_all_screens_full_rebuild(sm):
    """Запасной путь: полная пересборка (если текущий экран не умеет перекрашиваться на месте)."""
    from kivy.uix.screenmanager import NoTransition
    old_transition = sm.transition
    sm.transition = NoTransition()
    cur_name = sm.current
    sm.current = 'main'
    for screen in list(sm.screens):
        sm.remove_widget(screen)
    for name in _SCREEN_FACTORIES:
        sm.add_widget(make_screen(name))
    sm.current = cur_name if cur_name in _SCREEN_FACTORIES else 'main'
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

# ----- ПОДТВЕРЖДЕНИЕ ВЫХОДА ИЗ ИГРОВОГО РЕЖИМА -----

# Иконка-предупреждение (alert-circle.png) всегда красная - это универсальный
# сигнал "внимание", он не завязан на текущую цветовую тему оформления.
EXIT_ALERT_BADGE_COLOR = (254/255, 226/255, 226/255, 1.0)
EXIT_ALERT_ICON_COLOR = (185/255, 28/255, 28/255, 1.0)

def is_confirm_exit_enabled():
    """
    Читает настройку "Спрашивать о выходе из игры" (ключ confirm_exit).
    При самом первом запуске игры (пока сохранённых настроек ещё нет)
    настройка считается включённой по умолчанию.
    """
    if 'MOBILE_PLAYER_STATS' in globals() and MOBILE_PLAYER_STATS:
        saved_settings = MOBILE_PLAYER_STATS.get("settings", {})
        return saved_settings.get("confirm_exit", True)
    return True

class ExitConfirmButton(Button):
    """Простая прямоугольная кнопка со скруглёнными углами и затемнением
    при нажатии - используется в плашке подтверждения выхода."""

    def __init__(self, text="", base_color=None, text_color=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_name = font_path("ClearSans-Bold.ttf")
        self.font_size = '18sp'
        self.bold = True
        self.halign = 'center'
        self.valign = 'middle'

        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)

        self.base_color = base_color if base_color else color_key
        self.color = text_color if text_color else color_text

        with self.canvas.before:
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[14])

        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)

    def update_canvas(self, *args):
        if self.state == 'normal':
            self.bg_color_instr.rgba = self.base_color
        else:
            self.bg_color_instr.rgba = (self.base_color[0]*0.85, self.base_color[1]*0.85,
                                         self.base_color[2]*0.85, self.base_color[3])
        radius = min(self.height / 2.0, dp(14))
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.bg_rect.radius = [radius]
        # text_size сюда специально не пишем: раньше это заставляло текст
        # переноситься на вторую строку при нехватке ширины. Актуальный
        # text_size выставляется снаружи, в show_exit_confirm_popup, вместе
        # с подбором размера шрифта под фактическую ширину кнопки.

def show_exit_confirm_popup(on_confirm):
    """
    Показывает плашку "Вы точно хотите выйти?" со значком alert-circle,
    мелкой подписью про сброс игры и двумя кнопками - "Отмена" (просто
    закрывает плашку) и "Выйти" (закрывает плашку и вызывает on_confirm).
    """
    def _popup_width():
        # Ширина ограничена сверху фиксированным значением, чтобы на
        # широких/альбомных экранах кнопки не расходились слишком далеко.
        return min(Window.width * 0.82, dp(420))

    popup_width = _popup_width()
    # Высота плашки больше НЕ берётся долей от высоты окна - её вычисляет
    # _layout_popup() ниже, по фактически измеренному содержимому (значок +
    # заголовок + подпись + кнопки + отступы). Так гарантируется, что при
    # любом размере шрифта и на любом экране ничего не наедет друг на
    # друга - высоты просто неоткуда взяться "лишней" или "недостающей".
    # Здесь - только временная заглушка на первый кадр до первого расчёта.
    view = ModalView(size_hint=(None, None), size=(popup_width, dp(300)), auto_dismiss=True)
    view.background = ''
    view.background_color = (0, 0, 0, 0)
    view.overlay_color = (0, 0, 0, 0.5)

    box = FloatLayout()
    with box.canvas.before:
        Color(*color_bg)
        popup_rect = RoundedRectangle(pos=view.pos, size=view.size, radius=[dp(18)])

    def update_popup_bg(inst, value):
        popup_rect.pos = view.pos
        popup_rect.size = view.size
        popup_rect.radius = [min(dp(18), view.height * 0.08)]
    view.bind(pos=update_popup_bg, size=update_popup_bg)

    icon_badge = FloatLayout(size_hint=(None, None))
    with icon_badge.canvas.before:
        Color(*EXIT_ALERT_BADGE_COLOR)
        badge_ellipse = Ellipse(pos=icon_badge.pos, size=icon_badge.size)

    def update_badge(inst, value):
        badge_ellipse.pos = icon_badge.pos
        badge_ellipse.size = icon_badge.size
    icon_badge.bind(pos=update_badge, size=update_badge)

    icon_img = Image(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                      fit_mode="contain", color=EXIT_ALERT_ICON_COLOR)
    icon_img.texture = load_white_icon_texture(icon_path("alert-circle.png"))
    icon_badge.add_widget(icon_img)

    lbl_title = Label(text="Вы точно хотите выйти?", font_name=font_path("ClearSans-Bold.ttf"),
                      color=color_text, bold=True, halign='center', valign='middle',
                      size_hint=(1, None))

    lbl_msg = Label(text="При выходе игра сбрасывается.", font_name=font_path("ClearSans-Bold.ttf"),
                    color=color_not_in_word, bold=True, halign='center', valign='middle',
                    size_hint=(1, None))

    # Зазор и боковые отступы кнопок заданы в фиксированных dp (а не в
    # долях ширины плашки), поэтому на широких экранах кнопки не
    # расходятся слишком далеко друг от друга.
    btn_gap = dp(14)
    btn_side_margin = dp(20)
    btn_cancel = ExitConfirmButton(text="Отмена",
                                    base_color=lerp_color(color_bg, color_key, 0.35),
                                    text_color=color_text,
                                    size_hint=(None, None), pos_hint={'y': 0.08})
    btn_exit = ExitConfirmButton(text="Выйти",
                                  base_color=EXIT_ALERT_ICON_COLOR,
                                  text_color=(1.0, 1.0, 1.0, 1.0),
                                  size_hint=(None, None), pos_hint={'y': 0.08})

    def _on_cancel(instance):
        view.dismiss()

    def _on_confirm(instance):
        view.dismiss()
        if on_confirm:
            on_confirm()

    btn_cancel.bind(on_release=_on_cancel)
    btn_exit.bind(on_release=_on_confirm)

    for widget in (icon_badge, lbl_title, lbl_msg, btn_cancel, btn_exit):
        box.add_widget(widget)

    # Флаг защиты от рекурсии: внутри _layout_popup мы сами меняем
    # view.height, а на это событие подписан тот же _layout_popup (через
    # view.bind(size=...)). Флаг гарантирует, что повторный вызов,
    # вызванный этим изменением, ничего не делает и сразу выходит.
    _updating = [False]

    def _layout_popup(*args):
        if _updating[0]:
            return

        # box_w - это ЕДИНСТВЕННЫЙ вход в расчёт: высота плашки ниже сама
        # выводится из содержимого, а не наоборот. Раньше высота бралась
        # фиксированной долей от высоты окна, и при увеличении шрифта
        # текст переставал в неё помещаться - отсюда наезд подписи на
        # кнопки. Теперь такое невозможно в принципе: сколько места
        # реально заняли значок/заголовок/подпись/кнопки - столько плашка
        # и получит, плюс отступы.
        box_w = view.width if view.width > 1 else popup_width

        # Значок круглый и от ширины плашки, с разумными пределами, чтобы
        # не раздувался на планшетах и не сжимался в точку на мелких
        # экранах.
        badge_side = max(dp(60), min(box_w * 0.22, dp(88)))
        icon_badge.size = (badge_side, badge_side)
        icon_img.size = (badge_side * 0.52, badge_side * 0.52)

        fit_font_size(lbl_title, box_w * 0.9, min(box_w * 0.086, dp(30)))
        lbl_title.text_size = (box_w, None)
        lbl_title.texture_update()
        title_h = max(lbl_title.texture_size[1] * 1.25, dp(22))
        lbl_title.height = title_h
        lbl_title.text_size = (box_w, title_h)

        # Подпись - одна строка (fit_font_size, а не fit_font_size_wrapped):
        # при нехватке места шрифт уменьшается, а не переносится на строку.
        fit_font_size(lbl_msg, box_w * 0.86, min(box_w * 0.05, dp(17)))
        lbl_msg.text_size = (box_w, None)
        lbl_msg.texture_update()
        msg_h = max(lbl_msg.texture_size[1] * 1.25, dp(16))
        lbl_msg.height = msg_h
        lbl_msg.text_size = (box_w, msg_h)

        # Кнопки: высота фиксирована в dp (с небольшим запасом от ширины
        # плашки), а не долей от высоты - высоты у плашки на этом этапе
        # ещё толком нет, она вычисляется ниже как раз из этих величин.
        btn_h = max(dp(46), min(box_w * 0.145, dp(58)))
        margin_frac = btn_side_margin / box_w
        gap_frac = btn_gap / box_w
        btn_w_frac = max((1.0 - margin_frac * 2 - gap_frac) / 2.0, 0.05)
        for btn in (btn_cancel, btn_exit):
            btn.height = btn_h
        btn_cancel.size_hint = (btn_w_frac, None)
        btn_exit.size_hint = (btn_w_frac, None)

        btn_w_px = btn_w_frac * box_w
        for btn in (btn_cancel, btn_exit):
            btn.text_size = (None, None)
            fit_font_size(btn, btn_w_px - dp(16), btn_h * 0.42)
            btn.text_size = (btn_w_px, btn_h)

        # Отступы - фиксированные dp. pad_top и gap_badge_title специально
        # РАВНЫ друг другу: именно из-за того, что раньше это были разные
        # доли высоты плашки, значок визуально "плавал" не по центру между
        # верхним краем и заголовком.
        pad_top = dp(26)
        gap_badge_title = dp(26)
        gap_title_msg = dp(10)
        gap_msg_btn = dp(24)
        pad_bottom = dp(22)

        # Высота плашки = сумма ровно того, что реально заняло содержимое.
        # Совпадает с суммой отступов между элементами ниже, поэтому
        # раскладка сходится без зазоров и без наложений - по построению,
        # а не "обычно должно хватить места".
        content_h = (pad_top + badge_side + gap_badge_title + title_h +
                     gap_title_msg + msg_h + gap_msg_btn + btn_h + pad_bottom)
        target_h = max(min(content_h, Window.height * 0.85), dp(240))

        if abs(view.height - target_h) > 1:
            _updating[0] = True
            view.height = target_h
            _updating[0] = False
        box_h = view.height

        # Раскладка сверху вниз по РЕАЛЬНЫМ измеренным высотам - значок,
        # заголовок, подпись и кнопки больше не наезжают друг на друга при
        # любой длине текста, любом размере шрифта и любом экране.
        badge_top = box_h - pad_top
        icon_badge.pos_hint = {'center_x': 0.5, 'top': badge_top / box_h}

        title_top = badge_top - badge_side - gap_badge_title
        lbl_title.pos_hint = {'center_x': 0.5, 'top': title_top / box_h}

        msg_top = title_top - title_h - gap_title_msg
        lbl_msg.pos_hint = {'center_x': 0.5, 'top': msg_top / box_h}

        btn_y_frac = pad_bottom / box_h
        btn_cancel.pos_hint = {'x': margin_frac, 'y': btn_y_frac}
        btn_exit.pos_hint = {'right': 1.0 - margin_frac, 'y': btn_y_frac}

    view.bind(size=_layout_popup)
    _layout_popup()

    # Плашка пересчитывает раскладку (включая свою высоту, см. выше) при
    # изменении размера окна: поворот экрана, ресайз окна на десктопе и
    # т.п. Меняем только ширину - высоту _layout_popup выставит сама.
    def _on_window_resize(*args):
        view.width = _popup_width()
    Window.bind(size=_on_window_resize)
    view.bind(on_dismiss=lambda *a: Window.unbind(size=_on_window_resize))

    view.add_widget(box)
    view.open()

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

class IconMenuButton(MenuButton):
    def __init__(self, image_source="arrow-narrow-left.png", icon_ratio=0.6, **kwargs):
        super().__init__(text="", **kwargs)
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
        if hasattr(self, 'icon'):
            self.icon.color = self.color

class MainMenuButton(ButtonBehavior, FloatLayout):
    """
    Кнопка главного экрана: иконка слева (без цветного "чипа" под ней, просто
    тонированная в content_color иконка) и текст справа от неё, без шеврона.

    variant="primary"   -> заливка color_correct, текст/иконка белые (кнопка "Играть")
    variant="secondary" -> заливка - лёгкая смесь color_bg/color_key (как в "Меню"),
                            текст/иконка color_text

    Тень - настоящий blur через kivy.graphics.BoxShadow (не имитация слоями),
    всегда чёрная, расходится равномерно во все стороны (без сдвига вниз).
    """

    SHADOW_COLOR = (0, 0, 0, 0.22)
    SHADOW_BLUR_RADIUS = dp(12)
    SHADOW_SPREAD_RADIUS = (-dp(1), -dp(1))
    CARD_RADIUS = 20

    def __init__(self, text="", icon_name="", variant="secondary", **kwargs):
        super().__init__(**kwargs)

        self.variant = variant
        if variant == "primary":
            self.base_color = color_correct
            self.content_color = (1.0, 1.0, 1.0, 1.0)
        else:
            self.base_color = lerp_color(color_bg, color_key, 0.20)
            self.content_color = color_text

        with self.canvas.before:
            # настоящая мягкая тень под карточкой (реальный blur, не имитация слоями)
            # На Kivy < 2.2.0 (нет BoxShadow) тень просто отключается, без падения приложения
            self.shadow = None
            if _BOX_SHADOW_AVAILABLE:
                self.shadow_color_instr = Color(*self.SHADOW_COLOR)
                self.shadow = BoxShadow(
                    pos=self.pos,
                    size=self.size,
                    offset=(0, 0),  # без сдвига вниз - тень равномерная со всех сторон
                    blur_radius=self.SHADOW_BLUR_RADIUS,
                    spread_radius=self.SHADOW_SPREAD_RADIUS,
                    border_radius=(self.CARD_RADIUS,) * 4,
                )

            # заливка самой карточки
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.CARD_RADIUS])

        self.icon_img = Image(size_hint=(None, None), fit_mode="contain", color=self.content_color)
        if icon_name:
            self.icon_img.texture = load_white_icon_texture(icon_path(icon_name))
        self.add_widget(self.icon_img)

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            font_size='24sp',
            bold=True,
            color=self.content_color,
            halign='left',
            valign='middle',
            size_hint=(None, None),
        )
        self.add_widget(self.label)

        self.bind(pos=self._reposition, size=self._reposition, state=self._update_canvas)
        self._reposition()

    def _reposition(self, *args):
        w, h = self.width, self.height
        pad_side = h * 0.18

        if self.shadow is not None:
            self.shadow.pos = self.pos
            self.shadow.size = self.size

        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        icon_side = h * 0.34
        self.icon_img.size = (icon_side, icon_side)
        self.icon_img.center = (self.x + pad_side + icon_side / 2, self.y + h / 2)

        label_x = self.x + pad_side + icon_side + pad_side
        # небольшой сдвиг вверх компенсирует оптический "провис" текста ниже
        # геометрической середины карточки (эффект метрик жирного шрифта)
        label_w = max(self.x + w - pad_side - label_x, dp(10))
        self.label.pos = (label_x, self.y + dp(2))
        self.label.size = (label_w, h)
        self.label.text_size = (label_w, h)
        fit_font_size(self.label, label_w, h * 0.38)

    def _update_canvas(self, *args):
        if self.state == 'normal':
            self.bg_color_instr.rgba = self.base_color
        else:
            self.bg_color_instr.rgba = (
                self.base_color[0] * 0.94, self.base_color[1] * 0.94,
                self.base_color[2] * 0.94, self.base_color[3]
            )
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class TagChip(FloatLayout):
    """
    Маленькая заполненная плашка-чип для коротких подписей ("ОФФЛАЙН",
    "ОСНОВНОЙ РЕЖИМ"): фон color_key, текст color_text. Ширина сама
    подстраивается под фактическую ширину текста + отступы (тот же приём,
    что и в RarityBadge/FilterTabButton) - поэтому чип корректно выглядит
    на любом экране без единого захардкоженного px.
    """
    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)

        with self.canvas.before:
            self.bg_color_instr = Color(*color_key)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.add_widget(self.label)
        self.bind(pos=self._sync, size=self._sync)

    def update_size(self, height, font_scale=0.5, pad_scale=0.6):
        _k = (round(height, 2), font_scale, pad_scale, self.label.text)
        if _k == getattr(self, '_size_key', None):
            return
        self._size_key = _k
        self.height = height
        self.label.font_size = f"{max(int(height * font_scale), 10)}px"
        self.label.text_size = (None, None)
        self.label.texture_update()
        pad_x = height * pad_scale
        text_w = self.label.texture_size[0]
        self.width = text_w + pad_x * 2
        self.label.size = (text_w, height)
        self.label.text_size = (text_w, height)
        self._sync()

    def _sync(self, *args):
        pos = (round(self.x), round(self.y))
        size = (round(self.width), round(self.height))
        self.bg_rect.pos = pos
        self.bg_rect.size = size
        self.bg_rect.radius = [round(self.height / 2.0)]
        self.label.pos = pos
        self.label.size = size
        self.label.text_size = size

class ModeButton(ButtonBehavior, FloatLayout):
    """
    Карточка режима игры на экране выбора режима (PlayScreen).

    variant="featured" -> крупная карточка основного режима: плашка
                           (badge_text) прижата к верхнему левому углу и
                           слегка выступает за верхний край карточки.
    variant="compact"  -> компактная строка на всю ширину: иконка слева,
                           название + короткая подпись, шеврон справа.

    Фон карточки - lerp_color(color_bg, color_key, 0.20) (как в
    MenuRowButton), рамка - color_blank, квадрат-подложка иконки -
    color_key, весь текст/иконки - color_text, кроме описания
    (color_not_in_word). Нажатие слегка затемняет фон (тот же множитель
    0.94, что и в MenuRowButton/MainMenuButton).

    Внутренняя раскладка (позиции иконки/текста/шеврона/плашки) считается
    в layout_content() - PlayScreen лишь подбирает и проставляет размеры
    шрифтов/текстур title_label и sub_label (как и раньше), а сам виджет
    расставляет их по уже готовым размерам.
    """

    BORDER_W = dp(1.2)
    CARD_RADIUS = dp(16)

    def __init__(self, title_text="", description_text="", icon_name="",
                 variant="compact", badge_text=None, chevron_name="c-right.png",
                 on_release=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.variant = variant
        self.on_release_func = on_release

        self.base_color = lerp_color(color_bg, color_key, 0.20)

        with self.canvas.before:
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.CARD_RADIUS])
            self.border_color_instr = Color(*color_blank)
            self.border_line = Line(width=self.BORDER_W)

            self.chip_color_instr = Color(*color_key)
            self.chip_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(10)])

        self.icon_img = Image(size_hint=(None, None), fit_mode="contain", color=color_text)
        if icon_name:
            self.icon_img.texture = load_white_icon_texture(icon_path(icon_name))
        self.add_widget(self.icon_img)

        self.title_label = Label(
            text=title_text,
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            halign='left',
            valign='top',
            size_hint=(None, None)
        )
        self.add_widget(self.title_label)

        self.sub_label = Label(
            text=description_text,
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_not_in_word,
            halign='left',
            valign='top',
            size_hint=(None, None)
        )
        self.add_widget(self.sub_label)

        self.chevron_img = Image(size_hint=(None, None), fit_mode="contain", color=color_text)
        self.chevron_img.texture = load_white_icon_texture(icon_path(chevron_name))
        self.add_widget(self.chevron_img)

        self.badge = None
        if badge_text:
            self.badge = TagChip(text=badge_text)
            self.add_widget(self.badge)

        self.bind(pos=self._sync_canvas, size=self._sync_canvas, state=self._update_bg)

    def _update_bg(self, *args):
        if self.state == 'normal':
            self.bg_color_instr.rgba = self.base_color
        else:
            self.bg_color_instr.rgba = (
                self.base_color[0] * 0.94, self.base_color[1] * 0.94,
                self.base_color[2] * 0.94, self.base_color[3]
            )

    def _sync_canvas(self, *args):
        pos = (round(self.x), round(self.y))
        size = (round(self.width), round(self.height))
        self.bg_rect.pos = pos
        self.bg_rect.size = size
        # Line рисуется ПО ЦЕНТРУ заданного пути - сдвигаем путь внутрь на
        # половину толщины линии, чтобы обводка целиком помещалась внутри
        # pos/size (тот же приём, что и в create_stat_card/achievement card).
        half_w = self.BORDER_W / 2.0
        self.border_line.rounded_rectangle = (
            pos[0] + half_w, pos[1] + half_w,
            max(size[0] - self.BORDER_W, 0), max(size[1] - self.BORDER_W, 0),
            self.CARD_RADIUS, self.CARD_RADIUS, self.CARD_RADIUS, self.CARD_RADIUS
        )

    def on_release(self):
        if self.on_release_func:
            self.on_release_func(self)

    def layout_content(self, icon_side, chevron_side, pad_left, pad_right,
                        pad_bottom, gap_icon_text, title_gap):
        """
        Расставляет иконку (в цветном квадрате), заголовок, описание,
        шеврон и плашку (если есть) внутри уже выставленных self.pos/self.size.
        title_label/sub_label должны быть заранее посчитаны и выставлены
        (fit_font_size / fit_font_size_wrapped) снаружи, в PlayScreen.
        """
        text_block_h = self.title_label.height + title_gap + self.sub_label.height
        content_h = max(text_block_h, icon_side)
        content_center_y = self.y + pad_bottom + content_h / 2.0

        icon_x = self.x + pad_left
        icon_y = content_center_y - icon_side / 2.0
        self.chip_rect.pos = (round(icon_x), round(icon_y))
        self.chip_rect.size = (round(icon_side), round(icon_side))
        icon_inner = icon_side * 0.52
        self.icon_img.size = (icon_inner, icon_inner)
        self.icon_img.center = (icon_x + icon_side / 2.0, icon_y + icon_side / 2.0)

        chevron_x = self.x + self.width - pad_right - chevron_side
        self.chevron_img.size = (chevron_side, chevron_side)
        self.chevron_img.center = (chevron_x + chevron_side / 2.0, content_center_y)

        text_x = icon_x + icon_side + gap_icon_text
        text_top = content_center_y + text_block_h / 2.0
        self.title_label.pos = (round(text_x), round(text_top - self.title_label.height))
        self.sub_label.pos = (round(text_x), round(text_top - self.title_label.height - title_gap - self.sub_label.height))

        if self.badge is not None:
            badge_x = self.x + pad_left
            badge_y = self.top - self.badge.height * 0.6
            self.badge.pos = (round(badge_x), round(badge_y))

class GameCell(Label):
    # Радиус скругления всегда = этой доле от меньшей стороны клетки.
    # Значение подобрано по пиксельным замерам референсного скриншота
    # (там радиус ≈ 7px при клетке ≈159px, то есть ~4.5%).
    # Никакого фиксированного "потолка" в пикселях больше нет, поэтому
    # уголки масштабируются вместе с размером клетки и не раздуваются
    # на маленьких бланках (квадрат больше не превращается в кружок).
    CORNER_RATIO = 0.045

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
            init_radius = min(self.size[0], self.size[1]) * self.CORNER_RATIO
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[init_radius])

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
        corner_radius = min(self.width, self.height) * self.CORNER_RATIO
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
    """
    Карточка темы в сетке 2 в ряд: фон/рамка в стиле остальных экранов
    (lerp(color_bg, color_key, 0.20) + рамка color_blank), внутри -
    «окошко» с палитрой самой темы (5 плиток + 2 ряда мини-клавиш),
    ниже название и чип статуса: "ПРИМЕНЕНО" / "ОТКРЫТО" / монета + цена.
    Выбранная карточка - рамка color_text потолще.
    Все размеры считаются от ширины карточки (metrics), без фиксированных px.
    """
    CARD_RADIUS = dp(16)

    @staticmethod
    def metrics(w):
        pad = min(w * 0.05, dp(10))
        inner_w = w - 2 * pad
        ppad = inner_w * 0.055
        tgap = inner_w * 0.03
        tile = max((inner_w - 2 * ppad - 4 * tgap) / 5.0, 1.0)
        kgap = max(dp(2), inner_w * 0.012)
        key = max((inner_w - 2 * ppad - 9 * kgap) / 10.0, 1.0)
        prev_h = ppad * 1.2 + tile + ppad * 0.8 + key + kgap + key + ppad
        gap_a = pad * 1.1
        name_h = max(w * 0.10, dp(14))
        chip_h = min(max(w * 0.14, dp(22)), dp(26))
        gap_b = pad * 0.6
        h = pad + prev_h + gap_a + name_h + gap_b + chip_h + pad * 1.4
        return dict(pad=pad, inner_w=inner_w, ppad=ppad, tgap=tgap, tile=tile,
                    kgap=kgap, key=key, prev_h=prev_h, gap_a=gap_a,
                    name_h=name_h, chip_h=chip_h, gap_b=gap_b, h=h)

    def __init__(self, theme_id="classic", theme_data=None, on_click_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.theme_id = theme_id
        self.theme_data = theme_data or color_themes[theme_id]
        self.on_click_callback = on_click_callback
        self.is_selected = False
        self.is_active = False
        self.is_owned = True
        self.chip = None
        self._tile_ink = (0, 0)

        d = self.theme_data
        self.base_color = lerp_color(color_bg, color_key, 0.20)
        tile_colors = [d['color_blank'], d['color_correct'], d['color_in_word'],
                       d['color_not_in_word'], d['color_blank']]
        tile_text = [d['color_text'], (1, 1, 1, 1), (0, 0, 0, 1), (1, 1, 1, 1), d['color_text']]

        with self.canvas.before:
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.CARD_RADIUS])

        with self.canvas:
            Color(*d['color_bg'])
            self.preview_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(10)])
            self.tile_rects = []
            for col in tile_colors:
                Color(*col)
                self.tile_rects.append(RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(4)]))
            Color(*d['color_key'])
            self.key_rects = [RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(2)]) for _ in range(20)]

        with self.canvas.after:
            self.border_color_instr = Color(*color_blank)
            self.border_line = Line(width=dp(1.2))

        self.tile_labels = []
        for i in range(5):
            lbl = Label(text="А", font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                        color=tile_text[i], size_hint=(None, None), halign='center', valign='middle')
            self.tile_labels.append(lbl)
            self.add_widget(lbl)

        self.name_label = Label(text=d.get("color_name", theme_id), font_name=font_path("ClearSans-Bold.ttf"),
                                bold=True, color=color_text, size_hint=(None, None),
                                halign='left', valign='middle')
        self.add_widget(self.name_label)

        self.lock_icon = Image(size_hint=(None, None), fit_mode="contain", color=color_not_in_word)
        self.lock_icon.texture = load_white_icon_texture(icon_path("lock.png"))
        self.add_widget(self.lock_icon)

        self._rebuild_chip()
        self.bind(pos=self._relayout, size=self._relayout, state=self._update_bg)

    # ----- состояние -----
    def set_state(self, owned, active):
        changed = (owned != self.is_owned) or (active != self.is_active) or self.chip is None
        self.is_owned = owned
        self.is_active = active
        if changed:
            self._rebuild_chip()
        self.lock_icon.opacity = 0 if owned else 1
        self.update_indicators()
        self._relayout()

    def _rebuild_chip(self):
        if self.chip is not None:
            self.remove_widget(self.chip)
        if not self.is_owned:
            price = self.theme_data.get("price", 1000)
            self.chip = RewardBadge(text=str(price))
        elif self.is_active:
            self.chip = RarityBadge(dot_color=color_correct, text="ПРИМЕНЕНО", filled=True)
        else:
            self.chip = RarityBadge(dot_color=color_not_in_word, text="ОТКРЫТО", filled=True)
        self.add_widget(self.chip)

    def update_indicators(self):
        if self.is_selected:
            self.border_color_instr.rgba = color_text
            self.border_line.width = dp(1.2)
        else:
            self.border_color_instr.rgba = color_blank
            self.border_line.width = dp(1.2)
        self._sync_border()

    def _sync_border(self):
        x0, y0 = round(self.x), round(self.y)
        w, h = round(self.width), round(self.height)
        half = self.border_line.width / 2.0
        r = self.CARD_RADIUS
        self.border_line.rounded_rectangle = (x0 + half, y0 + half, max(w - half * 2, 0),
                                              max(h - half * 2, 0), r, r, r, r)

    def _update_bg(self, *args):
        if self.state == 'normal':
            self.bg_color_instr.rgba = self.base_color
        else:
            c = self.base_color
            self.bg_color_instr.rgba = (c[0] * 0.94, c[1] * 0.94, c[2] * 0.94, c[3])

    def on_release(self):
        if self.on_click_callback:
            self.on_click_callback(self.theme_id)

    # ----- раскладка -----
    def _refit_fonts(self, m):
        """Тяжёлая часть (шрифты и измерение букв) - только при смене размера карточки."""
        tile = m['tile']
        for lbl in self.tile_labels:
            lbl.text_size = (None, None)
            lbl.font_size = f"{tile * 0.62}px"
            lbl.texture_update()
            lbl.size = lbl.texture_size
        first = self.tile_labels[0]
        center = glyph_ink_center(first) if first.texture is not None else None
        tw, th = first.texture_size
        # центр самой БУКВЫ (а не строки с запасом под выносные) - в центр плитки
        self._tile_ink = center if center is not None else (tw / 2.0, th / 2.0)

        name_h = m['name_h']
        lock_side = name_h * 0.9
        name_w = max(m['inner_w'] - lock_side - dp(6), dp(10))
        fit_font_size(self.name_label, name_w, name_h * 0.95)
        self.name_label.size = (name_w, name_h)
        self.name_label.text_size = (name_w, name_h)

    def _relayout(self, *args):
        w, h = self.width, self.height
        if w <= 1 or h <= 1:
            return
        m = self.metrics(w)
        x0, y0 = round(self.x), round(self.y)

        self.bg_rect.pos = (x0, y0)
        self.bg_rect.size = (round(w), round(h))
        self._sync_border()

        fkey = (round(w), round(h))
        if fkey != getattr(self, '_font_key', None):
            self._font_key = fkey
            self._refit_fonts(m)

        top = y0 + h - m['pad']
        prev_x = x0 + m['pad']
        prev_y = top - m['prev_h']
        self.preview_rect.pos = (round(prev_x), round(prev_y))
        self.preview_rect.size = (round(m['inner_w']), round(m['prev_h']))

        tile = m['tile']
        tile_y = top - m['ppad'] * 1.2 - tile
        ink_x, ink_y = self._tile_ink
        for i in range(5):
            tx = prev_x + m['ppad'] + i * (tile + m['tgap'])
            self.tile_rects[i].pos = (round(tx), round(tile_y))
            self.tile_rects[i].size = (round(tile), round(tile))
            self.tile_rects[i].radius = [tile * 0.2]
            self.tile_labels[i].pos = (round(tx + tile / 2.0 - ink_x),
                                       round(tile_y + tile / 2.0 - ink_y))

        key = m['key']
        row1_y = tile_y - m['ppad'] * 0.8 - key
        row2_y = row1_y - m['kgap'] - key
        for idx in range(20):
            row, col = divmod(idx, 10)
            kx = prev_x + m['ppad'] + col * (key + m['kgap'])
            ky = row1_y if row == 0 else row2_y
            self.key_rects[idx].pos = (round(kx), round(ky))
            self.key_rects[idx].size = (round(key), round(key))

        name_h = m['name_h']
        name_y = prev_y - m['gap_a'] - name_h
        lock_side = name_h * 0.9
        self.name_label.pos = (round(prev_x + dp(2)), round(name_y))
        self.lock_icon.size = (lock_side, lock_side)
        self.lock_icon.pos = (round(prev_x + m['inner_w'] - lock_side - dp(2)),
                              round(name_y + (name_h - lock_side) / 2.0))

        if self.chip is not None:
            self.chip.update_size(m['chip_h'], font_scale=0.5)
            chip_y = name_y - m['gap_b'] - m['chip_h']
            self.chip.pos = (round(prev_x + dp(2)), round(chip_y))


class ThemeActionButton(ButtonBehavior, FloatLayout):
    """
    Нижняя кнопка действия. Стили:
      primary   - заливка color_correct, белый текст (ПРИМЕНИТЬ / КУПИТЬ)
      secondary - карточка lerp(color_bg, color_key, 0.20), текст color_text (ПРОДАТЬ)
      done      - как secondary, но неактивна и с зелёной галочкой (ПРИМЕНЕНО)
      disabled  - как secondary, но приглушена (нельзя продать / не хватает монет)
    Справа от текста может стоять плашка с монетой и суммой (RewardBadge).
    Тень - тот же BoxShadow, что у MainMenuButton.
    """
    SHADOW_COLOR = (0, 0, 0, 0.22)
    SHADOW_BLUR_RADIUS = dp(12)
    SHADOW_SPREAD_RADIUS = (-dp(1), -dp(1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.on_release_func = None
        self._enabled = False
        self.icon_name = None
        self.pill = None
        self._bg_color = lerp_color(color_bg, color_key, 0.20)

        radius = dp(18)
        with self.canvas.before:
            self.shadow = None
            if _BOX_SHADOW_AVAILABLE:
                self.shadow_color_instr = Color(*self.SHADOW_COLOR)
                self.shadow = BoxShadow(pos=self.pos, size=self.size, offset=(0, 0),
                                        blur_radius=self.SHADOW_BLUR_RADIUS,
                                        spread_radius=self.SHADOW_SPREAD_RADIUS,
                                        border_radius=(radius,) * 4)
            self.bg_color_instr = Color(*self._bg_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])

        self.icon_img = Image(size_hint=(None, None), fit_mode="contain", color=color_text)
        self.add_widget(self.icon_img)
        self.label = Label(text="", font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                           color=color_text, size_hint=(None, None), halign='left', valign='middle')
        self.add_widget(self.label)

        self.bind(pos=self._reposition, size=self._reposition, state=self._update_canvas)

    def set_content(self, text, style, icon_name=None, pill_text=None, on_release=None):
        # Все цвета - только из текущей темы, никаких фиксированных значений и opacity:
        #   primary   - заливка color_correct, текст/иконка/плашка color_bg
        #   secondary - карточка (color_bg + color_key), текст color_text
        #   done      - как secondary, зелёная галочка color_correct
        #   disabled  - как secondary, но текст/иконка/монета color_not_in_word
        self.opacity = 1.0
        if style == "primary":
            self._bg_color = color_correct
            content = color_bg
            icon_color = content
        else:
            self._bg_color = lerp_color(color_bg, color_key, 0.20)
            content = color_not_in_word if style == "disabled" else color_text
            icon_color = color_correct if style == "done" else content

        self.on_release_func = on_release
        # ВАЖНО: НЕ используем Widget.disabled - Kivy выставляет его всем дочерним
        # Label, и они рисуются цветом disabled_color (белый, alpha 0.3) -> текст
        # "пропадает". Вместо этого свой флаг.
        self._enabled = (style in ("primary", "secondary")) and on_release is not None
        self.label.text = text
        self.label.color = content

        self.icon_name = icon_name
        if icon_name:
            self.icon_img.texture = load_white_icon_texture(icon_path(icon_name))
            self.icon_img.color = icon_color
            self.icon_img.opacity = 1
        else:
            self.icon_img.opacity = 0

        if self.pill is not None:
            self.remove_widget(self.pill)
            self.pill = None
        if pill_text:
            self.pill = RewardBadge(text=pill_text)
            if style == "primary":
                # на зелёной кнопке плашка полупрозрачная белая, как в макете
                self.pill.bg_color_instr.rgba = (color_bg[0], color_bg[1], color_bg[2], 0.24)
                self.pill.label.color = color_bg
                self.pill.icon.color = color_bg
            elif style == "disabled":
                self.pill.label.color = color_not_in_word
                self.pill.icon.color = color_not_in_word
            self.add_widget(self.pill)

        self._update_canvas()
        self._reposition()

    def on_release(self):
        if self._enabled and self.on_release_func:
            self.on_release_func(self)

    def _update_canvas(self, *args):
        c = self._bg_color
        k = 0.9 if (self.state == 'down' and self._enabled) else 1.0
        self.bg_color_instr.rgba = (c[0] * k, c[1] * k, c[2] * k, c[3])

    def _reposition(self, *args):
        w, h = self.width, self.height
        if w <= 1 or h <= 1:
            return
        pos = (round(self.x), round(self.y))
        size = (round(w), round(h))
        radius = min(dp(18), h / 2.0)
        if self.shadow is not None:
            self.shadow.pos = pos
            self.shadow.size = size
            self.shadow.border_radius = (radius,) * 4
        self.bg_rect.pos = pos
        self.bg_rect.size = size
        self.bg_rect.radius = [radius]

        pad = h * 0.20
        gap = h * 0.14
        icon_side = h * 0.34 if self.icon_name else 0
        pill_w = 0
        if self.pill is not None:
            self.pill.update_size(h * 0.42, font_scale=0.5)
            pill_w = self.pill.width
        max_label_w = w - pad * 2
        if icon_side:
            max_label_w -= icon_side + gap
        if pill_w:
            max_label_w -= pill_w + gap
        fit_font_size(self.label, max(max_label_w, dp(10)), h * 0.30)
        lw, lh = self.label.texture_size
        self.label.size = (lw, lh)
        self.label.text_size = (lw, lh)

        total = lw
        if icon_side:
            total += icon_side + gap
        if pill_w:
            total += pill_w + gap
        x = self.x + (w - total) / 2.0
        cy = self.y + h / 2.0

        if icon_side:
            self.icon_img.size = (icon_side, icon_side)
            self.icon_img.pos = (round(x), round(cy - icon_side / 2.0))
            x += icon_side + gap
        # центр ЗАГЛАВНОЙ буквы (а не строки с запасом под выносные) - на середину кнопки
        dy = cap_ink_offset_y(self.label.font_size)
        self.label.pos = (round(x), round(cy - lh / 2.0 - dy))
        x += lw + gap
        if self.pill is not None:
            self.pill.pos = (round(x), round(cy - self.pill.height / 2.0))


class LogoWordTiles(FloatLayout):
    """
    Ряд из 5 плиток логотипа "СЛОВО", раскрашенных так же, как игровые тайлы
    (зелёный/жёлтый/серый) - С зелёная, Л жёлтая, О серая, В зелёная, О серая.
    Цвета берутся из глобальных color_correct/color_in_word/color_not_in_word,
    поэтому ряд автоматически подстраивается под смену темы (экран
    пересоздаётся заново при смене темы).
    """

    LETTERS = ["С", "Л", "О", "В", "О"]
    SPREAD_RATIO = 0.20  # отступ между плитками = 20% от размера плитки
    TILE_RADIUS_RATIO = 0.20

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tile_bg_colors = [color_correct, color_in_word, color_not_in_word, color_correct, color_not_in_word]
        self.tile_color_instrs = []
        self.tile_rects = []
        self.labels = []

        with self.canvas:
            for col in self.tile_bg_colors:
                c = Color(*col)
                r = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[6])
                self.tile_color_instrs.append(c)
                self.tile_rects.append(r)

        for letter in self.LETTERS:
            lbl = Label(
                text=letter,
                font_name=font_path("ClearSans-Bold.ttf"),
                bold=True,
                color=(1.0, 1.0, 1.0, 1.0),
                halign='center',
                valign='middle',
                size_hint=(None, None),
            )
            self.labels.append(lbl)
            self.add_widget(lbl)

        self.bind(pos=self._reposition, size=self._reposition)
        self._reposition()

    def _reposition(self, *args):
        w, h = self.width, self.height
        n = len(self.LETTERS)
        if w <= 0 or h <= 0:
            return

        k = self.SPREAD_RATIO
        tile_by_w = w / (n + (n - 1) * k)
        tile_size = min(tile_by_w, h)
        spacing = tile_size * k
        total_w = tile_size * n + spacing * (n - 1)
        start_x = self.x + (w - total_w) / 2
        tile_y = self.y + (h - tile_size) / 2
        radius = tile_size * self.TILE_RADIUS_RATIO

        for i in range(n):
            tx = start_x + i * (tile_size + spacing)
            self.tile_rects[i].pos = (tx, tile_y)
            self.tile_rects[i].size = (tile_size, tile_size)
            self.tile_rects[i].radius = [radius]

            lbl = self.labels[i]
            fit_font_size(lbl, tile_size * 0.6, tile_size * 0.62)
            lbl.texture_update()
            center = glyph_ink_center(lbl) if lbl.texture is not None else None
            if center is not None:
                # Лейбл == его текстура (без text_size), текстура рисуется ровно
                # в lbl.pos. Ставим её так, чтобы центр самой БУКВЫ (а не центр
                # строки с запасом под выносные) совпал с центром плитки.
                lbl.text_size = (None, None)
                lbl.size = lbl.texture_size
                lbl.pos = (
                    round(tx + tile_size / 2.0 - center[0]),
                    round(tile_y + tile_size / 2.0 - center[1]),
                )
            else:
                # запасной вариант, если измерить пиксели не удалось
                lbl.pos = (tx, tile_y)
                lbl.size = (tile_size, tile_size)
                lbl.text_size = (tile_size, tile_size)

class MainScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.title_label = Label(
            text="УГАДАЙ",
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True, 
            color=color_text,
            size_hint=(None, None), 
            halign='center', 
            valign='middle'
        )

        self.logo_tiles = LogoWordTiles(size_hint=(None, None))

        self.buttons_container = BoxLayout(
            orientation='vertical', 
            size_hint=(None, None)
        )

        self.buttons = [
            MainMenuButton(text="Играть", icon_name="player-play.png", variant="primary"),
            MainMenuButton(text="Меню", icon_name="menu-2.png", variant="secondary"),
            MainMenuButton(text="Настройки", icon_name="settings.png", variant="secondary")
        ]

        self.buttons[0].bind(on_release=lambda x: setattr(self.manager, 'current', 'play'))
        self.buttons[1].bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.buttons[2].bind(on_release=lambda x: setattr(self.manager, 'current', 'options'))

        for btn in self.buttons:
            btn.size_hint = (1, None)
            self.buttons_container.add_widget(btn)

        self.copy_label = Label(
            text="Угадай слово by MGGamesStudio. v.1.2.0", 
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_not_in_word,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.logo_tiles)
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

        distance_to_top = top_limit - self.buttons_container.top
        gap = dp(10)
        title_h = min(distance_to_top * 0.42, dp(56))
        tiles_h = min(distance_to_top * 0.30, dp(46))
        content_h = title_h + gap + tiles_h
        content_bottom = self.buttons_container.top + (distance_to_top - content_h) / 2

        self.logo_tiles.size = (win_w * 0.68, tiles_h)
        self.logo_tiles.center_x = win_w / 2
        self.logo_tiles.y = content_bottom

        self.title_label.size = (win_w * 0.9, title_h)
        self.title_label.center_x = win_w / 2
        self.title_label.y = self.logo_tiles.top + gap
        fit_font_size(self.title_label, win_w * 0.9, title_h * 0.85)

class MenuRowButton(ButtonBehavior, FloatLayout):
    """
    Строка меню в стиле карточки: квадратная иконка слева (в цветном "чипе"),
    текст по центру-слева и шеврон ">" справа.

    Фон карточки — очень слабая смесь color_bg и color_key (небольшой уклон в
    сторону color_key, не чистый color_bg), а чип под иконкой — чистый color_key. Тень под
    карточкой — настоящая мягкая тень, нарисованная через kivy.graphics.BoxShadow
    (аппаратный gaussian blur, а не имитация стопкой полупрозрачных слоёв). Тень
    всегда чёрная и расходится равномерно во все стороны от карточки
    (offset = (0, 0), без сдвига вниз). Текст/иконка/шеврон = color_text.
    """

    # тень всегда чёрная (не зависит от цвета текста/темы)
    SHADOW_COLOR = (0, 0, 0, 0.22)
    # мягкость тени (радиус размытия) и равномерное распространение вокруг карточки
    SHADOW_BLUR_RADIUS = dp(12)
    SHADOW_SPREAD_RADIUS = (-dp(1), -dp(1))
    CARD_RADIUS = 18

    def __init__(self, text="", icon_name="", chevron_name="c-right.png", **kwargs):
        super().__init__(**kwargs)

        self.base_color = lerp_color(color_bg, color_key, 0.20)
        self.chip_color = color_key
        self.text_color = color_text

        with self.canvas.before:
            # настоящая мягкая тень под карточкой (реальный blur, не имитация слоями)
            # На Kivy < 2.2.0 (нет BoxShadow) тень просто отключается, без падения приложения
            self.shadow = None
            if _BOX_SHADOW_AVAILABLE:
                self.shadow_color_instr = Color(*self.SHADOW_COLOR)
                self.shadow = BoxShadow(
                    pos=self.pos,
                    size=self.size,
                    offset=(0, 0),  # без сдвига вниз - тень равномерная со всех сторон
                    blur_radius=self.SHADOW_BLUR_RADIUS,
                    spread_radius=self.SHADOW_SPREAD_RADIUS,
                    border_radius=(self.CARD_RADIUS,) * 4,
                )

            # заливка самой карточки
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[18])

            # "чип" под иконкой
            self.chip_color_instr = Color(*self.chip_color)
            self.chip_rect = RoundedRectangle(pos=self.pos, size=(0, 0), radius=[12])

        self.icon_img = Image(size_hint=(None, None), fit_mode="contain", color=self.text_color)
        if icon_name:
            self.icon_img.texture = load_white_icon_texture(icon_path(icon_name))
        self.add_widget(self.icon_img)

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            font_size='24sp',
            bold=True,
            color=self.text_color,
            halign='left',
            valign='middle',
            size_hint=(None, None),
        )
        self.add_widget(self.label)

        self.chevron_img = Image(size_hint=(None, None), fit_mode="contain", color=self.text_color)
        self.chevron_img.texture = load_white_icon_texture(icon_path(chevron_name))
        self.add_widget(self.chevron_img)

        self.bind(pos=self._reposition, size=self._reposition, state=self._update_canvas)
        self._reposition()

    def _reposition(self, *args):
        w, h = self.width, self.height
        pad_side = h * 0.16
        chip_side = h * 0.62

        if self.shadow is not None:
            self.shadow.pos = self.pos
            self.shadow.size = self.size

        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        chip_x = self.x + pad_side
        chip_y = self.y + (h - chip_side) / 2
        self.chip_rect.pos = (chip_x, chip_y)
        self.chip_rect.size = (chip_side, chip_side)

        icon_side = chip_side * 0.5
        self.icon_img.size = (icon_side, icon_side)
        self.icon_img.center = (chip_x + chip_side / 2, chip_y + chip_side / 2)

        chevron_side = h * 0.24
        self.chevron_img.size = (chevron_side, chevron_side)
        self.chevron_img.center = (self.x + w - pad_side - chevron_side / 2, self.y + h / 2)

        label_x = chip_x + chip_side + pad_side
        label_w = max(self.x + w - pad_side * 1.7 - chevron_side - label_x, dp(10))
        # небольшой сдвиг вверх компенсирует оптический "провис" текста ниже
        # геометрической середины карточки (эффект метрик жирного шрифта)
        self.label.pos = (label_x, self.y + dp(2))
        self.label.size = (label_w, h)
        self.label.text_size = (label_w, h)
        fit_font_size(self.label, label_w, h * 0.34)

    def _update_canvas(self, *args):
        if self.state == 'normal':
            self.bg_color_instr.rgba = self.base_color
        else:
            self.bg_color_instr.rgba = (
                self.base_color[0] * 0.94, self.base_color[1] * 0.94,
                self.base_color[2] * 0.94, self.base_color[3]
            )
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class MenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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
            MenuRowButton(text="Как играть", icon_name="question-mark.png"),
            MenuRowButton(text="Достижения", icon_name="trophy.png"),
            MenuRowButton(text="Кастомизация", icon_name="palette.png"),
            MenuRowButton(text="Квесты", icon_name="clipboard-text.png")
        ]
        for btn in self.buttons:
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
        spacing_h = dp(18)
        max_btn_h = dp(84)

        btn_h = (available_h - spacing_h * (total_elements - 1)) / total_elements
        btn_h = max(min(btn_h, max_btn_h), dp(44))
        container_h = btn_h * total_elements + spacing_h * (total_elements - 1)

        self.buttons_container.size = (container_w, container_h)
        self.buttons_container.spacing = spacing_h
        self.buttons_container.center_x = win_w / 2
        self.buttons_container.center_y = bottom_limit + available_h * 0.5

        for btn in self.buttons:
            btn.height = btn_h

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

class OptionsScreen(BaseScreen):
    settings_definitions = [
        {"type": "toggle", "key": "confirm_exit", "text": "Спрашивать о выходе из игры", "default": True},
        {"type": "link", "text": "О программе", "target": "about"},
        {"type": "link", "text": "Что нового", "target": "whats_new"}
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

class AboutScreen(BaseScreen):
    about_definitions = [
        {"type": "info", "text": "Версия игры", "value": "v.1.2.0"},
        {"type": "info", "text": "Автор", "value": "MGGamesStudio"},
        {"type": "link", "text": "Особая благодарность", "target": "special_thanks"},
        {"type": "link", "text": "Лицензия", "target": "license"},
        {"type": "link", "text": "Сторонние компоненты", "target": "third_party"},
        {"type": "link", "text": "О игре", "target": "about_game"}
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

class TextDocumentScreen(BaseScreen):
    def __init__(self, title_text="", back_target="about", source_file=None, **kwargs):
        super().__init__(**kwargs)
        self.back_target = back_target
        self.layout = FloatLayout()

        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

class PlayScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

        # маленький чип "ОФФЛАЙН" под заголовком (фон color_key, текст color_text)
        self.category_chip = TagChip(text="ОФФЛАЙН")
        self.layout.add_widget(self.category_chip)

        self.offline_modes = [
            {
                "title": "Одиночная игра",
                "description": "Одиночная оффлайн игра с монетами, достижениями и квестами.",
                "icon_name": "user.png",
                "variant": "featured",
                "badge_text": "ОСНОВНОЙ РЕЖИМ",
                "target_screen": "one_player_game",
            },
            {
                "title": "Игра вдвоём",
                "description": "Игра вдвоём за одним устройством.",
                "icon_name": "users.png",
                "variant": "compact",
                "badge_text": None,
                "target_screen": "two_player_game",
            },
            {
                "title": "Генерация сида",
                "description": "Введите сид или создайте сид, чтобы друг смог поиграть на другом устройстве.",
                "icon_name": "replace-user.png",
                "variant": "compact",
                "badge_text": None,
                "target_screen": "seed_generation",
            },
        ]

        self.mode_buttons = []
        for mode in self.offline_modes:
            card = ModeButton(
                title_text=mode["title"],
                description_text=mode["description"],
                icon_name=mode["icon_name"],
                variant=mode["variant"],
                badge_text=mode["badge_text"],
                on_release=self._make_mode_opener(mode["target_screen"])
            )
            self.mode_buttons.append(card)
            self.layout.add_widget(card)

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

        back_w, back_h = dp(48), dp(48)
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

        # "ОФФЛАЙН" - крупный, хорошо читаемый чип (только пропорции от
        # win_h + потолок dp(), без нижнего порога - чтобы честно ужимался
        # на маленьких окнах, а не оставался "статичным").
        chip_gap = min(win_h * 0.013, dp(10))
        chip_h = min(win_h * 0.034, dp(26))
        self.category_chip.update_size(chip_h, font_scale=0.62, pad_scale=0.62)
        self.category_chip.center_x = win_w / 2
        self.category_chip.top = self.title_label.y - chip_gap

        content_top = self.category_chip.y - min(win_h * 0.026, dp(20))
        bottom_limit = BOTTOM_SAFE_MARGIN
        footer_gap = min(win_h * 0.018, dp(14))
        cards_spacing = min(win_h * 0.013, dp(10))
        count = len(self.mode_buttons)
        card_w = win_w * 0.93

        # ----- ОДНИ и те же пропорции для всех трёх карточек: иконка-квадрат,
        # шеврон и внутренние отступы везде одного размера ("все блоки
        # одинакового размера"). Единственное отличие основной карточки -
        # плашка в углу и чуть больший верхний отступ под неё. Все величины
        # заданы как доля от card_w/win_h с потолком dp() и БЕЗ нижнего
        # порога, поэтому при сильном уменьшении окна всё ужимается
        # пропорционально и ничего не вылезает за карточку/экран.
        icon_side = min(card_w * 0.145, dp(56))
        chevron_side = min(card_w * 0.05, dp(18))
        pad_left = min(card_w * 0.045, dp(16))
        pad_right = min(card_w * 0.038, dp(14))
        gap_icon_text = min(card_w * 0.038, dp(14))
        extra_gap = min(card_w * 0.03, dp(10))
        pad_bottom = min(card_w * 0.035, dp(14))
        pad_top_base = min(card_w * 0.035, dp(14))
        title_gap = min(card_w * 0.017, dp(6))

        badge_h = min(win_h * 0.032, dp(26))
        badge_extra_top = badge_h * 0.55

        # Шрифты - тоже общие для всех карточек и заметно крупнее прежних,
        # чтобы текст было хорошо видно.
        desc_font_start = min(win_h * 0.024, dp(17))
        title_ratio = 1.45
        desc_h_cap = min(win_h * 0.11, dp(66))

        text_max_w = max(
            card_w - pad_left - icon_side - gap_icon_text - chevron_side - extra_gap - pad_right,
            dp(10)
        )

        def layout_cards(font_scale):
            heights = []
            for card in self.mode_buttons:
                fit_font_size_wrapped(card.sub_label, text_max_w, desc_h_cap, desc_font_start * font_scale)
                desc_real_h = card.sub_label.texture_size[1]
                card.sub_label.width = text_max_w
                card.sub_label.height = desc_real_h
                card.sub_label.text_size = (text_max_w, desc_real_h)

                title_target_font = card.sub_label.font_size * title_ratio
                fit_font_size(card.title_label, text_max_w, title_target_font)
                title_real_h = card.title_label.texture_size[1]
                card.title_label.width = text_max_w
                card.title_label.height = title_real_h
                card.title_label.text_size = (text_max_w, title_real_h)

                text_block_h = title_real_h + title_gap + desc_real_h
                content_h = max(text_block_h, icon_side)
                pad_top = pad_top_base + (badge_extra_top if card.badge is not None else 0)
                this_card_h = pad_top + content_h + pad_bottom
                heights.append(this_card_h)

            total_h = sum(heights) + cards_spacing * max(count - 1, 0)
            return heights, total_h

        heights, total_cards_h = layout_cards(1.0)

        footer_h_reserved = min(win_h * 0.018, dp(13))
        available_for_cards = content_top - bottom_limit - footer_h_reserved - footer_gap
        if count > 0 and total_cards_h > 0 and total_cards_h > available_for_cards:
            scale = max(available_for_cards / total_cards_h, 0.5)
            heights, total_cards_h = layout_cards(scale)

        y_cursor = content_top
        for card, this_card_h in zip(self.mode_buttons, heights):
            card.size = (card_w, this_card_h)
            card.pos = (win_w / 2 - card_w / 2, y_cursor - this_card_h)
            if card.badge is not None:
                card.badge.update_size(badge_h, font_scale=0.55, pad_scale=0.6)
            card.layout_content(
                icon_side=icon_side,
                chevron_side=chevron_side,
                pad_left=pad_left,
                pad_right=pad_right,
                pad_bottom=pad_bottom,
                gap_icon_text=gap_icon_text,
                title_gap=title_gap,
            )
            y_cursor -= this_card_h + cards_spacing

        last_card_bottom = (y_cursor + cards_spacing) if count > 0 else content_top

        desc_final_font_px = self.mode_buttons[-1].sub_label.font_size if self.mode_buttons else footer_h_reserved
        self.footer_label.text_size = (None, None)
        fit_font_size(self.footer_label, win_w * 0.85, desc_final_font_px)
        self.footer_label.size = self.footer_label.texture_size
        self.footer_label.center_x = win_w / 2
        self.footer_label.top = last_card_bottom - footer_gap


class OnePlayerGameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.lbl_error = Label(text="", font_name=font_path("ClearSans-Bold.ttf"),
                               font_size='15sp', color=color_in_word, bold=True, size_hint=(None, None))
        self.layout.add_widget(self.lbl_error)

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

        self.btn_exit_top = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

        self.btn_exit_top.size = (dp(48), dp(48))
        self.btn_exit_top.pos = (win_w - dp(48) - dp(14), win_h - TOP_SAFE_MARGIN - dp(48))
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

        space_below_cells = block_bottom_y - keyboard_top_y
        center_below_y = keyboard_top_y + (space_below_cells / 2)

        fit_font_size(self.lbl_error, win_w * 0.85, dp(16))
        self.lbl_error.text_size = (None, None)
        self.lbl_error.size = self.lbl_error.texture_size
        self.lbl_error.pos = (win_w // 2 - self.lbl_error.width // 2, center_below_y - self.lbl_error.height // 2)

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

                self.lbl_error.color = color_in_word
                self.lbl_error.text = "Такого слова нет в словаре!"
                self.reposition_elements(None, None)
        else:
            self.lbl_error.color = color_in_word
            self.lbl_error.text = "Слово не из 5 букв!"
            self.reposition_elements(None, None)

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
        if is_confirm_exit_enabled():
            show_exit_confirm_popup(lambda: self._do_exit(instance))
        else:
            self._do_exit(instance)

    def _do_exit(self, instance):
        self.reset_game()
        self.manager.current = 'play'

    def reset_game(self):
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
        view.background = ''
        view.background_color = (0, 0, 0, 0)
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
            view.bind(on_dismiss=lambda x: self._do_exit(None))
            
        view.open()

class TwoPlayerGameScreen(BaseScreen):
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

        self.btn_exit_top = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

        self.btn_exit_top.size = (dp(48), dp(48))
        self.btn_exit_top.pos = (win_w - dp(48) - dp(14), win_h - TOP_SAFE_MARGIN - dp(48))
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

            space_below_cells = block_bottom_y - keyboard_top_y
            center_below_y = keyboard_top_y + (space_below_cells / 2)

            fit_font_size(self.lbl_error, win_w * 0.85, dp(16))
            self.lbl_error.text_size = (None, None)
            self.lbl_error.size = self.lbl_error.texture_size
            self.lbl_error.pos = (win_w // 2 - self.lbl_error.width // 2, center_below_y - self.lbl_error.height // 2)

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
            self.lbl_error.color = color_in_word
            self.lbl_error.text = "Слово не из 5 букв!"
            self.reposition_elements(None, None)
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
            self.lbl_error.color = color_in_word
            self.lbl_error.text = "Такого слова нет в словаре!"
            self.reposition_elements(None, None)

    def press_exit_key(self, instance):
        if is_confirm_exit_enabled():
            show_exit_confirm_popup(lambda: self._do_exit(instance))
        else:
            self._do_exit(instance)

    def _do_exit(self, instance):
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
        view.background = ''
        view.background_color = (0, 0, 0, 0)
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
            view.bind(on_dismiss=lambda x: self._do_exit(None))
            
        view.open()

class SeedGenerationScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

        back_w, back_h = dp(48), dp(48)
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

class SeedCreateScreen(BaseScreen):
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

        self.btn_exit_top = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

        self.btn_exit_top.size = (dp(48), dp(48))
        self.btn_exit_top.pos = (win_w - dp(48) - dp(14), win_h - TOP_SAFE_MARGIN - dp(48))
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
        if is_confirm_exit_enabled():
            show_exit_confirm_popup(lambda: self._do_exit(instance))
        else:
            self._do_exit(instance)

    def _do_exit(self, instance):
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

class SeedEnterScreen(BaseScreen):
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

        self.btn_exit_top = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

        self.btn_exit_top.size = (dp(48), dp(48))
        self.btn_exit_top.pos = (win_w - dp(48) - dp(14), win_h - TOP_SAFE_MARGIN - dp(48))
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
        if is_confirm_exit_enabled():
            show_exit_confirm_popup(lambda: self._do_exit(instance))
        else:
            self._do_exit(instance)

    def _do_exit(self, instance):
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

class HowToPlayScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
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

        back_w, back_h = dp(48), dp(48)
        btn_y = win_h - TOP_SAFE_MARGIN - back_h
        self.btn_back.size = (back_w, back_h)
        self.btn_back.pos = (win_w - back_w - dp(14), btn_y)
        fit_font_size(self.btn_back, back_w - dp(18), back_h * 0.42)

        title_max_w = max(win_w - back_w - dp(14) - dp(15) - dp(10), dp(1))
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

class RarityBadge(FloatLayout):
    """
    Плашка редкости (в карточке достижения) и элемент легенды (без заливки).
    Сама плашка НЕ цветная - фон всегда color_key (или прозрачный для
    легенды), цвет несёт только точка внутри. Ширина считается от
    фактической ширины текста + отступов, поэтому плашка сама подстраивается
    под любой размер шрифта на любом экране (никаких фиксированных px).
    """
    def __init__(self, dot_color, text, filled=True, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.filled = filled
        self.dot_color = dot_color

        with self.canvas.before:
            self.bg_color_instr = Color(*(color_key if filled else (0, 0, 0, 0)))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
            self.dot_color_instr = Color(*dot_color)
            self.dot_ellipse = Ellipse(pos=(0, 0), size=(0, 0))

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )
        self.add_widget(self.label)
        self.bind(pos=self._sync_graphics, size=self._sync_graphics)

    def update_size(self, height, font_scale=0.52):
        _k = (round(height, 2), font_scale, self.label.text)
        if _k == getattr(self, '_size_key', None):
            return
        self._size_key = _k
        """Пересчитывает плашку под заданную высоту: шрифт - доля от высоты
        (увеличена, т.к. на маленькой высоте текст читался плохо), ширина -
        по фактической ширине получившегося текста + отступы."""
        self.height = height
        self.label.font_size = f"{max(int(height * font_scale), 12)}px"
        self._cap_dy = cap_ink_offset_y(max(int(height * font_scale), 12))
        self.label.text_size = (None, None)
        self.label.texture_update()
        dot_d = height * 0.32
        pad_x = height * (0.42 if self.filled else 0.0)
        gap = dp(6)
        text_w = self.label.texture_size[0]
        self.width = pad_x * 2 + dot_d + gap + text_w
        self.label.size = (text_w, height)
        # ВАЖНО: без text_size, равного size, halign/valign лейбла не
        # применяются вообще - текст рисуется по нижнему краю без выравнивания
        # (отсюда была "неровная" точка редкости на скриншотах).
        self.label.text_size = (text_w, height)
        self._sync_graphics()

    def _sync_graphics(self, *args):
        pos = (round(self.x), round(self.y))
        size = (round(self.width), round(self.height))
        self.bg_rect.pos = pos
        self.bg_rect.size = size
        self.bg_rect.radius = [round(self.height / 2.0)] if self.filled else [0]
        if self.height <= 0:
            return
        dot_d = round(self.height * 0.32)
        pad_x = self.height * (0.42 if self.filled else 0.0)
        gap = dp(6)
        self.dot_ellipse.size = (dot_d, dot_d)
        self.dot_ellipse.pos = (round(self.x + pad_x), round(self.y + (self.height - dot_d) / 2))
        label_x = self.x + pad_x + dot_d + gap
        self.label.pos = (round(label_x), round(pos[1] - getattr(self, '_cap_dy', 0.0)))
        self.label.size = (max(round(self.width - (label_x - self.x)), dp(4)), size[1])
        self.label.text_size = self.label.size


class FilterTabButton(ButtonBehavior, FloatLayout):
    """
    Таб-фильтр списка достижений ("ВСЕ" / "ОТКРЫТО" / "В ПРОЦЕССЕ").
    Только два состояния окраски, обе из существующей палитры темы:
    выбранный - заливка color_text с текстом color_bg (инверсия, как
    активная кнопка), невыбранный - тем же светлым тоном, что и фон
    карточек (lerp_color(color_bg, color_key, 0.20)), текст color_text.
    """
    def __init__(self, text="", on_select_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.on_select_callback = on_select_callback
        self.selected = False

        with self.canvas.before:
            self.bg_color_instr = Color(*lerp_color(color_bg, color_key, 0.20))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        self.add_widget(self.label)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *args):
        pos = (round(self.x), round(self.y))
        size = (round(self.width), round(self.height))
        self.bg_rect.pos = pos
        self.bg_rect.size = size
        self.bg_rect.radius = [min(round(self.height / 2.0), dp(12))]
        self.label.text_size = (None, None)
        fit_font_size(self.label, self.width - dp(14), self.height * 0.42)
        self.label.size = size
        self.label.text_size = size
        self.label.pos = pos

    def update_visual(self):
        if self.selected:
            self.bg_color_instr.rgba = color_text
            self.label.color = color_bg
        else:
            self.bg_color_instr.rgba = lerp_color(color_bg, color_key, 0.20)
            self.label.color = color_text

    def on_release(self):
        if self.on_select_callback:
            self.on_select_callback(self)


class StatCardsMixin:
    """Общая верхняя строка карточек статистики для экранов "Достижения" и "Квесты".
    Методы перенесены из AchievementsScreen без изменений."""

    # ------------------------------------------------------------------
    # ПОЛОСА СТАТИСТИКИ: раскладка с запасом под обводку
    # ------------------------------------------------------------------
    def _layout_stats_strip(self, win_w, win_h, header_bottom):
        """Раскладывает горизонтальную строку карточек статистики и возвращает
        y нижнего края самих карточек (для расчёта положения табов).

        Размер и положение карточек не менялись. Меняется только область
        обрезки ScrollView: раньше её высота в точности равнялась высоте
        карточки, и обводка лежала ровно на границе обрезки. ScrollView
        обрезает содержимое по своим (дробным) границам, а карточка рисуется
        по округлённым пикселям, поэтому на верхней и нижней сторонах
        обрезался крайний пиксельный ряд - горизонтальные линии получались
        уже вертикальных. Теперь у ScrollView есть запас pad сверху и снизу,
        и обводка рисуется целиком."""
        pad = max(int(round(dp(4))), 3)
        stats_h = min(max(win_h * 0.13, dp(88)), dp(112))
        cards_bottom = header_bottom - stats_h

        self.stats_scroll.size = (win_w, stats_h + pad * 2)
        self.stats_scroll.pos = (0, cards_bottom - pad)

        card_w = min(max(win_w * 0.30, dp(96)), dp(150))
        self.stats_row.height = stats_h + pad * 2
        self.stats_row.padding = [dp(14), pad, dp(14), pad]
        for card in self.stats_row.children:
            card.size = (card_w, stats_h)
            self._layout_stat_card(card, card_w, stats_h)
        return cards_bottom

    # ------------------------------------------------------------------
    # КАРТОЧКА СТАТИСТИКИ (верхняя горизонтальная строка)
    # ------------------------------------------------------------------
    def create_stat_card(self, icon_name, label_text):
        card = FloatLayout(size_hint=(None, None))

        border_w = dp(1.2)
        with card.canvas.before:
            Color(*lerp_color(color_bg, color_key, 0.20))
            bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(14)])
            Color(*color_blank)
            border_line = Line(width=border_w, rounded_rectangle=(card.x, card.y, card.width, card.height, dp(14), dp(14), dp(14), dp(14)))

        def sync_bg(inst, val):
            # round() убирает субпиксельное дрожание рамки (та же причина
            # разной толщины обводки по разным сторонам карточки, что видна
            # на скриншотах) - приём уже используется в SettingLinkRow.
            pos = (round(inst.x), round(inst.y))
            size = (round(inst.width), round(inst.height))
            bg_rect.pos = pos
            bg_rect.size = size
            # Line рисуется ПО ЦЕНТРУ заданного пути, поэтому обводка шириной
            # border_w всегда "вылезает" на border_w/2 за пределы pos/size.
            # Карточка лежит в ScrollView, чья видимая область по высоте в
            # точности равна высоте карточки (без запаса сверху/снизу, в
            # отличие от горизонтали, где есть padding строки) - вылезающий
            # за границы кусок обводки обрезался стенсилом скролла, из-за
            # чего верхняя и нижняя линии казались вдвое тоньше боковых.
            # Сдвигаем путь внутрь на половину толщины линии, чтобы вся
            # обводка целиком помещалась внутри pos/size и никогда не обрезалась.
            half_w = border_w / 2.0
            border_line.rounded_rectangle = (
                pos[0] + half_w, pos[1] + half_w,
                max(size[0] - border_w, 0), max(size[1] - border_w, 0),
                dp(14), dp(14), dp(14), dp(14)
            )
        card.bind(pos=sync_bg, size=sync_bg)

        icon_img = Image(size_hint=(None, None), fit_mode="contain", color=color_text)
        icon_img.texture = load_white_icon_texture(icon_path(icon_name))
        card.add_widget(icon_img)

        lbl_val = Label(
            text="0",
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_text,
            bold=True,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        card.add_widget(lbl_val)

        lbl_lbl = Label(
            text=label_text,
            font_name=font_path("ClearSans-Bold.ttf"),
            color=color_not_in_word,
            bold=True,
            size_hint=(None, None),
            halign='center',
            valign='middle'
        )
        card.add_widget(lbl_lbl)

        card.icon_ref = icon_img
        card.value_ref = lbl_val
        card.label_ref = lbl_lbl
        card.bind(pos=self._layout_stat_card, size=self._layout_stat_card)
        return card

    def _layout_stat_card(self, card, *args):
        # Позиции считаются вручную и округляются (чёткий текст при прокрутке),
        # а дорогой подбор шрифта - только если изменились размер или текст.
        w, h = card.width, card.height
        if w <= 0 or h <= 0:
            return

        icon_side = round(h * 0.24)
        card.icon_ref.size = (icon_side, icon_side)
        card.icon_ref.pos = (
            round(card.x + (w - icon_side) / 2.0),
            round(card.y + h * 0.86 - icon_side),
        )

        val_h = h * 0.34
        lbl_h = h * 0.2
        val_w = w - dp(8)
        lbl_w = w - dp(8)

        fit_key = (round(w), round(h), card.value_ref.text, card.label_ref.text)
        if getattr(card, '_fit_key', None) != fit_key:
            card._fit_key = fit_key
            card.value_ref.text_size = (None, None)
            fit_font_size(card.value_ref, w - dp(16), val_h * 0.9)
            card.value_ref.size = (val_w, val_h)
            card.value_ref.text_size = card.value_ref.size

            card.label_ref.text_size = (None, None)
            fit_font_size(card.label_ref, w - dp(14), lbl_h * 0.85)
            card.label_ref.size = (lbl_w, lbl_h)
            card.label_ref.text_size = card.label_ref.size

        card.value_ref.pos = (
            round(card.x + (w - val_w) / 2.0),
            round(card.y + h * 0.28),
        )
        card.label_ref.pos = (
            round(card.x + (w - lbl_w) / 2.0),
            round(card.y + h * 0.06),
        )

class AchievementsScreen(StatCardsMixin, BaseScreen):
    # Табы-фильтры списка: (ключ фильтра, подпись на кнопке)
    FILTER_TABS = [
        ("all", "ВСЕ"),
        ("unlocked", "ОТКРЫТО"),
        ("inprogress", "В ПРОЦЕССЕ"),
    ]
    # Легенда редкости: (ключ типа, подпись)
    RARITY_LEGEND = [
        ("common", "Обычное"),
        ("rare", "Редкое"),
        ("epic", "Эпическое"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.stub_layout = create_stub_layout(self, "")
        self.layout.add_widget(self.stub_layout)

        self.top_overlay = FloatLayout(size_hint=(1, None))
        with self.top_overlay.canvas.before:
            Color(*color_bg)
            self.overlay_rect = RoundedRectangle(pos=(0, 0), size=(360, 200), radius=[0])
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

        # ----- горизонтально прокручиваемая строка статистики -----
        self.stats_scroll = SharpScrollView(size_hint=(1, None), do_scroll_x=True, do_scroll_y=False, bar_width=0)
        from kivy.effects.scroll import ScrollEffect
        self.stats_scroll.effect_cls = ScrollEffect

        self.stats_row = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(None, None))
        self.stats_row.bind(minimum_width=self.stats_row.setter('width'))
        self.stats_scroll.add_widget(self.stats_row)
        self.layout.add_widget(self.stats_scroll)

        stat_defs = [
            ("coins", "copyright.png", "Монеты"),
            ("wins", "trophy.png", "Победы"),
            ("losses", "trophy-off.png", "Поражения"),
            ("streak", "flame.png", "Серия побед"),
            ("ach_ratio", "award.png", "Достижения"),
            ("quests", "clipboard-text.png", "Квесты"),
        ]
        self._stat_cards = {}
        for key, icon_name, label_text in stat_defs:
            card = self.create_stat_card(icon_name, label_text)
            self.stats_row.add_widget(card)
            self._stat_cards[key] = card

        # ----- табы-фильтры -----
        self.tabs_row = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(None, None))
        self.layout.add_widget(self.tabs_row)

        self.current_filter = "all"
        self._tab_buttons = {}
        for key, label_text in self.FILTER_TABS:
            btn = FilterTabButton(
                text=label_text,
                size_hint=(1, 1),
                on_select_callback=lambda inst, k=key: self._on_tab_selected(k)
            )
            btn.selected = (key == self.current_filter)
            btn.update_visual()
            self.tabs_row.add_widget(btn)
            self._tab_buttons[key] = btn

        # ----- строка-легенда редкости -----
        self.legend_row = BoxLayout(orientation='horizontal', spacing=dp(18), size_hint=(None, None))
        self.legend_row.bind(minimum_width=self.legend_row.setter('width'))
        self.layout.add_widget(self.legend_row)

        legend_colors = {"common": color_not_in_word, "rare": color_in_word, "epic": color_correct}
        self._legend_dots = {}
        for type_key, label_text in self.RARITY_LEGEND:
            dot = RarityBadge(dot_color=legend_colors[type_key], text=label_text, filled=False)
            self.legend_row.add_widget(dot)
            self._legend_dots[type_key] = dot

        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        # ----- прокручиваемый список карточек достижений -----
        self.scroll_view = SharpScrollView(size_hint=(1, None), do_scroll_x=False, do_scroll_y=True, bar_width=0)
        from kivy.effects.scroll import ScrollEffect
        self.scroll_view.effect_cls = ScrollEffect

        # padding слева/справа = тот же отступ dp(15), что и у остальных
        # элементов шапки (табы, легенда) - раньше его не было, и карточки
        # доставали до самого края экрана. Небольшой верхний padding не даёт
        # верхней обводке первой карточки упираться вплотную в подложку
        # шапки (там был почти незаметный нахлёст, из-за которого обводка
        # выглядела обрезанной на скриншотах).
        self.ach_list_layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[dp(15), dp(6), dp(15), dp(20)])
        self.ach_list_layout.bind(minimum_height=self.ach_list_layout.setter('height'))
        self.scroll_view.add_widget(self.ach_list_layout)
        self.layout.add_widget(self.scroll_view)

        if hasattr(self, 'top_overlay'):
            self.layout.remove_widget(self.scroll_view)
            self.layout.add_widget(self.scroll_view, index=len(self.layout.children))

        self._ach_last_signature = None
        self._ach_build_event = None
        self._ach_all_cards = []  # [(widget, got_bool), ...] - чтобы табы переключались мгновенно, без пересборки

        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def on_pre_enter(self, *args):
        # Данные обновляются ДО показа экрана - статистика видна сразу.
        # Обычно всё уже подготовлено в фоне и тут срабатывает ранний выход.
        self.refresh_stats_and_achievements()
        self._speed_up_build()

    def prepare_in_background(self):
        self.refresh_stats_and_achievements(background=True)

    # ------------------------------------------------------------------
    # РАЗМЕТКА ЭКРАНА
    # ------------------------------------------------------------------
    def reposition_elements(self, instance, size):
        win_w = self.width
        win_h = self.height
        if win_w <= 0 or win_h <= 0:
            return

        back_w, back_h = dp(48), dp(48)
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

        header_bottom = (back_btn.y if back_btn is not None else win_h - TOP_SAFE_MARGIN - back_h) - dp(14)

        # --- строка статистики ---
        cards_bottom = self._layout_stats_strip(win_w, win_h, header_bottom)

        # --- табы-фильтры ---
        tabs_h = min(max(win_h * 0.055, dp(40)), dp(50))
        tabs_top = cards_bottom - dp(16)
        self.tabs_row.size = (win_w - dp(30), tabs_h)
        self.tabs_row.pos = (dp(15), tabs_top - tabs_h)

        # --- легенда редкости ---
        # Высота увеличена (была 20-26dp), а для текста легенды отдельно
        # задан font_scale побольше, чем дефолтный 0.52 у RarityBadge -
        # раньше подписи "Обычное/Редкое/Эпическое" получались всего
        # 12-13px и читались плохо.
        # На узком экране высота (а с ней шрифт/отступы/зазор между
        # плашками) шаг за шагом уменьшается, пока строка целиком не
        # впишется в ширину экрана - раньше высота считалась только от
        # win_h, ширина не проверялась вовсе, и на узких экранах строка
        # "Обычное • Редкое • Эпическое" не сужалась и вылезала за край.
        legend_available_w = max(win_w - dp(30), dp(10))
        legend_h = min(max(win_h * 0.04, dp(24)), dp(32))
        legend_min_h = dp(15)
        legend_gap = dp(18)

        def _legend_layout(h, gap):
            self.legend_row.spacing = gap
            for type_key, _ in self.RARITY_LEGEND:
                self._legend_dots[type_key].update_size(h, font_scale=0.62)
            return sum(self._legend_dots[k].width for k, _ in self.RARITY_LEGEND) + gap * (len(self.RARITY_LEGEND) - 1)

        legend_total_w = _legend_layout(legend_h, legend_gap)
        shrink_steps = 0
        while legend_total_w > legend_available_w and legend_h > legend_min_h and shrink_steps < 20:
            legend_h = max(legend_min_h, legend_h - dp(1))
            legend_gap = max(dp(8), legend_gap - dp(1))
            legend_total_w = _legend_layout(legend_h, legend_gap)
            shrink_steps += 1

        legend_top = self.tabs_row.y - dp(14)
        self.legend_row.height = legend_h
        self.legend_row.pos = (dp(15), legend_top - legend_h)

        list_top = self.legend_row.y - dp(16)

        # --- фоновая подложка шапки (чтобы список не наезжал на неё при скролле) ---
        overlay_h = max(win_h - list_top, 0)
        self.top_overlay.height = overlay_h
        self.top_overlay.pos = (0, list_top)
        self.overlay_rect.size = (win_w, overlay_h)
        self.overlay_rect.pos = (0, list_top)

        # --- список достижений ---
        self.scroll_view.size = (win_w, max(list_top - BOTTOM_SAFE_MARGIN, dp(10)))
        self.scroll_view.pos = (0, BOTTOM_SAFE_MARGIN)
        self.ach_list_layout.width = win_w

    # ------------------------------------------------------------------
    # ТАБЫ-ФИЛЬТРЫ
    # ------------------------------------------------------------------
    def _on_tab_selected(self, key):
        if key == self.current_filter:
            return
        self.current_filter = key
        for k, btn in self._tab_buttons.items():
            btn.selected = (k == key)
            btn.update_visual()
        self._apply_filter()

    def _apply_filter(self):
        self.ach_list_layout.clear_widgets()
        for widget, got in self._ach_all_cards:
            if self.current_filter == "unlocked" and not got:
                continue
            if self.current_filter == "inprogress" and got:
                continue
            self.ach_list_layout.add_widget(widget)

    # ------------------------------------------------------------------
    # РАЗБОР ЧИСЛОВЫХ ДОСТИЖЕНИЙ ("Выиграйте N раз." / "Проиграйте N раз.")
    # ------------------------------------------------------------------
    def _parse_ach_progress(self, description, stats):
        match = re.search(r"(Выиграйте|Проиграйте)\s+(\d+)\s+раз", description or "", re.IGNORECASE)
        if not match:
            return False, 0, 0
        target = int(match.group(2))
        if target <= 0:
            return False, 0, 0
        verb = match.group(1).lower()
        if verb.startswith("выиграйте"):
            current = stats.get("total_wins", 0)
        else:
            current = stats.get("total_losses", 0)
        return True, current, target

    # ------------------------------------------------------------------
    # КАРТОЧКА ДОСТИЖЕНИЯ
    # ------------------------------------------------------------------
    def create_achievement_card(self, name, description, ach_data, got, date_str, stats):
        r_type = "common"
        if isinstance(ach_data, dict):
            r_type = ach_data.get("type", "common").lower().strip()

        if r_type == "rare":
            dot_color = color_in_word
            type_text = "Редкое"
        elif r_type == "epic":
            dot_color = color_correct
            type_text = "Эпическое"
        else:
            dot_color = color_not_in_word
            type_text = "Обычное"

        is_numeric, current, target = self._parse_ach_progress(description, stats)
        show_progress = is_numeric and not got

        if got and date_str:
            status_text = date_str
        elif show_progress:
            status_text = f"{min(current, target)} / {target}"
        elif not got:
            status_text = "ЗАБЛОКИРОВАНО"
        else:
            status_text = ""

        row = FloatLayout(size_hint_y=None, height=dp(140))

        with row.canvas.before:
            Color(*lerp_color(color_bg, color_key, 0.20))
            bg_rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(14)])
            Color(*color_blank)
            border_line = Line(width=dp(1.2), rounded_rectangle=(row.x, row.y, row.width, row.height, dp(14), dp(14), dp(14), dp(14)))

        def sync_bg(inst, val):
            # round() убирает субпиксельное дрожание рамки при некруглых
            # размерах окна (та же причина "обрезанной" обводки на скринах).
            pos = (round(inst.x), round(inst.y))
            size = (round(inst.width), round(inst.height))
            bg_rect.pos = pos
            bg_rect.size = size
            border_line.rounded_rectangle = (pos[0], pos[1], size[0], size[1], dp(14), dp(14), dp(14), dp(14))
        row.bind(pos=sync_bg, size=sync_bg)

        # Все дочерние элементы кладём не прямо в row, а в обёртку content:
        # size_hint=(1,1) + pos_hint={'x':0,'y':0} заставляет Kivy держать её
        # координаты синхронно с row САМ, без наших ручных перевызовов. Ниже
        # позиции всех элементов внутри content задаются через pos_hint
        # (доли от текущего размера row) - это ключевое отличие от прежней
        # версии, где позиции присваивались один раз через .pos от row.x/
        # row.width, прочитанных в момент относительно ненадёжного колбэка
        # (GridLayout пересчитывает фактические x/width строки с задержкой
        # в кадр, и наше чтение могло "поймать" ещё не обновлённое значение -
        # отсюда нестабильность при резком ресайзе окна). pos_hint же Kivy
        # пересчитывает сам и непрерывно, поэтому расхождений не возникает.
        content = FloatLayout(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        row.add_widget(content)

        ach_font = font_path("ClearSans-Bold.ttf")
        name_lbl = Label(
            text=name.upper(), font_name=ach_font, font_size='17sp', bold=True, color=color_text,
            size_hint=(None, None), halign='left', valign='top'
        )
        desc_lbl = Label(
            text=description, font_name=ach_font, font_size='13sp', color=color_not_in_word,
            size_hint=(None, None), halign='left', valign='top'
        )
        status_icon = Image(size_hint=(None, None), fit_mode="contain", color=color_text)
        status_icon.texture = load_white_icon_texture(icon_path("check.png" if got else "lock.png"))

        badge = RarityBadge(dot_color=dot_color, text=type_text, filled=True)

        lbl_status = Label(
            text=status_text, font_name=ach_font, bold=True, color=color_not_in_word,
            size_hint=(None, None), halign='right', valign='middle'
        )

        for widget in (name_lbl, desc_lbl, status_icon, badge, lbl_status):
            content.add_widget(widget)

        progress_row = None
        prog_track = prog_fill = None
        if show_progress:
            progress_row = FloatLayout(size_hint=(None, None))
            with progress_row.canvas:
                Color(*color_blank)
                prog_track = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(4)])
                Color(*color_not_in_word)
                prog_fill = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(4)])

            def sync_progress(inst, val):
                pos = (round(inst.x), round(inst.y))
                size = (round(inst.width), round(inst.height))
                prog_track.pos = pos
                prog_track.size = size
                ratio = max(0.0, min(1.0, (current / target) if target > 0 else 0.0))
                prog_fill.pos = pos
                prog_fill.size = (round(size[0] * ratio), size[1])
            progress_row.bind(pos=sync_progress, size=sync_progress)
            content.add_widget(progress_row)

        PAD = dp(16)
        ICON_SIZE = dp(20)
        BADGE_H = dp(28)
        PROG_H = dp(8)
        GAP_S = dp(4)
        GAP_M = dp(10)

        def relayout(*args):
            w = row.width
            if w <= 0:
                return

            if getattr(relayout, '_w', None) != round(w):
                relayout._w = round(w)
                name_w = max(w - PAD * 2 - ICON_SIZE - dp(8), dp(10))
                name_lbl.text_size = (name_w, None)
                name_lbl.width = name_w
                name_lbl.texture_update()
                name_lbl.height = name_lbl.texture_size[1]

                desc_w = max(w - PAD * 2, dp(10))
                desc_lbl.text_size = (desc_w, None)
                desc_lbl.width = desc_w
                desc_lbl.texture_update()
                desc_lbl.height = desc_lbl.texture_size[1]

                badge.update_size(BADGE_H)

                lbl_status.text_size = (None, None)
                fit_font_size(lbl_status, w * 0.55, dp(13))
                lbl_status.texture_update()
                lbl_status.size = lbl_status.texture_size
                lbl_status.text_size = lbl_status.size

            total_h = PAD + name_lbl.height + GAP_S + desc_lbl.height + GAP_M
            if show_progress:
                total_h += PROG_H + GAP_M
            total_h += BADGE_H + PAD
            new_h = max(dp(96), total_h)
            row.height = new_h

            # Раньше здесь были доли (pos_hint): {'x': PAD / w, 'top': ...} -
            # Kivy сам пересчитывал пиксели от row.width/row.height, но
            # результат почти всегда получался дробным (нецелым), и текст
            # карточки размывался - особенно заметно при прокрутке списка
            # достижений. content - обычный FloatLayout (не RelativeLayout),
            # поэтому координаты его детей - те же абсолютные координаты,
            # что и у row; берём row.x/row.y напрямую и округляем (round())
            # каждую позицию, как и в остальных местах экрана. row.bind
            # ниже подписан и на pos, и на size - это сохраняет то же
            # "пересчитывается само" поведение, что раньше давал pos_hint.
            row_x, row_y = row.x, row.y
            name_top_y = row_y + new_h - PAD
            name_lbl.pos = (round(row_x + PAD), round(name_top_y - name_lbl.height))

            desc_top_y = name_top_y - name_lbl.height - GAP_S
            desc_lbl.pos = (round(row_x + PAD), round(desc_top_y - desc_lbl.height))

            status_icon.size = (ICON_SIZE, ICON_SIZE)
            status_icon.pos = (round(row_x + w - PAD - ICON_SIZE), round(name_top_y - ICON_SIZE))

            if show_progress:
                progress_row.size = (max(w - PAD * 2, dp(10)), PROG_H)
                progress_top_y = desc_top_y - desc_lbl.height - GAP_M
                progress_row.pos = (round(row_x + PAD), round(progress_top_y - PROG_H))
                badge_top_y = progress_top_y - PROG_H - GAP_M
            else:
                badge_top_y = desc_top_y - desc_lbl.height - GAP_M

            badge.pos = (round(row_x + PAD), round(badge_top_y - BADGE_H))
            status_y = round(badge_top_y - BADGE_H / 2 - lbl_status.height / 2)
            lbl_status.pos = (round(row_x + w - PAD - lbl_status.width), status_y)

        name_lbl.bind(texture_size=relayout)
        desc_lbl.bind(texture_size=relayout)
        row.bind(pos=relayout, size=relayout)
        relayout()

        return row

    # ------------------------------------------------------------------
    # ПОСТРОЕНИЕ СПИСКА (по частям, чтобы не подвешивать кадр)
    # ------------------------------------------------------------------
    def _card_visible(self, got):
        if self.current_filter == "unlocked" and not got:
            return False
        if self.current_filter == "inprogress" and got:
            return False
        return True

    def build_achievements_list(self, launcher_achievements, stats, background=False):
        if self._ach_build_event is not None:
            self._ach_build_event.cancel()
            self._ach_build_event = None

        self.ach_list_layout.clear_widgets()
        self._ach_all_cards = []
        self._ach_remaining = []
        self._ach_stats = stats

        if not launcher_achievements:
            return

        sorted_keys = sorted(launcher_achievements.keys(),
                             key=lambda k: launcher_achievements[k].get("got", False), reverse=True)
        self._ach_remaining = [(k, launcher_achievements[k]) for k in sorted_keys]

        if background:
            # экран не виден: строим по одной карточке, не мешая остальному
            self._ach_rows_per_tick = 1
            self._ach_build_event = Clock.schedule_interval(self._ach_build_tick, 0.03)
        else:
            # экран сейчас откроется: первые карточки сразу, остальное по кадрам
            self._ach_rows_per_tick = 4
            self._ach_build_tick(0)
            if self._ach_remaining:
                self._ach_build_event = Clock.schedule_interval(self._ach_build_tick, 0)

    def _ach_build_tick(self, dt):
        for _ in range(self._ach_rows_per_tick):
            if not self._ach_remaining:
                self._ach_build_event = None
                return False
            _key, ach_data = self._ach_remaining.pop(0)
            got = ach_data.get("got", False)
            card = self.create_achievement_card(
                ach_data.get("name", "Секретное достижение"),
                ach_data.get("description", ""),
                ach_data, got, ach_data.get("date", ""), self._ach_stats)
            self._ach_all_cards.append((card, got))
            # карточка добавляется в список один раз, а не пересобирается весь список каждый кадр
            if self._card_visible(got):
                self.ach_list_layout.add_widget(card)
        return True

    def _speed_up_build(self):
        """Если экран открыли, пока фоновая сборка ещё идёт - ускоряем её."""
        if self._ach_build_event is not None and self._ach_rows_per_tick < 4:
            self._ach_build_event.cancel()
            self._ach_build_event = None
            self._ach_rows_per_tick = 4
            self._ach_build_tick(0)
            if self._ach_remaining:
                self._ach_build_event = Clock.schedule_interval(self._ach_build_tick, 0)

    # ------------------------------------------------------------------
    # ОБНОВЛЕНИЕ СТАТИСТИКИ И СПИСКА
    # ------------------------------------------------------------------
    def refresh_stats_and_achievements(self, background=False):
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
        if signature == self._ach_last_signature:
            return
        self._ach_last_signature = signature

        stat_values = {
            "coins": str(coins),
            "wins": str(wins),
            "losses": str(losses),
            "streak": streak,
            "ach_ratio": ach_ratio,
            "quests": str(quests),
        }
        for key, card in self._stat_cards.items():
            card.value_ref.text = stat_values.get(key, "0")

        self.reposition_elements(None, None)
        self.build_achievements_list(launcher_ach, stats, background=background)

import colorsys
from kivy.uix.textinput import TextInput


# ======================================================================
# СВОЯ ТЕМА: вспомогательное
# ======================================================================
def _hsv_to_rgba(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (r, g, b, 1.0)


def _rgba_to_hsv(color):
    return colorsys.rgb_to_hsv(color[0], color[1], color[2])


def _prep_caps_label(label):
    """Готовит лейбл (размер = текстура) и возвращает (w, h, dy). Чтобы центр ЗАГЛАВНЫХ
    букв встал в точку (cx, cy): label.pos = (cx - w/2, cy - h/2 - dy). Тяжёлое (рендер
    текста) делается тут один раз, а при прокрутке/сдвиге только меняется pos."""
    label.text_size = (None, None)
    label.texture_update()
    tw, th = label.texture_size
    label.size = (tw, th)
    return tw, th, cap_ink_offset_y(label.font_size)


class CustomThemeCard(ButtonBehavior, FloatLayout):
    """
    Широкая карточка "Своя тема" в самом верху списка тем: полоска из 7 цветов
    темы игрока, название, подпись и чип (цена 10000 / ОТКРЫТО / ПРИМЕНЕНО).
    Интерфейс тот же, что у ThemeCard (is_selected, set_state, update_indicators).
    """
    CARD_RADIUS = dp(16)

    @staticmethod
    def metrics(w):
        pad = dp(10)
        panel_pad = dp(12)
        sgap = dp(6)
        sw = max((w - 2 * pad - 2 * panel_pad - 6 * sgap) / 7.0, 1.0)
        panel_h = sw + 2 * panel_pad
        name_h, sub_h, chip_h = dp(26), dp(18), dp(26)
        h = pad + panel_h + dp(12) + name_h + dp(2) + sub_h + dp(10) + chip_h + pad * 1.4
        return dict(pad=pad, panel_pad=panel_pad, sgap=sgap, sw=sw, panel_h=panel_h,
                    name_h=name_h, sub_h=sub_h, chip_h=chip_h, h=h)

    def __init__(self, theme_id=CUSTOM_THEME_ID, theme_data=None, on_click_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.theme_id = theme_id
        self.on_click_callback = on_click_callback
        self.is_selected = False
        self.is_active = False
        self.is_owned = False
        self.chip = None
        self.base_color = lerp_color(color_bg, color_key, 0.20)

        with self.canvas.before:
            self.bg_color_instr = Color(*self.base_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.CARD_RADIUS])
            Color(*color_bg)
            self.panel_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(12)])

        slot_colors = color_themes[CUSTOM_THEME_ID]
        with self.canvas:
            self.sw_colors, self.sw_rects, self.sw_outer = [], [], []
            for key, _name in CUSTOM_SLOTS:
                Color(*color_blank)
                self.sw_outer.append(RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(6)]))
                self.sw_colors.append(Color(*slot_colors[key]))
                self.sw_rects.append(RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(6)]))

        with self.canvas.after:
            self.border_color_instr = Color(*color_blank)
            self.border_line = Line(width=dp(1.2))

        self.name_label = Label(text="Своя тема", font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                                color=color_text, size_hint=(None, None), halign='left', valign='middle')
        self.add_widget(self.name_label)
        self.sub_label = Label(text="Настройте цвет каждого элемента", font_name=font_path("ClearSans-Bold.ttf"),
                               bold=True, color=color_not_in_word, size_hint=(None, None),
                               halign='left', valign='middle')
        self.add_widget(self.sub_label)
        self.lock_icon = Image(size_hint=(None, None), fit_mode="contain", color=color_not_in_word)
        self.lock_icon.texture = load_white_icon_texture(icon_path("lock.png"))
        self.add_widget(self.lock_icon)

        self._rebuild_chip()
        self.bind(pos=self._relayout, size=self._relayout, state=self._update_bg)

    # ----- состояние -----
    def set_state(self, owned, active):
        changed = (owned != self.is_owned) or (active != self.is_active) or self.chip is None
        self.is_owned = owned
        self.is_active = active
        if changed:
            self._rebuild_chip()
        self.lock_icon.opacity = 0 if owned else 1
        self.update_indicators()
        self._relayout()

    def _rebuild_chip(self):
        if self.chip is not None:
            self.remove_widget(self.chip)
        if not self.is_owned:
            self.chip = RewardBadge(text=str(CUSTOM_THEME_PRICE))
        elif self.is_active:
            self.chip = RarityBadge(dot_color=color_correct, text="ПРИМЕНЕНО", filled=True)
        else:
            self.chip = RarityBadge(dot_color=color_not_in_word, text="ОТКРЫТО", filled=True)
        self.add_widget(self.chip)

    def update_indicators(self):
        if self.is_selected:
            self.border_color_instr.rgba = color_text
            self.border_line.width = dp(1.2)
        else:
            self.border_color_instr.rgba = color_blank
            self.border_line.width = dp(1.2)
        self._sync_border()

    def _sync_border(self):
        x0, y0 = round(self.x), round(self.y)
        w, h = round(self.width), round(self.height)
        half = self.border_line.width / 2.0
        r = self.CARD_RADIUS
        self.border_line.rounded_rectangle = (x0 + half, y0 + half, max(w - half * 2, 0),
                                              max(h - half * 2, 0), r, r, r, r)

    def _update_bg(self, *args):
        if self.state == 'normal':
            self.bg_color_instr.rgba = self.base_color
        else:
            c = self.base_color
            self.bg_color_instr.rgba = (c[0] * 0.94, c[1] * 0.94, c[2] * 0.94, c[3])

    def on_release(self):
        if self.on_click_callback:
            self.on_click_callback(self.theme_id)

    # ----- раскладка -----
    def _relayout(self, *args):
        w, h = self.width, self.height
        if w <= 1 or h <= 1:
            return
        m = self.metrics(w)
        x0, y0 = round(self.x), round(self.y)
        self.bg_rect.pos = (x0, y0)
        self.bg_rect.size = (round(w), round(h))
        self._sync_border()

        lock_side = m['name_h'] * 0.8
        fkey = (round(w), round(h))
        if fkey != getattr(self, '_font_key', None):
            self._font_key = fkey
            name_w = max(w - 2 * m['pad'] - lock_side - dp(8), dp(10))
            fit_font_size(self.name_label, name_w, m['name_h'] * 0.85)
            self.name_label.size = (name_w, m['name_h'])
            self.name_label.text_size = self.name_label.size
            sub_w = max(w - 2 * m['pad'] - dp(8), dp(10))
            fit_font_size(self.sub_label, sub_w, m['sub_h'] * 0.8)
            self.sub_label.size = (sub_w, m['sub_h'])
            self.sub_label.text_size = self.sub_label.size

        left = x0 + m['pad']
        top = y0 + h - m['pad']
        panel_y = top - m['panel_h']
        self.panel_rect.pos = (round(left), round(panel_y))
        self.panel_rect.size = (round(w - 2 * m['pad']), round(m['panel_h']))

        # целые размеры и равные промежутки: квадраты ровные, контур совпадает с заливкой
        sw = int(m['sw'])
        gap = int(round(m['sgap']))
        bw = max(int(round(dp(1.2))), 1)
        n = len(CUSTOM_SLOTS)
        total = n * sw + (n - 1) * gap
        start = round(left + (w - 2 * m['pad'] - total) / 2.0)
        sy = round(panel_y + (m['panel_h'] - sw) / 2.0)
        r = sw * 0.22
        for i in range(n):
            sx = start + i * (sw + gap)
            self.sw_outer[i].pos = (sx, sy)
            self.sw_outer[i].size = (sw, sw)
            self.sw_outer[i].radius = [r]
            self.sw_rects[i].pos = (sx + bw, sy + bw)
            self.sw_rects[i].size = (sw - 2 * bw, sw - 2 * bw)
            self.sw_rects[i].radius = [max(r - bw, 0)]

        name_y = panel_y - dp(12) - m['name_h']
        self.name_label.pos = (round(left + dp(2)), round(name_y))
        self.lock_icon.size = (lock_side, lock_side)
        self.lock_icon.pos = (round(x0 + w - m['pad'] - lock_side - dp(2)),
                              round(name_y + (m['name_h'] - lock_side) / 2.0))
        sub_y = name_y - dp(2) - m['sub_h']
        self.sub_label.pos = (round(left + dp(2)), round(sub_y))
        if self.chip is not None:
            self.chip.update_size(m['chip_h'], font_scale=0.5)
            self.chip.pos = (round(left + dp(2)), round(sub_y - dp(10) - m['chip_h']))


class ColorSlider(FloatLayout):
    """Ползунок с градиентной дорожкой (значение 0..1). Градиент - маленькая текстура."""
    SAMPLES = 96

    def __init__(self, on_change=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.value = 0.0
        self.on_change = on_change
        self._tex = Texture.create(size=(self.SAMPLES, 1), colorfmt='rgba')
        self._tex.mag_filter = 'linear'
        self._tex.min_filter = 'linear'
        self.set_gradient([(0, 0, 0, 1), (1, 1, 1, 1)])
        with self.canvas:
            Color(1, 1, 1, 1)
            self._track = RoundedRectangle(texture=self._tex, pos=self.pos, size=self.size, radius=[dp(8)])
            Color(*color_blank)
            self._border = Line(width=dp(1.2))
            Color(*color_text)
            self._ring = Ellipse(pos=(0, 0), size=(0, 0))
            Color(*color_bg)
            self._core = Ellipse(pos=(0, 0), size=(0, 0))
        self.bind(pos=self._redraw, size=self._redraw)

    def set_gradient(self, stops):
        n = self.SAMPLES
        last = len(stops) - 1
        buf = bytearray()
        for i in range(n):
            t = i / float(n - 1) * last
            a = min(int(t), last - 1)
            f = t - a
            c0, c1 = stops[a], stops[a + 1]
            for j in range(3):
                buf.append(int(round(255 * (c0[j] + (c1[j] - c0[j]) * f))))
            buf.append(255)
        self._tex.blit_buffer(bytes(buf), colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

    def set_value(self, value, notify=False):
        self.value = max(0.0, min(1.0, value))
        self._redraw()
        if notify and self.on_change:
            self.on_change(self.value)

    def _thumb_d(self):
        return self.height * 0.78

    def _redraw(self, *args):
        if self.width <= 1 or self.height <= 1:
            return
        th = self.height * 0.40
        ty = self.y + (self.height - th) / 2.0
        self._track.pos = (round(self.x), round(ty))
        self._track.size = (round(self.width), round(th))
        self._track.radius = [th / 2.0]
        half = dp(1.2) / 2.0
        self._border.rounded_rectangle = (round(self.x) + half, round(ty) + half,
                                          max(round(self.width) - 2 * half, 0), max(round(th) - 2 * half, 0),
                                          th / 2.0, th / 2.0, th / 2.0, th / 2.0)
        d = self._thumb_d()
        r = d / 2.0
        cx = self.x + r + self.value * max(self.width - d, 1)
        cy = self.y + self.height / 2.0
        # целые размеры одной чётности: внутренний кружок ровно по центру внешнего
        big = int(round(d))
        inset = max(int(round(dp(3.5))), 1)
        small = max(big - 2 * inset, 1)
        ring_x = int(round(cx - big / 2.0))
        ring_y = int(round(cy - big / 2.0))
        self._ring.pos = (ring_x, ring_y)
        self._ring.size = (big, big)
        self._core.pos = (ring_x + inset, ring_y + inset)
        self._core.size = (small, small)

    def _value_from_x(self, x):
        d = self._thumb_d()
        return (x - (self.x + d / 2.0)) / max(self.width - d, 1)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.set_value(self._value_from_x(touch.x), notify=True)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.set_value(self._value_from_x(touch.x), notify=True)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super().on_touch_up(touch)


class SlotChip(ButtonBehavior, FloatLayout):
    """Чип выбора редактируемого цвета: образец цвета + название."""
    def __init__(self, text, rgba, on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.on_press_callback = on_press_callback
        self.selected = False
        self._lbl = (0, 0, 0)

        with self.canvas.before:
            self.bg_color_instr = Color(*lerp_color(color_bg, color_key, 0.20))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
        with self.canvas:
            self.sw_color = Color(*rgba)
            self.sw_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(8)])
            Color(*color_not_in_word)
            self.sw_border = Line(width=dp(1.2))
        with self.canvas.after:
            self.border_color_instr = Color(*color_blank)
            self.border_line = Line(width=dp(1.2))

        self.label = Label(text=text, font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                           color=color_text, size_hint=(None, None))
        self.add_widget(self.label)
        self.bind(pos=self._relayout, size=self._relayout)

    def set_rgba(self, rgba):
        self.sw_color.rgba = rgba

    def set_selected(self, value):
        self.selected = value
        self.border_color_instr.rgba = color_text if value else color_blank
        self.border_line.width = dp(1.2)
        self._sync_border()

    def fit_to_height(self, h):
        key = round(h, 1)
        if key == getattr(self, '_fit_h', None):
            return
        self._fit_h = key
        self.label.font_size = f"{max(int(h * 0.30), 10)}px"
        tw, th, dy = _prep_caps_label(self.label)
        self._lbl = (tw, th, dy)
        sw = h * 0.62
        self.size = (h * 0.17 + sw + h * 0.17 + tw + h * 0.32, h)
        self._relayout()

    def _sync_border(self):
        x0, y0 = round(self.x), round(self.y)
        w, h = round(self.width), round(self.height)
        half = self.border_line.width / 2.0
        r = min(dp(14), h / 2.0)
        self.border_line.rounded_rectangle = (x0 + half, y0 + half, max(w - half * 2, 0),
                                              max(h - half * 2, 0), r, r, r, r)

    def _relayout(self, *args):
        w, h = self.width, self.height
        if w <= 1 or h <= 1:
            return
        x0, y0 = round(self.x), round(self.y)
        self.bg_rect.pos = (x0, y0)
        self.bg_rect.size = (round(w), round(h))
        self.bg_rect.radius = [min(dp(14), h / 2.0)]
        self._sync_border()
        sw = h * 0.62
        sx, sy = x0 + h * 0.17, y0 + (h - sw) / 2.0
        self.sw_rect.pos = (round(sx), round(sy))
        self.sw_rect.size = (round(sw), round(sw))
        self.sw_rect.radius = [sw * 0.26]
        half = dp(1.2) / 2.0
        r = sw * 0.26
        self.sw_border.rounded_rectangle = (round(sx) + half, round(sy) + half,
                                            max(round(sw) - 2 * half, 0), max(round(sw) - 2 * half, 0),
                                            r, r, r, r)
        tw, th, dy = self._lbl
        self.label.pos = (round(sx + sw + h * 0.17), round(y0 + h / 2.0 - th / 2.0 - dy))

    def on_release(self):
        if self.on_press_callback:
            self.on_press_callback(self)


class ThemePreviewBoard(FloatLayout):
    """Живое превью темы: игровое поле (плитки + клавиатура) в редактируемых цветах.
    Цвета букв на плитках - те же, что в игровых клетках (белый/чёрный)."""
    WORD = "ЦВЕТА"
    KEY_ROWS = ("ЙЦУКЕНГШЩЗ", "ФЫВАПРОЛДЖ")

    @staticmethod
    def metrics(w):
        pad = w * 0.035
        tile = w * 0.133
        tg = w * 0.0167
        kg = w * 0.0083
        k = (w - 2 * pad - 9 * kg) / 10.0
        top_gap = tg * 1.2
        h = pad * 1.2 + 2 * tile + tg + top_gap + 2 * k + kg + pad
        return dict(pad=pad, tile=tile, tg=tg, kg=kg, k=k, top_gap=top_gap, h=h)

    @staticmethod
    def height_for_width(w):
        return ThemePreviewBoard.metrics(w)['h']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.colors = {k: hex_to_rgba(v) for k, v in CUSTOM_DEFAULT_HEX.items()}

        with self.canvas.before:
            self.bg_color = Color(*self.colors['color_bg'])
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
        with self.canvas:
            self.tile_colors, self.tile_rects = [], []
            for _ in range(10):
                self.tile_colors.append(Color(1, 1, 1, 1))
                self.tile_rects.append(RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(8)]))
            self.key_color = Color(*self.colors['color_key'])
            self.key_rects = [RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(5)]) for _ in range(20)]
        with self.canvas.after:
            Color(*color_blank)
            self.border_line = Line(width=dp(1.5))

        self.tile_labels, self.key_labels = [], []
        for ch in self.WORD:
            lbl = Label(text=ch, font_name=font_path("ClearSans-Bold.ttf"), bold=True, size_hint=(None, None))
            self.tile_labels.append(lbl)
            self.add_widget(lbl)
        for row in self.KEY_ROWS:
            for ch in row:
                lbl = Label(text=ch, font_name=font_path("ClearSans-Bold.ttf"), bold=True, size_hint=(None, None))
                self.key_labels.append(lbl)
                self.add_widget(lbl)
        self._tile_lbl = [(0, 0, 0)] * 5
        self._key_lbl = [(0, 0, 0)] * 20
        self.set_colors(self.colors)
        self.bind(pos=self._relayout, size=self._relayout)

    def set_colors(self, colors):
        """colors: {ключ слота: rgba}."""
        self.colors = colors
        c = colors
        self.bg_color.rgba = c['color_bg']
        states = [c['color_blank'], c['color_correct'], c['color_in_word'], c['color_not_in_word'], c['color_blank']]
        letter = [c['color_text'], (1, 1, 1, 1), (0, 0, 0, 1), (1, 1, 1, 1), c['color_text']]
        for i in range(10):
            self.tile_colors[i].rgba = states[i] if i < 5 else c['color_blank']
        for i, lbl in enumerate(self.tile_labels):
            lbl.color = letter[i]
        self.key_color.rgba = c['color_key']
        for lbl in self.key_labels:
            lbl.color = c['color_text']

    def _relayout(self, *args):
        w, h = self.width, self.height
        if w <= 1 or h <= 1:
            return
        full = self.metrics(w)
        s = min(1.0, h / full['h'])
        ew = w * s
        m = self.metrics(ew)
        x0, y0 = round(self.x), round(self.y)
        self.bg_rect.pos = (x0, y0)
        self.bg_rect.size = (round(w), round(h))
        half = self.border_line.width / 2.0
        r = dp(16)
        self.border_line.rounded_rectangle = (x0 + half, y0 + half, max(round(w) - 2 * half, 0),
                                              max(round(h) - 2 * half, 0), r, r, r, r)

        tile, k = m['tile'], m['k']
        fkey = (round(tile, 1), round(k, 1))
        if fkey != getattr(self, '_font_key', None):
            self._font_key = fkey
            for i, lbl in enumerate(self.tile_labels):
                lbl.font_size = f"{max(int(tile * 0.55), 8)}px"
                self._tile_lbl[i] = _prep_caps_label(lbl)
            for i, lbl in enumerate(self.key_labels):
                lbl.font_size = f"{max(int(k * 0.55), 7)}px"
                self._key_lbl[i] = _prep_caps_label(lbl)

        ox = self.x + (w - ew) / 2.0
        block_bottom = self.y + (h - m['h']) / 2.0
        top = block_bottom + m['h']
        row1_y = top - m['pad'] * 1.2 - tile
        row2_y = row1_y - m['tg'] - tile
        tiles_w = 5 * tile + 4 * m['tg']
        tx0 = ox + (ew - tiles_w) / 2.0
        for row, ty in ((0, row1_y), (1, row2_y)):
            for col in range(5):
                tx = tx0 + col * (tile + m['tg'])
                rect = self.tile_rects[row * 5 + col]
                rect.pos = (round(tx), round(ty))
                rect.size = (round(tile), round(tile))
                rect.radius = [tile * 0.17]
                if row == 0:
                    tw, th, dy = self._tile_lbl[col]
                    self.tile_labels[col].pos = (round(tx + tile / 2.0 - tw / 2.0),
                                                 round(ty + tile / 2.0 - th / 2.0 - dy))
        key1_y = row2_y - m['top_gap'] - k
        key2_y = key1_y - m['kg'] - k
        for row, ky in ((0, key1_y), (1, key2_y)):
            for col in range(10):
                kx = ox + m['pad'] + col * (k + m['kg'])
                idx = row * 10 + col
                rect = self.key_rects[idx]
                rect.pos = (round(kx), round(ky))
                rect.size = (round(k), round(k))
                rect.radius = [k * 0.17]
                tw, th, dy = self._key_lbl[idx]
                self.key_labels[idx].pos = (round(kx + k / 2.0 - tw / 2.0), round(ky + k / 2.0 - th / 2.0 - dy))


class NameInput(TextInput):
    """Поле названия: не длиннее CUSTOM_NAME_MAX символов."""
    def insert_text(self, substring, from_undo=False):
        room = CUSTOM_NAME_MAX - len(self.text)
        if room <= 0:
            return super().insert_text('', from_undo=from_undo)
        return super().insert_text(substring[:room], from_undo=from_undo)


class ThemeEditorScreen(BaseScreen):
    """Экран "Своя тема": живое превью, выбор цвета элемента, ползунки Тон/Насыщенность/Яркость.
    Правки живут на экране (черновик) и сохраняются/применяются кнопкой ПРИМЕНИТЬ;
    сам интерфейс экрана красится текущей применённой темой, а не редактируемой."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = None
        self.slot_index = 0
        self._btn_state = None
        self._head_h, self._row_h = dp(44), dp(40)
        self._load_draft()
        self._build_ui()
        self.bind(size=self.reposition_elements)
        self.reposition_elements(None, None)
        self._refresh_all()
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    # ------------------------------------------------------------------
    # ДАННЫЕ
    # ------------------------------------------------------------------
    def _stats(self):
        if 'MOBILE_PLAYER_STATS' in globals() and MOBILE_PLAYER_STATS is not None:
            return MOBILE_PLAYER_STATS
        return {}

    def _is_owned(self):
        return bool(self._stats().get("unlocked_themes", {}).get(CUSTOM_THEME_ID, False))

    def _load_draft(self):
        name, colors = get_custom_theme_data()
        self.name_text = name
        self.draft = {k: _rgba_to_hsv(hex_to_rgba(v)) for k, v in colors.items()}

    def _load_defaults(self):
        self.name_text = CUSTOM_DEFAULT_NAME
        self.draft = {k: _rgba_to_hsv(hex_to_rgba(v)) for k, v in CUSTOM_DEFAULT_HEX.items()}

    def _draft_rgba(self):
        return {k: _hsv_to_rgba(*v) for k, v in self.draft.items()}

    def _draft_hex(self):
        return {k: rgba_to_hex(c) for k, c in self._draft_rgba().items()}

    # ------------------------------------------------------------------
    # СБОРКА ИНТЕРФЕЙСА (заново при смене темы)
    # ------------------------------------------------------------------
    def _build_ui(self):
        self.layout = FloatLayout()
        card_bg = lerp_color(color_bg, color_key, 0.20)

        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'customization'))
        self.layout.add_widget(self.btn_back)
        self.title_label = Label(text="Своя тема", font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                                 color=color_text, size_hint=(None, None), halign='left', valign='middle')
        self.layout.add_widget(self.title_label)

        # --- название ---
        self.name_card = FloatLayout(size_hint=(None, None))
        with self.name_card.canvas.before:
            Color(*card_bg)
            self._name_bg = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(14)])
        with self.name_card.canvas.after:
            Color(*color_blank)
            self._name_border = Line(width=dp(1.2))
        self.name_icon = Image(size_hint=(None, None), fit_mode="contain", color=color_text)
        self.name_icon.texture = load_white_icon_texture(icon_path("pencil.png"))
        self.name_card.add_widget(self.name_icon)
        self.name_caption = Label(text="Название", font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                                  color=color_not_in_word, size_hint=(None, None))
        self.name_card.add_widget(self.name_caption)
        self.name_input = NameInput(text=self.name_text, multiline=False, write_tab=False,
                                    font_name=font_path("ClearSans-Bold.ttf"), size_hint=(None, None),
                                    foreground_color=color_text, cursor_color=color_text,
                                    selection_color=(color_correct[0], color_correct[1], color_correct[2], 0.35),
                                    background_color=(0, 0, 0, 0), background_normal='', background_active='',
                                    background_disabled_normal='', halign='right')
        self.name_input.bind(text=self._on_name_text)
        self.name_input.bind(scroll_y=lambda inst, value: setattr(inst, 'scroll_y', 0))
        self.name_input.bind(on_text_validate=lambda inst: setattr(inst, 'focus', False))
        self.name_card.add_widget(self.name_input)
        self.layout.add_widget(self.name_card)

        # --- превью ---
        self.preview = ThemePreviewBoard()
        self.layout.add_widget(self.preview)

        # --- выбор элемента ---
        self.slot_scroll = SharpScrollView(size_hint=(1, None), do_scroll_x=True, do_scroll_y=False, bar_width=0)
        self.slot_scroll.effect_cls = ScrollEffect
        self.slot_row = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint=(None, None),
                                  padding=[dp(15), dp(4), dp(15), dp(4)])
        self.slot_row.bind(minimum_width=self.slot_row.setter('width'))
        self.slot_scroll.add_widget(self.slot_row)
        self.slot_chips = []
        for i, (key, label_text) in enumerate(CUSTOM_SLOTS):
            chip = SlotChip(text=label_text, rgba=hex_to_rgba(CUSTOM_DEFAULT_HEX[key]),
                            on_press_callback=lambda inst, idx=i: self._select_slot(idx))
            self.slot_row.add_widget(chip)
            self.slot_chips.append(chip)
        self.layout.add_widget(self.slot_scroll)

        # --- панель цвета ---
        self.picker = FloatLayout(size_hint=(None, None))
        with self.picker.canvas.before:
            Color(*card_bg)
            self._picker_bg = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(16)])
        with self.picker.canvas:
            self._picker_sw_color = Color(1, 1, 1, 1)
            self._picker_sw = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(10)])
            Color(*color_not_in_word)
            self._picker_sw_border = Line(width=dp(1.2))
        with self.picker.canvas.after:
            Color(*color_blank)
            self._picker_border = Line(width=dp(1.2))
        self.cur_label = Label(text="", font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                               color=color_text, size_hint=(None, None), halign='left', valign='middle')
        self.cur_hex = Label(text="", font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                             color=color_not_in_word, size_hint=(None, None), halign='left', valign='middle')
        self.picker.add_widget(self.cur_label)
        self.picker.add_widget(self.cur_hex)
        self.contrast_chip = RarityBadge(dot_color=color_correct, text="ЧИТАЕТСЯ", filled=True)
        self.picker.add_widget(self.contrast_chip)
        self.row_captions, self.sliders = [], []
        for i, caption in enumerate(("Тон", "Насыщ.", "Яркость")):
            cap = Label(text=caption, font_name=font_path("ClearSans-Bold.ttf"), bold=True,
                        color=color_not_in_word, size_hint=(None, None), halign='left', valign='middle')
            slider = ColorSlider(on_change=lambda v, idx=i: self._on_slider(idx, v))
            self.picker.add_widget(cap)
            self.picker.add_widget(slider)
            self.row_captions.append(cap)
            self.sliders.append(slider)
        self.sliders[0].set_gradient([(1, 0, 0, 1), (1, 1, 0, 1), (0, 1, 0, 1), (0, 1, 1, 1),
                                      (0, 0, 1, 1), (1, 0, 1, 1), (1, 0, 0, 1)])
        self.layout.add_widget(self.picker)

        # --- нижняя панель ---
        self.bottom_bar = FloatLayout(size_hint=(None, None))
        with self.bottom_bar.canvas.before:
            Color(*color_bg)
            self._bar_bg = Rectangle(pos=(0, 0), size=(0, 0))
            Color(*color_blank)
            self._bar_line = Rectangle(pos=(0, 0), size=(0, 0))
        self.btn_reset = ThemeActionButton()
        self.btn_apply = ThemeActionButton()
        self.bottom_bar.add_widget(self.btn_reset)
        self.bottom_bar.add_widget(self.btn_apply)
        self.layout.add_widget(self.bottom_bar)
        self.btn_reset.set_content("СБРОС", "secondary", on_release=self._on_reset)
        self._btn_state = None

        self.add_widget(self.layout)

    def apply_theme_instant(self):
        """Вызывается из redraw_all_screens: пересобираем под новую тему, черновик сохраняется."""
        if self.layout is not None:
            self.remove_widget(self.layout)
        self._build_ui()
        self.reposition_elements(None, None)
        self._refresh_all()

    def on_pre_enter(self, *args):
        if not self._is_owned():
            self.manager.current = 'customization'
            return
        self._load_draft()
        self.name_input.text = self.name_text
        self._refresh_all()

    def on_leave(self, *args):
        if getattr(self, 'name_input', None) is not None:
            self.name_input.focus = False

    # ------------------------------------------------------------------
    # РАЗМЕТКА
    # ------------------------------------------------------------------
    def reposition_elements(self, instance, size):
        win_w, win_h = self.width, self.height
        if win_w <= 0 or win_h <= 0:
            return
        content_top = position_header(self.title_label, self.btn_back, win_w, win_h)
        side, gap = dp(15), dp(10)
        inner_w = win_w - 2 * side

        btn_h = min(max(win_h * 0.075, dp(54)), dp(66))
        bar_h = dp(12) + btn_h + BOTTOM_SAFE_MARGIN
        line_h = max(dp(1.2), 1)
        self.bottom_bar.size = (win_w, bar_h)
        self.bottom_bar.pos = (0, 0)
        self._bar_bg.pos = (0, 0)
        self._bar_bg.size = (win_w, bar_h)
        self._bar_line.pos = (0, bar_h - line_h)
        self._bar_line.size = (win_w, line_h)
        btn_w = (win_w - side * 2 - gap) / 2.0
        for i, btn in enumerate((self.btn_reset, self.btn_apply)):
            btn.size = (btn_w, btn_h)
            btn.pos = (round(side + i * (btn_w + gap)), round(BOTTOM_SAFE_MARGIN))

        # --- вертикальная раскладка сверху вниз ---
        # Блоки: название, превью, лента элементов, панель цвета. Нехватка места
        # забирается сначала у превью, потом у высоты ползунков, потом у промежутков;
        # запас места делится между превью и промежутками - никаких наездов друг на друга.
        avail = content_top - bar_h
        name_h = dp(52)
        chip_h = dp(48)
        slots_h = chip_h + dp(8)
        head_h, row_h = dp(44), dp(40)
        ratio = ThemePreviewBoard.metrics(1.0)['h']
        prev_nat = ratio * inner_w
        prev_min = ratio * min(inner_w, dp(220))
        g = dp(10)

        def picker_height(rh):
            return dp(14) + head_h + dp(6) + 3 * rh + dp(10)

        prev_h = prev_nat
        need = name_h + prev_h + slots_h + picker_height(row_h) + 5 * g
        if need > avail:
            deficit = need - avail
            cut = min(deficit, max(prev_h - prev_min, 0))
            prev_h -= cut
            deficit -= cut
            if deficit > 0:
                dr = min(deficit / 3.0, dp(8))
                row_h -= dr
                deficit -= 3 * dr
            if deficit > 0:
                g = max(dp(4), g - deficit / 5.0)
        else:
            slack = avail - need
            extra = min(slack * 0.5, prev_nat * 0.25)
            prev_h += extra
            slack -= extra
            g += min(slack / 5.0, dp(14))

        self._head_h, self._row_h = head_h, row_h
        picker_h = picker_height(row_h)

        y = content_top - g
        self.name_card.size = (inner_w, name_h)
        self.name_card.pos = (side, y - name_h)
        self._layout_name_card()
        y -= name_h + g

        prev_w = min(inner_w, prev_h / ratio)
        self.preview.size = (prev_w, prev_h)
        self.preview.pos = (side + (inner_w - prev_w) / 2.0, y - prev_h)
        y -= prev_h + g

        self.slot_scroll.size = (win_w, slots_h)
        self.slot_scroll.pos = (0, y - slots_h)
        self.slot_row.height = slots_h
        for chip in self.slot_chips:
            chip.fit_to_height(chip_h)
        y -= slots_h + g

        self.picker.size = (inner_w, picker_h)
        self.picker.pos = (side, y - picker_h)
        self._layout_picker()

    def _layout_name_card(self):
        c = self.name_card
        w, h = c.width, c.height
        x0, y0 = round(c.x), round(c.y)
        self._name_bg.pos = (x0, y0)
        self._name_bg.size = (round(w), round(h))
        half = dp(1.2) / 2.0
        r = dp(14)
        self._name_border.rounded_rectangle = (x0 + half, y0 + half, max(round(w) - 2 * half, 0),
                                               max(round(h) - 2 * half, 0), r, r, r, r)
        icon = dp(22)
        self.name_icon.size = (icon, icon)
        self.name_icon.pos = (round(x0 + dp(14)), round(y0 + (h - icon) / 2.0))
        self.name_caption.font_size = f"{dp(13)}px"
        self.name_caption.texture_update()
        cw, ch = self.name_caption.texture_size
        self.name_caption.size = (cw, ch)
        self.name_caption.pos = (round(x0 + dp(14) + icon + dp(10)), round(y0 + (h - ch) / 2.0))
        in_x = self.name_caption.right + dp(8)
        self.name_input.font_size = f"{dp(18)}px"
        self._name_geom = (in_x, max(x0 + w - dp(10) - in_x, dp(40)), y0, h)
        self._fit_name_input()
        # Kivy обновляет высоту строки (line_height) не сразу после смены шрифта/текста,
        # поэтому подгоняем поле ещё раз, когда он закончит пересчёт.
        Clock.schedule_once(self._fit_name_input, 0.05)

    def _fit_name_input(self, *args):
        """Высота поля = реальная строка + запас; строка стоит ровно по центру карточки."""
        geom = getattr(self, '_name_geom', None)
        ti = getattr(self, 'name_input', None)
        if geom is None or ti is None:
            return
        in_x, in_w, y0, h = geom
        line_h = int(round(ti.line_height))
        slack = max(int(round(dp(8))), 4)
        box_h = line_h + slack
        top_pad = slack // 2                      # строка по центру поля
        bottom_pad = max(slack - top_pad - 2, 0)  # окно просмотра = строка + 2 px запаса
        new_size = (in_w, box_h)
        new_pos = (round(in_x), round(y0 + (h - box_h) / 2.0))
        new_pad = [dp(4), top_pad, dp(4), bottom_pad]
        if list(ti.size) != list(new_size):
            ti.size = new_size
        if tuple(ti.pos) != new_pos:
            ti.pos = new_pos
        if list(ti.padding) != new_pad:
            ti.padding = new_pad
        if ti.scroll_y != 0:
            ti.scroll_y = 0

    def _layout_picker(self):
        p = self.picker
        w, h = p.width, p.height
        x0, y0 = round(p.x), round(p.y)
        self._picker_bg.pos = (x0, y0)
        self._picker_bg.size = (round(w), round(h))
        half = dp(1.2) / 2.0
        r = dp(16)
        self._picker_border.rounded_rectangle = (x0 + half, y0 + half, max(round(w) - 2 * half, 0),
                                                 max(round(h) - 2 * half, 0), r, r, r, r)
        padx = dp(14)
        head_top = y0 + h - dp(14)
        sw = self._head_h * 0.82
        sw_y = head_top - self._head_h / 2.0 - sw / 2.0
        self._picker_sw.pos = (round(x0 + padx), round(sw_y))
        self._picker_sw.size = (round(sw), round(sw))
        sr = dp(10)
        self._picker_sw_border.rounded_rectangle = (round(x0 + padx) + half, round(sw_y) + half,
                                                    max(round(sw) - 2 * half, 0), max(round(sw) - 2 * half, 0),
                                                    sr, sr, sr, sr)
        tx = x0 + padx + sw + dp(10)
        text_w = max(x0 + w - padx - tx - dp(120), dp(60))
        half_h = self._head_h / 2.0
        self.cur_label.font_size = f"{dp(16)}px"
        self.cur_label.size = (text_w, half_h)
        self.cur_label.text_size = self.cur_label.size
        self.cur_label.pos = (round(tx), round(head_top - half_h))
        self.cur_hex.font_size = f"{dp(12)}px"
        self.cur_hex.size = (text_w, half_h)
        self.cur_hex.text_size = self.cur_hex.size
        self.cur_hex.pos = (round(tx), round(head_top - self._head_h))
        self._layout_contrast_chip()

        cap_w = dp(64)
        rows_top = head_top - self._head_h - dp(6)
        for i in range(3):
            ry = rows_top - (i + 1) * self._row_h
            cap = self.row_captions[i]
            cap.font_size = f"{dp(12)}px"
            cap.size = (cap_w, self._row_h)
            cap.text_size = cap.size
            cap.pos = (round(x0 + padx), round(ry))
            sx = x0 + padx + cap_w + dp(8)
            self.sliders[i].size = (max(x0 + w - padx - sx, dp(40)), self._row_h)
            self.sliders[i].pos = (round(sx), round(ry))

    def _layout_contrast_chip(self):
        p = self.picker
        chip = self.contrast_chip
        chip.update_size(dp(26), font_scale=0.46)
        head_top = p.y + p.height - dp(14)
        chip.pos = (round(p.x + p.width - dp(14) - chip.width),
                    round(head_top - self._head_h / 2.0 - chip.height / 2.0))

    # ------------------------------------------------------------------
    # ОБНОВЛЕНИЕ
    # ------------------------------------------------------------------
    def _cur_key(self):
        return CUSTOM_SLOTS[self.slot_index][0]

    def _select_slot(self, idx):
        self.slot_index = idx
        self._refresh_all()

    def _on_slider(self, which, value):
        key = self._cur_key()
        h, s, v = self.draft[key]
        if which == 0:
            h = min(value, 0.9999)
        elif which == 1:
            s = value
        else:
            v = value
        self.draft[key] = (h, s, v)
        self._refresh_live()

    def _on_name_text(self, instance, value):
        self.name_text = value
        self._refresh_buttons()
        # после ввода Kivy пересчитывает высоту строки в следующих кадрах - подгоняем поле заново
        Clock.schedule_once(self._fit_name_input, 0.05)

    def _on_reset(self, *args):
        self._load_defaults()
        self.name_input.text = self.name_text
        self._refresh_all()

    def _on_apply(self, *args):
        stats = self._stats()
        name = (self.name_text.strip() or CUSTOM_DEFAULT_NAME)[:CUSTOM_NAME_MAX]
        self.name_text = name
        stats['custom_theme'] = {'name': name, 'colors': self._draft_hex()}
        sync_custom_theme()
        # choose_theme сохраняет прогресс и перекрашивает приложение (в т.ч. этот экран)
        Clock.schedule_once(lambda dt: choose_theme(CUSTOM_THEME_ID), 0)

    def _refresh_all(self):
        for i, chip in enumerate(self.slot_chips):
            chip.set_selected(i == self.slot_index)
        key = self._cur_key()
        self.cur_label.text = CUSTOM_SLOTS[self.slot_index][1]
        h, s, v = self.draft[key]
        self.sliders[0].set_value(h)
        self.sliders[1].set_value(s)
        self.sliders[2].set_value(v)
        self._refresh_live()

    def _refresh_live(self):
        colors = self._draft_rgba()
        self.preview.set_colors(colors)
        for (key, _), chip in zip(CUSTOM_SLOTS, self.slot_chips):
            chip.set_rgba(colors[key])
        key = self._cur_key()
        h, s, v = self.draft[key]
        self._picker_sw_color.rgba = colors[key]
        self.cur_hex.text = rgba_to_hex(colors[key])
        self.sliders[1].set_gradient([_hsv_to_rgba(h, 0, v), _hsv_to_rgba(h, 1, v)])
        self.sliders[2].set_gradient([_hsv_to_rgba(h, s, 0), _hsv_to_rgba(h, s, 1)])

        readable = contrast_ratio(colors['color_text'], colors['color_bg']) >= 3.0
        self.contrast_chip.dot_color_instr.rgba = color_correct if readable else color_in_word
        self.contrast_chip.label.text = "ЧИТАЕТСЯ" if readable else "МАЛО КОНТРАСТА"
        self._layout_contrast_chip()
        self._refresh_buttons()

    def _refresh_buttons(self):
        saved_name, saved_colors = get_custom_theme_data()
        name = (self.name_text.strip() or CUSTOM_DEFAULT_NAME)[:CUSTOM_NAME_MAX]
        is_active = self._stats().get("active_theme_name") == CUSTOM_THEME_ID
        same = (name == saved_name and self._draft_hex() == saved_colors)
        state = "done" if (is_active and same) else "apply"
        if state == self._btn_state:
            return
        self._btn_state = state
        if state == "done":
            self.btn_apply.set_content("ПРИМЕНЕНО", "done", icon_name="circle-check.png")
        else:
            self.btn_apply.set_content("ПРИМЕНИТЬ", "primary", on_release=self._on_apply)


class CustomizationScreen(StatCardsMixin, BaseScreen):
    FILTER_TABS = [
        ("all", "ВСЕ"),
        ("owned", "ОТКРЫТО"),
        ("shop", "МАГАЗИН"),
    ]
    FREE_THEMES = ('classic', 'night')
    SELL_PRICE = 900

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_filter = "all"
        self.theme_cards = {}
        self.layout = None
        self.active_theme_id = self._read_active_theme()
        self.selected_theme_id = self.active_theme_id

        self._build_ui()
        self.bind(size=self.reposition_elements)
        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    # ------------------------------------------------------------------
    # ДАННЫЕ
    # ------------------------------------------------------------------
    def _stats(self):
        if 'MOBILE_PLAYER_STATS' in globals() and MOBILE_PLAYER_STATS is not None:
            return MOBILE_PLAYER_STATS
        return {}

    def _read_active_theme(self):
        name = self._stats().get("active_theme_name", "classic")
        return name if name in color_themes else "classic"

    def _is_unlocked(self, theme_id):
        data = color_themes[theme_id]
        if theme_id in self.FREE_THEMES or data.get("price", 0) == 0:
            return True
        return bool(self._stats().get("unlocked_themes", {"classic": True}).get(theme_id, False))

    # ------------------------------------------------------------------
    # СБОРКА ИНТЕРФЕЙСА (вызывается заново при смене темы - всё перекрашивается)
    # ------------------------------------------------------------------
    def _build_ui(self):
        self.layout = FloatLayout()

        self.btn_back = IconMenuButton(size_hint=(None, None), size=(dp(48), dp(48)))
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(self.btn_back)

        self.title_label = Label(text="Кастомизация", font_name=font_path("ClearSans-Bold.ttf"),
                                 bold=True, color=color_text, size_hint=(None, None),
                                 halign='left', valign='middle')
        self.layout.add_widget(self.title_label)

        # --- 3 карточки статистики (без прокрутки - всегда помещаются) ---
        self.stats_row = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(None, None))
        self._stat_cards = {}
        for key, icon_name, label_text in [("coins", "copyright.png", "Монеты"),
                                           ("theme", "palette.png", "Тема"),
                                           ("status", "circle-check.png", "Статус")]:
            card = self.create_stat_card(icon_name, label_text)
            self.stats_row.add_widget(card)
            self._stat_cards[key] = card
        self.layout.add_widget(self.stats_row)

        # --- табы-фильтры ---
        self.tabs_row = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(None, None))
        self._tab_buttons = {}
        for key, label_text in self.FILTER_TABS:
            btn = FilterTabButton(text=label_text, size_hint=(1, 1),
                                  on_select_callback=lambda inst, k=key: self._on_tab_selected(k))
            btn.selected = (key == self.current_filter)
            btn.update_visual()
            self.tabs_row.add_widget(btn)
            self._tab_buttons[key] = btn
        self.layout.add_widget(self.tabs_row)

        # --- сетка карточек тем ---
        self.scroll_view = SharpScrollView(size_hint=(1, None), do_scroll_x=False,
                                           do_scroll_y=True, bar_width=0)
        self.scroll_view.effect_cls = ScrollEffect
        # content: [широкая карточка "Своя тема"] + [сетка тем в 2 колонки]
        self.content = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=None,
                                 padding=[dp(15), dp(4), dp(15), dp(24)])
        self.content.bind(minimum_height=self.content.setter('height'))
        self.grid = GridLayout(cols=2, spacing=dp(12), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.content.add_widget(self.grid)
        self.scroll_view.add_widget(self.content)
        self.layout.add_widget(self.scroll_view)

        self.theme_cards = {}
        for t_id, t_data in color_themes.items():
            if t_id == CUSTOM_THEME_ID:
                self.theme_cards[t_id] = CustomThemeCard(theme_id=t_id, theme_data=t_data,
                                                         on_click_callback=self.select_theme)
            else:
                self.theme_cards[t_id] = ThemeCard(theme_id=t_id, theme_data=t_data,
                                                   on_click_callback=self.select_theme)

        # --- нижняя панель с кнопками ---
        self.bottom_bar = FloatLayout(size_hint=(None, None))
        with self.bottom_bar.canvas.before:
            self._bar_bg_color = Color(*color_bg)
            self._bar_bg = Rectangle(pos=(0, 0), size=(0, 0))
            self._bar_line_color = Color(*color_blank)
            self._bar_line = Rectangle(pos=(0, 0), size=(0, 0))
        self.btn_action = ThemeActionButton()
        self.btn_sell = ThemeActionButton()
        self.bottom_bar.add_widget(self.btn_action)
        self.bottom_bar.add_widget(self.btn_sell)
        self.layout.add_widget(self.bottom_bar)

        self.add_widget(self.layout)

        self._apply_filter()
        self._refresh_cards_state()
        self._refresh_panels()

    def apply_theme_instant(self):
        """Вызывается из redraw_all_screens: пересобираем экран под новые цвета."""
        self.active_theme_id = self._read_active_theme()
        sy = self.scroll_view.scroll_y if getattr(self, 'scroll_view', None) else 1.0
        if self.layout is not None:
            self.remove_widget(self.layout)
        self._build_ui()
        self.reposition_elements(None, None)
        self.scroll_view.scroll_y = sy

    def on_pre_enter(self, *args):
        self.active_theme_id = self._read_active_theme()
        self._apply_filter()
        self._refresh_cards_state()
        self._refresh_panels()

    # ------------------------------------------------------------------
    # РАЗМЕТКА
    # ------------------------------------------------------------------
    def reposition_elements(self, instance, size):
        win_w, win_h = self.width, self.height
        if win_w <= 0 or win_h <= 0:
            return

        content_top = position_header(self.title_label, self.btn_back, win_w, win_h)
        side = dp(15)
        gap = dp(10)

        # статистика
        stats_h = min(max(win_h * 0.13, dp(88)), dp(112))
        card_w = (win_w - side * 2 - gap * 2) / 3.0
        self.stats_row.spacing = gap
        self.stats_row.size = (win_w - side * 2, stats_h)
        self.stats_row.pos = (side, content_top - stats_h)
        for card in self.stats_row.children:
            card.size = (card_w, stats_h)
            self._layout_stat_card(card)

        # табы
        tabs_h = min(max(win_h * 0.055, dp(40)), dp(50))
        self.tabs_row.size = (win_w - side * 2, tabs_h)
        self.tabs_row.pos = (side, self.stats_row.y - dp(16) - tabs_h)
        list_top = self.tabs_row.y - dp(14)

        # нижняя панель
        btn_h = min(max(win_h * 0.075, dp(54)), dp(66))
        bar_h = dp(12) + btn_h + BOTTOM_SAFE_MARGIN
        line_h = max(dp(1.2), 1)
        self.bottom_bar.size = (win_w, bar_h)
        self.bottom_bar.pos = (0, 0)
        self._bar_bg.pos = (0, 0)
        self._bar_bg.size = (win_w, bar_h)
        self._bar_line.pos = (0, bar_h - line_h)
        self._bar_line.size = (win_w, line_h)
        btn_w = (win_w - side * 2 - gap) / 2.0
        for i, btn in enumerate((self.btn_action, self.btn_sell)):
            btn.size = (btn_w, btn_h)
            btn.pos = (round(side + i * (btn_w + gap)), round(BOTTOM_SAFE_MARGIN))

        # список
        self.scroll_view.pos = (0, bar_h)
        self.scroll_view.size = (win_w, max(list_top - bar_h, dp(10)))
        self.content.width = win_w
        self._size_cards()

    def _size_cards(self):
        scroll_w = self.scroll_view.width
        if scroll_w <= dp(100):
            return
        card_w = int((scroll_w - dp(15) * 2 - dp(12)) // 2)
        card_h = round(ThemeCard.metrics(card_w)['h'])
        for t_id, card in self.theme_cards.items():
            if t_id != CUSTOM_THEME_ID:
                card.size = (card_w, card_h)
        custom_card = self.theme_cards.get(CUSTOM_THEME_ID)
        if custom_card is not None:
            wide_w = int(scroll_w - dp(15) * 2)
            custom_card.size = (wide_w, round(CustomThemeCard.metrics(wide_w)['h']))

    # ------------------------------------------------------------------
    # ТАБЫ
    # ------------------------------------------------------------------
    def _on_tab_selected(self, key):
        if key == self.current_filter:
            return
        self.current_filter = key
        for k, btn in self._tab_buttons.items():
            btn.selected = (k == key)
            btn.update_visual()
        self._apply_filter()

    def _apply_filter(self):
        self.grid.clear_widgets()
        self.content.clear_widgets()
        custom_card = None
        for t_id, card in self.theme_cards.items():
            owned = self._is_unlocked(t_id)
            if self.current_filter == "owned" and not owned:
                continue
            if self.current_filter == "shop" and owned:
                continue
            if t_id == CUSTOM_THEME_ID:
                custom_card = card
            else:
                self.grid.add_widget(card)
        if custom_card is not None:
            self.content.add_widget(custom_card)
        if self.grid.children:
            self.content.add_widget(self.grid)
        self._size_cards()

    # ------------------------------------------------------------------
    # СОСТОЯНИЕ
    # ------------------------------------------------------------------
    def _refresh_cards_state(self):
        for t_id, card in self.theme_cards.items():
            card.is_selected = (t_id == self.selected_theme_id)
            card.set_state(self._is_unlocked(t_id), t_id == self.active_theme_id)

    def _set_stat(self, card, value, value_color, icon_name, icon_color):
        card.value_ref.text = value
        card.value_ref.color = value_color
        card.icon_ref.texture = load_white_icon_texture(icon_path(icon_name))
        card.icon_ref.color = icon_color
        self._layout_stat_card(card)

    def _refresh_panels(self):
        stats = self._stats()
        coins = stats.get('player_coins', 0)
        theme_id = self.selected_theme_id
        data = color_themes[theme_id]
        owned = self._is_unlocked(theme_id)
        is_active = (theme_id == self.active_theme_id)
        price = data.get('price', 1000)

        # --- карточки статистики ---
        self._set_stat(self._stat_cards['coins'], str(coins), color_text, "copyright.png", color_in_word)
        self._set_stat(self._stat_cards['theme'], data.get("color_name", theme_id.capitalize()),
                       color_text, "palette.png", color_text)
        if owned and is_active:
            self._set_stat(self._stat_cards['status'], "Применено", color_correct, "circle-check.png", color_correct)
        elif owned:
            self._set_stat(self._stat_cards['status'], "Открыто", color_text, "circle-check.png", color_not_in_word)
        else:
            self._set_stat(self._stat_cards['status'], "Закрыто", color_text, "lock.png", color_not_in_word)

        # --- главная кнопка ---
        if theme_id == CUSTOM_THEME_ID:
            # своя тема: слева ПРИМЕНИТЬ / КУПИТЬ, справа РЕДАКТОР (продавать её нельзя)
            if not owned and coins >= price:
                self.btn_action.set_content("КУПИТЬ", "primary", pill_text=str(price),
                                            on_release=self.process_theme_action)
            elif not owned:
                self.btn_action.set_content("КУПИТЬ", "disabled", pill_text=str(price))
            elif is_active:
                self.btn_action.set_content("ПРИМЕНЕНО", "done", icon_name="circle-check.png")
            else:
                self.btn_action.set_content("ПРИМЕНИТЬ", "primary", on_release=self.process_theme_action)
            if owned:
                self.btn_sell.set_content("РЕДАКТОР", "secondary", icon_name="pencil.png",
                                          on_release=self._open_editor)
            else:
                self.btn_sell.set_content("РЕДАКТОР", "disabled", icon_name="pencil.png")
            return

        if owned and is_active:
            self.btn_action.set_content("ПРИМЕНЕНО", "done", icon_name="circle-check.png")
        elif owned:
            self.btn_action.set_content("ПРИМЕНИТЬ", "primary", on_release=self.process_theme_action)
        elif coins >= price:
            self.btn_action.set_content("КУПИТЬ", "primary", pill_text=str(price),
                                        on_release=self.process_theme_action)
        else:
            self.btn_action.set_content("КУПИТЬ", "disabled", pill_text=str(price))

        # --- кнопка продажи ---
        if owned and theme_id not in self.FREE_THEMES and price > 0:
            self.btn_sell.set_content("ПРОДАТЬ", "secondary", pill_text=f"+{self.SELL_PRICE}",
                                      on_release=self.process_theme_sell)
        else:
            self.btn_sell.set_content("ПРОДАТЬ", "disabled", pill_text=f"+{self.SELL_PRICE}")

    def _open_editor(self, instance=None):
        if self._is_unlocked(CUSTOM_THEME_ID):
            self.manager.current = 'theme_editor'

    def select_theme(self, theme_id):
        self.selected_theme_id = theme_id
        for t_id, card in self.theme_cards.items():
            new_selected = (t_id == theme_id)
            if card.is_selected != new_selected:
                card.is_selected = new_selected
                card.update_indicators()
        self._refresh_panels()

    # ------------------------------------------------------------------
    # ДЕЙСТВИЯ
    # ------------------------------------------------------------------
    def process_theme_action(self, instance=None):
        stats = self._stats()
        theme_id = self.selected_theme_id
        data = color_themes[theme_id]

        if self._is_unlocked(theme_id):
            if theme_id == self.active_theme_id:
                return
        else:
            price = data.get('price', 1000)
            coins = stats.get('player_coins', 0)
            if coins < price:
                return
            stats['player_coins'] = coins - price
            stats.setdefault('unlocked_themes', {"classic": True})[theme_id] = True

        self.active_theme_id = theme_id
        self._refresh_cards_state()
        self._refresh_panels()
        # choose_theme сохраняет прогресс и перекрашивает экран (apply_theme_instant);
        # вызываем на следующем кадре, чтобы не пересобирать кнопку прямо в её же обработчике
        Clock.schedule_once(lambda dt: choose_theme(theme_id), 0)
        print(f"[MGGamesStudio] Тема {theme_id} применена!")

    def process_theme_sell(self, instance=None):
        stats = self._stats()
        theme_id = self.selected_theme_id
        if theme_id in self.FREE_THEMES or theme_id == CUSTOM_THEME_ID or not self._is_unlocked(theme_id):
            return

        stats['player_coins'] = stats.get('player_coins', 0) + self.SELL_PRICE
        stats.setdefault('unlocked_themes', {"classic": True})[theme_id] = False

        was_active = (theme_id == self.active_theme_id)
        if was_active:
            self.active_theme_id = 'classic'

        if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
            MOBILE_SAVE_FUNC(stats)

        self._apply_filter()
        self._refresh_cards_state()
        self._refresh_panels()
        if was_active:
            Clock.schedule_once(lambda dt: choose_theme('classic'), 0)
        print(f"[MGGamesStudio] Тема {theme_id} продана за {self.SELL_PRICE} монет!")



class RewardBadge(FloatLayout):
    """
    Плашка награды квеста: иконка монеты + сумма ("+50").
    Устроена так же, как заполненная RarityBadge (фон color_key, скругление
    на всю высоту, ширина считается от фактической ширины текста), только
    вместо цветной точки - монета, та же иконка, что у карточки "Монеты".
    """
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)

        with self.canvas.before:
            self.bg_color_instr = Color(*color_key)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

        self.icon = Image(size_hint=(None, None), fit_mode="contain", color=color_in_word)
        self.icon.texture = load_white_icon_texture(icon_path("copyright.png"))
        self.add_widget(self.icon)

        self.label = Label(
            text=text,
            font_name=font_path("ClearSans-Bold.ttf"),
            bold=True,
            color=color_text,
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )
        self.add_widget(self.label)
        self.bind(pos=self._sync_graphics, size=self._sync_graphics)

    def update_size(self, height, font_scale=0.52):
        _k = (round(height, 2), font_scale, self.label.text)
        if _k == getattr(self, '_size_key', None):
            return
        self._size_key = _k
        self.height = height
        self.label.font_size = f"{max(int(height * font_scale), 12)}px"
        self._cap_dy = cap_ink_offset_y(max(int(height * font_scale), 12))
        self.label.text_size = (None, None)
        self.label.texture_update()
        icon_d = height * 0.5
        pad_x = height * 0.42
        gap = dp(5)
        text_w = self.label.texture_size[0]
        self.width = pad_x * 2 + icon_d + gap + text_w
        self.label.size = (text_w, height)
        self.label.text_size = (text_w, height)
        self._sync_graphics()

    def _sync_graphics(self, *args):
        pos = (round(self.x), round(self.y))
        size = (round(self.width), round(self.height))
        self.bg_rect.pos = pos
        self.bg_rect.size = size
        self.bg_rect.radius = [round(self.height / 2.0)]
        if self.height <= 0:
            return
        icon_d = round(self.height * 0.5)
        pad_x = self.height * 0.42
        gap = dp(5)
        self.icon.size = (icon_d, icon_d)
        self.icon.pos = (round(self.x + pad_x), round(self.y + (self.height - icon_d) / 2))
        label_x = self.x + pad_x + icon_d + gap
        self.label.pos = (round(label_x), round(pos[1] - getattr(self, '_cap_dy', 0.0)))
        self.label.size = (max(round(self.width - (label_x - self.x)), dp(4)), size[1])
        self.label.text_size = self.label.size


class QuestsScreen(StatCardsMixin, BaseScreen):
    # Табы-фильтры списка: (ключ фильтра, подпись на кнопке)
    FILTER_TABS = [
        ("all", "ВСЕ"),
        ("active", "АКТИВНЫЕ"),
        ("done", "ВЫПОЛНЕНО"),
    ]
    # Легенда редкости: (ключ типа, подпись)
    RARITY_LEGEND = [
        ("common", "Обычное"),
        ("rare", "Редкое"),
        ("epic", "Эпическое"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.stub_layout = create_stub_layout(self, "")
        self.layout.add_widget(self.stub_layout)

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

        # ----- горизонтально прокручиваемая строка статистики -----
        self.stats_scroll = SharpScrollView(size_hint=(1, None), do_scroll_x=True, do_scroll_y=False, bar_width=0)
        self.stats_scroll.effect_cls = ScrollEffect

        self.stats_row = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(None, None))
        self.stats_row.bind(minimum_width=self.stats_row.setter('width'))
        self.stats_scroll.add_widget(self.stats_row)
        self.layout.add_widget(self.stats_scroll)

        stat_defs = [
            ("coins", "copyright.png", "Монеты"),
            ("wins", "trophy.png", "Победы"),
            ("losses", "trophy-off.png", "Поражения"),
            ("streak", "flame.png", "Серия побед"),
            ("quests", "clipboard-text.png", "Выполнено"),
        ]
        self._stat_cards = {}
        for key, icon_name, label_text in stat_defs:
            card = self.create_stat_card(icon_name, label_text)
            self.stats_row.add_widget(card)
            self._stat_cards[key] = card

        # ----- табы-фильтры -----
        self.tabs_row = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(None, None))
        self.layout.add_widget(self.tabs_row)

        self.current_filter = "all"
        self._tab_buttons = {}
        for key, label_text in self.FILTER_TABS:
            btn = FilterTabButton(
                text=label_text,
                size_hint=(1, 1),
                on_select_callback=lambda inst, k=key: self._on_tab_selected(k)
            )
            btn.selected = (key == self.current_filter)
            btn.update_visual()
            self.tabs_row.add_widget(btn)
            self._tab_buttons[key] = btn

        # ----- строка-легенда редкости -----
        self.legend_row = BoxLayout(orientation='horizontal', spacing=dp(18), size_hint=(None, None))
        self.legend_row.bind(minimum_width=self.legend_row.setter('width'))
        self.layout.add_widget(self.legend_row)

        legend_colors = {"common": color_not_in_word, "rare": color_in_word, "epic": color_correct}
        self._legend_dots = {}
        for type_key, label_text in self.RARITY_LEGEND:
            dot = RarityBadge(dot_color=legend_colors[type_key], text=label_text, filled=False)
            self.legend_row.add_widget(dot)
            self._legend_dots[type_key] = dot

        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        # ----- прокручиваемый список карточек квестов -----
        self.scroll_view = SharpScrollView(size_hint=(1, None), do_scroll_x=False, do_scroll_y=True, bar_width=0)
        self.scroll_view.effect_cls = ScrollEffect

        # Те же отступы, что и у списка достижений: dp(15) по бокам, небольшой
        # верхний отступ, чтобы обводка первой карточки не упиралась в подложку шапки.
        self.quests_list_layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[dp(15), dp(6), dp(15), dp(20)])
        self.quests_list_layout.bind(minimum_height=self.quests_list_layout.setter('height'))
        self.scroll_view.add_widget(self.quests_list_layout)
        self.layout.add_widget(self.scroll_view)

        # список рисуется под подложкой шапки
        self.layout.remove_widget(self.scroll_view)
        self.layout.add_widget(self.scroll_view, index=len(self.layout.children))

        self._quests_last_signature = None
        self._quests_build_event = None
        self._quest_cards = []  # [(widget, done_bool), ...] - табы переключаются мгновенно, без пересборки

        self.reposition_elements(None, None)
        Clock.schedule_once(lambda dt: self.reposition_elements(None, None), 0)

    def on_pre_enter(self, *args):
        self.refresh_quests_data()
        self._speed_up_build()

    def prepare_in_background(self):
        self.refresh_quests_data(background=True)

    # ------------------------------------------------------------------
    # РАЗМЕТКА ЭКРАНА
    # ------------------------------------------------------------------
    def reposition_elements(self, instance, size):
        win_w = self.width
        win_h = self.height
        if win_w <= 0 or win_h <= 0:
            return

        back_w, back_h = dp(48), dp(48)
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

        header_bottom = (back_btn.y if back_btn is not None else win_h - TOP_SAFE_MARGIN - back_h) - dp(14)

        # --- строка статистики ---
        cards_bottom = self._layout_stats_strip(win_w, win_h, header_bottom)

        # --- табы-фильтры ---
        tabs_h = min(max(win_h * 0.055, dp(40)), dp(50))
        tabs_top = cards_bottom - dp(16)
        self.tabs_row.size = (win_w - dp(30), tabs_h)
        self.tabs_row.pos = (dp(15), tabs_top - tabs_h)

        # --- легенда редкости (на узком экране сжимается, пока не влезет в ширину) ---
        legend_available_w = max(win_w - dp(30), dp(10))
        legend_h = min(max(win_h * 0.04, dp(24)), dp(32))
        legend_min_h = dp(15)
        legend_gap = dp(18)

        def _legend_layout(h, gap):
            self.legend_row.spacing = gap
            for type_key, _ in self.RARITY_LEGEND:
                self._legend_dots[type_key].update_size(h, font_scale=0.62)
            return sum(self._legend_dots[k].width for k, _ in self.RARITY_LEGEND) + gap * (len(self.RARITY_LEGEND) - 1)

        legend_total_w = _legend_layout(legend_h, legend_gap)
        shrink_steps = 0
        while legend_total_w > legend_available_w and legend_h > legend_min_h and shrink_steps < 20:
            legend_h = max(legend_min_h, legend_h - dp(1))
            legend_gap = max(dp(8), legend_gap - dp(1))
            legend_total_w = _legend_layout(legend_h, legend_gap)
            shrink_steps += 1

        legend_top = self.tabs_row.y - dp(14)
        self.legend_row.height = legend_h
        self.legend_row.pos = (dp(15), legend_top - legend_h)

        list_top = self.legend_row.y - dp(16)

        # --- фоновая подложка шапки (чтобы список не наезжал на неё при скролле) ---
        overlay_h = max(win_h - list_top, 0)
        self.top_overlay.height = overlay_h
        self.top_overlay.pos = (0, list_top)
        self.overlay_rect.size = (win_w, overlay_h)
        self.overlay_rect.pos = (0, list_top)

        # --- список квестов ---
        self.scroll_view.size = (win_w, max(list_top - BOTTOM_SAFE_MARGIN, dp(10)))
        self.scroll_view.pos = (0, BOTTOM_SAFE_MARGIN)
        self.quests_list_layout.width = win_w

    # ------------------------------------------------------------------
    # ТАБЫ-ФИЛЬТРЫ
    # ------------------------------------------------------------------
    def _on_tab_selected(self, key):
        if key == self.current_filter:
            return
        self.current_filter = key
        for k, btn in self._tab_buttons.items():
            btn.selected = (k == key)
            btn.update_visual()
        self._apply_filter()

    def _apply_filter(self):
        self.quests_list_layout.clear_widgets()
        for widget, done in self._quest_cards:
            if self.current_filter == "active" and done:
                continue
            if self.current_filter == "done" and not done:
                continue
            self.quests_list_layout.add_widget(widget)

    # ------------------------------------------------------------------
    # КАРТОЧКА КВЕСТА (тот же макет, что у карточки достижения)
    # ------------------------------------------------------------------
    def create_quest_card(self, name, description, quest_data, progress, goal, reward, done):
        r_type = "common"
        if isinstance(quest_data, dict):
            r_type = str(quest_data.get("type", "common")).lower().strip()

        if r_type == "rare":
            dot_color = color_in_word
            type_text = "Редкое"
        elif r_type == "epic":
            dot_color = color_correct
            type_text = "Эпическое"
        else:
            dot_color = color_not_in_word
            type_text = "Обычное"

        try:
            goal = max(int(goal), 1)
        except (TypeError, ValueError):
            goal = 1
        try:
            progress = max(int(progress), 0)
        except (TypeError, ValueError):
            progress = 0

        show_progress = not done
        status_text = "ВЫПОЛНЕНО" if done else f"{min(progress, goal)} / {goal}"

        row = FloatLayout(size_hint_y=None, height=dp(140))

        with row.canvas.before:
            Color(*lerp_color(color_bg, color_key, 0.20))
            bg_rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(14)])
            Color(*color_blank)
            border_line = Line(width=dp(1.2), rounded_rectangle=(row.x, row.y, row.width, row.height, dp(14), dp(14), dp(14), dp(14)))

        def sync_bg(inst, val):
            # round() убирает субпиксельное дрожание рамки при некруглых размерах окна
            pos = (round(inst.x), round(inst.y))
            size = (round(inst.width), round(inst.height))
            bg_rect.pos = pos
            bg_rect.size = size
            border_line.rounded_rectangle = (pos[0], pos[1], size[0], size[1], dp(14), dp(14), dp(14), dp(14))
        row.bind(pos=sync_bg, size=sync_bg)

        content = FloatLayout(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        row.add_widget(content)

        q_font = font_path("ClearSans-Bold.ttf")
        name_lbl = Label(
            text=name.upper(), font_name=q_font, font_size='17sp', bold=True, color=color_text,
            size_hint=(None, None), halign='left', valign='top'
        )
        desc_lbl = Label(
            text=description, font_name=q_font, font_size='13sp', color=color_not_in_word,
            size_hint=(None, None), halign='left', valign='top'
        )
        status_icon = Image(size_hint=(None, None), fit_mode="contain", color=color_text)
        status_icon.texture = load_white_icon_texture(icon_path("check.png" if done else "clipboard-text.png"))

        badge = RarityBadge(dot_color=dot_color, text=type_text, filled=True)
        reward_badge = RewardBadge(text=f"+{reward}")

        lbl_status = Label(
            text=status_text, font_name=q_font, bold=True, color=(color_correct if done else color_not_in_word),
            size_hint=(None, None), halign='right', valign='middle'
        )

        for widget in (name_lbl, desc_lbl, status_icon, badge, reward_badge, lbl_status):
            content.add_widget(widget)

        progress_row = None
        prog_track = prog_fill = None
        if show_progress:
            progress_row = FloatLayout(size_hint=(None, None))
            with progress_row.canvas:
                Color(*color_blank)
                prog_track = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(4)])
                Color(*color_not_in_word)
                prog_fill = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[dp(4)])

            def sync_progress(inst, val):
                pos = (round(inst.x), round(inst.y))
                size = (round(inst.width), round(inst.height))
                prog_track.pos = pos
                prog_track.size = size
                ratio = max(0.0, min(1.0, progress / goal))
                prog_fill.pos = pos
                prog_fill.size = (round(size[0] * ratio), size[1])
            progress_row.bind(pos=sync_progress, size=sync_progress)
            content.add_widget(progress_row)

        PAD = dp(16)
        ICON_SIZE = dp(20)
        BADGE_H = dp(28)
        PROG_H = dp(8)
        GAP_S = dp(4)
        GAP_M = dp(10)
        GAP_BADGES = dp(8)

        def relayout(*args):
            w = row.width
            if w <= 0:
                return

            if getattr(relayout, '_w', None) != round(w):
                relayout._w = round(w)
                name_w = max(w - PAD * 2 - ICON_SIZE - dp(8), dp(10))
                name_lbl.text_size = (name_w, None)
                name_lbl.width = name_w
                name_lbl.texture_update()
                name_lbl.height = name_lbl.texture_size[1]

                desc_w = max(w - PAD * 2, dp(10))
                desc_lbl.text_size = (desc_w, None)
                desc_lbl.width = desc_w
                desc_lbl.texture_update()
                desc_lbl.height = desc_lbl.texture_size[1]

                badge.update_size(BADGE_H)
                reward_badge.update_size(BADGE_H)

                # статус ("2 / 3" / "ВЫПОЛНЕНО") занимает остаток нижней строки
                # справа от обеих плашек и сжимается, если места мало
                status_max_w = max(w - PAD * 2 - badge.width - reward_badge.width - GAP_BADGES * 2, dp(40))
                lbl_status.text_size = (None, None)
                fit_font_size(lbl_status, status_max_w, dp(13))
                lbl_status.texture_update()
                lbl_status.size = lbl_status.texture_size
                lbl_status.text_size = lbl_status.size

            total_h = PAD + name_lbl.height + GAP_S + desc_lbl.height + GAP_M
            if show_progress:
                total_h += PROG_H + GAP_M
            total_h += BADGE_H + PAD
            new_h = max(dp(96), total_h)
            row.height = new_h

            row_x, row_y = row.x, row.y
            name_top_y = row_y + new_h - PAD
            name_lbl.pos = (round(row_x + PAD), round(name_top_y - name_lbl.height))

            desc_top_y = name_top_y - name_lbl.height - GAP_S
            desc_lbl.pos = (round(row_x + PAD), round(desc_top_y - desc_lbl.height))

            status_icon.size = (ICON_SIZE, ICON_SIZE)
            status_icon.pos = (round(row_x + w - PAD - ICON_SIZE), round(name_top_y - ICON_SIZE))

            if show_progress:
                progress_row.size = (max(w - PAD * 2, dp(10)), PROG_H)
                progress_top_y = desc_top_y - desc_lbl.height - GAP_M
                progress_row.pos = (round(row_x + PAD), round(progress_top_y - PROG_H))
                badge_top_y = progress_top_y - PROG_H - GAP_M
            else:
                badge_top_y = desc_top_y - desc_lbl.height - GAP_M

            badge.pos = (round(row_x + PAD), round(badge_top_y - BADGE_H))
            reward_badge.pos = (round(badge.x + badge.width + GAP_BADGES), round(badge_top_y - BADGE_H))
            status_y = round(badge_top_y - BADGE_H / 2 - lbl_status.height / 2)
            lbl_status.pos = (round(row_x + w - PAD - lbl_status.width), status_y)

        name_lbl.bind(texture_size=relayout)
        desc_lbl.bind(texture_size=relayout)
        row.bind(pos=relayout, size=relayout)
        relayout()

        return row

    # ------------------------------------------------------------------
    # ПОСТРОЕНИЕ СПИСКА (по частям, чтобы не подвешивать кадр)
    # ------------------------------------------------------------------
    def _quest_visible(self, done):
        if self.current_filter == "active" and done:
            return False
        if self.current_filter == "done" and not done:
            return False
        return True

    def build_quests_list(self, launcher_quests, background=False):
        if self._quests_build_event is not None:
            self._quests_build_event.cancel()
            self._quests_build_event = None

        self.quests_list_layout.clear_widgets()
        self._quest_cards = []
        self._quests_remaining = []

        if not launcher_quests:
            return

        # невыполненные - сверху, выполненные - внизу
        sorted_keys = sorted(launcher_quests.keys(), key=lambda k: launcher_quests[k].get("done", False), reverse=False)
        self._quests_remaining = [(k, launcher_quests[k]) for k in sorted_keys]

        if background:
            self._quests_rows_per_tick = 1
            self._quests_build_event = Clock.schedule_interval(self._quests_build_tick, 0.03)
        else:
            self._quests_rows_per_tick = 4
            self._quests_build_tick(0)
            if self._quests_remaining:
                self._quests_build_event = Clock.schedule_interval(self._quests_build_tick, 0)

    def _quests_build_tick(self, dt):
        for _ in range(self._quests_rows_per_tick):
            if not self._quests_remaining:
                self._quests_build_event = None
                return False
            _key, q_data = self._quests_remaining.pop(0)
            done = q_data.get("done", False)
            card = self.create_quest_card(
                q_data.get("name", "Секретное задание"),
                q_data.get("description", ""),
                q_data,
                q_data.get("progress", 0),
                q_data.get("goal", 1),
                q_data.get("reward", 50),
                done,
            )
            self._quest_cards.append((card, done))
            if self._quest_visible(done):
                self.quests_list_layout.add_widget(card)
        return True

    def _speed_up_build(self):
        if self._quests_build_event is not None and self._quests_rows_per_tick < 4:
            self._quests_build_event.cancel()
            self._quests_build_event = None
            self._quests_rows_per_tick = 4
            self._quests_build_tick(0)
            if self._quests_remaining:
                self._quests_build_event = Clock.schedule_interval(self._quests_build_tick, 0)

    # ------------------------------------------------------------------
    # ОБНОВЛЕНИЕ СТАТИСТИКИ И СПИСКА
    # ------------------------------------------------------------------
    def refresh_quests_data(self, background=False):
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
        if signature == self._quests_last_signature:
            return
        self._quests_last_signature = signature

        stat_values = {
            "coins": str(coins),
            "wins": str(wins),
            "losses": str(losses),
            "streak": streak,
            "quests": quests_ratio,
        }
        for key, card in self._stat_cards.items():
            card.value_ref.text = stat_values.get(key, "0")

        self.reposition_elements(None, None)
        self.build_quests_list(launcher_quests, background=background)

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
    btn_back = IconMenuButton(
        size_hint=(None, None), 
        size=(dp(48), dp(48))
    )
    btn_back.pos = (Window.width - dp(48) - dp(14), Window.height - TOP_SAFE_MARGIN - dp(48))
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

        sync_custom_theme()
        if saved_theme not in color_themes:
            saved_theme = "classic"
        elif saved_theme == CUSTOM_THEME_ID and not MOBILE_PLAYER_STATS.get("unlocked_themes", {}).get(CUSTOM_THEME_ID):
            saved_theme = "classic"

        choose_theme(saved_theme)
        Window.clearcolor = color_bg

        sm = ThemedScreenManager(transition=NoTransition())

        self.loading_screen = LoadingScreen(name='loading')
        sm.add_widget(self.loading_screen)
        sm.current = 'loading'

        self._sm_ref = sm
        self._screens_to_build = list(_SCREEN_FACTORIES.items())
        self._screens_total = len(self._screens_to_build)
        Clock.schedule_once(self._build_next_screens, 0)

        return sm

    def _warm_up_screens(self, dt):
        # Когда всё построено, заранее готовим тяжёлые списки (в фоне, по одной карточке)
        sm = self._sm_ref
        for name in ('achievements', 'quests'):
            if sm.has_screen(name):
                scr = sm.get_screen(name)
                if scr is not sm.current_screen and hasattr(scr, 'prepare_in_background'):
                    scr.prepare_in_background()

    def _build_next_screens(self, dt):
        chunk_size = 2
        for _ in range(chunk_size):
            if not self._screens_to_build:
                break
            name, factory = self._screens_to_build.pop(0)
            self._sm_ref.add_widget(make_screen(name))

        done = self._screens_total - len(self._screens_to_build)
        self.loading_screen.set_progress(done / self._screens_total)

        if self._screens_to_build:
            Clock.schedule_once(self._build_next_screens, 0)
        else:
            self._sm_ref.current = 'main'
            Clock.schedule_once(lambda dt: self._sm_ref.remove_widget(self.loading_screen), 0)
            Clock.schedule_once(self._warm_up_screens, 0.6)

def start_mobile_game(words_list, player_stats, save_function):
    global MOBILE_ALL_WORDS, MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC, MOBILE_ACHIVEMENTS, MOBILE_QUESTS
    MOBILE_ALL_WORDS = words_list
    MOBILE_PLAYER_STATS = player_stats
    def _save_and_mark(stats):
        save_function(stats)
        mark_stats_dirty()   # Достижения/Квесты обновятся в фоне, до того как их откроют

    MOBILE_SAVE_FUNC = _save_and_mark

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