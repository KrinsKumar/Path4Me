import time

import numpy as np
import sounddevice as sd


# Function to calculate the sound panning based on angles
def get_panning(user_angle, target_angle):
    angle_diff = (target_angle - user_angle + 360) % 360
    panning = (angle_diff - 180) / 180  # Normalize between -1 (left) and 1 (right)
    return panning


# Function to generate a sine wave audio signal
def generate_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(
        0, duration, int(sample_rate * duration), endpoint=False
    )  # Time array
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Generate sine wave
    return wave


# Function to play the generated sound with panning
def play_sound_with_panning(frequency, user_angle, target_angle, duration):
    sample_rate = 44100  # Sample rate
    wave = generate_sine_wave(frequency, duration)  # Generate sine wave

    # Calculate panning
    panning = get_panning(user_angle, target_angle)

    # Calculate the volume for left and right channels
    left_volume = 1 + panning if panning < 0 else 1  # Left volume
    right_volume = 1 - panning if panning >= 0 else 1  # Right volume

    # Apply the panning effect
    left_channel = wave * left_volume
    right_channel = wave * right_volume
    stereo_sound = np.column_stack((left_channel, right_channel))

    # Play the audio
    sd.play(stereo_sound, samplerate=sample_rate)
    sd.wait()  # Wait until playback is finished


# Function to simulate user movement in real time
def user_movement(target_angle, frequency, duration):
    user_angle = 0  # Starting angle
    while True:
        print(f"User Angle: {user_angle}°, Target Angle: {target_angle}°")

        # Play sound with the calculated panning
        play_sound_with_panning(frequency, user_angle, target_angle, duration)

        # Simulate user input or update from a sensor
        user_angle += np.random.randint(-10, 11)  # Simulate random movement
        user_angle %= 360  # Keep the angle within 0-359

        # Delay for demonstration purposes
        time.sleep(duration)  # Wait for the duration of the sound


# Example usage
if __name__ == "__main__":
    target_angle = 235  # Target angle in degrees
    frequency = 440  # Frequency of the sine wave (in Hz)
    duration = 1  # Duration of each sound segment (in seconds)

    user_movement(target_angle, frequency, duration)
