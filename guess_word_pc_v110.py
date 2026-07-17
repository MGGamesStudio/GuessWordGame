import pygame
import sys
import pygame.freetype
import ctypes
import random
import time
import os
from platformdirs import user_data_dir

external_save_func = None

try:
    game_save_dir = user_data_dir("GuessWordGame", "MGGamesStudio")
    
    if not os.path.exists(game_save_dir):
        os.makedirs(game_save_dir)
        
    SAVE_FILE_PATH = os.path.join(game_save_dir, "guess_word_save_file_guess_word_save_file.json")
except Exception:
    SAVE_FILE_PATH = "guess_word_save_file_guess_word_save_file.json"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

pygame.init()
pygame.freetype.init()

screen_x = 1200
screen_y = 900

# виртуальный холст
screen = pygame.Surface((screen_x, screen_y))
is_fullscreen = False
real_window = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
timer = pygame.time.Clock()
pygame.display.set_caption("Угадай слово")

screen_icon = pygame.image.load(resource_path("1000074566.png")).convert_alpha()
pygame.display.set_icon(screen_icon)

# 1. МАТЕМАТИЧЕСКИЙ РАСЧЕТ МАСШТАБА МЫШКИ
def get_scaled_mouse_pos():
    raw_x, raw_y = pygame.mouse._orig_get_pos()
    current_w, current_h = real_window.get_size()
    
    scale_w = current_w / screen_x
    scale_h = current_h / screen_y
    scale = min(scale_w, scale_h)

    new_w = int(screen_x * scale)
    new_h = int(screen_y * scale)
    
    gap_x = (current_w - new_w) // 2
    gap_y = (current_h - new_h) // 2
    
    if scale > 0:
        scaled_x = int((raw_x - gap_x) / scale)
        scaled_y = int((raw_y - gap_y) / scale)
    else:
        scaled_x, scaled_y = raw_x, raw_y
        
    return scaled_x, scaled_y

# 2. ФУНКЦИЯ ОТРЕСОВКИ КАДРА
def flip_scaled_screen():
    current_w, current_h = real_window.get_size()
    scale_w = current_w / screen_x
    scale_h = current_h / screen_y
    scale = min(scale_w, scale_h)

    new_w = int(screen_x * scale)
    new_h = int(screen_y * scale)
    
    scaled_surface = pygame.transform.smoothscale(screen, (new_w, new_h))
    
    gap_x = (current_w - new_w) // 2
    gap_y = (current_h - new_h) // 2
    
    real_window.fill(color_bg)
    real_window.blit(scaled_surface, (gap_x, gap_y))
    pygame.display.update()


# 3. ПЕРЕХВАТ СЦЕН
_orig_event_get = pygame.event.get

def custom_event_get(*args, **kwargs):
    events = _orig_event_get(*args, **kwargs)
    for event in events:
        if hasattr(event, "pos"):
            try:
                event.__dict__["pos"] = get_scaled_mouse_pos()
            except:
                pass
    return events

# ЗАМЕНА МАТОДОВ
pygame.mouse._orig_get_pos = pygame.mouse.get_pos
pygame.mouse.get_pos = get_scaled_mouse_pos
pygame.display.flip = flip_scaled_screen
pygame.event.get = custom_event_get

font_20 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 20)
font_30 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 30)
font_45 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 45)
font_55 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 55)
font_70 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 70)
font_90 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 90)
font_120 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 120)

# Переменные для глобального поп-апа достижений
ach_popup_active = False
ach_popup_title = ""
ach_popup_reward = 0
ach_popup_end_time = 0

# ----- ПЕРЕМЕННЫЕ ДЛЯ СОХРАНЕНИЯ -----
total_wins = 0
total_losses = 0
player_coins = 0
current_win_streak = 0
max_win_streak = 0

# ----- ЦВЕТА -----
color_themes = {
    "classic": {"color_name": "Классика","price": 0,"unlocked": True,"color_bg": (255, 255, 255),"color_text": (31, 41, 55),"color_blank": (229, 231, 235),"color_correct": (34, 197, 94),"color_in_word": (250, 204, 21),"color_not_in_word": (148, 163, 184),"color_key": (226, 232, 240)},
    "night": {"color_name": "Ночь","price": 0,"unlocked": True,"color_bg": (15, 23, 42),"color_text": (248, 250, 252),"color_blank": (30, 41, 59),"color_correct": (34, 197, 94),"color_in_word": (234, 179, 8),"color_not_in_word": (71, 85, 105),"color_key": (51, 65, 85)},
    "ocean": {"color_name": "Океан","price": 1000,"unlocked": False,"color_bg": (224, 242, 254),"color_text": (15, 23, 42),"color_blank": (186, 230, 253),"color_correct": (2, 132, 199),"color_in_word": (56, 189, 248),"color_not_in_word": (148, 163, 184),"color_key": (125, 211, 252)},
    "sunset": {"color_name": "Закат","price": 1000,"unlocked": False,"color_bg": (255, 247, 237),"color_text": (67, 20, 7),"color_blank": (254, 215, 170),"color_correct": (234, 88, 12),"color_in_word": (251, 191, 36),"color_not_in_word": (168, 162, 158),"color_key": (253, 186, 116)},
    "sakura": {"color_name": "Сакура","price": 1000,"unlocked": False,"color_bg": (255, 241, 242),"color_text": (74, 4, 78),"color_blank": (251, 207, 232),"color_correct": (236, 72, 153),"color_in_word": (244, 114, 182),"color_not_in_word": (203, 213, 225),"color_key": (253, 164, 175)},
    "forest": {"color_name": "Лес","price": 1000,"unlocked": False,"color_bg": (240, 253, 244),"color_text": (5, 46, 22),"color_blank": (187, 247, 208),"color_correct": (21, 128, 61),"color_in_word": (101, 163, 13),"color_not_in_word": (148, 163, 184),"color_key": (134, 239, 172)},
    "royal": {"color_name": "Король","price": 1000,"unlocked": False,"color_bg": (245, 243, 255),"color_text": (46, 16, 101),"color_blank": (221, 214, 254),"color_correct": (124, 58, 237),"color_in_word": (168, 85, 247),"color_not_in_word": (148, 163, 184),"color_key": (196, 181, 253)},
    "lava": {"color_name": "Лава","price": 1000,"unlocked": False,"color_bg": (254, 242, 242),"color_text": (69, 10, 10),"color_blank": (254, 202, 202),"color_correct": (220, 38, 38),"color_in_word": (251, 146, 60),"color_not_in_word": (156, 163, 175),"color_key": (248, 113, 113)},
    "emerald": {"color_name": "Изумруд","price": 1000,"unlocked": False,"color_bg": (236, 253, 245),"color_text": (2, 44, 34),"color_blank": (167, 243, 208),"color_correct": (5, 150, 105),"color_in_word": (16, 185, 129),"color_not_in_word": (148, 163, 184),"color_key": (110, 231, 183)},
    "candy": {"color_name": "Конфета","price": 1000,"unlocked": False,"color_bg": (255, 247, 251),"color_text": (131, 24, 67),"color_blank": (249, 168, 212),"color_correct": (236, 72, 153),"color_in_word": (244, 114, 182),"color_not_in_word": (203, 213, 225),"color_key": (253, 164, 175)},
    "neon": {"color_name": "Неон","price": 1000,"unlocked": False,"color_bg": (15, 23, 42),"color_text": (255, 255, 255),"color_blank": (51, 65, 85),"color_correct": (0, 255, 136),"color_in_word": (255, 230, 0),"color_not_in_word": (100, 116, 139),"color_key": (0, 217, 255)},
    "gold": {"color_name": "Золото","price": 1000,"unlocked": False,"color_bg": (255, 251, 235),"color_text": (120, 53, 15),"color_blank": (253, 230, 138),"color_correct": (217, 119, 6),"color_in_word": (250, 204, 21),"color_not_in_word": (168, 162, 158),"color_key": (251, 191, 36)}
}
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
active_quests = {}
total_completed_quests = 0
last_update_day = -1

# ----- ----- -----
# -----  КОД  -----
# ----- ----- -----

color_name = color_themes["classic"]["color_name"]
color_bg = color_themes["classic"]["color_bg"]
color_text = color_themes["classic"]["color_text"]
color_blank = color_themes["classic"]["color_blank"]
color_correct = color_themes["classic"]["color_correct"]
color_in_word = color_themes["classic"]["color_in_word"]
color_not_in_word = color_themes["classic"]["color_not_in_word"]
color_key = color_themes["classic"]["color_key"]

# ----- СОХРАНЕНИЕ -----
def save_game_progress():
    save_data = {
        "player_coins": player_coins,
        "total_wins": total_wins,
        "total_losses": total_losses,
        "current_win_streak": current_win_streak,
        "max_win_streak": max_win_streak,
        "total_completed_quests": total_completed_quests,
        "last_update_day": last_update_day,
        "active_quests": active_quests,
        "unlocked_themes": {k: v["unlocked"] for k, v in color_themes.items()},
        "active_theme_name": color_name.lower() if 'color_name' in globals() else "classic",
        "unlocked_achivements": {k: {"got": v["got"], "date": v["date"]} for k, v in achivements.items()}
    }
    
    if 'external_save_func' in globals() and external_save_func is not None:
        external_save_func(save_data)
        print("Данные сохранены через лаунчер!")

# ----- ----- -----
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

def give_reward(ach_id):
    global player_coins
    global ach_popup_active, ach_popup_title, ach_popup_reward, ach_popup_end_time
    
    if not achivements[ach_id]["got"]:
        achivements[ach_id]["got"] = True
        
        achivements[ach_id]["date"] = time.strftime("%d.%m.%Y")
        
        ach_type = achivements[ach_id]["type"]
        if ach_type == "common":   reward = 30
        elif ach_type == "rare":   reward = 50
        elif ach_type == "epic":   reward = 500
        else:                      reward = 0
        player_coins += reward
        
        ach_popup_active = True
        ach_popup_title = achivements[ach_id]["name"].upper()
        ach_popup_reward = reward
        ach_popup_end_time = time.time() + 3.0

