import numpy as np
import pyaudio
import math
import threading
import time

# Parameters
duration = 1  # seconds
sampling_rate = 44100  # samples per second (standard for audio)
frequency = 220.0  # frequency of the sound (A3 note)
chunk_size = 1024  # Number of frames per buffer
waveform = np.sin(2 * np.pi * frequency * np.linspace(0, duration, int(sampling_rate * duration), endpoint=False))

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for stereo output
stream = p.open(format=pyaudio.paFloat32,
                channels=2,  # Stereo output
                rate=sampling_rate,
                output=True,
                frames_per_buffer=chunk_size)

# Globals to handle volume and playback state
left_volume = 1
right_volume = 1
start_index = 0
beep = False

def update_volume(angle, beep_val=False):
    """Update the stereo volumes based on angle input (in degrees)."""
    global left_volume, right_volume, beep
    left_volume = math.fabs(math.sin(math.radians(angle)))
    right_volume = math.fabs(math.cos(math.radians(angle)))
    beep = beep_val

def create_stereo_chunk(chunk, left_vol, right_vol):
    """Create stereo audio chunk by applying left and right volume."""
    stereo_chunk = np.zeros((len(chunk), 2))
    stereo_chunk[:, 0] = left_vol * chunk  # Left channel
    stereo_chunk[:, 1] = right_vol * chunk  # Right channel
    return stereo_chunk

def play_sound():
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
            beep = False

# Thread to update volume in real time
def volume_control():
    while True:
        # Example of volume update; you can replace it with actual logic
        for angle in range(0, 360, 1):
            update_volume(angle)
            time.sleep(0.01)  # Simulate real-time updates (can be customized)

if __name__ == "__main__":
    try:
        # Start audio playback in a separate thread
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()

        # Start volume control in another thread
        #volume_thread = threading.Thread(target=volume_control)
        #volume_thread.start()

        # Join threads (this will keep the main program running)
        sound_thread.join()
        #volume_thread.join()

    finally:
        # Close the stream and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()
