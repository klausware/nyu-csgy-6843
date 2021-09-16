import socket


def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\nThis is student nk3338\r\n"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope    

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    clientSocket = socket.socket()
    clientSocket.connect((mailserver,port))    
    recv = clientSocket.recv(1024).decode()
    #print(recv)
    
    if recv[:3] != '220':
        exit
        #print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'EHLO localhost\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    if recv1[:3] != '250':
        exit
        #print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    fromCommand = 'MAIL FROM: test@local.edu\r\n'
    clientSocket.send(fromCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    if recv1[:3] != '250':
        exit
        #print('250 reply not received from server.')

    # Send RCPT TO command and print server response.
    rcptCommand = 'RCPT TO: test@blackcatsecurity.com\r\n'
    clientSocket.send(rcptCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    if recv1[:3] != '250':
        exit
        #print('250 reply not received from server.')

    # Send DATA command and print server response.
    dataCommand = 'DATA\r\n'
    clientSocket.send(dataCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    if recv1[:3] != '250':
        exit
        #print('250 reply not received from server.')

    # Send message data.
    data = msg
    clientSocket.send(data.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    if recv1[:3] != '354':
        exit
        #print('354 reply not received from server.')

    # Message ends with a single period.
    periodCommand = endmsg
    clientSocket.send(periodCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    if recv1[:3] != '250':
        exit
        #print('250 reply not received from server.')

    # Send QUIT command and get server response.
    quitCommand = 'QUIT\r\n'
    clientSocket.send(quitCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    if recv1[:3] != '221':
        exit
        #print('221 reply not received from server.')


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
