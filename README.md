# EV_Charge_Sim
A simulation for an EV charging scenario.
An example of usage can be found in sample.py
The necessary class definitions and methods can be found in utils.py
The results are saved in the results folder by default.

Assumptions:
  - Electric vehicle (EV) has a battery capacity of 50 kWh, SOC of 10% and a maximum power capacity of 11 kW by default.
  - Charging unit has a maximum output of 22 kW by default.
  - Only one EV can be charged at a time.
  - Simulation runs between 9:00 and 21:00 for a given date.
  - Results are saved with 15-minute intervals. Calculation precision is 1 minute.
    
How to Use:
  - Set up and activate a virtual environment
  - Install dependencies by requirements.txt
  - Run sample.py or implement utils.py in your project
  - The resulting data is saved in .json and .xlsx format
  - SoC trajectory graph is saved as .png 
