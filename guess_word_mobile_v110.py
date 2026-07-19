import os
import sys
import random

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from kivy.graphics import Color, RoundedRectangle

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

def apply_adaptive_layouts(screen_instance, win_w, win_h):
    """
    Универсальная функция адаптивной верстки для GuessWordGame.
    Рассчитывает резиновые бланки, клавиатуру, шрифты и центрирует буквы.
    """
    # 1. АДАПТИВНЫЙ РАСЧЕТ РАЗМЕРОВ БЛАНКА (Жесткие 65% высоты)
    CELL_SPACING_X = 5
    CELL_SPACING_Y = 5
    side_margin = win_w * 0.11
    avail_cell_w = win_w - (2 * side_margin) - 20
    CELL_WIDTH = avail_cell_w / 5  
    CELL_HEIGHT = CELL_WIDTH * 1.243  

    total_blanks_height = (6 * CELL_HEIGHT) + (5 * CELL_SPACING_Y)
    max_allowed_height = win_h * 0.65

    if total_blanks_height > max_allowed_height:
        total_blanks_height = max_allowed_height
        CELL_HEIGHT = (total_blanks_height - (5 * CELL_SPACING_Y)) / 6
        CELL_WIDTH = CELL_HEIGHT / 1.243
        side_margin = (win_w - (5 * CELL_WIDTH) - 20) / 2

    # Идеальный масштаб шрифта бланка (48% от его высоты)
    cell_font_size_px = CELL_HEIGHT * 0.48

    for cell in screen_instance.cells:
        cell.size = (CELL_WIDTH, CELL_HEIGHT)
        cell.font_size = f"{cell_font_size_px}px"
        # Идеальное вертикальное и горизонтальное центрирование букв в ячейках
        cell.text_size = cell.size
        cell.halign = 'center'
        cell.valign = 'middle'

    # 2. ФИКСИРУЕМ ПОЛОЖЕНИЕ КЛАВИАТУРЫ ОТ ПОЛНОЙ ПАЧКИ БЛАНКОВ
    virtual_bottom_line = (win_h - 5) - total_blanks_height
    KEY_SPACING_X = 4
    avail_w = win_w - 16 - 44
    KEY_WIDTH = avail_w / 12  
    KEY_SPACING_Y = 4
    avail_h = virtual_bottom_line - 16 - 12
    KEY_HEIGHT = avail_h / 4  

    row_heights = [
        8,
        8 + (KEY_HEIGHT + KEY_SPACING_Y),
        8 + 2 * (KEY_HEIGHT + KEY_SPACING_Y),
        8 + 3 * (KEY_HEIGHT + KEY_SPACING_Y)
    ]

    # Масштабы шрифтов клавиатуры
    key_font_size_px = KEY_HEIGHT * 0.38       # Буквы (38%)
    sys_font_size_px = KEY_HEIGHT * 0.20       # СТЕРЕТЬ/ВЫХОД/ВВОД (20%)

    # Применяем размеры, шрифты и микро-сдвиг вверх ко всей клавиатуре
    for key in screen_instance.keyboard_keys:
        key.size = (KEY_WIDTH, KEY_HEIGHT)
        key.font_size = f"{key_font_size_px}px"
        key.text_size = key.size
        key.halign = 'center'
        key.valign = 'middle'
        key.padding_y = 3 # Точечно приподнимаем буквы к центру плашки

    # Раскладываем буквенные ряды по экрану
    line_to_height_idx = {0: 2, 1: 1, 2: 0}
    for i, line_keys in enumerate(screen_instance.letter_buttons):
        h_idx = line_to_height_idx[i]
        total_w = len(line_keys) * KEY_WIDTH + (len(line_keys) - 1) * KEY_SPACING_X
        start_l_x = (win_w - total_w) / 2
        for idx, key in enumerate(line_keys):
            key.pos = (start_l_x + idx * (KEY_WIDTH + KEY_SPACING_X), row_heights[h_idx])
            key.update_canvas()

    # Системные кнопки
    SYS_SPACING = 4
    avail_sys_w = win_w - 16 - (2 * SYS_SPACING)
    SYS_WIDTH = avail_sys_w / 3
    start_sys_x = 8
    
    for btn in [screen_instance.btn_erase, screen_instance.btn_exit, screen_instance.btn_enter]:
        btn.size = (SYS_WIDTH, KEY_HEIGHT)
        btn.font_size = f"{sys_font_size_px}px"
        btn.text_size = btn.size
        btn.halign = 'center'
        btn.valign = 'middle'
        btn.padding_y = 2

    screen_instance.btn_erase.pos = (start_sys_x, row_heights)
    screen_instance.btn_erase.update_canvas()
    
    screen_instance.btn_exit.pos = (start_sys_x + SYS_WIDTH + SYS_SPACING, row_heights)
    screen_instance.btn_exit.update_canvas()
    
    screen_instance.btn_enter.pos = (start_sys_x + 2 * (SYS_WIDTH + SYS_SPACING), row_heights)
    screen_instance.btn_enter.update_canvas()

    # Возвращаем наружу вычисленные данные, которые могут понадобиться экранам локально
    return CELL_WIDTH, CELL_HEIGHT, row_heights, KEY_HEIGHT

