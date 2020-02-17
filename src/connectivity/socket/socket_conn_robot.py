# -*- coding: utf-8 -*-


"""
 python2 -m  pip install --user SpeechRecognition
 This file should be run with Python 2

 Goals of methods which are in this file:
    -> tell out response
    -> send text recognized from Pepper to bot

  This file requires to be run with Python 2
"""
import socket
from time import sleep

from pip._vendor.distlib.compat import raw_input


class DataExchangeModule(object):
    def __init__(self, address, port, tts):
        self.data_socket = self.establish_connection(address, port)
        self.tts = tts

    def establish_connection(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            return s
        except socket.error:
            print('Error: connection to ' + host + ':' + str(port) + ' failed, reconnection...')
            sleep(1)
            return self.establish_connection(host, port)

    def send_data_and_tell_response(self, data):
        """
            send data via socket
        """
        try:
            self.data_socket.sendall(bytes(data))
            response = self.data_socket.recv(1024).decode('utf-8')
            print(response)
            # if response != '':
            # self.tell(response)
        except socket.error:
            return None

    def tell(self, text):
        """
            cause Pepper say `text`
        """
        self.tts.say(text)

    def perform_communication_with_chatbot(self):
        while True:
            # print('in loop...')
            # result_of_speech_recognition = self.speech_recognizer()
            # print("recognized:  " + result_of_speech_recognition + ";")
            user_input = raw_input('>>>')
            # send_result = None
            # while send_result is None:
            # self.send_data_and_tell_response(self.chatbot_socket, result_of_speech_recognition)
            self.send_data_and_tell_response(user_input)
            # if send_result != '':
            #     print(send_result)


DataExchangeModule('127.0.0.1', 9999, None).perform_communication_with_chatbot()
