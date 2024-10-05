import time

import smbus

# MPU6050 Registers
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

bus = smbus.SMBus(1)  # Open the I2C bus
address = 0x68  # MPU-6050 address

# Wake up MPU6050
bus.write_byte_data(address, PWR_MGMT_1, 0)


def read_word(reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -(65535 - value + 1)
    return value


def read_gyroscope():
    gyro_x = read_word(GYRO_XOUT_H)
    gyro_y = read_word(GYRO_YOUT_H)
    gyro_z = read_word(GYRO_ZOUT_H)
    return gyro_x, gyro_y, gyro_z


def calibrate_gyroscope(samples=100):
    offset_x = 0
    offset_y = 0
    offset_z = 0

    for _ in range(samples):
        gyro_x, gyro_y, gyro_z = read_gyroscope()
        offset_x += gyro_x
        offset_y += gyro_y
        offset_z += gyro_z
        time.sleep(0.01)  # 10ms delay between samples

    offset_x /= samples
    offset_y /= samples
    offset_z /= samples

    return offset_x, offset_y, offset_z


# Step 1: Calibrate the gyroscope
print("Calibrating gyroscope... Please keep the sensor still.")
gyro_offset_x, gyro_offset_y, gyro_offset_z = calibrate_gyroscope()
print(
    f"Calibration offsets - X: {gyro_offset_x}, Y: {gyro_offset_y}, Z: {gyro_offset_z}"
)

# Initialize angles
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0  # Z-axis (yaw) needs to wrap from 0 to 360 degrees

prev_time = time.time()

# Step 2: Read live data and apply calibration
print("Reading live gyroscope data and wrapping Z-axis to 0-360 degrees...")

while True:
    # Read gyroscope data and subtract offsets
    gyro_x, gyro_y, gyro_z = read_gyroscope()
    calibrated_gyro_x = gyro_x - gyro_offset_x
    calibrated_gyro_y = gyro_y - gyro_offset_y
    calibrated_gyro_z = gyro_z - gyro_offset_z

    # Calculate time difference (dt)
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time

    # Convert gyroscope values to angular displacement (in degrees)
    # Sensitivity is usually 131 LSB per degree/s for the MPU-6050 by default
    gyro_sensitivity = 131.0
    angle_x += (calibrated_gyro_x / gyro_sensitivity) * dt
    angle_y += (calibrated_gyro_y / gyro_sensitivity) * dt
    angle_z += (calibrated_gyro_z / gyro_sensitivity) * dt

    # Wrap the Z-axis angle (yaw) to stay within 0-360 degrees
    angle_z = angle_z % 360  # Ensures angle stays between 0 and 360

    # Print the live angle values (with Z-axis wrapped)
    print(f"Angles (X: {angle_x:.2f}°, Y: {angle_y:.2f}°, Z: {angle_z:.2f}°)")

    # Small delay to avoid flooding the console
    time.sleep(0.5)