class MenuButton(Button):
    def __init__(self, text="", pos_hint=None, size_hint=(0.93, None), height=84, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_name = resource_path("ClearSans-Bold.ttf")
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
        
        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.state == 'normal':
                Color(*self.base_color)
            else:
                Color(self.base_color[0]*0.8, self.base_color[1]*0.8, self.base_color[2]*0.8, 1.0)
            
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

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
        
        # 1. Название режима (30sp, жирный, опущен к нижней границе своей половины через valign='bottom')
        self.title_label = Label(
            text=title_text,
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='30sp',
            bold=True,
            color=color_text,
            halign='center',
            valign='bottom',
            size_hint=(1, 0.5)
        )
        self.title_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        
        # 2. Описание режима (14sp, прижато к верхней границе своей половины через valign='top')
        self.sub_label = Label(
            text=description_text,
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='14sp',
            color=description_color if description_color else color_text,
            halign='center',
            valign='top',
            size_hint=(1, 0.5)
        )
        self.sub_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        
        self.add_widget(self.title_label)
        self.add_widget(self.sub_label)
        
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.current_bg)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

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
        self.font_name = resource_path("ClearSans-Bold.ttf")
        self.font_size = '32sp'
        self.bold = True
        
        # Жестко фиксируем позицию и оригинальный мобильный масштаб
        self.size_hint = (None, None)
        self.size = size
        self.pos = pos
        
        self.cell_status = "blank"
        self.base_color = color_blank
        self.text_color = color_text
        
        self.color = self.text_color
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
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.base_color)
            # Фиксируем числовое скругление без конфликтов типов
            RoundedRectangle(pos=self.pos, size=self.size, radius=[6])

