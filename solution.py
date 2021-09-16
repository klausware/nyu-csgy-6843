from socket import *


def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope
    mailserver = ("mail.digisync.com", 10587)    

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(mailserver)    

    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'EHLO localhost\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    fromCommand = 'MAIL FROM: nk3338@nyu.edu\r\n'
    clientSocket.send(fromCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send RCPT TO command and print server response.
    rcptCommand = 'RCPT TO: localhost@localhost.com\r\n'
    clientSocket.send(rcptCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send DATA command and print server response.
    dataCommand = 'DATA\r\n'
    clientSocket.send(dataCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send message data.
    data = 'This is user nk3338\r\n'
    clientSocket.send(data.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '354':
        print('354 reply not received from server.')

    # Message ends with a single period.
    periodCommand = '.\r\n'
    clientSocket.send(periodCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send QUIT command and get server response.
    quitCommand = 'QUIT\r\n'
    clientSocket.send(quitCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '221':
        print('221 reply not received from server.')


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
