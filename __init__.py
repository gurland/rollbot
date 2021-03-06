import logging
import re

import telebot
import botan

from data.settings import API_TOKEN1, BOTAN_KEY

OFF_CHATS = [-1001119348462]


def is_command_on(msg):
    return msg.chat.id in OFF_CHATS


# Command list handler function
def commands_handler(cmnds, inline=False, switchable=False):
    BOT_NAME = '@rollclub_bot'

    def wrapped(msg):
        if not msg.text:
            return False
        if switchable and msg.chat.id in OFF_CHATS:
            return False

        split_message = re.split(r'[^\w@\/]', msg.text)
        if not inline:
            s = split_message[0]
            result = (s in cmnds) or (s.endswith(BOT_NAME) and s.split('@')[0] in cmnds)
        else:
            result = any(cmnd in split_message or cmnd + BOT_NAME in split_message for cmnd in cmnds)

        # if result:
        #     botan.track(BOTAN_KEY, msg.chat.id, msg, cmnds[0])
        return result

    return wrapped


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(API_TOKEN1, threaded=False)
