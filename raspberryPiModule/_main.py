import threading
import time

from mpu6050 import mpu6050
from utils.LLM import full_flow
from utils.sensor import loop
from utils.sound import create_sound, update_volume
import subprocess
import os

mpu = mpu6050(0x68)


def calibrate_gyro():
    print("Calculating gyro offset, do not move MPU6050...")
    sound_file = os.path.join("utils","assets", "ten.mp3")
    if os.path.exists(sound_file):
        subprocess.run(["mpg123", sound_file])

    n_samples = 1000
    gyro_offsets = {"x": 0, "y": 0, "z": 0}

    for _ in range(n_samples):
        gyro_data = mpu.get_gyro_data()
        gyro_offsets["x"] += gyro_data["x"]
        gyro_offsets["y"] += gyro_data["y"]
        gyro_offsets["z"] += gyro_data["z"]
        time.sleep(0.01)

    gyro_offsets["x"] /= n_samples
    gyro_offsets["y"] /= n_samples
    gyro_offsets["z"] /= n_samples

    print(f"Gyro offsets calculated: {gyro_offsets}")

    return gyro_offsets


def setup():
    print("Initializing MPU6050...")
    subprocess.run(["amixer", "sset", "'Master'", f"70%"])
    time.sleep(1)
    print("MPU6050 ready.")


setup()

gyro_offsets = calibrate_gyro()

loop(gyro_offsets)
target_degrees = full_flow() or 220
gyro_degrees = 0


def loop_pure(gyro_offsets):
    global gyro_degrees
    timer = time.time()  # Start the timer
    current_angle_x = 0  # Initialize the current angle
    
    while True:
        if (time.time() - timer) > 0.1:
            # Read accelerometer and gyroscope data
            accel_data = mpu.get_accel_data()
            gyro_data = mpu.get_gyro_data()

            # Subtract offsets from gyro readings
            corrected_gyro = {
                "x": gyro_data["x"] - gyro_offsets["x"],
                "y": gyro_data["y"] - gyro_offsets["y"],
                "z": gyro_data["z"] - gyro_offsets["z"],
            }

            # Update the current angle based on gyro X reading
            current_angle_x += (
                corrected_gyro["x"] * 0.1
            )  # Scale the gyro reading to time passed
            current_angle_x = current_angle_x % 360  # Normalize to 0-360 degrees

            # Print the data to the console
            print(
                f"Current Angle X: {current_angle_x:.2f}, Target Degrees: {target_degrees: .2f}"
            )

            gyro_degrees = current_angle_x

            timer = time.time()


def call_sound_generator():
    global gyro_degrees
    global target_degrees

    while True:
        a1 = abs(gyro_degrees - target_degrees)
        a2 = 360 - a1

        print(f"Sound emmited for gyro: {gyro_degrees} | target: {target_degrees}")

        if a1 > 90 and a2 > 90:
            update_volume(135, False, True)  # No volume
            continue

        A = target_degrees - gyro_degrees
        if A > 180 or A < -180:
            B = 360 - abs(A)
            if target_degrees > gyro_degrees:
                update_volume(135 + B / 2)
            else:
                update_volume(135 - B / 2)
        else:
            update_volume(135 - A / 2)


t1 = threading.Thread(target=loop_pure, args=(gyro_offsets,))
t2 = threading.Thread(target=call_sound_generator)
t3 = threading.Thread(target=create_sound)

if __name__ == "__main__":
    t1.start()
    t2.start()

    sound_file = os.path.join("utils","assets", "start.mp3")
    if os.path.exists(sound_file):
        subprocess.run(["mpg123", sound_file])
    
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("\n\nAll functions executed successfully!\n")
