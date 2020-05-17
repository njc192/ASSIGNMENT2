''' UDPClient.py
 Programming Assignment 2: UDP Pinger
 Team 7: Central Coast Programming Consultants
 Team Members: Nick D'Orazio
               Christal O'Connell
               Nate Carrasco
               Kyle Oakes
 Date last modified: Friday, May 15th, 2020
 Program Description: This program is used in collaboration with UDPServer.py.
               Together they demonstrate a client pinging a server using the User Datagram Protocol (UDP).
'''

from socket import *
import time
# Client needs the name and port of the server to send packets.
serverName = 'localhost'
serverPort = 12000
time_difference = 0
# Creates a UDP socket.
clientSocket = socket(AF_INET, SOCK_DGRAM)

for x in range(0, 10):
   clientSocket.settimeout(2.0) # Times out at 2 seconds.
   message = "Ping" + str(x + 1) # Creates application layer message
   # Creates transport layer packet while sending to the server


   #starting_time is the time the message was sent
   time_start = time.time()
   clientSocket.sendto(message.encode(),(serverName, serverPort))
   print("Mesg sent: " + message)


   try:
      # Receive the server packet along with the address it is coming from
      # Application layer message gets separated from transport layer packet.
      
      modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
      time_end = time.time()

      print("Mesg rcvd: " + modifiedMessage.decode() + "\n")
      print("sent at: ", time_start)
      print("received at: ",time_end)
      print("PONG" + str(x+1) + " " +   str(time_end - time_start))
      print("")

   except timeout:
       # Packet was lost.
       print("No Mesg rcvd \nPONG " + str(x + 1) + " Request Timed out\n")

# The client closes the socket when all pings are done.
clientSocket.close()


