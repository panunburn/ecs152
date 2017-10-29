# UDPPingerClient.py
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
        1: 'M',
        2: 'T',
        3: 'W',
        4: 'R',
        5: 'F',
        6: 'S',
        7: 'U'}.get(x)
        
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
message = 'abc'

#Try 10 times
for i in range(1,10):
    timeStart = time.clock()
    start = datetime.datetime.now()
    try:
        clientSocket.sendto(str.encode(message), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        end = datetime.datetime.now()
        RTT = (time.clock() - timeStart) * 1000
        print("Ping", i, start.strftime("%Y-%m-%d"),
              abbrev(start.weekday()),start.strftime("%H:%M"), "PCT")
        print("Ping", i, end.strftime("%Y-%m-%d"),
              abbrev(end.weekday()), end.strftime("%H:%M"), "PCT")
        print("RTT: %.3f\n" % RTT)
    except:
        print("Ping", i, start.strftime("%Y-%m-%d"),
              abbrev(start.weekday()),start.strftime("%H:%M"), "PCT")
        print("Request time out\n")
 

clientSocket.close()
