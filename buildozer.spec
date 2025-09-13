[app]
title = MCGG-Xbot
package.name = mcggxbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Icon (opsional kalau ada)
icon.filename = %(source.dir)s/data/icon.png

# Entry point
entrypoint = main.py

# APK name
package.name = mcggxbot
package.domain = org.mcgg

# Permissions (tambahkan sesuai kebutuhan app kamu)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Target Android SDK & NDK
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_path = $ANDROID_NDK_HOME

# Build tools (cocok dengan yang diinstal di workflow)
android.build_tools_version = 33.0.2

# Release config
p4a.release = 1

# Jika perlu log debug
log_level = 2
