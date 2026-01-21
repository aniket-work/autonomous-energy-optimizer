import time
import random
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel

from models import EnergyState, PriceData
from forecasting import PriceForecaster, SolarPredictor
from agents import EnergyAgent

console = Console()

def main():
    # Simulation Setup
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    current_time = start_time
    
    price_model = PriceForecaster()
    solar_model = SolarPredictor(max_output_kw=6.0)
    agent = EnergyAgent(charge_threshold=0.12, discharge_threshold=0.35)
    
    state = EnergyState(battery_level=5.0, battery_capacity=13.5, current_load=0.0) # Tesla Powerwall 2 specs
    
    total_savings = 0.0
    total_cost_without_agent = 0.0
    total_cost_with_agent = 0.0
    
    table = Table(title="Autonomous Energy Manager Simulation")
    table.add_column("Time", style="cyan")
    table.add_column("Grid Price", style="magenta")
    table.add_column("Solar (kW)", style="yellow")
    table.add_column("Load (kW)", style="white")
    table.add_column("Battery %", style="green")
    table.add_column("Action", style="bold blue")
    table.add_column("Savings ($)", style="bold green")

    console.print("[bold yellow]Initializing Autonomous Energy Manager...[/bold yellow]")
    time.sleep(1)
    console.print("[dim]Connecting to Smart Meter... OK[/dim]")
    time.sleep(0.5)
    console.print("[dim]Loading Price Forecast Models... OK[/dim]")
    time.sleep(0.5)
    console.print("[dim]Syncing with Solar Inverter... OK[/dim]\n")

    with Live(table, refresh_per_second=4) as live:
        for _ in range(24): # Simulate 24 hours
            # Update Simulated Environment
            market = PriceData(
                timestamp=current_time,
                grid_price=price_model.get_price(current_time),
                solar_production=solar_model.get_production(current_time)
            )
            
            # Simulate random home load (AC, lights, etc.)
            base_load = 0.5
            if 17 <= current_time.hour <= 22: base_load += 2.0 # Evening peak
            if 7 <= current_time.hour <= 9: base_load += 1.0 # Morning peak
            state.current_load = round(base_load + random.uniform(-0.2, 0.5), 2)
            
            # Agent Decision
            decision = agent.decide(state, market)
            
            # Apply Decision & Update State
            cost_step_no_agent = (state.current_load - market.solar_production) * market.grid_price
            if cost_step_no_agent < 0: cost_step_no_agent = 0 # Net metering simplified
            
            actual_cost = 0.0
            
            if decision.action == "CHARGE":
                state.battery_level = min(state.battery_capacity, state.battery_level + decision.amount)
                # Cost is grid price for amount charged + any load not covered
                # Simplified: assuming charge comes from grid or excess solar
                if "Excess Solar" in decision.reason:
                    actual_cost = 0 # Free energy!
                else:
                    actual_cost = (decision.amount + max(0, state.current_load - market.solar_production)) * market.grid_price

            elif decision.action == "DISCHARGE":
                state.battery_level = max(0, state.battery_level - decision.amount)
                # We used battery, so cost is 0 for that portion
                remaining_load = max(0, state.current_load - market.solar_production - decision.amount)
                actual_cost = remaining_load * market.grid_price
            
            elif decision.action == "HOLD":
                # Standard grid usage
                net_needed = max(0, state.current_load - market.solar_production)
                actual_cost = net_needed * market.grid_price

            total_cost_without_agent += cost_step_no_agent
            total_cost_with_agent += actual_cost
            savings = total_cost_without_agent - total_cost_with_agent
            
            # Render Row
            table.add_row(
                current_time.strftime("%H:%00"),
                f"${market.grid_price:.2f}/kWh",
                f"{market.solar_production:.2f}",
                f"{state.current_load:.2f}",
                f"{state.battery_percentage:.1f}%",
                decision.reason,
                f"${savings:.2f}"
            )
            
            current_time += timedelta(hours=1)
            time.sleep(0.15) # Typing effect speed

    console.print(f"\n[bold green]DAILY REPORT:[/bold green]")
    console.print(f"Total Cost (Standard): ${total_cost_without_agent:.2f}")
    console.print(f"Total Cost (AI Agent): ${total_cost_with_agent:.2f}")
    console.print(f"Total Savings: [bold]${savings:.2f}[/bold] ({(savings/total_cost_without_agent)*100:.1f}%)")

if __name__ == "__main__":
    main()
