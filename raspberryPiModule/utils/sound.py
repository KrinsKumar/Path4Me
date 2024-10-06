import numpy as np
import pyaudio
import math
import time

# Parameters
duration = 1  # seconds
sampling_rate = 44100  # samples per second (standard for audio)
frequency = 220.0  # frequency of the sound (A4)
chunk_size = 8192  # Increased chunk size to reduce underrun errors
current_byte = 0

# Generate the waveform for the entire duration
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
waveform = np.sin(2 * np.pi * frequency * t)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for stereo output
stream = p.open(format=pyaudio.paFloat32,
                channels=2,  # Stereo (left and right channels)
                rate=sampling_rate,
                output=True,
                frames_per_buffer=chunk_size)

left_volume = 1
right_volume = 1
start_index = 0
beep = False

def update_volume(angle, beep_val=False):
    global beep, start_index, current_byte, chunk_size, waveform
    print("new volume: ", angle)

    left_volume = math.fabs(math.sin(math.radians(angle)))
    right_volume = math.fabs(math.cos(math.radians(angle)))

    beep = beep_val

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
    current_byte = stereo_chunk
    print("new byte ", current_byte)


def create_sound():
    global start_index, left_volume, right_volume, beep, current_byte

    while True:
        print("using byte: ", current_byte)
        stereo_chunk = current_byte 
        # Write the chunk to the audio stream
        try:
            stream.write(stereo_chunk.astype(np.float32).tobytes())
        except IOError as e:
            print(f"Stream write error: {e}")

        # Move to the next chunk
        start_index = end_index % len(waveform)

        if beep:
            stream.stop_stream()
            time.sleep(0.5)
            stream.start_stream()

if __name__ == "__main__":
    try:
        # Play the sound
        create_sound()
    finally:
        # Close the stream and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()