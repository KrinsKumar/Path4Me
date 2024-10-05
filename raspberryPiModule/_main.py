from utils.LLM import full_flow
from utils.sensors import fetch_sensor_data

# Run all the functions sequentially
fetch_sensor_data()
full_flow()
