#!/bin/bash

# Exit if something fails
set -e


if [[ -z "$XDG_DATA_HOME" ]]; then
    prefix=~/.local/share
else
    prefix="$XDG_DATA_HOME"
fi

mkdir -p $prefix/kservices5/krunner/dbusplugins/
mkdir -p $prefix/dbus-1/services/

cp krunnersteam.desktop $prefix/kservices5/krunner/dbusplugins/
sed "s|%{PROJECTDIR}/krunnersteam.py|${PWD}/krunnersteam.py|" "com.github.xtibor.krunnersteam.service" > $prefix/dbus-1/services/com.github.xtibor.krunnersteam.service

kquitapp5 krunner

