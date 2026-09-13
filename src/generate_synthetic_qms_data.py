from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

rng = np.random.default_rng(42)
today = pd.Timestamp.today().normalize()

# Quality events
n = 180
opened = today - pd.to_timedelta(rng.integers(0, 365, n), unit="D")
event_type = rng.choice(["Complaint", "Investigation"], n, p=[0.45, 0.55])
severity = rng.choice(["Low", "Medium", "High", "Critical"], n, p=[0.25, 0.45, 0.23, 0.07])
status = rng.choice(["Open", "Closed"], n, p=[0.28, 0.72])
target_days = np.select([severity=="Critical", severity=="High", severity=="Medium"], [15,30,45], default=60)
cycle = rng.integers(7, 95, n)
closed = pd.Series(opened + pd.to_timedelta(cycle, unit="D")).where(status=="Closed", pd.NaT)
root_causes = rng.choice(["Procedure","Training","Equipment","Supplier","Material","Data / Documentation","Process Design"], n)
age_days = np.where(status=="Closed",
                    (closed - pd.Series(opened)).dt.days,
                    (today - pd.Series(opened)).dt.days)

qe = pd.DataFrame({
    "event_id":[f"QE-{i:04d}" for i in range(1,n+1)],
    "event_type":event_type,
    "opened_date":opened,
    "closed_date":closed,
    "status":status,
    "severity":severity,
    "root_cause_category":root_causes,
    "target_days":target_days,
    "age_days":age_days
})
qe["overdue"] = (qe["status"]=="Open") & (qe["age_days"]>qe["target_days"])
qe["high_risk"] = qe["severity"].isin(["High","Critical"])
qe.to_csv(DATA/"quality_events.csv", index=False)

# CAPAs
n = 95
opened = today - pd.to_timedelta(rng.integers(0, 330, n), unit="D")
due = opened + pd.to_timedelta(rng.integers(30, 91, n), unit="D")
status = rng.choice(["Open","Closed"], n, p=[0.25,0.75])
completion = pd.Series(opened + pd.to_timedelta(rng.integers(20,110,n), unit="D")).where(status=="Closed", pd.NaT)
effectiveness = rng.choice(["Effective","Ineffective","Pending"], n, p=[0.72,0.08,0.20])
effectiveness = np.where(status=="Open","Pending",effectiveness)

capas = pd.DataFrame({
    "capa_id":[f"CAPA-{i:04d}" for i in range(1,n+1)],
    "source":rng.choice(["Complaint","Investigation","Audit","Trend","Supplier"], n),
    "opened_date":opened,
    "due_date":due,
    "completion_date":completion,
    "status":status,
    "risk_level":rng.choice(["Low","Medium","High"], n, p=[0.25,0.50,0.25]),
    "effectiveness_result":effectiveness
})
capas["overdue"] = (capas["status"]=="Open") & (today>capas["due_date"])
capas["cycle_days"] = np.where(capas["status"]=="Closed",
    (pd.to_datetime(capas["completion_date"])-pd.to_datetime(capas["opened_date"])).dt.days,
    (today-pd.to_datetime(capas["opened_date"])).dt.days)
capas.to_csv(DATA/"capas.csv", index=False)

# Changes
n = 120
submitted = today - pd.to_timedelta(rng.integers(0,365,n), unit="D")
status = rng.choice(["Implemented","In Progress"], n, p=[0.78,0.22])
approval_days = rng.integers(2,28,n)
implementation_days = approval_days + rng.integers(5,55,n)
implemented = pd.Series(submitted + pd.to_timedelta(implementation_days, unit="D")).where(status=="Implemented", pd.NaT)

changes = pd.DataFrame({
    "change_id":[f"CHG-{i:04d}" for i in range(1,n+1)],
    "change_type":rng.choice(["Process","Document","Training","ERP / Software","Equipment","Supplier"], n),
    "submitted_date":submitted,
    "implemented_date":implemented,
    "status":status,
    "risk_level":rng.choice(["Low","Medium","High"], n, p=[0.30,0.50,0.20]),
    "approval_days":approval_days,
    "training_required":rng.choice([True,False], n, p=[0.60,0.40]),
    "training_complete_pct":rng.integers(70,101,n),
    "verification_complete":rng.choice([True,False], n, p=[0.88,0.12])
})
changes["cycle_days"] = np.where(changes["status"]=="Implemented",
    (pd.to_datetime(changes["implemented_date"])-pd.to_datetime(changes["submitted_date"])).dt.days,
    (today-pd.to_datetime(changes["submitted_date"])).dt.days)
changes.to_csv(DATA/"changes.csv", index=False)

# Training / capability
processes = ["Complaint Handling","Investigation / RCA","CAPA","Change Management",
             "Supplier Quality","QMS Metrics","Document Control","Risk Assessment"]
rows = []
for process in processes:
    qualified = int(rng.integers(1,6))
    required = int(rng.integers(max(qualified,2),7))
    rows.append({
        "process":process,
        "qualified_personnel":qualified,
        "required_coverage":required,
        "backup_personnel":max(0,qualified-1)
    })

training = pd.DataFrame(rows)
training["coverage_pct"] = (training["qualified_personnel"]/training["required_coverage"]*100).clip(upper=100).round(1)
training["single_point_failure"] = training["qualified_personnel"]<=1
training.to_csv(DATA/"training_coverage.csv", index=False)

print("Synthetic QMS datasets generated.")
