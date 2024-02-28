from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import time
import random
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor, Unit


# Prometheus metric: Gauge
HUMIDITY_GAUGE = Gauge('humidity_percentage', 'Current humidity percentage', ['instance'])
TEMPERATURE_GAUGE = Gauge('temperature_percentage', 'Current temperature percentage', ['instance'])

# Function to simulate measuring humidity
def measure_humidity():
    # Simulate measuring humidity (replace with your logic)
    return random.uniform(0, 100)

def measure_temperature(sensor):
    return sensor.get_temperature(Unit.DEGREES_F)

def relay_on(gpio):
        GPIO.output(gpio,GPIO.HIGH)

def relay_off(gpio):
        GPIO.output(gpio,GPIO.LOW)

if __name__ == '__main__':
    # Your application logic
    registry = CollectorRegistry()
    registry.register(HUMIDITY_GAUGE)
    registry.register(TEMPERATURE_GAUGE)
    sensor = W1ThermSensor()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False) #disable annoying warning messages
    GPIO.setup(17,GPIO.OUT)

    while True:
        # Simulate measuring humidity
        humidity = measure_humidity()
        temperature = measure_temperature(sensor)
        if temperature >72.0:
            relay_on(17)
        else:
            relay_off(17)
        print("temperature: " + str(temperature))
        # Set the gauge metric value
        HUMIDITY_GAUGE.labels(instance='humidity').set(humidity)
        TEMPERATURE_GAUGE.labels(instance='temperature').set(temperature)

        # Push the metric to the Pushgateway on the EC2 instance
        job_name = 'pushgateway'
        endpoint = 'http://54.187.139.103:9091/'  # Replace with your EC2 instance's public IP

        # Pass the handler to push_to_gateway
        push_to_gateway(endpoint, job=job_name, registry=registry, timeout=30)

        time.sleep(5)  # Adjust the sleep duration based on your desired frequency

        print("wokeup")

