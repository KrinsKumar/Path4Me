from utils.LLM import full_flow
from utils.sensors import fetch_sensor_data
import threading
import time # For testing purposes

fetch_sensor_data() #Image capture
target_degrees = full_flow() # Image analysis

gyro_degrees = 0

def capture_gyro_data():
    global gyro_degrees

    # Capture gyro data
    while True:
        for i in range(20, 210):
            gyro_degrees = i
            time.sleep(0.1)

def call_sound_generator():
    global gyro_degrees
    global target_degrees

    while True:
        print("Playing sound. User is facing: ", gyro_degrees, " | Target is at: ", target_degrees)
        time.sleep(0.05)

t1 = threading.Thread(target=capture_gyro_data)
t2 = threading.Thread(target=call_sound_generator)

if __name__ == "__main__":
    t1.start()
    t2.start()

    t1.join()
    t2.join()
            
