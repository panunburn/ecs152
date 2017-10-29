# UDPPingerClient.py
# we need to implement the client program

from socket import *
import os
import signal
import time

serverName = 'localhost'
serverPort = 12000

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
message = input('Input lowercase sentence: ')
#Try 10 times
for i in range(1,10):

    timeStart = time.clock()
    try:
        clientSocket.sendto(str.encode(message), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        print("Server says:", bytes.decode(modifiedMessage))
        RTT = (time.clock() - timeStart) * 1000
    except:
        print("Request time out")
 

clientSocket.close()
