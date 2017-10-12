# -*- coding:utf-8 -*-
import socket

host = "localhost"
port = 20000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect((host, port)) 

while True:
    print ('Please input orders to show led contents.')
    input_word = raw_input('>>>  ')
    print (input_word)
    client.send(input_word + "\n") 

