#!/bin/bash

# Exit if something fails
set -e

if [[ -z "$XDG_DATA_HOME" ]]; then
    prefix=~/.local/share
else
    prefix="$XDG_DATA_HOME"
fi

rm $prefix/kservices5/krunner/dbusplugins/krunnersteam.desktop
rm $prefix/dbus-1/services/com.github.xtibor.krunnersteam.service
kquitapp5 krunner

