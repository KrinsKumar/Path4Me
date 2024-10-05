import numpy as np
import pyaudio
import math
import time

# Parameters
duration = 1  # seconds
sampling_rate = 44100  # samples per second (standard for audio)
frequency = 220.0  # frequency of the sound (A4)
chunk_size = 1024  # Smaller chunks of data to process per iteration

# Generate the waveform for the entire duration
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
waveform = np.sin(2 * np.pi * frequency * t)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for stereo output
stream = p.open(format=pyaudio.paFloat32,
                channels=2,  # Stereo (left and right channels)
                rate=sampling_rate,
                output=True)


start_index = 0
def create_sound(angle, beep=False):
    global start_index

    left_volume = math.fabs(math.sin(math.radians(angle)))
    right_volume = math.fabs(math.cos(math.radians(angle)))

    # Calculate the end index for the current chunk
    end_index = start_index + chunk_size

    # Check if we need to wrap around to the beginning of the waveform
    if end_index > len(waveform):
        chunk = np.concatenate((waveform[start_index:], waveform[:end_index % len(waveform)]))
    else:
        chunk = waveform[start_index:end_index]

    # Create the stereo chunk
    stereo_chunk = np.zeros((len(chunk), 2))
    stereo_chunk[:, 0] = left_volume * chunk  # Left channel
    stereo_chunk[:, 1] = right_volume * chunk  # Right channel

    # Write the chunk to the audio stream
    stream.write(stereo_chunk.astype(np.float32).tobytes())

    # Move to the next chunk
    start_index = end_index % len(waveform)

    if(beep):
        time.sleep(0.3)


angle = 210
while True:
  #angle += 0.3
  #angle %= 360
  #if(angle < 180):
    #create_sound(135, True)
    #angle += 10
  #else:
  create_sound(45)
