import numpy as np
import pyaudio
import math
import time
import threading

# Parameters
duration = 1  # seconds
sampling_rate = 44100  # samples per second (standard for audio)
frequency = 220.0  # frequency of the sound (A4)
chunk_size = 8192  # Increased chunk size to reduce underrun errors

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
    global left_volume, right_volume, beep

    left_volume = math.fabs(math.sin(math.radians(angle)))
    right_volume = math.fabs(math.cos(math.radians(angle)))

    beep = beep_val

def create_stereo_chunk(chunk, left_vol, right_vol):
    stereo_chunk = np.zeros((len(chunk), 2))
    stereo_chunk[:, 0] = left_vol * chunk  # Left channel
    stereo_chunk[:, 1] = right_vol * chunk  # Right channel
    return stereo_chunk

def create_sound():
    """Continuously generate and play sound with real-time volume updates."""
    global start_index, waveform, beep

    while True:
        # Calculate end index for the chunk
        end_index = (start_index + chunk_size) % len(waveform)

        # Fetch the next chunk from the waveform
        if end_index > start_index:
            chunk = waveform[start_index:end_index]
        else:
            chunk = np.concatenate((waveform[start_index:], waveform[:end_index]))

        # Create stereo chunk with current volume levels
        stereo_chunk = create_stereo_chunk(chunk, left_volume, right_volume)

        # Write the stereo chunk to the audio stream
        try:
            stream.write(stereo_chunk.astype(np.float32).tobytes())
        except IOError as e:
            print(f"Stream write error: {e}")

        # Update start index for the next chunk
        start_index = end_index

        # Optional beep functionality
        if beep:
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        # Run the create_sound function in a separate thread with higher priority
        sound_thread = threading.Thread(target=create_sound)
        sound_thread.daemon = True
        sound_thread.start()

        # Keep the main thread alive
        while True:
            time.sleep(1)
    finally:
        # Close the stream and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()