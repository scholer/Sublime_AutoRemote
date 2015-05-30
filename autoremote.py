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

Sublime AutoRemote - plugin to interact with AutoRemote on your device.

Supported settings:

autoremote_key
autoremote_default_sender
autoremote_devices:
  <device>:
    target
    password
autoremote_default_ttl
autoremote_baseurl

"""

import os
from urllib.parse import urljoin

## Sublime imports:
import sublime
import sublime_plugin

## Local imports:
from .autoremote_utils import *
from .sublime_utils import *

## Constants
SETTINGS_NAME = "AutoRemote.sublime-settings"


class AutoremoteSetKeyFromUrl(sublime_plugin.WindowCommand):
    """
    Set AutoRemote key.
    Command string: autoremote_set_key_from_url (WindowCommand)
    """
    def run(self, url=None):
        # show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
        self.window.show_input_panel('AutoRemote URL:', url or '', self.on_done, None, None)
    def on_done(self, url):
        if not url:
            msg = "No URL input..."
        else:
            try:
                key = get_key_from_url(url)
            except (KeyError, AttributeError, IndexError) as e:
                msg = "Failed to parse url. %s: %s" % (type(e), e)
            else:
                persist_setting("autoremote_key", key)
                msg = "Your AutoRemote key has been updated (%s)" % len(key)
        print(msg)
        sublime.status_message(msg)


class AutoremoteSendMessagePrompt(sublime_plugin.WindowCommand):
    """
    Send AutoRemote message (will be prompted by from the user).
    Command string: autoremote_send_message (WindowCommand)
    """
    def run(self, message=None, **kwargs):
        # show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
        self.kwargs = kwargs
        self.window.show_input_panel('AutoRemote URL:', url, self.on_done, None, None)
    def on_done(self, url):
        send_message(message, **self.kwargs)


class AutoremoteSendMessage(sublime_plugin.WindowCommand):
    """
    Send AutoRemote message.
    Command string: autoremote_send_message (WindowCommand)
    """
    def run(self, message, **kwargs):
        # show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
        send_message(message, **kwargs)


class AutoremoteSendNotification(sublime_plugin.WindowCommand):
    """
    Send AutoRemote notification.
    Command string: autoremote_send_notification (WindowCommand)
    """
    def run(self, message, **kwargs):
        # show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
        send_notification(message, **kwargs)


class AutoremoteSendIntent(sublime_plugin.WindowCommand):
    """
    Send AutoRemote intent.
    Command string: autoremote_send_intent (WindowCommand)
    """
    def run(self, message, **kwargs):
        # show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
        send_intent(message, **kwargs)




class AutoremoteCmdsPanelCommand(sublime_plugin.WindowCommand):
    """
    Displays a quick panel with available commands.
    """
    options = []
    SNIPPET_CHAR = u'\u24C8'

    def run(self):
        self.SNIPPET_CHAR = mw.get_setting('mediawiker_snippet_char')
        self.options = mw.get_setting('mediawiker_panel', {})
        if self.options:
            office_panel_list = ['\t%s' % val['caption'] if val['type'] != 'snippet' else '\t%s %s' % (self.SNIPPET_CHAR, val['caption']) for val in self.options]
            self.window.show_quick_panel(office_panel_list, self.on_done)

    def on_done(self, index):
        if index >= 0:
            # escape from quick panel return -1
            try:
                action_type = self.options[index]['type']
                action_value = self.options[index]['value']
                action_args = self.options[index].get('args') # None is an acceptable value for run_command args
                print("Mediawiker Panel selection: action_type=%s, action_value=%s, action_args=%s" % (action_type, action_value, action_args))
                if action_type == 'snippet':
                    # run snippet
                    self.window.active_view().run_command("insert_snippet", {"name": action_value})
                elif action_type == 'window_command':
                    # run command
                    self.window.run_command(action_value, action_args)
                elif action_type == 'text_command':
                    # run command
                    self.window.active_view().run_command(action_value, action_args)
            except ValueError as e:
                sublime.status_message(e)
