"""
EchoChain Synthetic Data Generator
====================================
Generates production-grade, realistic synthetic datasets for:
1. Manufacturing Bill of Materials (BOM)
2. Internal Warranty Claims
3. 50,000 External Secondary Marketplace Listings across 4 platforms (eBay, FB Marketplace, OLX, BackMarket)
"""

import os
import json
import random
import csv
from datetime import datetime, timedelta

# Seed for reproducibility
random.seed(42)

OUTPUT_RAW_DIR = os.path.join("data", "raw")
OUTPUT_SAMPLE_DIR = os.path.join("datasets", "sample_data")

os.makedirs(OUTPUT_RAW_DIR, exist_ok=True)
os.makedirs(OUTPUT_SAMPLE_DIR, exist_ok=True)

# Electronics & Household Products Portfolio
PRODUCTS_CATALOG = [
    {
        "sku": "SKU-APP-IP14P-256",
        "product": "iPhone 14 Pro 256GB",
        "manufacturer": "Apple",
        "category": "Smartphones",
        "components": ["Lithium-Ion Battery", "OLED Display Assembly", "A16 Bionic Logic Board", "Titanium Frame", "Triple Camera Module"],
        "materials": ["Aluminum", "Glass", "Lithium", "Cobalt", "Rare Earth Elements"],
        "base_cost": 480.00,
        "carbon_footprint_kg": 65.5,
        "weight_g": 206,
        "warranty_months": 24,
    },
    {
        "sku": "SKU-APP-MBA-M2",
        "product": "MacBook Air M2 13-inch",
        "manufacturer": "Apple",
        "category": "Laptops",
        "components": ["M2 SoC Logic Board", "Liquid Retina Panel", "52.6Wh Battery", "Magic Keyboard", "MagSafe 3 Connector"],
        "materials": ["100% Recycled Aluminum", "Glass", "Copper", "Gold"],
        "base_cost": 650.00,
        "carbon_footprint_kg": 147.0,
        "weight_g": 1240,
        "warranty_months": 12,
    },
    {
        "sku": "SKU-SAM-GS23U-512",
        "product": "Galaxy S23 Ultra 512GB",
        "manufacturer": "Samsung",
        "category": "Smartphones",
        "components": ["Dynamic AMOLED 2X Screen", "Snapdragon 8 Gen 2 Board", "5000mAh Battery", "S-Pen Digitizer", "200MP Camera Sensor"],
        "materials": ["Armor Aluminum", "Gorilla Glass Victus 2", "Cobalt", "Recycled Plastics"],
        "base_cost": 440.00,
        "carbon_footprint_kg": 70.2,
        "weight_g": 234,
        "warranty_months": 24,
    },
    {
        "sku": "SKU-SON-WH1000-M5",
        "product": "WH-1000XM5 Wireless Headphones",
        "manufacturer": "Sony",
        "category": "Audio",
        "components": ["30mm Driver Units", "Dual Noise Canceling Chips", "Soft Fit Leather Earpads", "30-hour Battery", "Integrated Microphone Array"],
        "materials": ["ABS Plastic", "Synthetic Leather", "Neodymium Magnet"],
        "base_cost": 110.00,
        "carbon_footprint_kg": 18.4,
        "weight_g": 250,
        "warranty_months": 12,
    },
    {
        "sku": "SKU-DEL-XPS15-9530",
        "product": "XPS 15 Laptop i9 32GB",
        "manufacturer": "Dell",
        "category": "Laptops",
        "components": ["Intel i9-13900H Board", "NVIDIA RTX 4070 GPU", "4K OLED Touch Display", "86Wh Battery Module", "Carbon Fiber Palmrest"],
        "materials": ["CNC Machined Aluminum", "Carbon Fiber", "Copper Heatpipes"],
        "base_cost": 1100.00,
        "carbon_footprint_kg": 280.0,
        "weight_g": 1920,
        "warranty_months": 36,
    },
    {
        "sku": "SKU-DYS-V15-DETECT",
        "product": "V15 Detect Cordless Vacuum",
        "manufacturer": "Dyson",
        "category": "Home Appliances",
        "components": ["Hyperdymium Motor", "Laser Slim Fluffy Cleaner Head", "HEPA Filtration Cylinder", "7-cell Click-in Battery", "Cyclonic Dust Bin"],
        "materials": ["Polycarbonate", "ABS Plastic", "Aluminum Tube"],
        "base_cost": 210.00,
        "carbon_footprint_kg": 42.0,
        "weight_g": 3100,
        "warranty_months": 24,
    },
    {
        "sku": "SKU-LG-OLED65-C3",
        "product": "OLED65 C3 4K Smart TV",
        "manufacturer": "LG Electronics",
        "category": "Televisions",
        "components": ["65-inch Self-lit OLED Panel", "alpha9 AI Processor Gen6 Board", "40W 2.2 Ch Speaker Array", "Power Supply Unit", "Magical Remote Sensor"],
        "materials": ["Composite Fiber", "Glass", "Steel Chassis"],
        "base_cost": 780.00,
        "carbon_footprint_kg": 310.0,
        "weight_g": 16600,
        "warranty_months": 24,
    },
    {
        "sku": "SKU-NIN-SWITCH-OLED",
        "product": "Nintendo Switch OLED Model",
        "manufacturer": "Nintendo",
        "category": "Gaming",
        "components": ["7-inch OLED Display", "Tegra X1 System Board", "Joy-Con Rail Controls", "4310mAh Battery", "Docking Station Mainboard"],
        "materials": ["Plastic", "Glass", "Lithium"],
        "base_cost": 140.00,
        "carbon_footprint_kg": 26.5,
        "weight_g": 420,
        "warranty_months": 12,
    },
    {
        "sku": "SKU-BOS-WASH-SER8",
        "product": "Series 8 Front Load Washer",
        "manufacturer": "Bosch",
        "category": "Home Appliances",
        "components": ["EcoSilence Drive Motor", "VarioDrum Stainless Tub", "AquaStop Safety Valve", "Digital Touch Control Board", "Heavy Weight Ballast Block"],
        "materials": ["Stainless Steel", "Concrete Ballast", "Rubber", "Copper"],
        "base_cost": 420.00,
        "carbon_footprint_kg": 410.0,
        "weight_g": 73500,
        "warranty_months": 36,
    },
    {
        "sku": "SKU-CAN-EOS-R6M2",
        "product": "EOS R6 Mark II Mirrorless Body",
        "manufacturer": "Canon",
        "category": "Cameras",
        "components": ["24.2MP CMOS Full-Frame Sensor", "DIGIC X Image Processor Board", "5-axis In-Body Stabilizer", "EVF Display Module", "Magnesium Alloy Frame"],
        "materials": ["Magnesium Alloy", "Optical Glass", "Engineering Plastic"],
        "base_cost": 890.00,
        "carbon_footprint_kg": 95.0,
        "weight_g": 670,
        "warranty_months": 24,
    }
]

