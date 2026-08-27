import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz
import io

st.set_page_config(page_title="Pencari Data Excel", page_icon="🔍", layout="centered")

st.title("🔍 Web Tool Pencari Data Excel")
st.write("Unggah file Excel Anda, pilih kolomnya, lalu cari datanya dengan mudah.")

# 1. Upload File Excel
uploaded_file = st.file_uploader("Upload File Excel Anda (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file).fillna("-")
    
    st.subheader("📋 Preview Data Excel")
    st.dataframe(df.head())

    # 2. Pengguna Memilih Kolom yang Ingin Dicari
    semua_kolom = df.columns.tolist()
    kolom_terpilih = st.selectbox("Pilih Kolom yang Ingin Dicari:", semua_kolom)

    if kolom_terpilih:
        daftar_data = df[kolom_terpilih].astype(str).tolist()
        tanya = st.text_input(f"Ketik kata kunci untuk mencari di kolom '{kolom_terpilih}':")
        
        if tanya:
            # Pencarian Fuzzy
            hasil = process.extractOne(tanya, daftar_data, scorer=fuzz.partial_ratio)
            
            if hasil and hasil[1] >= 50:
                data_ditemukan = hasil[0]
                skor = hasil[1]
                
                # Ambil baris data yang cocok
                row = df[df[kolom_terpilih].astype(str) == data_ditemukan].iloc[0]
                
                st.markdown("---")
                st.success(f"Ditemukan: **{data_ditemukan}** (Tingkat Kemiripan: {skor:.0f}%)")
                
                # Tampilkan detail data dalam tabel
                st.subheader("📄 Detail Informasi Lengkap:")
                df_detail = pd.DataFrame([row])
                st.dataframe(df_detail)
                
                # --- FITUR TOMBOL DOWNLOAD HASIL PENCARIAN ---
                st.subheader("📥 Download Hasil")
                
                # Konversi hasil pencarian ke format Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_detail.to_excel(writer, index=False, sheet_name='Hasil_Pencarian')
                data_excel = buffer.getvalue()
                
                # Tombol Download Excel
                st.download_button(
                    label="📊 Download Hasil Ini (.xlsx)",
                    data=data_excel,
                    file_name=f"hasil_pencarian_{data_ditemukan}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            else:
                st.warning("Data tidak ditemukan. Coba ketik kata kunci lain.")
