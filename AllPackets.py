from StructureOfAnControlPacket import *
class CONNECT(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
        if _header_fix.GetControlPacketType() != 1 :
            raise Exception("This packet has the  type 0001")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 0:
            raise Exception("This packet has the remaining length 0000")
        self.headerfix = _header_fix
    def HeaderVariabil(self,connect_flags, keepAlive):
       
        self.headervariabil.SetField("Protocol_Name", "MQTT", 2)

       
        self.headervariabil.SetField("Level",4, 1)

       
        self.headervariabil.SetField("Connect_Flags", int(connect_flags), 1)

        
        self.headervariabil.SetField("Keep_Alive", keepAlive, 2)

    def Payload(self, client_Id, will_Topic="", will_Message="", username="", password=""):
        
        pass
    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())

class CONNACK(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
       
        if _header_fix.GetControlPacketType() != 2:
            raise Exception("This packet has the  type 0010")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 2:
            raise Exception("This packet has the remaining length 0010")
        self.headerfix = _header_fix
    def HeaderVariabil(self, SP, connect_return_code):
        
        self.headervariabil.setField("Connect_Acknowledge_Flags",SP , 1)
        self.headervariabil.setField("Connect_Return_Code",connect_return_code , 1)

    def Payload(self):
       
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())

class PUBLISH(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, DUP_flag, QoS_level, RETAIN, _header_fix):
      
        if _header_fix.GetControlPacketType() != 3:
            raise Exception("This packet has the  type 0011")
        if _header_fix.GetRemainingLength() != 0:
            raise Exception("This packet has the remaining length 0000")
		 if QoS_level == 0:
            DUP_flag = 0	
        self.headerfix = _header_fix
    def HeaderVariabil(self):
       
        pass

    def Payload(self):
       
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())

class PUBACK(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
        
        if _header_fix.GetControlPacketType() != 4:
            raise Exception("This packet has the  type 0100")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 2:
            raise Exception("This packet has the remaining length 0010")
        self.headerfix = _header_fix
    def HeaderVariabil(self,packet_ID):
        self.headervariabil.setField("Packet_Identifier", packet_ID, 2)

    def Payload(self):
        #The PUBACK Packet has no payload
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())



class PUBREC(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
       
        if _header_fix.GetControlPacketType() != 5:
            raise Exception("This packet has the  type 0101")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 2:
            raise Exception("This packet has the remaining length 0010")
        self.headerfix = _header_fix

    def HeaderVariabil(self, packet_ID):
        
        self.headervariabil.setField("Packet_Identifier", packet_ID, 2)

    def Payload(self):
        #The PUBREC Packet has no payload.
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())



class PUBREL(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
        
        if _header_fix.GetControlPacketType() != 6:
            raise Exception("This packet has the  type 0110")
        if _header_fix.GetFlags() != 2:
            raise Exception("This packet has the flag 0010")
        if _header_fix.GetRemainingLength() != 2:
            raise Exception("This packet has the remaining length 0010")
        self.headerfix = _header_fix

    def HeaderVariabil(self, packet_ID):
        
        self.headervariabil.setField("Packet_Identifier", packet_ID, 2)

    def Payload(self):
        #The PUBREL Packet has no payload.
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())


class PUBCOMP(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
        
        if _header_fix.GetControlPacketType() != 7:
            raise Exception("This packet has the  type 0111")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 2:
            raise Exception("This packet has the remaining length 0010")
        self.headerfix = _header_fix

    def HeaderVariabil(self, packet_ID):
       
        self.headervariabil.setField("Packet_Identifier", packet_ID, 2)

    def Payload(self):
        #The PUBCOMP Packet has no payload.
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())



class SUBSCRIBE(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
       
        if _header_fix.GetControlPacketType() != 8:
            raise Exception("This packet has the  type 1000")
        if _header_fix.GetFlags() != 2:
            raise Exception("This packet has the flag 0010")
        if _header_fix.GetRemainingLength() != 0:
            raise Exception("This packet has the remaining length 0000")
        self.headerfix = _header_fix

    def HeaderVariabil(self, packet_ID):
        # byte 1 Packet Identifier MSB, byte 2 Packet Identifier LSB
        self.headervariabil.setField("Packet_Identifier", packet_ID, 2)

    def Payload(self,topic_filter, requested_QoS):
        # to do
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())



