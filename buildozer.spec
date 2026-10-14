[app]
title = Календарь смен
package.name = calendarapp
package.domain = org.mytest
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
requirements = python3==3.11.5,kivy
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
