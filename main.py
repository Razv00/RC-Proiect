import socket
from AllPackets import *
def binar(bin):
    result = bytearray()
    for index in range(0, len(bin), 8):
        result.append(int(bin[index:index + 8], 2))
    return result
def back_str(binar):
    string = ""
    for caracter in binar:
        value = int(str(caracter))
        for i in range(7, -1, -1):
            if (value & pow(2, i)) > 0:
                string += '1'
            else:
                string += '0'
    return string
if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 1883))
    test = CONNECT()
    test.createPacketConnect('Client', 'teodora', 'teodora', 10, '11000110', "hello world!","/register")
    print("pachet creat connect " + test.string())
    connect_encode = test.encode()
    in_binar = binar(connect_encode)
    print(in_binar)
    sent = s.send(binar(connect_encode))
    print(binar(connect_encode))
    primesc = s.recv(4)
    date = back_str(primesc)
    print("date = " + date)
    test_decode = DecodeConnack()
    result = test_decode.decode(date)
    print("pachet decodificat connack " + result.string())
    print()

    pingreq = PINGREQ()
    pingreq.createPacketPingreq()
    print("pachet creat pingreq " + pingreq.string())
    encode = pingreq.encode()
    print(encode)
    in_binar = binar(encode)
    print(in_binar)

    s.send(in_binar)


    primesc = s.recv(4)
    print("date = " + date)
    date = back_str(primesc)
    test_decode = DecodePingresp()
    result = test_decode.decode(date)
    print("pachet decodificat pingreq " + result.string())
    print()

    """
    test = PUBLISH()
    test.createPacketPublish(0, 0, 1, "topic_name", 1, "app_message")
    print("pachet creat publish " + test.string())
    encode = test.encode()
    print(encode)
    in_binar = binar(encode)
    print(in_binar)
    s.send(in_binar)

    
    print()
    test = SUBSCRIBE()
    test.createPacketSubscribe(1, ["verific"], [0])
    print("pachet creat subscribe " + test.string())
    encode = test.encode()
    print(encode)
    in_binar = binar(encode)
    print(in_binar)
    s.send(in_binar)
    """
    test = PUBLISH()
    test.createPacketPublish(0, 2, 1, "topic_name", 11, "message")
    print("pachet creat publish " + test.string())
    encode = test.encode()
    print(encode)
    in_binar = binar(encode)
    print(in_binar)
    s.send(in_binar)


    primesc = s.recv(4)
    date = back_str(primesc)
    print("data mea " + date)
    test_decode = DecodePubrec()
    result = test_decode.decode(date)
    print("pachet decodificat pubrec " + result.string())



    test = UNSUBSCRIBE()
    test.createPacketUnsubscribe(11, ["verific"])
    print("pachet creat unsubscribe " + test.string())
    encode = test.encode()
    print(encode)
    in_binar = binar(encode)
    print(in_binar)
    s.send(in_binar)

    primesc = s.recv(4)
    print("date = " + date)
    date = back_str(primesc)
    test_decode = DecodeUnsuback()
    result = test_decode.decode(date)
    print("pachet decodificat pingreq " + result.string())
    print()


    test_decode = DecodeUnsuback()
    result = test_decode.decode(encode)
    print("pachet decodific unsuback " + result.string())
    print()


    print()
    test = PUBREL()
    test.createPacketPubrel(11)
    print("pachet creat pubrel " + test.string())
    encode = test.encode()
    print(encode)
    in_binar = binar(encode)
    print(in_binar)
    s.send(in_binar)

    primesc = s.recv(4)
    print("date = " + date)
    date = back_str(primesc)
    test_decode = DecodePubcomp()
    result = test_decode.decode(date)
    print("pachet decodificat pubcomp " + result.string())
    print()







    test = DISCONNECT()
    test.createPacketDisconnect()
    print("pachet creat disconnect " + test.string())
    encode = test.encode()
    print(encode)
    in_binar = binar(encode)
    print(in_binar)
    s.send(in_binar)
















