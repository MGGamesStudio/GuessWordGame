import os
import sys
import json
from platformdirs import user_data_dir
from kivy.utils import platform

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
    "q3": {"type": "common", "name": "В ПОИСКАХ ИСТИНЫ", "description": "Найдите хотя бы 5 жёлтых букв за одну игру.", "reward": 50, "goal": 1, "progress": 0, "done": False},
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

try:
    game_save_dir = user_data_dir("GuessWordGame", "MGGamesStudio")
    if not os.path.exists(game_save_dir):
        os.makedirs(game_save_dir)
    SAVE_FILE_PATH = os.path.join(game_save_dir, "guess_word_save_file_guess_word_save_file.json")
except Exception:
    SAVE_FILE_PATH = "guess_word_save_file_guess_word_save_file.json"

# Сохранение
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
        "unlocked_achivements": {}
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

ALL_WORDS = load_words_list()
PLAYER_STATS = load_game_progress()

print(f"[MGGamesStudio] Успешно загружено уникальных слов: {len(ALL_WORDS)}")

# Лаунчер
# "auto"    — игра сама определяет платформу (ПК на Pygame или телефон на Kivy)
# "pc"      — принудительно запустить ПК-версию на Pygame
# "mobile"  — принудительно запустить мобильную версию
DEV_MODE = "pc"
START_MOBILE = False

if platform in ('android', 'ios'):
    START_MOBILE = True
else:
    if DEV_MODE == "auto" or DEV_MODE == "pc":
        START_MOBILE = False
    elif DEV_MODE == "mobile":
        START_MOBILE = True

if START_MOBILE:
    os.environ["MGGAMES_MODE"] = "mobile"
    print("[MGGamesStudio] ЗАПУСК МОБИЛЬНОЙ ВЕРСИИ ИГРЫ")
    from kivy.config import Config
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '640')

    from kivy.core.window import Window
    Window.size = (360, 640)
    try:
        import guess_word_mobile_v110
        guess_word_mobile_v110.start_mobile_game(ALL_WORDS, PLAYER_STATS, save_game_progress) 
    except ModuleNotFoundError:
        print("[MGGamesStudio] Ошибка: Файл guess_word_mobile_v110.py не найден в этой папке!")
else:
    print("[MGGamesStudio] ЗАПУСК ПК ВЕРСИИ ИГРЫ")
    try:
        import guess_word_pc_v110
        guess_word_pc_v110.start_pc_game(ALL_WORDS, PLAYER_STATS, save_game_progress, achivements, all_quests)
    except ModuleNotFoundError:
        print("[MGGamesStudio] Ошибка: Файл guess_word_pc_v110.py не найден!")