COUNTRIES = ["United States", "Germany", "Japan", "South Korea", "China", "Taiwan", "Mexico", "Vietnam"]
SUPPLIERS = ["Foxconn Tech", "TSMC Semiconductor", "Samsung SDI", "LG Display", "Murata Electronics", "Kyocera Components", "Nidec Motor", "Sony Semiconductor"]
MARKETPLACES = ["eBay", "Facebook Marketplace", "OLX", "BackMarket"]
CONDITIONS = ["New - Open Box", "Refurbished - Grade A", "Used - Excellent", "Used - Good", "Used - Fair", "For Parts / Non-Functional"]
CURRENCIES = ["USD", "EUR", "GBP", "BRL", "INR"]
CURRENCY_RATES = {"USD": 1.0, "EUR": 1.09, "GBP": 1.27, "BRL": 0.18, "INR": 0.012}

LOCATIONS = [
    "New York, USA", "Berlin, Germany", "London, UK", "Sao Paulo, Brazil", "Mumbai, India",
    "San Francisco, USA", "Tokyo, Japan", "Paris, France", "Toronto, Canada", "Sydney, Australia"
]

FAILURE_ISSUES = [
    "Battery Drain / Rapid Discharge", "Screen Flicker / Dead Pixels", "Thermal Throttling / Overheating",
    "Logic Board Power Failure", "Noisy Motor / Bearing Friction", "Camera Sensor Artifacts",
    "Wireless Connectivity Loss", "Physical Port Corruption", "Drifting Analog Stick", "Water Seal Compromise"
]

RESOLUTIONS = [
    "Battery Replacement", "Screen Assembly Swapped", "Refurbished Board Soldered",
    "Unit Replaced Under Warranty", "Component Cleaned & Re-calibrated", "Claim Rejected - User Damage"
]

