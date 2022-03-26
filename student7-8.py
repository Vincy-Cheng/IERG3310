import socket
import random
import time
import array as arr
robotVersion = "3.0"
listenPort = 3310
socket.setdefaulttimeout(10)
localhost = '127.0.0.1'
# create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s connect to server
s.connect((localhost, listenPort)) 
sid = "1155125313" # student id

# sending Student ID to server
s.send(sid.encode())

# receive the socket description(ddddd) from server
data = s.recv(5)

print('Received', data.decode())
s.close()

# create a new socket for a new connection of port ddddd
print ("Preparing to receive server connection")
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((localhost, int(data.decode())))
s1.listen(1)
s2, address = s1.accept()
serverIP = address[0]
s1.close()
print("Connected")

# receiver buffer size
buffer_size1 = s2.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print('Buffer size = ', str(buffer_size1) )

# (step 7) send the buffer size to server(Robot)
send_buffer_size = "bs" + str(buffer_size1)
s2.send(send_buffer_size.encode())

# receive the large number from Robot

i = 0  # Number of received messages
size = 0  # size of messages
print("Receiving message of buffer size = %d" % buffer_size1)
start = time.time()
while (time.time() - start) <= 30:
    re_message = s2.recv(10)
    re_message = re_message.decode()
    size += re_message.__sizeof__()
    i += 1
print("Number of received messages: <%d>, total received bytes: <%d>.\n" % (i, size))

time.sleep(1)
# (step 8) repeat step 7 with the changing receiver buffer size
# (e.g. [1, 5, 10, 25, 50, 200, 500 or even 1000] % of 1000 bytes.)

buffer = arr.array('i', [10, 50, 100, 500, 2000, 5000, 10000, 20000])

for k in range(0, 8):
    buffer_size1 = buffer[k]
    print('Buffer size = ', str(buffer_size1))
    send_buffer_size = "bs" + str(buffer_size1)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size1)
    s2.send(send_buffer_size.encode())
    i = 0  # Number of received messages
    size = 0  # size of messages
    print("Receiving message of buffer size = %d" % (s2.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))
    start = time.time()
    while (time.time() - start) <= 30:
        re_message = s2.recv(10)
        size += len(re_message)
        re_message = re_message.decode()
        i += 1
    print("Number of received messages: <%d>, total received bytes: <%d>.\n" % (i, size))

time.sleep(1)

s2.close()

