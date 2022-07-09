import serial
import time

class SerialFluteInterface(object):
    def __init__(self,port='COM4'):
        self._port = port
        #self._key_number_to_position = dict([(49, 18), (50, 38), (51, 56), (52, 75), (53, 92), (54, 109), (55, 125), (56, 141), (57, 157), (58, 172),
        # (59, 193), (60, 229)])
        self._key_number_to_position = dict([(49, 17), (50, 38), (51, 55), (52, 75), (53, 93), (54, 109), (55, 125), (56, 141), (57, 156), (58, 170),
         (59, 188), (60, 216)])

        self._min_key_number = min(self._key_number_to_position)
        self._max_key_number = max(self._key_number_to_position)
        self._min_position = 0
        self._max_position = 240
        self._old_position = self._max_position

        self._servoOnPosition = 100
        self._servoOffPosition = 65
    def __enter__(self):
        self._ser = serial.Serial(self._port, baudrate=115200,timeout=8)
        ans = self._ser.readline() ## wait for ready
        self.servo_off()
        return self

    def _send_command(self,command):
        command += "\r\n"
        bcommand = command.encode('ascii')
        self._ser.write(bcommand)
        ans = self._ser.readline()

    def fan_speed(self,speed):
        self._send_command('f {0}'.format(speed))

    def servo_off(self):
        self._send_command('a {0}'.format(self._servoOffPosition))

    def servo_on(self):
        self._send_command('a {0}'.format(self._servoOnPosition))

    def pos(self,pos):
        #if pos < self._old_position:
        #    in_pos = max(0, pos - 10)
        #    self._send_command('p {0}'.format(in_pos))
        self._send_command('p {0}'.format(pos))
        self._old_position = pos

    def goto_key(self,key_number):
        pos = self._key_number_to_position.get(key_number)
        if not pos is None:
            self.pos(pos)
        else:
            raise Exception('key {0} does not exist.'.format(key_number))

    def goto_wrapped_key_number(self,key_number):
        #print('original: ',key_number)
        while key_number < self._min_key_number:
            key_number += 12
        while key_number > self._max_key_number:
            key_number -= 12
        #print("playing: ", key_number)
        self.goto_key(key_number)


    def __exit__(self, exc_type, exc_value, tb):
        #print(exc_type,exc_value,tb)
        self.fan_speed(0)
        self.pos(0)
        self._ser.close()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            # return False # uncomment to pass exception through

        return True


if __name__=="__main__":
    with SerialFluteInterface('COM4') as flute:
        flute.fan_speed(200)
        time.sleep(1)
        flute.pos(100)
        time.sleep(1)
        flute.fan_speed(0)
        flute.pos(0)
        time.sleep(1)
        for pos in range(0,220,2):
            print(pos)
            flute.pos(pos)
            time.sleep(0.1)
    #time.sleep(5)
