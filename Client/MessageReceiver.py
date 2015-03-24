# -*- coding: utf-8 -*-
from threading import Thread
import json

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and permits
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        super(MessageReceiver, self).__init__()
        
        
        # Flag to run thread as a deamon
        self.daemon = True
        self.client = client
        self.connection = connection

        # TODO: Finish initialization of MessageReceiver

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            try:
                message = json.loads(self.connection.recv(1024))
                message1 = message['timestamp']
                message2 = message['username']
                message3 = message['message']
                message4 = message['content']
                newMessage = message1 + ' '+ message2 + ' '  + message3 + ' ' + message4
                self.client.receive_message(newMessage)
            except ValueError:
                print "There is a value error!"



