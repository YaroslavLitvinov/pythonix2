__author__ = 'JekaX'


from FreeBSDDev import FreeBSDDev
from LinuxDev import LinuxDev
from MikroTikDev import MikroTikDev

class ActionDevice():


    def __init__(self,type_device):
        self.type_device = type_device
        if type_device == "mikrotik":
            self.dev_obj = MikroTikDev()
        elif type_device == "freebsd":
            self.dev_obj = FreeBSDDev()
        elif type_device == "linux":
            self.dev_obj = LinuxDev()



if __name__ == "__main__":
    action_dev = ActionDevice("linux")
    action_dev.dev_obj.add_client()