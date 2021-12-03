import time
class ClientMQTT:
    def __init__(self):
        self.isConnected = False
        self.keep_alive = 0
        self.packedId = 0
        self.keep_alive_flag = False


    def keep_alive_clock(self):
        while self.keep_alive_flag is True:
            wait_time = self.keep_alive / 2
            step = wait_time / 10
            while wait_time > 0 and self.keep_alive_flag is True:
                time.sleep(step)
                wait_time -= step
if __name__ == "__main__":
    pass