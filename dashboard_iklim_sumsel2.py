import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# BACA DATA
# =====================
data = pd.read_excel("Data_Tahunan_SUMSEL.xlsx")

# Rename agar lebih mudah
data = data.rename(columns={
    "Tavg": "Suhu",
    "curah_hujan": "Curah_Hujan",
    "Tx": "Suhu_Max",
    "Tn": "Suhu_Min"
})

# =====================
# HEADER
# =====================
st.title("🌦️ Dashboard Analisis Iklim Sumatera Selatan")
st.markdown("Visualisasi data iklim tahunan berdasarkan parameter suhu, hujan, kelembaban, angin, dan radiasi matahari.")

# =====================
# TABEL DATA
# =====================
st.subheader("📄 Data Iklim")
st.dataframe(data)

# =====================
# SUHU
# =====================
st.subheader("🌡️ Tren Suhu Rata-rata Tahunan")
st.line_chart(data.set_index("Tahun")["Suhu"])

# =====================
# CURAH HUJAN
# =====================
st.subheader("🌧️ Curah Hujan Tahunan")
st.bar_chart(data.set_index("Tahun")["Curah_Hujan"])

# =====================
# RENTANG SUHU
# =====================
st.subheader("📉 Rentang Suhu Tahunan (Max - Min)")
data["Rentang_Suhu"] = data["Suhu_Max"] - data["Suhu_Min"]
st.line_chart(data.set_index("Tahun")["Rentang_Suhu"])

# =====================
# ANOMALI SUHU
# =====================
st.subheader("📈 Anomali Suhu terhadap Rata-rata 1981–2010")
baseline = data[(data["Tahun"] >= 1981) & (data["Tahun"] <= 2010)]["Suhu"].mean()
data["Anomali_Suhu"] = data["Suhu"] - baseline

fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.barplot(x="Tahun", y="Anomali_Suhu", data=data, palette="coolwarm", ax=ax1)
ax1.axhline(0, color="black", linestyle="--")
ax1.set_ylabel("Anomali (°C)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# =====================
# KORELASI SUHU - HUJAN
# =====================
st.subheader("🔍 Korelasi Suhu vs Curah Hujan")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=data, x="Suhu", y="Curah_Hujan", ax=ax2)
sns.regplot(data=data, x="Suhu", y="Curah_Hujan", scatter=False, ax=ax2, color="red")
st.pyplot(fig2)

# =====================
# RATA-RATA PER DEKADE
# =====================
st.subheader("📊 Rata-rata Suhu & Curah Hujan per Dekade")
data["Dekade"] = (data["Tahun"] // 10) * 10
avg_dekade = data.groupby("Dekade")[["Suhu", "Curah_Hujan"]].mean().round(2)
st.dataframe(avg_dekade)

fig3, ax3 = plt.subplots()
avg_dekade.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Rata-rata")
st.pyplot(fig3)

# =====================
# TAHUN EKSTREM
# =====================
st.subheader("📌 Tahun Ekstrem")
st.markdown(f"""
- 🌡️ **Tahun Terpanas**: {data.loc[data['Suhu'].idxmax()]['Tahun']} ({data['Suhu'].max():.2f} °C)  
- ❄️ **Tahun Terdingin**: {data.loc[data['Suhu'].idxmin()]['Tahun']} ({data['Suhu'].min():.2f} °C)  
- 🌧️ **Hujan Terbanyak**: {data.loc[data['Curah_Hujan'].idxmax()]['Tahun']} ({data['Curah_Hujan'].max():.1f} mm)  
- ☀️ **Hujan Terkering**: {data.loc[data['Curah_Hujan'].idxmin()]['Tahun']} ({data['Curah_Hujan'].min():.1f} mm)
""")

# =====================
# HISTOGRAM KELEMBABAN
# =====================
st.subheader("💧 Distribusi Kelembaban Tahunan")
fig4, ax4 = plt.subplots()
sns.histplot(data["kelembaban"], kde=True, bins=20, color="skyblue", ax=ax4)
ax4.set_xlabel("Kelembaban (%)")
st.pyplot(fig4)

# =====================
# TREN KELEMBABAN
# =====================
st.subheader("💨 Kelembaban Tahunan")
st.line_chart(data.set_index("Tahun")["kelembaban"])

# =====================
# TREN MATAHARI
# =====================
if "matahari" in data.columns:
    st.subheader("🌞 Durasi Penyinaran Matahari")
    st.line_chart(data.set_index("Tahun")["matahari"])

# =====================
# TREN KECEPATAN ANGIN
# =====================
if "kecepatan_angin" in data.columns:
    st.subheader("🍃 Kecepatan Angin Tahunan")
    st.line_chart(data.set_index("Tahun")["kecepatan_angin"])

# =====================
# MATRIX KORELASI
# =====================
st.subheader("📌 Korelasi Antar Variabel Iklim")
fig5, ax5 = plt.subplots(figsize=(8, 6))
sns.heatmap(data.select_dtypes(include='number').corr(), annot=True, cmap="coolwarm", ax=ax5)
st.pyplot(fig5)
