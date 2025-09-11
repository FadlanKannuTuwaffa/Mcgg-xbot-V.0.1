[app]
title = MCGG Pairing Predictor (OCR Offline)
package.name = mcggpredictorocr
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg
version = 0.5
requirements = python3,kivy,kivymd,easyocr,torch,pillow
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.ndk = 25b
