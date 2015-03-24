# -*- coding: utf-8 -*-
import SocketServer
import json
import datetime
import time
import re

usersConnected =[]
usernames = []
messages = []


def special_match(strg, search=re.compile(r'[^a-z0-9.]').search):
    return not bool(search(strg))

def respond(username,type,message):
    response_string ={'timestamp':timeStamp(),'username':username, 'message':type , 'content':message}
    return json.dumps(response_string)

def broadcastMessage(message):
    for i in range(0,len(usersConnected)):
        usersConnected[i].connection.sendall(message)


def timeStamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = None
        self.logged_in = False
        
        # Loop that listens for messages from the client

        while True:
            received_string = self.connection.recv(1024)
            received_string = json.loads(received_string.replace('\x00','')) #Gets the JSON object

            print repr(received_string)
            
            if(received_string['request'] == 'login' and len(received_string['content']) >1 ):
                    if(self.logged_in == True):
                        self.connection.send(respond('SERVER','INFO','You are already logged in, sir'))

                    else:

                        self.logged_in = self.handleLogin(received_string['content'])
        
        
            elif(self.logged_in == True and received_string['request'] == 'logout'):
                self.connection.send(respond('SERVER','INFO','You are now logged out'))
                self.handleLogout(self.username)
            
            elif(received_string['request'] == 'names'):
                for i in range(0,len(usernames)):
                    self.connection.send(respond('SERVER','INFO',usernames[i]))
            
            elif(self.logged_in == True and received_string['request'] == 'msg'):
                message = received_string['content']
                broadcastMessage(respond(self.username,'MSG',message))
                messages.append(respond(self.username,'HISTORY',message))
            elif(received_string['request'] == 'HELP'):
                self.connection.send(respond('SERVER','INFO',self.helpUser()))
            
            else:
                self.connection.send(respond('SERVER','ERROR','Something went wrong. Please type HELP to get help.'))


    def handleLogin(self, username):
        if(not special_match(username)):
            if(username in usernames):
                self.connection.send(respond('SERVER','INFO','This username is already taken sir'))
                return False
            else:
                self.username = username
                usersConnected.append(self)
                usernames.append(username)
                for i in range(0,len(messages)):
                    self.connection.send(messages[i])
                self.connection.send(respond(username,'INFO','Successfully logged in'))
                broadcastMessage(respond('SERVER','INFO',username + 'has joined the chat'))
                return True
        else:
            self.connection.send(respond('SERVER','INFO','You can only use a-z and 0-9 as characters in your username.'))





    def handleLogout(self,username):
        try:
            self.logged_in = False
            broadcastMessage(respond('SERVER','INFO',username + 'has left the chat'))
            usernames.remove(username)
        except ValueError:
            broadcastMessage(respond('SERVER','ERROR','Not Logged in'))

    def helpUser(self):
        helpMessage = 'You can use the following commands in this chat:\n' +'login <username> - makes you login with the typed username\n' +'logout - makes you log out if you are logged in\n' +'names - gives you a list of the connected users\n' +'msg <message> - makes you send message when logged in'
        return helpMessage












class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
