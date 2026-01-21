import base64
import requests
import os

diagrams = {
    "title_diagram": """graph TD
    subgraph " "
    A[Autonomous Home Energy Manager] --- B(AI Simulation)
    end
    style A fill:#00E676,stroke:#333,stroke-width:2px,color:black,font-size:20px
    style B fill:#FFFFFF,stroke:#333,stroke-width:2px,color:black
    """,
    
    "architecture_diagram": """graph TB
    subgraph "External Environment"
    A[Grid Pricing API] --> B(PriceForecaster)
    C[Solar Inverter] --> D(SolarPredictor)
    E[Smart Meter] --> F(EnergyState)
    end
    
    subgraph "Autonomous Agent"
    B --> G{EnergyAgent}
    D --> G
    F --> G
    G --> H[BatteryManager]
    end
    
    subgraph "Control"
    H --> I[Battery Storage]
    H --> J[Smart Grid]
    end
    
    style G fill:#f9f,stroke:#333,stroke-width:4px
    """,
    
    "sequence_diagram": """sequenceDiagram
    participant Main as Simulation Loop
    participant Env as Environment
    participant Agent as EnergyAgent
    participant Batt as Battery

    loop Every Hour
        Main->>Env: Get Market Data
        Env-->>Main: Returns State
        Main->>Agent: decide(state, market_data)
        Agent->>Agent: Check Price Tiers
        alt High Price
            Agent-->>Main: DISCHARGE
        else Low Price
            Agent-->>Main: CHARGE
        else Normal
            Agent-->>Main: HOLD
        end
        Main->>Batt: Apply Action
        Batt-->>Main: New SOC
    end
    """,
    
    "flow_diagram": """graph TD
    Start[Start Simulation] --> Init[Initialize Models]
    Init --> Loop{Hourly Loop}
    Loop --> Read[Read Factors]
    Read --> Check{Net Load < 0?}
    
    Check -- Yes --> Full{Battery Full?}
    Full -- No --> Charge[Charge Battery]
    Full -- Yes --> Export[Export to Grid]
    
    Check -- No --> Price{Price High?}
    Price -- Yes --> BatAvail{Battery > 0?}
    BatAvail -- Yes --> Discharge[Discharge Battery]
    BatAvail -- No --> Grid[Buy from Grid]
    
    Price -- No --> ChargeGrid[Charge from Grid]
    
    Charge --> Next[Next Hour]
    Export --> Next
    Discharge --> Next
    Grid --> Next
    ChargeGrid --> Next
    
    Next --> Loop
    """
}

def generate():
    if not os.path.exists("images"):
        os.makedirs("images")
        
    for name, code in diagrams.items():
        print(f"Generating {name}...")
        encoded = base64.b64encode(code.encode()).decode()
        url = f"https://mermaid.ink/img/{encoded}?bgColor=white"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(f"images/{name}.png", 'wb') as f:
                    f.write(response.content)
                print(f"Saved images/{name}.png")
            else:
                print(f"Failed to generate {name}: Status {response.status_code}")
        except Exception as e:
            print(f"Error generating {name}: {e}")

if __name__ == "__main__":
    generate()
