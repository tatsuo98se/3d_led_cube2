# -*- coding:utf-8 -*-
import socket

host = "localhost"
port = 20000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect((host, port)) 

while True:
    print ('何か文字を入力してください。')
    input_word = raw_input('>>>  ')
    print (input_word)
    client.send(input_word + "\n") 

