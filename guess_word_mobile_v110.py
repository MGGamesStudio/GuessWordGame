import os
import sys

# Импорты базовых элементов интерфейса Kivy и менеджера экранов
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

# Адаптер путей для встроенных ресурсов (Шрифты)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ========================================================================
# 1. ГЛАВНЫЙ ЭКРАН: МЕНЮ МОБИЛКИ С ТЕСТОВЫМ ВЫВОДОМ СТАТИСТИКИ
# ========================================================================
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Главный контейнер
        main_layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        # 1. Заголовок игры
        title_label = Label(
            text="Угадай слово",
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='50sp',
            bold=True,
            color=(0.12, 0.15, 0.18, 1),
            size_hint_y=0.2,
            halign='center', valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        main_layout.add_widget(title_label)
        
        # 2. БЛОК СТАТИСТИКИ (Выводим монеты)
        coins = MOBILE_PLAYER_STATS.get("player_coins", 0)
        wins = MOBILE_PLAYER_STATS.get("total_wins", 0)
        streak = MOBILE_PLAYER_STATS.get("current_win_streak", 0)
        
        # Присваиваем текстовую метку переменной self.stats_label, чтобы обновлять её напрямую
        self.stats_label = Label(
            text=f"Ваши монеты: {coins}\nПобед: {wins} | Серия: {streak}",
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='18sp',
            bold=True,
            color=(0.25, 0.45, 0.75, 1),
            size_hint_y=0.15,
            halign='center', valign='middle'
        )
        self.stats_label.bind(size=self.stats_label.setter('text_size'))
        main_layout.add_widget(self.stats_label)
        
        # 3. Блок кнопок меню
        menu_buttons_box = BoxLayout(orientation='vertical', spacing=12, size_hint_x=None, width=320)
        menu_buttons_box.pos_hint = {'center_x': 0.5} 
        
        btn_play = self.create_menu_button("Играть")
        btn_play.bind(on_release=self.go_to_game)
        
        btn_how_to = self.create_menu_button("Как играть")
        btn_achievements = self.create_menu_button("Достижения")
        
        # Кнопка теста
        btn_add_coins = self.create_menu_button("Тест: Получить +10 монет")
        btn_add_coins.bind(on_release=self.test_add_coins)
        
        menu_buttons_box.add_widget(btn_play)
        menu_buttons_box.add_widget(btn_how_to)
        menu_buttons_box.add_widget(btn_achievements)
        menu_buttons_box.add_widget(btn_add_coins)
        
        # Нижний ряд
        bottom_row_box = BoxLayout(spacing=12, size_hint_y=None, height=52)
        btn_quests = self.create_menu_button("Квесты")
        btn_exit = self.create_menu_button("Выйти")
        btn_exit.bind(on_release=lambda x: App.get_running_app().stop())
        
        bottom_row_box.add_widget(btn_quests)
        bottom_row_box.add_widget(btn_exit)
        menu_buttons_box.add_widget(bottom_row_box)
        main_layout.add_widget(menu_buttons_box)
        
        # Копирайт
        copyright_label = Label(
            text="Угадай слово by MGGamesStudio. v.1.1.0",
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='11sp',
            color=(0.6, 0.64, 0.68, 1),
            size_hint_y=0.1,
            halign='center', valign='bottom'
        )
        copyright_label.bind(size=copyright_label.setter('text_size'))
        main_layout.add_widget(copyright_label)
        
        self.add_widget(main_layout)

    def create_menu_button(self, text):
        return Button(
            text=text,
            font_name=resource_path("ClearSans-Bold.ttf"),
            font_size='20sp',
            bold=True,
            color=(0.12, 0.15, 0.18, 1),
            background_normal='',
            background_color=(0.86, 0.89, 0.93, 1),
            size_hint_y=None, height=52
        )
        
    def go_to_game(self, instance):
        self.manager.current = 'game'

    def test_add_coins(self, instance):
        """ БЕЗОПАСНОЕ НАЧИСЛЕНИЕ МОНЕТ: Прямое обращение без индексов списков """
        global MOBILE_PLAYER_STATS
        MOBILE_PLAYER_STATS["player_coins"] = MOBILE_PLAYER_STATS.get("player_coins", 0) + 10
        
        # Отправляем измененные данные лаунчеру для записи в AppData
        if MOBILE_SAVE_FUNC is not None:
            MOBILE_SAVE_FUNC(MOBILE_PLAYER_STATS)
            
        # Обновляем текст на экране напрямую через сохраненную ссылку
        coins = MOBILE_PLAYER_STATS["player_coins"]
        wins = MOBILE_PLAYER_STATS.get("total_wins", 0)
        streak = MOBILE_PLAYER_STATS.get("current_win_streak", 0)
        
        self.stats_label.text = f"Ваши монеты: {coins}\nПобед: {wins} | Серия: {streak}"

# ========================================================================
# 2. ИГРОВОЙ ЭКРАН (ЗАГЛУШКА)
# ========================================================================
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)
        label = Label(text="Здесь будет мобильный игровой процесс", font_name=resource_path("ClearSans-Bold.ttf"), font_size='24sp', color=(0.12, 0.15, 0.18, 1))
        layout.add_widget(label)
        
        btn_back = Button(text="Назад в меню", size_hint=(None, None), size=(150, 50), background_normal='', background_color=(0.86, 0.89, 0.93, 1), color=(0.12, 0.15, 0.18, 1))
        btn_back.bind(on_release=self.go_to_menu)
        layout.add_widget(btn_back)
        self.add_widget(layout)
        
    def go_to_menu(self, instance):
        self.manager.current = 'menu'

# ========================================================================
# 3. ТОЧКА ВХОДА ДЛЯ ТОТАЛ-ЛАУНЧЕРА
# ========================================================================
# Теперь функция ЖЕЛЕЗНО принимает 3 аргумента от лаунчера, исправляя TypeError
def start_mobile_game(words_list, player_stats, save_function):
    global MOBILE_ALL_WORDS, MOBILE_PLAYER_STATS, MOBILE_SAVE_FUNC
    MOBILE_ALL_WORDS = words_list
    MOBILE_PLAYER_STATS = player_stats
    MOBILE_SAVE_FUNC = save_function
    
    Window.size = (360, 640)
    Window.clearcolor = (0.96, 0.97, 0.98, 1)
    sm = ScreenManager()
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(GameScreen(name='game'))
    
    class MobileApp(App):
        def build(self):
            return sm
            
    MobileApp().run()