def check_achivements(last_win_attempt=None):
    global player_coins
    
    # 1. Проверяем накопительные ачивки на победы
    win_conditions = {5: "ach_1", 10: "ach_2", 15: "ach_3", 20: "ach_4", 25: "ach_5"}
    if total_wins in win_conditions:
        ach_id = win_conditions[total_wins]
        give_reward(ach_id)

    # 2. Проверяем накопительные ачивки на поражения
    loss_conditions = {5: "ach_6", 10: "ach_7", 15: "ach_8", 20: "ach_9", 25: "ach_10"}
    if total_losses in loss_conditions:
        ach_id = loss_conditions[total_losses]
        give_reward(ach_id)

    # 3. Проверяем ачивки за конкретную попытку (если раунд был выигран)
    if last_win_attempt is not None:
        attempt_conditions = {1: "ach_11", 2: "ach_12", 3: "ach_13", 4: "ach_14", 5: "ach_15", 6: "ach_16"}
        if last_win_attempt in attempt_conditions:
            ach_id = attempt_conditions[last_win_attempt]
            give_reward(ach_id)

def draw_ach_notification(surface):
    global ach_popup_active

    if ach_popup_active and time.time() > ach_popup_end_time:
        ach_popup_active = False

    if ach_popup_active:
        if "КВЕСТ:" in ach_popup_title:
            display_title = ach_popup_title
        else:
            display_title = f"ДОСТИЖЕНИЕ: {ach_popup_title}"

        reward_str = f"Вы получили {ach_popup_reward} монет!"

        title_rect_measure = font_30.get_rect(display_title)
        
        font_25 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 25)
        reward_rect_measure = font_25.get_rect(reward_str)

        max_text_width = max(title_rect_measure.width, reward_rect_measure.width)
        dynamic_width = max_text_width + 140
        
        if dynamic_width < 500:  dynamic_width = 500
        if dynamic_width > 1100: dynamic_width = 1100

        popup_x = (1200 - dynamic_width) // 2
        notif_rect = pygame.Rect(popup_x, 20, dynamic_width, 110)
        
        pygame.draw.rect(surface, color_blank, notif_rect, border_radius=16)

        font_45.render_to(surface, (notif_rect.x + 30, notif_rect.y + 32), " ", color_text)
        font_30.render_to(surface, (notif_rect.x + 100, notif_rect.y + 22), display_title, color_text)
        font_25.render_to(surface, (notif_rect.x + 100, notif_rect.y + 65), reward_str, color_correct)

def update_daily_quests():
    global active_quests, last_update_day
    current_time_struct = time.localtime()
    current_day = current_time_struct.tm_mday 
    if current_day == last_update_day and active_quests:
        return

    last_update_day = current_day
    active_quests = {}
    
    commons = [k for k, v in all_quests.items() if v["type"] == "common"]
    rares = [k for k, v in all_quests.items() if v["type"] == "rare"]
    epics = [k for k, v in all_quests.items() if v["type"] == "epic"]
    
    chosen_keys = random.sample(commons, 2) + random.sample(rares, 2) + random.sample(epics, 1)
    
    for key in chosen_keys:
        import copy
        active_quests[key] = copy.deepcopy(all_quests[key])
        active_quests[key]["progress"] = 0
        active_quests[key]["done"] = False
    save_game_progress()

def check_and_advance_quest(quest_id, amount=1):
    global player_coins, total_completed_quests, active_quests
    global ach_popup_active, ach_popup_title, ach_popup_reward, ach_popup_end_time

    if quest_id in active_quests:
        q = active_quests[quest_id]
        
        if q["done"]:
            return

        q["progress"] += amount
        if q["progress"] >= q["goal"]:
            q["progress"] = q["goal"]
            q["done"] = True
            
            player_coins += q["reward"]
            total_completed_quests += 1

            ach_popup_active = True
            ach_popup_title = f"КВЕСТ: {q['name']}"
            ach_popup_reward = q["reward"]
            ach_popup_end_time = time.time() + 3.0

def render_wrapped_text(surface, text, x, y, max_width, font, color, line_spacing=40):
        words_list = text.split(' ')
        current_line = ""
        current_y = y

        for word in words_list:
            test_line = current_line + " " + word if current_line else word
            text_rect = font.get_rect(test_line)
            
            if text_rect.width <= max_width:
                current_line = test_line
            else:
                font.render_to(surface, (x, current_y), current_line, color)
                current_y += line_spacing
                current_line = word

        if current_line:
            font.render_to(surface, (x, current_y), current_line, color)
            
        return current_y + line_spacing

class Button:
    def __init__(self,x,y,w,h,base_color,border):
        self.rect=pygame.Rect(x,y,w,h)
        self.base_color=pygame.Color(base_color)
        self.current_color=base_color
        self.border=border

    def button_color_mouse(self, color):
        self.base_color=pygame.Color(color)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color=self.base_color.lerp((0,0,0), 0.2)
        else:
            self.current_color=self.base_color

    def button_draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=self.border)

letters=["","А","Б","В","Г","Д","Е","Ё","Ж","З","И","Й","К","Л","М","Н","О","П","Р","С","Т","У","Ф","Х","Ц","Ч","Ш","Щ","Ъ","Ы","Ь","Э","Ю","Я"]
class RectInGame:
    def __init__(self,x,y,w,h,border,letter_type,letter,font_x):
        self.rect=pygame.Rect(x,y,w,h)
        self.letter_color=color_text
        if letter_type == "blank":
            self.base_color=pygame.Color(color_blank)
            self.base_color_=color_blank
            self.letter_color=color_text
        elif letter_type == "correct":
            self.base_color=pygame.Color(color_correct)
            self.base_color_=color_correct
            self.letter_color=(255, 255, 255)
        elif letter_type == "in_word":
            self.base_color=pygame.Color(color_in_word)
            self.base_color_=color_in_word
            self.letter_color=(0, 0, 0)
        elif letter_type == "not_in_word":
            self.base_color=pygame.Color(color_not_in_word)
            self.base_color_=color_not_in_word
            self.letter_color=(255, 255, 255)
        self.border=border
        self.letter=letter
        self.font_x=font_x

    def change_type(self, new_type):
        if new_type == "blank":
            self.base_color = pygame.Color(color_blank)
            self.letter_color=color_text
        elif new_type == "correct":
            self.base_color = pygame.Color(color_correct)
            self.letter_color=(255, 255, 255)
        elif new_type == "in_word":
            self.base_color = pygame.Color(color_in_word)
            self.letter_color=(0, 0, 0)
        elif new_type == "not_in_word":
            self.base_color = pygame.Color(color_not_in_word)
            self.letter_color=(255, 255, 255)

    def make_letter(self):
        if self.font_x == 70:
            ref_rect = font_70.get_rect("А")
            ref_rect.center = self.rect.center
            text_rect = font_70.get_rect(self.letter)
            text_rect.centerx = self.rect.centerx
            text_rect.centery = ref_rect.centery
            if self.letter == "Й" or self.letter == "Ё":
                text_rect.y -= (3*1.55)+1
            elif self.letter == "Ц" or self.letter == "Щ" or self.letter == "Д":
                text_rect.y += (3*1.55)-1
            font_70.render_to(screen, text_rect, self.letter, self.letter_color)

        elif self.font_x == 45:
            text_rect = font_45.get_rect(self.letter)
            text_rect.center = self.rect.center
            if self.letter == "Й" or self.letter == "Ё":
                text_rect.y -= 3
            elif self.letter == "Ц" or self.letter == "Щ" or self.letter == "Д":
                text_rect.y += 3
            font_45.render_to(screen, text_rect, self.letter, self.letter_color)
        
    def color_draw(self, surface):
        pygame.draw.rect(surface, self.base_color, self.rect, border_radius=self.border)

