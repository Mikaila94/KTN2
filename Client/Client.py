# -*- coding: utf-8 -*-
import socket
import re
import json
from MessageReceiver import MessageReceiver

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        self.messageReceiver = MessageReceiver(self,self.connection)
        self.run()

        
        

    
    

        # TODO: Finish init process with necessary code

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.messageReceiver.start()
        print 'Welcome to this chatting room! Start chatting by using command login <username>'
        while True:
            input = raw_input('>')
            self.send_payload(input)


    
    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.disconnect()

    def receive_message(self, message):
        # TODO: Handle incoming message1
        print (message)


    def send_payload(self, data):
        # TODO: Handle sending of a payload
        stringarray = data.split(' ')
        content = ""
        for i in range(1, len(stringarray)):
            content += stringarray[i]
            content += ' '
        data = {'request':stringarray[0],'content':content}
        
        self.connection.sendall(json.dumps(data))



if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
