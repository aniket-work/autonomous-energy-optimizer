import math
import random
from datetime import datetime, timedelta

class PriceForecaster:
    def __init__(self):
        # Base TOU pricing: Low (Night), High (Evening), Mid (Day)
        self.base_prices = {
            0: 0.10, 1: 0.10, 2: 0.10, 3: 0.10, 4: 0.10, 5: 0.12,
            6: 0.15, 7: 0.20, 8: 0.25, 9: 0.20, 10: 0.18, 11: 0.18,
            12: 0.18, 13: 0.18, 14: 0.20, 15: 0.25, 16: 0.35, 17: 0.45, # Peak
            18: 0.45, 19: 0.40, 20: 0.30, 21: 0.20, 22: 0.15, 23: 0.12
        }

    def get_price(self, timestamp: datetime) -> float:
        hour = timestamp.hour
        base = self.base_prices.get(hour, 0.15)
        # Add random volatility simulation
        volatility = random.uniform(-0.02, 0.05)
        return max(0.05, round(base + volatility, 3))

class SolarPredictor:
    def __init__(self, max_output_kw: float = 5.0):
        self.max_output = max_output_kw
    
    def get_production(self, timestamp: datetime) -> float:
        hour = timestamp.hour
        # Simple bell curve for solar production (6am - 6pm)
        if 6 <= hour <= 18:
            # Peak at 12
            factor = 1 - (abs(hour - 12) / 6)
            # Add random cloud cover
            cloud_cover = random.uniform(0.7, 1.0)
            production = self.max_output * factor * cloud_cover
            return max(0.0, round(production, 2))
        return 0.0
