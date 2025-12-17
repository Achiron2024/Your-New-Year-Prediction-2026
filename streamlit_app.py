import streamlit as st
import pandas as pd
import hashlib
import os
from datetime import datetime

# --- CONFIGURATION & LOGGING ---
LOG_FILE = "predictions_log.csv"

def load_log():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    return pd.DataFrame(columns=["timestamp", "user_name", "dob", "beer_score", "western", "chinese"])

def save_prediction(data):
    df = load_log()
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
    return len(df)

# --- LOGIC FUNCTIONS (Stable from your original code) ---
def stable_index(key: str, n: int) -> int:
    h = int(hashlib.sha256(key.encode("utf-8")).hexdigest(), 16)
    return h % n

def get_western_zodiac(dob):
    m, d = dob.month, dob.day
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini"
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo"
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio"
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius"
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius"
    else: return "Pisces"

def get_chinese_zodiac(year):
    animals = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Boar"]
    return animals[(year - 2020) % 12]

def build_predictions(dob_str, beer_score):
    # (Templates truncated for brevity - keep your full lists from the original code here)
    success_templates = ["2026 will open new doors. Enjoy the rise, like a cold {beer}."] 
    love_templates = ["Love will feel warm in 2026, soft like bubbles in a {beer}."]
    beers = ["Asahi Super Dry", "Sapporo Classic", "Guinness", "Heineken", "Corona"]

    key_base = f"{dob_str}_{beer_score}"
    idx_s_b = stable_index(key_base + "_beer_success", len(beers))
    idx_l_b = (idx_s_b + 1) % len(beers)
    
    idx_s = stable_index(key_base + "_success", len(success_templates))
    idx_l = stable_index(key_base + "_love", len(love_templates))

    return success_templates[idx_s].format(beer=beers[idx_s_b]), love_templates[idx_l].format(beer=beers[idx_l_b])

# --- STREAMLIT UI ---
st.set_page_config(page_title="Beer Horoscope 2026", page_icon="🍺")

st.title("🍺 Beer Horoscope 2026")
st.write("Find out what 2026 holds for your love life and success!")

with st.form("horoscope_form"):
    name = st.text_input("Your Name")
    dob = st.date_input("Date of Birth", min_value=datetime(1940, 1, 1), max_value=datetime(2025, 1, 1), format="DD/MM/YYYY")
    beer_score = st.slider("How much do you like beer? (1-5)", 1, 5, 3)
    submitted = st.form_submit_button("Get my Prediction")

if submitted and name:
    dob_str = dob.strftime("%Y-%m-%d")
    western = get_western_zodiac(dob)
    chinese = get_chinese_zodiac(dob.year)
    success, love = build_predictions(dob_str, beer_score)
    
    # Save and get count
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user_name": name, "dob": dob_str, "beer_score": beer_score,
        "western": western, "chinese": chinese
    }
    total_users = save_prediction(log_data)

    # Display Results
    st.success(f"Cheers, {name}! Here is your 2026 outlook:")
    
    dob_formatted = dob.strftime("%d/%m/%Y")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Date of Birth", dob_formatted)
    col2.metric("Western Sign", western)
    col3.metric("Chinese Sign", chinese)
    col4.metric("Beer Score", beer_score)
    
    st.subheader("🚀 Success in 2026")
    st.info(success)
    
    st.subheader("❤️ Love in 2026")
    st.warning(love)
    
    st.divider()
    st.write(f"📊 You are the **{total_users}th** person to check their beer destiny!")

elif submitted and not name:
    st.error("Please enter your name!")

# --- ADMIN VIEW (Optional) ---
if st.checkbox("Show recent activity (Admin)"):
    st.dataframe(load_log().tail(10))