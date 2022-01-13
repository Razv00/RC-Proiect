from headerfix import *
def generate(val):
    string = ''
    for i in range(val):
        string += format(0,'08b')
    return string


def encodeRemainingLength(remLength):
    if remLength == 0:
        return "00000000"

    remLengthStr = ""
    while remLength > 0:
        encoded = remLength % 128
        remLength = remLength // 128

        if remLength > 0:
            encodedByte = (encoded | 128)

        remLengthStr += format(encoded, '08b')

    return remLengthStr
class CONNECT(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)

        self.VariabileHeader_protocol_name = ''
        self.VariabileHeader_protocol_name_length = 0
        self.VariabileHeader_level = 0
        self.VariabileHeader_connect_flags = 0
        self.VariabileHeader_keep_alive = 0

        self.Payload_client_id = ''
        self.Payload_client_id_length = 0
        self.Payload_will_topic = ''
        self.Payload_will_topic_length = 0
        self.Payload_will_message = ''
        self.Payload_will_message_length = 0
        self.Payload_username = ''
        self.Payload_username_length = 0
        self.Payload_password = ''
        self.Payload_password_length = 0

    def createPacketConnect(self,client_id,username, password, keepAlive, connectFlags, willMessage,willTopic):
        #headerfix
        self.FixedHeader= HeaderFix(1, 0, 0)

        #header_variabil
        self.VariabileHeader_protocol_name = "MQTT"
        self.VariabileHeader_protocol_name_length = 4
        self.VariabileHeader_level = 4
        #7 User Name Flag | 6 Password Flag  | 5 Will Retain | 3-4  Will QoS|  Will Flag | 2 | 1 Clean Session | 0 Reserved
        self.VariabileHeader_connect_flags = int(connectFlags, 2)
        self.VariabileHeader_keep_alive = keepAlive

        #payload
        self.Payload_client_id = client_id
        self.Payload_client_id_length = len(client_id)
        # 7 User Name Flag | 6 Password Flag  | 5 Will Retain | 3-4  Will QoS|  Will Flag | 2 | 1 Clean Session | 0 Reserved
        pay_flag = str(format(self.VariabileHeader_connect_flags, '08b'))
        if pay_flag[5] == "1":
            self.Payload_will_topic = willTopic
            self.Payload_will_topic_length = len(willTopic)
            self.Payload_will_message = willMessage
            self.Payload_will_message_length = len(willMessage)

        if pay_flag[0] == "1":
            self.Payload_username = username
            self.Payload_username_length = len(username)
            if pay_flag[1] == "1":
                self.Payload_password = password
                self.Payload_password_length = len(password)

        # trebuie sa fie calculat remaining_length
        suma_varhed_payload = 2 + self.VariabileHeader_protocol_name_length + 1 + 1 + 2 + 2 + self.Payload_client_id_length
        if pay_flag[5] == "1":
            suma_varhed_payload += self.Payload_will_topic_length + self.Payload_will_message_length  + 4

        if pay_flag[0] == "1":
            suma_varhed_payload += self.Payload_username_length + 2
            if pay_flag[1] == "1":
                suma_varhed_payload += self.Payload_password_length + 2
        self.FixedHeader.SetRemainingLength(suma_varhed_payload)

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b') #control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b') #flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  #remaining_length

        # codific headerul variabil
        encoded = encoded + generate(2 - 1) + format(self.VariabileHeader_protocol_name_length,'08b')  # self.VariabileHeader_protocol_name_length, 2 deoarece in documentatie protocol name este pe 2 bytes, byte 1 si byte 2
        for elem in  self.VariabileHeader_protocol_name:
            encoded += format(ord(elem), '08b')
        encoded = encoded + generate(1 - 1) + format(self.VariabileHeader_level,'08b')  # self.VariabileHeader_protocol_name_length, 1 deoarece in documentatie este  byte 7
        encoded += generate(1 - 1) + format(self.VariabileHeader_connect_flags,'08b')  # self.VariabileHeader_protocol_name_length, 1 deoarece in documentatie este byte 8
        encoded += generate(2 - 1) + format(self.VariabileHeader_keep_alive,'08b')  # self.VariabileHeader_protocol_name_length, 2 deoarece in documentatie este byte 9 si 10

        #codific payload
        encoded += generate(2 - 1) + format(self.Payload_client_id_length,'08b')  # 2 deoarece la password am vazut ca byte 1 si 2 sunt pentru lungime
        for elem in  self.Payload_client_id:
            encoded += format(ord(elem), '08b')

        pay_flag = str(format(self.VariabileHeader_connect_flags, '08b'))
        if pay_flag[5] == "1":
            encoded += generate(2 - 1) + format(self.Payload_will_topic_length,'08b')
            for elem in self.Payload_will_topic:
                encoded += format(ord(elem), '08b')
            encoded += generate(2 - 1) + format(self.Payload_will_message_length,'08b')
            for elem in self.Payload_will_message:
                encoded += format(ord(elem), '08b')

        if pay_flag[0] == "1":
            encoded += generate(2 - 1) + format(self.Payload_username_length,'08b')
            for elem in self.Payload_username:
                encoded += format(ord(elem), '08b')
            if pay_flag[1] == "1":
                encoded += generate(2 - 1) + format(self.Payload_password_length,'08b')
                for elem in self.Payload_password:
                    encoded += format(ord(elem), '08b')
        return encoded
    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + self.VariabileHeader_protocol_name + ", " + str(
            self.VariabileHeader_protocol_name_length) + ", " + str(self.VariabileHeader_level) + ", " + str(
            self.VariabileHeader_connect_flags) + ", " + str(self.VariabileHeader_keep_alive) + "} "
        return result
    def stringPayload(self):
        result = ' Payload: {' + str(self.Payload_client_id) + ", " + str(
            self.Payload_client_id_length) + ", " + self.Payload_will_topic + ", " + str(
            self.Payload_will_topic_length) + ", " + self.Payload_will_message + ", " + str(
            self.Payload_will_message_length) + ", " + self.Payload_username + ", " + str(
            self.Payload_username_length) + ", " + self.Payload_password + ", " + str(
            self.Payload_password_length) + "}"
        return result
    def string(self):
        result = "PachetConnect{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil()+ "," + self.stringPayload()+"}"
        return result
