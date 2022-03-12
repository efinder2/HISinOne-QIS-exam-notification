import smtplib
import ssl
from enum import Enum

import requests


class ConsoleOutputMode(Enum):
    NONE = 0
    PRETTY_CHANGES = 1
    JSON_ALL = 2


class Notifier:
    mailSSLPort = 465
    mailSmtpHost = ''
    mailLoginUser = ''
    mailLoginPassword = ''
    mailSenderMail = ''
    mailReceiverMail = ''

    telegramBotToken = ''
    telegramChatId = ''

    consoleOutputMode = ConsoleOutputMode.NONE

    def enableMailNotifications(self, port, smtpHost, user, password, senderMail, receiverMail):
        self.mailSSLPort = port
        self.mailSmtpHost = smtpHost
        self.mailLoginUser = user
        self.mailLoginPassword = password
        self.mailSenderMail = senderMail
        self.mailReceiverMail = receiverMail

    def enableTelegramNotifications(self, botToken, chatId):
        self.telegramBotToken = botToken
        self.telegramChatId = chatId

    def setConsoleOutputMode(self, mode: ConsoleOutputMode):
        self.consoleOutputMode = mode

    def notify(self, message, noten):
        if self.consoleOutputMode == ConsoleOutputMode.JSON_ALL:
            print(noten)
        elif self.consoleOutputMode == ConsoleOutputMode.PRETTY_CHANGES:
            print(message)

        if self.mailSmtpHost != '':
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(self.mailSmtpHost, self.mailSSLPort, context=context) as server:
                server.login(self.mailLoginUser, self.mailLoginPassword)
                server.sendmail(self.mailSenderMail, self.mailReceiverMail, message)

        if self.telegramChatId != '':
            send_text = 'https://api.telegram.org/bot' + self.telegramBotToken + '/sendMessage?chat_id=' \
                        + self.telegramChatId + '&parse_mode=Markdown&text=' + message
            requests.get(send_text)
