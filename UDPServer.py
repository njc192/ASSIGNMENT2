''' UDPServer.py
 Programming Assignment 2: UDP Pinger
 Team 7: Central Coast Programming Consultants
 Team Members: Nick D'Orazio
               Christal O'Connell
               Nate Carrasco
               Kyle Oakes
 Date last modified: Friday, May 15th, 2020
 Program Description: This program is used in collaboration with UDPClient.py.
               Together they demonstrate a client pinging a server using the User Datagram Protocol (UDP).
'''

import random
from socket import *

serverPort = 12000
pingNum = 0  # A ping counter.
# Creates a UDP socket.
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket.
serverSocket.bind(('', serverPort))

# Server is now listening on the socket for incoming packets.
print('Waiting for Client...\n')
while True:
   # Generates a random number in the range of 0 to 10 to determine which packets get lost.
   rand = random.randint(0, 10)
   # Receive the client packet along with the address it is coming from
   # Application layer message gets separated from transport layer packet.
   message, address = serverSocket.recvfrom(1024)
   modifiedMessage = message.decode().upper()

   # If rand is greater than or equal to 4 the packet was received.
   if rand >= 4:
      pingNum += 1
      print("Ping" + str(pingNum) + " Received")
      print("Mesg rcvd: " + message)
   # If rand is less than 4, we consider the packet lost and do not respond. Represents a 30% drop rate.
   else:
      print("\nPacket was lost.\n\n")
      continue

   # Otherwise, the server responds by creating a transport layer packet while sending to the client.
   serverSocket.sendto(modifiedMessage.encode(), address)
   print("Mesg sent: " + modifiedMessage + "\n")
