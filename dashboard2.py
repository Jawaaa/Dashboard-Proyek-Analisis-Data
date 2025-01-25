import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from io import StringIO

# STEP 1: Persiapkan DataFrame
st.title("Dashboard Sewa Sepeda")
st.sidebar.header("Filter")

# Load datasets
day_df = pd.read_csv("https://raw.githubusercontent.com/Jawaaa/Dataset-Proyek-Data-Scient/refs/heads/main/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/Jawaaa/Dataset-Proyek-Data-Scient/refs/heads/main/hour.csv")

# Cleaning Data
# Menghapus duplikasi
hour_df.drop_duplicates(inplace=True)
day_df.drop_duplicates(inplace=True)

# Memastikan tidak ada nilai duplikat atau missing value setelah pembersihan
assert hour_df.duplicated().sum() == 0, "Hourly data masih memiliki duplikasi"
assert day_df.duplicated().sum() == 0, "Daily data masih memiliki duplikasi"
assert hour_df.isna().sum().sum() == 0, "Hourly data masih memiliki missing value"
assert day_df.isna().sum().sum() == 0, "Daily data masih memiliki missing value"

# Memperbaiki tipe data
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# Menambahkan kolom bulan pada daily data
day_df["month"] = day_df["dteday"].dt.month

# STEP 2: Filter Sidebar
year_filter = st.sidebar.selectbox("Pilih Tahun", options=[0, 1], format_func=lambda x: "2011" if x == 0 else "2012")
season_filter = st.sidebar.multiselect("Pilih Musim", options=[1, 2, 3, 4], format_func=lambda x: ["Spring", "Summer", "Fall", "Winter"][x - 1])

# Filter data berdasarkan pilihan pengguna
filtered_data = day_df[(day_df["yr"] == year_filter)]
if season_filter:
    filtered_data = filtered_data[filtered_data["season"].isin(season_filter)]

# STEP 3: Visualisasi 1 - Pola Penyewaan Sepeda Bulanan
monthly_data = filtered_data.groupby(["month", "yr"]).agg({"casual": "mean", "registered": "mean"}).reset_index()

st.subheader("Pola Perubahan Penyewaan Sepeda Bulanan")
fig, ax = plt.subplots(figsize=(12, 7))

# Plot pengguna casual
sns.lineplot(
    x="month", 
    y="casual", 
    data=monthly_data, 
    marker="o", 
    label=f"Casual {2011 + year_filter}", 
    color="red", 
    ax=ax
)

# Plot pengguna registered
sns.lineplot(
    x="month", 
    y="registered", 
    data=monthly_data, 
    marker="o", 
    label=f"Registered {2011 + year_filter}", 
    color="blue", 
    ax=ax
)

# Detil pada plot
ax.set_title(f"Pola Perubahan Penyewaan Sepeda Bulanan\n(Casual vs Registered, Tahun {2011 + year_filter})", fontsize=14)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.set_xticks(np.arange(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.legend(title="Kategori Pengguna dan Tahun")
ax.grid(alpha=0.3)

st.pyplot(fig)

# STEP 4: Visualisasi 2 - Rata-rata Penyewaan Sepeda Berdasarkan Musim
season_avg = filtered_data.groupby("season").agg({"cnt": "mean"}).reset_index()
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_avg["season"] = season_avg["season"].map(season_mapping)

st.subheader("Rata-rata Penyewaan Sepeda Harian Berdasarkan Musim")
fig2, ax2 = plt.subplots(figsize=(8, 6))

sns.barplot(x="season", y="cnt", data=season_avg, palette="Blues_d", ax=ax2)
ax2.set_title(f"Rata-rata Jumlah Penyewaan Sepeda Harian Berdasarkan Musim ({2011 + year_filter})", fontsize=14)
ax2.set_xlabel("Musim", fontsize=12)
ax2.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax2.grid(alpha=0.3)

st.pyplot(fig2)

# STEP 5: Ekspor Data Gabungan
st.sidebar.download_button("Download Data Filtered", data=filtered_data.to_csv(index=False), file_name="filtered_data_sewa_sepeda.csv")
