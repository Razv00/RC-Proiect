from abc import ABC
class HeaderFix(ABC):
    control_packet_type : int
    flags : int
    remaining_length : int
    def __init__(self,_control_packet_type, _flags,_remaining_length):
        self.SetControlPacketType(_control_packet_type)
        self.SetFlags(_flags)
        self.SetRemainingLength(_remaining_length)
    def SetControlPacketType(self,_control_packet_type):
        
            if _control_packet_type in range(0,16):
                self.control_packet_type = _control_packet_type
            else:
             raise ValueError("Your control packet type must be between 0 and 15")

    def SetFlags(self, flags):
        
        if flags in range(0, 16):
            self.flags = flags
        else:
            raise ValueError("Your flag must be between 0 and 15")

    def SetRemainingLength(self, _remaining_length):
        self.remaining_length = _remaining_length

    def GetControlPacketType(self):
        return self.control_packet_type
    def GetFlags(self):
        return self.flags
    def GetRemainingLength(self):
        return self.remaining_length


class HeaderVariabil(ABC):
    all_fields: dict
    all_lengths: dict
    def __init__(self):
        self.all_fields = {}
        self.all_lengths = {}
    def SetField(self,field_name, field_value, field_length):
        self.all_fields[field_name] = field_value
        self.all_lengths[field_name] = field_length
    def GetField(self, field_name):
        return self.all_fields[field_name]
    def GetLengthField(self, field_name):
        return self.all_lengths[field_name]
   
    def GetLength(self):
        use_length = 0
        for _ in self.all_fields:
            use_length = use_length + self.all_lengths[_]
        return use_length
    def GetFields(self):
        return self.all_fields
    def GetLengths(self):
        return self.all_lengths

class Payload(ABC):
    all_fields: dict
    all_lengths: dict
    def __init__(self):
        self.all_fields = {}
        self.all_lengths = {}
    def SetField(self,field_name, field_value, field_length):
        self.all_fields[field_name] = field_value
        self.all_lengths[field_name] = field_length
    def GetField(self, field_name):
        return self.all_fields[field_name]
    def GetLengthField(self, field_name):
        return self.all_lengths[field_name]
   
    def GetLength(self):
        use_length = 0
        for _ in self.all_fields:
            use_length = use_length + self.all_lengths[_]
        return use_length
    def GetFields(self):
        return self.all_fields
    def GetLengths(self):
        return self.all_lengths

class ControlPacket(ABC):
    headerfix: HeaderFix()
    headervariabil : HeaderVariabil()
    payload : Payload()
    def __init__(self, _headerfix, _headervariabil, _payload):
        self.headerfix = _headerfix
        self.headervariabil = _headervariabil
        self.payload = _payload
    def GetControlPacketType(self):
        return self.GetControlPacketType()
    def GetHeaderFix(self):
        return self.headerfix
    def GetHeaderVariabil(self):
        return self.headervariabil
    def GetPayload(self):
        return self.payload