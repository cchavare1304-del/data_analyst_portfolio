import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Analyst Portfolio", page_icon="📊", layout="wide")

def run_query(query):
    with sqlite3.connect('portfolio.db') as conn:
        return pd.read_sql_query(query, conn)

profile_df = run_query("SELECT * FROM profile LIMIT 1")
projects_df = run_query("SELECT * FROM projects")

if not profile_df.empty:
    name = profile_df['name'].iloc[0]
    role = profile_df['role'].iloc[0]
    summary = profile_df['summary'].iloc[0]
    skills = profile_df['skills'].iloc[0].split(', ')
else:
    name, role, summary, skills = "Candidate", "Data Analyst", "", []

st.title(f"👋 Hi, I'm chaitanya chavare")
st.subheader(f"🎯 Aspiring {role}")
st.write(summary)
st.markdown("---")

st.sidebar.header("🛠️ Technical Skills")
for skill in skills:
    st.sidebar.markdown(f"- **{skill}**")

st.sidebar.markdown("---")
st.sidebar.header("📬 Contact")
st.sidebar.write("📧 cchavare1304@gmail.com")

st.header("💻 Featured Data Analytics Projects")
col1, col2 = st.columns(2)

for index, row in projects_df.iterrows():
    target_col = col1 if index % 2 == 0 else col2
    with target_col:
        st.subheader(f"{index+1}. {row['title']}")
        st.markdown(f"**Tech Stack:** `{row['tech_stack']}`")
        st.write(row['description'])
        st.metric(label="Business Impact", value=f"{row['impact_metric']}%")
        st.markdown("---")

st.header("📊 Live SQL Data Demonstration")
st.code("SELECT title, impact_metric FROM projects ORDER BY impact_metric DESC;", language="sql")

fig = px.bar(
    projects_df, x='title', y='impact_metric', 
    labels={'title': 'Project Name', 'impact_metric': 'Efficiency Lift (%)'},
    title="Project Impact Driven by SQL Backend", color='impact_metric'
)
st.plotly_chart(fig, use_container_width=True)
