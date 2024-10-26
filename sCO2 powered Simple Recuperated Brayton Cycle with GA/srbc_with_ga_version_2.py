# -*- coding: utf-8 -*-
"""srbc with ga version 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HyHHeS0IZewyU8_7hc7PMdpYQnPwke_n
"""

pip install CoolProp pygad matplotlib pandas

import CoolProp.CoolProp as CP
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pygad

# Constants
mass_flow_rate_cycle = 93.2  # kg/s
gas_cooler_temp_out = 305.4  # K
gas_cooler_pressure_out = 7700  # kPa
turbine_pressure_out = 7855  # kPa
ht_recuperator_temp_out = 479.1  # K
losses = 0.07

# Function to calculate thermal efficiency for a given pressure ratio and machinery performance
def calculate_efficiency(pressure_ratio, eff_turbine, eff_compressor, max_temp):
    fluid = 'CO2'
    primary_hx_temp_out = max_temp
    primary_hx_pressure = gas_cooler_pressure_out * pressure_ratio

    # Compressor inlet state (Point 1)
    T_inlet_compressor = gas_cooler_temp_out
    P_inlet_compressor = gas_cooler_pressure_out
    h_inlet_compressor = CP.PropsSI('H', 'T', T_inlet_compressor, 'P', P_inlet_compressor * 1000, fluid)
    s_inlet_compressor = CP.PropsSI('S', 'T', T_inlet_compressor, 'P', P_inlet_compressor * 1000, fluid)

    # Compressor outlet state (Point 2)
    P_out_compressor = P_inlet_compressor * pressure_ratio
    h_out_isentropic_compressor = CP.PropsSI('H', 'P', P_out_compressor * 1000, 'S', s_inlet_compressor, fluid)
    h_out_actual_compressor = h_inlet_compressor + (h_out_isentropic_compressor - h_inlet_compressor) / eff_compressor
    T_out_compressor = CP.PropsSI('T', 'H', h_out_actual_compressor, 'P', P_out_compressor * 1000, fluid)

    # HT recuperator outlet state (Point 4)
    T_out_ht_recuperator_high = ht_recuperator_temp_out
    P_out_ht_recuperator_high = primary_hx_pressure
    h_out_ht_recuperator_high = CP.PropsSI('H', 'T', T_out_ht_recuperator_high, 'P', P_out_ht_recuperator_high * 1000, fluid)

    # Heater outlet state (Point 5)
    T_out_heater = primary_hx_temp_out
    h_out_heater = CP.PropsSI('H', 'T', T_out_heater, 'P', primary_hx_pressure * 1000, fluid)

    # Turbine outlet state (Point 6)
    P_out_turbine = turbine_pressure_out
    h_out_isentropic_turbine = CP.PropsSI('H', 'P', P_out_turbine * 1000, 'S', CP.PropsSI('S', 'H', h_out_heater, 'P', primary_hx_pressure * 1000, fluid), fluid)
    h_out_actual_turbine = h_out_heater - eff_turbine * (h_out_heater - h_out_isentropic_turbine)
    T_out_turbine = CP.PropsSI('T', 'H', h_out_actual_turbine, 'P', P_out_turbine * 1000, fluid)

    # Overall cycle efficiency
    W_turbine = mass_flow_rate_cycle * (h_out_heater - h_out_actual_turbine)
    W_comp = mass_flow_rate_cycle * (h_out_actual_compressor - h_inlet_compressor)
    Q_in = mass_flow_rate_cycle * (h_out_heater - h_out_ht_recuperator_high)

    net_power_output = (W_turbine - W_comp) * (1 - losses)
    thermal_efficiency = net_power_output / Q_in

    return thermal_efficiency, net_power_output, Q_in, W_turbine, W_comp

# Define temperature ranges, turbine/compressor efficiencies, and pressure ratios
temperature_ranges = [500 + 273.15, 600 + 273.15, 700 + 273.15, 800 + 273.15]  # K
turbine_efficiencies = [0.80, 0.85, 0.90]
compressor_efficiencies = [0.75, 0.80, 0.85]
pressure_ratios = np.linspace(2.0, 10.0, 100)

# Empty lists for results
compressor_results = []
turbine_results = []
temperature_results = []

# 1. Effect of varying compressor efficiency on cycle parameters
for eff_compressor in compressor_efficiencies:
    for temp in temperature_ranges:
        efficiencies = []
        for pr in pressure_ratios:
            eff, net_power, q_in, w_turbine, w_comp = calculate_efficiency(pr, 0.85, eff_compressor, temp)  # Assume turbine efficiency = 85%
            efficiencies.append([temp - 273.15, pr, eff_compressor, eff, net_power, q_in, w_turbine, w_comp])
        compressor_results.append(efficiencies)

# 2. Effect of varying turbine efficiency on cycle parameters
for eff_turbine in turbine_efficiencies:
    for temp in temperature_ranges:
        efficiencies = []
        for pr in pressure_ratios:
            eff, net_power, q_in, w_turbine, w_comp = calculate_efficiency(pr, eff_turbine, 0.85, temp)  # Assume compressor efficiency = 85%
            efficiencies.append([temp - 273.15, pr, eff_turbine, eff, net_power, q_in, w_turbine, w_comp])
        turbine_results.append(efficiencies)