class DecodeConnect(ABC):
    def type(self):
        return 1
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        connect_decode = CONNECT()
        connect_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        connect_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        connect_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        #decodific tot ce reprezinta header variabil
        connect_decode.VariabileHeader_protocol_name_length = int(encoded[8:16],2)
        encoded = encoded[16:]
        protocol_name = ''
        for elem in  range(connect_decode.VariabileHeader_protocol_name_length):
            protocol_name += chr(int(encoded[0:8], 2))
            encoded = encoded[8:]
        connect_decode.VariabileHeader_protocol_name = protocol_name
        connect_decode.VariabileHeader_level = int(encoded[0:8], 2)
        encoded = encoded[8:]
        connect_decode.VariabileHeader_connect_flags = int(encoded[0:8], 2)
        encoded = encoded[8:]
        connect_decode.VariabileHeader_keep_alive = int(encoded[8:16], 2)
        encoded = encoded[16:]
        #decodific tot ce reprezinta payload
        connect_decode.Payload_client_id_length = int(encoded[8:16], 2)
        encoded = encoded[16:]
        client_id = ''
        for elem in range(connect_decode.Payload_client_id_length):
            client_id += chr(int(encoded[0:8], 2))
            encoded = encoded[8:]
        connect_decode.Payload_client_id = client_id
        pay_flag = str(format(connect_decode.VariabileHeader_connect_flags, '08b'))
        if pay_flag[5] == "1":
            connect_decode.Payload_will_topic_length = int(encoded[8:16], 2)
            encoded = encoded[16:]
            will_topic = ''
            for elem in range(connect_decode.Payload_will_topic_length):
                will_topic += chr(int(encoded[0:8], 2))
                encoded = encoded[8:]
            connect_decode.Payload_will_topic = will_topic
            connect_decode.Payload_will_message_length = int(encoded[8:16], 2)
            encoded = encoded[16:]
            will_message = ''
            for elem in range(connect_decode.Payload_will_message_length):
                will_message += chr(int(encoded[0:8], 2))
                encoded = encoded[8:]
            connect_decode.Payload_will_message = will_message
        if pay_flag[0] == "1":
            connect_decode.Payload_username_length = int(encoded[8:16], 2)
            encoded = encoded[16:]
            username = ''
            for elem in range(connect_decode.Payload_username_length):
                username += chr(int(encoded[0:8], 2))
                encoded = encoded[8:]
            connect_decode.Payload_username = username
            if pay_flag[1] == "1":
                connect_decode.Payload_password_length = int(encoded[8:16], 2)
                encoded = encoded[16:]
                password = ''
                for elem in range(connect_decode.Payload_password_length):
                    password += chr(int(encoded[0:8], 2))
                    encoded = encoded[8:]
                connect_decode.Payload_password = password

        return connect_decode

