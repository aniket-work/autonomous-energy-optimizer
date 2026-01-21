from models import EnergyState, PriceData, Decision

class EnergyAgent:
    def __init__(self, charge_threshold: float = 0.15, discharge_threshold: float = 0.30):
        self.charge_threshold = charge_threshold # Price below which we charge from grid
        self.discharge_threshold = discharge_threshold # Price above which we discharge to grid/home

    def decide(self, state: EnergyState, market: PriceData) -> Decision:
        # 1. Critical usage: If solar < load, we need energy. 
        #    Ideally forecast checks if we should use battery or grid based on CURRENT price vs FUTURE price,
        #    but for a simple agent, we use simple thresholds.
        
        net_load = state.current_load - market.solar_production
        
        # Scenario A: Excess Solar
        if net_load < 0:
            excess = abs(net_load)
            if state.battery_level < state.battery_capacity:
                return Decision("CHARGE", excess, "Excess Solar -> Battery")
            else:
                return Decision("HOLD", 0, "Battery Full, Solar to Grid (Net Metering)")

        # Scenario B: Solar Deficit (Need Energy)
        # Should we use battery or grid?
        if market.grid_price >= self.discharge_threshold:
            # High price time! Use battery if possible.
            if state.battery_level > 0:
                amount = min(state.battery_level, net_load)
                return Decision("DISCHARGE", amount, "Peak Price -> Discharge Battery")
        
        if market.grid_price <= self.charge_threshold:
            # Low price time! Charge battery if not full, also cover load from grid.
            if state.battery_level < state.battery_capacity:
                charge_amount = min(5.0, state.battery_capacity - state.battery_level) # Max charge rate 5kW
                return Decision("CHARGE", charge_amount, f"Low Price (${market.grid_price}) -> Charge")
        
        # Default: Cover load from battery if available to be self-sufficient, else grid
        if state.battery_level > state.current_load * 2: # Keep some reserve
             return Decision("DISCHARGE", net_load, "Self-Consumption")
             
        return Decision("HOLD", 0, "Using Grid (Normal Operation)")
