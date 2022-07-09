import serial
import time

class SerialRelais():
    def __init__(self, device='/dev/ttyACM0', baudrate=115200,duration=15):
        self._ser = serial.Serial(device,baudrate=baudrate,timeout=0.5)
        self.duration = duration
        #welcome message #
        welcome = ""
        while welcome.find('Ready')<0:
            welcome = str(self._ser.readline())
            time.sleep(0.1)
        self._send_serial_command("set_duration {0}".format(duration))

    def _send_serial_command(self,command):
        command += '\r\n'
        try:
            self._ser.write(bytes(command,'ascii'))
            return self._ser.readline()
        except serial.SerialTimeoutException as e:
            print("exception!")
        return

    def set_duration(self,duration):
        cmd = 'set_duration {0}'.format(duration)
        self._send_serial_command(cmd)

    def hit_relais(self,chs):
        cmd = 'hit_relais ' + ' '.join([str(ch) for ch in chs])
        self._send_serial_command(cmd)


class SerialXylofone(object):
    def __init__(self,port):
        self._port = port
        self._ser_relais = SerialRelais(self._port)
        self._key_range = 22
        self._min_key_number = 52 # C5 in key numbers, not in midi numbers! Midi numbers are key numbers + 9
        self._max_key_number = self._min_key_number + self._key_range

    def play_key(self,key_number):
        relais_number = key_number - self._min_key_number
        if self._min_key_number<= key_number <= self._max_key_number:
            self._ser_relais.hit_relais([relais_number])
        else:
            raise Exception('key {0} does not exist.'.format(key_number))

    def play_wrapped_key_number(self, key_number):
        #print('original: ',key_number)
        while key_number < self._min_key_number:
            key_number += 12
        while key_number > self._max_key_number:
            key_number -= 12
        #print("playing: ", key_number)
        self.play_key(key_number)


