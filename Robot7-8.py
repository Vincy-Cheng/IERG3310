# IERG3310 Project
# first version written by FENG, Shen Cody
# second version modified by YOU, Lizhao
# Third version modified by Jonathan Liang @ 2016.10.25

import socket
import random
import time

robotVersion = "3.0"
listenPort = 3310
socket.setdefaulttimeout(10)
localhost = '127.0.0.1'

print ("Robot is started")
print ("You are reminded to check for the latest available version")

print ("")

# Create a TCP socket to listen connection
print ("Creating TCP socket...")
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((localhost, listenPort))
listenSocket.listen(5)
print ("Done")

print ("\nTCP socket created, ready for listening and accepting connection...")
# print "Waiting for connection on port %(listenPort)s" % locals()
print ("Waiting for connection on port", listenPort)

# accept connections from outside, a new socket is constructed
s1, address = listenSocket.accept()
studentIP = address[0]
print ("\nClient from %s at port %d connected" %(studentIP,address[1]))
# Close the listen socket
# Usually you can use a loop to accept new connections
listenSocket.close()
data = s1.recv(10)
print ("Student ID received: " ),
print(data.decode())

iTCPPort2Connect = random.randint(0,9999) + 20000
print ("Requesting STUDENT to accept TCP <%d>..." %iTCPPort2Connect)

s1.send(str(iTCPPort2Connect).encode()) # sending ddddd to student
print ("Done")


time.sleep(1)
print ("\nConnecting to the STUDENT s1 <%d>..." %iTCPPort2Connect)

############################################################################# phase 1
# Connect to the server (student s2)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((studentIP,iTCPPort2Connect))

print("Done\n")

# (step 7) receive the buffer size from student
buffer_size = s2.recv(10)
buffer_size = buffer_size.decode().split("s")
print('buffer size of student : ', buffer_size[1])

# send a large number of message to student within 30 seconds
message = "Buffer size "#str(int(buffer_size[1]))  # message is 65536
size = 0
i = 0
print("Sending message to buffer size = %d " % (int(buffer_size[1])))
start = time.time()
while (time.time() - start) <= 30:
    s2.send(message.encode())
    i += 1
    size += message.__sizeof__()

print("Number of sent messages: <%d>, total sent   bytes: <%d>.\n" % (i, size))

time.sleep(1)
# (step 8) repeat step 7 with the changing receiver buffer size
# (e.g. [1, 5, 10, 25, 50, 200, 500 or even 1000] % of 1000 bytes.)
for k in range(0, 8):
    buffer_size = s2.recv(10)
    buffer_size = buffer_size.decode().split("s")
    print('buffer size of student : ', buffer_size[1])
    message = str(int(buffer_size[1]))
    size = 0
    i = 0
    print("Sending message to buffer size = %d " % (int(buffer_size[1])))
    start = time.time()
    while (time.time() - start) <= 30:
        s2.send(message.encode())
        i += 1
        size += message.__sizeof__()
    print("Number of sent messages: <%d>, total sent   bytes: <%d>.\n" % (i, size))

s1.close()
s2.close()

exit()
