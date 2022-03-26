import socket
import random
import time

robotVersion = "3.0"
listenPort = 45321
socket.setdefaulttimeout(10)
serverhost = '172.16.5.11'
localhost = '172.16.5.13'
# create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s connect to server
s.connect((serverhost, listenPort)) 
sid = "1155125313" # student id

# sending Student ID to server
s.send(sid.encode())

# receive the socket description from server
data = s.recv(5) # receiving ddddd
print('Received', data.decode())
s.close()

# create a new  TCP socket for a new connection
print ("Preparing to receive server connection")
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((localhost, int(data.decode())))
s1.listen(1)
s2, address = s1.accept()
serverIP = address[0]
s1.close()
print("Connected")

# receive the 12 char fffff,eeeee.
data = s2.recv(12)
s2.close()
print('Received', data.decode())

# create a new UDP socket to connect sever

s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverPt = data.decode() # getting server port no.
serverPt = serverPt.split(",")
studentPT = serverPt[1].split(".") # client port no. to be use

#sending random num
num = random.randint(5, 10)
snum = str(num).encode() # num to be sent
s3.sendto(snum,(serverIP,int(serverPt[0])))
s3.close()

#create a new UDP socket
s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s4.bind((localhost,int(studentPT[0])))

#sending str with length = num*10
xxx , addr = s4.recvfrom(num*10)
xxx = xxx.decode()
for i in range(0,5):
    s4.sendto(xxx.encode(),addr)
    time.sleep(1)
    print ("UDP packet %d sent" %(i+1))

s4.close()
