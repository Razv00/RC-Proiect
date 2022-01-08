from abc import ABC
class HeaderFix(ABC):
    def __init__(self,_control_packet_type , _flags ,_remaining_length):
        self.control_packet_type =_control_packet_type
        self.flags=_flags
        self.remaining_length =_remaining_length

    def SetControlPacketType(self, _control_packet_type):
        self.control_packet_type = _control_packet_type

    def SetFlags(self, flags):
            self.flags = flags

    def SetRemainingLength(self, _remaining_length):
        self.remaining_length = _remaining_length

    def GetControlPacketType(self):
        return self.control_packet_type

    def GetFlags(self):
        return self.flags

    def GetRemainingLength(self):
        return self.remaining_length

    def string(self):
        result = "HeaderFix{" + "[" + str(self.control_packet_type) + ", " + str(self.flags) + "][" + str(self.remaining_length) + "]" +"}\n"
        return result

if __name__ == "__main__":
    Header = HeaderFix(0,0,0)
    print(Header.string())