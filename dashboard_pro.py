import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Analitik Pro",
    page_icon="📊",
    layout="wide"
)

# --- JUDUL & SIDEBAR ---
st.title("📊 Dashboard Analisis Data Otomatis")
st.markdown("---")

st.sidebar.header("📂 Panel Kontrol")
st.sidebar.info("Upload file Excel/CSV kamu di sini:")

uploaded_file = st.sidebar.file_uploader("Upload File:", type=["csv", "xlsx"])

# --- LOGIKA UTAMA ---
if uploaded_file is not None:
    try:
        # 1. BACA FILE
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.sidebar.success("✅ File berhasil dibaca!")
        
        # 2. DATA PREVIEW
        with st.expander("Lihat Tabel Data Asli"):
            st.dataframe(df)
            
        # 3. RINGKASAN
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Baris", df.shape[0])
        col2.metric("Total Kolom", df.shape[1])
        
        # Cari kolom angka
        angka_cols = df.select_dtypes(include=['float', 'int', 'int64']).columns
        if len(angka_cols) > 0:
            col3.metric(f"Total {angka_cols[0]}", f"{df[angka_cols[0]].sum():,.0f}")

        st.markdown("---")

        # 4. VISUALISASI GRAFIK (BAGIAN YANG DIPERBAIKI)
        st.subheader("📈 Visualisasi Grafik")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            x_axis = st.selectbox("Sumbu X (Bawah)", df.columns)
        with c2:
            y_axis = st.selectbox("Sumbu Y (Kiri)", angka_cols)
        with c3:
            tipe = st.selectbox("Jenis Grafik", ["Bar Chart", "Line Chart", "Area Chart"])

        # --- JURUS ANTI-ERROR ---
        # Kita buat tabel kecil khusus grafik, biar tabel aslinya gak rusak
        chart_data = df[[x_axis, y_axis]].copy()
        
        # Kita set Sumbu X jadi Index, tapi pakai cara aman
        chart_data = chart_data.set_index(x_axis)

        # Tampilkan
        st.write(f"Grafik: **{y_axis}** per **{x_axis}**")
        
        if tipe == "Bar Chart":
            st.bar_chart(chart_data)
        elif tipe == "Line Chart":
            st.line_chart(chart_data)
        elif tipe == "Area Chart":
            st.area_chart(chart_data)
            
    except Exception as e:
        st.error(f"Terjadi Kesalahan: {e}")
        st.warning("Tips: Pastikan kamu memilih kolom Angka untuk Sumbu Y.")

else:
    st.info("👋 Silakan upload file Excel/CSV di menu sebelah kiri.")
    
    # Data Palsu buat Demo (Biar user tau bentuknya)
    demo_df = pd.DataFrame({
        'Bulan': ['Jan', 'Feb', 'Mar', 'Apr'],
        'Terjual': [100, 150, 120, 200]
    })
    st.write("Contoh tampilan nanti:")
    st.bar_chart(demo_df.set_index('Bulan'))