class KeyKeyboard:
    def __init__(self,x,y,w,h,letter):
        self.rect=pygame.Rect(x,y,w,h)
        self.letter=letter.upper()
        self.status="blank"

    def key_draw(self, surface):
        if self.status=="blank":
            bg_color=color_key
            letter_color=color_text
        elif self.status=="correct":
            bg_color=color_correct
            letter_color=(255, 255, 255)
        elif self.status=="in_word":
            bg_color=color_in_word
            letter_color=(0, 0, 0)
        elif self.status=="not_in_word":
            bg_color=color_not_in_word
            letter_color=(255, 255, 255)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        bg_color = pygame.Color(bg_color)
        if self.rect.collidepoint(mouse_pos):
            if mouse_click[0]: 
                bg_color = bg_color.lerp((0, 0, 0), 0.35)
            else:
                bg_color = bg_color.lerp((0, 0, 0), 0.15)
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)
        text_rect = font_45.get_rect(self.letter)
        text_rect.center = self.rect.center
        if self.letter == "Й" or self.letter == "Ё":
            text_rect.y -= 3
        elif self.letter == "Ц" or self.letter == "Щ" or self.letter == "Д":
            text_rect.y += 3
        font_45.render_to(surface, text_rect, self.letter, letter_color)

    def change_type(self, new_status):
        if self.status == "correct":
            return
        if self.status == "in_word" and new_status == "not_in_word":
            return
        self.status = new_status

    def check_press(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
class SpecialKey(KeyKeyboard):
    def __init__(self, x, y, action):
        self.w = 90
        self.h = 162
        self.action = action
        self.status = "blank"
        self.surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        if self.action == "enter":
            self.rect_v = pygame.Rect(x + 33, y, 57, 162)
            self.rect_h = pygame.Rect(x, y + 86, 90, 76)
            
        elif self.action == "delete":
            self.rect_v = pygame.Rect(x, y, 57, 162)
            self.rect_h = pygame.Rect(x, y + 86, 90, 76)

    def key_draw(self, surface):
        if self.status == "blank":
            bg_rgb = color_key
            letter_color = color_text
        bg_color = pygame.Color(bg_rgb)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.rect_v.collidepoint(mouse_pos) or self.rect_h.collidepoint(mouse_pos):
            if mouse_click[0]: 
                bg_color = bg_color.lerp((0, 0, 0), 0.35)
            else:
                bg_color = bg_color.lerp((0, 0, 0), 0.15)

        self.surf.fill((0, 0, 0, 0))

        if self.action == "enter":
            pygame.draw.rect(self.surf, bg_color, (33, 0, 57, 162), border_radius=6)
            pygame.draw.rect(self.surf, bg_color, (0, 86, 90, 76), border_radius=6)
            surface.blit(self.surf, (self.rect_h.x, self.rect_v.y))
            text_rect = font_20.get_rect("ВВОД")
            text_rect.center = self.rect_h.center
            font_20.render_to(surface, text_rect, "ВВОД", letter_color)

        elif self.action == "delete":
            pygame.draw.rect(self.surf, bg_color, (0, 0, 57, 162), border_radius=6)
            pygame.draw.rect(self.surf, bg_color, (0, 86, 90, 76), border_radius=6)
            surface.blit(self.surf, (self.rect_v.x, self.rect_v.y))
            text_rect = font_20.get_rect("СТЕРЕТЬ")
            text_rect.center = self.rect_h.center
            font_20.render_to(surface, text_rect, "СТЕРЕТЬ", letter_color)

    def check_press(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_v.collidepoint(event.pos) or self.rect_h.collidepoint(event.pos):
                return True
        return False
    
class AchivementCard:
    def __init__(self, x, y, w, h, ach_id):
        self.rect = pygame.Rect(x, y, w, h)
        self.ach_id = ach_id

    def draw(self, surface, offset_y):
        render_rect = self.rect.copy()
        render_rect.y += offset_y

        data = achivements[self.ach_id]
        is_got = data["got"]
        ach_type = data["type"]

        # АДАПТИВНЫЕ ЦВЕТА РЕДКОСТИ:
        base_text_color = pygame.Color(color_text)
        
        if ach_type == "common":
            type_text = "Обычное"
            rare_color = base_text_color.lerp(color_bg, 0.3)
        elif ach_type == "rare":
            type_text = "Редкое"
            rare_color = base_text_color.lerp(color_in_word, 0.5)
        elif ach_type == "epic":
            type_text = "Эпическое"
            rare_color = base_text_color.lerp(color_correct, 0.6)

        if is_got:
            bg_color = color_blank
            text_color = color_text
            status_str = "ПОЛУЧЕНО"
            status_color = color_correct
        else:
            bg_color = pygame.Color(color_blank).lerp(color_bg, 0.5)
            text_color = pygame.Color(color_text).lerp(color_bg, 0.4)
            rare_color = pygame.Color(rare_color).lerp(color_bg, 0.3)
            status_str = "НЕ ПОЛУЧЕНО"
            status_color = color_not_in_word

        pygame.draw.rect(surface, bg_color, render_rect, border_radius=12)
        pygame.draw.rect(surface, rare_color, (render_rect.x, render_rect.y, 10, render_rect.h))

        name_str = data["name"].upper()
        font_30.render_to(surface, (render_rect.x + 25, render_rect.y + 20), name_str, text_color)
        font_20.render_to(surface, (render_rect.x + 25, render_rect.y + 60), data["description"], text_color)

        font_20.render_to(surface, (render_rect.right - 180, render_rect.y + 22), type_text, rare_color)
        font_20.render_to(surface, (render_rect.right - 180, render_rect.y + 58), status_str, status_color)

        if is_got and data["date"]:
            date_str = f"Дата: {data['date']}"
            txt_date = font_20.get_rect(date_str)
            txt_date.right = render_rect.x + 550
            txt_date.centery = render_rect.y + (render_rect.h // 2)
            
            font_20.render_to(surface, txt_date, date_str, color_not_in_word)

class QuestCard:
    def __init__(self, x, y, w, h, quest_id):
        self.rect = pygame.Rect(x, y, w, h)
        self.quest_id = quest_id

    def draw(self, surface, offset_y):
        render_rect = self.rect.copy()
        render_rect.y += offset_y

        data = active_quests[self.quest_id]
        is_done = data["done"]
        q_type = data["type"]

        base_text_color = pygame.Color(color_text)
        if q_type == "common":
            rare_color = base_text_color.lerp(color_bg, 0.3)
        elif q_type == "rare":
            rare_color = base_text_color.lerp(color_in_word, 0.5)
        elif q_type == "epic":
            rare_color = base_text_color.lerp(color_correct, 0.6)

        if is_done:
            bg_color = color_blank
            text_color = color_text
            status_str = "ВЫПОЛНЕНО"
            status_color = color_correct
        else:
            bg_color = pygame.Color(color_blank).lerp(color_bg, 0.5)
            text_color = pygame.Color(color_text).lerp(color_bg, 0.4)
            rare_color = pygame.Color(rare_color).lerp(color_bg, 0.3)
            status_str = f"{data['progress']}/{data['goal']}"
            status_color = color_not_in_word

        pygame.draw.rect(surface, bg_color, render_rect, border_radius=12)
        pygame.draw.rect(surface, rare_color, (render_rect.x, render_rect.y, 10, render_rect.h))

        name_str = data["name"].upper()
        font_30.render_to(surface, (render_rect.x + 25, render_rect.y + 20), name_str, text_color)
        font_20.render_to(surface, (render_rect.x + 25, render_rect.y + 60), data["description"], text_color)

        right_alignment = render_rect.right - 25

        reward_str = f"Награда: {data['reward']}"
        txt_reward = font_20.get_rect(reward_str)
        txt_status = font_20.get_rect(status_str)

        txt_left_name = font_30.get_rect(name_str)
        txt_left_name.y = render_rect.y + 20

        txt_left_desc = font_20.get_rect(data["description"])
        txt_left_desc.y = render_rect.y + 60

        txt_reward.right = right_alignment
        txt_reward.bottom = txt_left_name.bottom
        font_20.render_to(screen, txt_reward, reward_str, color_in_word if not is_done else color_not_in_word)

        txt_status.right = right_alignment
        txt_status.bottom = txt_left_desc.bottom
        font_20.render_to(screen, txt_status, status_str, status_color)

# ----- СЦЕНА ВЫБОРА РЕЖИМА ИГРЫ -----
def choose_game_mode_scene():
    mode_btn_1 = Button(185, 350, 350, 200, color_key, 16)
    mode_btn_2 = Button(665, 350, 350, 200, color_key, 16)

    button_exit = Button(1045, 5, 150, 75, color_blank, 10)
    button_exit_text = font_30.get_rect("Выйти")
    button_exit_text.center = button_exit.rect.center
    button_exit_text.y -= 5 * 0.55

    t1_rect = font_45.get_rect("1 ИГРОК")
    t1_rect.center = mode_btn_1.rect.center
    t1_rect.y -= 25
    
    t1_sub = font_20.get_rect("С достижениями и монетами")
    t1_sub.center = mode_btn_1.rect.center
    t1_sub.y += 35

    t2_rect = font_45.get_rect("2 ИГРОКА")
    t2_rect.center = mode_btn_2.rect.center
    t2_rect.y -= 25
    
    t2_sub = font_20.get_rect("Без достижений и монет")
    t2_sub.center = mode_btn_2.rect.center
    t2_sub.y += 35

    while True:
        # ---- БЛОК СОБЫТИЙ ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_exit.rect.collidepoint(event.pos):
                    return
                if mode_btn_1.rect.collidepoint(event.pos):
                    start_game_scene_1_1()
                if mode_btn_2.rect.collidepoint(event.pos):
                    start_game_scene_1_2()

        # ---- БЛОК ОТРИСОВКИ ----
        screen.fill(color_bg)

        title_rect = font_70.get_rect("ВЫБЕРИТЕ РЕЖИМ ИГРЫ")
        title_rect.centerx = screen_x // 2
        title_rect.y = 140
        font_70.render_to(screen, title_rect, "ВЫБЕРИТЕ РЕЖИМ ИГРЫ", color_text)

        # Ховер и отрисовка кнопок режимов
        mode_btn_1.button_color_mouse(color_key)
        mode_btn_1.button_draw(screen)
        
        mode_btn_2.button_color_mouse(color_key)
        mode_btn_2.button_draw(screen)

        # Вывод текстов
        font_45.render_to(screen, t1_rect, "1 ИГРОК", color_text)
        font_20.render_to(screen, t1_sub, "С достижениями и монетами", color_correct)

        font_45.render_to(screen, t2_rect, "2 ИГРОКА", color_text)
        font_20.render_to(screen, t2_sub, "Без достижений и монет", color_not_in_word)

        # Кнопка выхода в меню
        button_exit.button_color_mouse(color_key)
        button_exit.button_draw(screen)
        font_30.render_to(screen, button_exit_text, "Выйти", color_text)

        timer.tick(60)
        pygame.display.flip()

# ----- играть -----
def start_game_scene_1_1():
    global total_wins, total_losses, player_coins, current_win_streak
    used_delete_key = False

    # Пустые клетки
    game_grid=[]
    blank_x = 600-(425//2)
    blank_y = 5
    for a1 in range(6):
        for a2 in range(5):
            blank=RectInGame(blank_x, blank_y, 80, 100, 6, "blank", "", 70)
            game_grid.append(blank)
            blank_x+=80+5
        blank_x=600-(425//2)
        blank_y+=100+5

    # Клавиатура
    line1="ЙЦУКЕНГШЩЗХЪ"
    line2="ФЫВАПРОЛДЖЭ"
    line3="ЯЧСМИТЬБЮЁ"
    keyboard=[]
    l_w=57
    l_h=76
    l1_x=201
    l2_x=235
    l3_x=268
    for keyboard_line1 in line1:
        key_n=KeyKeyboard(l1_x, 640, l_w, l_h, keyboard_line1)
        keyboard.append(key_n)
        l1_x+=67
    for keyboard_line2 in line2:
        key_n=KeyKeyboard(l2_x, 726, l_w, l_h, keyboard_line2)
        keyboard.append(key_n)
        l2_x+=67
    for keyboard_line3 in line3:
        key_n=KeyKeyboard(l3_x, 812, l_w, l_h, keyboard_line3)
        keyboard.append(key_n)
        l3_x+=67
    enter_key = SpecialKey(938, 726, "enter")
    delete_key = SpecialKey(168, 726, "delete")

    # Дополнительное
    current_word=""
    current_attempt=0
    correct_word=random.choice(words).upper()
    game_state = "playing"
    notification_end_time = 0

    # Кнопки
    button_1_1 = Button(225, 20, 750, 110, color_key, 16)

    # Текст
    game_text_1_1 = font_45.get_rect("Слово:")
    game_text_1_1.x = 30
    game_text_1_1.y = 284
    button_text_1_1 = font_30.get_rect("Такого слова нет в словаре или слово не из 5 букв.")
    button_text_1_1.center = button_1_1.rect.center
    button_text_1_1.y += 1

    # Проверка
    correct_check=False

    # Кнопка выхода
    button_exit = Button(1045, 5, 150, 75, color_blank, 10)
    button_exit_text = font_30.get_rect("Выйти")
    button_exit_text.center = button_exit.rect.center
    button_exit_text.y -= 5*0.55

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
            # Кнопка выхода
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_exit.rect.collidepoint(event.pos):
                        return
                    
            if game_state != "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return

            if game_state == "playing" and current_attempt < 6:  
                if delete_key.check_press(event) and len(current_word) > 0:
                    used_delete_key = True
                    current_word = current_word[:-1]
                    cell_idx = (current_attempt * 5) + len(current_word)
                    game_grid[cell_idx].letter = ""

                for key_btn in keyboard:
                    if key_btn.check_press(event):
                        if len(current_word) < 5:
                            cell_idx = (current_attempt * 5) + len(current_word)
                            game_grid[cell_idx].letter = key_btn.letter
                            current_word += key_btn.letter

            if enter_key.check_press(event):
                if game_state != "playing":
                    return
                
                if len(current_word) == 5:
                    if current_word.lower() in words:
                        current_match_greens = 0
                        current_match_yellows = 0

                        word_remain = list(correct_word)
                        
                        # --- ЦИКЛ 1: ЗЕЛЕНЫЕ БУКВЫ ---
                        for i in range(5):
                            cell_idx = current_attempt * 5 + i
                            current_letter = current_word[i]

                            if current_word[i] == correct_word[i]:
                                game_grid[cell_idx].change_type("correct")
                                word_remain[i] = "_"
                                player_coins += 5
                                
                                current_match_greens += 1

                                for key_button in keyboard:
                                    if key_button.letter == current_letter:
                                        key_button.change_type("correct")

                        # --- ЦИКЛ 2: ЖЕЛТЫЕ И СЕРЫЕ БУКВЫ ---
                        for i in range(5):
                            cell_idx = current_attempt * 5 + i
                            current_letter = current_word[i]

                            if current_letter == correct_word[i]:
                                continue

                            if current_word[i] in word_remain:
                                game_grid[cell_idx].change_type("in_word")
                                idx_in_remain = word_remain.index(current_letter)
                                word_remain[idx_in_remain] = "_"
                                player_coins += 3
                                
                                current_match_yellows += 1

                                for key_button in keyboard:
                                    if key_button.letter == current_letter:
                                        key_button.change_type("in_word")

                            else:
                                game_grid[cell_idx].change_type("not_in_word")
                                player_coins += 1

                                for key_button in keyboard:
                                    if key_button.letter == current_letter:
                                        key_button.change_type("not_in_word")

                        if current_word == correct_word:
                            game_state = "won"
                            total_wins += 1
                            player_coins += 10
                            
                            global current_win_streak, max_win_streak
                            current_win_streak += 1

                            if current_win_streak > max_win_streak:
                                max_win_streak = current_win_streak
                            
                            check_achivements(last_win_attempt=current_attempt + 1)

                            grey_keys_count = sum(1 for key_btn in keyboard if key_btn.status == "not_in_word")

                            # АЧИВКИ
                            check_and_advance_quest("q1", amount=1)   # Разминка
                            check_and_advance_quest("q5", amount=1)   # Стабильный результат
                            check_and_advance_quest("q11", amount=1)  # Лингвист-марафон

                            if current_match_greens >= 3:
                                check_and_advance_quest("q2", amount=1)  # Точное попадание
                            if current_match_yellows >= 5:
                                check_and_advance_quest("q3", amount=1)  # В поисках истины
                            if current_match_greens == 5 and current_match_yellows == 0:
                                check_and_advance_quest("q10", amount=1) # Чистая победа
                            if grey_keys_count >= 10:
                                check_and_advance_quest("q8", amount=1)   # Буквенный пост

                            # По тонкому льду (победа строго на 5-й или 6-й попытке)
                            if current_attempt == 5 or current_attempt == 6:
                                check_and_advance_quest("q6", amount=1)
                                
                            # Экономный эрудит (победа не более чем за 4 попытки)
                            if current_attempt <= 4:
                                check_and_advance_quest("q7", amount=1)
                                
                            # Интуиция гения (победа строго на 2-й или 3-й попытке)
                            if current_attempt == 2 or current_attempt == 3:
                                check_and_advance_quest("q9", amount=1)

                            if not used_delete_key:
                                check_and_advance_quest("q12", amount=1) # Ювелирная работа
                            save_game_progress()

                        current_attempt += 1
                        current_word = ""

                        if current_attempt == 6 and game_state == "playing":
                            game_state = "lost"
                            total_losses += 1
                            current_win_streak = 0
                            if "q5" in active_quests:
                                active_quests["q5"]["progress"] = 0
                            check_achivements(last_win_attempt=None)

                            grey_keys_count = sum(1 for key_btn in keyboard if key_btn.status == "not_in_word")

                            check_and_advance_quest("q1", amount=1) # Разминка
                            if current_match_greens >= 3:      check_and_advance_quest("q2", amount=1)
                            if current_match_yellows >= 5:     check_and_advance_quest("q3", amount=1)
                            if grey_keys_count >= 10: check_and_advance_quest("q8", amount=1)
                            save_game_progress()
                            
                    else:
                        correct_check=True
                        print("Такого слова нет.")
                        notification_end_time = time.time() + 2
                        check_and_advance_quest("q4", amount=1) # Разведка боем
                            
                else:
                    correct_check=True
                    print("Слово не из 5 букв.")
                    notification_end_time = time.time() + 2

        # Вывод на экран
        screen.fill(color_bg)

        for blank_1 in game_grid:
            blank_1.color_draw(screen)
            blank_1.make_letter()

        for k_draw in keyboard:
            k_draw.key_draw(screen)

        enter_key.key_draw(screen)
        delete_key.key_draw(screen)

        # Автоматическое скрытие плашки ошибок по таймеру
        if correct_check and time.time() > notification_end_time:
            correct_check = False

        if correct_check == True:
            bx, by, bw, bh = 225, 20, 750, 110
            
            pygame.draw.rect(screen, color_key, (bx, by, bw, bh), border_radius=16)

            font_45.render_to(screen, (bx + 30, by + 32), " ", color_text)
            font_25 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 25)
            
            line1 = "Такого слова нет в словаре"
            line2 = "или введенное слово состоит не из 5 букв."
            
            font_25.render_to(screen, (bx + 95, by + 28), line1, color_text)
            font_25.render_to(screen, (bx + 95, by + 60), line2, color_text)

        # Кнопка выхода
        button_exit.button_color_mouse(color_key)
        button_exit.button_draw(screen)

        font_30.render_to(screen, button_exit_text, "Выйти", color_text)

        # Финал
        if game_state != "playing":
            overlay = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            popup_rect = pygame.Rect(600 - 275, 300, 550, 250)
            pygame.draw.rect(screen, color_blank, popup_rect, border_radius=15)
            
            if game_state == "won":
                end_title = "ПОБЕДА!"
                title_color = color_correct
            else:
                end_title = "ИГРА ОКОНЧЕНА"
                title_color = color_not_in_word

            # Заголовок
            txt_title = font_55.get_rect(end_title)
            txt_title.center = (popup_rect.centerx, popup_rect.y + 60)
            font_55.render_to(screen, txt_title, end_title, title_color)

            # Слово
            word_info = f"Загаданное слово: {correct_word}"
            txt_info = font_30.get_rect(word_info)
            txt_info.center = (popup_rect.centerx, popup_rect.y + 130)
            font_30.render_to(screen, txt_info, word_info, color_text)

            # Текст снизу
            hint_text = "Нажмите ESC или по экрану для выхода в меню"
            txt_hint = font_20.get_rect(hint_text)
            txt_hint.center = (popup_rect.centerx, popup_rect.y + 200)
            font_20.render_to(screen, txt_hint, hint_text, color_text)

        draw_ach_notification(screen)

        timer.tick(60)
        pygame.display.flip()

# ----- как играть -----
def start_game_scene_2():
    active_tab = "about"

    # Бланки
    demo_blank = RectInGame(100, 325, 60, 60, 6, "blank", "А", 45)
    demo_absent = RectInGame(100, 415, 60, 60, 6, "not_in_word", "А", 45)
    demo_present = RectInGame(100, 505, 60, 60, 6, "in_word", "А", 45)
    demo_correct = RectInGame(100, 595, 60, 60, 6, "correct", "А", 45)

    # Заголовок сцены
    title_rect = font_90.get_rect("Как играть:")
    title_rect.x = 25
    title_rect.y = 25

    # Кнопка выхода
    button_exit = Button(1045, 5, 150, 75, color_blank, 10)
    button_exit_text = font_30.get_rect("Выйти")
    button_exit_text.center = button_exit.rect.center
    button_exit_text.y -= 5 * 0.55

    # Координаты для верхнего горизонтального меню вкладок
    tab_buttons = {
        "about":   Button(25,  150, 220, 55, color_blank, 10),
        "colors":  Button(260, 150, 220, 55, color_blank, 10),
        "coins":   Button(495, 150, 220, 55, color_blank, 10),
        "achiev":  Button(730, 150, 220, 55, color_blank, 10),
        "quests":  Button(965, 150, 220, 55, color_blank, 10)
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_progress()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_exit.rect.collidepoint(event.pos):
                    return
                
                # Клик по вкладкам переключения больших блоков
                for tab_name, btn in tab_buttons.items():
                    if btn.rect.collidepoint(event.pos):
                        active_tab = tab_name

        screen.fill(color_bg)

        font_90.render_to(screen, title_rect, "Как играть:", color_in_word)
        tab_labels = {
            "about": "ОБ ИГРЕ", "colors": "ЦВЕТА", "coins": "МОНЕТЫ", 
            "achiev": "ДОСТИЖЕНИЯ", "quests": "КВЕСТЫ"
        }

        for tab_name, btn in tab_buttons.items():
            if active_tab == tab_name:
                btn.button_color_mouse(color_key)
                btn.button_draw(screen)
                txt_color = color_bg
            else:
                btn.button_color_mouse(color_key)
                btn.button_draw(screen)
                txt_color = color_text

            t_rect = font_20.get_rect(tab_labels[tab_name])
            t_rect.center = btn.rect.center
            font_20.render_to(screen, t_rect, tab_labels[tab_name], txt_color)

        # =========================================================================
        # ГЛАВНЫЙ БОЛЬШОЙ БЛОК ИНФОРМАЦИИ (Центральная плитка на весь экран)
        # =========================================================================
        main_block_rect = pygame.Rect(25, 220, 1150, 480)
        
        info_block_color = pygame.Color(color_blank).lerp(pygame.Color(color_bg), 0.4)
        pygame.draw.rect(screen, info_block_color, main_block_rect, border_radius=16)

        # ---------- БЛОК 1: О Б И Г Р Е ----------
        if active_tab == "about":
            font_45.render_to(screen, (70, 260), "О ЧЕМ ЭТА ИГРА?", color_in_word)
            font_30.render_to(screen, (70, 340), "Игра является цифровой головоломкой на логику и эрудицию.", color_text)
            font_30.render_to(screen, (70, 390), "Ваша главная цель - за 6 попыток вычислить секретное слово.", color_text)
            font_30.render_to(screen, (70, 440), "Загаданное слово всегда состоит строго из 5 букв.", color_text)
            font_30.render_to(screen, (70, 490), "Вводите ваши варианты слов и следите за изменением цветов ячеек!", color_text)
            font_30.render_to(screen, (70, 540), "Если вы потратите все 6 попыток и не угадаете - раунд завершится.", color_not_in_word)

        # ---------- БЛОК 2: Ч Т О О Б О З Н А Ч А Е Т ----------
        elif active_tab == "colors":
            font_45.render_to(screen, (70, 260), "РАСШИФРОВКА ЦВЕТОВ ЯЧЕЕК:", color_in_word)
            try:
                demo_blank.color_draw(screen); demo_blank.make_letter(screen)
                demo_absent.color_draw(screen); demo_absent.make_letter(screen)
                demo_present.color_draw(screen); demo_present.make_letter(screen)
                demo_correct.color_draw(screen); demo_correct.make_letter(screen)
            except:
                demo_blank.color_draw(screen); demo_blank.make_letter()
                demo_absent.color_draw(screen); demo_absent.make_letter()
                demo_present.color_draw(screen); demo_present.make_letter()
                demo_correct.color_draw(screen); demo_correct.make_letter()

            # --- ИДЕАЛЬНЫЙ СИММЕТРИЧНЫЙ ОТСТУП ОТ ПОТОЛКА И ПОЛА ---
            font_30.render_to(screen, (190, 330), "- Цвет пустой клетки. Буква введена, но еще", color_text)
            font_30.render_to(screen, (190, 365), "  не подтверждена клавишей ВВОД.", color_text)
            font_30.render_to(screen, (190, 420), "- Такой буквы нет в загаданном слове.", color_text)
            font_30.render_to(screen, (190, 455), "  На клавиатуре клавиша станет серой.", color_text)
            font_30.render_to(screen, (190, 510), "- Буква есть в слове, но в данный момент", color_text)
            font_30.render_to(screen, (190, 545), "  она стоит на другом месте.", color_text)
            font_30.render_to(screen, (190, 600), "- Буква угадана идеально и стоит", color_correct)
            font_30.render_to(screen, (190, 635), "  на своем правильном месте!", color_correct)

        # ---------- БЛОК 3: О М О Н Е Т А Х ----------
        elif active_tab == "coins":
            font_45.render_to(screen, (70, 260), "ЭКОНОМИКА И ЗАРАБОТОК МОНЕТ:", color_in_word)
            font_30.render_to(screen, (70, 340), "Каждая проверенная буква в раунде прибавляет монеты в ваш кошелёк:", color_text)
            font_30.render_to(screen, (100, 400), "Зелёная ячейка (Точное попадание) - +5 монет", color_correct)
            font_30.render_to(screen, (100, 450), "Жёлтая ячейка (Буква есть в слове) - +3 монеты", color_in_word)
            font_30.render_to(screen, (100, 500), "Серая ячейка (Буквы нет в слове) - +1 монета", color_not_in_word)
            font_30.render_to(screen, (100, 550), "Успешная полная победа в матче - +10 монет", color_correct)

        # ---------- БЛОК 4: О Д О С Т И Ж Е Н И Я Х ----------
        elif active_tab == "achiev":
            font_45.render_to(screen, (70, 252), "СИСТЕМА ДОСТИЖЕНИЙ:", color_in_word)
            font_30.render_to(screen, (70, 340), "За выполнение особых условий во время игры вы получаете Достижения.", color_text)
            font_30.render_to(screen, (70, 390), "При получении достижения оно показывается на экране.", color_text)
            font_30.render_to(screen, (70, 440), "В зависимости от сложности, достижения выдают крупные бонусы:", color_text)
            font_30.render_to(screen, (100, 500), "Лёгкие карточки наград - +30 монет", color_text)
            font_30.render_to(screen, (100, 540), "Средние карточки наград - +50 монет", color_in_word)
            font_30.render_to(screen, (100, 580), "Эпические карточки наград - +500 монет", color_correct)

        # ---------- БЛОК 5: О К В Е С Т А Х ----------
        elif active_tab == "quests":
            font_45.render_to(screen, (70, 260), "ЕЖЕДНЕВНЫЕ ЗАДАНИЯ И СЕРИИ:", color_in_word)
            font_30.render_to(screen, (70, 340), "Каждые новые сутки строго в 00:00 игра выдаёт 5 случайных квестов.", color_text)
            font_30.render_to(screen, (70, 390), "Выполняйте их в Одиночном режиме, чтобы забирать награды.", color_text)
            font_30.render_to(screen, (70, 440), "Текст наград выполненных квестов на карточках становится серым.", color_not_in_word)
            font_30.render_to(screen, (70, 490), "Копите непрерывные серии побед, чтобы увеличивать Серию побед.", color_text)
            font_30.render_to(screen, (70, 540), "Внимание: ЛЮБОЕ поражение полностью сбрасывает Серию побед!", color_not_in_word)

        # Нижний текст
        font_30.render_to(screen, (25, 725), "Если все 5 букв в ряду загорелись зелёным - ВЫ ВЫИГРАЛИ!", color_correct)
        font_20.render_to(screen, (25, 770), "Тратьте монеты в магазине Кастомизации, чтобы разблокировать новые цветовые палитры интерфейса.", color_not_in_word)

        # Кнопка выхода
        button_exit.button_color_mouse(color_key)
        button_exit.button_draw(screen)
        font_30.render_to(screen, button_exit_text, "Выйти", color_text)

        if globals().get("draw_ach_notification"):
            draw_ach_notification(screen)

        timer.tick(60)
        pygame.display.flip()

# ----- достижения -----
def start_game_scene_3():
    global total_wins, total_losses, player_coins
    
    # Кнопка выход
    button_exit = Button(1045, 5, 150, 75, color_blank, 10)
    button_exit_text = font_30.get_rect("Выйти")
    button_exit_text.center = button_exit.rect.center
    button_exit_text.y -= 5*0.55

    # Переменные для скроллинга
    scroll_y = 0
    is_dragging = False
    start_mouse_y = 0
    start_scroll_y = 0

    while True:
        got_count = sum(1 for ach in achivements.values() if ach["got"])

        all_keys = list(achivements.keys())
        sorted_keys = sorted(all_keys, key=lambda k: achivements[k]["got"], reverse=True)

        cards_list = []
        card_w, card_h = 750, 100
        start_card_x = 25
        start_card_y = 150 
        gap = 15

        for idx, ach_key in enumerate(sorted_keys):
            y = start_card_y + idx * (card_h + gap)
            cards_list.append(AchivementCard(start_card_x, y, card_w, card_h, ach_key))

        total_list_height = len(cards_list) * (card_h + gap)
        max_scroll_up = -(total_list_height - (screen_y - start_card_y) + 40)
        if max_scroll_up > 0: max_scroll_up = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Выход
                if button_exit.rect.collidepoint(event.pos):
                    return
                
                if event.pos[0] < 800:
                    is_dragging = True
                    start_mouse_y = event.pos[1]
                    start_scroll_y = scroll_y

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_dragging = False

            if event.type == pygame.MOUSEMOTION and is_dragging:
                delta_y = event.pos[1] - start_mouse_y
                scroll_y = start_scroll_y + delta_y
                if scroll_y > 0: scroll_y = 0
                if scroll_y < max_scroll_up: scroll_y = max_scroll_up

        screen.fill(color_bg)
        
        for card in cards_list:
            if card.rect.y + scroll_y >= 120 or card.rect.y + scroll_y <= screen_y:
                card.draw(screen, scroll_y)

        pygame.draw.rect(screen, color_bg, (0, 0, 800, 140))

        game_text = font_90.get_rect("ДОСТИЖЕНИЯ")
        game_text.x = 25
        game_text.y = 25
        font_90.render_to(screen, game_text, "ДОСТИЖЕНИЯ", color_text)

        stats_data = [
            ("Монеты", str(player_coins), color_in_word),
            ("Победы", str(total_wins), color_correct),
            ("Поражения", str(total_losses), color_text),
            ("Серия побед", f"{current_win_streak}/{max_win_streak}", color_text),
            ("Достижения", f"{got_count}/{len(achivements)}", color_text),
            ("Квесты", str(total_completed_quests), color_text)
        ]

        widget_x = 790
        widget_y = 150
        widget_w, widget_h = 385, 72
        widget_gap = 12

        for label, value, val_color in stats_data:
            pygame.draw.rect(screen, color_blank, (widget_x, widget_y, widget_w, widget_h), border_radius=12)

            txt_label = font_30.get_rect(label)
            txt_label.x = widget_x + 25 
            txt_label.centery = widget_y + (widget_h // 2)
            font_30.render_to(screen, txt_label, label, color_not_in_word)

            # Универсальный оптический зум шрифта
            if len(value) >= 9:
                active_font = font_20
            elif len(value) >= 6:
                active_font = font_30
            else:
                active_font = font_45

            txt_val = active_font.get_rect(value)
            txt_val.right = widget_x + widget_w - 25 
            txt_val.centery = widget_y + (widget_h // 2)
            active_font.render_to(screen, txt_val, value, val_color)

            widget_y += widget_h + widget_gap

        # Кнопка выхода
        button_exit.button_color_mouse(color_key)
        button_exit.button_draw(screen)
        font_30.render_to(screen, button_exit_text, "Выйти", color_text)

        draw_ach_notification(screen)

        timer.tick(60)
        pygame.display.flip()

# ----- кастомизация -----
def start_game_scene_4():
    global color_blank, color_correct, color_in_word, color_not_in_word, color_text, color_bg, color_key
    global player_coins, selected_theme

    try:
        selected_theme
    except NameError:
        selected_theme = "classic"

    # Кнопка выхода
    button_exit = Button(1045, 5, 150, 75, color_blank, 10)
    button_exit_text = font_30.get_rect("Выйти")
    button_exit_text.center = button_exit.rect.center
    button_exit_text.y -= 5 * 0.55

    btn_buy = Button(820, 560, 325, 80, color_correct, 12)
    btn_buy_text = font_30.get_rect("КУПИТЬ") 
    btn_buy_text.center = btn_buy.rect.center

    btn_sell = Button(820, 655, 325, 80, color_not_in_word, 12)
    btn_sell_text = font_30.get_rect("ПРОДАТЬ за 900") 
    btn_sell_text.center = btn_sell.rect.center

    # Переменные для скроллинга
    scroll_y = 0
    is_dragging = False
    start_mouse_y = 0
    start_scroll_y = 0

    while True:
        theme_keys = list(color_themes.keys())
        cards_list = []
        card_w, card_h = 360, 130  
        start_card_x = 25
        start_card_y = 150
        gap_x = 30                 
        gap_y = 15                 

        for idx, t_key in enumerate(theme_keys):
            row = idx // 2         
            col = idx % 2          
            x = start_card_x + col * (card_w + gap_x)
            y = start_card_y + row * (card_h + gap_y)
            cards_list.append((pygame.Rect(x, y, card_w, card_h), t_key))

        total_list_height = (6 * card_h) + (5 * gap_y)
        
        max_scroll_up = -(total_list_height - 715)
        if max_scroll_up > 0: 
            max_scroll_up = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_exit.rect.collidepoint(event.pos):
                    return
                
                # Клик по КУПИТЬ / ПРИМЕНИТЬ
                if btn_buy.rect.collidepoint(event.pos):
                    t_info = color_themes[selected_theme]
                    if not t_info["unlocked"]:
                        if player_coins >= t_info["price"]:
                            player_coins -= t_info["price"]
                            t_info["unlocked"] = True
                            choose_theme(selected_theme)
                            button_exit.base_color = pygame.Color(color_blank)
                            save_game_progress()
                    else:
                        choose_theme(selected_theme)
                        button_exit.base_color = pygame.Color(color_blank)
                        save_game_progress()

                # Клик по ПРОДАТЬ
                if btn_sell.rect.collidepoint(event.pos):
                    if selected_theme not in ["classic", "night"] and color_themes[selected_theme]["unlocked"]:
                        color_themes[selected_theme]["unlocked"] = False
                        player_coins += 900
                        choose_theme("classic")
                        selected_theme = "classic"
                        button_exit.base_color = pygame.Color(color_blank)
                        save_game_progress()

                if event.pos[0] < 790:
                    is_dragging = True
                    start_mouse_y = event.pos[1]
                    start_scroll_y = scroll_y
                    
                    for c_rect, t_key in cards_list:
                        actual_rect = c_rect.copy()
                        actual_rect.y += scroll_y
                        if actual_rect.collidepoint(event.pos) and actual_rect.y >= 120:
                            selected_theme = t_key

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_dragging = False

            if event.type == pygame.MOUSEMOTION and is_dragging:
                delta_y = event.pos[1] - start_mouse_y
                scroll_y = start_scroll_y + delta_y
                if scroll_y > 0: scroll_y = 0
                if scroll_y < max_scroll_up: scroll_y = max_scroll_up

        screen.fill(color_bg)
        
        for c_rect, t_key in cards_list:
            render_y = c_rect.y + scroll_y
            if render_y >= 120 or render_y <= screen_y:
                t_data = color_themes[t_key]
                
                pygame.draw.rect(screen, t_data["color_bg"], (c_rect.x, render_y, c_rect.width, c_rect.height), border_radius=15)
                
                if t_key == selected_theme:
                    pygame.draw.rect(screen, color_in_word, (c_rect.x, render_y, c_rect.width, c_rect.height), width=3, border_radius=15)
                
                if t_data["color_name"] == color_name:
                    pygame.draw.circle(screen, color_correct, (c_rect.right - 20, render_y + 20), 7)

                bx = c_rect.x + 15
                by = render_y + 15
                bw, bh = 32, 32
                statuses = ["blank", "correct", "in_word", "not_in_word", "blank"]
                for i in range(5):
                    if statuses[i] == "blank":    box_bg = t_data["color_blank"]
                    elif statuses[i] == "correct": box_bg = t_data["color_correct"]
                    elif statuses[i] == "in_word": box_bg = t_data["color_in_word"]
                    else:                          box_bg = t_data["color_not_in_word"]

                    pygame.draw.rect(screen, box_bg, (bx, by, bw, bh), border_radius=5)
                    l_color = (255, 255, 255) if statuses[i] in ["correct", "not_in_word"] else ((0,0,0) if statuses[i] == "in_word" else t_data["color_text"])
                    txt_rect = font_20.get_rect("А")
                    txt_rect.center = (bx + bw//2, by + bh//2)
                    font_20.render_to(screen, txt_rect, "А", l_color)
                    bx += bw + 5

                ky1 = render_y + 57
                ky2 = render_y + 75
                kx_start = c_rect.x + 15
                for i in range(10):
                    pygame.draw.rect(screen, t_data["color_key"], (kx_start + i * 19, ky1, 14, 13), border_radius=2)
                    pygame.draw.rect(screen, t_data["color_key"], (kx_start + i * 19, ky2, 14, 13), border_radius=2)

                display_name = t_data["color_name"]
                txt_rect = font_30.get_rect(display_name)
                txt_rect.x = c_rect.x + 18
                txt_rect.y = render_y + 95
                font_30.render_to(screen, txt_rect, display_name, t_data["color_text"])

        pygame.draw.rect(screen, color_bg, (0, 0, 790, 140))

        game_text = font_90.get_rect("КАСТОМИЗАЦИЯ")
        game_text.x = 25; game_text.y = 25
        font_90.render_to(screen, game_text, "КАСТОМИЗАЦИЯ", color_text)

        # ---- 2. ПРАВАЯ СТАТИЧНАЯ КАРТОЧКА УПРАВЛЕНИЯ ТЕМАМИ ----
        panel_x, panel_y, panel_w, panel_h = 790, 150, 385, 715
        pygame.draw.rect(screen, color_blank, (panel_x, panel_y, panel_w, panel_h), border_radius=15)

        right_y = 190
        step_y = 40       
        category_gap = 45 

        # Баланс Монет
        font_30.render_to(screen, (panel_x + 25, right_y), "Твои монеты:", color_not_in_word)
        right_y += step_y
        coins_str = str(player_coins)
        active_font = font_20 if len(coins_str) >= 9 else (font_30 if len(coins_str) >= 6 else font_45)
        active_font.render_to(screen, (panel_x + 25, right_y), coins_str, color_in_word)
        right_y += category_gap

        # Выбранная тема
        sel_info = color_themes[selected_theme]
        font_30.render_to(screen, (panel_x + 25, right_y), "Выбранная тема:", color_not_in_word)
        right_y += step_y
        font_45.render_to(screen, (panel_x + 25, right_y), sel_info["color_name"].upper(), color_text)
        
        right_y += category_gap + 20 

        # Текущий статус
        font_30.render_to(screen, (panel_x + 25, right_y), "Статус:", color_not_in_word)
        right_y += step_y
        if sel_info["unlocked"]:
            status_text = "КУПЛЕНА"
            status_color = color_correct
        else:
            status_text = f"ЦЕНА: {sel_info['price']} МОНЕТ"
            status_color = color_in_word
        font_30.render_to(screen, (panel_x + 25, right_y), status_text, status_color)

        # Кнопка КУПИТЬ / ПРИМЕНИТЬ
        btn_buy.rect.x, btn_buy.rect.y = 820, 665
        btn_buy.rect.width, btn_buy.rect.height = 325, 80 
        
        # Кнопка ПРОДАТЬ
        btn_sell.rect.x, btn_sell.rect.y = 820, 760 # Зазор ровно 15 пикселей между ними!
        btn_sell.rect.width, btn_sell.rect.height = 325, 80

        buy_label = "ПРИМЕНИТЬ" if sel_info["unlocked"] else "КУПИТЬ"
        
        btn_buy_text = font_30.get_rect(buy_label)
        btn_buy_text.center = btn_buy.rect.center
        
        btn_buy.button_color_mouse(color_correct if not (sel_info["color_name"] == color_name) else color_key)
        btn_buy.button_draw(screen)
        font_30.render_to(screen, btn_buy_text, buy_label, (255, 255, 255) if buy_label == "КУПИТЬ" else color_text)

        # Блок продажи обычных тем
        if selected_theme in ["classic", "night"] or not sel_info["unlocked"]:
            btn_sell.button_color_mouse(color_blank)
            btn_sell_text.center = btn_sell.rect.center
            font_30.render_to(screen, btn_sell_text, "ПРОДАТЬ за 900", color_not_in_word)
        else:
            btn_sell.button_color_mouse((220, 38, 38))
            btn_sell.button_draw(screen)
            btn_sell_text.center = btn_sell.rect.center
            font_30.render_to(screen, btn_sell_text, "ПРОДАТЬ за 900", (255, 255, 255))

        # Кнопка выхода
        button_exit.button_color_mouse(color_key)
        button_exit.button_draw(screen)
        font_30.render_to(screen, button_exit_text, "Выйти", color_text)
        
        timer.tick(60)
        pygame.display.flip()

# ----- 2 игрока -----
def start_game_scene_1_2():
    game_grid = []
    blank_x = 600 - (425 // 2)
    blank_y = 5
    for a1 in range(6):
        for a2 in range(5):
            blank = RectInGame(blank_x, blank_y, 80, 100, 6, "blank", "", 70)
            game_grid.append(blank)
            blank_x += 80 + 5
        blank_x = 600 - (425 // 2)
        blank_y += 100 + 5

    line1 = "ЙЦУКЕНГШЩЗХЪ"
    line2 = "ФЫВАПРОЛДЖЭ"
    line3 = "ЯЧСМИТЬБЮЁ"
    keyboard = []
    l_w = 57
    l_h = 76
    l1_x = 201
    l2_x = 235
    l3_x = 268
    for keyboard_line1 in line1:
        key_n = KeyKeyboard(l1_x, 640, l_w, l_h, keyboard_line1)
        keyboard.append(key_n)
        l1_x += 67
    for keyboard_line2 in line2:
        key_n = KeyKeyboard(l2_x, 726, l_w, l_h, keyboard_line2)
        keyboard.append(key_n)
        l2_x += 67
    for keyboard_line3 in line3:
        key_n = KeyKeyboard(l3_x, 812, l_w, l_h, keyboard_line3)
        keyboard.append(key_n)
        l3_x += 67
    enter_key = SpecialKey(938, 726, "enter")
    delete_key = SpecialKey(168, 726, "delete")

    current_word = ""
    current_attempt = 0
    correct_word = "" 
    
    mp_state = "setup" 

    button_1_1 = Button(225, 20, 750, 110, color_key, 16)
    button_text_1_1 = font_30.get_rect("Такого слова нет в словаре или слово не из 5 букв.")
    button_text_1_1.center = button_1_1.rect.center

    correct_check = False
    notification_end_time = 0

    button_exit = Button(1045, 5, 150, 75, color_blank, 10)
    button_exit_text = font_30.get_rect("Выйти")
    button_exit_text.center = button_exit.rect.center
    button_exit_text.y -= 5 * 0.55

    info_title = "ЗАГАДАЙТЕ СЛОВО"
    info_title_rect = font_55.get_rect(info_title)
    info_title_rect.centerx = screen_x // 2
    info_title_rect.y = 120

    info_subtitle = "Второй игрок должен отвернуться от экрана!"
    info_subtitle_rect = font_30.get_rect(info_subtitle)
    info_subtitle_rect.centerx = screen_x // 2
    info_subtitle_rect.y = 190

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if mp_state in ["won", "lost"]:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return

            # Кнопка выхода во время активной игры
            if event.type == pygame.MOUSEBUTTONDOWN and mp_state in ["setup", "playing"]:
                if event.button == 1:
                    if button_exit.rect.collidepoint(event.pos):
                        return

            if mp_state in ["setup", "playing"] and current_attempt < 6:  
                if delete_key.check_press(event) and len(current_word) > 0:
                    current_word = current_word[:-1]
                    cell_idx = (current_attempt * 5) + len(current_word)
                    game_grid[cell_idx].letter = ""

                for key_btn in keyboard:
                    if key_btn.check_press(event):
                        if len(current_word) < 5:
                            cell_idx = (current_attempt * 5) + len(current_word)
                            game_grid[cell_idx].letter = key_btn.letter
                            current_word += key_btn.letter

            if enter_key.check_press(event):
                if mp_state in ["won", "lost"]:
                    return
                
                if len(current_word) == 5:
                    if current_word.lower() in words:
                        
                        if mp_state == "setup":
                            correct_word = current_word.upper()
                            
                            for i in range(5):
                                game_grid[i].letter = ""
                                game_grid[i].rect.y = 5 
                                
                            current_word = ""
                            current_attempt = 0
                            mp_state = "playing"
                            continue 

                        word_remain = list(correct_word)
                        for i in range(5):
                            cell_idx = current_attempt * 5 + i
                            current_letter = current_word[i]

                            if current_word[i] == correct_word[i]:
                                game_grid[cell_idx].change_type("correct")
                                word_remain[i] = "_"
                                for key_button in keyboard:
                                    if key_button.letter == current_letter:
                                        key_button.change_type("correct")

                        for i in range(5):
                            cell_idx = current_attempt * 5 + i
                            current_letter = current_word[i]
                            if current_letter == correct_word[i]:
                                continue
                            if current_word[i] in word_remain:
                                game_grid[cell_idx].change_type("in_word")
                                idx_in_remain = word_remain.index(current_letter)
                                word_remain[idx_in_remain] = "_"
                                for key_button in keyboard:
                                    if key_button.letter == current_letter:
                                        key_button.change_type("in_word")
                            else:
                                game_grid[cell_idx].change_type("not_in_word")
                                for key_button in keyboard:
                                    if key_button.letter == current_letter:
                                        key_button.change_type("not_in_word")

                        if current_word == correct_word:
                            mp_state = "won"

                        current_attempt += 1
                        current_word = ""
                        
                        if current_attempt == 6 and mp_state == "playing":
                            mp_state = "lost"

                    else:
                        correct_check = True
                        notification_end_time = time.time() + 2
                else:
                    correct_check = True
                    notification_end_time = time.time() + 2

        screen.fill(color_bg)

        if mp_state == "setup":
            font_55.render_to(screen, info_title_rect, info_title, color_text)
            font_30.render_to(screen, info_subtitle_rect, info_subtitle, color_not_in_word)

            for i in range(5):
                game_grid[i].rect.y = 270
                game_grid[i].color_draw(screen)
                game_grid[i].make_letter()
        else:
            for blank_1 in game_grid:
                blank_1.color_draw(screen)
                blank_1.make_letter()

        for k_draw in keyboard:
            k_draw.key_draw(screen)

        enter_key.key_draw(screen)
        delete_key.key_draw(screen)

        # Вывод ошибок
        if correct_check and time.time() > notification_end_time:
            correct_check = False

        if correct_check == True:
            button_1_1.button_draw(screen)
            bx, by = button_1_1.rect.x, button_1_1.rect.y
            font_25 = pygame.freetype.Font(resource_path("ClearSans-Bold.ttf"), 25)
            
            line1 = "Такого слова нет в словаре"
            line2 = "или введенное слово состоит не из 5 букв."
            
            font_25.render_to(screen, (bx + 95, by + 28), line1, color_text)
            font_25.render_to(screen, (bx + 95, by + 60), line2, color_text)

        # Кнопка выхода
        if mp_state in ["setup", "playing"]:
            button_exit.button_color_mouse(color_key)
            button_exit.button_draw(screen)
            font_30.render_to(screen, button_exit_text, "Выйти", color_text)

        if mp_state in ["won", "lost"]:
            overlay = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            popup_rect = pygame.Rect(600 - 275, 300, 550, 250)
            pygame.draw.rect(screen, color_blank, popup_rect, border_radius=15)
            
            if mp_state == "won":
                end_title = "ПОБЕДА!"
                title_color = color_correct
            else:
                end_title = "ПОРАЖЕНИЕ"
                title_color = color_not_in_word

            txt_title = font_55.get_rect(end_title)
            txt_title.center = (popup_rect.centerx, popup_rect.y + 60)
            font_55.render_to(screen, txt_title, end_title, title_color)

            word_info = f"Было загадано слово: {correct_word}"
            txt_info = font_30.get_rect(word_info)
            txt_info.center = (popup_rect.centerx, popup_rect.y + 130)
            font_30.render_to(screen, txt_info, word_info, color_text)

            hint_text = "Кликните в любое место для выхода"
            txt_hint = font_20.get_rect(hint_text)
            txt_hint.center = (popup_rect.centerx, popup_rect.y + 200)
            font_20.render_to(screen, txt_hint, hint_text, color_text)

        timer.tick(60)
        pygame.display.flip()

# ----- квесты -----
def start_game_scene_5():
    global total_wins, total_losses, player_coins, total_completed_quests
    update_daily_quests()

    button_exit = Button(1045, 5, 150, 75, color_blank, 10)
    button_exit_text = font_30.get_rect("Выйти")
    button_exit_text.center = button_exit.rect.center
    button_exit_text.y -= 5 * 0.55

    # Переменные для скроллинга
    scroll_y = 0
    is_dragging = False
    start_mouse_y = 0
    start_scroll_y = 0

    while True:
        today_done_count = sum(1 for q in active_quests.values() if q["done"])
        active_keys = list(active_quests.keys())
        sorted_q_keys = sorted(active_keys, key=lambda k: active_quests[k]["done"])

        cards_list = []
        card_w, card_h = 750, 100
        start_card_x = 25
        start_card_y = 150 
        gap = 15

        for idx, q_key in enumerate(sorted_q_keys):
            y = start_card_y + idx * (card_h + gap)
            cards_list.append(QuestCard(start_card_x, y, card_w, card_h, q_key))

        total_list_height = len(cards_list) * (card_h + gap)
        max_scroll_up = -(total_list_height - (screen_y - start_card_y) + 40)
        if max_scroll_up > 0: 
            max_scroll_up = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_exit.rect.collidepoint(event.pos):
                    return
                
                if event.pos[0] < 800:
                    is_dragging = True
                    start_mouse_y = event.pos[1]
                    start_scroll_y = scroll_y

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_dragging = False

            if event.type == pygame.MOUSEMOTION and is_dragging:
                delta_y = event.pos[1] - start_mouse_y
                scroll_y = start_scroll_y + delta_y
                if scroll_y > 0: scroll_y = 0
                if scroll_y < max_scroll_up: scroll_y = max_scroll_up

        screen.fill(color_bg)
        
        for card in cards_list:
            if card.rect.y + scroll_y >= 120 or card.rect.y + scroll_y <= screen_y:
                card.draw(screen, scroll_y)

        pygame.draw.rect(screen, color_bg, (0, 0, 800, 140))

        game_text = font_90.get_rect("КВЕСТЫ")
        game_text.x = 25
        game_text.y = 25
        font_90.render_to(screen, game_text, "КВЕСТЫ", color_text)

        stats_data = [
            ("Монеты", str(player_coins), color_in_word),
            ("Победы", str(total_wins), color_correct),
            ("Поражения", str(total_losses), color_text),
            ("Серия побед", f"{current_win_streak}/{max_win_streak}", color_text),
            ("Выполнено", f"{today_done_count}/5", color_text)
        ]

        widget_x = 790
        widget_y = 150
        widget_w, widget_h = 385, 100  
        widget_gap = 15                

        for label, value, val_color in stats_data:
            pygame.draw.rect(screen, color_blank, (widget_x, widget_y, widget_w, widget_h), border_radius=12)

            txt_label = font_30.get_rect(label)
            txt_label.x = widget_x + 25 
            txt_label.centery = widget_y + (widget_h // 2)
            font_30.render_to(screen, txt_label, label, color_not_in_word)

            if len(value) >= 9:
                active_font = font_20
            elif len(value) >= 6:
                active_font = font_30
            else:
                active_font = font_45

            txt_val = active_font.get_rect(value)
            txt_val.right = widget_x + widget_w - 25 
            txt_val.centery = widget_y + (widget_h // 2)
            active_font.render_to(screen, txt_val, value, val_color)

            widget_y += widget_h + widget_gap

        # Кнопка выхода
        button_exit.button_color_mouse(color_key)
        button_exit.button_draw(screen)
        font_30.render_to(screen, button_exit_text, "Выйти", color_text)

        if globals().get("draw_ach_notification"):
            draw_ach_notification(screen)

        timer.tick(60)
        pygame.display.flip()

# ----- сцена -----
button_1=Button(275, 235, 650, 100, color_key, 15)
button_2=Button(275, 345, 650, 100, color_key, 15)
button_3=Button(275, 455, 650, 100, color_key, 15)
button_4=Button(275, 565, 650, 100, color_key, 15)
button_5=Button(275, 675, 320, 100, color_key, 15)
button_6=Button(605, 675, 320, 100, color_key, 15)

# 1. Заголовок
title_rect = font_120.get_rect("Угадай слово")
title_rect.center = (screen_x // 2, screen_y // 2)
title_rect.x -= 0
title_rect.y -= 325

# 3. Нижний текст
cpr_rect = font_20.get_rect("Угадай слово by MGGamesStudio. v.1.0.1")
cpr_rect.center = (screen_x // 2, screen_y // 2)
cpr_rect.x -= 0
cpr_rect.y += 425

# 3. Текст на кнопках
button_1_text_rect = font_55.get_rect("Играть")
button_1_text_rect.center = button_1.rect.center
button_1_text_rect.y += 2
button_2_text_rect = font_55.get_rect("Как играть")
button_2_text_rect.center = button_2.rect.center
button_2_text_rect.y += 2
button_3_text_rect = font_55.get_rect("Достижения")
button_3_text_rect.center = button_3.rect.center
button_4_text_rect = font_55.get_rect("Кастомизация")
button_4_text_rect.center = button_4.rect.center
button_5_text_rect = font_55.get_rect("Квесты")
button_5_text_rect.center = button_5.rect.center
button_5_text_rect.y -= 3
button_6_text_rect = font_55.get_rect("Выйти")
button_6_text_rect.center = button_6.rect.center
button_6_text_rect.y -= 5

def start_pc_game(all_words, player_stats, save_function):
    global words, external_save_func

    words = [w.lower() for w in all_words]
    external_save_func = save_function

    global player_coins, total_wins, total_losses, current_win_streak, max_win_streak, total_completed_quests, last_update_day
    global active_quests
    
    player_coins = player_stats.get("player_coins", 0)
    total_wins = player_stats.get("total_wins", 0)
    total_losses = player_stats.get("total_losses", 0)
    current_win_streak = player_stats.get("current_win_streak", 0)
    max_win_streak = player_stats.get("max_win_streak", 0)
    total_completed_quests = player_stats.get("total_completed_quests", 0)
    last_update_day = player_stats.get("last_update_day", -1)
    active_quests = player_stats.get("active_quests", {})
    
    unlocked_themes = player_stats.get("unlocked_themes", {})
    for k, is_unlocked in unlocked_themes.items():
        if k in color_themes:
            color_themes[k]["unlocked"] = is_unlocked
            
    unlocked_achivements = player_stats.get("unlocked_achivements", {})
    for k, ach_info in unlocked_achivements.items():
        if k in achivements:
            achivements[k]["got"] = ach_info.get("got", False)
            achivements[k]["date"] = ach_info.get("date", "")
            
    active_theme = player_stats.get("active_theme_name", "classic")
    if active_theme in color_themes:
        choose_theme(active_theme)
        
    print("[MGGamesStudio ПК] Все данные успешно приняты из лаунчера!")
    start_game_scene_menu() 

def start_game_scene_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_progress()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_1.rect.collidepoint(event.pos):
                        choose_game_mode_scene()
                    if button_2.rect.collidepoint(event.pos):
                        start_game_scene_2()
                    if button_3.rect.collidepoint(event.pos):
                        start_game_scene_3()
                    if button_4.rect.collidepoint(event.pos):
                        start_game_scene_4()
                    if button_5.rect.collidepoint(event.pos):
                        start_game_scene_5()
                    if button_6.rect.collidepoint(event.pos):
                        save_game_progress()
                        pygame.quit()
                        sys.exit()

        screen.fill(color_bg)

        # Кнопки
        button_1.button_color_mouse(color_key)
        button_1.button_draw(screen)
        button_2.button_color_mouse(color_key)
        button_2.button_draw(screen)
        button_3.button_color_mouse(color_key)
        button_3.button_draw(screen)
        button_4.button_color_mouse(color_key)
        button_4.button_draw(screen)
        button_5.button_color_mouse(color_key)
        button_5.button_draw(screen)
        button_6.button_color_mouse(color_key)
        button_6.button_draw(screen)

        # Текст
        font_120.render_to(screen, title_rect, "Угадай слово", color_text)
        font_20.render_to(screen, cpr_rect, "Угадай слово by MGGamesStudio. v.1.0.1", color_not_in_word)

        font_55.render_to(screen, button_1_text_rect, "Играть", color_text)
        font_55.render_to(screen, button_2_text_rect, "Как играть", color_text)
        font_55.render_to(screen, button_3_text_rect, "Достижения", color_text)
        font_55.render_to(screen, button_4_text_rect, "Кастомизация", color_text)
        font_55.render_to(screen, button_5_text_rect, "Квесты", color_text)
        font_55.render_to(screen, button_6_text_rect, "Выйти", color_text)

        draw_ach_notification(screen)

        timer.tick(60)
        flip_scaled_screen()
