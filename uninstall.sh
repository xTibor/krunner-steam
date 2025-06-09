#!/bin/bash

# Exit if something fails
set -e

prefix="${XDG_DATA_HOME:-$HOME/.local/share}"
krunner_dbusdir="$prefix/krunner/dbusplugins"

rm $prefix/dbus-1/services/com.github.xtibor.krunnersteam.service
rm $krunner_dbusdir/krunnersteam.desktop
kquitapp6 krunner
