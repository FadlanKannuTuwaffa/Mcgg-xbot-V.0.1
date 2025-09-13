[app]

# Nama aplikasi
title = MCGG-Xbot_V.0.1
package.name = mcgg_xbot
package.domain = org.mcgg.xbot

# Versi aplikasi
version = 0.1

# Source code utama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Ikon app (opsional bisa ganti file)
icon.filename = %(source.dir)s/data/icon.png

# Orientasi layar (portrait atau landscape)
orientation = portrait

# Masukkan permission Android yang dibutuhkan OCR & AI
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA

# Nama file saat di-build
android.archs = arm64-v8a, armeabi-v7a

# Keystore untuk signed APK
android.release_keystore = mcgg-release-key.jks
android.release_keystore_pass = xbot234
android.release_keyalias = mcgg-xbot-key
android.release_keyalias_pass = xbot234

# Minimum & target SDK
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# Extra requirements (OCR, Torch, dll.)
requirements = python3, kivy, pillow, easyocr, torch, torchvision

# Entry point
entrypoint = main.py

# (Opsional) Fullscreen
fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1
