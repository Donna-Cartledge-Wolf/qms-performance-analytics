from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

qe = pd.read_csv(DATA/"quality_events.csv")
capas = pd.read_csv(DATA/"capas.csv")
changes = pd.read_csv(DATA/"changes.csv")
training = pd.read_csv(DATA/"training_coverage.csv")

closed = capas[capas["status"]=="Closed"]
evaluated = closed[closed["effectiveness_result"].isin(["Effective","Ineffective"])]

summary = {
    "open_quality_events": int((qe["status"]=="Open").sum()),
    "overdue_quality_events": int(qe["overdue"].sum()),
    "high_risk_open_quality_events": int(((qe["status"]=="Open") & qe["high_risk"]).sum()),
    "overdue_capa": int(capas["overdue"].sum()),
    "capa_effectiveness_pct": round((evaluated["effectiveness_result"]=="Effective").mean()*100,1),
    "median_change_cycle_days": round(changes.loc[changes["status"]=="Implemented","cycle_days"].median(),1),
    "mean_training_coverage_pct": round(training["coverage_pct"].mean(),1),
    "single_point_failure_processes": int(training["single_point_failure"].sum())
}

pd.DataFrame([summary]).to_csv(OUT/"kpi_summary.csv", index=False)
print(pd.Series(summary))
