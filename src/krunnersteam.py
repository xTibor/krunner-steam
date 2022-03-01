#!/usr/bin/python3

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)

objpath = "/krunnersteam"
iface = "org.kde.krunner1"

class Runner(dbus.service.Object):
    def reload_steam_library(self):
        from blacklist import appid_blacklist
        from deserializer import steam_deserialize
        from os.path import exists as path_exists

        self.steam_library = {}
        libraryfolders = steam_deserialize(self.libraryfolders_path)

        library_index = 0
        while str(library_index) in libraryfolders:
            library_root = libraryfolders[str(library_index)]["path"]

            for appid in libraryfolders[str(library_index)]["apps"]:
                app_manifest_path = library_root + "/steamapps/appmanifest_" + appid + ".acf"
                if path_exists(app_manifest_path) and (appid not in appid_blacklist):
                    app_manifest = steam_deserialize(app_manifest_path)
                    app_icon_path = self.steam_root + "/appcache/librarycache/" + appid + "_icon.jpg"
                    app_local_files = library_root + "/steamapps/common/" + app_manifest["installdir"]

                    self.steam_library[app_manifest["appid"]] = {
                        "name": app_manifest["name"],
                        "icon": app_icon_path,
                        "local-files": app_local_files,
                    }
            library_index += 1

    def __init__(self):
        import os

        self.steam_root = os.path.expanduser("~/.local/share/Steam")
        self.libraryfolders_path = self.steam_root + "/steamapps/libraryfolders.vdf"
        self.reload_steam_library()

        dbus.service.Object.__init__(self, dbus.service.BusName("com.github.xtibor.krunnersteam", dbus.SessionBus()), objpath)
        # TODO: inotify libraryfolders.vdf -> reload_steam_library

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        results = []

        for appid, properties in self.steam_library.items():
            if query.lower() in properties["name"].lower():
                results.append((appid, properties["name"], properties["icon"], 100, 1.0, {}))

        results.sort(key = lambda result: result[1].lower())

        return results

    @dbus.service.method(iface, out_signature='a(sss)')
    def Actions(self):
        return [
            ("library",       "Steam Library", "folder-games-symbolic"),
            ("community-hub", "Community Hub", "system-users"         ),
            ("local-files",   "Local Files",   "folder"               ),
        ]

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, appid: str, action: str):
        import subprocess

        # https://developer.valvesoftware.com/wiki/Steam_browser_protocol
        if action == "":
            subprocess.Popen(["steam", "steam://rungameid/" + appid])
        elif action == "library":
            subprocess.Popen(["steam", "steam://nav/games/details/" + appid])
        elif action == "community-hub":
            subprocess.Popen(["steam", "steam://url/SteamWorkshopPage/" + appid])
        elif action == "local-files":
            subprocess.Popen(["xdg-open", self.steam_library[appid]["local-files"]])

runner = Runner()
loop = GLib.MainLoop()
loop.run()
