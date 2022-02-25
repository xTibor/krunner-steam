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

steam_root = os.path.expanduser("~/.local/share/Steam")

libraryfolders_path = steam_root + "/steamapps/libraryfolders.vdf"
libraryfolders = steam_deserialize(libraryfolders_path)

library_index = 0
while str(library_index) in libraryfolders:
    library_root = libraryfolders[str(library_index)]["path"]

    for appid in libraryfolders[str(library_index)]["apps"]:
        app_manifest_path = library_root + "/steamapps/appmanifest_" + appid + ".acf"
        app_manifest = steam_deserialize(app_manifest_path)
        print(app_manifest["name"])

    library_index += 1
