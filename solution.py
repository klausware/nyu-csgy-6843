#import socket module
from socket import *
import sys # In order to terminate the program
from email.parser import BytesParser
import email
import pprint
from io import StringIO

HOST = "127.0.0.1"
PORT = 13331
BUFFER_SIZE = 1024

def webServer(PORT):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    #Prepare a sever socket
    serverSocket.bind((HOST,PORT))
    serverSocket.listen(1)

    while True:
        #Wait for inbound client connection(s)
        print('Ready to serve...\n')
        clientConnectionSocket, clientAddr = serverSocket.accept()
        try:
            
            #Parse inbound HTTP Request Headers 
            message = clientConnectionSocket.recv(BUFFER_SIZE)
            _, headers = message.split(b'\r\n', 1)
            headerBytes = BytesParser().parsebytes(headers)
            headers = dict(headerBytes.items())
            print("Request Headers:\n")
            pprint.pprint(headers, width=160)
            print("")

            #Parse filename from HTTP Request
            filename = message.split()[1]
            print("File requested: %s\n" % filename.decode())
            f = open(filename[1:])
            outputdata = f.read()

            #Send HTTP headers line into socket
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Content-Type: text/html\n'
            response += '\n'
            clientConnectionSocket.send(response.encode()) 

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                clientConnectionSocket.send(outputdata[i].encode())

            clientConnectionSocket.send("\r\n".encode())
            clientConnectionSocket.close()
        except IOError:
            #Send response message for file not found (404)
            err = '404 Not Found'
            clientConnectionSocket.sendall(err.encode())

            #Close client socket
            clientConnectionSocket.close()

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)

