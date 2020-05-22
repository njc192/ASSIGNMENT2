
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
sent_count = 0; # No. of messages sent. Updated immediately after sending.
total_time = 0 # Sum of RTTs used to calculate average RTT at the end
alpha = 0.125 # Used in estimated rtt calculation
estimated_rtt = 0 # Estimated RTT used for dev_rtt & setting the timeout interval
beta = 0.25 # Used in dev rtt calculation
dev_rtt = 0 # Estimated RTT deviation used for setting the timeout interval
timeout_interval = 2.0 # Sets the initial timeout to about 2 seconds
last_packet_lost = False; # Stores whether last packet was lost. Used for Dev RTT

# Calculates RTT based on sent and received times
def calc_rtt(time_start, time_end):
   return (1000*(time_end - time_start))

# Update the running total sum of RTT so far
def add_to_avg(rtt, total_time):
   total_time += rtt
   return total_time

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
def handle_dev_rtt(dev_rtt, estimated_rtt, sample_rtt, last_packet_lost, sent_count):
   beta = 0.25
   # If the last packet was lost, keep the dev_rtt the same
   if last_packet_lost:
      return dev_rtt
   # If last response received is to the 1st msg we sent, set default value
   if (sent_count == 1): 
      dev_rtt = rtt / 2;
   else:
      # calc dev rtt
      dev_rtt = (1 - beta) * dev_rtt + beta * abs(sample_rtt - estimated_rtt)
   return dev_rtt

# Calculate a new timeout interval and return it
def update_timeout_interval(estimated_rtt, dev_rtt):
   timeout_interval = estimated_rtt + 4 * dev_rtt
   return timeout_interval

# Begin sending and receiving messages
for x in range(0, 10):
   clientSocket.settimeout(timeout_interval) # Times out at 2 seconds.
   message = "Ping" + str(x + 1) # Creates application layer message


   # Creates transport layer packet while sending to the server
   clientSocket.sendto(message.encode(),(serverName, serverPort))
   
   # Record the time the message was sent
   time_start = time.time()
   
   sent_count = sent_count + 1
   print("Mesg sent : " + message)

   try:
      # Receive the server packet along with the address it is coming from
      # Application layer message gets separated from transport layer packet.
      modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
      time_end = time.time()
      counter +=1
      last_packet_lost = False

      print("Mesg rcvd: " + modifiedMessage.decode())
      print("Start time: " + str(time_start))
      print("Return time: ",str(time_end))
      received_count = received_count + 1
      rtt = calc_rtt(time_start, time_end) 
      add_to_avg(rtt, total_time)
      estimated_rtt = handle_estimated_rtt(received_count, estimated_rtt, rtt)
      dev_rtt = handle_dev_rtt(dev_rtt, estimated_rtt, rtt, last_packet_lost, sent_count)
      timeout_interval = update_timeout_interval(estimated_rtt, dev_rtt)
      print("PONG " + str(x + 1) + " RTT: " +  str(rtt) + " ms")
      
      print("Estimated RTT: " + str(estimated_rtt) + " ms")
      print("Estimated RTT deviation: " + str(dev_rtt) + " ms")
      print("New timout interval: " + str(timeout_interval) + " ms")

      # Handle min and max
      if rtt > rtt_max:
          rtt_max = rtt
      if rtt < rtt_min:
          rtt_min = rtt 

   except timeout:
       # Packet was lost.
       last_packet_lost = True;
       print("No Mesg rcvd \nPONG " + str(x + 1) + " Request Timed out")
   
   print("")

# The client closes the socket when all pings are done.
clientSocket.close()

avg = float(total_time)/received_count

print("Min RTT:         " + str(rtt_min) + " ms")
print("Max RTT:         " + str(rtt_max) + " ms")
print("Avg RTT:         " + str(avg) + " ms")
print("Packet Loss:     " + str(100.0 - received_count / sent_count * 100) + "%");
print("Estimated RTT:   " + str(estimated_rtt) + " ms")
print("Dev RTT:         " + str(dev_rtt) + " ms")
print("Timeout Interval:" + str(timeout_interval) + " ms")

