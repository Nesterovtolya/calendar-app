[app]
title = Календарь смен
package.name = calendarapp
package.domain = org.mytest
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
requirements = python3,kivy==2.3.1,openssl,pillow
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/grafik.png
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
