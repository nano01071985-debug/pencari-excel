import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

st.set_page_config(page_title="Pencari Data Excel", page_icon="🔍", layout="centered")

st.title("🔍 Web Tool Pencari Data Excel")
st.write("Unggah file Excel Anda, lalu ketik kata kunci yang ingin dicari.")

uploaded_file = st.file_uploader("Upload File Excel Anda (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # Read Excel & hapus baris yang cuma berisi strip '-' atau kosong
    df = pd.read_excel(uploaded_file).fillna("")
    
    st.subheader("📋 Preview Data Excel")
    st.dataframe(df.head())

    tanya = st.text_input("Ketik kata kunci (Nama, Wilayah, dll):")

    if tanya:
        # Gabungkan semua data dalam satu baris menjadi satu teks panjang untuk pencarian global
        df['gabungan_teks'] = df.astype(str).values.tolist()
        df['gabungan_teks'] = df['gabungan_teks'].apply(lambda x: " ".join(x))
        
        daftar_teks = df['gabungan_teks'].tolist()
        
        # Cari dengan RapidFuzz
        hasil = process.extractOne(tanya, daftar_teks, scorer=fuzz.partial_ratio)
        
        if hasil and hasil[1] >= 40: # Ambang batas kemiripan
            idx_ditemukan = hasil[2]
            row_ditemukan = df.iloc[idx_ditemukan].drop('gabungan_teks')
            
            st.markdown("---")
            st.success(f"Ditemukan Data yang Cocok! (Kemiripan: {hasil[1]:.0f}%)")
            
            # Tampilkan detail baris yang cocok
            st.subheader("📄 Detail Informasi:")
            df_detail = pd.DataFrame(row_ditemukan).T
            st.dataframe(df_detail)
        else:
            st.warning("Data tidak ditemukan. Coba ketik kata kunci lain.")
