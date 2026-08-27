import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Pencari Data Barang", page_icon="🔍", layout="centered")

st.title("🔍 Alat Web Pencari data Excel")
st.write("Unggah file Excel Anda, lalu cari nama datanya menggunakan pencarian pintar.")

# 1. Fitur Upload File Excel
uploaded_file = st.file_uploader("Upload File Excel Anda (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # Membaca data dari file yang di-upload
    df = pd.read_excel(uploaded_file).fillna("-")
    
    st.subheader("📋 Preview Data Excel")
    st.dataframe(df.head()) # Menampilkan 5 baris pertama

    # Memastikan file Excel memiliki kolom 'Nama Barang'
    if 'Nama Barang' in df.columns:
        daftar_barang = df['Nama Barang'].astype(str).tolist()
        
        # 2. Kolom Input Pencarian Teks
        tanya = st.text_input("Ketik nama barang yang dicari:", placeholder="Contoh: semen gresik")
        
        if tanya:
            # Mengabaikan kata basa-basi
            kata_abaikan = ["cek", "harga", "stok", "ada", "gak", "dong", "bro", "berapa", "tolong"]
            kata_kunci = [k for k in tanya.lower().split() if k not in kata_abaikan]
            frasa_cari = " ".join(kata_kunci)
            
            # Pencarian Pintar dengan RapidFuzz
            hasil = process.extractOne(frasa_cari, daftar_barang, scorer=fuzz.partial_ratio)
            
            if hasil and hasil[1] >= 50:
                nama_ditemukan = hasil[0]
                skor = hasil[1]
                
                # Mengambil data baris barang yang paling cocok
                row = df[df['Nama Barang'].astype(str) == nama_ditemukan].iloc[0]
                
                st.markdown("---")
                st.success(f"Ditemukan: **{nama_ditemukan}** (Tingkat Kemiripan: {skor:.0f}%)")
                
                # Menampilkan Informasi dalam Bentuk Kartu (Metrics)
                col1, col2 = st.columns(2)
                col1.metric("Harga", f"Rp {row.get('Harga (Rp)', 0):,.0f}")
                col2.metric("Stok Tersedia", f"{row.get('Stok', '-')} {row.get('Satuan', '')}")
            else:
                st.warning("Barang tidak ditemukan. Coba gunakan kata kunci lain.")
    else:
        st.error("⚠️ File Excel harus memiliki header kolom bernama **'Nama Barang'**.")
