import numpy as np
import soundfile as sf
import pyaudio
import math

# Parameters
duration = 10.0  # seconds
sampling_rate = 44100  # samples per second (standard for audio)
frequency = 220.0  # frequency of the sound (A4) - - used to change how sound sounds
radius = 1.0  # radius of rotation (arbitrary units)

# Calculate the time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Generate a simple sine wave (single tone)
waveform = np.sin(2 * np.pi * frequency * t)

def get_stereo_waveform(duration, sampling_rate, waveform):
    """Precompute the entire stereo waveform for smoother playback."""
    total_samples = int(duration * sampling_rate)
    
    # Prepare the stereo waveform array (2 channels: left and right)
    stereo_waveform = np.zeros((total_samples, 2))

    # Angle step per sample for continuous rotation (2 * pi for a full circle)
    angular_velocity = 2 * np.pi / duration

    # Precompute the stereo waveform
    for i in range(total_samples):
        #angle = (i / total_samples) * 2 * np.pi * duration
        angle = 0
        left_volume = (1 + math.sin(math.radians(angle))) / 2
        right_volume = (1 + math.cos(math.radians(angle))) / 2
        stereo_waveform[i, 0] = left_volume * waveform[i]  # Left channel
        stereo_waveform[i, 1] = right_volume * waveform[i]  # Right channel
        # print(i, angle, left_volume, right_volume)

    return stereo_waveform

# Precompute the stereo waveform
stereo_waveform = get_stereo_waveform(duration, sampling_rate, waveform)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for stereo output
stream = p.open(format=pyaudio.paFloat32,
                channels=2,  # Stereo (left and right channels)
                rate=sampling_rate,
                output=True)

# Play the precomputed stereo waveform in chunks
chunk_size = 1024
for i in range(0, len(stereo_waveform), chunk_size):
    print(i)
    chunk = stereo_waveform[i:i + chunk_size]
    stream.write(chunk.astype(np.float32).tobytes())

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()
