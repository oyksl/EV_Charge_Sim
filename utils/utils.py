'''
    Electric Vehicle Charging Simulation
    Author: Oguzhan Yuksel
    Date: 2025-01-31 

    Assumptions:
    - Electric vehicle (EV) has a battery capacity of 50 kWh, SOC of 10% and a maximum power capacity of 11 kW by default.
    - Charging unit has a maximum output of 22 kW by default.
    - Only one EV can be charged at a time.
    - Simulation runs between 9:00 and 21:00 for a given date.
    - Results are saved with 15-minute intervals. Calculation precision is 1 minute.
'''

from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# Electric Vehicle class
class ElectricVehicle:
    # Constructor
    def __init__(self, battery_capacity=50, state_of_charge=0.1, max_power_capacity=11):
        self.max_power_capacity = max_power_capacity  # kW - user defined o.w. 11
        self.battery_capacity = battery_capacity  # kWh - user defined o.w. 50
        self.state_of_charge = state_of_charge  # user defined o.w. 0.1
        self.charge_level = self.state_of_charge * self.battery_capacity

    # Charge method
    def charge(self, amount: float):
        self.charge_level = min(self.battery_capacity, self.charge_level + amount)
        # update state of charge
        self.state_of_charge = self.charge_level / self.battery_capacity

    # Log method
    def __str__(self):
        return f"EV : {self.charge_level}/{self.battery_capacity} kWh"


# Charging Unit class
class ChargingUnit:
    # Constructor
    def __init__(self, max_output=22):
        self.max_output = max_output  # kW - user defined o.w. 22

    # Charge vehicle method
    def charge_vehicle(self, ev: ElectricVehicle, hours: float):
        charge_power = min(self.max_output, ev.max_power_capacity)
        charge_amount = charge_power * hours
        ev.charge(charge_amount)
        return charge_power

    # Log method
    def __str__(self):
        return f"Charging Unit : {self.max_output} kW"


# Simulation class
class Simulation:
    def __init__(self, connection_time: datetime, disconnection_time: datetime, interval_minutes=15):
        self.simulation_start_time = connection_time.replace(hour=9, minute=0, second=0)
        self.simulation_end_time = disconnection_time.replace(hour=21, minute=0, second=0)  
        if connection_time.date() != disconnection_time.date():
            raise ValueError("Connection and disconnection times must be on the same day!")      
        self.interval = timedelta(minutes=interval_minutes)
        self.one_minute = timedelta(minutes=1)
        self.connection_time = connection_time
        self.disconnection_time = disconnection_time
        if self.connection_time < self.simulation_start_time or self.disconnection_time > self.simulation_end_time\
            or self.connection_time > self.simulation_end_time or self.disconnection_time < self.simulation_start_time:
            raise ValueError("Connection and disconnection times must be between 09:00 and 21:00!")
        if self.connection_time >= self.disconnection_time:
            raise ValueError("Invalid connection or disconnection time!")
        self.current_time = self.simulation_start_time
        self.data = []
        self.result = None

    def run(self, ev: ElectricVehicle, charging_unit: ChargingUnit):
        net_energy_charged = 0

        # Determine initial charging power
        if self.connection_time == self.simulation_start_time and ev.state_of_charge < 1.0:
            charging_power = min(charging_unit.max_output, ev.max_power_capacity) # First minute charging power
        else:
            charging_power = 0
        
        # Store initial state at 09:00
        self.data.append({
            "Timestamp": self.current_time,
            "Charging Power (kW)": charging_power,
            "SOC (%)": ev.state_of_charge * 100,
            "Net Energy Charged (kWh)": net_energy_charged
        })

        while self.current_time < self.simulation_end_time:
            for i in range(int(self.interval.total_seconds()/60)):
                if self.connection_time <= self.current_time < self.disconnection_time:
                    if ev.state_of_charge < 1.0:
                        charging_power = charging_unit.charge_vehicle(ev, 1 / 60) # Calculation precision is 1 minute, returns charging power
                        net_energy_charged += charging_power/60  
                    else:
                        charging_power = 0
                else:
                    charging_power = 0
                self.current_time += self.one_minute
            self.data.append({
                "Timestamp": self.current_time,
                "Charging Power (kW)": charging_power,
                "SOC (%)": ev.state_of_charge * 100,
                "Net Energy Charged (kWh)": net_energy_charged
            })
            
    def get_results(self, path: str = './results/'):
        self.result = pd.DataFrame(self.data)
        self.result.to_json(path+'simulation_results.json', orient='records', date_format='iso')
        self.result.to_excel(path+'simulation_results.xlsx', index=False)
        plt.figure(figsize=(10, 6))
        plt.plot(self.result['Timestamp'], self.result['SOC (%)'], marker='o', linestyle='-')
        plt.xlabel('Time (HH:MM)')
        plt.ylabel('State of Charge (%)')
        plt.title(f'SOC Trajectory Over Simulation Period - {self.simulation_start_time.date()}')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))
        plt.tight_layout()
        plt.savefig(path + 'soc_trajectory.png')
        plt.close()
        return self.result
