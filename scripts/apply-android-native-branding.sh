#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="native-android-res"
TARGET_DIR="android/app/src/main/res"

if [ ! -d "$TARGET_DIR" ]; then
  echo "Android resource directory not found: $TARGET_DIR" >&2
  echo "Run this after 'npx cap add android' / Capacitor sync." >&2
  exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
  echo "Native branding source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

echo "Applying TCCC launcher icon and native splash resources..."
cp -R "$SOURCE_DIR"/* "$TARGET_DIR"/
test -f "$TARGET_DIR/mipmap-xxxhdpi/ic_launcher.png"
test -f "$TARGET_DIR/mipmap-xxxhdpi/ic_launcher_foreground.png"
test -f "$TARGET_DIR/drawable-port-xxxhdpi/splash.png"
test -f "$TARGET_DIR/values-v31/tccc_splash_styles.xml"

echo "TCCC native Android branding applied successfully."
