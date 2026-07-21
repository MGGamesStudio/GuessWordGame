import os
import sys
import json
import random
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
# "auto"   — игра сама определяет платформу (ПК на Pygame или телефон на Kivy)
# "1"      — ПК ВЕРСИЯ
# "2"      — МОБИЛЬНАЯ ВЕРСИЯ
DEV_MODE = "2"
START_MOBILE = False

if platform in ('android', 'ios'):
    START_MOBILE = True
else:
    if DEV_MODE == "auto" or DEV_MODE == "1":
        START_MOBILE = False
    elif DEV_MODE == "2":
        START_MOBILE = True

if START_MOBILE:
    os.environ["MGGAMES_MODE"] = "mobile"
    print("[MGGamesStudio] ЗАПУСК МОБИЛЬНОЙ ВЕРСИИ ИГРЫ")
    
    config_x = 360 # 360
    config_y = 640 # 640
    
    from kivy.config import Config
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'width', f'{config_x}')
    Config.set('graphics', 'height', f'{config_y}')
    
    from kivy.core.window import Window
    Window.size = (config_x, config_y)
    
    try:
        import guess_word_mobile_v110
        saved_ach = PLAYER_STATS.get("unlocked_achivements", {})
        if saved_ach:
            for ach_key, saved_data in saved_ach.items():
                if ach_key in achivements:
                    achivements[ach_key]["got"] = saved_data.get("got", False)
                    achivements[ach_key]["date"] = saved_data.get("date", "")

        # =========================================================================
        # ИСПРАВЛЕНО: Безопасный первый старт без вылетов, если сейв пустой
        # =========================================================================
        import time
        import copy
        
        current_time_struct = time.localtime()
        current_day = current_time_struct.tm_mday
        
        last_update_day = PLAYER_STATS.get("last_update_day", -1)
        saved_quests = PLAYER_STATS.get("active_quests", {})

        # Если день сменился ИЛИ в сейве вообще нет активных квестов (чистый старт!)
        if current_day != last_update_day or not saved_quests:
            print("[MGGamesStudio] Чистый старт или новый день! Генерируем 5 квестов...")
            
            commons = [k for k, v in all_quests.items() if v.get("type", "common") == "common"]
            rares = [k for k, v in all_quests.items() if v.get("type", "common") == "rare"]
            epics = [k for k, v in all_quests.items() if v.get("type", "common") == "epic"]
            
            # Страховка: проверяем, что в базе хватает квестов для выборки
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
            # Если день тот же, просто синхронизируем прогресс
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
