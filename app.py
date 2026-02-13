import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# 1. Konfigurasi Dasar
st.set_page_config(page_title="FASTECH | Executive Dashboard", layout="wide", page_icon="🏗️")

# 2. Custom CSS (Premium UI Look)
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Header */
    .header-container {
        background: linear-gradient(90deg, #002b5b 0%, #004a99 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
    }

    /* Stat Cards */
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #eee;
    }
    
    /* Real-time Clock Styling */
    .clock-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ffd700;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Real-time Clock (JavaScript Injection)
st.markdown("""
    <div id="clock-container" style="text-align: right; padding-right: 20px;">
        <span id="clock" class="clock-text"></span>
    </div>
    <script>
    function updateClock() {
        var now = new Date();
        var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        document.getElementById('clock').innerHTML = now.toLocaleDateString('id-ID', options);
    }
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """, unsafe_allow_html=True)

# 4. Database Logic
DATA_FILE = "tasks_fastech_v2.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])

# --- HEADER SECTION ---
with st.container():
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=150)
        else:
            st.title("🏗️")
    with col_title:
        st.markdown("<div class='header-container'><h1>TIM CREATIVE FASTECH ARCHITECT</h1><p>Sistem Monitoring Proyek & Automasi Arsitektur</p></div>", unsafe_allow_html=True)

# --- SIDEBAR: Input ---
with st.sidebar:
    st.header("📌 Input Pekerjaan")
    with st.form("main_form", clear_on_submit=True):
        project = st.text_input("Nama Proyek", placeholder="e.g. Villa Sentul - Rev 01")
        task = st.text_area("Deskripsi Brief")
        
        # Daftar PIC sesuai permintaan Anda
        pic = st.selectbox("PIC Bertanggung Jawab", ["Tim CS", "PIC / Owner", "Tim Drafter", "Other"])
        
        deadline = st.date_input("Target Selesai")
        if st.form_submit_button("Submit ke Antrean"):
            if project and task:
                new_row = pd.DataFrame([[project, task, pic, str(deadline), "To Do", datetime.now().strftime("%Y-%m-%d %H:%M")]], 
                                        columns=["Project", "Task", "Pic", "Deadline", "Status", "Timestamp"])
                df = load_data()
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("Tugas Berhasil Terdaftar!")
                st.rerun()

# --- MAIN CONTENT ---
df = load_data()

# Quick Stats Overview
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Project", len(df))
c2.metric("Pending", len(df[df['Status'] == "To Do"]))
c3.metric("On Progress", len(df[df['Status'] == "In Progress"]))
c4.metric("Done", len(df[df['Status'] == "Done"]))

st.divider()

# Tabs for Organization
tab_active, tab_history = st.tabs(["🚀 Pekerjaan Aktif", "📜 Riwayat Selesai"])

with tab_active:
    active_df = df[df['Status'] != "Done"]
    if not active_df.empty:
        for idx, row in active_df.iterrows():
            with st.expander(f"📌 {row['Project']} | {row['Pic']} (Deadline: {row['Deadline']})"):
                st.write(f"**Brief:** {row['Task']}")
                st.caption(f"Dibuat pada: {row['Timestamp']}")
                
                ca, cb, cc = st.columns([2, 1, 1])
                new_status = ca.selectbox("Update Progress", ["To Do", "In Progress", "Done"], 
                                         index=["To Do", "In Progress", "Done"].index(row['Status']), 
                                         key=f"upd_{idx}")
                
                if new_status != row['Status']:
                    full_df = load_data()
                    full_df.at[idx, 'Status'] = new_status
                    full_df.to_csv(DATA_FILE, index=False)
                    st.rerun()
                
                if cc.button("🗑️ Hapus", key=f"del_{idx}"):
                    full_df = load_data()
                    full_df = full_df.drop(idx)
                    full_df.to_csv(DATA_FILE, index=False)
                    st.rerun()
    else:
        st.info("Tidak ada pekerjaan aktif saat ini. Tim bisa istirahat sejenak! ☕")

with tab_history:
    done_df = df[df['Status'] == "Done"]
    if not done_df.empty:
        st.table(done_df[["Project", "Pic", "Deadline", "Timestamp"]])
    else:
        st.write("Belum ada riwayat pekerjaan selesai.")
