import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 1: Persiapkan DataFrame
st.title("Dashboard Sewa Sepeda")
st.sidebar.header("Filter")

# Load datasets
day_df = pd.read_csv("https://raw.githubusercontent.com/Jawaaa/Dataset-Proyek-Data-Scient/refs/heads/main/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/Jawaaa/Dataset-Proyek-Data-Scient/refs/heads/main/hour.csv")

# Periksa data
day_df.drop_duplicates(inplace=True)
hour_df.drop_duplicates(inplace=True)

# Gabungkan data
all_df = pd.merge(
    day_df, hour_df, 
    how="left", 
    left_on="dteday", 
    right_on="dteday"
)

# STEP 2: Buat Fungsi Helper untuk Data Agregasi
def aggregate_by_season(data):
    return data.groupby(["season_x", "season_y"]).agg({
        "cnt_x": "sum",
        "cnt_y": "sum"
    }).reset_index()

def aggregate_by_year(data):
    return data.groupby(["yr_x", "yr_y"]).agg({
        "cnt_x": "sum",
        "cnt_y": "sum",
        "registered_x": "sum",
        "registered_y": "sum",
        "casual_x": "sum",
        "casual_y": "sum"
    }).reset_index()

season_data = aggregate_by_season(all_df)
year_data = aggregate_by_year(all_df)

# STEP 3: Tambahkan Filter Sidebar
year_filter = st.sidebar.selectbox("Pilih Tahun", options=[0, 1], format_func=lambda x: "2011" if x == 0 else "2012")
season_filter = st.sidebar.selectbox("Pilih Musim", options=[1, 2, 3, 4], format_func=lambda x: ["Spring", "Summer", "Fall", "Winter"][x-1])

filtered_data = all_df[(all_df["yr_x"] == year_filter) & (all_df["season_x"] == season_filter)]

# STEP 4: Bangun Visualisasi
# Total Penyewaan per Musim
seasons = ["Spring", "Summer", "Fall", "Winter"]
filtered_season_data = season_data[season_data["season_x"] == season_data["season_y"]]

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(seasons))
bar_width = 0.35

ax.bar(x - bar_width / 2, filtered_season_data["cnt_x"], width=bar_width, label="Count of Total Day", color="#72BCD4")
ax.bar(x + bar_width / 2, filtered_season_data["cnt_y"], width=bar_width, label="Count of Total Hour", color="#F6A9A9")

ax.set_title("Total Rentals by Season", fontsize=16)
ax.set_xlabel("Season", fontsize=12)
ax.set_ylabel("Total Rentals", fontsize=12)
ax.set_xticks(ticks=x)
ax.set_xticklabels(seasons, fontsize=10)
ax.legend(title="Rental Type", loc="upper left")
ax.grid(alpha=0.3)
ax.set_yscale('log')

st.pyplot(fig)

# Total Penyewaan Sepeda per Tahun
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.barplot(x="yr_x", y="cnt_x", data=year_data, ax=axes[0, 0], color="skyblue", label="day")
sns.barplot(x="yr_y", y="cnt_y", data=year_data, ax=axes[0, 0], color="orange", label="hour")
axes[0, 0].set_title("Total Penyewaan Sepeda per Tahun")
axes[0, 0].set_xlabel("Tahun (0=2011 , 1=2012)")
axes[0, 0].set_ylabel("Total Penyewaan")
axes[0, 0].legend()
axes[0, 0].set_yscale('log')

sns.barplot(x="yr_x", y="registered_x", data=year_data, ax=axes[0, 1], color="green", label="day")
sns.barplot(x="yr_y", y="registered_y", data=year_data, ax=axes[0, 1], color="red", label="hour")
axes[0, 1].set_title("Total Pengguna Terdaftar per Tahun")
axes[0, 1].set_xlabel("Tahun (0=2011 , 1=2012)")
axes[0, 1].set_ylabel("Total Pengguna Terdaftar")
axes[0, 1].legend()
axes[0, 1].set_yscale('log')

sns.barplot(x="yr_x", y="casual_x", data=year_data, ax=axes[1, 0], color="purple", label="day")
sns.barplot(x="yr_y", y="casual_y", data=year_data, ax=axes[1, 0], color="yellow", label="hour")
axes[1, 0].set_title("Total Pengguna Casual per Tahun")
axes[1, 0].set_xlabel("Tahun (0=2011 , 1=2012)")
axes[1, 0].set_ylabel("Total Pengguna Casual")
axes[1, 0].legend()
axes[1, 0].set_yscale('log')

sns.barplot(x="yr_x", y="cnt_x", data=year_data, ax=axes[1, 1], color="skyblue", label="day")
sns.barplot(x="yr_y", y="cnt_y", data=year_data, ax=axes[1, 1], color="orange", label="hour")
axes[1, 1].set_title("Perbandingan Total Penyewaan per Tahun")
axes[1, 1].set_xlabel("Tahun (0=2011 , 1=2012)")
axes[1, 1].set_ylabel("Total Penyewaan Sepeda")
axes[1, 1].legend()
axes[1, 1].set_yscale('log')

st.pyplot(fig)

# STEP 5: Ekspor dan Tampilkan Data
st.sidebar.download_button("Download Data Gabungan", data=all_df.to_csv(index=False), file_name="all_data_sewa_sepeda.csv")