class CONNACK(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0,0,0)
        self.VariableHeader_SP = 0
        self.VariableHeader_connect_return_code = 0

    def createPacketConnack(self, SP, connect_return_code):
        # headerfix
        self.FixedHeader = HeaderFix(2, 0, 2)

        #header variabil
        self.VariableHeader_SP = SP
        self.VariableHeader_connect_return_code = connect_return_code

        #nu are payload

        #calculez remaining_length

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())   # remaining_length

        #codific headerul variabil
        encoded = encoded + generate(1 - 1) + format(self.VariableHeader_SP,'08b')  # byte 1
        encoded = encoded + generate(1 - 1) + format(self.VariableHeader_connect_return_code,'08b')  # byte 1

        #nu are payload

        return encoded
    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_SP) + ", " + str(
            self.VariableHeader_connect_return_code) +  "} "
        return result
    def stringPayload(self):
        result = ' Payload: {' + "Nu are"+ "}"
        return result
    def string(self):
        result = "PachetConnack{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + ","+ self.stringPayload()+"}"
        return result
class DecodeConnack(ABC):
    def type(self):
        return 2
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        connack_decode = CONNACK()
        connack_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        connack_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        connack_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        connack_decode.VariableHeader_SP = int(encoded[0:8],2)
        encoded = encoded[8:]
        connack_decode.VariableHeader_connect_return_code = int(encoded[0:8], 2)
        encoded = encoded[8:]
        #decodific tot ce reprezinta header variabil

        return connack_decode

