# Autonomous Home Energy Manager

> **How I Built an Agent to Slash Electricity Bills by 40% Using Solar & Price Forecasting**

![Title](https://raw.githubusercontent.com/aniket-work/autonomous-energy-optimizer/main/images/title-animation.gif)

## Overview
This project is an experimental Proof of Concept (PoC) exploring how an autonomous AI agent can optimize home energy usage. By simulating real-time electricity pricing (Time-of-Use) and solar panel generation, the agent intelligently manages battery charging and discharging cycles to minimize costs and maximize green energy utilization.

## Key Features
- **Dynamic Price Forecasting**: Simulates grid pricing that fluctuates based on demand.
- **Solar Production Prediction**: Models solar output based on time of day and random weather patterns.
- **Intelligent Battery Management**: Decides when to charge (low price/high solar) and discharge (high price).
- **Rich Terminal Interface**: vivid simulation logs and ASCII reporting.

## Project Structure
- `main.py`: The simulation loop and entry point.
- `agents.py`: Core logic for the `EnergyAgent`.
- `forecasting.py`: Simulation models for pricing and weather.
- `generate_diagrams.py`: Generates architecture diagrams.
- `generate_gif.py`: Creates the project's visual assets.

## Disclaimer
The views and opinions expressed here are solely my own and do not represent the views, positions, or opinions of my employer or any organization I am affiliated with. The content is based on my personal experience and experimentation and may be incomplete or incorrect. Any errors or misinterpretations are unintentional, and I apologize in advance if any statements are misunderstood or misrepresented.
