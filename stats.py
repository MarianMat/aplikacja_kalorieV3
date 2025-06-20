import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_stats(user_data):
    if user_data.empty:
        st.info("Brak danych do wyświetlenia statystyk.")
        return

    st.subheader("Statystyki tygodniowe")

    user_data["date_only"] = pd.to_datetime(user_data["date"]).dt.date
    week_data = user_data[user_data["date_only"] >= (pd.Timestamp.now() - pd.Timedelta(days=7)).date()]

    if week_data.empty:
        st.info("Brak danych z ostatniego tygodnia.")
        return

    calories_per_day = week_data.groupby("date_only")["calories"].sum()

    fig, ax = plt.subplots()
    calories_per_day.plot(kind="bar", ax=ax)
    ax.set_ylabel("Kalorie")
    ax.set_xlabel("Data")
    ax.set_title("Kalorie spożyte w ostatnim tygodniu")

    st.pyplot(fig)
# Wykresy i statystyki
