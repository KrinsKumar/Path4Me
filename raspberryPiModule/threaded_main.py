#from utils.LLM import full_flow
from utils.sensors import fetch_sensor_data, calibrate_gyroscope, read_gyroscope, read_accelerometer
import threading
import math
import time # For testing purposes

fetch_sensor_data() #Image capture
#target_degrees = full_flow() # Image analysis
target_degrees = 220

gyro_degrees = 0

def capture_gyro_data():
    global gyro_degrees

    gyro_offset_x, gyro_offset_y, gyro_offset_z = calibrate_gyroscope()

    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0

    prev_time = time.time()

    alpha = 0.98

    while True:
        gyro_x, gyro_y, gyro_z = read_gyroscope()
        calibrated_gyro_x = gyro_x - gyro_offset_x
        calibrated_gyro_y = gyro_y - gyro_offset_y
        calibrated_gyro_z = gyro_z - gyro_offset_z

        accel_x, accel_y, accel_z = read_accelerometer()

        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time

        gyro_sensitivity = 131.0
        angle_x += (calibrated_gyro_x / gyro_sensitivity) * dt
        angle_y += (calibrated_gyro_y / gyro_sensitivity) * dt
        angle_z += (calibrated_gyro_z / gyro_sensitivity) * dt

        accel_angle_x = math.atan2(accel_y, accel_z) * 180 / math.pi
        accel_angle_y = math.atan2(-accel_x, math.sqrt(accel_y**2 + accel_z**2)) * 180 / math.pi

        angle_x = alpha * angle_x + (1 - alpha) * accel_angle_x
        angle_y = alpha * angle_y + (1 - alpha) * accel_angle_y

        angle_z = angle_z % 360

        gyro_degrees = angle_z

def sound_generator(angle, beep=False):
    # Play sound
    print(f"Playing sound. At the angle: {angle}. [Gyro: {gyro_degrees}]")

def call_sound_generator():
    global gyro_degrees
    global target_degrees

    while True:
        a1 = abs(gyro_degrees - target_degrees)
        a2 = 360 - a1

        if a1 > 90 and a2 > 90:
            sound_generator(135, True)
            continue
        
        A = target_degrees - gyro_degrees
        if A > 180 or A < -180:
            B = 360 - abs(A)
            if target_degrees > gyro_degrees:
                sound_generator(135 + B/2)
            else:
                sound_generator(135 - B/2)
        else:
            sound_generator(135 - A/2)

        time.sleep(0.05)

t1 = threading.Thread(target=capture_gyro_data)
t2 = threading.Thread(target=call_sound_generator)

if __name__ == "__main__":
    t1.start()
    t2.start()

    t1.join()
    t2.join()
            
