[app]
# Nama package dan versi
title = MCGG-Xbot
package.name = mcggxbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,md,json
version = 1.0.0
requirements = python3,kivy,torch,torchvision,easyocr,pillow
orientation = portrait
fullscreen = 0

# Ikon (opsional, pastikan file ada)
icon.filename = %(source.dir)s/icon.png

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO

# Entry point (pastikan file ini ada di project kamu)
entrypoint = main.py

# APK output name
package.release.name = MCGG-Xbot-$(version).apk

# Keystore untuk signing (diinject dari secrets GitHub)
android.release_keystore = mcgg-release-key.jks
android.release_keyalias = ${KEY_ALIAS}
android.release_keyalias_passwd = ${KEY_PASSWORD}
android.release_keystore_passwd = ${KEYSTORE_PASSWORD}


[buildozer]
log_level = 2
warn_on_root = 1
