from utils.LLM import full_flow
from utils.sensors import fetch_sensor_data, calibrate_gyroscope, read_gyroscope, read_accelerometer
from utils.sound import create_sound, update_volume
import threading
import math
import time

# fetch_sensor_data() # Image capture
# target_degrees = full_flow() # Image analysis
target_degrees = 225

gyro_degrees = 0
gyro_lock = threading.Lock()

def low_pass_filter(value, prev_value, alpha=0.5):
    return alpha * prev_value + (1 - alpha) * value

def capture_gyro_data():
    global gyro_degrees

    gyro_offset_x, gyro_offset_y, gyro_offset_z = calibrate_gyroscope()

    # Initialize angles
    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0  # Z-axis (yaw) needs to wrap from 0 to 360 degrees

    prev_time = time.time()

    # Complementary filter constant
    alpha = 0.98

    # Initialize previous accelerometer values for low-pass filter
    prev_accel_x = 0.0
    prev_accel_y = 0.0
    prev_accel_z = 0.0

    print("Reading live gyroscope data and wrapping Y-axis to 0-360 degrees...")

    while True:
        # Read gyroscope data and subtract offsets
        gyro_x, gyro_y, gyro_z = read_gyroscope()
        calibrated_gyro_x = gyro_x - gyro_offset_x
        calibrated_gyro_y = gyro_y - gyro_offset_y
        calibrated_gyro_z = gyro_z - gyro_offset_z

        # Read accelerometer data
        accel_x, accel_y, accel_z = read_accelerometer()

        # Apply low-pass filter to accelerometer data
        accel_x = low_pass_filter(accel_x, prev_accel_x)
        accel_y = low_pass_filter(accel_y, prev_accel_y)
        accel_z = low_pass_filter(accel_z, prev_accel_z)

        # Update previous accelerometer values
        prev_accel_x = accel_x
        prev_accel_y = accel_y
        prev_accel_z = accel_z

        # Calculate time difference (dt)
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time

        # Convert gyroscope values to angular displacement (in degrees)
        gyro_sensitivity = 131.0
        angle_x += (calibrated_gyro_x / gyro_sensitivity) * dt
        angle_y += (calibrated_gyro_y / gyro_sensitivity) * dt
        angle_z += (calibrated_gyro_z / gyro_sensitivity) * dt

        # Calculate accelerometer angles
        accel_angle_x = math.atan2(accel_y, accel_z) * 180 / math.pi
        accel_angle_y = math.atan2(-accel_x, math.sqrt(accel_y**2 + accel_z**2)) * 180 / math.pi

        # Apply complementary filter
        angle_x = alpha * angle_x + (1 - alpha) * accel_angle_x
        angle_y = alpha * angle_y + (1 - alpha) * accel_angle_y

        # Wrap the Y-axis angle to stay within 0-360 degrees
        angle_y = angle_y % 360  # Ensures angle stays between 0 and 360

        # Update the global gyro_degrees variable with a lock
        with gyro_lock:
            gyro_degrees = angle_y

def call_sound_generator():
    global gyro_degrees
    global target_degrees

    while True:
        with gyro_lock:
            current_gyro_degrees = gyro_degrees

        a1 = abs(current_gyro_degrees - target_degrees)
        a2 = 360 - a1

        print(f"Sound emitted for gyro: {current_gyro_degrees} | target: {target_degrees}")

        if a1 > 90 and a2 > 90:
            update_volume(135, True)
            continue
        
        A = target_degrees - current_gyro_degrees
        if A > 180 or A < -180:
            B = 360 - abs(A)
            if target_degrees > current_gyro_degrees:
                update_volume(135 + B / 2)
            else:
                update_volume(135 - B / 2)
        else:
            update_volume(135 - A / 2)

t1 = threading.Thread(target=capture_gyro_data)
t2 = threading.Thread(target=call_sound_generator)

if __name__ == "__main__":
    t1.start()
    t2.start()

    t1.join()
    t2.join()