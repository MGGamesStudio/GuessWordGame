import os
import sys

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

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

CURRENT_WORD = ""
CURRENT_ATTEMPT = 0
CORRECT_WORD = ""
GAME_STATE = "playing"
GUESSES = ["", "", "", "", "", ""]
KEYBOARD_STATUS = {}

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ""
        self.font_name = resource_path("ClearSans-Bold.ttf")
        self.font_size = '42sp' # Крупный шрифт под оригинальный бланк
        self.bold = True
        
        # СТРОГО ОРИГИНАЛЬНЫЙ РАЗМЕР ПК-ВЕРСИИ
        self.size_hint = (None, None)
        self.size = (80, 100) 
        
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
            # Оригинальный радиус скругления 6 пикселей из file_1_1
            RoundedRectangle(pos=self.pos, size=self.size, radius=[6])

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
            # Оригинальное скругление углов на 6 пикселей
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
        
        # Кнопка "Выйти"
        btn_back = MenuButton(text="Выйти", size_hint=(None, None), size=(100, 54))
        btn_back.pos = (Window.width - 100 - 15, Window.height - 54 - 44)
        btn_back.font_size = '20sp'
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'game'))
        self.layout.add_widget(btn_back)
        
        # МАТЕМАТИЧЕСКИЙ ПЕРЕНОС ТВОЕГО ЦИКЛА ИЗ PYGAME В KIVY
        self.cells = []
        
        # Высчитываем стартовую точку X для идеального центра в окне 360
        # Ширина всей пачки: 5 * 80 + 4 * 5 = 420px. 
        # Центр: (360 - 420) // 2 = -30px (сетка выйдет за края ровно на 30px с каждой стороны)
        blank_x = (Window.width - 420) // 2 
        
        # Стартовая точка Y (в Kivy считаем снизу вверх, ставим на высоту 150px, чтобы снизу был воздух)
        blank_y = 150 
        
        # Твой оригинальный двойной цикл 6х5 из репозитория GitHub
        for a1 in range(6):
            for a2 in range(5):
                cell = GameCell()
                cell.pos = (blank_x, blank_y) # Ручное пиксельное позиционирование
                
                self.cells.append(cell)
                self.layout.add_widget(cell)
                
                blank_x += 80 + 5 # Твой оригинальный шаг по горизонтали
            
            blank_x = (Window.width - 420) // 2 # Сброс X на начало строки
            blank_y += 100 + 5 # Твой оригинальный шаг по вертикали
            
        self.add_widget(self.layout)

class TwoPlayerGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(create_stub_layout(self, "Режим: 2 Игрока"))

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
    
    Window.size = (360, 640)
    MobileApp().run()
