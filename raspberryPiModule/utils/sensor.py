import os
import subprocess
import time

from mpu6050 import mpu6050
from picamera import PiCamera

image_folder = "assets"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

mpu = mpu6050(0x68)


def setup():
    print("Initializing MPU6050...")
    time.sleep(1)
    print("MPU6050 ready.")




def take_picture(num, val):
    camera = PiCamera()

    image_name = f"{num}.jpg"
    image_path = os.path.join(image_folder, image_name)

    sound_file = os.path.join("utils","assets", "wait.mp3")
    if os.path.exists(sound_file):
        subprocess.run(["mpg123", sound_file])

    camera.start_preview()

    camera.capture(image_path)

    camera.stop_preview()

    camera.close()

    print(f"Image saved at {image_path} at gyro value of {val}")


def calibrate_gyro():
    print("Calculating gyro offset, do not move MPU6050...")
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


def low_pass_filter(value, prev_value, alpha=0.5):
    return alpha * prev_value + (1 - alpha) * value


def loop(gyro_offsets):
    timer = time.time()
    current_angle_x = 0
    pictures_taken = [False, False, False]
    take_picture(1, 0)

    sound_file = os.path.join("utils","assets", "start.mp3")
      if os.path.exists(sound_file):
          subprocess.run(["mpg123", sound_file])

    prev_time = time.time()
    prev_gyro_x = 0.0

    while True:
        if (time.time() - timer) > 0.1:
            accel_data = mpu.get_accel_data()
            gyro_data = mpu.get_gyro_data()

            corrected_gyro = {
                "x": gyro_data["x"] - gyro_offsets["x"],
                "y": gyro_data["y"] - gyro_offsets["y"],
                "z": gyro_data["z"] - gyro_offsets["z"],
            }

            corrected_gyro["x"] = low_pass_filter(corrected_gyro["x"], prev_gyro_x)
            prev_gyro_x = corrected_gyro["x"]

            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time

            current_angle_x += corrected_gyro["x"] * dt
            current_angle_x = current_angle_x % 360  # Normalize to 0-360 degrees

            if current_angle_x > 88 and current_angle_x < 92 and not pictures_taken[0]:
                take_picture(2, current_angle_x)
                pictures_taken[0] = True
            elif (
                current_angle_x > 178
                and current_angle_x < 182
                and not pictures_taken[1]
                and pictures_taken[0]
            ):
                take_picture(3, current_angle_x)
                pictures_taken[1] = True
            elif (
                current_angle_x > 265
                and current_angle_x < 285
                and not pictures_taken[2]
                and pictures_taken[1]
            ):
                take_picture(4, current_angle_x)
                pictures_taken[2] = True
            elif pictures_taken[2] and (current_angle_x < 10):
                sound_file = os.path.join("utils","assets", "thanthan.mp3")
                if os.path.exists(sound_file):
                    subprocess.run(["mpg123", sound_file])
                break

            print(
                f"Current Angle X: {current_angle_x:.2f}"
            )

            timer = time.time()


if __name__ == "__main__":
    setup()
    gyro_offsets = calibrate_gyro()
    loop(gyro_offsets)
