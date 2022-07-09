from tuner import Tuner
from floete_interface import SerialFluteInterface

import time

def get_average_pitch(flute_tuner,n_samples,min_pitch=50):
    flute_tuner.record_one_sample()
    average_pitch = 0
    ii = 0
    while ii < n_samples:
        current_pitch, current_closest_pitch, current_closest_note = flute_tuner.record_one_sample()
        # current_pitch, current_closest_pitch, current_closest_note = flute_tuner.current_pitch_clostest_pitch_closest_note()
        if current_pitch> min_pitch:
            average_pitch += current_pitch
            ii += 1
        # print(current_pitch, current_closest_pitch, current_closest_note)
    average_pitch /= n_samples
    return average_pitch


if __name__ == "__main__":

    fan_speed = 3000

    with SerialFluteInterface('COM4') as flute:
        flute.fan_speed(fan_speed)
        flute.servo_on()
        pos_min = flute._min_position
        pos_max = flute._max_position

        flute.pos(pos_min)
        flute_tuner = Tuner()
        ## find the min frequency and the max frequency ##
        ## Take n samples and average ##
        average_pitch = 0
        n_samples = 1
        average_pitch = get_average_pitch(flute_tuner,n_samples)
        print(average_pitch)
        closest_note,closest_pitch = flute_tuner.find_closest_note(average_pitch)
        print(average_pitch, closest_pitch, closest_note)
        if closest_pitch < average_pitch:
            lowest_key_number = flute_tuner.key_number_of_note(closest_note) + 1
        else:
            lowest_key_number = flute_tuner.key_number_of_note(closest_note)




        flute.pos(pos_max)
        time.sleep(1)
        flute_tuner.record_one_sample()
        average_pitch = get_average_pitch(flute_tuner,n_samples,min_pitch=500)
        flute.fan_speed(0)
        #bla


        closest_note, closest_pitch = flute_tuner.find_closest_note(average_pitch)
        print(average_pitch, closest_pitch, closest_note)
        if closest_pitch > average_pitch:
            highest_key_number = flute_tuner.key_number_of_note(closest_note) -1
        else:
            highest_key_number = flute_tuner.key_number_of_note(closest_note)

        print(lowest_key_number,highest_key_number)
        lowest_note = flute_tuner.note_of_key_number(lowest_key_number)
        highest_note = flute_tuner.note_of_key_number(highest_key_number)
        print(lowest_note,highest_note)

        ## and now start tuning ##
        flute.fan_speed(fan_speed)
        time.sleep(1)
        key_number_positions = []
        position = 0
        current_min_pitch = 0
        for key_number in range(lowest_key_number,highest_key_number+1):
            frequency_to_find = flute_tuner.frequency_of_key_number(key_number)
            matched_frequency = False
            #position = 0
            while not matched_frequency:
                #flute.pos(0)
                #time.sleep(0.5)
                if(position<pos_min or position>pos_max+5):
                    raise Exception("position outside range!")
                if position < 10:
                    flute.pos(0)
                    time.sleep(0.2)
                else:
                    flute.pos(position - 10)
                    time.sleep(0.2)
                print(position)
                flute.pos(position)
                time.sleep(0.1)
                print('recording...')
                average_pitch = get_average_pitch(flute_tuner,n_samples,min_pitch=current_min_pitch)
                if average_pitch > current_min_pitch:
                    current_min_pitch = average_pitch - 10
                print('average pitch: ', average_pitch, ' searching for:',frequency_to_find)
                #current_pitch, current_closest_pitch, current_closest_note = flute_tuner.current_pitch_clostest_pitch_closest_note()
                if average_pitch < frequency_to_find:
                    position += 1
                else:
                    matched_frequency = True
                    key_number_positions.append((key_number,position))
                    print("pitch found")
                    print(frequency_to_find, average_pitch)
                    print(key_number, position)
        print(key_number_positions)


