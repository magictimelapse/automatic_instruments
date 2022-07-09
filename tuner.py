import sounddevice as sd
import numpy as np
import scipy.fftpack
import os
import threading
import re
import math
class Tuner():
    def __init__(self):
        self._current_pitch = -1
        self._current_closest_pitch = -1
        self._current_closest_note = "K"

        self.SAMPLE_FREQ = 44100  # sample frequency in Hz
        self.WINDOW_SIZE = 44100  # window size of the DFT in samples
        self.WINDOW_STEP = 21050  # step size of window
        #self.WINDOW_STEP = self.WINDOW_SIZE/2  # step size of window
        self.WINDOW_T_LEN = self.WINDOW_SIZE / self.SAMPLE_FREQ  # length of the window in seconds
        self.SAMPLE_T_LENGTH = 1 / self.SAMPLE_FREQ  # length between two samples in seconds
        self.windowSamples = [0 for _ in range(self.WINDOW_SIZE)]
    # This function finds the closest note for a given pitch
    # Returns: note (e.g. A4, G#3, ..), pitch of the tone
        self.CONCERT_PITCH = 440
        self.ALL_NOTES = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]

    def find_closest_note(self,pitch):
          i = int(np.round(np.log2(pitch/self.CONCERT_PITCH)*12))
          closest_note = self.ALL_NOTES[i%12] + str(4 + (i + 9) // 12)
          closest_pitch = self.CONCERT_PITCH*2**(i/12)
          return closest_note, closest_pitch

    def key_number_of_note(self,note):
        note_name = re.sub(r'[0-9]', '', note)
        octave = int(re.findall(r'\d+', note)[0])
        index_of_note_in_octave = self.ALL_NOTES.index(note_name)
        if index_of_note_in_octave < 3:
            key_number = index_of_note_in_octave + 12 + ((octave - 1) * 12) + 1
        else:
            key_number = index_of_note_in_octave + ((octave - 1) * 12) + 1
        return key_number

    def note_of_key_number(self,key_number):
        return self.find_closest_note(self.frequency_of_key_number(key_number))[0]

    def frequency_of_key_number(self,key_number):
        return self.CONCERT_PITCH * math.pow(2, ((key_number - 49.) / 12.))

    def frequency_of_note(self,note):
        key_number = self.key_number_of_note(note)
        return self.frequency_of_key_number(key_number)
        #print(note_name,octave,index_of_note_in_octave)



# The sounddecive callback function
# Provides us with new data once WINDOW_STEP samples have been fetched
    def callback(self,indata, frames, time, status):
      #global windowSamples
      if status:
        print(status)
      if any(indata):
        self.windowSamples = np.concatenate((self.windowSamples,indata[:, 0])) # append new samples
        self.windowSamples = self.windowSamples[len(indata[:, 0]):] # remove old samples
        magnitudeSpec = abs( scipy.fftpack.fft(self.windowSamples)[:len(self.windowSamples)//2] )

        for i in range(int(62/(self.SAMPLE_FREQ/self.WINDOW_SIZE))):
          magnitudeSpec[i] = 0 #suppress mains hum

        maxInd = np.argmax(magnitudeSpec)
        maxFreq = maxInd * (self.SAMPLE_FREQ/self.WINDOW_SIZE)
        closestNote, closestPitch = self.find_closest_note(maxFreq)
        self._current_pitch = maxFreq
        self._current_closest_pitch = closestPitch
        self._current_closest_note = closestNote
        #os.system('cls' if os.name=='nt' else 'clear')
        #print(f"Closest note: {closestNote} {maxFreq:.1f}/{closestPitch:.1f}")
        self._done = True
      #else:
      #  print('no input')
    def current_pitch_clostest_pitch_closest_note(self):
        return self._current_pitch, self._current_closest_pitch, self._current_closest_note

    def current_pitch(self):
        return self._current_pitch
    def current_closest_pitch(self):
        return self._current_closest_pitch
    def current_closest_note(self):
        return self._current_closest_note

    def record_one_sample(self):
       # Start the microphone input stream
        self._done = False
        try:
          with sd.InputStream(channels=1, callback=self.callback,
            blocksize=self.WINDOW_STEP,
            samplerate=self.SAMPLE_FREQ):
            while not self._done:
                pass
        except Exception as e:
            print(str(e))
        return self.current_pitch_clostest_pitch_closest_note()

if __name__=="__main__":
    flute_tuner = Tuner()
    while True:
        current_pitch, current_closest_pitch, current_closest_note  = flute_tuner.record_one_sample()

        print(current_pitch,current_closest_pitch,current_closest_note)


