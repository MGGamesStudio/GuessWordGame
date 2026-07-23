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
from kivy.uix.scrollview import ScrollView

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

def redraw_all_screens():
    from kivy.uix.screenmanager import NoTransition
    from kivy.graphics import Color
    from kivy.core.window import Window
    
    app = App.get_running_app()
    if not app or not app.root: 
        return
        
    sm = app.root  # Твой ScreenManager
    
    # 1. Меняем цвет самого окна Kivy (на случай, если фон завязан на clearcolor)
    Window.clearcolor = color_bg

    # 2. Безопасно обновляем ВСЕ инструкции цвета на холсте менеджера экранов БЕЗ .clear()
    if hasattr(sm, 'canvas'):
        # Проверяем .before холст
        if sm.canvas.before:
            for instr in sm.canvas.before.children:
                if instr.__class__.__name__ == 'Color':
                    instr.rgba = color_bg
        # Проверяем основной холст
        if sm.canvas.children:
            for instr in sm.canvas.children:
                if instr.__class__.__name__ == 'Color':
                    # Перекрашиваем только фоновые цвета (обычно они идут первыми)
                    instr.rgba = color_bg

    # 3. Отключаем анимацию переходов на время перезагрузки
    old_transition = sm.transition
    sm.transition = NoTransition()
    
    # 4. Временно уходим на меню
    sm.current = 'menu'
    
    # 5. Собираем список всех экранов
    screens_to_recreate = [screen.name for screen in list(sm.screens)]
    
    # 6. Вычищаем все старые экраны из памяти
    for screen_name in screens_to_recreate:
        old_scr = sm.get_screen(screen_name)
        sm.remove_widget(old_scr)
    
    # 7. Пересоздаем все экраны с нуля с новыми глобальными цветами кнопок и текстов
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(GameScreen(name='game'))
    sm.add_widget(HowToPlayScreen(name='how_to_play'))
    sm.add_widget(AchievementsScreen(name='achievements'))
    sm.add_widget(CustomizationScreen(name='customization'))
    sm.add_widget(QuestsScreen(name='quests'))
    sm.add_widget(OnePlayerGameScreen(name='one_player_game'))
    sm.add_widget(TwoPlayerGameScreen(name='two_player_game'))
    
    # 8. Возвращаем игрока обратно в кастомизацию
    sm.current = 'customization'
    
    # 9. Восстанавливаем анимацию
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
    
    for btn in [screen_instance.btn_erase, screen_instance.btn_exit, screen_instance.btn_enter]:
        btn.font_size = f"{key_font_size_px}px"
        btn.text_size = btn.size
        btn.halign = 'center'
        btn.valign = 'middle'
        btn.shorten = False
        btn.padding = [0, 0, 0, sys_pad_bottom]

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
            
            RoundedRectangle(pos=self.pos, size=self.size, radius=[6])

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Ellipse
from kivy.graphics import Line
from kivy.effects.scroll import ScrollEffect

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

        # Списки цветов теперь создаются тоже ДО super(), чтобы они всегда были доступны
        self.block_colors = [self.c_blank, self.c_correct, self.c_in_word, self.c_not_in_word, self.c_blank]
        self.text_colors  = [self.c_text, (1, 1, 1, 1), (0, 0, 0, 1), (1, 1, 1, 1), self.c_text]

        # 2. И ТОЛЬКО ПОСЛЕ ЭТОГО ИНИЦИАЛИЗИРУЕМ ВИДЖЕТ
        super().__init__(**kwargs)
        self.size_hint = (None, None)

        # Отрисовка фона конкретной темы и кружка строго друг за другом
        with self.canvas.before:
            Color(*self.c_bg) # ЗАМЕНИЛИ color_bg НА self.c_bg, ЧТОБЫ ЦВЕТА ВЕРНУЛИСЬ
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
            
            self.active_circle_color = Color(*self.c_correct)
            self.active_circle = Ellipse(pos=(0, 0), size=(0, 0))
            
        # Название темы снизу (цветом текста конкретной темы!)
        self.lbl_name = Label(
            text=theme_name,
            font_name=resource_path("ClearSans-Bold.ttf"),
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
        
        # Создаем 5 плиток "А"
        for i in range(5):
            lbl_a = Label(
                text="A",
                font_name=resource_path("ClearSans-Bold.ttf"),
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

        # Отрисовка мини-клавиатуры цветом клавиш текущей темы (c_key)
        self.kb_rects = []
        self.kb_colors = []
        with self.canvas:
            for _ in range(20):
                c_inst = Color(*self.c_key)
                rect = RoundedRectangle(pos=(0,0), size=(0,0), radius=[3])
                self.kb_colors.append(c_inst)
                self.kb_rects.append(rect)
            
        self.bind(pos=self.update_graphics, size=self.update_graphics)

        # Флаг: выбрана ли эта карточка игроком прямо сейчас
        self.is_selected = False
        
        # Инструкция для жёлтой рамки выбора (рисуем в after, чтобы она была поверх всего)
        with self.canvas.after:
            self.select_line_color = Color(*color_in_word) # Твой жёлтый цвет
            self.select_line = Line(width=2)

    def update_graphics(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
        self.lbl_name.size = (self.width, 35)
        self.lbl_name.pos = (self.x, self.y + 5)
        
        # Расчет сетки 1х5
        tile_size = self.height * 0.33  
        spacing = 8                     
        total_grid_w = (tile_size * 5) + (spacing * 4)
        start_x = self.x + (self.width - total_grid_w) / 2
        tile_y = self.y + self.height - tile_size - 10
        
        for i, lbl_a in enumerate(self.tiles):
            current_x = start_x + i * (tile_size + spacing)
            lbl_a.size = (tile_size, tile_size)
            lbl_a.pos = (current_x, tile_y)
            lbl_a.text_size = (tile_size, tile_size)
            
            self.tile_colors[i].rgba = self.block_colors[i]
            self.tile_rects[i].pos = (current_x, tile_y)
            self.tile_rects[i].size = (tile_size, tile_size)

        # Расчет мини-клавиатуры
        kb_size = tile_size * 0.38  
        kb_spacing_x = 4  
        kb_spacing_y = 4  
        total_kb_w = (kb_size * 10) + (kb_spacing_x * 9)
        start_kb_x = self.x + (self.width - total_kb_w) / 2
        start_kb_y = tile_y - (kb_size * 2 + kb_spacing_y) - 8
        
        for index in range(20):
            row = index // 10  
            col = index % 10   
            kx = start_kb_x + col * (kb_size + kb_spacing_x)
            ky = start_kb_y + (1 - row) * (kb_size + kb_spacing_y)
            
            self.kb_colors[index].rgba = self.c_key
            self.kb_rects[index].pos = (kx, ky)
            self.kb_rects[index].size = (kb_size, kb_size)

        # --- ИСПРАВЛЕННЫЙ РАСЧЕТ ИНДИКАТОРА АКТИВНОЙ ТЕМЫ ---
        if self.is_active:
            circle_size = 16
            cx = self.x + self.width - circle_size - 15
            cy = self.y + self.height - circle_size - 15
            
            # Принудительно обновляем цвет и координаты видимого шарика
            self.active_circle_color.rgba = self.c_correct
            self.active_circle.pos = (cx, cy)
            self.active_circle.size = (circle_size, circle_size)
        else:
            # ВАЖНО: Полностью сбрасываем размеры и делаем его невидимым налету!
            self.active_circle.size = (0, 0)
            self.active_circle_color.rgba = (0, 0, 0, 0)

        # --- РАСЧЕТ РАМКИ ВЫБОРА ТЕМЫ ---
        if self.is_selected:
            # Если тема выбрана, рисуем рамку строго по контуру карточки со скруглением 12px
            self.select_line_color.rgba = color_in_word
            self.select_line.rounded_rectangle = (self.x, self.y, self.width, self.height, 12, 12, 12, 12)
        else:
            # Если тема не выбрана, убираем рамку (задаем нулевые координаты)
            self.select_line.rounded_rectangle = (0, 0, 0, 0, 0)

    def on_touch_down(self, touch):
        # Если клик произошел внутри границ этой карточки темы
        if self.collide_point(*touch.pos):
            # Проверяем, что это не скролл мышкой или перетаскивание
            if not touch.is_mouse_scrolling:
                # Если функция привязана — вызываем её строго один раз!
                if self.on_click_callback:
                    self.on_click_callback(self.theme_id)
                return True
        return super().on_touch_down(touch)

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
        
        mode_container = BoxLayout(
            orientation='vertical', 
            spacing=55, 
            size_hint=(None, None), 
            size=(350, 440),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
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

        with self.canvas.before:
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))

        self.cells = []
        for _ in range(30):
            cell = GameCell(size=(74, 92))
            cell.base_color = color_blank
            self.cells.append(cell)
            self.layout.add_widget(cell)

        self.keyboard_keys = []

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

        # ----- ИГРА ----
        self.current_word = ""
        self.current_attempt = 0
        self.secret_word = ""

        self.reset_game()

    def reposition_elements(self, instance, size):
        win_w = Window.width
        win_h = Window.height
        self.bg_rect.size = (win_w, win_h)

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

        start_blank_x = side_margin
        start_blank_y = win_h - CELL_HEIGHT - 5
        
        cell_idx = 0
        for row in range(6):
            for col in range(5):
                if cell_idx < len(self.cells):
                    self.cells[cell_idx].pos = (start_blank_x + col * (CELL_WIDTH + CELL_SPACING_X), start_blank_y - row * (CELL_HEIGHT + CELL_SPACING_Y))
                    self.cells[cell_idx].update_canvas()
                    cell_idx += 1

        bottom_blanks_line = (win_h - 5) - total_blanks_height

        KEY_SPACING_X = 4
        avail_w = win_w - 16 - 44
        KEY_WIDTH = avail_w / 12

        KEY_SPACING_Y = 4

        avail_h = bottom_blanks_line - 16 - 12
        KEY_HEIGHT = avail_h / 4

        for key in self.keyboard_keys:
            key.size = (KEY_WIDTH, KEY_HEIGHT)

        row_heights = [
            8,
            8 + (KEY_HEIGHT + KEY_SPACING_Y),
            8 + 2 * (KEY_HEIGHT + KEY_SPACING_Y),
            8 + 3 * (KEY_HEIGHT + KEY_SPACING_Y)
        ]

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
        
        self.btn_erase.pos = (start_sys_x, row_heights[3])
        self.btn_erase.size = (SYS_WIDTH, KEY_HEIGHT)
        self.btn_erase.update_canvas()
        
        self.btn_exit.pos = (start_sys_x + SYS_WIDTH + SYS_SPACING, row_heights[3])
        self.btn_exit.size = (SYS_WIDTH, KEY_HEIGHT)
        self.btn_exit.update_canvas()
        
        self.btn_enter.pos = (start_sys_x + 2 * (SYS_WIDTH + SYS_SPACING), row_heights[3])
        self.btn_enter.size = (SYS_WIDTH, KEY_HEIGHT)
        self.btn_enter.update_canvas()

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

                self.show_game_popup("Такого слова нет в словаре", "или введенное слово состоит не из 5 букв.", color_text, is_end_game=False)
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
                    
                    if status == "correct": btn.base_color = color_correct
                    elif status == "in_word": btn.base_color = color_in_word
                    elif status == "not_in_word": btn.base_color = color_not_in_word
                    btn.cell_status = status
                    btn.update_canvas()

        coins = sum(5 if s == "correct" else (2 if s == "in_word" else 1) for s in row_statuses)

        if check_word == self.secret_word: coins += 10
        MOBILE_PLAYER_STATS["player_coins"] = MOBILE_PLAYER_STATS.get("player_coins", 0) + coins
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
        """Продвижение прогресса ежедневного квеста и начисление награды"""
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
        self.manager.current = 'game'

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

        lbl_title = Label(text=title_text, font_name=resource_path("ClearSans-Bold.ttf"),
                          font_size=f"{title_font_size}px", color=title_color, bold=True,
                          size_hint=(1, None), height=popup_height * 0.25, 
                          pos_hint={'center_x': 0.5, 'top': 0.9})

        lbl_msg = Label(text=msg_text, font_name=resource_path("ClearSans-Bold.ttf"),
                        font_size=f"{msg_font_size}px", color=color_text, bold=True,
                        size_hint=(1, None), height=popup_height * 0.25, 
                        pos_hint={'center_x': 0.5, 'center_y': 0.45})

        tip_text = "Кликните в любое место для выхода в меню" if is_end_game else "Кликните в любое место, чтобы скрыть"
        lbl_tip = Label(text=tip_text, font_name=resource_path("ClearSans-Bold.ttf"),
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

        self.lbl_title = Label(text="ЗАГАДАЙТЕ СЛОВО", font_name=resource_path("ClearSans-Bold.ttf"),
                               font_size='32sp', color=color_text, bold=True, size_hint=(None, None))
        self.lbl_subtitle = Label(text="Второй игрок должен отвернуться от экрана!", font_name=resource_path("ClearSans-Bold.ttf"),
                                  font_size='14sp', color=color_not_in_word, bold=True, size_hint=(None, None))
        self.lbl_error = Label(text="", font_name=resource_path("ClearSans-Bold.ttf"),
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

        start_blank_x = side_margin
        
        if self.stage == "setup":
            kbd_top_y = row_heights[3] + KEY_HEIGHT

            total_free_space_y = win_h - kbd_top_y
            start_blank_y = kbd_top_y + (total_free_space_y - CELL_HEIGHT) // 2

            space_above_cells = win_h - (start_blank_y + CELL_HEIGHT)
            center_above_y = (start_blank_y + CELL_HEIGHT) + (space_above_cells // 2)

            self.lbl_title.pos = (win_w // 2 - self.lbl_title.width // 2, center_above_y + 15)
            self.lbl_subtitle.pos = (win_w // 2 - self.lbl_subtitle.width // 2, center_above_y - 15)

            space_below_cells = start_blank_y - kbd_top_y
            center_below_y = kbd_top_y + (space_below_cells // 2)

            self.lbl_error.pos = (win_w // 2 - self.lbl_error.width // 2, center_below_y - self.lbl_error.height // 2)
        else:
            start_blank_y = win_h - CELL_HEIGHT - 5

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

        self.btn_erase.pos = (start_sys_x, row_heights[3])
        self.btn_erase.update_canvas()
        
        self.btn_exit.pos = (start_sys_x + SYS_WIDTH + SYS_SPACING, row_heights[3])
        self.btn_exit.update_canvas()
        
        self.btn_enter.pos = (start_sys_x + 2 * (SYS_WIDTH + SYS_SPACING), row_heights[3])
        self.btn_enter.update_canvas()

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
        if len(self.current_word) == 5:
            check_word = self.current_word.upper()

            if 'MOBILE_ALL_WORDS' in globals() and MOBILE_ALL_WORDS and check_word in MOBILE_ALL_WORDS:

                if self.stage == "setup":
                    self.secret_word = check_word
                    self.stage = "playing"
                    self.current_word = ""

                    self.lbl_title.text = ""
                    self.lbl_subtitle.text = ""
                    
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
                            if status_for_char == "correct": key_btn.base_color = color_correct
                            elif status_for_char == "in_word": key_btn.base_color = color_in_word
                            elif status_for_char == "not_in_word": key_btn.base_color = color_not_in_word
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
                    self.lbl_error.text = "Такого слова нет в словаре!"
                    self.reposition_elements(None, None)
                else:
                    self.show_game_popup("Такого слова нет в словаре", "или введенное слово состоит не из 5 букв.", color_text, is_end_game=False)

    def press_exit_key(self, instance):
        self.reset_game()
        self.manager.current = 'game'

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

        for btn in [self.btn_erase, self.btn_enter, self.btn_exit]:
            btn.base_color = color_key
            btn.color = color_text
            btn.update_canvas()

        self.reposition_elements(None, None)

    def show_game_popup(self, title_text, msg_text, title_color, is_end_game=False):
        win_w = Window.width
        win_h = Window.height

        safe_screen_side = min(win_w, win_h)

        popup_height = win_h * 0.30
        
        view = ModalView(size_hint=(0.8, None), height=popup_height, auto_dismiss=True, background='')
        
        with view.canvas.before:
            Color(*color_bg)
            self.popup_rect = RoundedRectangle(pos=view.pos, size=view.size, radius=[(0, 0), (0, 0), (0, 0), (0, 0)])
            
        def update_popup_bg(inst, value):
            self.popup_rect.pos = inst.pos
            self.popup_rect.size = inst.size
        view.bind(pos=update_popup_bg, size=update_popup_bg)

        box = FloatLayout()

        title_font_size = safe_screen_side * 0.06
        msg_font_size = safe_screen_side * 0.04
        tip_font_size = safe_screen_side * 0.03

        lbl_title = Label(text=title_text, font_name=resource_path("ClearSans-Bold.ttf"),
                          font_size=f"{title_font_size}px", color=title_color, bold=True,
                          size_hint=(1, None), height=popup_height * 0.25, 
                          pos_hint={'center_x': 0.5, 'top': 0.9})

        lbl_msg = Label(text=msg_text, font_name=resource_path("ClearSans-Bold.ttf"),
                        font_size=f"{msg_font_size}px", color=color_text, bold=True,
                        size_hint=(1, None), height=popup_height * 0.25, 
                        pos_hint={'center_x': 0.5, 'center_y': 0.45})
        
        tip_text = "Кликните в любое место для выхода в меню" if is_end_game else "Кликните в любое место, чтобы скрыть"
        lbl_tip = Label(text=tip_text, font_name=resource_path("ClearSans-Bold.ttf"),
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

class HowToPlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        # Кнопка НАЗАД в верхнем правом руку
        self.btn_back = MenuButton(text="Назад", size_hint=(None, None), size=(100, 54))
        self.btn_back.font_size = '20sp'
        self.btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(self.btn_back)
        
        # Твой идеальный заголовок экрана
        self.title_label = Label(
            text="Как играть",
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='28sp',
            bold=True,
            color=color_text,
            size_hint=(None, None)
        )
        self.layout.add_widget(self.title_label)
        
        # Скролл-контейнер для мобильных устройств
        self.scroll_view = ScrollView(size_hint=(None, None), do_scroll_x=False, do_scroll_y=True)
        self.content_box = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None, padding=[20, 10, 20, 20])
        self.content_box.bind(minimum_height=self.content_box.setter('height'))
        
        # Списки для динамического перерасчета ширины текста в reposition_elements
        self.title_labels = []
        self.text_labels = []
        self.row_labels = []

        # --- Вспомогательные мини-функции для верстки контента ---
        def add_title(text):
            lbl = Label(text=text, font_name=resource_path("ClearSans-Bold.ttf"), font_size='18sp', 
                        bold=True, color=color_in_word, size_hint_y=None, halign='left', valign='middle')
            # Исправлено: берем высоту через val[1]
            lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
            self.title_labels.append(lbl)
            self.content_box.add_widget(lbl)
            
        def add_text(text, custom_color=None):
            lbl = Label(text=text, font_name=resource_path("ClearSans-Bold.ttf"), font_size='14sp', 
                        color=custom_color if custom_color else color_text, size_hint_y=None, halign='left', valign='top')
            # Исправлено: берем высоту через val[1]
            lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
            self.text_labels.append(lbl)
            self.content_box.add_widget(lbl)
            
        def add_row(letter, status, description, text_col=None):
            row = BoxLayout(orientation='horizontal', spacing=14, size_hint_y=None, height=54)
            
            # Ячейка с буквой, приподнятой на 5 пикселей вверх
            cell = GameCell(size=(54, 54))
            cell.text = letter
            cell.change_type(status)
            cell.text_size = cell.size
            cell.halign = 'center'
            cell.valign = 'middle'
            cell.padding = [0, 0, 0, 5]
            
            desc = Label(text=description, font_name=resource_path("ClearSans-Bold.ttf"), font_size='14sp', 
                        color=text_col if text_col else color_text, size_hint_y=None, halign='left', valign='top')
            
            # КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: берем строго высоту val[1] из кортежа texture_size
            desc.bind(texture_size=lambda inst, val: [
                setattr(inst, 'height', val[1]), 
                setattr(row, 'height', max(54, val[1]))
            ])
            
            row.add_widget(cell)
            row.add_widget(desc)
            self.row_labels.append(desc)
            self.content_box.add_widget(row)

        # --- ЗАПОЛНЕНИЕ ПОЛНЫМ ТЕКСТОМ ИЗ ПК-ВЕРСИИ ---
        add_title("О ЧЕМ ЭТА ИГРА?")
        add_text("Игра является цифровой головоломкой на логику и эрудицию.")
        add_text("Ваша главная цель - за 6 попыток вычислить секретное слово.")
        add_text("Загаданное слово всегда состоит строго из 5 букв.")
        add_text("Вводите ваши варианты слов и следите за изменением цветов ячеек!")
        add_text("Если вы потратите все 6 попыток и не угадаете - раунд завершится.", color_not_in_word)
        
        add_title("РАСШИФРОВКА ЦВЕТОВ ЯЧЕЕК:")
        add_row("А", "blank", "- Цвет пустой клетки. Буква введена, но еще не подтверждена клавишей ВВОД.")
        add_row("А", "not_in_word", "- Такой буквы нет в загаданном слове.\n  На клавиатуре клавиша станет серой.")
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
        
        # Подписка на обновление размеров экрана
        self.bind(size=self.reposition_elements)

    def reposition_elements(self, instance, size):
        win_w, win_h = Window.width, Window.height
        
        # Расчет верхней линии кнопок
        btn_y = win_h - 54 - 44
        self.btn_back.pos = (win_w - 100 - 15, btn_y)
        
        # Твой проверенный заголовок
        self.title_label.texture_update()
        self.title_label.size = self.title_label.texture_size
        self.title_label.x = 15
        self.title_label.y = btn_y + 15
        
        # Настройка скролл-зоны
        self.scroll_view.size = (win_w, btn_y - 20)
        self.scroll_view.pos = (0, 0)
        
        # ЖЕСТКОЕ ОТКЛЮЧЕНИЕ НАТЯГИВАНИЯ И ПОЛОСЫ ПРОКРУТКИ
        self.scroll_view.effect_cls = ScrollEffect
        if self.scroll_view.effect_cls:
            self.scroll_view.effect_cls.bounces = False  # Отключает резиновое натягивание списка
        self.scroll_view.bar_width = 0                   # Полностью убирает боковую полосу прокрутки
        
        # Перевод размеров в int для Kivy
        text_width = int(win_w - 40)
        row_text_width = int(win_w - 40 - 54 - 14)
        
        # Передаем тексту его честную ширину, чтобы Kivy переносил строки, а не обрубал их
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
            font_name=resource_path("ClearSans-Bold.ttf"), 
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

        self.ach_list_layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[0])
        self.ach_list_layout.bind(minimum_height=self.ach_list_layout.setter('height'))

        self.scroll_view.add_widget(self.ach_list_layout)

        self.layout.add_widget(self.scroll_view)

        if hasattr(self, 'top_overlay'):
            self.layout.remove_widget(self.scroll_view)
            self.layout.add_widget(self.scroll_view, index=len(self.layout.children))

    def on_enter(self):
        self.refresh_stats_and_achievements()

    def reposition_elements(self, instance, size):
        win_w = Window.width
        win_h = Window.height
        overlay_height = 280

        self.top_overlay.height = overlay_height
        self.top_overlay.pos = (0, win_h - overlay_height)

        self.overlay_rect.size = (win_w, overlay_height)
        self.overlay_rect.pos = (0, win_h - overlay_height)

        self.lbl_main_title.font_size = f"{min(win_w, win_h) * 0.08}px"
        self.lbl_main_title.size = (win_w - 150, 54)
        self.lbl_main_title.text_size = self.lbl_main_title.size
        self.lbl_main_title.center_y = win_h - 54
        self.lbl_main_title.x = 15

        self.stats_scroll.height = 152

        self.stats_scroll.pos = (0, win_h - 54 - 44 - 152 - 15)
        self.stats_container.height = 152

        self.scroll_view.size = (win_w, win_h - 280 - 15)
        self.scroll_view.pos = (0, 10)

        self.ach_list_layout.width = win_w

    def create_card(self, label_text, val_text, val_color):
        """Создает карточку статистики с огромными хитбоксами против любых переносов"""
        card = FloatLayout(size_hint=(None, None), size=(385, 72))
        
        # Подложка плашки (светло-серая со скруглением 12)
        with card.canvas.before:
            Color(*color_blank)
            r_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
        card.bind(pos=lambda inst, v: setattr(r_rect, 'pos', inst.pos), 
                  size=lambda inst, v: setattr(r_rect, 'size', inst.size))
        
        # 1. ТЕКСТ ЯРЛЫКА (Слева, вернули оригинальный 20sp и дали огромный хитбокс 345px)
        lbl_lbl = Label(
            text=label_text, 
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='20sp', 
            color=color_not_in_word, 
            size_hint=(None, None),
            size=(345, 72),
            text_size=(345, 72),  # ИСПРАВЛЕНО: Дали огромный хитбокс, чтобы ничего не переносилось
            pos_hint={'x': 0.06, 'center_y': 0.5}, 
            halign='left', 
            valign='middle'
        )
        card.add_widget(lbl_lbl)
        
        # Оптический зум шрифта для больших чисел из твоей ПК-версии file_3
        val_len = len(val_text)
        if val_len >= 9:
            v_font = '14sp'
        elif val_len >= 6:
            v_font = '20sp'
        else:
            v_font = '30sp'
        
        # 2. ЧИСЛОВОЕ ЗНАЧЕНИЕ (Справа, дали такой же огромный хитбокс 345px)
        lbl_val = Label(
            text=val_text, 
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size=v_font, 
            color=val_color, 
            bold=True, 
            size_hint=(None, None),
            size=(345, 72),
            text_size=(345, 72),  # ИСПРАВЛЕНО: Дали огромный хитбокс, цифры никогда не улетят вниз
            pos_hint={'right': 0.94, 'center_y': 0.5}, 
            halign='right', 
            valign='middle'
        )
        card.add_widget(lbl_val)
        
        return card
    
    def create_achievement_row(self, name, description, ach_data, got, date_str):
        """Часть 1: Попиксельное смешивание цветов и точное чтение ключа 'type' из словаря лаунчера"""
        row = FloatLayout(size_hint_y=None, height=110)
        
        # ЖЕСТКОЕ ИСПРАВЛЕНИЕ: Честный попиксельный расчет каналов (R, G, B) для Kivy-кортежей
        def lerp_color(c1, c2, factor):
            return (
                c1[0] + (c2[0] - c1[0]) * factor,
                c1[1] + (c2[1] - c1[1]) * factor,
                c1[2] + (c2[2] - c1[2]) * factor,
                1.0
            )

        # ТОЧНОЕ СЧИТЫВАНИЕ: Берем ключ 'type' прямо из твоего словаря achivements!
        r_type = "common"
        if isinstance(ach_data, dict):
            r_type = ach_data.get("type", "common").lower().strip()

        # Выставляем правильный текст и базовый цвет редкости
        if r_type == "rare":
            rare_color = lerp_color(color_text, color_in_word, 0.5)
            type_text = "Редкое"
        elif r_type == "epic":
            rare_color = lerp_color(color_text, color_correct, 0.6)
            type_text = "Эпическое"
        else:
            rare_color = lerp_color(color_text, color_bg, 0.3)
            type_text = "Обычное"

        # Настраиваем фон карточки в зависимости от того, разблокирована ачивка или нет
        if got:
            bg_color = color_blank
            text_color = color_text
            status_color = color_correct
        else:
            bg_color = lerp_color(color_blank, color_bg, 0.5)
            text_color = lerp_color(color_text, color_bg, 0.4)
            rare_color = lerp_color(rare_color, color_bg, 0.3)
            status_color = color_not_in_word

        # Рисуем подложку
        with row.canvas.before:
            Color(*bg_color)
            bg_rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[12])
            
            Color(*rare_color)
            # Внутренние правые углы полоски — абсолютно острые (0), скруглены только левые внешние!
            ribbon_rect = RoundedRectangle(pos=row.pos, size=(10, 110), radius=[(12, 12), (0, 0), (0, 0), (12, 12)])
            
        def sync_graphics(instance, value):
            bg_rect.pos = (instance.x + 15, instance.y)
            bg_rect.size = (instance.width - 30, instance.height)
            ribbon_rect.pos = (instance.x + 15, instance.y)
            ribbon_rect.size = (10, instance.height)
        row.bind(pos=sync_graphics, size=sync_graphics)

        return self.fill_achievement_widgets(row, name, description, got, date_str, type_text, rare_color, text_color, status_color, bg_rect, ribbon_rect)

    def fill_achievement_widgets(self, row, name, description, got, date_str, type_text, rarity_color, text_color, status_color, bg_rect, ribbon_rect):
        """Часть 2: Полностью динамическая высота плашки достижения на основе texture_size"""
        
        # Сбалансированная ширина для текста (6% отступы слева и справа)
        text_w = Window.width - 45
        font_path = resource_path("ClearSans-Bold.ttf")

        # 1. НАЗВАНИЕ ДОСТИЖЕНИЯ (Высота управляется текстом, разрешен перенос на любое число строк!)
        name_lbl = Label(
            text=name.upper(), font_name=font_path,
            font_size='18sp', color=text_color, bold=True,
            size_hint=(None, None), width=text_w, text_size=(text_w, None),
            halign='left', valign='top'
        )
        # Привязываем автоматический расчет высоты заголовка по тексту
        name_lbl.bind(texture_size=lambda inst, sz: setattr(inst, 'height', sz[1]))

        # 2. ОПИСАНИЕ ДОСТИЖЕНИЯ (Высота управляется текстом, растет строго вниз)
        desc_lbl = Label(
            text=description, font_name=font_path,
            font_size='13sp', color=text_color,
            size_hint=(None, None), width=text_w, text_size=(text_w, None),
            halign='left', valign='top'
        )
        # Привязываем автоматический расчет высоты описания по тексту
        desc_lbl.bind(texture_size=lambda inst, sz: setattr(inst, 'height', sz[1]))

        # 3. НИЖНЯЯ ИНФО-СТРОКА (Высота 35px, статус прижат к right: 0.94 для идеальной симметрии!)
        info_line = FloatLayout(size_hint=(1, None), height=35)
        
        lbl_rare = Label(
            text=type_text, font_name=font_path, font_size='13sp', color=rarity_color, bold=True, 
            size_hint=(None, None), size=(120, 35), text_size=(120, 35), 
            pos_hint={'x': 0.06, 'center_y': 0.5}, halign='left', valign='middle'
        )
        
        lbl_date = Label(
            text=f"Дата: {date_str}" if (got and date_str) else "", 
            font_name=font_path, font_size='12sp', color=color_not_in_word, bold=True, 
            size_hint=(None, None), size=(240, 35), text_size=(240, 35), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}, halign='center', valign='middle'
        )
        
        lbl_stat = Label(
            text="ПОЛУЧЕНО" if got else "НЕ ПОЛУЧЕНО", font_name=font_path, font_size='14sp', color=status_color, bold=True, 
            size_hint=(None, None), size=(200, 35), text_size=(200, 35), 
            pos_hint={'right': 0.94, 'center_y': 0.5}, halign='right', valign='middle'
        )
        
        info_line.add_widget(lbl_rare)
        info_line.add_widget(lbl_date)
        info_line.add_widget(lbl_stat)

        # Локальный FloatLayout для изоляции внутренних координат плашки
        text_group = FloatLayout(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        text_group.add_widget(name_lbl)
        text_group.add_widget(desc_lbl)
        text_group.add_widget(info_line)

        # ФУНКЦИЯ ДИНАМИЧЕСКОГО СБОРЩИКА ВЫСОТЫ ПЛАШКИ
        def sync_row_height(*args):
            # Жестко обновляем высоты из Kivy-текстур (sz[1] — чистая высота в пикселях)
            name_lbl.height = name_lbl.texture_size[1]
            desc_lbl.height = desc_lbl.texture_size[1]
            
            # Твоя идеальная плотная математика из квестов: 4px верх + Текст + 2px зазор + Текст + 8px зазор + Инфо + 4px низ
            total_h = 4 + name_lbl.height + 2 + desc_lbl.height + 8 + info_line.height + 4
            
            # Минимальный порог высоты 75px, чтобы пустые или короткие плашки оставались красивыми
            row.height = max(75, total_h)
            ribbon_rect.size = (10, row.height)
            
            # Выстраиваем элементы сверху вниз относительно динамического потолка row.height
            name_lbl.pos_hint = {'x': 0.06, 'top': 1.0 - (4 / row.height)}
            desc_lbl.pos_hint = {'x': 0.06, 'top': name_lbl.pos_hint['top'] - (name_lbl.height / row.height) - (2 / row.height)}
            
            # Инфо-строка лежит идеально зеркально на расстоянии 4 пикселя от пола карточки
            info_line.pos_hint = {'x': 0, 'y': 4 / row.height}

        # Привязываем триггеры пересчета к тексту
        desc_lbl.bind(texture_size=sync_row_height)
        name_lbl.bind(texture_size=sync_row_height)
        row.bind(size=sync_row_height)

        row.add_widget(text_group)
        return row
    
    def build_achievements_list(self, launcher_achievements):
        """Полный вывод достижений с автоматической сортировкой выполненных наверх"""
        self.ach_list_layout.clear_widgets()
        
        if not launcher_achievements:
            return

        # ВОССТАНОВЛЕНО: Полученные (got=True) всегда уходят на самый верх списка!
        all_keys = list(launcher_achievements.keys())
        sorted_keys = sorted(all_keys, key=lambda k: launcher_achievements[k].get("got", False), reverse=True)
        
        for ach_key in sorted_keys:
            ach_data = launcher_achievements[ach_key]
            
            name = ach_data.get("name", "Секретное достижение")
            description = ach_data.get("description", "")
            got = ach_data.get("got", False)
            date_str = ach_data.get("date", "")

            row_widget = self.create_achievement_row(name, description, ach_data, got, date_str)
            self.ach_list_layout.add_widget(row_widget)

    def refresh_stats_and_achievements(self):
        """Загружает данные лаунчера и строит карточки статистики строго в 2 ряда."""
        stats = MOBILE_PLAYER_STATS if ('MOBILE_PLAYER_STATS' in globals() and MOBILE_PLAYER_STATS) else {}
        launcher_ach = MOBILE_ACHIVEMENTS if ('MOBILE_ACHIVEMENTS' in globals() and MOBILE_ACHIVEMENTS) else {}
        
        coins = stats.get("player_coins", 0)
        wins = stats.get("total_wins", 0)
        losses = stats.get("total_losses", 0)
        streak = f"{stats.get('current_win_streak', 0)}/{stats.get('max_win_streak', 0)}"
        quests = stats.get("total_completed_quests", 0)
        
        got_count = sum(1 for ach in launcher_ach.values() if ach.get("got", False))
        ach_ratio = f"{got_count}/{len(launcher_ach)}" if launcher_ach else "0/16"

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

        self.stats_container.padding = [10, 0, 10, 0]

        total_scroll_width = 3 * 385 + 2 * 10 + 20
        
        self.stats_row1.size = (total_scroll_width - 20, 72)
        self.stats_row2.size = (total_scroll_width - 20, 72)
        self.stats_container.size = (total_scroll_width, 152)

        self.build_achievements_list(launcher_ach)

class CustomizationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        with self.canvas.before:
            # Основной фон всего экрана кастомизации
            Color(*color_bg)
            self.bg_rect = RoundedRectangle(pos=(0, 0), size=(360, 640))
            
            # ВАЖНО: Возвращаем большие фоновые плашки без скруглений для слияния
            Color(*color_bg)
            self.top_pad_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[0])
            self.bottom_pad_rect = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[0])
            
            # Переменные цвета и прямоугольники для 3 внутренних блоков (сверху)
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
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='32sp', 
            color=color_text, 
            bold=True, 
            size_hint=(None, None),
            halign='left',
            valign='middle'
        )

        # Тексты внутри блоков
        self.lbl_coins_title = Label(text="Монеты:", font_name=resource_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')
        self.lbl_theme_title = Label(text="Тема:", font_name=resource_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')
        self.lbl_status_title = Label(text="Статус:", font_name=resource_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')

        # Метка монет теперь горит цветом color_in_word
        self.lbl_coins_val = Label(
            text="0",  # Начальное значение (обновится в reposition_elements или при входе)
            font_name=resource_path("ClearSans-Bold.ttf"), 
            font_size='16sp', 
            color=color_in_word,  # Поменяли на твой цвет
            size_hint=(None, None), 
            halign='center', 
            valign='middle'
        )
        self.lbl_theme_val = Label(text="Классика", font_name=resource_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')
        self.lbl_status_val = Label(text="Применено", font_name=resource_path("ClearSans-Bold.ttf"), font_size='16sp', color=color_text, size_hint=(None, None), halign='center', valign='middle')

        for lbl in [self.lbl_coins_title, self.lbl_theme_title, self.lbl_status_title, self.lbl_coins_val, self.lbl_theme_val, self.lbl_status_val]:
            lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

        # Сначала создаем сам виджет левой кнопки
        self.btn_action = MenuButton(text="КУПИТЬ", size_hint=(None, None))
        self.btn_action.background_normal = 'atlas://data/images/defaulttheme/button_pressed'
        self.btn_action.background_color = (0, 0, 0, 0)
        self.btn_action.color = color_text
        self.btn_action.font_size = '18sp'
        self.btn_action.disabled_color = color_text 

        # Для нижних кнопок:
        with self.btn_action.canvas.before:
            self.btn_action_color = Color(*color_key) # Сохраняем ссылку
            self.rect_action = RoundedRectangle(pos=self.btn_action.pos, size=self.btn_action.size, radius=[12])

        # Аналогично для правой кнопки продажи
        self.btn_sell = MenuButton(text="ПРОДАТЬ за 900", size_hint=(None, None))
        self.btn_sell.background_normal = 'atlas://data/images/defaulttheme/button_pressed'
        self.btn_sell.background_color = (0, 0, 0, 0)
        self.btn_sell.color = color_text
        self.btn_sell.font_size = '18sp'
        self.btn_sell.disabled_color = color_not_in_word

        with self.btn_sell.canvas.before:
            self.btn_sell_color = Color(*color_key) # Сохраняем ссылку
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

        # Создаем окно прокрутки с жесткой остановкой без пружины
        self.scroll_view = ScrollView(
            size_hint=(None, None), 
            do_scroll_x=False, 
            do_scroll_y=True, 
            bar_width=0,
            effect_cls=ScrollEffect  # Переключаем на строгий эффект без баунса
        )
        
        # Контейнер для списка тем (одна под другой)
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
            
            # Передаем метод select_theme напрямую в карточку (card.bind больше НЕ используем!)
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
            
        # Активируем рамку выбора один раз при заходе
        self.select_theme(self.selected_theme_id)

    def reposition_elements(self, instance, size):
        # Объявляем чтение глобальной переменной со статистикой от лаунчера
        global MOBILE_PLAYER_STATS
        # Проверяем, существует ли переменная и есть ли в ней ключ player_coins
        if 'MOBILE_PLAYER_STATS' in globals() and isinstance(MOBILE_PLAYER_STATS, dict) and 'player_coins' in MOBILE_PLAYER_STATS:
            # Выводим НАСТОЯЩИЕ живые монеты из сохранения игры!
            self.lbl_coins_val.text = str(MOBILE_PLAYER_STATS['player_coins'])
        else:
            # Если по какой-то причине переменная недоступна, пишем 0
            self.lbl_coins_val.text = "0"
        win_w = Window.width
        win_h = Window.height
        
        self.bg_rect.size = (win_w, win_h)
        self.btn_back.pos = (win_w - 100 - 15, win_h - 54 - 44)
        self.lbl_title.size = (win_w - 140, 54)
        self.lbl_title.text_size = (win_w - 140, 54)
        self.lbl_title.pos = (15, win_h - 54 - 44 + 20)
        
        top_pad_h = win_h * 0.12
        top_pad_y = win_h - top_pad_h - 95
        self.top_pad_rect.size = (win_w, top_pad_h)
        self.top_pad_rect.pos = (0, top_pad_y)
        
        bottom_pad_h = win_h * 0.12
        self.bottom_pad_rect.size = (win_w, bottom_pad_h)
        self.bottom_pad_rect.pos = (0, 0)
        
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
        btn_y = 10 

        self.btn_action.size = (btn_w, btn_h)
        self.btn_action.pos = (10, btn_y)

        self.btn_sell.size = (btn_w, btn_h)
        self.btn_sell.pos = (10 + btn_w + 10, btn_y)

        self.rect_action.pos = self.btn_action.pos
        self.rect_action.size = self.btn_action.size

        self.rect_sell.pos = self.btn_sell.pos
        self.rect_sell.size = self.btn_sell.size

        # Вычисляем верхнюю границу (где заканчивается верхняя плашка статусов)
        scroll_top = top_pad_y - 15
        
        # Вычисляем нижнюю границу (где начинается нижняя плашка кнопок)
        scroll_bottom = bottom_pad_h + 15
        
        # Высота прокручиваемой области — это всё пространство между ними
        scroll_h = scroll_top - scroll_bottom
        
        # Настраиваем ScrollView строго под размеры экрана телефона
        self.scroll_view.size = (win_w, scroll_h)
        self.scroll_view.pos = (0, scroll_bottom)
        
        # Динамически задаем ширину и фиксированную высоту для КАЖДОЙ карточки внутри списка
        for card in self.scroll_content.children:
            card.size = (win_w - 30, 140)

    def select_theme(self, theme_id):
        global MOBILE_PLAYER_STATS
        self.selected_theme_id = theme_id
        
        # Переключаем рамки выбора карточек
        for t_id, card in self.theme_cards.items():
            card.is_selected = (t_id == theme_id)
            card.update_graphics(card, card.size)
            
        theme_data = color_themes[theme_id]
        self.lbl_theme_val.text = theme_data.get("color_name", theme_id.capitalize())
        
        # Получаем статус разблокировки из сохранений лаунчера
        unlocked_themes = MOBILE_PLAYER_STATS.get("unlocked_themes", {"classic": True})
        is_unlocked = unlocked_themes.get(theme_id, False)
        
        # Если это стартовые бесплатные темы игры — они ВСЕГДА разблокированы
        if theme_id in ['classic', 'night'] or theme_data.get("price", 0) == 0:
            is_unlocked = True
        
        # --- ОБНОВЛЕНИЕ СТАТУСА НА ВЕРХНЕЙ ПЛАШКЕ (С ЦВЕТАМИ) ---
        if is_unlocked:
            # Проверяем, горит ли зеленый кружок активности на этой карточке
            if self.theme_cards[theme_id].is_active:
                self.lbl_status_val.text = "Применено"
                self.lbl_status_val.color = color_correct  # Зеленый цвет
            else:
                self.lbl_status_val.text = "Куплено"
                self.lbl_status_val.color = color_text     # Жестко твой color_text (НЕ белый!)
        else:
            price = theme_data.get('price', 1000)
            self.lbl_status_val.text = f"{price} мон."
            self.lbl_status_val.color = color_in_word   # Желтый цвет

        # --- ОБНОВЛЕНИЕ ЛЕВОЙ КНОПКИ ---
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

        # --- ОБНОВЛЕНИЕ ПРАВОЙ КНОПКИ ---
        if theme_id in ['classic', 'night']:
            self.btn_sell.disabled = True
        else:
            self.btn_sell.disabled = not is_unlocked

    def process_theme_action(self, instance):
        global MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC
        # Импортируем глобальные цвета скрипта игры, чтобы перезаписать их налету
        global color_bg, color_text, color_correct, color_in_word, color_not_in_word, color_blank, color_key
        
        theme_id = self.selected_theme_id
        theme_data = color_themes[theme_id]
        
        unlocked_themes = MOBILE_PLAYER_STATS.get("unlocked_themes", {"classic": True})
        is_unlocked = unlocked_themes.get(theme_id, False)
        
        if theme_id in ['classic', 'night'] or theme_data.get("price", 0) == 0:
            is_unlocked = True
            
        if is_unlocked:
            # --- ПРИМЕНЕНИЕ ТЕМЫ ---
            if self.theme_cards[theme_id].is_active:
                return  
                
            # Гарантированно тушим ВСЕ зеленые шарики у ВСЕХ тем
            for t_id, card in self.theme_cards.items():
                card.is_active = False
                card.update_graphics(card, card.size)
                
            # Зажигаем шарик строго у выбранной темы
            self.theme_cards[theme_id].is_active = True
            self.theme_cards[theme_id].update_graphics(self.theme_cards[theme_id], self.theme_cards[theme_id].size)
            
            # 1. Вызываем твою системную смену темы
            choose_theme(theme_id)
            
            # 2. МГНОВЕННОЕ ОБНОВЛЕНИЕ ГЛОБАЛЬНЫХ ЦВЕТОВ ИГРЫ НАЛЕТУ
            color_bg = theme_data.get("color_bg", color_bg)
            color_text = theme_data.get("color_text", color_text)
            color_correct = theme_data.get("color_correct", color_correct)
            color_in_word = theme_data.get("color_in_word", color_in_word)
            color_not_in_word = theme_data.get("color_not_in_word", color_not_in_word)
            color_blank = theme_data.get("color_blank", color_blank)
            color_key = theme_data.get("color_key", color_key)
            
            # 3. Заставляем холст экрана кастомизации немедленно перекраситься в новые цвета
            self.reposition_elements(self, self.size)
            self.scroll_content.do_layout()
            
            if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
                MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)
            
            self.select_theme(theme_id)
            print(f"[MGGamesStudio] Тема {theme_id} успешно применена!")
            
        else:
            # --- ПОКУПКА ТЕМЫ ---
            price = theme_data.get('price', 1000)
            current_coins = MOBILE_PLAYER_STATS.get('player_coins', 0)
            
            if current_coins >= price:
                MOBILE_PLAYER_STATS['player_coins'] = current_coins - price
                MOBILE_PLAYER_STATS['unlocked_themes'][theme_id] = True
                self.lbl_coins_val.text = str(MOBILE_PLAYER_STATS['player_coins'])
                
                for t_id, card in self.theme_cards.items():
                    card.is_active = False
                    card.update_graphics(card, card.size)
                    
                self.theme_cards[theme_id].is_active = True
                self.theme_cards[theme_id].update_graphics(self.theme_cards[theme_id], self.theme_cards[theme_id].size)
                
                # 1. Вызываем твою системную смену темы
                choose_theme(theme_id)
                
                # 2. МГНОВЕННОЕ ОБНОВЛЕНИЕ ГЛОБАЛЬНЫХ ЦВЕТОВ ИГРЫ НАЛЕТУ ПРИ ПОКУПКЕ
                color_bg = theme_data.get("color_bg", color_bg)
                color_text = theme_data.get("color_text", color_text)
                color_correct = theme_data.get("color_correct", color_correct)
                color_in_word = theme_data.get("color_in_word", color_in_word)
                color_not_in_word = theme_data.get("color_not_in_word", color_not_in_word)
                color_blank = theme_data.get("color_blank", color_blank)
                color_key = theme_data.get("color_key", color_key)
                
                # Защита текста кнопок от сброса в белый цвет
                self.btn_action.color = color_text
                self.btn_sell.color = color_text
                
                # 3. Перерисовываем экран под новые цвета
                self.reposition_elements(self, self.size)
                self.scroll_content.do_layout()
                
                if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
                    MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)
                
                self.select_theme(theme_id)
                print(f"[MGGamesStudio] Тема {theme_id} успешно куплена, применена и сохранена!")

    def process_theme_sell(self, instance):
        global MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC
        # Импортируем глобальные цвета скрипта игры для их сброса к классике налету
        global color_bg, color_text, color_correct, color_in_word, color_not_in_word, color_blank, color_key
        
        theme_id = self.selected_theme_id
        
        # Защита от продажи стартовых бесплатных тем
        if theme_id in ['classic', 'night']:
            return
            
        current_coins = MOBILE_PLAYER_STATS.get('player_coins', 0)
        MOBILE_PLAYER_STATS['player_coins'] = current_coins + 900
        MOBILE_PLAYER_STATS['unlocked_themes'][theme_id] = False
        self.lbl_coins_val.text = str(MOBILE_PLAYER_STATS['player_coins'])
        
        # Если продаваемая тема была активной прямо сейчас — сбрасываем на Классику
        if self.theme_cards[theme_id].is_active:
            # Тушим шарик у проданной темы
            self.theme_cards[theme_id].is_active = False
            self.theme_cards[theme_id].update_graphics(self.theme_cards[theme_id], self.theme_cards[theme_id].size)
            
            # Включаем шарик у Классики
            self.theme_cards['classic'].is_active = True
            self.theme_cards['classic'].update_graphics(self.theme_cards['classic'], self.theme_cards['classic'].size)
            
            # 1. Вызываем системную смену темы лаунчера на классическую
            choose_theme('classic')
            
            # 2. МГНОВЕННЫЙ СБРОС ГЛОБАЛЬНЫХ ЦВЕТОВ ИГРЫ К КЛАССИКЕ
            # Получаем чистые классические цвета напрямую из словаря настроек
            classic_data = color_themes['classic']
            color_bg = classic_data.get("color_bg")
            color_text = classic_data.get("color_text")
            color_correct = classic_data.get("color_correct")
            color_in_word = classic_data.get("color_in_word")
            color_not_in_word = classic_data.get("color_not_in_word")
            color_blank = classic_data.get("color_blank")
            color_key = classic_data.get("color_key")
            
            # 3. Принудительно заставляем холст и элементы экрана перекраситься в классику прямо сейчас
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
            font_name=resource_path("ClearSans-Bold.ttf"), 
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

        self.quests_list_layout = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[0, 10, 0, 15])
        self.quests_list_layout.bind(minimum_height=self.quests_list_layout.setter('height'))

        self.scroll_view.add_widget(self.quests_list_layout)
        self.layout.add_widget(self.scroll_view)

        if hasattr(self, 'top_overlay'):
            self.layout.remove_widget(self.scroll_view)
            self.layout.add_widget(self.scroll_view, index=len(self.layout.children))

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

        self.stats_container.padding = [10, 0, 10, 0]

        total_scroll_width = 3 * 385 + 2 * 10 + 20
        self.stats_row1.size = (total_scroll_width - 20, 72)
        self.stats_row2.size = (total_scroll_width - 20, 72)
        self.stats_container.size = (total_scroll_width, 152)

        self.build_quests_list(launcher_quests)

    def reposition_elements(self, instance, size):
        win_w = Window.width
        win_h = Window.height

        self.lbl_main_title.text = "Квесты"

        self.lbl_main_title.font_size = f"{min(win_w, win_h) * 0.08}px"
        self.lbl_main_title.size = (win_w - 150, 100) 
        self.lbl_main_title.text_size = self.lbl_main_title.size
        
        btn_center_y = win_h - 54
        self.lbl_main_title.center_y = btn_center_y
        self.lbl_main_title.x = 15  
        
        overlay_height = 280
        if hasattr(self, 'top_overlay'):
            self.top_overlay.height = overlay_height
            self.top_overlay.pos = (0, win_h - overlay_height)
            self.overlay_rect.size = (win_w, overlay_height)
            self.overlay_rect.pos = (0, win_h - overlay_height)
            
        if hasattr(self, 'stats_scroll'):
            self.stats_scroll.height = 152
            self.stats_scroll.pos = (0, win_h - 54 - 44 - 152 - 15)
            self.stats_container.height = 152
            
        if hasattr(self, 'scroll_view'):
            self.scroll_view.size = (win_w, win_h - overlay_height - 15)
            self.scroll_view.pos = (0, 10)
            self.quests_list_layout.width = win_w

        if hasattr(self, 'lbl_main_title') and self.lbl_main_title in self.layout.children:
            self.layout.remove_widget(self.lbl_main_title)
            self.layout.add_widget(self.lbl_main_title, index=0)

    def create_card(self, label_text, val_text, val_color):
        card = FloatLayout(size_hint=(None, None), size=(385, 72))
        
        with card.canvas.before:
            Color(*color_blank)
            r_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
        card.bind(pos=lambda inst, v: setattr(r_rect, 'pos', inst.pos), 
                  size=lambda inst, v: setattr(r_rect, 'size', inst.size))
        
        lbl_lbl = Label(
            text=label_text, 
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='20sp', 
            color=color_not_in_word, 
            size_hint=(None, None),
            size=(345, 72),
            text_size=(345, 72),
            pos_hint={'x': 0.06, 'center_y': 0.5}, 
            halign='left', 
            valign='middle'
        )
        card.add_widget(lbl_lbl)
        
        val_len = len(val_text)
        if val_len >= 9:
            v_font = '14sp'
        elif val_len >= 6:
            v_font = '20sp'
        else:
            v_font = '30sp'
        
        lbl_val = Label(
            text=val_text, 
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size=v_font, 
            color=val_color, 
            bold=True, 
            size_hint=(None, None),
            size=(345, 72),
            text_size=(345, 72),
            pos_hint={'right': 0.94, 'center_y': 0.5}, 
            halign='right', 
            valign='middle'
        )
        card.add_widget(lbl_val)
        
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
        text_w = Window.width - 45
        name_lbl = Label(
            text=name.upper(), font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='18sp', color=text_color, bold=True,
            size_hint=(None, None), width=text_w, text_size=(text_w, None),
            halign='left', valign='top'
        )

        desc_lbl = Label(
            text=description, font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='13sp', color=text_color,
            size_hint=(None, None), width=text_w, text_size=(text_w, None),
            halign='left', valign='top'
        )

        info_line = FloatLayout(size_hint=(1, None), height=35)
        
        lbl_rare = Label(
            text=type_text, font_name=resource_path("ClearSans-Bold.ttf"), 
            font_size='13sp', color=rarity_color, bold=True, size_hint=(None, None),
            size=(120, 35), text_size=(120, 35), pos_hint={'x': 0.06, 'center_y': 0.5},
            halign='left', valign='middle'
        )
        
        lbl_rew = Label(
            text=f"Награда: {reward}", font_name=resource_path("ClearSans-Bold.ttf"), 
            font_size='13sp', color=color_in_word, bold=True, size_hint=(None, None),
            size=(150, 35), text_size=(150, 35), pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center', valign='middle'
        )
        
        status_txt = "ВЫПОЛНЕНО" if is_done else f"{progress}/{goal}"
        lbl_stat = Label(
            text=status_txt, font_name=resource_path("ClearSans-Bold.ttf"), 
            font_size='14sp', color=progress_color, bold=True, size_hint=(None, None),
            size=(200, 35), text_size=(200, 35), pos_hint={'right': 0.94, 'center_y': 0.5},
            halign='right', valign='middle'
        )
        
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

        row.add_widget(text_group)
        return row

    def build_quests_list(self, launcher_quests):
        """Полный вывод квестов с правильной сортировкой: выполненные уходят ВНИЗ списка"""
        self.quests_list_layout.clear_widgets()
        
        if not launcher_quests:
            return

        # ИСПРАВЛЕНО: Сортируем так, чтобы выполненные (done=True) уходили в самый низ, как на ПК!
        all_keys = list(launcher_quests.keys())
        sorted_keys = sorted(all_keys, key=lambda k: launcher_quests[k].get("done", False), reverse=False)
        
        for q_key in sorted_keys:
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

    def update_daily_quests_mobile(self):
        """Полный перенос функции update_daily_quests из guess_word_pc_v110.py"""
        global MOBILE_PLAYER_STATS, MOBILE_QUESTS
        import time
        import copy

        current_time_struct = time.localtime()
        current_day = current_time_struct.tm_mday
        
        # Читаем день последнего сброса из файла сохранения
        last_update_day = MOBILE_PLAYER_STATS.get("last_update_day", -1)

        # Если день совпадает и в памяти уже крутится выбранная пятерка — ничего не сбрасываем
        if current_day == last_update_day and MOBILE_PLAYER_STATS.get("active_quests"):
            MOBILE_QUESTS = MOBILE_PLAYER_STATS["active_quests"]
            return

        # Наступил новый день! Выбираем 5 случайных квестов из полной базы данных (из 12 штук)
        print("[MGGamesStudio] Новый день по местному времени! Выбираем 5 случайных квестов...")
        
        # Нам нужен доступ к полной статичной базе из 12 квестов, которую передал лаунчер
        full_base_quests = MOBILE_PLAYER_STATS.get("quests_dict", {})
        if not full_base_quests:
            return

        commons = [k for k, v in full_base_quests.items() if v.get("type", "common") == "common"]
        rares = [k for k, v in full_base_quests.items() if v.get("type", "common") == "rare"]
        epics = [k for k, v in full_base_quests.items() if v.get("type", "common") == "epic"]

        # Рандомим строго по твоей формуле: 2 обычных, 2 редких, 1 эпический
        chosen_keys = random.sample(commons, 2) + random.sample(rares, 2) + random.sample(epics, 1)

        new_active_quests = {}
        for key in chosen_keys:
            new_active_quests[key] = copy.deepcopy(full_base_quests[key])
            new_active_quests[key]["progress"] = 0
            new_active_quests[key]["done"] = False

        # Фиксируем выбранную пятерку и сегодняшний день в сохранении лаунчера
        MOBILE_PLAYER_STATS["active_quests"] = new_active_quests
        MOBILE_PLAYER_STATS["last_update_day"] = current_day
        MOBILE_QUESTS = new_active_quests

        # Моментально записываем изменения в скрытый файл json
        if 'MOBILE_SAVE_FUNC' in globals() and MOBILE_SAVE_FUNC is not None:
            MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)

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
        
        # ИСПРАВЛЕНО: Накрываем менеджер экранов единым фоном, который никогда не мигает!
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
    global MOBILE_ALL_WORDS, MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC, MOBILE_ACHIVEMENTS, MOBILE_QUESTS
    MOBILE_ALL_WORDS = words_list
    MOBILE_PLAYER_STATS = player_stats
    MOBILE_SAVE_FUNC = save_function
    
    # Считывание достижений (Твой рабочий код)
    if "achivements_dict" in player_stats and player_stats["achivements_dict"]:
        MOBILE_ACHIVEMENTS = player_stats["achivements_dict"]
    else:
        MOBILE_ACHIVEMENTS = player_stats.get("unlocked_achivements", {})
        
    if "quests_dict" in player_stats and player_stats["quests_dict"]:
        MOBILE_QUESTS = player_stats["quests_dict"]
    else:
        MOBILE_QUESTS = player_stats.get("active_quests", {})
        
    print(f"[MGGamesStudio ТЕЛ] Достижений {len(MOBILE_ACHIVEMENTS)}, квестов {len(MOBILE_QUESTS)}.")
    MobileApp().run()