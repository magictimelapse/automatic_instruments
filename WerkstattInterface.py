import serial
import time

## interface for the moog Werkstatt, connected to an Arduino ###

class SerialWerkstattInterface:
    def __init__(self,port='COM4',baudrate = 115200):
        self._ser = serial.Serial(port, baudrate=baudrate, timeout=2.5)

        # welcome message #
        welcome = ""
        while welcome.find('ready') < 0:
            welcome = str(self._ser.readline())
            time.sleep(0.1)
        self._debug = False

    def _send_serial_command(self, command):
        command += '\r\n'
        try:
            self._ser.write(bytes(command, 'ascii'))
            if self._debug:
                return self._ser.readline()
        except serial.SerialTimeoutException as e:
            print("Serial Timeout!")

    def set_vcoe(self, vcoe):
        cmd = 'vcoe {0}'.format(vcoe)
        self._send_serial_command(cmd)

    def set_vca(self, vca):
        cmd = 'vca {0}'.format(vca)
        self._send_serial_command(cmd)

    def set_adsr(self,attack,sustain,release):
        cmd = 'adsr {0} {1} {2}'.format(attack,sustain,release)
        self._send_serial_command(cmd)

    def click(self):
        cmd = 'click'
        self._send_serial_command(cmd)


class Werkstatt:
    def __init__(self,port='COM4'):
        self._port = port
        self._DAC_values_difference_half_tone = 4
        self._vcoe_vals = list(range(0,256,self._DAC_values_difference_half_tone))
        self._note_offset = 13
        self._octave_offset = 0

    def __enter__(self):
        self._serial_werkstatt = SerialWerkstattInterface(self._port)

        self._serial_werkstatt.set_vca(0)
        #self._serial_werkstatt.set_vcoe(0)

        return self

    def __exit__(self, exc_type, exc_value, tb):
        self._serial_werkstatt.set_vca(0)
        #self._serial_werkstatt.set_vcoe(0)
        self._serial_werkstatt._ser.close()

        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            # return False # uncomment to pass exception through

        return True

    def set_adsr(self,attack,sustain,release):
        self._serial_werkstatt.set_adsr(attack,sustain,release)

    def set_octave_offset(self,octave_offset):
        self._octave_offset = octave_offset

    def note_on(self,note):

        note_to_set = (note-self._note_offset + self._octave_offset*12)*self._DAC_values_difference_half_tone
        while note_to_set < 0:
            note_to_set += self._DAC_values_difference_half_tone*12 # octaves
        while note_to_set>255:
            note_to_set -= self._DAC_values_difference_half_tone*12
        print(self._serial_werkstatt.set_vcoe(note_to_set))
    def set_volume(self, volume):
        print(self._serial_werkstatt.set_vca(volume))
    def note_off(self):
        self._serial_werkstatt.set_vca(0)

    def click(self):
        self._serial_werkstatt.click()