class PUBLISH(ABC):
    def __init__(self):
        self.FixedHeader =HeaderFix(0,0,0)

        self.VariableHeader_topic_name = ''
        self.VariableHeader_topic_name_length = 0
        self.VariableHeader_pachet_identifier = 0

        self.Payload_app_message = '' # la asta nu am pus lungime deoarece nu stiu pe cati bytes sa codific lungimea


    def createPacketPublish(self, DUP_flag, QoS_level, RETAIN,topic_name, pachet_identifier, app_message):
        #headerfix
        self.FixedHeader = HeaderFix(3, int('{0:01b}'.format(DUP_flag) + '{0:02b}'.format(QoS_level) + '{0:01b}'.format(RETAIN), 2), 0)

        #header variabil
        if QoS_level == 2 or QoS_level == 1:
            self.VariableHeader_pachet_identifier = pachet_identifier
        self.VariableHeader_topic_name = topic_name
        self.VariableHeader_topic_name_length = len(topic_name)

        #payload
        self.Payload_app_message = app_message

        #calculez remaining_length
        suma_varhed_payload = 2 + 2 + self.VariableHeader_topic_name_length

        self.FixedHeader.SetRemainingLength(suma_varhed_payload + int('{0:01b}'.format(DUP_flag) + '{0:02b}'.format(QoS_level) + '{0:01b}'.format(RETAIN), 2) + len(self.Payload_app_message))


    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

       #codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_pachet_identifier,'08b') #byte 6 si 7
        encoded += generate(2 - 1) + format(self.VariableHeader_topic_name_length, '08b')  # byte 6 si 7
        for elem in self.VariableHeader_topic_name:
            encoded += format(ord(elem), '08b')

        #codific payload
        encoded += format(len(self.Payload_app_message), '08b')
        for elem in self.Payload_app_message:
            encoded += format(ord(elem), '08b')

        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_pachet_identifier) + ", " + self.VariableHeader_topic_name + ", " +   str(
            self.VariableHeader_topic_name_length) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: {' +  self.Payload_app_message + "}"
        return result

    def string(self):
        result = "PachetPublish{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodePublish(ABC):
    def type(self):
        return 3
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        publish_decode = PUBLISH()
        publish_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        publish_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        publish_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        publish_decode.VariableHeader_pachet_identifier = int(encoded[8:16],2)
        encoded = encoded[16:]
        publish_decode.VariableHeader_topic_name_length = int(encoded[8:16], 2)
        encoded = encoded[16:]
        topic_name = ''
        for elem in range(publish_decode.VariableHeader_topic_name_length):
            topic_name += chr(int(encoded[0:8], 2))
            encoded = encoded[8:]
        publish_decode.VariableHeader_topic_name = topic_name
        # decodific tot ce reprezinta payload
        app_message_length = int(encoded[0:8], 2)
        encoded = encoded[8:]
        app_message = ''
        for elem in range(app_message_length):
            app_message += chr(int(encoded[0:8], 2))
            encoded = encoded[8:]
        publish_decode.Payload_app_message = app_message

        return publish_decode

class PUBACK(ABC):
    def __init__(self):
        self.FixedHeader =HeaderFix(0,0,0)
        self.VariableHeader_packet_ID = 0

    def createPacketPuback(self,packet_ID):
        # headerfix
        self.FixedHeader = HeaderFix(4,0,2)

        # header variabil
        self.VariableHeader_packet_ID = packet_ID

        # nu are payload



    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        #codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_packet_ID, '08b')

        #nu are payload

        return encoded
    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_packet_ID) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: {' + "Nu are" + "}"
        return result

    def string(self):
        result = "PachetPuback{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodePuback(ABC):
    def type(self):
        return 4
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        puback_decode = PUBACK()
        puback_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        puback_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        puback_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        puback_decode.VariableHeader_packet_ID = int(encoded[8:16],2)
        encoded = encoded[16:]

        #nu are payload
        return puback_decode

class PUBREC(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)
        self.VariableHeader_packet_ID = 0

    def createPacketPubrec(self, packet_ID):
        # headerfix
        self.FixedHeader = HeaderFix(5, 0, 2)

        # header variabil
        self.VariableHeader_packet_ID = packet_ID

        # nu are payload

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        # codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_packet_ID, '08b')

        # nu are payload

        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_packet_ID) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: {' + "Nu are" + "}"
        return result

    def string(self):
        result = "PachetPubrec{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodePubrec(ABC):
    def type(self):
        return 5
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        pubrec_decode = PUBREC()
        pubrec_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        pubrec_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        pubrec_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        pubrec_decode.VariableHeader_packet_ID = int(encoded[8:16],2)
        encoded = encoded[16:]

        #nu are payload
        return pubrec_decode

class PUBREL(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)
        self.VariableHeader_packet_ID = 0

    def createPacketPubrel(self, packet_ID):
        # headerfix
        self.FixedHeader = HeaderFix(6, 2, 2)

        # header variabil
        self.VariableHeader_packet_ID = packet_ID

        # nu are payload

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())# remaining_length

        # codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_packet_ID, '08b')

        # nu are payload

        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_packet_ID) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: {' + "Nu are" + "}"
        return result

    def string(self):
        result = "PachetPubrel{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodePubrel(ABC):
    def type(self):
        return 6
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        pubrel_decode = PUBREL()
        pubrel_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        pubrel_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        pubrel_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        pubrel_decode.VariableHeader_packet_ID = int(encoded[8:16],2)
        encoded = encoded[16:]

        #nu are payload
        return pubrel_decode

class PUBCOMP(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)
        self.VariableHeader_packet_ID = 0

    def createPacketPubcomp(self, packet_ID):
        # headerfix
        self.FixedHeader = HeaderFix(7, 0, 2)

        # header variabil
        self.VariableHeader_packet_ID = packet_ID

        # nu are payload

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())# remaining_length

        # codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_packet_ID, '08b')

        # nu are payload

        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_packet_ID) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: {' + "Nu are" + "}"
        return result

    def string(self):
        result = "PachetPubcomp{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodePubcomp(ABC):
    def type(self):
        return 7
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        pubcomp_decode = PUBCOMP()
        pubcomp_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        pubcomp_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        pubcomp_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        pubcomp_decode.VariableHeader_packet_ID = int(encoded[8:16],2)
        encoded = encoded[16:]

        #nu are payload
        return pubcomp_decode

class SUBSCRIBE(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)
        self.VariableHeader_packet_ID = 0
        self.Payload_topics = []

    def createPacketSubscribe(self, packet_ID, topics, QoS):
        # headerfix
        self.FixedHeader = HeaderFix(8, 2, 2)

        # header variabil
        self.VariableHeader_packet_ID = packet_ID

        # payload
        index = 0;
        length_payload = 0
        for elem in topics:
            self.Payload_topics.append(len(elem))
            length_payload += len(elem)
            self.Payload_topics.append(elem)
            self.Payload_topics.append(QoS[index])
            length_payload += 1
            index = index + 1

            # calculez remaining_length
            self.FixedHeader.SetRemainingLength(length_payload+2)

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        # codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_packet_ID, '08b')

        # codific payload
        lista_topic = self.Payload_topics
        for elem in range(0, len(lista_topic), 3):
            encoded += generate(2 - 1) + format(lista_topic[elem], '08b')
            for caracter in lista_topic[elem +1]:
                encoded += format(ord(caracter), '08b')
            encoded += generate(1 - 1) + format(lista_topic[elem + 2], '08b')
        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_packet_ID) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: '
        result = result + str(self.Payload_topics)
        return result

    def string(self):
        result = "PachetSubscribe{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodeSubscribe:
    def type(self):
        return 8
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        subscribe_decode = SUBSCRIBE()
        subscribe_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        subscribe_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        subscribe_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        subscribe_decode.VariableHeader_packet_ID = int(encoded[8:16],2)
        encoded = encoded[16:]

        #decodific payload
        while encoded != '':
            topic_filter_length = int(encoded[8:16], 2)
            encoded = encoded[16:]
            topic_filter = ''
            for elem in range(topic_filter_length):
                topic_filter += chr(int(encoded[0:8], 2))
                encoded = encoded[8:]
            requested_qos = int(encoded[0:8], 2)
            encoded = encoded[8:]
            subscribe_decode.Payload_topics.append(topic_filter_length)
            subscribe_decode.Payload_topics.append(topic_filter)
            subscribe_decode.Payload_topics.append(requested_qos)

        return subscribe_decode

