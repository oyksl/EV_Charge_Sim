'''
    sample.py is a sample file for the project.
    Author: Oguzhan Yuksel
'''
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *  

# User input for connection and disconnection times
connection_time_str = input("Enter connection time (YYYY-MM-DD HH:MM): ")
disconnection_time_str = input("Enter disconnection time (YYYY-MM-DD HH:MM): ")

# Parse input times
connection_time = datetime.strptime(connection_time_str, "%Y-%m-%d %H:%M")
disconnection_time = datetime.strptime(disconnection_time_str, "%Y-%m-%d %H:%M")

# Create instances
ev = ElectricVehicle() # if not specified, battery_capacity=50, max_power_capacity=11, state_of_charge=0.1
charging_unit = ChargingUnit() # if not specified, max_output=22
simulation = Simulation(connection_time, disconnection_time) # if not specified, interval_minutes=15

# Run simulation with user-defined connection and disconnection times
simulation.run(ev, charging_unit) 

# Get results as DataFrame
results_df = simulation.get_results() # if not specified, results are saved at './results/'

# Print results
print(results_df)

