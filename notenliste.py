import hashlib
import os.path
from pathlib import Path

import lxml.html as lh

from configuration import Configuration
from notifier import Notifier


def parseFromHTML(content):
    doc = lh.fromstring(content)
    table_elements = doc.xpath('//table')
    stammdaten_table = table_elements[0]
    notenuebersicht_table = table_elements[1]

    abschluss = ''
    fach = ''

    for tr in stammdaten_table:
        if "Abschluss</th>" in str(lh.tostring(tr)):
            for td in tr:
                text = str(td.text.replace("\\t", "").replace("\\r", "").replace("\\n", "").strip())
                abschluss = text
        if "Fach</th>" in str(lh.tostring(tr)):
            for td in tr:
                text = str(td.text.replace("\\t", "").replace("\\r", "").replace("\\n", "").strip())
                fach = text

    studiengang = abschluss + " - " + fach
    noten = {}

    for tr in notenuebersicht_table:
        if "qis_kontoOnTop" in str(lh.tostring(tr)) or "tabelleheader" in str(lh.tostring(tr)):
            continue

        i = 0
        pruefungsnr = 0
        pruefungstext = 0
        note = 0
        status = 0
        credits = 0
        versuch = 0
        datum = ''

        for td in tr:
            text = str(td.text.replace("\\t", "").replace("\\r", "").replace("\\n", "").strip())

            i = i + 1
            if i == 1:
                pruefungsnr = text
            if i == 2:
                pruefungstext = text
            if i == 3:
                note = text
            if i == 4:
                status = text
            if i == 5:
                credits = text
            if i == 6:
                versuch = text
            if i == 7:
                datum = text

        noten[pruefungsnr] = {
            'pruefungstext': pruefungstext,
            'note': note,
            'status': status,
            'credits': credits,
            'versuch': versuch,
            'datum': datum
        }

    return [noten, studiengang]


def processList(noten, studiengang, notifier: Notifier, config: Configuration):
    stateFile = config.getDefault('stateFile')
    subject = "Neuer Pruefungsstatus fuer '" + studiengang + "'"
    message = ''
    changes = 0

    for pruefungsnr in noten:
        toHash = pruefungsnr + noten[pruefungsnr]["status"]
        hash = hashlib.md5(toHash.encode("UTF-8")).hexdigest()

        knownHashes = []
        if os.path.exists(stateFile):
            knownHashes = Path(stateFile).read_text()
            f = open(stateFile, 'a+')
        else:
            f = open(stateFile, 'w')

        if hash not in knownHashes:
            changes += 1
            f.write(hash + "\n")

            message += "\n\n" + \
                       "\nModul: " + noten[pruefungsnr]["pruefungstext"] + \
                       "\nPruefungsnummer: " + pruefungsnr + \
                       "\nStatus: " + noten[pruefungsnr]["status"] + \
                       "\nNote: " + noten[pruefungsnr]["note"] + \
                       "\nVersuch: " + noten[pruefungsnr]["versuch"] + \
                       "\nDatum: " + noten[pruefungsnr]["datum"]
        f.close()

    # remove non-ascii characters
    message = message.encode('ascii', 'ignore').decode('ascii')
    subject = subject.encode('ascii', 'ignore').decode('ascii')

    if changes > 0:
        notifier.notify(message, subject, noten)
