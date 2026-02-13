import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Page Configuration
st.set_page_config(page_title="Fastech | Elite Dashboard", layout="wide", page_icon="🏗️")

# 2. CSS Elite Dark Mode + Point Box Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    .stApp {
        background-color: #0e1117 !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Premium Dark Header */
    .premium-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 50px;
        border-radius: 20px;
        margin-bottom: 30px;
        border: 1px solid #FF6B00;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    .premium-header h1 { 
        color: #FF6B00 !important; 
        font-weight: 800; 
        font-size: 2.8rem; 
        text-shadow: 2px 2px 10px rgba(255, 107, 0, 0.3);
        margin: 0;
    }

    /* Task Point Box Styling */
    .point-box {
        background: rgba(255, 107, 0, 0.05);
        border: 1px solid rgba(255, 107, 0, 0.3);
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        transition: 0.3s;
    }
    .point-box:hover {
        border-color: #FF6B00;
        background: rgba(255, 107, 0, 0.1);
        box-shadow: 0 0 10px rgba(255, 107, 0, 0.2);
    }
    .point-icon {
        color: #FF6B00;
        margin-right: 12px;
        font-weight: bold;
    }

    /* Sidebar & Metrics Customization */
    section[data-testid="stSidebar"] { background-color: #000000 !important; }
    div[data-testid="stMetric"] {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 18px !important;
    }

    /* Clock Styling */
    .clock-widget {
        background: #000000;
        padding: 12px 30px;
        border-radius: 50px;
        color: #FF6B00 !important;
        font-weight: 800;
        border: 1px solid #FF6B00;
        box-shadow: 0 0 15px rgba(255, 107, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Real-time Clock (Neon JavaScript)
st.markdown("""
    <div style="text-align: right;">
        <div id="pro-clock" class="clock-widget">🕒 Sinkronisasi...</div>
    </div>
    <script>
    function updateClock() {
        const now = new Date();
        const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
        document.getElementById('pro-clock').innerHTML = '🕒 ' + new Intl.DateTimeFormat('id-ID', options).format(now);
    }
    setInterval(updateClock, 1000); updateClock();
    </script>
    """, unsafe_allow_html=True)

# 4. Data Core
DB_FILE = "fastech_pro_tasks.csv"
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Proyek", "Poin_Tugas", "PIC", "Deadline", "Status", "Input_At"])

# --- SIDEBAR BRANDING ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown("---")
    st.write("**Fastech Architect**")
    st.caption("Creative Engineering Control")

# --- MAIN HEADER ---
st.markdown("""
    <div class="premium-header">
        <h1>Fastech Architect | Dashboard Monitoring</h1>
        <p>TIM CREATIVE • ADVANCED TASK MANAGEMENT SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL INPUT (Point-Based Input) ---
with st.expander("➕ DAFTARKAN PEKERJAAN DENGAN POIN-POIN", expanded=False):
    with st.form("pro_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Nama Proyek")
            # PIC List
            pic = st.selectbox("Assign PIC", ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"])
        with c2:
            limit = st.date_input("Deadline")
            # Help text untuk banyak poin
            st.caption("Tips: Gunakan Enter (baris baru) untuk memisahkan setiap poin pekerjaan.")
        
        # Area input besar untuk banyak poin sekaligus
        points_input = st.text_area("Detail Pekerjaan (Tulis per poin, satu baris satu poin)", 
                                  height=200,
                                  placeholder="Contoh:\nRevisi tampak depan bangunan\nGanti material lantai ke marmer\nTambahkan lampu taman neon orange")
        
        if st.form_submit_button("LOCK DATA KE DATABASE"):
            if name and points_input:
                new_data = pd.DataFrame([[name, points_input, pic, str(limit), "To Do", datetime.now().strftime("%d/%m/%Y %H:%M")]],
                                        columns=["Proyek", "Poin_Tugas", "PIC", "Deadline", "Status", "Input_At"])
                df = load_db()
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success("Tugas Berhasil Terkunci!")
                st.rerun()

# --- STATISTICS ---
df = load_db()
col1, col2, col3 = st.columns(3)
col1.metric("TOTAL PROJECT", len(df))
col2.metric("ACTIVE TASKS", len(df[df['Status'] != "Done"]))
col3.metric("COMPLETED", len(df[df['Status'] == "Done"]))

st.markdown("<br>", unsafe_allow_html=True)

# --- TASK DISPLAY ---
tab_active, tab_history = st.tabs(["⚡ MONITORING POIN PEKERJAAN", "📂 ARSIP SELESAI"])

with tab_active:
    ongoing = df[df['Status'] != "Done"]
    if not ongoing.empty:
        for i, row in ongoing.iterrows():
            st.markdown(f"""
            <div style="background: #1a1a1a; padding: 25px; border: 1px solid #333; border-radius: 15px; margin-bottom: 20px; border-left: 8px solid #FF6B00;">
                <h3 style="margin:0; color:#FF6B00; font-size: 1.5rem;">{row['Proyek']}</h3>
                <p style="color:#888; margin-bottom: 20px;">PIC: {row['PIC']} | Target: {row['Deadline']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Rendering Poin-Poin Pekerjaan sebagai Box
            raw_points = str(row['Poin_Tugas']).split('\n')
            for point in raw_points:
                if point.strip(): # Hanya tampilkan jika tidak kosong
                    st.markdown(f"""
                    <div class="point-box">
                        <span class="point-icon">🔸</span>
                        <span style="color: #e0e0e0;">{point.strip()}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Control Actions
            ca, cb = st.columns([4, 1])
            new_st = ca.select_slider("UPDATE PROGRES", options=["To Do", "In Progress", "Done"], value=row['Status'], key=f"s_{i}")
            if cb.button("HAPUS PROJECT", key=f"d_{i}"):
                df = df.drop(i)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
            
            if new_st != row['Status']:
                df.at[i, 'Status'] = new_st
                df.to_csv(DB_FILE, index=False)
                st.rerun()
            st.markdown("---")
    else:
        st.info("Zero tasks active. System standby.")

with tab_history:
    done = df[df['Status'] == "Done"]
    if not done.empty:
        st.table(done[["Proyek", "PIC", "Deadline", "Input_At"]])
