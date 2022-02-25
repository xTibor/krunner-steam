#!/usr/bin/env python3

def steam_deserialize(filename):
    from tokenize import tokenize

    # Reusing Python's source tokenizer to read Steam's custom serialization format
    # https://docs.python.org/3/library/tokenize.html
    file = open(filename, "rb")
    tokens = [token.string.strip('"') for token in tokenize(file.readline)]

    def read_object(tokens):
        result = {}

        tokens.pop(0) # Remove "{"
        tokens.pop(0) # Remove "\n"

        while tokens[:2] != ["}", "\n"]:
            name = tokens.pop(0)
            if tokens[:3] == ["\n", "{", "\n"]:
                tokens.pop(0) # Remove "\n"
                result[name] = read_object(tokens)
            else:
                result[name] = tokens.pop(0)
                tokens.pop(0) # Remove "\n"

        tokens.pop(0) # Remove "}"
        tokens.pop(0) # Remove "\n"
        return result

    tokens.pop(0) # Remove encoding
    tokens.pop(0) # Remove root name
    tokens.pop(0) # Remove "\n"

    return read_object(tokens)

import os

appid_blacklist = [
    "228980",  # Steamworks Common Redistributables
    "1391110", # Steam Linux Runtime - Soldier
    "1493710", # Proton Experimental
    "1580130", # Proton 6.3
    "1887720", # Proton 7.0
]

steam_root = os.path.expanduser("~/.local/share/Steam")

libraryfolders_path = steam_root + "/steamapps/libraryfolders.vdf"
libraryfolders = steam_deserialize(libraryfolders_path)

library_index = 0
while str(library_index) in libraryfolders:
    library_root = libraryfolders[str(library_index)]["path"]

    for appid in libraryfolders[str(library_index)]["apps"]:
        if appid not in appid_blacklist:
            app_manifest_path = library_root + "/steamapps/appmanifest_" + appid + ".acf"
            app_manifest = steam_deserialize(app_manifest_path)
            app_icon_path = steam_root + "/appcache/librarycache/" + appid + "_icon.jpg"

            print(app_manifest["appid"], app_manifest["name"])

    library_index += 1

# steam steam://rungameid/1289310
# https://invent.kde.org/frameworks/krunner/-/tree/master/templates/runnerpython
