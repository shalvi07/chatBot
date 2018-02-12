import socket
from dateutil import tz
from chatApp.models import USERS_COLLECTION,MESSAGE_COLLECTION
users = USERS_COLLECTION.find()
userlist = list()
for record in users:
    userlist.append(record['name'])


class Listerner():
    # def __init__():
    #     print()



    def listerner(self,port):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", port))
        print ("waiting on port:", port)
        while 1:
            data, addr = s.recvfrom(1024)
            if not data: break
            conn.send(data)
            print (data)
        conn.close()




class Sender():

    def __init__(self):
        self.bufsize = 1024 # Modify to suit your needs
        self.targetHost = "127.0.0.1"
        # self.listenPort = 8788


    def sender(self,data,port,listenport):
        print "Forwarding: '%s' from port %s" % (data, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("localhost", port)) # Bind to the port data came in on
        print("Sending to %s" %listenport)
        sock.sendto(data, (self.targetHost, listenport))



    def listen(self,host, port):
        listenSocket = socket(AF_INET, SOCK_DGRAM)
        listenSocket.bind((host, port))
        while True:
            data, addr = listenSocket.recvfrom(self.bufsize)
            forward(data, addr[1]) # data and port

class Utils():
    def __init__(self):
        self.from_zone = tz.tzutc()
        self.to_zone = tz.tzlocal()

    def userexits(self,user):
        global userlist
        if user in userlist:
            return True
        else:
            return False


    def convert_to_local_tz(self,temp):
        temp = temp.replace(tzinfo=self.from_zone)
        temp = temp.astimezone(self.to_zone)
        return temp

#
# listen("localhost", listenPort)