def generate_manufacturing_bom():
    print("Generating Manufacturing BOM dataset...")
    rows = []
    start_date = datetime(2021, 1, 1)
    
    for item in PRODUCTS_CATALOG:
        for idx, comp in enumerate(item["components"]):
            prod_date = start_date + timedelta(days=random.randint(0, 1000))
            comp_cost = round(item["base_cost"] * (random.uniform(0.1, 0.35)), 2)
            comp_carbon = round(item["carbon_footprint_kg"] * (random.uniform(0.12, 0.3)), 2)
            comp_weight = round(item["weight_g"] * (random.uniform(0.08, 0.35)), 1)
            material = item["materials"][idx % len(item["materials"])]
            
            # Failure rate & claims
            failure_rate = round(random.uniform(0.01, 0.08), 4)
            warranty_claims = int(random.randint(15, 450) * (failure_rate * 20))
            
            rows.append({
                "SKU": item["sku"],
                "Product": item["product"],
                "Manufacturer": item["manufacturer"],
                "Category": item["category"],
                "Component": comp,
                "Manufacturing Cost": comp_cost,
                "Production Date": prod_date.strftime("%Y-%m-%d"),
                "Country": random.choice(COUNTRIES),
                "Supplier": random.choice(SUPPLIERS),
                "Carbon Footprint": comp_carbon,
                "Weight": comp_weight,
                "Material": material,
                "Warranty Period": item["warranty_months"],
                "Warranty Claims": warranty_claims,
                "Failure Rate": failure_rate
            })
            
    # Write to CSV
    for target_dir in [OUTPUT_RAW_DIR, OUTPUT_SAMPLE_DIR]:
        filepath = os.path.join(target_dir, "manufacturing_bom.csv")
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
            
    print(f"[OK] Generated {len(rows)} BOM component records.")

def generate_warranty_dataset(num_records=10000):
    print(f"Generating Warranty Claims dataset ({num_records} records)...")
    rows = []
    start_date = datetime(2022, 1, 1)
    
    for i in range(1, num_records + 1):
        item = random.choice(PRODUCTS_CATALOG)
        comp = random.choice(item["components"])
        issue = random.choice(FAILURE_ISSUES)
        resolution = random.choice(RESOLUTIONS)
        claim_date = start_date + timedelta(days=random.randint(0, 730))
        repair_cost = round(random.uniform(25.0, item["base_cost"] * 0.6), 2)
        
        rows.append({
            "Customer ID": f"CUST-{random.randint(10000, 99999)}",
            "SKU": item["sku"],
            "Issue": issue,
            "Failure Component": comp,
            "Claim Date": claim_date.strftime("%Y-%m-%d"),
            "Resolution": resolution,
            "Repair Cost": repair_cost
        })
        
    for target_dir in [OUTPUT_RAW_DIR, OUTPUT_SAMPLE_DIR]:
        filepath = os.path.join(target_dir, "warranty_claims.csv")
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
            
    print(f"[OK] Generated {len(rows)} warranty claim records.")

