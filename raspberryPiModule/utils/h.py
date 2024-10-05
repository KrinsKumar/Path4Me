import time
from mpu6050 import mpu6050  # Ensure you have a compatible MPU6050 library installed
import os
import time
import smbus
from picamera import PiCamera
import math
from utils.sound import update_volume
import subprocess

image_folder = "assets"  # The folder with the images
if not os.path.exists(image_folder):
    os.makedirs(image_folder)


# Create an instance of the MPU6050 class
mpu = mpu6050(0x68)  # Adjust the I2C address if necessary

# Initialize the MPU6050 and print initial messages
def setup():
    print("Initializing MPU6050...")
    time.sleep(1)  # Allow time for MPU6050 to start
    print("MPU6050 ready.")

def take_picture(num, val):
    # Initialize PiCamera
    camera = PiCamera()

    # Capture image
    image_name = f"{num}.jpg"  # Unique name based on timestamp
    image_path = os.path.join(image_folder, image_name)

    # Start the camera preview (optional)
    subprocess.run(["mpg123", "utils/notif.mp3"])
    camera.start_preview()
    # time.sleep(0.5)  # Give the camera time to adjust to lighting

    # Capture the image
    camera.capture(image_path)
    
    # Stop the camera preview (optional)
    camera.stop_preview()

    # Close the camera
    camera.close()

    print(f"Image saved at {image_path} at gyro value of {val}")

def calibrate_gyro():
    print("Calculating gyro offset, do not move MPU6050...")
    n_samples = 1000
    gyro_offsets = {'x': 0, 'y': 0, 'z': 0}

    # Collect data samples
    for _ in range(n_samples):
        gyro_data = mpu.get_gyro_data()
        gyro_offsets['x'] += gyro_data['x']
        gyro_offsets['y'] += gyro_data['y']
        gyro_offsets['z'] += gyro_data['z']
        time.sleep(0.01)  # Slight delay to avoid overwhelming the sensor

    # Calculate average offsets
    gyro_offsets['x'] /= n_samples
    gyro_offsets['y'] /= n_samples
    gyro_offsets['z'] /= n_samples

    print(f"Gyro offsets calculated: {gyro_offsets}")

    return gyro_offsets

def loop(gyro_offsets):
    timer = time.time()  # Start the timer
    current_angle_x = 0  # Initialize the current angle
    pictures_taken = [False, False, False]
    take_picture(1, 0)

    while True:
        if (time.time() - timer) > 0.1:  # Print data every 100ms
            # Read accelerometer and gyroscope data
            accel_data = mpu.get_accel_data()
            gyro_data = mpu.get_gyro_data()

            # Subtract offsets from gyro readings
            corrected_gyro = {
                'x': gyro_data['x'] - gyro_offsets['x'],
                'y': gyro_data['y'] - gyro_offsets['y'],
                'z': gyro_data['z'] - gyro_offsets['z'],
            }

            # Update the current angle based on gyro X reading
            current_angle_x += corrected_gyro['x'] * 0.1  # Scale the gyro reading to time passed
            current_angle_x = current_angle_x % 360  # Normalize to 0-360 degrees
            
            if current_angle_x > 88 and current_angle_x < 92 and not pictures_taken[0]:
                take_picture(2, current_angle_x)
                pictures_taken[0] = True
            elif current_angle_x > 178 and current_angle_x < 182 and not pictures_taken[1] and pictures_taken[0]:
                take_picture(3, current_angle_x)
                pictures_taken[1] = True
            elif current_angle_x > 235 and current_angle_x < 272 and not pictures_taken[2] and pictures_taken[1]:
                take_picture(4, current_angle_x)
                pictures_taken[2] = True
                break

            # Print the data to the console
            print(f"Current Angle X: {current_angle_x:.2f}° | R: {corrected_gyro['y']:.2f} | Y: {corrected_gyro['z']:.2f}")
            print(f"Accel: X={accel_data['x']:.2f} | Y={accel_data['y']:.2f} | Z={accel_data['z']:.2f}")

            timer = time.time()  # Reset timer
            



if __name__ == "__main__":
    setup()
    gyro_offsets = calibrate_gyro()  # Call the calibration function
    loop(gyro_offsets)  # Pass the offsets to the loop
