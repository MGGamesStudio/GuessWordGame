[app]
title = Угадай Слово
package.name = guesswordgame
package.domain = org.mggamesstudio

# Указываем файлы игры для мобильной сборки
source.dir = .
source.include_exts = png,jpg,ttf,txt,ico
source.include_files = guess_word_total_v110.py, guess_word_mobile_v110.py

# Версия и СТАБИЛЬНЫЕ зависимости
version = 1.1.0
requirements = python3,kivy==2.3.0,pillow

# Ориентация экрана (только вертикально для телефонов)
orientation = portrait
fullscreen = 1

# Фиксируем стабильное API и NDK, чтобы hstrerror не ломал сборку
android.api = 33
android.minapi = 21
android.ndk = 25.2.9519653

# Архитектуры процессоров для современных смартфонов
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