class SUBACK(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)
        self.VariableHeader_packet_ID = 0
        self.Payload_return_codes = []

    def createPacketSuback(self, packet_ID, return_codes):
        # headerfix
        self.FixedHeader = HeaderFix(9, 0, 2)

        # header variabil
        self.VariableHeader_packet_ID = packet_ID

        # payload
        suma_payload = 0
        for elem in return_codes:
            self.Payload_return_codes.append(elem)
            suma_payload += len(elem)

            # calculez remaining_length
            self.FixedHeader.SetRemainingLength(suma_payload)

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        # codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_packet_ID, '08b')

        return_codes = self.Payload_return_codes
        for elem in return_codes:
            encoded += generate(2 - 1) + format(len(elem), '08b')
            for caracter in elem:
                encoded += format(ord(caracter), '08b')
        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_packet_ID) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: '
        result = result + str(self.Payload_return_codes)
        return result

    def string(self):
        result = "PachetSuback{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodeSuback(ABC):
    def type(self):
        return 9
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        suback_decode = SUBACK()
        suback_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        suback_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        suback_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        suback_decode.VariableHeader_packet_ID = int(encoded[8:16],2)
        encoded = encoded[16:]
        #decodific payload
        while encoded != '':
            return_codes_length = int(encoded[8:16], 2)
            encoded = encoded[16:]
            return_codes = ''
            for elem in range(return_codes_length):
                return_codes += chr(int(encoded[0:8], 2))
                encoded = encoded[8:]
            suback_decode.Payload_return_codes.append(return_codes)
        return suback_decode


