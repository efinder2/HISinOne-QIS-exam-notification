#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import urllib.parse as urlparse
from urllib.parse import parse_qs

import requests
from bs4 import BeautifulSoup

import notenliste
from notifier import Notifier, ConsoleOutputMode

customNotifier = Notifier()

# configure here:

customNotifier.setConsoleOutputMode(ConsoleOutputMode.PRETTY_CHANGES)
# customNotifier.enableTelegramNotifications('****replace_with_bot_token****', '****replace_with_chat_id****')
# customNotifier.enableMailNotifications(465, 'smtp.example.com', 'myuser@example.com', 'mypasswd1234',
#                                        'sendermail@example.com', 'receiver@example.com')

icms_username = '********'
icms_password = '********'
icms_server_part = 'https://horstl.hs-fulda.de'
icms_qispos_server_part = 'https://qispos.hs-fulda.de'

verboseMode = False

###############################


payload = {
    "asdf": icms_username,
    "fdsa": icms_password,
    "name": "submit"
}

session_requests = requests.session()
session_requests.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})

login_url = icms_server_part + "/qisserver/rds?state=user&type=0"
if verboseMode:
    print("Rufe Startseite auf")
result = session_requests.get(login_url)

# login...
if verboseMode:
    print("Einloggen...")
url_loginPost = icms_server_part + "/qisserver/rds?state=user&type=1&category=auth.login&startpage=portal.vm"
result = session_requests.post(
    url_loginPost,
    data=payload
)

resultContainingAsi = session_requests.get(
    icms_server_part + "/qisserver/rds?state=redirect&sso=qisstu&myre=state%253Duser%2526type%253D0%2526htmlBodyOnly%253Dtrue%2526topitem%253Dfunctions%2526language%253Dde")

# Extract SessionID
asi = None

soup = BeautifulSoup(str(resultContainingAsi.content), 'html.parser')
for link in soup.find_all('a'):
    parsed = urlparse.urlparse(link.get('href'))
    params = parse_qs(parsed.query)
    if "asi" in params:
        asi = params.get("asi")[0]

if asi is None:
    print("SessionID couldn't be extracted")
    sys.exit()

if verboseMode:
    print("Rufe Notenspiegel Auswahl Seite auf...")
result = session_requests.get(
    icms_qispos_server_part + "/qisserver/rds?state=notenspiegelStudent&next=tree.vm&nextdir=qispos/notenspiegel/student&navigationPosition=functions%2CnotenspiegelStudent&breadcrumb=notenspiegel&topitem=functions&subitem=notenspiegelStudent&asi=" + asi)

soup = BeautifulSoup(str(result.content), 'html.parser')
for link in soup.find_all('a'):
    parsed = urlparse.urlparse(link.get('href'))
    params = parse_qs(parsed.query)
    if "struct" in params and params.get("struct")[0] == "auswahlBaum":
        if verboseMode:
            print("Rufe Notenuebersicht Seite auf...")
        result = session_requests.get(
            link.get('href'),
            headers=dict(referer=icms_server_part + "/qisserver/rds?state=sitemap&topitem=leer&breadCrumbSource=portal")
        )

        [noten, studiengang] = notenliste.parseFromHTML(str(result.content))
        notenliste.processList(noten, studiengang, customNotifier)
