#!/usr/bin/env python
# -*- coding: utf-8 -*-
##    Copyright 2015 Rasmus Scholer Sorensen, rasmusscholer@gmail.com
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=C0103,W0232,R0903,R0201


"""

Module with autoremote functions.
(Separated to enable debugging and use as library import.)

"""


## Sublime imports:
import sublime
import sublime_plugin

## Constants
SETTINGS_NAME = "AutoRemote.sublime-settings"


def get_settings():
    return sublime.load_settings(SETTINGS_NAME)

def get_setting(key, setting=None, settings=None):
    """
    Specify the settings will basically just do settings.get(key)
    """
    if settings is None:
        settings = sublime.load_settings(SETTINGS_NAME)
    return settings.get(key)

def persist_setting(key, value):
    settings = sublime.load_settings(SETTINGS_NAME)
    settings.set(key, value)
    sublime.save_settings(SETTINGS_NAME)
