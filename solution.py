from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
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

def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    # Code copied from Pinger lab skeleton solution.py pretty much verbatim
    ID = os.getpid() & 0xFFFF
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)

    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    tracelist1 = [] #This is your list to use when iterating through each trace 
    tracelist2 = [] #This is your list to contain all traces

    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                #print(whatReady)
                howLongInSelect = (time.time() - startedSelect)
                if (whatReady[0] == []): # Timeout
                    tracelist1 = ([str(ttl), "*", "Request timed out"])
                    tracelist2.append(tracelist1)
                    print("\t*\t\t*\t\t*\t\tRequest timed out.") 
                    continue
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    tracelist1 = ([ttl, "*", "Request timed out"])
                    tracelist2.append(tracelist1)
                    print("\t*\t\t*\t\t*\t\tRequest timed out.") 
            except timeout:
                continue

            else:
                (types, code, checksum, Id, seq) = struct.unpack("bbHHh", recvPacket[20:28])
                try: #try to fetch the hostname
                    #Fill in start
                    #Fill in end
                    host = gethostbyaddr(addr[0])[0]
                    #print(host)
                except error:   #if the host does not provide a hostname
                    #Fill in start
                    #Fill in end
                    host = "hostname not returnable"
                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should add your responses to your lists here
                    #Fill in end
                    tracelist1 = ([str(ttl), str((timeReceived - t)*1000)+'ms', str(addr[0]), str(host)])
                    #print(tracelist1)
                    tracelist2.append(tracelist1)
                    print("%d\t%.0fms " " %s " " %s" %(ttl, (timeReceived -t)*1000, addr[0], host))
                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should add your responses to your lists here 
                    #Fill in end
                    tracelist1 = ([str(ttl), str((timeReceived - t)*1000)+'ms', str(addr[0]), str(host)])
                    tracelist2.append(tracelist1)
                    print("%d\t%.0fms " " %s " " %s" %(ttl, (timeReceived -t)*1000, addr[0], host))
                elif types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should add your responses to your lists here and return your list if your destination IP is met
                    #Fill in end
                    tracelist1 = ([str(ttl), str((timeReceived - t)*1000)+'ms', str(addr[0]), str(host)])
                    tracelist2.append(tracelist1)
                    print("%d\t%.0fms " " %s " " %s" %(ttl, (timeReceived -t)*1000, addr[0], host))
                else:
                    #Fill in start
                    #If there is an exception/error to your if statements, you should append that to your list here
                    #Fill in end
                    print("Exception")
                break
            finally:
                mySocket.close()
    print(tracelist2)
    return tracelist2

if __name__ == '__main__':
    get_route("google.com")
