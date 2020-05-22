from socket import *

import time

serverName = 'localhost'
serverPort = 12000

rtt_max = 0 #zero is okay because we cannot have a negative time
rtt_min = float("inf")
estimated_rtt =0
dev_rtt =0

timeout_interval = 2.0

time_start = 0
time_end = 0

average = 0
receieved_count = 0

clientSocket = socket(AF_INET,SOCK_DGRAM)
total_time = 0

alpha = 0.125
beta = 0.25

def calc_rtt(time_start, time_end):
    return (1000*(time_end-time_start))

def add_to_avg(rtt,total_time):
    total_time += rtt
    return total_time

def handle_estimated_rtt(received_count,estimated_rtt,sample_rtt):
    if(received_count ==1):
        estimated_rtt = sample_rtt

    estimated_rtt = (1-alpha) * estimated_rtt + (alpha*sample_rtt)
    return estimated_rtt


def handle_dev_rtt(received_count, dev_rtt, estimated_rtt, sample_rtt):
    if(receieved_count == 1):
        dev_rtt = sample_rtt/2 #should this be sample_rtt
    dev_rtt = (1-alpha)*estimated_rtt + (alpha*sample_rtt)
    return dev_rtt


def update_timeout_interval(estimated_rtt,dev_rtt):
    timeout_interval = estimated_rtt + 4*dev_rtt
    return timeout_interval

def min(rtt):
    if(rtt < rtt_min):
        return rtt
    return rtt_min

def max(rtt):
    if(rtt > rtt_max):
        return rtt
    return rtt_max


for x in range(0,10):
    clientSocket.settimeout(timeout_interval)
    message = "Ping" + str(x+1)



    time_start = time.time()

    clientSocket.sendto(message.encode(),(serverName,serverPort))

    print("Message sent: " + message)

    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        receieved_count +=1

        time_end = time.time()

        print("Message received: " + modifiedMessage.decode() + "\n")
        print("Sent:" + str(time_start) + "\t" +"Received" + str(time_end))
        rtt = calc_rtt(time_start,time_end)
        total_time = add_to_avg(rtt,total_time)
        print("!!!! total time is: " + str(total_time))
        estimated_rtt = handle_estimated_rtt(receieved_count, estimated_rtt, rtt)
        dev_rtt = handle_dev_rtt(receieved_count,dev_rtt, estimated_rtt,rtt)
        timeout_interval = update_timeout_interval(estimated_rtt,dev_rtt)

        rtt_min = min(rtt)
        rtt_max = max(rtt)

        print("RTT:" + str(rtt))
        print("Estimated RTT:" + str(estimated_rtt))
        print("Dev RTT:" + str(dev_rtt))
        print("New timeout interval:" + str(timeout_interval))
        print()

    except timeout:
        print("No message was recevied :(" + " PONG " + str(x+1) + "request timed out")


clientSocket.close()
print("counter" + str(receieved_count))
print("sum " + str(total_time))
average = float(total_time)/receieved_count

print("Average: " + str(average))
print("min rtt was : " + str(rtt_min))
print("max rtt was : " + str(rtt_max))
