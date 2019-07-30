import pyaudio
import wave
import time
import sys
import os

# See if we can just make some white noise

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    data = bytes(bytearray(os.urandom(100000)))
    print("---------")
    
    return (data, pyaudio.paContinue)


stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True,
                stream_callback=callback)


stream.start_stream()

time.sleep(3)

stream.stop_stream()
stream.close()

p.terminate()