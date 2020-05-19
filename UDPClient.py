
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
rtt_max = 0
rtt_min = float("inf")
time_start = 0
time_end = 0
avg = 0
counter =0
# Creates a UDP socket.
clientSocket = socket(AF_INET, SOCK_DGRAM)

for x in range(0, 10):
   clientSocket.settimeout(2.0) # Times out at 2 seconds.
   message = "Ping" + str(x + 1) # Creates application layer message
   # Creates transport layer packet while sending to the server
   time_start = time.time()
   clientSocket.sendto(message.encode(),(serverName, serverPort))
   print("Mesg sent: " + message)

   try:
      # Receive the server packet along with the address it is coming from
      # Application layer message gets separated from transport layer packet.
      modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
      counter +=1
      time_end = time.time()
      rtt = time_end - time_start
      if rtt > rtt_max:
          rtt_max = rtt
      if rtt < rtt_min:
          rtt_min = rtt
      
      avg += rtt
      print("Mesg rcvd: " + modifiedMessage.decode())
      print("RTT:" + str(rtt) + "\n")
   except timeout:
       # Packet was lost.
       print("No Mesg rcvd \nPONG " + str(x + 1) + " Request Timed out\n")

# The client closes the socket when all pings are done.
clientSocket.close()
print("counter" + str(counter))
print("sum" + str(avg))
avg = float(avg)/counter
print("avg was : " + str(avg))
print("min rtt was : " + str(rtt_min))
print("max rtt was : " + str(rtt_max))

