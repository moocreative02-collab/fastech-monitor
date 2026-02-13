import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Page Configuration
st.set_page_config(page_title="Fastech | Elite Dashboard", layout="wide", page_icon="🏗️")

# 2. CSS Elite Dark Mode (Ultra Premium)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    /* Background Utama Hitam Pekat */
    .stApp {
        background-color: #0e1117 !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Sembunyikan Header/Footer Default Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar Dark Mode */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #333;
    }
    /* Memastikan semua teks di sidebar putih */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #ffffff !important;
    }

    /* Header Premium Dark Gradient */
    .premium-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 50px;
        border-radius: 20px;
        margin-bottom: 30px;
        color: white !important;
        border: 1px solid #FF6B00;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        position: relative; /* Untuk positioning jika perlu */
    }
    .premium-header h1 { 
        color: #FF6B00 !important; 
        font-weight: 800; 
        margin: 0; 
        font-size: 2.8rem; 
        letter-spacing: -1px;
        text-shadow: 2px 2px 10px rgba(255, 107, 0, 0.3);
    }
    .premium-header p { 
        color: #d1d1d1 !important; 
        font-size: 1.1rem; 
        margin-top: 10px; 
        opacity: 0.9;
    }

    /* Metric Cards - Dark Glassmorphism */
    div[data-testid="stMetric"] {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        padding: 25px !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    div[data-testid="stMetric"] label { color: #aaaaaa !important; font-weight: 600 !important; }
    div[data-testid="stMetric"] div { color: #FF6B00 !important; font-weight: 800 !important; }

    /* Jam Real-time Neon */
    .clock-widget {
        background: #000000;
        padding: 12px 30px;
        border-radius: 50px;
        color: #FF6B00 !important;
        font-weight: 800;
        display: inline-block;
        border: 1px solid #FF6B00;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(255, 107, 0, 0.4);
    }

    /* Tombol Neon Orange */
    .stButton>button {
        background-color: transparent !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(255, 107, 0, 0.6);
    }

    /* Tab Styling Dark */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        color: #888;
        border-radius: 10px 10px 0 0;
        padding: 12px 25px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF6B00 !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Widget Jam Real-time (Neon JavaScript)
st.markdown("""
    <div style="text-align: right;">
        <div id="neon-clock" class="clock-widget">🕒 Sinkronisasi...</div>
    </div>
    <script>
    function updateClock() {
        const now = new Date();
        const options = { 
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false 
        };
        document.getElementById('neon-clock').innerHTML = '🕒 ' + new Intl.DateTimeFormat('id-ID', options).format(now);
    }
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """, unsafe_allow_html=True)

# 4. Data Core
DB_FILE = "fastech_elite_db.csv"
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Proyek", "Deskripsi", "PIC", "Deadline", "Status", "Input_At"])

# --- SIDEBAR BRANDING (LOGO) ---
with st.sidebar:
    # Mengecek apakah file logo.png ada di GitHub
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        # Placeholder jika logo belum diupload
        st.header("🏗️ FASTECH")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("**Sistem Kontrol Operasional**")
    st.caption("Tim Creative & Engineering")

# --- MAIN HEADER ---
st.markdown("""
    <div class="premium-header">
        <h1>Fastech Architect | Dashboard Monitoring</h1>
        <p>TIM CREATIVE • DARK MODE ELITE OPERATIONAL CONTROL</p>
    </div>
    """, unsafe_allow_html=True)

# --- PANEL INPUT (Hidden in Expander) ---
with st.expander("➕ DAFTARKAN PEKERJAAN BARU (KLIK DISINI)", expanded=False):
    with st.form("elite_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Nama Proyek")
            # List PIC sesuai permintaan
            pic = st.selectbox("Assign PIC", ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"])
        with c2:
            limit = st.date_input("Deadline")
            short_desc = st.text_input("Ringkasan Tugas")
        
        detail = st.text_area("Detail Instruksi Lengkap")
        
        if st.form_submit_button("LOCK DATA KE DATABASE"):
            if name and short_desc:
                new_data = pd.DataFrame([[name, f"{short_desc} - {detail}", pic, str(limit), "To Do", datetime.now().strftime("%d/%m/%Y %H:%M")]],
                                        columns=["Proyek", "Deskripsi", "PIC", "Deadline", "Status", "Input_At"])
                df = load_db()
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success("Data Terkunci di Sistem!")
                st.rerun()

# --- STATISTICS ---
df = load_db()
col1, col2, col3 = st.columns(3)
col1.metric("TOTAL PROJECT", len(df))
col2.metric("ACTIVE TASKS", len(df[df['Status'] != "Done"]))
col3.metric("COMPLETED", len(df[df['Status'] == "Done"]))

st.markdown("<br>", unsafe_allow_html=True)

# --- TASK DISPLAY ---
tab_active, tab_history = st.tabs(["⚡ MONITORING AKTIF", "📂 ARSIP SELESAI"])

with tab_active:
    ongoing = df[df['Status'] != "Done"]
    if not ongoing.empty:
        for i, row in ongoing.iterrows():
            st.markdown(f"""
            <div style="background: #1a1a1a; padding: 25px; border: 1px solid #333; border-radius: 15px; margin-bottom: 20px; border-left: 8px solid #FF6B00; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                <h3 style="margin:0; color:#FF6B00; font-size: 1.4rem;">{row['Proyek']}</h3>
                <p style="color:#aaaaaa; font-weight: bold; margin-bottom: 15px; font-size: 0.9rem;">PIC: {row['PIC']} | Target: {row['Deadline']}</p>
                <div style="color:#e0e0e0; font-size:1rem; border-top: 1px solid #333; padding-top:15px; line-height: 1.5;">{row['Deskripsi']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Update & Action
            ca, cb = st.columns([4, 1])
            new_st = ca.select_slider("UPDATE PROGRES", options=["To Do", "In Progress", "Done"], value=row['Status'], key=f"s_{i}")
            if cb.button("HAPUS", key=f"d_{i}"):
                df = df.drop(i)
                df.to_csv(DB_FILE, index=False)
                st.rerun()
            
            if new_st != row['Status']:
                df.at[i, 'Status'] = new_st
                df.to_csv(DB_FILE, index=False)
                st.rerun()
    else:
        st.info("Tidak ada tugas aktif. Sistem standby.")

with tab_history:
    done = df[df['Status'] == "Done"]
    if not done.empty:
        st.table(done[["Proyek", "PIC", "Deadline", "Input_At"]])
    else:
        st.caption("Arsip pekerjaan selesai masih kosong.")
