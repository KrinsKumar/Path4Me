import numpy as np
import pyaudio
import math
import time

# Parameters
duration = 1  # seconds
sampling_rate = 11050  # samples per second (standard for audio)
frequency = 220.0  # frequency of the sound (A4)
chunk_size = 2048  # Increased chunk size to reduce underrun errors
current_byte = 0

# Generate the waveform for the entire duration
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
waveform = (np.sin(2 * np.pi * frequency * t) * 1.5).astype(np.int16)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for stereo output
stream = p.open(format=pyaudio.paFloat32,
                channels=2,  # Stereo (left and right channels)
                rate=sampling_rate,
                output=True)

left_volume = 1
right_volume = 1
start_index = 0
end_index = 0
beep = False

def update_volume(angle, beep_val=False, noVolume=False):
    """Update the stereo volumes based on angle input (in degrees)."""
    global left_volume, right_volume, beep
    if(noVolume):
        left_volume = 0
        right_volume = 0
        beep = beep_val
    else:
        left_volume = math.fabs(math.sin(math.radians(angle))) / 10
        right_volume = math.fabs(math.cos(math.radians(angle))) / 10
        beep = beep_val
    
def create_stereo_chunk(chunk, left_vol, right_vol):
    """Create stereo audio chunk by applying left and right volume."""
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
        stream.stop_stream()
        if beep:
            time.sleep(0.5)
            beep = False
        else:
            time.sleep(0.1)
        stream.start_stream()

if __name__ == "__main__":
    try:
        # Play the sound
        update_volume(167)
        create_sound()
    finally:
        # Close the stream and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()
