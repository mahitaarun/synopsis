import sys
sys.path.append('../')
import time
from CQRobot_ADS1115 import ADS1115
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16
ads1115 = ADS1115()

# Prometheus metric: Gauge
HUMIDITY_GAUGE_1 = Gauge('humidity_percentage1', 'Current humidity percentage', ['instance'])
# Prometheus metric: Gauge
HUMIDITY_GAUGE_2 = Gauge('humidity_percentage2', 'Current humidity percentage', ['instance'])
HUMIDITY_GAUGE_3 = Gauge('humidity_percentage3', 'Current humidity percentage', ['instance'])
# Your application logic
registry = CollectorRegistry()
registry.register(HUMIDITY_GAUGE_1)
registry.register(HUMIDITY_GAUGE_2)
registry.register(HUMIDITY_GAUGE_3)

while True :
    #Set the IIC address
    ads1115.setAddr_ADS1115(0x48)
    #Sets the gain and input voltage range.
    ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
    #Get the Digital Value of Analog of selected channel
    adc1 = ads1115.readVoltage(0)
    adc3 = ads1115.readVoltage(2)
    adc4 = ads1115.readVoltage(3)
    time.sleep(0.2)
    print(" A1:%dmV "%(adc1['r']))
    print(" A1:%dmV "%(adc3['r']))
    print(" A4:%dmV "%(adc4['r']))
    # Define the range of the original values
    min_value = 1370
    max_value = 3000
    
    # Calculate the percentage using linear interpolation
    percentage_A1 = 100 - ((adc1['r'] - min_value) / (max_value - min_value)) * 100
    percentage_A3 = 100 - ((adc3['r'] - min_value) / (max_value - min_value)) * 100
    percentage_A4 = 100 - ((adc4['r'] - min_value) / (max_value - min_value)) * 100
    
    # Ensure the percentage is within the range of 0% to 100%
    percentage_A1 = max(min(percentage_A1, 100), 0)
    percentage_A3 = max(min(percentage_A3, 100), 0)
    percentage_A4 = max(min(percentage_A4, 100), 0)
    print("A1: "+str(percentage_A1))
    print("A3: "+str(percentage_A3))
    print("A4: "+str(percentage_A4))
    # Set the gauge metric value
    HUMIDITY_GAUGE_1.labels(instance='humidity').set(percentage_A1)
    HUMIDITY_GAUGE_2.labels(instance='humidity').set(percentage_A3)
    HUMIDITY_GAUGE_3.labels(instance='humidity').set(percentage_A4)
    # Push the metric to the Pushgateway on the EC2 instance
    job_name = 'pushgateway'
    endpoint = 'http://54.214.96.27:9091/'  # Replace with your EC2 instance's public IP
    # Pass the handler to push_to_gateway
    try:
      push_to_gateway(endpoint, job=job_name, registry=registry, timeout=30)
    except Exception as e:
       print(f"An error occured while pushing to pushgateway: {e}")
    print("Program continues...")
    time.sleep(1)
