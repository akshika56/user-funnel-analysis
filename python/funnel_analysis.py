import pandas as pd
import numpy as np
import os

# -----------------------------
# Resolve paths safely
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

DATA_FILE = os.path.join(DATA_DIR, "events.csv")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_FILE, parse_dates=["event_time"])

print(f"Loaded {len(df):,} events")
print(f"Unique users: {df.user_id.nunique():,}")

# -----------------------------
# Basic sanity checks
# -----------------------------
assert df.event_time.is_monotonic_increasing is False, "Expected mixed timestamps"
assert df.event_name.isin(
    ["signup", "product_view", "add_to_cart", "checkout"]
).all(), "Unexpected event detected"

# -----------------------------
# User-level funnel construction
# -----------------------------
funnel = (
    df.assign(
        signup=lambda x: (x.event_name == "signup").astype(int),
        view=lambda x: (x.event_name == "product_view").astype(int),
        cart=lambda x: (x.event_name == "add_to_cart").astype(int),
        checkout=lambda x: (x.event_name == "checkout").astype(int),
    )
    .groupby("user_id")
    .agg(
        signup=("signup", "max"),
        view=("view", "max"),
        cart=("cart", "max"),
        checkout=("checkout", "max"),
    )
    .reset_index()
)

# -----------------------------
# Funnel summary
# -----------------------------
funnel_counts = funnel[["signup", "view", "cart", "checkout"]].sum()

signup_users = funnel_counts["signup"]
conversion_rate = funnel_counts["checkout"] / signup_users

print("\n--- FUNNEL SUMMARY ---")
print(funnel_counts)
print(f"\nCheckout conversion: {conversion_rate:.2%}")

# -----------------------------
# Drop-off stage detection
# -----------------------------
def detect_drop_stage(row):
    if row.signup == 1 and row.view == 0:
        return "signup"
    if row.view == 1 and row.cart == 0:
        return "product_view"
    if row.cart == 1 and row.checkout == 0:
        return "add_to_cart"
    return "completed"

funnel["drop_stage"] = funnel.apply(detect_drop_stage, axis=1)

# -----------------------------
# Join user attributes
# -----------------------------
user_attrs = (
    df.sort_values("event_time")
      .groupby("user_id")
      .first()[["device", "city", "event_time"]]
      .rename(columns={"event_time": "first_event_time"})
)

analysis = funnel.merge(user_attrs, on="user_id")

analysis["hour"] = pd.to_datetime(analysis.first_event_time).dt.hour
analysis["is_late_night"] = analysis.hour.between(22, 23) | analysis.hour.between(0, 4)

# -----------------------------
# Segment analysis
# -----------------------------
print("\n--- DROP-OFF BY DEVICE ---")
print(
    analysis.groupby("device")["drop_stage"]
    .value_counts(normalize=True)
    .unstack()
)

print("\n--- DROP-OFF BY LATE NIGHT ---")
print(
    analysis.groupby("is_late_night")["drop_stage"]
    .value_counts(normalize=True)
    .unstack()
)

print("\n--- DROP-OFF BY CITY ---")
print(
    analysis.groupby("city")["drop_stage"]
    .value_counts(normalize=True)
    .unstack()
)

# -----------------------------
# Key insights (printed clearly)
# -----------------------------
mobile_checkout_drop = (
    analysis.query("device == 'mobile' and drop_stage == 'add_to_cart'")
    .shape[0] / analysis.query("device == 'mobile'").shape[0]
)

desktop_checkout_drop = (
    analysis.query("device == 'desktop' and drop_stage == 'add_to_cart'")
    .shape[0] / analysis.query("device == 'desktop'").shape[0]
)

late_night_conv = (
    analysis.query("is_late_night == True and drop_stage == 'completed'")
    .shape[0] / analysis.query("is_late_night == True").shape[0]
)

day_conv = (
    analysis.query("is_late_night == False and drop_stage == 'completed'")
    .shape[0] / analysis.query("is_late_night == False").shape[0]
)

print("\n--- EXECUTIVE INSIGHTS ---")
print(f"Mobile add-to-cart drop-off: {mobile_checkout_drop:.2%}")
print(f"Desktop add-to-cart drop-off: {desktop_checkout_drop:.2%}")
print(f"Late-night conversion: {late_night_conv:.2%}")
print(f"Daytime conversion: {day_conv:.2%}")
