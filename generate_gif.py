import random
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

# --- Configuration ---
WIDTH = 800
HEIGHT = 450
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (0, 255, 0) # Terminal Green
HIGHLIGHT_COLOR = (255, 255, 255)
UI_BG_COLOR = (15, 23, 42) # Dark Slate Blue
CARD_COLOR = (30, 41, 59)
FONT_PATH = "/System/Library/Fonts/Monaco.ttf" 

def create_base_terminal():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    # Title Bar
    draw.rectangle([0, 0, WIDTH, 30], fill=(50, 50, 50))
    # Buttons
    draw.ellipse([10, 8, 22, 20], fill=(255, 95, 86)) # Red
    draw.ellipse([30, 8, 42, 20], fill=(255, 189, 46)) # Yellow
    draw.ellipse([50, 8, 62, 20], fill=(39, 201, 63)) # Green
    draw.text((WIDTH//2 - 40, 5), "energy-agent -- zsh", fill=(200, 200, 200), font=ImageFont.truetype(FONT_PATH, 14))
    return img

def create_terminal_frame(text_lines, cursor_visible=True):
    img = create_base_terminal()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 14)
    
    y = 40
    for line in text_lines:
        draw.text((15, y), line, fill=TEXT_COLOR, font=font)
        y += 18
        
    if cursor_visible:
        # Draw cursor at end of last line
        if text_lines:
            last_line = text_lines[-1]
            width = font.getbbox(last_line)[2]
            draw.rectangle([15 + width + 2, y - 18, 15 + width + 10, y - 4], fill=TEXT_COLOR)
        else:
             draw.rectangle([15, y - 18, 23, y - 4], fill=TEXT_COLOR)
            
    return img

def create_ui_dashboard(savings, battery_pct, cost_std, cost_ai):
    img = Image.new('RGB', (WIDTH, HEIGHT), UI_BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Fonts
    title_font = ImageFont.truetype("Arial.ttf", 36)
    value_font = ImageFont.truetype("Arial.ttf", 48)
    label_font = ImageFont.truetype("Arial.ttf", 18)
    
    # Try to load Arial, fallback to default if not found (MacOS usually has Arial)
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 36)
        value_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 48)
        label_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
    except:
        pass # Use default

    # Convert to floats for math
    savings_f = float(savings)
    cost_std_f = float(cost_std)
    cost_ai_f = float(cost_ai)

    # Header
    draw.text((40, 40), "Auto-Energy Optimizer Results", fill=(255, 255, 255), font=title_font)
    
    # Card 1: Savings
    draw.rectangle([40, 100, 360, 250], fill=CARD_COLOR, outline=(0, 200, 100), width=2)
    draw.text((60, 120), "Total Savings", fill=(200, 200, 200), font=label_font)
    draw.text((60, 160), f"${savings}", fill=(0, 255, 100), font=value_font)
    
    # Card 2: Battery Status
    draw.rectangle([400, 100, 720, 250], fill=CARD_COLOR)
    draw.text((420, 120), "Battery End State", fill=(200, 200, 200), font=label_font)
    draw.text((420, 160), f"{battery_pct}%", fill=(0, 150, 255), font=value_font)
    
    # Card 3: Comparison
    draw.rectangle([40, 280, 720, 400], fill=CARD_COLOR)
    draw.text((60, 300), "Optimization Impact", fill=(200, 200, 200), font=label_font)
    
    # Bar Chart inside card
    max_width = 500
    bar_height = 30
    
    # Standard Cost Bar
    draw.text((60, 340), "Standard", fill=(255, 100, 100), font=label_font)
    draw.rectangle([160, 340, 160 + max_width, 340 + bar_height], fill=(50, 50, 50)) # Track
    draw.rectangle([160, 340, 160 + max_width, 340 + bar_height], fill=(255, 100, 100)) # Fill (100%)
    draw.text((160 + max_width + 10, 345), f"${cost_std}", fill=HIGHLIGHT_COLOR, font=label_font)

    # AI Cost Bar
    ratio = cost_ai_f / cost_std_f if cost_std_f > 0 else 0
    draw.text((60, 380), "AI Agent", fill=(0, 255, 100), font=label_font)
    draw.rectangle([160, 380, 160 + max_width, 380 + bar_height], fill=(50, 50, 50)) # Track
    draw.rectangle([160, 380, 160 + (max_width * ratio), 380 + bar_height], fill=(0, 255, 100)) # Fill
    draw.text((160 + (max_width * ratio) + 10, 385), f"${cost_ai}", fill=HIGHLIGHT_COLOR, font=label_font)

    return img

def main():
    if not os.path.exists("images"):
        os.makedirs("images")

    frames = []
    
    # Part 1: Terminal Animation
    # Typing command
    command = "python main.py"
    current_text = "$ "
    for char in command:
        current_text += char
        frames.append(create_terminal_frame([current_text], cursor_visible=True))
        frames.append(create_terminal_frame([current_text], cursor_visible=False)) # Blink speed up

    # Execution logs
    logs = [
        "$ python main.py",
        "[bold yellow]Initializing Autonomous Energy Manager...[/]",
        "[dim]Connecting to Smart Meter... OK[/]",
        "[dim]Loading Price Forecast Models... OK[/]",
        "[dim]Syncing with Solar Inverter... OK[/]",
        "",
        "Time   Grid Price   Solar   Load   Batt %   Action          Savings",
        "-------------------------------------------------------------------",
        "08:00  $0.25/kWh    0.5kW   1.2kW  15.0%    HOLD            $0.00",
        "09:00  $0.20/kWh    1.8kW   1.1kW  15.0%    CHARGE          $0.12",
        "10:00  $0.18/kWh    3.2kW   0.8kW  35.0%    CHARGE          $0.45",
        "11:00  $0.18/kWh    4.5kW   0.9kW  60.0%    CHARGE          $0.68",
        "...",
        "17:00  $0.45/kWh    0.2kW   2.5kW  95.0%    DISCHARGE       $1.15",
        "18:00  $0.45/kWh    0.0kW   2.8kW  75.0%    DISCHARGE       $1.26",
        "",
        "[bold green]DAILY REPORT:[/]",
        "Total Cost (Standard): $18.45",
        "Total Cost (AI Agent): $10.12",
        "Total Savings: $8.33 (45.1%)",
        ""
    ]
    
    displayed_logs = []
    for line in logs:
        displayed_logs.append(line)
        if len(displayed_logs) > 22: # Scroll
            displayed_logs.pop(0)
        frames.append(create_terminal_frame(displayed_logs, cursor_visible=True))
        if "DAILY REPORT" in line: # Pause at end for effect
             for _ in range(15):
                 frames.append(create_terminal_frame(displayed_logs, cursor_visible=True))

    # Hold terminal result
    for _ in range(30):
        frames.append(create_terminal_frame(displayed_logs, cursor_visible=False))

    # Part 2: Transition to UI
    # Part 3: UI Dashboard
    ui_frame = create_ui_dashboard("8.33", "35", "18.45", "10.12")
    for _ in range(50): # Hold for 5 seconds
        frames.append(ui_frame)

    # Save
    print("Saving GIF...")
    # Quantize to improve palette quality for mixed content
    frames[0].save(
        "images/title-animation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100, # 100ms per frame
        loop=0
    )
    print("Saved images/title-animation.gif")

if __name__ == "__main__":
    main()
