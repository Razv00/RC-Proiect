import time
import socket
from AllPackets import *
from main import *
import string
import random
class ClientMQTT:
    def __init__(self,addr):
        self.isConnected = False
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(addr)
        self.keep_alive_flag = False;
        self.keep_alive = 0


    def connect(self, flags, keep_alive, username='', password='', willTopic='', willMessage=''):

        length = random.randint(4, 10)
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
        test = CONNECT()
        test.createPacketConnect(result_str, username, password, keep_alive, flags, willMessage,willTopic)

        print("pachet creat connect " + test.string())
        connect_encode = test.encode()
        in_binar = binar(connect_encode)
        print(in_binar)
        self.conn.send(binar(connect_encode))
        print(binar(connect_encode))
        primit = self.conn.recv(4)
        buffer = back_str(primit)
        test_decode = DecodeConnack()
        result = test_decode.decode(buffer)
        print("pachet decodificat connack " + result.string())
        print()

    def disconnect(self):
        test = DISCONNECT()
        test.createPacketDisconnect()
        print("pachet creat disconnect " + test.string())
        encode = test.encode()
        print(encode)
        in_binar = binar(encode)
        print(in_binar)
        self.conn.send(in_binar)

    def subscribe(self, topics, QoS):
        pass

    def unsubscribe(self, topics):
        pass

    def publish(self, topic, message, QoS, retain=0):
        pass
    def keepAlive(self):
                pass
if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    address = (ip, 1883)

    username = str(input("Username = "))
    password = str(input("Password = "))

    client = ClientMQTT(address)
    client.connect("11000110", 10, username=username, password=password, willTopic="/register", willMessage="Buna ! Eu  sunt " + username)

    client.disconnect()