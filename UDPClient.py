
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
# Variables used in calculations
received_count = 0 # No. of reponses received. Updated immediately on new response
total_time = 0 # Sum of RTTs used to calculate average RTT at the end
alpha = 0.125 # Used in estimated rtt calculation
estimated_rtt = 0 # Estimated RTT used for dev_rtt & setting the timeout interval
beta = 0.25 # Used in dev rtt calculation
dev_rtt = 0 # Estimated RTT deviation used for setting the timeout interval
timeout_interval = 2.0 # Sets the initial timeout to about 2 seconds

# Calculates RTT based on sent and received times
def calc_rtt(time_start, time_end):
   return (1000*(time_end - time_start))

# Update the running total sum of RTT so far
def add_to_avg(rtt, total_time):
   total_time += rtt

# Calculate and return Estimated RTT
def handle_estimated_rtt(received_count, estimated_rtt, sample_rtt):
   alpha = 0.125
   # If this is the first response we've received (assumes received_count has 
   #  been incremented for the first response), then set default values
   if (received_count == 1): 
      estimated_rtt = sample_rtt;
   # Calc estimated rtt
   estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
   return estimated_rtt

# Calculate and return Estimated RTT Deviation
def handle_dev_rtt(received_count, dev_rtt, estimated_rtt, sample_rtt):
   beta = 0.25
   # If this is the first response we've received (assumes received_count has 
   #  been incremented for the first response), then set default values
   if (received_count == 1): 
      dev_rtt = rtt / 2;
   # calc dev rtt
   dev_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
   return dev_rtt

# Calculate a new timeout interval and return it
def update_timeout_interval(estimated_rtt, dev_rtt):
   timeout_interval = estimated_rtt + 4 * dev_rtt
   return timeout_interval

# Begin sending and receiving messages
for x in range(0, 10):
   clientSocket.settimeout(timeout_interval) # Times out at 2 seconds.
   message = "Ping" + str(x + 1) # Creates application layer message


   #starting_time is the time the message was sent

   time_start = time.time()
   # Creates transport layer packet while sending to the server
   clientSocket.sendto(message.encode(),(serverName, serverPort))

   print("Mesg sent : " + message)


   try:
      # Receive the server packet along with the address it is coming from
      # Application layer message gets separated from transport layer packet.
      modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
      counter +=1
      time_end = time.time()


      print("Mesg rcvd: " + modifiedMessage.decode() + "\n")
      print("Sent at: ", time_start)
      print("Received at: ",time_end)
      received_count = received_count + 1
      rtt = calc_rtt(time_start, time_end) 
      add_to_avg(rtt, total_time)
      estimated_rtt = handle_estimated_rtt(received_count, estimated_rtt, rtt)
      dev_rtt = handle_dev_rtt(received_count, dev_rtt, estimated_rtt, rtt);
      timeout_interval = update_timeout_interval(estimated_rtt, dev_rtt)
      print("RTT: " +  str(rtt))
      print("Estimated RTT: " + str(estimated_rtt))
      print("Estimated RTT deviation: " + str(dev_rtt))
      print("New timout interval: " + str(timeout_interval))

      print("")


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

