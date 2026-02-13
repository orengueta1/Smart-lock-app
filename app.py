import streamlit as st
import pandas as pd
from datetime import date, datetime
from data_manager import load_data, save_entry, delete_entry
from ai_parser import parse_natural_language

# Page Config
st.set_page_config(page_title="Smart-Clock AI", page_icon="🕒", layout="wide")

# Custom CSS for "Premium" & Friendly Look
st.markdown("""
    <style>
    /* Gradient Background - Softer, more colorful */
    .stApp {
        background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }
    
    /* Header Styling */
    h1 {
        background: -webkit-linear-gradient(45deg, #FF9966, #FF5E62);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 800;
        text-align: center;
        padding-bottom: 10px;
    }
    
    /* Subheaders */
    h3 {
        color: #444;
        font-weight: 600;
        border-left: 5px solid #FF5E62;
        padding-left: 10px;
        margin-top: 20px !important;
    }
    
    /* Card-like Metrics */
    div[data-testid="stMetric"] {
        background-color: white; 
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: none; /* Clean look */
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetricLabel"] {
        color: #888;
        font-size: 0.9rem;
    }
    div[data-testid="stMetricValue"] {
        color: #FF5E62;
        font-weight: 700;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stDateInput > div > div > input, .stTimeInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    
    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9966, #FF5E62);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 94, 98, 0.3);
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 94, 98, 0.5);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-weight: 600;
        color: #444;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Config
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2928/2928750.png", width=50) # Friendly Icon
st.sidebar.title("Settings")
hourly_rate = st.sidebar.number_input("Hourly Rate (₪)", value=50.0, step=0.5)
st.sidebar.info("💡 **Tip:** Default rate is ₪50/hr.")

st.title("🍊 Smart-Clock") # Friendly name change to match orange theme? Or keep Smart-Clock AI. Let's keep name but use Emoji.

# --- Onboarding Section ---
with st.expander("👋 New here? Click to learn how to use user!", expanded=True):
    st.markdown("""
    Welcome to **Smart-Clock**! Tracking your work hours has never been easier.
    
    **Two ways to log your work:**
    1.  **⚡ Quick-Log (Recommended):** Just type like you speak! 
        *   *"Worked yesterday from 9am to 5pm"*
        *   *"18/1/26 15:00-20:00"*
        *   The AI understands dates and 24h times.
    2.  **📝 Manual Entry:** Use the calendar and clocks below to pick exact times.
    
    All your data is saved automatically below. **Happy workings!** 💼
    """)

# Session State Initialization
if "form_date" not in st.session_state:
    st.session_state["form_date"] = date.today()
if "form_start" not in st.session_state:
    st.session_state["form_start"] = "09:00"
if "form_end" not in st.session_state:
    st.session_state["form_end"] = "17:00"

# --- Smart Parsing Section ---
st.write("") # Spacer
st.subheader("⚡ Quick-Log")
with st.form("ai_form"):
    text_input = st.text_area("Describe your shift (e.g., 'Worked yesterday from 9am to 6pm')", height=80)
    submitted = st.form_submit_button("Auto-Fill Form")
    
    if submitted and text_input:
        with st.spinner("Processing..."):
            # No API key needed anymore
            result = parse_natural_language(text_input)
            if "error" in result:
                st.error(result["error"])
            else:
                try:
                    # Update session state with parsed values
                    st.session_state["form_date"] = datetime.strptime(result["Date"], "%Y-%m-%d").date()
                    st.session_state["form_start"] = result["Start_Time"]
                    st.session_state["form_end"] = result["End_Time"]
                    st.success("Extracted successfully! Check the form below.")
                except Exception as e:
                    st.error(f"Error parsing response: {e}")
    # Parse response

# --- Manual Entry / Confirmation Section ---
st.subheader("📝 Shift Details")
col1, col2, col3 = st.columns(3)

with col1:
    d = st.date_input("Date", value=st.session_state["form_date"])
with col2:
    # Time input in Streamlit returns datetime.time, but we store strings/process strings often.
    # We'll use text_input for simplified 24h format or time_input. time_input is safer.
    # Parse session state strings back to time objects for the widget
    try:
        t_start_val = datetime.strptime(str(st.session_state["form_start"]), "%H:%M").time()
    except:
        t_start_val = datetime.strptime("09:00", "%H:%M").time()
        
    t_start = st.time_input("Start Time", value=t_start_val)

with col3:
    try:
        t_end_val = datetime.strptime(str(st.session_state["form_end"]), "%H:%M").time()
    except:
        t_end_val = datetime.strptime("17:00", "%H:%M").time()

    t_end = st.time_input("End Time", value=t_end_val)

if st.button("💾 Save Entry", type="primary"):
    # Convert back to string for backend consistency
    s_str = t_start.strftime("%H:%M")
    e_str = t_end.strftime("%H:%M")
    d_str = d.strftime("%Y-%m-%d")
    
    success, msg = save_entry(d_str, s_str, e_str, hourly_rate)
    if success:
        st.success(msg)
        # Optional: Clear form or keep it
    else:
        st.error(msg)

# --- Dashboard & Data ---
st.markdown("---")
st.subheader("📊 Attendance Log")

df = load_data()

if not df.empty:
    # Metrics
    total_hours = df["Hours"].sum()
    total_earnings = df["Earnings"].sum()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Shifts", len(df))
    m2.metric("Total Hours", f"{total_hours:.1f}")
    m3.metric("Total Earnings", f"₪{total_earnings:,.2f}")

    # Data Table with Delete support
    # Streamlit data_editor is editable, but simple table + delete button is easier for now
    # We'll show the table and a delete widget below
    st.dataframe(df, use_container_width=True)
    
    with st.expander("Delete an Entry"):
        entry_to_delete = st.number_input("Index to delete", min_value=0, max_value=len(df)-1 if len(df)>0 else 0, step=1)
        if st.button("Delete Entry"):
            success, msg = delete_entry(entry_to_delete)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
else:
    st.info("No shifts recorded yet.")
