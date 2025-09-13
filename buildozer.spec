[app]
# Nama package unik (jangan pakai spasi atau karakter aneh)
package.name = mcgg_xbot
package.domain = org.mcggxbot

# Nama aplikasi yang akan tampil di HP
title = MCGG-Xbot_V.0.1

# Versi aplikasi
version = 0.1

# File utama (entry point Python)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# File python utama (sesuaikan dengan nama file kamu, misal main.py)
main.py = main.py

# Ikon aplikasi
icon.filename = %(source.dir)s/assets/icon.png

# Orientation (all, landscape, portrait)
orientation = all

# Permissions (contoh kalau butuh kamera/ocr/storage)
android.permissions = CAMERA, INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# Minimum Android API (21 = Android 5.0 Lollipop)
android.minapi = 21

# Target Android API (disarankan 33 untuk Android 13)
android.api = 33

# SDK versi terbaru
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# Nama file keystore
android.release_keystore = mcgg-release-key.jks
android.release_keyalias = mcgg-xbot-key

# Password keystore (gunakan secrets di GitHub, jangan hardcode di sini!)
# biarkan kosong, nanti buildozer pakai environment
# android.release_keystore_pass = 
# android.release_keyalias_pass = 

# Package mode
fullscreen = 0
