# UDPPingerClient.py
# we need to implement the client program

from socket import *
import os

serverName = 'localhost'
serverPort = 12000

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence: ')
clientSocket.sendto(str.encode(message), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
print(bytes.decode(modifiedMessage))

clientSocket.close()
