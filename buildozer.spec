[app]
title = Угадай Слово
package.name = guesswordgame
package.domain = org.mggamesstudio

# Указываем файлы игры для мобильной сборки
source.dir = .
source.include_exts = png,jpg,ttf,txt,ico
source.include_files = guess_word_total_v110.py, guess_word_mobile_v110.py

# Версия и зависимости
version = 1.1.0
requirements = python3,kivy

# Ориентация экрана (только вертикально для телефонов)
orientation = portrait
fullscreen = 1

# Архитектуры процессоров для современных смартфонов
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
