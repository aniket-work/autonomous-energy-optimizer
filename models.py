from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class PriceData:
    timestamp: datetime
    grid_price: float  # Current grid price in $/kWh
    solar_production: float  # Current solar production in kW

@dataclass
class EnergyState:
    battery_level: float  # Current battery level in kWh
    battery_capacity: float  # Max battery capacity in kWh
    current_load: float  # Current house load in kW
    
    @property
    def battery_percentage(self) -> float:
        return (self.battery_level / self.battery_capacity) * 100

@dataclass
class Decision:
    action: str  # "CHARGE", "DISCHARGE", "HOLD"
    amount: float  # Amount of energy in kWh
    reason: str
