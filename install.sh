#!/bin/bash

# Standalone install script for copying files

set -e

prefix="${XDG_DATA_HOME:-$HOME/.local/share}"
krunner_dbusdir="$prefix/krunner/dbusplugins"
services_dir="$prefix/dbus-1/services/"

mkdir -p "$krunner_dbusdir"
mkdir -p "$services_dir"

cp krunner-steam.desktop "$krunner_dbusdir"
printf '[D-BUS Service]\nName=com.github.xtibor.krunnersteam\nExec=%s/src/main.py' "$PWD" > "$services_dir/com.github.xtibor.krunnersteam.service"

kquitapp6 krunner
