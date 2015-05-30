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


Send message fields/parameters: (It seems all data is sent as url query params)

message
target      # Target (Optional)
sender      # Act as Sender (Optional)
password    # password (optional)
ttl         # Time to live, message validity time in seconds (optional)
collapseKey # Message group (optional)

Further doc:
Target:         Sets the Target on this message
Sender:         The device that receives this message will reply to this device key when choosing
                "Last Sender" in the devices list).
Password:       The password you have configured on your device.
TTL:            Time in seconds AutoRemote will try to deliver the message for before giving up.
Message group:  If the receiving device is unreachable, only one message in a
                message group will be delivered. Useful you if e.g. leave a device in airplane
                mode at night and only want to receive the last of the messages that were sent
                during that time. Leave blank to deliver all messages.


AutoRemoteNotification params:
text
sound
vibration
url
id
action
icon
led
ledon
ledoff
picture     # picture url
message     # Action on Receive
share
action1
action1name
action1icon
action2
action2name
action2icon
action3
action3name
action3icon
persistent
statusbaricon
ticker
dismissontouch
priority
number
contentinfo
subtext
maxprogress
progress
actionondismiss
cancel

(no target?)
sender      # Act as Sender (Optional)
password    # password (optional)
ttl         # Time to live, message validity time in seconds (optional)
collapseKey # Message group (optional)

"""

import os
import sys
from urllib.parse import urljoin, urlparse, parse_qs # parse_qsl returns a list of tuples.
# OH MY FUCKING GOD, requests IS NOT AVAILABLE IN DEFAUTL SUBLIME ??
try:
    import requests
except ImportError:
    libdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
    # If using requests as a zipped library, you have to have the cacert.pem file readable
    # (which it usually wont be from within the zip file. Same problem you had with pyfiglet.)
    os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(libdir, "cacert.pem")
    sys.path.insert(0, os.path.join(libdir, "requests.zip"))
    #sys.path.insert(0, os.path.join(libdir, "requests"))
    import requests


## Local imports
from .sublime_utils import *


def get_endpoint_url(endpoint, baseurl=None):
    if baseurl is None:
        settings = get_settings()
        baseurl = settings.get("autoremote_baseurl", "https://autoremotejoaomgcd.appspot.com/")
    url = urljoin(baseurl, endpoint)
    return url

def get_params(target=None, sender=None, password=None, device=None,
               ttl=None, collapseKey=None, key=None, existingparams=None):
    settings = get_settings()
    if target is None:
        target = settings.get("autoremote_devices", {}).get(device, {}).get("target")
    if password is None:
        password = settings.get("autoremote_devices", {}).get(device, {}).get("password")
    if sender is None:
        sender = settings.get("autoremote_default_sender")
    if ttl is None:
        ttl = settings.get("autoremote_default_ttl")
    if key is None:
        key = settings.get("autoremote_key")
    loca = locals()
    params = {v: loca[v]
              for v in ("target", "password", "sender", "ttl", "key", "collapseKey")
              if loca[v] is not None}
    if existingparams is not None:
        params.update(existingparams)
    return params

def send_message(message, target=None, sender=None, password=None, device=None,
                 ttl=None, collapseKey=None,
                 key=None, baseurl=None):
    s = requests.Session()
    endpoint = get_endpoint_url("sendmessage", baseurl)
    params = get_params(target=target, sender=sender, password=password, device=device,
                        ttl=ttl, collapseKey=collapseKey, key=key)
    params["message"] = message
    r = s.get(endpoint, params=params)
    return r

def send_intent(intent, device=None, key=None, baseurl=None):
    endpoint = get_endpoint_url("sendintent", baseurl)
    params = get_params(key=key)
    params["intent"] = intent
    r = requests.get(endpoint, params=params)
    return r

def send_notification(message, params, key=None, baseurl=None):
    """
    params can include any of text, sound, vibration, url, id, and many more...
    """
    endpoint = get_endpoint_url("sendnotification", baseurl)
    params = get_params(key=key)
    if message is not None:
        # message (action) might not be required when sending notifications.
        params["message"] = message
    r = requests.get(endpoint, params=params)
    return r

def get_key_from_url(url):
    """
    Get key, querying and parsing the url.
    This is useful to get key from the typical goo.gl/<short-key> url.
    """
    # make a request to the url, in case url is the goo.gl/<short-key> thing
    r = requests.get(url)
    key = parse_qs(urlparse(r.url).query)["key"]
    if isinstance(key, list):
        key = key.pop()
    return key
