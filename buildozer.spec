[app]

# (str) Title of your application
title = Stealth Network Intelligence

# (str) Package name
package.name = stealthnetworkintel

# (str) Package domain (needed for android/ios packaging)
package.domain = com.stealth.intel

# (str) Source code where the main.py live
source = .
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,db

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,android

# (str) Presplash of the application
#presplash.filename = %(source_dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source_dir)s/data/icon.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_PHONE_STATE,GET_TASKS

# (int) Target Android API, should be as high as possible.
android.api = 30

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
android.theme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
android.whitelist = 

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx requires android.api >= 28
android.enable_androidx = False

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for further information
android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle dependencies to add
android.gradle_dependencies = 

# (bool) Enable AndroidX build. Use when android.enable_androidx is True
# android.enable_androidx_build = False

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin

# (bool) — Don't ask to download the闲置依赖项s even if needed
android.download_ignore_cache_version = False

# (bool) — Ignore redundant instock resources
android.copy_libs = 1

# (str) — Override the minimal Android SDK version
android.minapi = 21

# (bool) — Enable AndroidX deployment. When True, Buildozer will download
#         aiflow-AndroidX.startswith, android.build.tools and android.repository packages
#         as if android.gradle_dependencies contain aiflow-AndroidX.startswith
android.enable_androidx = False

# (bool) — Enable Android Gradle plugin build. When True, Buildozer will
#         use Android Gradle plugin build. When False, Buildozer will
#         use Android Ant build. When True, Buildozer will also add the
#         `buildozer require` command in the spec.
android.enable_gradle_plugin_build = False