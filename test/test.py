'''
    test.py is a test file for the project.
    Author: Oguzhan Yuksel
'''
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import *  

# Create instances
ev = ElectricVehicle()
charging_unit = ChargingUnit()

# Test instances
print(ev.__str__())
print(charging_unit.__str__())
# Test charge() method of ElectricVehicle class
ev.charge(10)
print(ev.__str__())
# Test charge_vehicle() method of ChargingUnit class
charging_unit.charge_vehicle(ev, 1)
print(ev.__str__())

# User input for connection and disconnection times
connection_time_str = input("Enter connection time (YYYY-MM-DD HH:MM): ")
disconnection_time_str = input("Enter disconnection time (YYYY-MM-DD HH:MM): ")

# Parse input times
connection_time = datetime.strptime(connection_time_str, "%Y-%m-%d %H:%M")
disconnection_time = datetime.strptime(disconnection_time_str, "%Y-%m-%d %H:%M")

# Run simulation with user-defined connection and disconnection times
ev = ElectricVehicle()
charging_unit = ChargingUnit()
simulation = Simulation(connection_time, disconnection_time)
simulation.run(ev, charging_unit)

# Get results as DataFrame
results_df = simulation.get_results()

# Print results
print(results_df)

