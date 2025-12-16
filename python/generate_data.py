import pandas as pd
import numpy as np
from datetime import timedelta
import os

# -----------------------------
# Reproducibility
# -----------------------------
np.random.seed(42)

# -----------------------------
# Configuration
# -----------------------------
N_USERS = 12000

CITIES_TIER1 = ["Delhi", "Mumbai", "Bangalore"]
CITIES_OTHER = ["Jaipur", "Indore", "Lucknow", "Patna"]
DEVICES = ["mobile", "desktop"]

# -----------------------------
# Resolve absolute paths safely
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))        # /python
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..")) # project root
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(DATA_DIR, "events.csv")

# -----------------------------
# Data generation
# -----------------------------
events = []
start_date = pd.Timestamp("2024-01-01")

for user_id in range(1, N_USERS + 1):
    sessions = np.random.randint(1, 4)
    device = np.random.choice(DEVICES, p=[0.65, 0.35])
    city = np.random.choice(
        CITIES_TIER1 + CITIES_OTHER,
        p=[0.18, 0.18, 0.18, 0.12, 0.12, 0.11, 0.11]
    )

    for s in range(sessions):
        session_id = f"{user_id}_{s}"
        t = start_date + pd.to_timedelta(np.random.randint(0, 180), unit="D")
        hour = np.random.randint(0, 24)
        t += pd.to_timedelta(hour, unit="h")

        # Signup
        events.append([user_id, session_id, t, "signup", device, city])

        # Product view
        if np.random.rand() < 0.85:
            t += timedelta(minutes=2)
            events.append([user_id, session_id, t, "product_view", device, city])

        # Add to cart
        if np.random.rand() < 0.60:
            t += timedelta(minutes=3)
            events.append([user_id, session_id, t, "add_to_cart", device, city])

        # Checkout probability adjustments
        checkout_prob = 0.45

        if device == "mobile":
            checkout_prob -= 0.15

        if hour >= 22 or hour <= 4:
            checkout_prob -= 0.10

        if city in CITIES_TIER1:
            checkout_prob -= 0.05

        # Checkout
        if np.random.rand() < checkout_prob:
            t += timedelta(minutes=4)
            events.append([user_id, session_id, t, "checkout", device, city])

# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame(
    events,
    columns=["user_id", "session_id", "event_time", "event_name", "device", "city"]
)

df = df.sort_values(["user_id", "event_time"])

# -----------------------------
# Save to CSV
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Dataset created successfully")
print(f"📁 File location: {OUTPUT_FILE}")
print(f"📊 Rows: {len(df):,}")