class KeyButton(Button):
    def __init__(self, text="", size=(40, 85), **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_name = resource_path("ClearSans-Bold.ttf")
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
        
        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.state == 'normal':
                Color(*self.base_color)
            else:
                Color(self.base_color[0]*0.8, self.base_color[1]*0.8, self.base_color[2]*0.8, 1.0)
            
            # Рисуем строго по размерам объекта кнопки без фиксированных костылей
            RoundedRectangle(pos=self.pos, size=self.size, radius=[6])

# ----- ИГРА ----
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        layout.add_widget(Label(
            text="Угадай слово", 
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='52sp', 
            bold=True, 
            color=color_text,
            size_hint=(1, None), 
            height=80,
            pos_hint={'center_x': 0.5, 'center_y': 0.88}))
        
        buttons_container = BoxLayout(
            orientation='vertical', 
            spacing=14, 
            size_hint=(0.93, None), 
            height=476,
            pos_hint={'center_x': 0.5, 'center_y': 0.50} )
        
        # Кнопки
        btn_play = MenuButton(text="Играть", size_hint=(1, None), height=84)
        btn_play.bind(on_release=lambda x: setattr(self.manager, 'current', 'game'))
        buttons_container.add_widget(btn_play)
        
        btn_how = MenuButton(text="Как играть", size_hint=(1, None), height=84)
        btn_how.bind(on_release=lambda x: setattr(self.manager, 'current', 'how_to_play'))
        buttons_container.add_widget(btn_how)
        
        btn_achievements = MenuButton(text="Достижения", size_hint=(1, None), height=84)
        btn_achievements.bind(on_release=lambda x: setattr(self.manager, 'current', 'achievements'))
        buttons_container.add_widget(btn_achievements)
        
        btn_customization = MenuButton(text="Кастомизация", size_hint=(1, None), height=84)
        btn_customization.bind(on_release=lambda x: setattr(self.manager, 'current', 'customization'))
        buttons_container.add_widget(btn_customization)
        
        # Нижний ряд (Квесты и Выйти)
        bottom_row = BoxLayout(orientation='horizontal', spacing=14, size_hint=(1, None), height=84)
        
        btn_quests = MenuButton(text="Квесты", size_hint=(0.5, 1))
        btn_quests.bind(on_release=lambda x: setattr(self.manager, 'current', 'quests'))
        bottom_row.add_widget(btn_quests)
        
        btn_exit = MenuButton(text="Выйти", size_hint=(0.5, 1))
        btn_exit.bind(on_release=lambda x: App.get_running_app().stop())
        bottom_row.add_widget(btn_exit)
        
        buttons_container.add_widget(bottom_row)
        layout.add_widget(buttons_container)
        
        copy_label = Label(
            text="Угадай слово by MGGamesStudio. v.1.1.0", 
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='11sp', 
            color=color_not_in_word, 
            pos_hint={'center_x': 0.5, 'center_y': 0.03})
        layout.add_widget(copy_label)
        
        self.add_widget(layout)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # Кнопка назад
        btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        btn_back.pos = (Window.width - 100 - 15, Window.height - 54 - 44)
        btn_back.font_size = '20sp'
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(btn_back)
        
        layout.add_widget(Label(
            text="ВЫБЕРИТЕ РЕЖИМ ИГРЫ", 
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='26sp', 
            bold=True, 
            color=color_text,
            size_hint=(1, None), 
            height=60,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        ))
        
        # ИСПРАВЛЕНО: Ширина контейнера увеличена до 350px под оригинальный размер блоков
        mode_container = BoxLayout(
            orientation='vertical', 
            spacing=55, 
            size_hint=(None, None), 
            size=(350, 440),
            pos_hint={'center_x': 0.5, 'center_y': 0.5} # Оставляем твой идеальный центр 0.5
        )
        
        btn_1p = ModeButton(
            title_text="1 ИГРОК", 
            description_text="С достижениями и монетами", 
            description_color=color_correct,
            on_release=lambda x: setattr(self.manager, 'current', 'one_player_game')
        )
        mode_container.add_widget(btn_1p)
        
        btn_2p = ModeButton(
            title_text="2 ИГРОКА", 
            description_text="Без достижений и монет", 
            description_color=color_not_in_word,
            on_release=lambda x: setattr(self.manager, 'current', 'two_player_game')
        )
        mode_container.add_widget(btn_2p)
        
        layout.add_widget(mode_container)
        self.add_widget(layout)

class OnePlayerGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        # 1. Задний фон экрана
        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))
            
        # 2. Создаем бланки сетки 6х5
        self.cells = []
        for _ in range(30):
            cell = GameCell(size=(74, 92))
            cell.base_color = color_blank
            self.cells.append(cell)
            self.layout.add_widget(cell)
            
        # 3. Список для хранения буквенных клавиш (критично для reposition)
        self.keyboard_keys = []
        
        # 4. Три новые большие системные кнопки в белом пространстве
        self.btn_erase = KeyButton(text="СТЕРЕТЬ", size=(100, 50))
        self.btn_erase.font_size = '22sp'
        self.btn_erase.bind(on_release=self.press_erase_key)
        
        self.btn_exit = KeyButton(text="ВЫХОД", size=(100, 50))
        self.btn_exit.font_size = '22sp'
        self.btn_exit.bind(on_release=self.press_exit_key)

        
        self.btn_enter = KeyButton(text="ВВОД", size=(100, 50))
        self.btn_enter.font_size = '22sp'
        self.btn_enter.bind(on_release=self.press_enter_key)
        
        self.layout.add_widget(self.btn_erase)
        self.layout.add_widget(self.btn_exit)
        self.layout.add_widget(self.btn_enter)
        
        # 5. Буквенная клавиатура с привязкой событий тача
        self.lines = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮЁ"]
        self.letter_buttons = []
        for line in self.lines:
            row_buttons = []
            for char in line:
                key = KeyButton(text=char, size=(40, 85))
                key.font_size = '22sp'
                
                # ЖЕСТКАЯ ПРИВЯЗКА КЛИКА: передаем нажатую букву в метод
                key.bind(on_release=self.press_letter_key)
                
                self.keyboard_keys.append(key)
                self.layout.add_widget(key)
                row_buttons.append(key)
            self.letter_buttons.append(row_buttons)
                
        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        # ----- ИГРА ----
        self.current_word = ""
        self.current_attempt = 0
        self.secret_word = ""

        self.reset_game()

    def reposition_elements(self, instance, size):
        win_w = Window.width
        win_h = Window.height
        self.bg_rect.size = (win_w, win_h)

        # =========================================================================
        # 1. АДАПТИВНЫЙ РАСЧЕТ БЛАНКОВ С ЛИМИТОМ В 65% ОТ ВЫСОТЫ ЭКРАНА
        # =========================================================================
        CELL_SPACING_X = 5
        CELL_SPACING_Y = 5
        
        # Стартовый базовый отступ от стен (11% от ширины)
        side_margin = win_w * 0.11
        
        # Считаем стандартные размеры ячейки по горизонтали
        avail_cell_w = win_w - (2 * side_margin) - 20
        CELL_WIDTH = avail_cell_w / 5  
        CELL_HEIGHT = CELL_WIDTH * 1.243  

        # ПРЕДОХРАНИТЕЛЬ: Проверяем, не превышает ли вся пачка бланков 65% высоты окна
        # Высота всей пачки: 6 рядов по CELL_HEIGHT + 5 зазоров по 5px
        total_blanks_height = (6 * CELL_HEIGHT) + (5 * CELL_SPACING_Y)
        max_allowed_height = win_h * 0.65

        if total_blanks_height > max_allowed_height:
            # Если превышает (окно квадратное), принудительно зажимаем сетку в лимит
            total_blanks_height = max_allowed_height
            # Обратным ходом вычисляем высоту и ширину одной ячейки из лимита
            CELL_HEIGHT = (total_blanks_height - (5 * CELL_SPACING_Y)) / 6
            CELL_WIDTH = CELL_HEIGHT / 1.243
            # Пересчитываем боковые отступы, чтобы уменьшенная сетка осталась строго по центру
            side_margin = (win_w - (5 * CELL_WIDTH) - 20) / 2

        # Принудительно растягиваем визуальные размеры RoundedRectangle у бланков
        for cell in self.cells:
            cell.size = (CELL_WIDTH, CELL_HEIGHT)

        # Позиционируем ячейки сетки (start_blank_x теперь зависит от side_margin)
        start_blank_x = side_margin
        start_blank_y = win_h - CELL_HEIGHT - 5
        
        cell_idx = 0
        for row in range(6):
            for col in range(5):
                if cell_idx < len(self.cells):
                    self.cells[cell_idx].pos = (start_blank_x + col * (CELL_WIDTH + CELL_SPACING_X), start_blank_y - row * (CELL_HEIGHT + CELL_SPACING_Y))
                    self.cells[cell_idx].update_canvas()
                    cell_idx += 1

        # НАХОДИМ ОКОНЧАТЕЛЬНУЮ НИЖНЮЮ ЛИНИЮ БЛОКОВ (Клавиатура сама подстроится под неё!)
        bottom_blanks_line = (win_h - 5) - total_blanks_height

        # =========================================================================
        # 2. РЕЗИНОВАЯ МАТЕМАТИКА КЛАВИАТУРЫ (Остается без изменений!)
        # =========================================================================
        KEY_SPACING_X = 4
        avail_w = win_w - 16 - 44
        KEY_WIDTH = avail_w / 12  # Динамическая ширина кнопки по 1-му ряду
        
        KEY_SPACING_Y = 4
        # Доступная чистая высота — от пола до вычисленной нижней линии бланков
        # Минус отступы сверху и снизу по 8px (16px) и 3 зазора между 4 рядами по 4px (12px)
        avail_h = bottom_blanks_line - 16 - 12
        KEY_HEIGHT = avail_h / 4  # Идеальная динамическая высота кнопки

        # Принудительно растягиваем размеры всех кнопок клавиатуры
        for key in self.keyboard_keys:
            key.size = (KEY_WIDTH, KEY_HEIGHT)

        # Высчитываем высоты для каждого из 4-х рядов от пола (8px отступ)
        row_heights = [
            8,                                              # 3-й ряд букв ("ЯЧС...")
            8 + (KEY_HEIGHT + KEY_SPACING_Y),               # 2-й ряд букв ("ФЫВА...")
            8 + 2 * (KEY_HEIGHT + KEY_SPACING_Y),           # 1-й ряд букв ("ЙЦУКЕН...")
            8 + 3 * (KEY_HEIGHT + KEY_SPACING_Y)            # 0-й ряд ("СТЕРЕТЬ ВЫХОД ВВОД")
        ]

        # Д. Расстановка буквенных рядов строго по центру экрана
        line_to_height_idx = {0: 2, 1: 1, 2: 0}
        for i, line_keys in enumerate(self.letter_buttons):
            h_idx = line_to_height_idx[i]
            total_w = len(line_keys) * KEY_WIDTH + (len(line_keys) - 1) * KEY_SPACING_X
            start_l_x = (win_w - total_w) / 2
                
            for idx, key in enumerate(line_keys):
                key.pos = (start_l_x + idx * (KEY_WIDTH + KEY_SPACING_X), row_heights[h_idx])
                key.update_canvas()

        # Е. Расстановка 0 ряда "СТЕРЕТЬ ВЫХОД ВВОД" абсолютно одинаковой длины
        SYS_SPACING = 4
        avail_sys_w = win_w - 16 - (2 * SYS_SPACING)
        SYS_WIDTH = avail_sys_w / 3
        
        start_sys_x = 8
        
        self.btn_erase.pos = (start_sys_x, row_heights[3])
        self.btn_erase.size = (SYS_WIDTH, KEY_HEIGHT)
        self.btn_erase.update_canvas()
        
        self.btn_exit.pos = (start_sys_x + SYS_WIDTH + SYS_SPACING, row_heights[3])
        self.btn_exit.size = (SYS_WIDTH, KEY_HEIGHT)
        self.btn_exit.update_canvas()
        
        self.btn_enter.pos = (start_sys_x + 2 * (SYS_WIDTH + SYS_SPACING), row_heights[3])
        self.btn_enter.size = (SYS_WIDTH, KEY_HEIGHT)
        self.btn_enter.update_canvas()

    def press_letter_key(self, instance):
        """Срабатывает при нажатии на любую букву виртуальной клавиатуры"""
        letter = instance.text
        
        # Твоя проверка из ПК-версии: если в слове меньше 5 букв
        if len(self.current_word) < 5:
            # Математический расчет индекса клетки из твоего оригинального кода
            cell_idx = (self.current_attempt * 5) + len(self.current_word)
            
            if cell_idx < len(self.cells):
                # Записываем букву в бланк Kivy (используем .text вместо .letter)
                self.cells[cell_idx].text = letter
                
                # Добавляем букву в наше текущее слово
                self.current_word += letter

    def press_erase_key(self, instance):
        """Срабатывает при нажатии на большую кнопку СТЕРЕТЬ"""
        # Твоя проверка из ПК-версии: стирать можно, только если в слове уже есть буквы
        if len(self.current_word) > 0:
            # Точный расчет индекса последней заполненной ячейки
            cell_idx = (self.current_attempt * 5) + len(self.current_word) - 1
            
            if cell_idx < len(self.cells):
                # Стираем текст на экране Kivy
                self.cells[cell_idx].text = ""
                
                # Обрезаем последнюю букву в нашей переменной слова
                self.current_word = self.current_word[:-1]

    def press_enter_key(self, instance):
        """Срабатывает при нажатии на большую кнопку ВВОД"""
        if len(self.current_word) == 5:
            check_word = self.current_word.upper()
            
            if 'MOBILE_ALL_WORDS' in globals() and MOBILE_ALL_WORDS and check_word in MOBILE_ALL_WORDS:
                print(f"Слово валидно и найдено в словаре: {self.current_word}")
                
                row_statuses = ["not_in_word"] * 5
                secret_chars = list(self.secret_word)
                guess_chars = list(check_word)
                
                # ШАГ А: Ищем точные совпадения (Зелёные буквы)
                for i in range(5):
                    if guess_chars[i] == secret_chars[i]:
                        row_statuses[i] = "correct"
                        secret_chars[i] = None
                        guess_chars[i] = b" "
                        
                # ШАГ Б: Ищем частичные совпадения (Жёлтые буквы)
                for i in range(5):
                    if guess_chars[i] != b" " and guess_chars[i] in secret_chars:
                        row_statuses[i] = "in_word"
                        idx = secret_chars.index(guess_chars[i])
                        secret_chars[idx] = None
                
                # ШАГ В: Применяем цвета к бланкам Kivy на экране
                start_idx = self.current_attempt * 5
                for i in range(5):
                    cell_idx = start_idx + i
                    if cell_idx < len(self.cells):
                        self.cells[cell_idx].change_type(row_statuses[i])

                # ПОКРАСКА КНОПОК ВИРТУАЛЬНОЙ КЛАВИАТУРЫ
                for i in range(5):
                    char_in_guess = self.current_word[i].upper()
                    status_for_char = row_statuses[i]
                    
                    for key_btn in self.keyboard_keys:
                        if key_btn.text == char_in_guess:
                            if key_btn.cell_status == "correct":
                                continue
                            elif key_btn.cell_status == "in_word" and status_for_char != "correct":
                                continue
                                
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

                # Проверяем победу
                if check_word == self.secret_word:
                    self.show_game_popup(
                        "ПОБЕДА!", 
                        f"Было загадано слово: {self.secret_word}",
                        color_correct,
                        is_end_game=True
                    )
                    return

                # Переходим к следующей строке попыток
                self.current_attempt += 1
                self.current_word = ""
                
                # Если проигрыш (ИСПРАВЛЕНО: Заголовок красится в color_not_in_word)
                if self.current_attempt >= 6:
                    self.show_game_popup(
                        "ИГРА ОКОНЧЕНА", 
                        f"Загаданное слово было: {self.secret_word}",
                        color_not_in_word,
                        is_end_game=True
                    )
            else:
                # ИСПРАВЛЕНО: Заголовок ошибки полностью подчиняется цвету темы color_text
                self.show_game_popup(
                    "Такого слова нет в словаре", 
                    "или введенное слово состоит не из 5 букв.",
                    color_text,
                    is_end_game=False
                )

    def press_exit_key(self, instance):
        """Срабатывает при нажатии на ВЫХОД: сбрасывает поле и уводит в меню"""
        self.reset_game()  # Вызываем очистку поля
        self.manager.current = 'game'  # Переключаем экран обратно в меню выбора режимов

    def reset_game(self):
        """Полностью сбрасывает состояние игрового поля, клавиатуры и выбирает новое слово"""
        for cell in self.cells:
            cell.text = ""
            cell.base_color = color_blank
            # ИСПРАВЛЕНО: Принудительно возвращаем тексту ячеек твой родной color_text темы!
            cell.color = color_text
            cell.update_canvas()
            
        # Сбрасываем цвета кнопок букв клавиатуры при новой игре
        for key_btn in self.keyboard_keys:
            key_btn.base_color = color_key
            key_btn.color = color_text
            key_btn.cell_status = "blank"
            key_btn.update_canvas()
            
        # Возвращаем дефолтный цвет системным кнопкам
        for btn in [self.btn_erase, self.btn_enter, self.btn_exit]:
            btn.base_color = color_key
            btn.color = color_text
            btn.update_canvas()
            
        self.current_word = ""
        self.current_attempt = 0

        if 'MOBILE_ALL_WORDS' in globals() and MOBILE_ALL_WORDS:
            self.secret_word = random.choice(MOBILE_ALL_WORDS).upper()
            print(f"[MGGamesStudio] Загадано новое секретное слово: {self.secret_word}")
        else:
            self.secret_word = "СЛОВО"

    def show_game_popup(self, title_text, msg_text, title_color, is_end_game=False):
        """Создает базовое мобильное модальное окно на базе ModalView с прямыми углами"""
        # Создаем стандартное окно с прозрачным фоном Kivy
        view = ModalView(size_hint=(0.8, None), height=220, auto_dismiss=True, background='')
        
        # Подложка плашки строго в цвет твоей темы
        with view.canvas.before:
            Color(*color_bg)
            self.popup_rect = RoundedRectangle(pos=view.pos, size=view.size, radius=[(0, 0), (0, 0), (0, 0), (0, 0)])
            
        def update_popup_bg(inst, value):
            self.popup_rect.pos = inst.pos
            self.popup_rect.size = inst.size
        view.bind(pos=update_popup_bg, size=update_popup_bg)
        
        box = FloatLayout()
        
        # Заголовок сообщения
        lbl_title = Label(text=title_text, font_name=resource_path("ClearSans-Bold.ttf"),
                          font_size='24sp', color=title_color, bold=True,
                          size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'top': 0.9})
        
        # Текст сообщения
        lbl_msg = Label(text=msg_text, font_name=resource_path("ClearSans-Bold.ttf"),
                        font_size='15sp', color=color_text, bold=True,
                        size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        tip_text = "Кликните в любое место для выхода в меню" if is_end_game else "Кликните в любое место, чтобы скрыть"
        lbl_tip = Label(text=tip_text, font_name=resource_path("ClearSans-Bold.ttf"),
                        font_size='11sp', color=color_not_in_word, bold=True,
                        size_hint=(None, None), size=(300, 30), pos_hint={'center_x': 0.5, 'y': 0.08})
        
        box.add_widget(lbl_title)
        box.add_widget(lbl_msg)
        box.add_widget(lbl_tip)
        view.add_widget(box)
        
        # Перехватываем клик по экрану напрямую через ModalView
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
        
        # 1. Задний фон экрана
        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.lbl_title = Label(text="ЗАГАДАЙТЕ СЛОВО", font_name=resource_path("ClearSans-Bold.ttf"),
                               font_size='32sp', color=color_text, bold=True, size_hint=(None, None))
        self.lbl_subtitle = Label(text="Второй игрок должен отвернуться от экрана!", font_name=resource_path("ClearSans-Bold.ttf"),
                                  font_size='14sp', color=color_not_in_word, bold=True, size_hint=(None, None))
        self.lbl_error = Label(text="", font_name=resource_path("ClearSans-Bold.ttf"),
                               font_size='15sp', color=color_in_word, bold=True, size_hint=(None, None))
        self.layout.add_widget(self.lbl_error)
        self.layout.add_widget(self.lbl_title)
        self.layout.add_widget(self.lbl_subtitle)
            
        # 2. Создаем бланки сетки 6х5
        self.cells = []
        for _ in range(30):
            cell = GameCell(size=(74, 92))
            cell.base_color = color_blank
            self.cells.append(cell)
            self.layout.add_widget(cell)
            
        # 3. Список для хранения буквенных клавиш (критично для reposition)
        self.keyboard_keys = []
        
        # 4. Три новые большие системные кнопки в белом пространстве
        self.btn_erase = KeyButton(text="СТЕРЕТЬ", size=(100, 50))
        self.btn_erase.font_size = '22sp'
        self.btn_erase.bind(on_release=self.press_erase_key)
        
        self.btn_exit = KeyButton(text="ВЫХОД", size=(100, 50))
        self.btn_exit.font_size = '22sp'
        self.btn_exit.bind(on_release=self.press_exit_key)

        
        self.btn_enter = KeyButton(text="ВВОД", size=(100, 50))
        self.btn_enter.font_size = '22sp'
        self.btn_enter.bind(on_release=self.press_enter_key)
        
        self.layout.add_widget(self.btn_erase)
        self.layout.add_widget(self.btn_exit)
        self.layout.add_widget(self.btn_enter)
        
        # 5. Буквенная клавиатура с привязкой событий тача
        self.lines = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮЁ"]
        self.letter_buttons = []
        for line in self.lines:
            row_buttons = []
            for char in line:
                key = KeyButton(text=char, size=(40, 85))
                key.font_size = '22sp'
                
                # ЖЕСТКАЯ ПРИВЯЗКА КЛИКА: передаем нажатую букву в метод
                key.bind(on_release=self.press_letter_key)
                
                self.keyboard_keys.append(key)
                self.layout.add_widget(key)
                row_buttons.append(key)
            self.letter_buttons.append(row_buttons)
                
        self.add_widget(self.layout)
        self.bind(size=self.reposition_elements)

        # ----- ИГРА ----
        self.current_word = ""
        self.current_attempt = 0
        self.secret_word = ""
        self.stage = "setup"

        self.reset_game()

    def reposition_elements(self, instance, size):
        win_w = Window.width
        win_h = Window.height
        self.bg_rect.size = (win_w, win_h)

        # 1. АДАПТИВНЫЙ РАСЧЕТ РАЗМЕРОВ БЛАНКА (Как в OnePlayer)
        CELL_SPACING_X = 5
        CELL_SPACING_Y = 5
        side_margin = win_w * 0.11
        avail_cell_w = win_w - (2 * side_margin) - 20
        CELL_WIDTH = avail_cell_w / 5  
        CELL_HEIGHT = CELL_WIDTH * 1.243  

        total_blanks_height = (6 * CELL_HEIGHT) + (5 * CELL_SPACING_Y)
        max_allowed_height = win_h * 0.65

        if total_blanks_height > max_allowed_height:
            total_blanks_height = max_allowed_height
            CELL_HEIGHT = (total_blanks_height - (5 * CELL_SPACING_Y)) / 6
            CELL_WIDTH = CELL_HEIGHT / 1.243
            side_margin = (win_w - (5 * CELL_WIDTH) - 20) / 2

        for cell in self.cells:
            cell.size = (CELL_WIDTH, CELL_HEIGHT)

        # 2. ФИКСИРУЕМ ПОЛОЖЕНИЕ КЛАВИАТУРЫ (Чтобы она не прыгала)
        virtual_bottom_line = (win_h - 5) - total_blanks_height
        KEY_SPACING_X = 4
        avail_w = win_w - 16 - 44
        KEY_WIDTH = avail_w / 12  
        KEY_SPACING_Y = 4
        avail_h = virtual_bottom_line - 16 - 12
        KEY_HEIGHT = avail_h / 4  

        row_heights = [
            8,
            8 + (KEY_HEIGHT + KEY_SPACING_Y),
            8 + 2 * (KEY_HEIGHT + KEY_SPACING_Y),
            8 + 3 * (KEY_HEIGHT + KEY_SPACING_Y)
        ]

        # =========================================================================
        # 3. ИСПРАВЛЕНО: ЧИСТАЯ МАТЕМАТИКА РАСПРЕДЕЛЕНИЯ ПРОСТРАНСТВА ПОПОЛАМ
        # =========================================================================
        start_blank_x = side_margin
        
        if self.stage == "setup":
            # Точная высота начала клавиатуры (Y-координата верхнего ряда + высота кнопки)
            kbd_top_y = row_heights[3] + KEY_HEIGHT
            
            # А. Бланки встают строго ПОСЕРЕДИНЕ между потолком (win_h) и верхом клавиатуры (kbd_top_y)
            total_free_space_y = win_h - kbd_top_y
            start_blank_y = kbd_top_y + (total_free_space_y - CELL_HEIGHT) // 2
            
            # Б. Заголовки: берем расстояние от потолка до верха бланка и делим ровно НА 2
            space_above_cells = win_h - (start_blank_y + CELL_HEIGHT)
            center_above_y = (start_blank_y + CELL_HEIGHT) + (space_above_cells // 2)
            
            # Ставим главный заголовок по центру этого пространства
            self.lbl_title.pos = (win_w // 2 - self.lbl_title.width // 2, center_above_y + 15)
            # Подсказку опускаем чуть ниже с аккуратным фиксированным зазором (30px от главного текста)
            self.lbl_subtitle.pos = (win_w // 2 - self.lbl_subtitle.width // 2, center_above_y - 15)
            
            # В. Текст ошибки: берем свободное пространство МЕЖДУ низом бланка и клавиатурой и делим НА 2
            space_below_cells = start_blank_y - kbd_top_y
            center_below_y = kbd_top_y + (space_below_cells // 2)
            
            # Ставим ошибку ровно по центру нижнего белого пространства
            self.lbl_error.pos = (win_w // 2 - self.lbl_error.width // 2, center_below_y - self.lbl_error.height // 2)
        else:
            # Во время игры возвращаем всю сетку 6х5 стандартно к потолку
            start_blank_y = win_h - CELL_HEIGHT - 5

        # Расставляем ячейки по вычисленным координатам
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

        # 4. РАССТАНОВКА БУКВ И СИСТЕМНЫХ КНОПОК КЛАВИАТУРЫ (Без изменений)
        for key in self.keyboard_keys:
            key.size = (KEY_WIDTH, KEY_HEIGHT)

        line_to_height_idx = {0: 2, 1: 1, 2: 0}
        for i, line_keys in enumerate(self.letter_buttons):
            h_idx = line_to_height_idx[i]
            total_w = len(line_keys) * KEY_WIDTH + (len(line_keys) - 1) * KEY_SPACING_X
            start_l_x = (win_w - total_w) / 2
            for idx, key in enumerate(line_keys):
                key.pos = (start_l_x + idx * (KEY_WIDTH + KEY_SPACING_X), row_heights[h_idx])
                key.update_canvas()

        SYS_SPACING = 4
        avail_sys_w = win_w - 16 - (2 * SYS_SPACING)
        SYS_WIDTH = avail_sys_w / 3
        start_sys_x = 8
        
        for btn in [self.btn_erase, self.btn_exit, self.btn_enter]:
            btn.size = (SYS_WIDTH, KEY_HEIGHT)
            
        # =========================================================================
        # ИСПРАВЛЕНО НАВЕК: Добавили индексы [3] для системных кнопок управления!
        # =========================================================================
        self.btn_erase.pos = (start_sys_x, row_heights[3])
        self.btn_erase.update_canvas()
        
        self.btn_exit.pos = (start_sys_x + SYS_WIDTH + SYS_SPACING, row_heights[3])
        self.btn_exit.update_canvas()
        
        self.btn_enter.pos = (start_sys_x + 2 * (SYS_WIDTH + SYS_SPACING), row_heights[3])
        self.btn_enter.update_canvas()

    def press_letter_key(self, instance):
        self.lbl_error.text = ""
        """Срабатывает при нажатии на любую букву виртуальной клавиатуры"""
        letter = instance.text
        
        # Твоя проверка из ПК-версии: если в слове меньше 5 букв
        if len(self.current_word) < 5:
            # Математический расчет индекса клетки из твоего оригинального кода
            cell_idx = (self.current_attempt * 5) + len(self.current_word)
            
            if cell_idx < len(self.cells):
                # Записываем букву в бланк Kivy (используем .text вместо .letter)
                self.cells[cell_idx].text = letter
                
                # Добавляем букву в наше текущее слово
                self.current_word += letter

    def press_erase_key(self, instance):
        self.lbl_error.text = ""
        """Срабатывает при нажатии на большую кнопку СТЕРЕТЬ"""
        # Твоя проверка из ПК-версии: стирать можно, только если в слове уже есть буквы
        if len(self.current_word) > 0:
            # Точный расчет индекса последней заполненной ячейки
            cell_idx = (self.current_attempt * 5) + len(self.current_word) - 1
            
            if cell_idx < len(self.cells):
                # Стираем текст на экране Kivy
                self.cells[cell_idx].text = ""
                
                # Обрезаем последнюю букву в нашей переменной слова
                self.current_word = self.current_word[:-1]

    def press_enter_key(self, instance):
        """Срабатывает при нажатии на большую кнопку ВВОД в режиме двух игроков"""
        if len(self.current_word) == 5:
            check_word = self.current_word.upper()
            
            if 'MOBILE_ALL_WORDS' in globals() and MOBILE_ALL_WORDS and check_word in MOBILE_ALL_WORDS:
                
                if self.stage == "setup":
                    self.secret_word = check_word
                    self.stage = "playing"
                    self.current_word = ""
                    
                    # Стираем текст заголовков, чтобы они исчезли с экрана
                    self.lbl_title.text = ""
                    self.lbl_subtitle.text = ""
                    
                    for cell in self.cells:
                        cell.text = ""
                        
                    # Пересчитываем экран — Kivy автоматически вернет бланки к потолку и откроет все 6 рядов!
                    self.reposition_elements(None, None)
                    return
                
                # Дальше идёт твой стандартный код проверки букв (оставляем его без изменений)
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

                # Покраска кнопок клавиатуры (оставляем твой код как есть)
                for i in range(5):
                    char_in_guess = self.current_word[i].upper()
                    status_for_char = row_statuses[i]
                    for key_btn in self.keyboard_keys:
                        if key_btn.text == char_in_guess:
                            if key_btn.cell_status == "correct": continue
                            elif key_btn.cell_status == "in_word" and status_for_char != "correct": continue
                            if status_for_char == "correct": key_btn.base_color = color_correct
                            elif status_for_char == "in_word": key_btn.base_color = color_in_word
                            elif status_for_char == "not_in_word": key_btn.base_color = color_not_in_word
                            key_btn.cell_status = status_for_char
                            key_btn.update_canvas()

                # Проверка победы (ИСПРАВЛЕНО: Меняем текст уведомления на "Второй игрок")
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
                    # Вместо модального окна выводим ошибку текстом в белое пространство!
                    self.lbl_error.text = "Такого слова нет в словаре!"
                    self.reposition_elements(None, None) # Обновляем позицию текста
                else:
                    self.show_game_popup("Такого слова нет в словаре", "или введенное слово состоит не из 5 букв.", color_text, is_end_game=False)

    def press_exit_key(self, instance):
        """Срабатывает при нажатии на ВЫХОД: сбрасывает поле и уводит в меню"""
        self.reset_game()  # Вызываем очистку поля
        self.manager.current = 'game'  # Переключаем экран обратно в меню выбора режимов

    def reset_game(self):
        """Полностью очищает игру двух игроков и возвращает состояние к стартовому setup"""
        self.stage = "setup"
        self.current_word = ""
        self.current_attempt = 0
        self.secret_word = ""
        
        # 1. Возвращаем исходные чистые заголовки на экран
        self.lbl_title.text = "ЗАГАДАЙТЕ СЛОВО"
        self.lbl_subtitle.text = "Второй игрок должен отвернуться от экрана!"
        self.lbl_error.text = ""
        
        # 2. Очищаем бланки клеток, возвращая дефолтные цвета ячейкам и шрифтам
        for cell in self.cells:
            cell.text = ""
            cell.base_color = color_blank
            cell.color = color_text
            cell.update_canvas()
            
        # 3. ИСПРАВЛЕНО: Принудительно сбрасываем цвета кнопок букв клавиатуры в серый!
        for key_btn in self.keyboard_keys:
            key_btn.base_color = color_key
            key_btn.color = color_text
            key_btn.cell_status = "blank"
            key_btn.update_canvas()
            
        # 4. Возвращаем дефолтный цвет системным кнопкам
        for btn in [self.btn_erase, self.btn_enter, self.btn_exit]:
            btn.base_color = color_key
            btn.color = color_text
            btn.update_canvas()
            
        # 5. ИСПРАВЛЕНО: Принудительно заставляем макет пересчитать геометрию,
        # чтобы спрятать 25 ячеек обратно и выровнять клавиатуру
        self.reposition_elements(None, None)

    def show_game_popup(self, title_text, msg_text, title_color, is_end_game=False):
        """Создает базовое мобильное модальное окно на базе ModalView с прямыми углами"""
        # Создаем стандартное окно с прозрачным фоном Kivy
        view = ModalView(size_hint=(0.8, None), height=220, auto_dismiss=True, background='')
        
        # Подложка плашки строго в цвет твоей темы
        with view.canvas.before:
            Color(*color_bg)
            self.popup_rect = RoundedRectangle(pos=view.pos, size=view.size, radius=[(0, 0), (0, 0), (0, 0), (0, 0)])
            
        def update_popup_bg(inst, value):
            self.popup_rect.pos = inst.pos
            self.popup_rect.size = inst.size
        view.bind(pos=update_popup_bg, size=update_popup_bg)
        
        box = FloatLayout()
        
        # Заголовок сообщения
        lbl_title = Label(text=title_text, font_name=resource_path("ClearSans-Bold.ttf"),
                          font_size='24sp', color=title_color, bold=True,
                          size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'top': 0.9})
        
        # Текст сообщения
        lbl_msg = Label(text=msg_text, font_name=resource_path("ClearSans-Bold.ttf"),
                        font_size='15sp', color=color_text, bold=True,
                        size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        tip_text = "Кликните в любое место для выхода в меню" if is_end_game else "Кликните в любое место, чтобы скрыть"
        lbl_tip = Label(text=tip_text, font_name=resource_path("ClearSans-Bold.ttf"),
                        font_size='11sp', color=color_not_in_word, bold=True,
                        size_hint=(None, None), size=(300, 30), pos_hint={'center_x': 0.5, 'y': 0.08})
        
        box.add_widget(lbl_title)
        box.add_widget(lbl_msg)
        box.add_widget(lbl_tip)
        view.add_widget(box)
        
        # Перехватываем клик по экрану напрямую через ModalView
        def self_dismiss(instance, touch):
            instance.dismiss()
            return True
            
        view.bind(on_touch_down=self_dismiss)
        
        if is_end_game:
            view.bind(on_dismiss=lambda x: self.press_exit_key(None))
            
        view.open()

class HowToPlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(create_stub_layout(self, "Правила игры"))

class AchievementsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(create_stub_layout(self, "Достижения"))

class CustomizationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(create_stub_layout(self, "Кастомизация"))

class QuestsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(create_stub_layout(self, "Квесты"))

def create_stub_layout(screen_instance, text):
    layout = FloatLayout()
    
    btn_back = MenuButton(
        text="Назад", 
        size_hint=(None, None), 
        size=(100, 54)
    )
    btn_back.pos = (Window.width - 100 - 15, Window.height - 54 - 44)
    btn_back.font_size = '20sp' 
    btn_back.bind(on_release=lambda x: setattr(screen_instance.manager, 'current', 'menu'))
    layout.add_widget(btn_back)
    
    layout.add_widget(Label(
        text=text, 
        font_name=resource_path("ClearSans-Bold.ttf"), 
        font_size='32sp', 
        bold=True, 
        color=color_text,
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    ))
    
    return layout

class MobileApp(App):
    def build(self):
        self.words_list = MOBILE_ALL_WORDS
        saved_theme = MOBILE_PLAYER_STATS.get("active_theme_name", "classic")
        theme_translator = {"классика": "classic", "ночь": "night", "океан": "ocean", "закат": "sunset", "сакура": "sakura", "лес": "forest", "король": "royal", "лава": "lava", "изумруд": "emerald", "конфета": "candy", "неон": "neon", "золото": "gold"}
        
        if isinstance(saved_theme, str):
            saved_theme = theme_translator.get(saved_theme.lower(), saved_theme.lower())

        choose_theme(saved_theme)
        Window.clearcolor = color_bg
        
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(HowToPlayScreen(name='how_to_play'))
        sm.add_widget(AchievementsScreen(name='achievements'))
        sm.add_widget(CustomizationScreen(name='customization'))
        sm.add_widget(QuestsScreen(name='quests'))
        sm.add_widget(OnePlayerGameScreen(name='one_player_game'))
        sm.add_widget(TwoPlayerGameScreen(name='two_player_game'))
        return sm

def start_mobile_game(words_list, player_stats, save_function):
    global MOBILE_ALL_WORDS, MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC
    MOBILE_ALL_WORDS = words_list
    MOBILE_PLAYER_STATS = player_stats
    MOBILE_SAVE_FUNC = save_function
    
    Window.size = (360, 640) # (360, 640)
    MobileApp().run()
