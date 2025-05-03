import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px

# --- Load and parse data ---
with open("Agent 1/summary.json") as f1:
    raw_tasks = json.load(f1)

with open("Agent 2/summary_jira.json") as f2:
    jira_tasks = json.load(f2)

with open("Agent 3/final_summary.json") as f3:  
    text_summary = json.load(f3)

summary_df = pd.DataFrame(raw_tasks)
jira_df = pd.DataFrame(jira_tasks.get("Alice", []))

# Convert dates
summary_df["deadline"] = pd.to_datetime(summary_df["deadline"], errors="coerce")
summary_df["completed_date"] = pd.to_datetime(summary_df["completed_date"], errors="coerce")
jira_df["duedate"] = pd.to_datetime(jira_df["duedate"], errors="coerce")
jira_df["completed"] = pd.to_datetime(jira_df["completed"], errors="coerce")

# --- Streamlit Layout ---
st.set_page_config(page_title="Task Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>📋 Task Summary Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("✅ Completed", len(summary_df[summary_df.status == "completed"]))
col2.metric("❌ Not Completed", len(summary_df[summary_df.status == "not completed"]))
col3.metric("📊 Jira Tasks", len(jira_df))

# --- Tabs for detailed views ---
tab1, tab2, tab3 = st.tabs(["🧾 Summary Tasks", "🛠️ Jira Tasks", "📄 Text Summary"])

with tab1:
    st.subheader("✅ Completed Tasks")
    st.dataframe(summary_df[summary_df.status == "completed"])

    st.subheader("❌ Incomplete Tasks")
    st.dataframe(summary_df[summary_df.status == "not completed"])

with tab2:
    st.subheader("👩‍💻 Jira - Alice's Tasks")
    st.dataframe(jira_df)

with tab3:
    st.subheader("📘 Work Completed")
    for item in text_summary["Work completed"]:
        st.success(f"✔️ {item}")
    st.subheader("⚠️ Work Not Completed")
    for item in text_summary["Work not completed"]:
        st.warning(f"❌ {item}")
    st.subheader("📅 Tasks Completed On Time")
    for item in text_summary["Tasks completed on time"]:
        st.info(f"🕒 {item}")
    if text_summary["Missed deadlines"]:
        st.subheader("🚨 Missed Deadlines")
        for item in text_summary["Missed deadlines"]:
            st.error(f"⏰ {item}")
    else:
        st.info("✅ No missed deadlines!")

# --- Timeline chart ---
st.markdown("## 🗓️ Task Timeline")
timeline_df = summary_df.copy()
timeline_df["Task"] = timeline_df["description"]
timeline_df["Start"] = timeline_df["completed_date"].fillna(timeline_df["deadline"])
timeline_df["End"] = timeline_df["deadline"]

fig = px.timeline(timeline_df, x_start="Start", x_end="End", y="Task", color="status", title="Task Timeline")
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("🔧 Built with Streamlit · 📁 Inputs from 3 JSON files · 💡 Dashboard Summary View")
