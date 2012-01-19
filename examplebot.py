#!/usr/bin/env python
# encoding: utf-8
"""
bloedbot.py

Created by TheDude on 2006-08-23.
Copyright (c) 2006 Netgarage. All rights reserved.
"""

import sys
import os
from ircbot import *

class BloedBot (IrcBot):
    def handle_message(self, msg_type, msg_from_user, msg_hostmask, msg_channel, msg_argument):
        print 'handle_message(): ' + msg_type + ', ' + msg_from_user + ', ' + msg_hostmask + ', ' + msg_channel + ', ' + msg_argument
        if msg_type != 'PRIVMSG':
            return
            
        arguments = msg_argument.split()
        if arguments[0][:len(self.nick)] != self.nick:
            return
        
        command = arguments[1].upper()
        if command == 'HALLO':
            self.say('tach auch (' + msg_from_user + ', ' + msg_hostmask + ', ' + msg_channel + ')')



def main():
    bot = BloedBot('irc1.netgarage.org', 6667, '#test', 'bloedbot')
    bot.login()


if __name__ == '__main__':
    main()
