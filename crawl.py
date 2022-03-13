#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import urllib.parse as urlparse
from urllib.parse import parse_qs

import requests
from bs4 import BeautifulSoup

import notenliste
from configuration import Configuration
from notifier import Notifier

config = Configuration()
config.load()

if config.getDefault('icmsUsername') == '' or config.getDefault('icmsPassword') == '':
    print("Die Konfiguration von Benutzername und Passwort ist notwendig!")
    sys.exit(1)

if config.getDefault('stateFile') == '':
    print("Die Konfiguration des 'stateFile' ist notwendig!")
    sys.exit(1)

customNotifier = Notifier(config)

payload = {
    "asdf": config.getDefault('icmsUsername'),
    "fdsa": config.getDefault('icmsPassword'),
    "name": "submit"
}

session_requests = requests.session()
session_requests.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})

login_url = config.getDefault('icmsServerPart') + "/qisserver/rds?state=user&type=0"
if config.verbose:
    print("Rufe Startseite auf")
result = session_requests.get(login_url)

# login...
if config.verbose:
    print("Einloggen...")
url_loginPost = config.getDefault('icmsServerPart') + "/qisserver/rds?state=user&type=1&category=auth.login&startpage=portal.vm"
result = session_requests.post(
    url_loginPost,
    data=payload
)

resultContainingAsi = session_requests.get(
    config.getDefault(
        'icmsServerPart') + "/qisserver/rds?state=redirect&sso=qisstu&myre=state%253Duser%2526type%253D0%2526htmlBodyOnly%253Dtrue%2526topitem%253Dfunctions%2526language%253Dde")

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

if config.verbose:
    print("Rufe Notenspiegel Auswahl Seite auf...")
result = session_requests.get(
    config.getDefault(
        'icmsQisposServerPart') + "/qisserver/rds?state=notenspiegelStudent&next=tree.vm&nextdir=qispos/notenspiegel/student&navigationPosition=functions%2CnotenspiegelStudent&breadcrumb=notenspiegel&topitem=functions&subitem=notenspiegelStudent&asi=" + asi)

soup = BeautifulSoup(str(result.content), 'html.parser')
for link in soup.find_all('a'):
    parsed = urlparse.urlparse(link.get('href'))
    params = parse_qs(parsed.query)
    if "struct" in params and params.get("struct")[0] == "auswahlBaum":
        if config.verbose:
            print("Rufe Notenuebersicht Seite auf...")
        result = session_requests.get(
            link.get('href'),
            headers=dict(referer=config.getDefault('icmsServerPart') + "/qisserver/rds?state=sitemap&topitem=leer&breadCrumbSource=portal")
        )

        [noten, studiengang] = notenliste.parseFromHTML(str(result.content))
        notenliste.processList(noten, studiengang, customNotifier, config)
