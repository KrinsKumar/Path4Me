import math
import time
import wave

import numpy as np
import pyaudio

# Path to your .wav file
audio_file_path = "./music.wav"

# Open the .wav file
wav_file = wave.open(audio_file_path, 'rb')

# Setup PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wav_file.getsampwidth()),
                channels=wav_file.getnchannels(),
                rate=wav_file.getframerate(),
                output=True)

# Read the .wav file in chunks
chunk_size = 1024

# Initialize volume control
left_volume = 1
right_volume = 1
start_index = 0
beep = False

def update_volume(angle, beep_val=False):
    global left_volume, right_volume, beep

    left_volume = math.fabs(math.sin(math.radians(angle)))
    right_volume = math.fabs(math.cos(math.radians(angle)))

    beep = beep_val

def create_sound():
    global left_volume, right_volume, beep

    # Read the .wav file in chunks
    data = wav_file.readframes(chunk_size)
    angle=0
    while data:
        angle+=0.2
        angle%=360
        update_volume(angle)
        # Convert binary data to numpy array for manipulation
        chunk = np.frombuffer(data, dtype=np.int16).copy()  # Make the array writable

        # Reshape into stereo (2 channels)
        stereo_chunk = chunk.reshape((-1, 2))

        # Adjust the stereo volume for left and right channels
        stereo_chunk[:, 0] = left_volume * stereo_chunk[:, 0]  # Left channel
        stereo_chunk[:, 1] = right_volume * stereo_chunk[:, 1]  # Right channel

        # Write the modified chunk to the audio stream
        stream.write(stereo_chunk.astype(np.int16).tobytes())

        # Read the next chunk of data from the .wav file
        data = wav_file.readframes(chunk_size)

        if beep:
            stream.stop_stream()
            time.sleep(0.5)
            stream.start_stream()


if __name__ == "__main__":
    angle=0
    try:
        # Play the sound with spatial navigation
        while True:
            angle+=1
            angle%=360
            create_sound()

    finally:
        # Clean up resources
        stream.stop_stream()
        stream.close()
        p.terminate()
        wav_file.close()