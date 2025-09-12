[app]
title = MCGG-Xbot_V.0.1
package.name = mcggxbot
package.domain = org.mcgg.xbot

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

main.py = main.py

version = 0.1

icon.filename = %(source.dir)s/mcgg1.webp

orientation = portrait

android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.ndk_api = 21

fullscreen = 0

android.release_keystore = mcgg-release-key.jks
android.release_keystore_pass = xbot234
android.release_keyalias = mcgg-xbot-key
android.release_keyalias_pass = xbot234

requirements = python3,kivy,pillow,easyocr,torch,torchvision,python-for-android

android.add_src = src
android.add_libs_armeabi = libs/armeabi/*.so
android.add_libs_arm64 = libs/arm64-v8a/*.so
android.add_libs_x86 = libs/x86/*.so
android.add_libs_x86_64 = libs/x86_64/*.so

log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
