# UDPPingerClient.py
# Weiran Guo(912916431)
# we need to implement the client program

from socket import *
import os
import datetime
import signal
import time

serverName = 'localhost'
serverPort = 12000

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
def abbrev(x):
    return{
        0: 'M',
        1: 'T',
        2: 'W',
        3: 'R',
        4: 'F',
        5: 'S',
        6: 'U'}.get(x)
        
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

#Try 10 times
for i in range(1,10):
    timeStart = time.clock()
    start = datetime.datetime.now()
    message = 'Ping ' + str(i) + ' ' + start.strftime("%Y-%m-%d") + ' ' + abbrev(start.weekday()) + ' ' + start.strftime("%H:%M") + ' PCT'
    try:
        clientSocket.sendto(str.encode(message), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        end = datetime.datetime.now()
        RTT = (time.clock() - timeStart) * 1000
        print(message)
        modifiedMessage = modifiedMessage.decode()
        print(modifiedMessage)
        print("RTT: %.3f\n" % RTT)
    except:
        print(message)
        print("Request time out\n")
 

clientSocket.close()
