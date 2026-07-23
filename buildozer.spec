[app]
title = Guess Word Game
package.name = guesswordgame
package.domain = org.mggamesstudio
source.dir = .

# Указываем расширения всех важных файлов проекта
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,ico

version = 1.1.0

# Основные зависимости для Kivy приложения
requirements = python3,kivy

# Иконка приложения (Buildozer подхватит её)
icon.filename = %(source.dir)s/app_icon.ico

orientation = portrait
fullscreen = 0

# Настройки сборки под Android
android.api = 33
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True