# 3. Effect of varying cycle temperature on cycle parameters
for temp in temperature_ranges:
    efficiencies = []
    for pr in pressure_ratios:
        eff, net_power, q_in, w_turbine, w_comp = calculate_efficiency(pr, 0.85, 0.85, temp)  # Assume turbine and compressor efficiency = 85%
        efficiencies.append([temp - 273.15, pr, eff, net_power, q_in, w_turbine, w_comp])
    temperature_results.append(efficiencies)

# Plot effect of varying compressor efficiencies
for i, eff_compressor in enumerate(compressor_efficiencies):
    results = np.array(compressor_results[i])
    plt.plot(results[:, 1], results[:, 3], label=f'Compressor Efficiency = {eff_compressor}')
plt.xlabel('Pressure Ratio')
plt.ylabel('Thermal Efficiency')
plt.title('Effect of Compressor Efficiency on Thermal Efficiency')
plt.legend()
plt.grid(True)
plt.show()

# Plot effect of varying turbine efficiencies
for i, eff_turbine in enumerate(turbine_efficiencies):
    results = np.array(turbine_results[i])
    plt.plot(results[:, 1], results[:, 3], label=f'Turbine Efficiency = {eff_turbine}')
plt.xlabel('Pressure Ratio')
plt.ylabel('Thermal Efficiency')
plt.title('Effect of Turbine Efficiency on Thermal Efficiency')
plt.legend()
plt.grid(True)
plt.show()

# Plot effect of varying cycle temperatures
for i, temp in enumerate(temperature_ranges):
    results = np.array(temperature_results[i])
    plt.plot(results[:, 1], results[:, 3], label=f'Temperature = {temp - 273.15} °C')
plt.xlabel('Pressure Ratio')
plt.ylabel('Thermal Efficiency')
plt.title('Effect of Cycle Temperature on Thermal Efficiency')
plt.legend()
plt.grid(True)
plt.show()

# Tabulate results
compressor_df = pd.DataFrame(np.vstack(compressor_results), columns=['Temp (°C)', 'Pressure Ratio', 'Compressor Eff', 'Thermal Eff', 'Net Power Output', 'Heat In', 'Work Turbine', 'Work Compressor'])
turbine_df = pd.DataFrame(np.vstack(turbine_results), columns=['Temp (°C)', 'Pressure Ratio', 'Turbine Eff', 'Thermal Eff', 'Net Power Output', 'Heat In', 'Work Turbine', 'Work Compressor'])
temperature_df = pd.DataFrame(np.vstack(temperature_results), columns=['Temp (°C)', 'Pressure Ratio', 'Thermal Eff', 'Net Power Output', 'Heat In', 'Work Turbine', 'Work Compressor'])

print("\nCompressor Efficiency Results:")
print(compressor_df)

print("\nTurbine Efficiency Results:")
print(turbine_df)

print("\nTemperature Results:")
print(temperature_df)

# GA Optimization
def fitness_function(ga_instance, solution, solution_idx):
    eff_turbine, eff_compressor, pressure_ratio, max_temp = solution
    efficiency, _, _, _, _ = calculate_efficiency(pressure_ratio, eff_turbine, eff_compressor, max_temp)
    return efficiency

# Set up GA
ga_instance = pygad.GA(
    num_generations=100,
    num_parents_mating=5,
    fitness_func=fitness_function,
    sol_per_pop=20,
    num_genes=4,
    gene_space=[
        {'low': 0.7, 'high': 0.95},  # Turbine Efficiency
        {'low': 0.7, 'high': 0.95},  # Compressor Efficiency
        {'low': 2.0, 'high': 10.0},  # Pressure Ratio
        {'low': 773.15, 'high': 1073.15}  # Maximum Temperature (500°C to 800°C)
    ],
    parent_selection_type="sss",
    crossover_type="single_point",
    mutation_type="random",
    mutation_percent_genes=25
)

# Run GA optimization
ga_instance.run()

# Best solution from GA
best_solution, best_fitness, _ = ga_instance.best_solution()
best_turbine_efficiency, best_compressor_efficiency, best_pressure_ratio, best_max_temp = best_solution
best_max_temp_c = best_max_temp - 273.15  # Convert temperature to Celsius

# Display GA optimized results
print("\nGA Optimized Results:")
print(f"Best Turbine Efficiency: {best_turbine_efficiency}")
print(f"Best Compressor Efficiency: {best_compressor_efficiency}")
print(f"Best Pressure Ratio: {best_pressure_ratio}")
print(f"Best Maximum Temperature (°C): {best_max_temp_c}")
print(f"Best Thermal Efficiency: {best_fitness}")

# Plot comparison of baseline and GA optimized pressure ratios
baseline_opt_prs = compressor_df.groupby(['Temp (°C)'])['Pressure Ratio'].mean()  # Adjust this line depending on your preferred comparison
plt.plot(baseline_opt_prs.index, baseline_opt_prs.values, label="Baseline Optimal PR", marker='o')

plt.scatter([best_max_temp_c], [best_pressure_ratio], color='red', label="GA Optimized PR", s=100)
plt.xlabel('Cycle Temperature (°C)')
plt.ylabel('Optimal Pressure Ratio')
plt.title('Comparison of Baseline and GA Optimized Pressure Ratios')
plt.legend()
plt.grid(True)
plt.show()

