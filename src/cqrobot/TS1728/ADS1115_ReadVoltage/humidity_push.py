# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from adafruit_seesaw.seesaw import Seesaw

# Prometheus metric: Gauge
HUMIDITY_GAUGE = Gauge('humidity_percentage', 'Current humidity percentage', ['instance'])
TEMPERATURE_GAUGE = Gauge('temperature_percentage', 'Current temperature percentage', ['instance'])

if __name__ == '__main__':
    # Your application logic
    registry = CollectorRegistry()
    registry.register(HUMIDITY_GAUGE)
    registry.register(TEMPERATURE_GAUGE)
    i2c_bus = board.I2C()  # uses board.SCL and board.SDA
    ss = Seesaw(i2c_bus, addr=0x36)
    # Define the range of raw moisture values
    min_raw_value = 200
    max_raw_value = 1015

    while True:
      # read moisture level through capacitive touch pad
      humidity = ss.moisture_read()
      if humidity is not None:
        #calucultate humidity percentage based on min and max reading
        humidity_percentage = (humidity - min_raw_value) / (max_raw_value - min_raw_value) * 100


      # read temperature from the temperature sensor
      temperature = ss.get_temp()
      if temperature is not None:
         temperature_fahrenheit = (temperature * 9/5) + 32
      print("temp: " + str(temperature_fahrenheit) + "  moisture: " + str(humidity_percentage))
      # Set the gauge metric value
      HUMIDITY_GAUGE.labels(instance='humidity').set(humidity_percentage)
      TEMPERATURE_GAUGE.labels(instance='temperature').set(temperature_fahrenheit)
      # Push the metric to the Pushgateway on the EC2 instance
      job_name = 'pushgateway'
      endpoint = 'http://54.187.139.103:9091/'  # Replace with your EC2 instance's public IP
      # Pass the handler to push_to_gateway
      try:
        push_to_gateway(endpoint, job=job_name, registry=registry, timeout=30)
      except Exception as e:
         print(f"An error occured while pushing to pushgateway: {e}")
      print("Program continues...")
      time.sleep(1)
