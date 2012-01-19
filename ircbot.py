# encoding: utf-8
"""
ircbot.py

Created by TheDude on 2006-08-23.
Copyright (c) 2006 Netgarage. All rights reserved.
"""

import socket
import select

class IrcBot:
    ''' quick'n'dirty generic irc bot class. overwrite self.notify() for stuff you want to do everytime
        select() returns. overwrite self.handle_message() to react to pre-parsed irc messages '''
        
    def __init__(self, host, port, channel, nick, password='', select_timeout=30.0):                 
        self.host           = host
        self.port           = port
        self.nick           = nick
        self.password       = password
        self.channel        = channel
        self.select_timeout = select_timeout
        self.sock           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_msg_len    = 512   # according to rfc 1459, irc messages have a max. length of 512 bytes
    
        
    def login(self):
        self.sock.connect((self.host, self.port))
        self.send('NICK ' + self.nick + '\r\n')
        self.send('USER ' + self.nick + ' 0 * :' + self.nick + '\r\n')

        if self.password != '':
            self.send('NickServ IDENTIFY ' + password)
        
        # command = ''
        # while command != '376':
        #     msg = self.receive()
        #     prefix, command, arguments = self.parse_message(msg)
        self.send('JOIN ' + self.channel + '\r\n')
        self.run()
    
      
    def run(self):
        while True:
            ready_to_read, ready_to_write, in_error = select.select([self.sock], [], [], self.select_timeout)
            self.notify()
            if self.sock in ready_to_read:
                msg = self.receive()
                if msg[:5] == 'PING ':
                    self.send('PONG ' + msg[6:] + '\r\n')
                else:
                    prefix, command, arguments = self.parse_message(msg)
                    self.handle_message(prefix, command, arguments)
    
    
    def receive(self):
        ''' socket.recv() is called in a loop until a complete irc message has been received (\r\n terminated) '''
        
        msg = ''
        while (len(msg) < self.max_msg_len) and (msg[-2:] != '\r\n'):
            chunk = self.sock.recv(self.max_msg_len-len(msg))
            if chunk == '':     # if the message is not complete yet and there's no more data left
                msg += '\r\n'   # something went wrong. let handle_message() take care of it...
            else:
                msg += chunk
            
        return msg
    
    
    def send(self, msg):
        ''' this function only sends its argument in a loop. no care is taken to send messages of at most
            self.max_msg_len length and with proper termination. this is done in self.say(). '''
            
        total_sent = 0
        while total_sent < len(msg):
            sent = self.sock.send(msg[total_sent:])
            if sent == 0:       # we really should do error handling here, 
                break           # the socket broke in some way
            total_sent += sent
    
    
    def say(self, msg):
        ''' this function splits a message of arbitrary length into n PRIVMSGs 
            less or equal to self.max_msg_len characters long and appends \r\n '''
            
        privmsgs        = []
        privmsg_prefix  = 'PRIVMSG ' + self.channel + ' :'
        max_payload_len = self.max_msg_len - len(privmsg_prefix) - len('\r\n')
        msg_offset      = 0
        remaining_msg   = len(msg)
        
        while remaining_msg > 0:
            tmp_msg        = privmsg_prefix + msg[msg_offset:max_payload_len]
            remaining_msg -= len(tmp_msg)
            msg_offset    += len(tmp_msg)
            self.send(tmp_msg + '\r\n')
    
    
    # ripped from twised matrix code (words/protocols/irc.py)
    def parse_message(self, msg):
        ''' Breaks a message from an IRC server into its prefix, command, and arguments. '''
        
        prefix   = ''
        trailing = []
        if not msg:
            return '', '', []
        if msg[0] == ':':
            prefix, msg = msg[1:].split(' ', 1)
        if msg.find(' :') != -1:
            msg, trailing = msg.split(' :', 1)
            args = msg.split()
            args.append(trailing)
        else:
            args = msg.split()
        command = args.pop(0)
        return prefix, command, args
    
        
    
    def notify(self):
        pass
    
    # parameters are: string, string, list
    def handle_message(self, prefix, command, arguments):
        pass