def generate_marketplace_listings(total_listings=50000):
    print(f"Generating Marketplace Listings dataset ({total_listings} listings)...")
    listings = []
    start_date = datetime(2023, 1, 1)
    
    # Title variations to test title-to-SKU matching
    title_templates = {
        "SKU-APP-IP14P-256": [
            "Apple iPhone 14 Pro 256GB Space Black - Excellent Condition",
            "iPhone 14 Pro - 256GB - Unlocked Deep Purple",
            "Apple iPhone 14 Pro (256 GB) - Gold (Refurbished)",
            "iPhone 14 Pro 256gb cracked back works great",
            "Apple iPhone 14 Pro 256GB - For parts or repair"
        ],
        "SKU-APP-MBA-M2": [
            "Apple MacBook Air M2 13.6 inch 256GB SSD Midnight",
            "MacBook Air 13\" M2 Chip 2022 Space Gray",
            "Apple MacBook Air M2 - 8GB RAM 256GB - Starlight Good",
            "2022 MacBook Air M2 13 inch Silver Refurbished Grade A",
            "MacBook Air M2 logic board bad - selling for parts"
        ],
        "SKU-SAM-GS23U-512": [
            "Samsung Galaxy S23 Ultra 512GB Phantom Black Unlocked",
            "Galaxy S23 Ultra 512 GB Cream - Mint Condition w/ Box",
            "Samsung Galaxy S23 Ultra - Green 512GB Dual SIM",
            "S23 Ultra 512GB - Minor screen scratches",
            "Samsung S23 Ultra 512gb non functional bootloop"
        ],
        "SKU-SON-WH1000-M5": [
            "Sony WH-1000XM5 Wireless Noise Canceling Headphones Black",
            "Sony WH1000XM5 Headphones - Silver Like New",
            "Sony WH-1000XM5 Over-Ear Bluetooth Headset",
            "Sony WH 1000 XM5 used earpads worn out",
            "Sony WH-1000XM5 left ear silent - parts only"
        ],
        "SKU-DEL-XPS15-9530": [
            "Dell XPS 15 9530 Laptop Intel Core i9 32GB RAM 1TB SSD RTX 4070",
            "Dell XPS 15 (9530) 15.6\" 3.5K OLED Touch i9-13900H",
            "Dell XPS 15 i9 32GB RAM 4K Display - Great Condition",
            "Dell XPS 15 Laptop 9530 - Used with minor cosmetic wear",
            "Dell XPS 15 9530 motherboard issue no power"
        ],
        "SKU-DYS-V15-DETECT": [
            "Dyson V15 Detect Cordless Vacuum Cleaner Yellow/Nickel",
            "Dyson V15 Detect Extra Cordless Vacuum - Complete Kit",
            "Dyson V15 Cordless Stick Vacuum - Refurbished Direct",
            "Dyson V15 Detect used missing motorhead",
            "Dyson V15 vacuum motor broken for parts"
        ],
        "SKU-LG-OLED65-C3": [
            "LG OLED65C3PUA 65-inch C3 Series 4K Smart TV 2023",
            "LG 65\" C3 OLED 4K UHD TV - Factory Refurbished",
            "LG OLED 65 C3 TV Open Box Display Model",
            "LG OLED 65 inch TV slight burn in fully functional",
            "LG 65 inch OLED C3 mainboard failure - screen intact"
        ],
        "SKU-NIN-SWITCH-OLED": [
            "Nintendo Switch OLED Model White Set w/ White Joy-Con",
            "Nintendo Switch - OLED Model HEG-001 Mario Red Edition",
            "Switch OLED Model 64GB Console - Gently Used",
            "Nintendo Switch OLED tablet only - screen scratches",
            "Nintendo Switch OLED bad game card reader parts"
        ],
        "SKU-BOS-WASH-SER8": [
            "Bosch Series 8 Front Load Washer 9kg 1400rpm White",
            "Bosch Serie 8 Washing Machine - Refurbished Grade A",
            "Bosch Front Load Washer Series 8 - Works Perfectly",
            "Bosch Series 8 Washer dented side panel",
            "Bosch Series 8 Washer drum bearing noise needs repair"
        ],
        "SKU-CAN-EOS-R6M2": [
            "Canon EOS R6 Mark II Mirrorless Digital Camera Body",
            "Canon EOS R6 Mark 2 Body - Low Shutter Count Mint",
            "Canon R6 Mark II 24.2MP Camera Body Refurbished",
            "Canon EOS R6 Mk II Used Body Only with battery",
            "Canon EOS R6 Mark II broken shutter mechanism"
        ]
    }
    
    for i in range(1, total_listings + 1):
        item = random.choice(PRODUCTS_CATALOG)
        sku = item["sku"]
        marketplace = random.choice(MARKETPLACES)
        condition = random.choice(CONDITIONS)
        title = random.choice(title_templates[sku])
        
        # Price variance based on condition
        base = item["base_cost"] * random.uniform(1.1, 1.8)
        if "Refurbished" in condition:
            price_usd = base * random.uniform(0.7, 0.85)
        elif "Excellent" in condition or "Open Box" in condition:
            price_usd = base * random.uniform(0.8, 0.95)
        elif "Good" in condition:
            price_usd = base * random.uniform(0.6, 0.75)
        elif "Fair" in condition:
            price_usd = base * random.uniform(0.4, 0.6)
        else: # Parts / Non-Functional
            price_usd = base * random.uniform(0.15, 0.35)
            
        currency = random.choice(CURRENCIES)
        price_local = round(price_usd / CURRENCY_RATES[currency], 2)
        
        rating = round(random.uniform(3.5, 5.0), 2) if marketplace != "OLX" else round(random.uniform(2.0, 4.8), 2)
        sold_count = random.randint(0, 150)
        list_date = start_date + timedelta(days=random.randint(0, 540))
        shipping = round(random.uniform(0.0, 35.0), 2)
        
        description = (
            f"{title}. Offered on {marketplace}. Verified condition: {condition}. "
            f"Seller located at {random.choice(LOCATIONS)}. Includes original hardware accessories."
        )
        
        listings.append({
            "listing_id": f"LIST-{marketplace[:3].upper()}-{100000 + i}",
            "marketplace": marketplace,
            "product_title": title,
            "condition": condition,
            "price": price_local,
            "currency": currency,
            "location": random.choice(LOCATIONS),
            "seller_rating": rating,
            "sold_count": sold_count,
            "listing_date": list_date.strftime("%Y-%m-%d"),
            "shipping_cost": shipping,
            "images_count": random.randint(1, 8),
            "description": description
        })

    # Save to JSON and CSV
    for target_dir in [OUTPUT_RAW_DIR, OUTPUT_SAMPLE_DIR]:
        json_path = os.path.join(target_dir, "marketplace_listings.json")
        csv_path = os.path.join(target_dir, "marketplace_listings.csv")
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(listings, f, indent=2)
            
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=listings[0].keys())
            writer.writeheader()
            writer.writerows(listings)
            
    print(f"[OK] Generated {len(listings)} marketplace listings.")

if __name__ == "__main__":
    print("=== EchoChain Data Generator Starting ===")
    generate_manufacturing_bom()
    generate_warranty_dataset(10000)
    generate_marketplace_listings(50000)
    print("=== All EchoChain Datasets Successfully Generated ===")
