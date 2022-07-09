import mido
from floete_interface import SerialFluteInterface
from SerialXylofoneInterface import SerialXylofone
from WerkstattInterface import Werkstatt
from tuner import Tuner
import time
import threading
if __name__ == "__main__":
    tuner = Tuner()
    fan_off_timeout = 20
    with Werkstatt() as ws:
        click_track_channel = None
    #with SerialFluteInterface("COM4") as flute:
        #ws = Werkstatt()
        #xylofone = SerialXylofone("COM7")
        #mid = mido.MidiFile('midi/titanic-3.mid')
        #flute_channels = [0,2]
        #xylofone_channels = [10]
        #note_offset = 7  ## if you want to play in a different key

        #mid = mido.MidiFile('midi/Hallelujah.mid')


        mid = mido.MidiFile("midi/Ave-Maria-2_piano_flute.mid")
        flute_channels = [3]
        xylofone_channels = [0,2]
        note_offset = 3






        mid = mido.MidiFile('midi/Happy-Birthday-To-You-4.mid')
        flute_channels = [1]
        xylofone_channels = []
        note_offset = 0

        mid = mido.MidiFile("midi/Ave-Maria-2-JustFlute.mid")
        flute_channels = []
        xylofone_channels = []
        ws_channels = [3]
        note_offset =-3





        mid = mido.MidiFile('midi/BWV1067/BADINERI.mid')
        ws_channels = [4]
        xylofone_channels = [0,1,2,3]
        flute_channels = []
        for msg in mid:
            if msg.type == "program_change":
                print(msg)



        mid = mido.MidiFile("midi/GounodAveMaria.mid")
        flute_channels = []
        #xylofone_channels = []
        xylofone_channels = [0]
        ws_channels = [1]
        note_offset = 0
        ws.set_adsr(0.1, 4, 0.1)
        mid = mido.MidiFile("midi/GounodAveMaria.mid")
        flute_channels = []
        xylofone_channels = []
        # xylofone_channels = [0]
        ws_channels = [1]
        note_offset = 0
        ws.set_adsr(0.4, 4, 0.1)



        mid = mido.MidiFile('midi/BWV1067/BADINERI.mid')
        ws_channels = [4]
        ws.set_adsr(0.05,1,0.05)
        #xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = []
        flute_channels = []

        mid = mido.MidiFile('midi/bach-air-on-the-g-string.mid')
        ws_channels = [2]
        ws.set_adsr(0.3, 2, 2)
        ws.set_octave_offset = -2
        # xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = [3,4,5]
        flute_channels = []

        mid = mido.MidiFile('midi/vivaldi_4_stagioni_inverno_1_(c)pollen.mid')
        ws_channels = [1]
        ws.set_adsr(0.3, 2, 2)
        ws.set_octave_offset = -2
        # xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = list(range(3,4))
        flute_channels = []






        mid = mido.MidiFile('midi/vivaldi_4_stagioni_inverno_2_(c)pollen.mid')
        ws_channels = [1]
        ws.set_adsr(0.3, 2, 2)
        ws.set_octave_offset = -2
        # xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = list(range(3, 4))
        flute_channels = []

        mid = mido.MidiFile('midi/Tetris - Tetris Main Theme.mid')
        ws_channels = [0,1]
        ws.set_adsr(0.3, 2, 2)
        ws.set_octave_offset = -2
        # xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = list(range(3, 4))
        flute_channels = []

        """ 
        mid = mido.MidiFile('midi/mira.mid')
        ws_channels = [0]
        ws.set_adsr(0, 1, 0)
        # xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = []
        flute_channels = []
        for msg in mid:
            if msg.type == "program_change":
                print(msg)
        """
        mid = mido.MidiFile('midi/Faur-pav.mid')
        ws_channels = [0]
        ws.set_adsr(0.3, 2, 2)
        ws.set_octave_offset = -2
        # xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = []
        flute_channels = []
        note_offset = 1

        mid = mido.MidiFile('midi/Faur-pav-synth.mid')
        ws_channels = [0]
        ws.set_adsr(0.3, 2, 2)
        ws.set_octave_offset = -2
        # xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = []
        flute_channels = []
        note_offset = 1

        mid = mido.MidiFile('midi/pulp_fiction_misirlou.mid')
        # flute_channels = [6]
        # xylofone_channels = [5, 6]
        xylofone_channels = []
        flute_channels = []
        note_offset = 5
        ws_channels = [1, 6]
        ws.set_adsr(0.04, 0.04, 0.02)

        mid = mido.MidiFile('midi/bach-air-on-the-g-string.mid')
        ws_channels = [2]
        ws.set_adsr(0.3, 2, 2)
        ws.set_octave_offset = -2
        # xylofone_channels = [0, 1, 2, 3]
        xylofone_channels = []
        flute_channels = []

        mid = mido.MidiFile('midi/Happy-Birthday-To-You-4.mid')
        #flute_channels = [1]
        ws_channels=[1]
        xylofone_channels = []
        click_track_channel = 11 #is also on the ws
        note_offset = 0

        mid = mido.MidiFile('midi/Happy-Birthday-To-You-4_clicktrack.mid')
        #flute_channels = [1]
        ws_channels=[1]
        xylofone_channels = []
        click_track_channel = 10 #is also on the ws
        note_offset = 0
    # parse the header to analyse the instruments #


        #input("press enter")
        # channel to play #

        ws.note_off()
        #flute.fan_speed(3000)
        werkstatt_time_start = time.monotonic()
        max_time_diff = 0.05
        werkstatt_note_is_off = True
        last_werkstatt_velocity = 0
        min_time_diff_note_played = 0.01
        werkstatt_time_last_note_played_start = time.monotonic()
        for msg in mid.play():
            #print(msg)

            if hasattr(msg,'channel') and msg.channel in flute_channels:
                if msg.type == 'note_off' or ( msg.type == 'note_on' and msg.velocity == 0):
                    threading.Thread(target=flute.servo_off).start()
                    #

                elif msg.type == 'note_on':
                        threading.Thread(target=flute.servo_on).start()
                        #print(msg)
                        key_number = msg.note + note_offset
                        print('flute', key_number, tuner.note_of_key_number(key_number))

                        threading.Thread(target=flute.goto_wrapped_key_number, args=(key_number,)).start()

            # xylofone #
            if hasattr(msg, 'channel') and msg.channel in xylofone_channels:
                if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    pass
                elif msg.type == 'note_on':
                    key_number = msg.note + note_offset
                    print('xylofone',key_number, tuner.note_of_key_number(key_number))
                    threading.Thread(target=xylofone.play_wrapped_key_number, args=(key_number,)).start()

            # werkstatt #
            if hasattr(msg, 'channel') and msg.channel == click_track_channel:
                print('click')
                threading.Thread(ws.click()).start()
                #ws.click()
            if hasattr(msg, 'channel') and msg.channel in ws_channels:
                print(msg)
                if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    werkstatt_time_stop = time.monotonic()
                    if werkstatt_time_stop - werkstatt_time_start > max_time_diff:
                        threading.Thread(ws.note_off(), args =()).start()
                        werkstatt_note_is_off = True
                        last_werkstatt_velocity = 0

                elif msg.type == 'note_on':
                    werkstatt_time_last_note_played_stop = time.monotonic()
                    if werkstatt_time_last_note_played_stop - werkstatt_time_last_note_played_start > min_time_diff_note_played:
                        key_number = msg.note + note_offset
                        key_number -= 12
                        velocity = msg.velocity
                        #print('werkstatt',midi_number, tuner.note_of_key_number(key_number),velocity)
                        threading.Thread(target=ws.note_on, args=(key_number,)).start()

                        if werkstatt_note_is_off or velocity != last_werkstatt_velocity:
                            threading.Thread(target=ws.set_volume, args=(2*velocity,)).start() # factor 2: velocity has 7 bits, vca 8 bits
                            print('setting velocity to ',velocity)
                            werkstatt_note_is_off = False
                        last_werkstatt_velocity = velocity
                        werkstatt_time_start = time.monotonic()

