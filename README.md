**sCO₂-Powered Waste Heat Recovery (WHR) Cycles**

_Overview_

This repository contains resources, models, and documentation focused on Waste Heat Recovery (WHR) cycles powered by supercritical carbon dioxide (sCO₂). These systems capture waste heat from industrial processes and convert it into useful power, thus enhancing energy efficiency and reducing emissions. Leveraging sCO₂ as a working fluid offers benefits such as high efficiency, a compact design, and a reduced environmental footprint, making it an ideal solution for waste heat recovery applications.

_Why sCO₂ for WHR?_

Supercritical carbon dioxide is gaining traction in thermodynamic cycle applications due to its unique properties:

-High Efficiency: sCO₂ cycles can achieve higher thermal efficiencies than traditional steam cycles, particularly at moderate temperatures.

-Compact System Design: The dense nature of sCO₂ at supercritical conditions allows for smaller turbomachinery and heat exchangers.

-Environmental Benefits: CO₂ is a non-toxic, readily available working fluid with a low global warming potential (when not leaked), making it an environmentally friendly option.

_Repository Contents_

-Model Files: Simulation models of various sCO₂-WHR cycle configurations.

-Performance Data: Datasets for cycle performance under different operating conditions and configurations.

-Scripts: Python scripts and other code for analysis, optimization, and visualization.

-Documentation: Detailed descriptions and insights on WHR cycle principles, sCO₂ properties, and system performance analysis.

_Getting Started_

**Prerequisites**

-Python: For running the simulation and analysis scripts.

-CoolProp (or similar thermodynamic library): For calculating sCO₂ properties and cycle efficiencies.

-Matplotlib: For visualization of cycle performance metrics.

To install the necessary packages, you can use the following commands:

##bash

Copy code

pip install CoolProp matplotlib

Running the Simulations

Clone the repository:

##bash

Copy code

git clone https://github.com/your-username/Supercritical-CO2-powered-Waste-Heat-Recovery-Cycles.git

cd Supercritical-CO2-powered-Waste-Heat-Recovery-Cycles

Run the main simulation script:

##bash

Copy code

python main_simulation.py

This script will load the required data, simulate the sCO₂-WHR cycle, and output efficiency metrics along with visualizations of the cycle.

_Applications_

-Industrial Heat Recovery: Capturing waste heat from high-temperature industrial processes such as steelmaking, glass production, and cement manufacturing.

-Power Generation: Enhancing the efficiency of power plants by recovering heat from exhaust gases.

-Renewable Energy: Integrating with solar and geothermal energy sources to improve overall energy yield.

_License_

This project is licensed under the MIT License. See the LICENSE file for more details.

