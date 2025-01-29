from datetime import datetime, timedelta
import pandas as pd

# Electric Vehicle class
class ElectricVehicle:
    # Constructor
    def __init__(self, id, battery_capacity=50, state_of_charge=0.1, max_power_capacity=11):
        self.id = id
        self.max_power_capacity = max_power_capacity  # kW - user defined o.w. 11
        self.battery_capacity = battery_capacity  # kWh - user defined o.w. 50
        self.state_of_charge = state_of_charge  # user defined o.w. 0.1
        self.current_charge = self.state_of_charge * self.battery_capacity

    # Charge method
    def charge(self, amount: float):
        self.current_charge = min(self.battery_capacity, self.current_charge + amount)
        # update state of charge
        self.state_of_charge = self.current_charge / self.battery_capacity

    # Log method
    def __str__(self):
        return f"EV {self.id}: {self.current_charge}/{self.battery_capacity} kWh"


# Charging Unit class
class ChargingUnit:
    # Constructor
    def __init__(self, id, max_output=22):
        self.id = id
        self.max_output = max_output  # kW - user defined o.w. 22

    # Charge vehicle method
    def charge_vehicle(self, ev: ElectricVehicle, hours: float):
        charge_amount = min(self.max_output, ev.max_power_capacity) * hours
        ev.charge(charge_amount)

    # Log method
    def __str__(self):
        return f"Charging Unit {self.id}: {self.max_output} kW"


# Simulation class
class Simulation:
    def __init__(self, connection_time: datetime, disconnection_time: datetime, interval_minutes=15):
        self.simulation_start_time = connection_time.replace(hour=9, minute=0, second=0)
        self.simulation_end_time = disconnection_time.replace(hour=21, minute=0, second=0)  
        self.interval = timedelta(minutes=interval_minutes)
        self.connection_time = connection_time
        self.disconnection_time = disconnection_time
        self.current_time = self.simulation_start_time
        self.data = []

    def run(self, ev: ElectricVehicle, charging_unit: ChargingUnit):
        while self.current_time < self.simulation_end_time:
            if self.connection_time <= self.current_time < self.disconnection_time:
                if ev.state_of_charge < 1.0:
                    charging_power = min(charging_unit.max_output, ev.max_power_capacity)
                    charging_unit.charge_vehicle(ev, self.interval.total_seconds() / 3600)
                    net_energy_charged = ev.current_charge
                else:
                    charging_power = 0
                    net_energy_charged = ev.current_charge
            else:
                charging_power = 0
                net_energy_charged = ev.current_charge
            self.data.append({
                "Timestamp": self.current_time,
                "Charging Power (kW)": charging_power,
                "SOC (%)": ev.state_of_charge * 100,
                "Net Energy Charged (kWh)": net_energy_charged
            })
            self.current_time += self.interval

    def get_results(self):
        return pd.DataFrame(self.data)


# User input for connection and disconnection times
connection_time_str = input("Enter connection time (YYYY-MM-DD HH:MM): ")
disconnection_time_str = input("Enter disconnection time (YYYY-MM-DD HH:MM): ")

# Parse input times
connection_time = datetime.strptime(connection_time_str, "%Y-%m-%d %H:%M")
disconnection_time = datetime.strptime(disconnection_time_str, "%Y-%m-%d %H:%M")

# Ensure connection and disconnection times are valid
if connection_time >= disconnection_time:
    raise ValueError("Invalid connection or disconnection time.")

# Create instances
ev = ElectricVehicle(id=1)
charging_unit = ChargingUnit(id=1)
simulation = Simulation(connection_time, disconnection_time)

# Run simulation with user-defined connection and disconnection times
simulation.run(ev, charging_unit)

# Get results as DataFrame
results_df = simulation.get_results()

# Print results
print(results_df)
