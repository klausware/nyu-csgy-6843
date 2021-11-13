from socket import *
import os
import sys
import struct
import time
import select
import binascii
import statistics as stat
# Should use stdev

ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer



def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out."
        
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        
        ''' 
        8 bits to a byte and ICMP header is bits 160-192
        So we want the 20th byte in the IP header
        Unpack requires a buffer of 8 bytes so we grab the 20th - 28th bytes
        '''
        header = recPacket[20:28]
        timeSentHeader = recPacket[28:36]

        #Spit out contents of unpacked headers for visibility
        #print(struct.unpack("bbHHh", header))
        #print(struct.unpack("q", timeSentHeader))
        
        '''      
        bbHHh are struct unpack's format characters
        (type): b - signed char int
        (code): b - signed char int
        (checksum): H - unsigned short int
        (packetID): H - unsigned short int
        (seq): h - short int     
        We unpack the icmp header into the respective variables
        '''
        (type, code, checksum, packetID, seq) = struct.unpack("bbHHh", header)

        timeSentHeaderPadded = recPacket[28:28 + struct.calcsize("d")]
        timeSent = struct.unpack("d", timeSentHeaderPadded)[0]

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <=0:
            #print("Time left is: %s" % timeLeft)
            return "Request timed out"		
        else: 
            #print("Time sent is: %s" % timeSent)
            delay = timeReceived - timeSent
            return delay

 


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)


    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")


    # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,  	# the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    delayTimes = []
    #Calculate vars values and return them
    #vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev(stdev_var), 2))]
    #Send ping requests to a server separated by approximately one second
    for i in range(0,4):
        delay = doOnePing(dest, timeout)
        delayTimes.append(delay*1000)
        print(delay)
        time.sleep(1)  # one second
    
    print(delayTimes)
    #delayTimes = delayTimes.sort
    #print(delayTimes)
    
    packet_min = min(delayTimes)
    print("min: %i" % packet_min)
    
    packet_avg = sum(delayTimes) / len(delayTimes)
    print("avg: %i" % packet_avg) 
    
    packet_max = max(delayTimes) 
    print("max: %i" % packet_max)
    
    stdev_var = stat.stdev(delayTimes)
    print("stddev = %i" % stdev_var)
    
    vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev_var, 2))]  
    
    return vars

if __name__ == '__main__':
    ping("google.co.il")
    #ping("127.0.0.1")
    #ping("google.com")
    #ping("no.no.e")
