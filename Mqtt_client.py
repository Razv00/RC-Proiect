import time
from main import *
import string
import random
class ClientMQTT:
    def __init__(self,addr):
        self.isConnected = False
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(addr)
        self.keep_alive_flag = False
        self.keep_alive = 0
        self.id_packet = 0


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
        primit = self.conn.recv(4)
        buffer = back_str(primit)
        test_decode = DecodeConnack()
        result = test_decode.decode(buffer)
        print("pachet decodificat connack " + result.string())
        print()
    def receiver(self):
        primesc = self.conn.recv(4)
        date = back_str(primesc)
        type =int(date[0:4],2)
        print(type)
        if type == 2:
            test_decode = DecodeConnack()
            result = test_decode.decode(date)
            print("pachet decodificat connack " + result.string())
            return result
        if type == 3:
            QoS = int(date[6:7], 2) #asa si asa ...
            if QoS == 0:
                pass
                #nu se intampla nimic
            elif QoS == 1:
                test_decode = DecodePuback()
                result = test_decode.decode(date)
                print("pachet decodificat puback " + result.string())
                return result
            elif QoS == 2:
                test_decode = DecodePubrec()
                result = test_decode.decode(date)
                print("pachet decodificat puback " + result.string())
                return result

        if type == 4:
            test_decode = DecodePuback()
            result = test_decode.decode(date)
            print("pachet decodificat pubrec " + result.string())
            return result
        if type == 5:
            test_decode = DecodePubrec()
            result = test_decode.decode(date)
            print("pachet decodificat pubrec " + result.string())
            return result
        if type == 6:
            test_decode = DecodePubrel()
            result = test_decode.decode(date)
            print("pachet decodificat pubrel " + result.string())
            return result
        if type == 7:
            test_decode = DecodePubcomp()
            result = test_decode.decode(date)
            print("pachet decodificat pubcomp " + result.string())
            return result
        if type == 9:
            test_decode = DecodeSuback()
            result = test_decode.decode(date)
            print("pachet decodificat suback " + result.string())
            return result
        if type == 11:
            test_decode = DecodeUnsuback()
            result = test_decode.decode(date)
            print("pachet decodificat unsuback " + result.string())
            return result
        if type == 13:
            test_decode = DecodePingresp()
            result = test_decode.decode(date)
            print("pachet decodificat pubrec " + result.string())
            return result

        raise Exception("Nu este de tip corect ")

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
        self.id_packet += 1
        test = SUBSCRIBE()
        test.createPacketSubscribe(self.id_packet, topics, QoS)
        print("pachet creat subscribe " + test.string())
        encode = test.encode()
        print(encode)
        in_binar = binar(encode)
        print(in_binar)
        s.send(in_binar)

        #trebuie facut ceva pentru pachetele pe care nu le primim


    def unsubscribe(self, topics):
        self.id_packet += 1
        test = UNSUBSCRIBE()
        test.createPacketUnsubscribe(self.id_packet, topics)
        print("pachet creat unsubscribe " + test.string())
        encode = test.encode()
        print(encode)
        in_binar = binar(encode)
        print(in_binar)
        self.conn.send(in_binar)

    def publish(self, topic, message, QoS, retain):
        test = PUBLISH()
        self.id_packet += 1
        test.createPacketPublish(0, QoS, retain, topic, self.id_packet, message)
        print("pachet creat publish " + test.string())
        encode = test.encode()
        print(encode)
        in_binar = binar(encode)
        print(in_binar)
        self.conn.send(in_binar)
    def keepAlive(self):
        while self.keep_alive_flag is True:
            asteapta = self.keep_alive / 2
            while asteapta > 0 and self.keep_alive_flag is True:
                time.sleep(1)
                asteapta -= 1
            if self.keep_alive_flag is True:
                pingreq = PINGREQ()
                pingreq.createPacketPingreq()
                encode = pingreq.encode()
                in_binar = binar(encode)
                s.send(in_binar)

if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    address = (ip, 1883)

    username = str(input("Username = "))
    password = str(input("Password = "))

    client = ClientMQTT(address)
    client.connect("11000110", 60, username=username, password=password, willTopic="/register", willMessage="Buna ! Eu  sunt " + username)
    #client.receiver()
    client.publish('topic', 'buna', 2, 1) #(0, 2, 1, "topic_name", 11, "message")
    client.receiver()
    #client.disconnect()