class UNSUBSCRIBE(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)
        self.VariableHeader_packet_ID = 0
        self.Payload_topics = []

    def createPacketUnsubscribe(self, packet_ID, topics):
        # headerfix
        self.FixedHeader = HeaderFix(10, 2, 2)

        # header variabil
        self.VariableHeader_packet_ID = packet_ID

        # payload
        suma_payload = 0
        for elem in topics:
            self.Payload_topics.append(len(elem))
            self.Payload_topics.append(elem)
            suma_payload = suma_payload + 2 + len(elem)

        # calculez remaining_length
        self.FixedHeader.SetRemainingLength(suma_payload+2)

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        # codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_packet_ID, '08b')

        topics = self.Payload_topics
        for elem in range (0, len(topics),2):
            encoded += generate(2 - 1) + format(topics[elem], '08b')
            for caracter in topics[elem+1]:
                encoded += format(ord(caracter), '08b')
        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_packet_ID) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: '
        result = result + str(self.Payload_topics)
        return result

    def string(self):
        result = "PachetUnsubscribe{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodeUnsubscribe(ABC):
    def type(self):
        return 10
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        unsubscribe_decode = UNSUBSCRIBE()
        unsubscribe_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        unsubscribe_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        unsubscribe_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        unsubscribe_decode.VariableHeader_packet_ID = int(encoded[8:16],2)
        encoded = encoded[16:]
        #decodific payload
        while encoded != '':
            topics_length = int(encoded[8:16], 2)
            encoded = encoded[16:]
            topics = ''
            for elem in range(topics_length):
                topics += chr(int(encoded[0:8], 2))
                encoded = encoded[8:]
            unsubscribe_decode.Payload_topics.append(topics_length)
            unsubscribe_decode.Payload_topics.append(topics)

        return unsubscribe_decode


class UNSUBACK(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)
        self.VariableHeader_packet_ID = 0

    def createPacketUnsuback(self, packet_ID):
        # headerfix
        self.FixedHeader = HeaderFix(11, 0, 2)

        # header variabil
        self.VariableHeader_packet_ID = packet_ID

        # nu are payload

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        # codific header variabil
        encoded += generate(2 - 1) + format(self.VariableHeader_packet_ID, '08b')

        # nu are payload

        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + str(self.VariableHeader_packet_ID) + "} "
        return result

    def stringPayload(self):
        result = ' Payload: {' + "Nu are" + "}"
        return result

    def string(self):
        result = "PachetUnsuback{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodeUnsuback(ABC):
    def type(self):
        return 11
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        unsuback_decode = UNSUBACK()
        unsuback_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        unsuback_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        unsuback_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        # decodific tot ce reprezinta header variabil
        unsuback_decode.VariableHeader_packet_ID = int(encoded[8:16],2)
        encoded = encoded[16:]

        #nu are payload
        return unsuback_decode

class PINGREQ(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)

    def createPacketPingreq(self):
        # headerfix
        self.FixedHeader = HeaderFix(12, 0, 0)

        # nu are header variabil

        # nu are payload

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        # nu header variabil

        # nu are payload

        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + "Nu are" + "}"
        return result

    def stringPayload(self):
        result = ' Payload: {' + "Nu are" + "}"
        return result

    def string(self):
        result = "PachetPingreq{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodePingreq(ABC):
    def type(self):
        return 12
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        pingreq_decode = PINGREQ()
        pingreq_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        pingreq_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        pingreq_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        #nu are header variabil

        #nu are payload
        return pingreq_decode

class PINGRESP(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)

    def createPacketPingresp(self):
        # headerfix
        self.FixedHeader = HeaderFix(13, 0, 0)

        # nu are header variabil

        # nu are payload

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        # nu header variabil

        # nu are payload

        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + "Nu are" + "}"
        return result

    def stringPayload(self):
        result = ' Payload: {' + "Nu are" + "}"
        return result

    def string(self):
        result = "PachetPingresp{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodePingresp(ABC):
    def type(self):
        return 13
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        pingresp_decode = PINGRESP()
        pingresp_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        pingresp_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        pingresp_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        #nu are header variabil

        #nu are payload
        return pingresp_decode

class DISCONNECT(ABC):
    def __init__(self):
        self.FixedHeader = HeaderFix(0, 0, 0)

    def createPacketDisconnect(self):
        # headerfix
        self.FixedHeader = HeaderFix(14, 0, 0)

        # nu are header variabil

        # nu are payload

    def encode(self):
        encoded = ''
        # codific headerul fix
        encoded += format(self.FixedHeader.GetControlPacketType(), '04b')  # control_packet_type
        encoded += format(self.FixedHeader.GetFlags(), '04b')  # flags
        encoded += encodeRemainingLength(self.FixedHeader.GetRemainingLength())  # remaining_length

        # nu header variabil

        # nu are payload

        return encoded

    def stringHeaderVariabil(self):
        result = ' Header Variabil: {' + "Nu are" + "}"
        return result

    def stringPayload(self):
        result = ' Payload: {' + "Nu are" + "}"
        return result

    def string(self):
        result = "PachetDisconnect{" + self.FixedHeader.string() + ", " + self.stringHeaderVariabil() + "," + self.stringPayload() + "}"
        return result
