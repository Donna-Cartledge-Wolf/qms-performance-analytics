from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

st.set_page_config(page_title="QMS Performance Analytics", layout="wide")
st.title("Wolf Analytics — QMS Performance & Change Management")
st.caption("Portfolio demonstration using 100% synthetic quality-system data.")

qe = pd.read_csv(DATA/"quality_events.csv")
capas = pd.read_csv(DATA/"capas.csv")
changes = pd.read_csv(DATA/"changes.csv")
training = pd.read_csv(DATA/"training_coverage.csv")

closed = capas[capas["status"]=="Closed"]
evaluated = closed[closed["effectiveness_result"].isin(["Effective","Ineffective"])]
capa_eff = (evaluated["effectiveness_result"]=="Effective").mean()*100 if len(evaluated) else 0

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Open Quality Events", int((qe["status"]=="Open").sum()))
c2.metric("Overdue Quality Events", int(qe["overdue"].sum()))
c3.metric("Overdue CAPAs", int(capas["overdue"].sum()))
c4.metric("CAPA Effectiveness", f"{capa_eff:.1f}%")
c5.metric("Median Change Cycle", f"{changes.loc[changes['status']=='Implemented','cycle_days'].median():.0f} days")

st.subheader("Root Cause Distribution")
fig, ax = plt.subplots()
qe["root_cause_category"].value_counts().sort_values().plot(kind="barh", ax=ax)
ax.set_xlabel("Quality Events")
ax.set_ylabel("")
st.pyplot(fig)

st.subheader("Open / Overdue Quality Events")
open_events = qe[qe["status"]=="Open"].sort_values("age_days", ascending=False)
st.dataframe(open_events[["event_id","event_type","severity","root_cause_category","age_days","target_days","overdue"]],
             use_container_width=True)

st.subheader("Change Management Performance")
fig, ax = plt.subplots()
changes.loc[changes["status"]=="Implemented","cycle_days"].plot(kind="hist", bins=12, ax=ax)
ax.set_xlabel("Implementation Cycle Time (days)")
st.pyplot(fig)

st.subheader("Organizational Capability / Cross-Training")
st.dataframe(training, use_container_width=True)
