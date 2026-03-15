import pandas as pd
import re

INPUT_CSV = "data/mieszkania_trojmiasto.csv"
OUTPUT_CSV = "data/mieszkania_trojmiasto_clean.csv"

# Load data
df = pd.read_csv(INPUT_CSV)

# Remove duplicates
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

# Clean numeric columns
def clean_price(price_str):
    # Extract only the number before 'zł' (Polish currency)
    s = str(price_str)
    match = re.search(r"([0-9][0-9 .]*)\s*zł", s)
    if match:
        price = match.group(1)
        price = price.replace(" ", "").replace(".", "")
        return int(price)
    # Fallback: try to extract the largest number in the string
    numbers = re.findall(r"[0-9]{3,}", s)
    if numbers:
        return int(numbers[-1])
    return None

def clean_area(area_str):
    # Replace comma with dot, remove non-numeric except dot, convert to float
    area = re.sub(r",", ".", str(area_str))
    area = re.sub(r"[^0-9.]", "", area)
    return float(area) if area else None

def clean_rooms(rooms_str):
    # Remove non-digit characters and convert to int
    rooms = re.sub(r"[^0-9]", "", str(rooms_str))
    return int(rooms) if rooms else None

# Apply cleaning functions
df["price"] = df["price"].apply(clean_price)
df["area"] = df["area"].apply(clean_area)
df["rooms"] = df["rooms"].apply(clean_rooms)

# Remove rows with missing or zero values after cleaning
df = df.dropna(subset=["price", "area", "rooms"])
df = df[(df["price"] > 0) & (df["area"] > 0) & (df["rooms"] > 0)]

# Add new columns
df["price_per_m2"] = df["price"] / df["area"]
df["area_per_room"] = df["area"] / df["rooms"]

# Filter for Gdańsk, Gdynia, Sopot
df = df[df["city"].str.lower().isin(["gdansk", "gdynia", "sopot"])]

# Save cleaned data
df.to_csv(OUTPUT_CSV, index=False)

print(f"Cleaned data saved to {OUTPUT_CSV}. Shape: {df.shape}")
