[app]

# Nama aplikasi yang tampil di HP
title = MCGG-Xbot_V.0.1

# Nama paket unik (ubah kalau mau)
package.name = mcggxbot
package.domain = org.mcgg.xbot

# File Python utama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Entry point (pastikan file ini ada di repo, misal main.py)
main.py = main.py

# Versi aplikasi
version = 0.1

# Ikon aplikasi (opsional, letakkan file di repo lalu ganti nama)
icon.filename = %(source.dir)s/mcgg1.webp

# Orientasi layar
orientation = portrait

# Permission yang diperlukan
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# Minimum Android SDK
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.ndk_api = 21

# Pilihan untuk packaging
fullscreen = 0

# --- Signing ---
android.release_keystore = mcgg-release-key.jks
android.release_keystore_pass = xbot234
android.release_keyalias = mcgg-xbot-key
android.release_keyalias_pass = xbot234

# --- Dependencies (OCR, ML, UI) ---
requirements = python3,kivy,buildozer,cython,pillow,easyocr,torch,torchvision

# Agar OCR bisa berjalan offline
android.add_src = src
android.add_libs_armeabi = libs/armeabi/*.so
android.add_libs_arm64 = libs/arm64-v8a/*.so
android.add_libs_x86 = libs/x86/*.so
android.add_libs_x86_64 = libs/x86_64/*.so

# --- Optimasi ---
log_level = 2
warn_on_root = 1

[buildozer]

log_level = 2
warn_on_root = 1