class DecodeDisconnect(ABC):
    def type(self):
        return 14
    def decode(self, encoded = ''):
        #decodific tot ce reprezinta header fix
        disconnect_decode = DISCONNECT()
        disconnect_decode.FixedHeader.SetControlPacketType(int(encoded[0:4],2))
        encoded = encoded[4:]
        disconnect_decode.FixedHeader.SetFlags(int(encoded[0:4],2))
        encoded = encoded[4:]
        disconnect_decode.FixedHeader.SetRemainingLength(int(encoded[0:8],2))
        encoded = encoded[8:]
        #nu are header variabil

        #nu are payload
        return disconnect_decode
if __name__ == '__main__':
    test = CONNECT()
    test.createPacketConnect('firstClient', 'Teodora', 'Teodora', 0, '11111111', '/register','hello world!',)
    print("pachet creat connect " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodeConnect()
    result = test_decode.decode(encode)
    print("pachet decodificat connect " +result.string())
    print()
    test = CONNACK()
    test.createPacketConnack(2,5)
    print("pachet creat connack " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodeConnack()
    result = test_decode.decode(encode)
    print("pachet decodificat connack " + result.string())
    print()
    test = PUBLISH()
    test.createPacketPublish( 1,1, 1,"topic_name",1, "app_message")
    print("pachet creat publish " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodePublish()
    result = test_decode.decode(encode)
    print("pachet decodificat publish " + result.string())
    print()
    test = PUBACK()
    test.createPacketPuback(1)
    print("pachet creat puback " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodePuback()
    result = test_decode.decode(encode)
    print("pachet decodificat puback " + result.string())
    print()
    test = PUBREC()
    test.createPacketPubrec(1)
    print("pachet creat pubrec " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodePubrec()
    result = test_decode.decode(encode)
    print("pachet decodificat pubrec " + result.string())
    print()
    test = PUBREL()
    test.createPacketPubrel(1)
    print("pachet creat pubrel " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodePubrel()
    result = test_decode.decode(encode)
    print("pachet decodificat pubrel " + result.string())
    print()
    test = PUBCOMP()
    test.createPacketPubcomp(1)
    print("pachet creat pubcomp " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodePubcomp()
    result = test_decode.decode(encode)
    print("pachet decodificat pubcomp " + result.string())
    print()
    test = SUBSCRIBE()
    test.createPacketSubscribe(1,["verific", 'testez', 'incerc'], [0,1,2])
    print("pachet creat subscribe " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodeSubscribe()
    result = test_decode.decode(encode)
    print("pachet decodificat subscribe " + result.string())
    print()
    test = SUBACK()
    test.createPacketSuback(1, ["verific", 'testez', 'incerc'])
    print("pachet creat suback " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodeSuback()
    result = test_decode.decode(encode)
    print("pachet decodificat suback " + result.string())
    print()
    test = UNSUBSCRIBE()
    test.createPacketUnsubscribe(1, ["verific", 'testez', 'incerc'])
    print("pachet creat unsubscribe " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodeUnsubscribe()
    result = test_decode.decode(encode)
    print("pachet decodificat unsubscribe " + result.string())
    print()
    test = UNSUBACK()
    test.createPacketUnsuback(1)
    print("pachet creat unsuback " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodeUnsuback()
    result = test_decode.decode(encode)
    print("pachet decodific unsuback " + result.string())
    print()
    test = PINGREQ()
    test.createPacketPingreq()
    print("pachet creat pingreq " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodePingreq()
    result = test_decode.decode(encode)
    print("pachet decodific pingreq " + result.string())
    print()
    test = PINGRESP()
    test.createPacketPingresp()
    print("pachet creat pingresp " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodePingresp()
    result = test_decode.decode(encode)
    print("pachet decodific pingresp " + result.string())
    print()
    test = DISCONNECT()
    test.createPacketDisconnect()
    print("pachet creat disconnect " + test.string())
    encode = test.encode()
    print(encode)
    test_decode = DecodeDisconnect()
    result = test_decode.decode(encode)
    print("pachet decodific disconnect " + result.string())
    print()



