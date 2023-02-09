#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

"""
Documentation of the REFERENCES Used:
I understood and learnt the conecept of parsing the input URL through urlparse to obtain the Host, Port and Path
and understood how to convert the argumenst present in the form of a dictiinary into a query string thorugh urlencode
from this resource: Author: Python Software Foundation, Date: Feb 09, 2023 (last update), Title: "urllib.parse — Parse URLs into components", Online Resource:https://docs.python.org/3/library/urllib.parse.html
I applied my understanding from the above website into writing the code.
"""
import sys
import socket
import re
# you may use urllib to encode data appropriately
# importing the necessary libraries from the urllib.parse that are useful in my code
from urllib.parse import urlparse
from urllib.parse import urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):
    
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # Initialising an int variable for the Content length
        i = 0
        # parsing the url recieved in the function to obtain path, Host Name and the Port Number
        main_url = urlparse(url)
        # obtaining the path of the main url
        main_path = main_url.path
        # if the path is missing in the main URL
        if (main_path == ""):
            # adding the default path
            main_path = "/"

        # obtaining the Host name of the main url
        main_host = main_url.hostname
        # obtaining the Port Number of the main url
        main_port = main_url.port
        # if the port field is empty in the main url
        if (main_port == None):
            # set the port to the default port of HTTP
            main_port = 80

        # connecting to the socket
        self.connect(main_host, main_port)
        # creating the message request that will be sent via the sendall() function
        main_message = "GET {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: Safari\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\nConnection: close\r\n\r\n[]".format(main_path, main_host, i)
        # sending the message created above via the sendall() function
        self.sendall(main_message)
        main_socket = self.socket
        # obtaining the message recieved from the server
        recv_message = self.recvall(main_socket)
        main_code = recv_message.split(" ")
        code = main_code[1]
        # obtaining the code from the message recieved 
        code = int (code)
        main_body = recv_message.split("\r\n\r\n")
        # obtaining the body from the message recieved 
        body = main_body[-1]
        # closing the socket that we connected above
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # Initialising an int variable for the Content length
        i = 0
        # parsing the url recieved in the function to obtain path, Host Name and the Port Number
        main_url = urlparse(url)
        # obtaining the path of the main url
        main_path = main_url.path
        # if the path is missing in the main URL
        if (main_path == ""):
            main_path = "/"

        # obtaining the Host name of the main url
        main_host = main_url.hostname
        # obtaining the Port Number of the main url
        main_port = main_url.port
        # if the port field is empty in the main url
        if (main_port == None):
            # set the port to the default port of HTTP
            main_port = 80
        
        # connecting to the socket
        self.connect(main_host, main_port)
        # if the message does not have any arguments
        if (args == None):
            # Since there are no argumentsm it is almost similar to a GET request
            # creating the message request that will be sent via the sendall() function
            # Since there are no arguments, sending an empty array with a 0 content length
            main_message = "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: Safari\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\nConnection: close\r\n\r\n[]".format(main_path, main_host, i)
        # if the message does have any arguments
        else:
            # converting the arguments present in the form of a dictionary into a query string
            # converting the arguments into 
            main_argument = urlencode(args)
            # computing the length of the arguments, which can be further sent as the content legth
            main_size = len(main_argument)
            # creating the message request that will be sent via the sendall() function
            main_message = "POST {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: Safari\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}".format(main_path, main_host, main_size, main_argument)
        
        # sending the message created above via the sendall() function
        self.sendall(main_message)
        main_socket = self.socket
        # obtaining the message recieved from the server
        recv_message = self.recvall(main_socket)
        main_code = recv_message.split(" ")
        code = main_code[1]
        # obtaining the code from the message recieved 
        code = int (code)
        main_body = recv_message.split("\r\n\r\n")
        # obtaining the body from the message recieved 
        body = main_body[-1]
        # closing the socket that we connected above
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
