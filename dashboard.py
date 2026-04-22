import streamlit as st
import json
import os
import time

st.set_page_config(page_title="Multi-Client Dashboard", layout="wide")

st.title("📊 Multi-Client File Transfer Dashboard")

def load_stats():
    if os.path.exists("stats.json"):
        with open("stats.json", "r") as f:
            return json.load(f)
    return {}

stats = load_stats()

if stats:

    for client_id, data in stats.items():

        st.subheader(f"🖥 Client: {client_id}")
        st.write(f"📄 File: {data['filename']}")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Packets Sent", data["packets_sent"])
        col2.metric("Retransmissions", data["retransmissions"])
        col3.metric("Packet Loss", data["packet_loss"])
        col4.metric("Transfer Time", data["transfer_time"])

        total = data["packets_sent"] + data["packet_loss"]
        loss_rate = (data["packet_loss"] / total * 100) if total else 0

        st.write(f"Loss Rate: {loss_rate:.2f}%")

        st.divider()

else:
    st.warning("No transfers yet")

time.sleep(2)
st.rerun()