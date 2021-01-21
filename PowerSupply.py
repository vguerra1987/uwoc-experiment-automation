import socket


# PowerSupply control
class PowerSupply(object):

    # Constructor
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (ip, port)

    def connect(self):
        try:
            self.socket.connect(self.server_address)
            return True
        except socket.timeout:
            return False

    # Period must be expressed in milliseconds, duty in percentage, and current in mA
    def initial_configuration(self, period, duty, current):
        self.send_to_device(':CHAN1:SOUR:FUNC CURR')
        self.send_to_device(':TRIG:TIM1 {:2.2g}ms'.format(period))
        self.send_to_device(':CHAN1:SOUR:CURR:PULS:WIDT {:2.2g}ms'.format(duty*period))
        self.send_to_device(':CHAN1:SOUR:CURR:LEV {:2.2g}mA'.format(current))
        self.send_to_device(':CHAN1:SOUR:CURR:PULS:BASE 1nA')

    def set_duty(self, duty, period):
        self.send_to_device(':CHAN1:SOUR:CURR:PULS:WIDT {:2.2g}ms'.format(duty * period))

    def send_to_device(self, query):
        print(query)
        self.socket.sendmsg([query.encode(), "\r\n".encode()])

    def output(self, state):
        self.send_to_device(':CHAN1:OUTP {}'.format('ON' if state else 'OFF'))


if __name__ == "__main__":
    # We create the device controller
    ps = PowerSupply('192.168.10.60', 7655)

    # If connection fails, we get out
    if ps.connect():
        print("Connected to the device!")
    else:
        print("An error occurred, check connectivity")
        raise Exception

    ps.initial_configuration(period=1, duty=0.5, current=50)

    ps.output(0)
