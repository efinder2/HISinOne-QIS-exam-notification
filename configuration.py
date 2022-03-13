import getopt
import sys
from os import access, R_OK
from os.path import isfile

import configparser


class Configuration:
    verbose = False
    configpath = None

    sample_config = """[default]
verbose = false

# add your QisInOne / horstl login data
icmsUsername = 
icmsPassword = 
icmsServerPart = https://horstl.hs-fulda.de
icmsQisposServerPart = https://qispos.hs-fulda.de

# if mailSmtpHost is set the script tries to send you a email notification
# but all following mail config fields are required for mail support
# only ssl supported, no starttls at the moment!
mailSSLPort = 465
mailSmtpHost = 
mailLoginUser = 
mailLoginPassword = 
mailSenderMail = 
mailReceiverMail = 

# if both options are set the script tries to send you a telegram notification
telegramBotToken = 
telegramChatId = 

# consoleOutputMode: 0 = NONE; 1 = PRETTY_CHANGES; 2 = JSON_ALL
consoleOutputMode = 1

# the state file stores hashes of exams that have already been read
# the file path must be writable
stateFile = examcheck.txt
"""
    config = configparser.ConfigParser(allow_no_value=True)

    def load(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hvc:", ["help", "verbose", "config="])
        except getopt.GetoptError:
            self.print_help()
            sys.exit(2)

        self.config.read_string(self.sample_config)

        for opt, arg in opts:
            if opt in ("-c", "--config"):
                self.configpath = str(arg)
            elif opt in ("-v", "--verbose"):
                self.verbose = True

        if self.configpath is not None and self.configpath != "":
            if self.file_readable(self.configpath):
                with open(self.configpath, 'r') as configfile:
                    if self.verbose:
                        print('Lade Konfigurationsdatei "%s"' % self.configpath)
                    self.config.read_file(configfile)
            else:
                with open(self.configpath, 'w') as configfile:
                    if self.verbose:
                        print('Erstelle neue Standard Konfigurationsdatei "%s"' % self.configpath)
                    # self.config.write(configfile)
                    configfile.write(self.sample_config)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.print_help()
                sys.exit(0)
            elif opt in ("-v", "--verbose"):
                self.config['default']['verbose'] = "true"

        if self.config['default']['verbose'] in (1, "1", "true", "True", True):
            self.verbose = True
        else:
            self.verbose = False

    def getDefault(self, key):
        return self.config.get('default', key)

    def setDefault(self, key, value):
        return self.config.set('default', key, value)

    def print_help(self):
        print('Usage: python3 crawl.py')
        print('\nArguments:')
        print('-c --config <filepath>          : Path to the configuration file in the filesystem')
        print('-v --verbose                    : Enable status messages')
        print('-h --help                       : Print this help text')

    def file_readable(self, path):
        return isfile(path) and access(path, R_OK)
