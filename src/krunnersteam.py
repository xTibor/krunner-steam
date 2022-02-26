#!/usr/bin/python3

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

import os
from blacklist import appid_blacklist
from deserializer import steam_deserialize

DBusGMainLoop(set_as_default=True)

objpath = "/krunnersteam"
iface = "org.kde.krunner1"

class Runner(dbus.service.Object):
    def reload_steam_library(self):
        print("Reloading Steam library...")

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

    def __init__(self):
        self.reload_steam_library()
        dbus.service.Object.__init__(self, dbus.service.BusName("com.github.xtibor.krunnersteam", dbus.SessionBus()), objpath)
        # TODO: inotify libraryfolders.vdf -> reload_steam_library

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        """This method is used to get the matches and it returns a list of tupels"""
        if query == "hello":
            # data, text, icon, type (Plasma::QueryType), relevance (0-1), properties (subtext, category and urls)
            return [("Hello", "Hello from %{APPNAME}!", "document-edit", 100, 1.0, {'subtext': 'Demo Subtext'})]
        return []

    @dbus.service.method(iface, out_signature='a(sss)')
    def Actions(self):
        return [
            # (id, text, icon)
            ("library", "Steam Library", "folder-games-symbolic"),
            ("community-hub", "Community Hub", "system-users"),
        ]

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, data: str, action_id: str):
        print(data, action_id)
        # https://developer.valvesoftware.com/wiki/Steam_browser_protocol
        # steam steam://rungameid/1289310
        # steam steam://nav/games/details/1289310
        # steam steam://url/SteamWorkshopPage/1289310


runner = Runner()
loop = GLib.MainLoop()
loop.run()