class SUBACK(ABC):
        headerfix: HeaderFix()
        headervariabil: HeaderVariabil()
        payload: Payload()

        def __init__(self):
            self.headerfix = HeaderFix()
            self.headervariabil = HeaderVariabil()
            self.payload = Payload()

        def HeaderFix(self, _header_fix):
            if _header_fix.GetControlPacketType() != 9:
                raise Exception("This packet has the  type 1001")
            if _header_fix.GetFlags() != 0:
                raise Exception("This packet has the flag 0000")
            if _header_fix.GetRemainingLength() != 0:
                raise Exception("This packet has the remaining length 0000")
            self.headerfix = _header_fix

        def HeaderVariabil(self, packet_ID):
            # byte 1 Packet Identifier MSB, byte 2 Packet Identifier LSB
            self.headervariabil.setField("Packet_Identifier", packet_ID, 2)

        def Payload(self,return_code):
           
            pass

        def SetRemainingLength(self):
            return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())



class UNSUBSCRIBE(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
       
        if _header_fix.GetControlPacketType() != 10:
            raise Exception("This packet has the  type 1010")
        if _header_fix.GetFlags() != 2:
            raise Exception("This packet has the flag 0010")
        if _header_fix.GetRemainingLength() != 0:
            raise Exception("This packet has the remaining length 0000")
        self.headerfix = _header_fix

    def HeaderVariabil(self, packet_ID):
        # byte 1 Packet Identifier MSB, byte 2 Packet Identifier LSB
        self.headervariabil.setField("Packet_Identifier", packet_ID, 2)

    def Payload(self, topic_filter):
        
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())



class UNSUBACK(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
      
        if _header_fix.GetControlPacketType() != 11:
            raise Exception("This packet has the  type 1011")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 2:
            raise Exception("This packet has the remaining length 0010")
        self.headerfix = _header_fix

    def HeaderVariabil(self, packet_ID):
        
        self.headervariabil.setField("Packet_Identifier", packet_ID, 2)

    def Payload(self):
        #The UNSUBACK Packet has no payload.
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())


class PINGREQ(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
        
        if _header_fix.GetControlPacketType() != 12:
            raise Exception("This packet has the  type 1100")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 0:
            raise Exception("This packet has the remaining length 0000")
        self.headerfix = _header_fix
    def HeaderVariabil(self):
        #The PINGREQ Packet has no variable header.
        pass

    def Payload(self):
        #The PINGREQ Packet has no payload.
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())



class PINGRESP(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
        
        if _header_fix.GetControlPacketType() != 13:
            raise Exception("This packet has the  type 1101")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 0:
            raise Exception("This packet has the remaining length 0000")
        self.headerfix = _header_fix

    def HeaderVariabil(self):
        # The PINGRESP Packet has no variable header.
        pass

    def Payload(self):
        # The PINGRESP Packet has no payload.
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())



class DISCONNECT(ABC):
    headerfix: HeaderFix()
    headervariabil: HeaderVariabil()
    payload: Payload()
    def __init__(self):
        self.headerfix =HeaderFix()
        self.headervariabil = HeaderVariabil()
        self.payload = Payload()

    def HeaderFix(self, _header_fix):
        
        if _header_fix.GetControlPacketType() != 14:
            raise Exception("This packet has the  type 1110")
        if _header_fix.GetFlags() != 0:
            raise Exception("This packet has the flag 0000")
        if _header_fix.GetRemainingLength() != 0:
            raise Exception("This packet has the remaining length 0000")
        self.headerfix = _header_fix

    def HeaderVariabil(self):
        # The DISCONNECT Packet has no variable header.
        pass

    def Payload(self):
        # The DISCONNECT Packet has no payload.
        pass

    def SetRemainingLength(self):
        return self.headerfix.SetRemainingLength(self.headervariabil.GetLength() + self.payload.GetLength())


