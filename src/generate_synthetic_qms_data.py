from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

rng = np.random.default_rng(42)
today = pd.Timestamp.today().normalize()

# ---------------------------------------------------------------------
# QUALITY EVENTS
# Healthy-but-imperfect synthetic QMS scenario:
# most events controlled, with a manageable overdue/high-risk subset.
# ---------------------------------------------------------------------
n = 180

status = np.array(["Closed"] * 140 + ["Open"] * 40, dtype=object)
rng.shuffle(status)

event_type = rng.choice(
    ["Complaint", "Investigation"],
    n,
    p=[0.45, 0.55]
)

severity = rng.choice(
    ["Low", "Medium", "High", "Critical"],
    n,
    p=[0.25, 0.45, 0.23, 0.07]
)

target_days = np.select(
    [
        severity == "Critical",
        severity == "High",
        severity == "Medium"
    ],
    [15, 30, 45],
    default=60
)

root_cause_category = rng.choice(
    [
        "Procedure",
        "Training",
        "Data / Documentation",
        "Process Design",
        "Equipment",
        "Supplier",
        "Material"
    ],
    n,
    p=[0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]
)

process_area = rng.choice(
    [
        "Complaint Handling",
        "Investigation / RCA",
        "CAPA",
        "Change Management",
        "Supplier Quality",
        "QMS Metrics",
        "Document Control",
        "Risk Assessment"
    ],
    n,
    p=[0.18, 0.15, 0.12, 0.15, 0.12, 0.10, 0.12, 0.06]
)

opened_dates = []
closed_dates = []
age_days = []

# Deliberately design a manageable overdue backlog:
# 8 of 40 open quality events (20%) will be overdue.
open_indices = np.where(status == "Open")[0]
overdue_open_indices = set(
    rng.choice(open_indices, size=8, replace=False).tolist()
)

for i in range(n):
    if status[i] == "Open":
        if i in overdue_open_indices:
            # Overdue, but not unrealistically old.
            extra_days = int(rng.integers(1, 46))
            age = int(target_days[i] + extra_days)
        else:
            # Open and still within its severity-based target window.
            age = int(rng.integers(1, int(target_days[i]) + 1))

        opened = today - pd.Timedelta(days=age)
        closed = pd.NaT
        event_age = age

    else:
        # Closed events are constructed so closure can never occur in the future.
        open_age = int(rng.integers(20, 366))
        max_cycle = max(7, min(90, open_age))
        cycle = int(rng.integers(7, max_cycle + 1))

        opened = today - pd.Timedelta(days=open_age)
        closed = opened + pd.Timedelta(days=cycle)
        event_age = cycle

    opened_dates.append(opened)
    closed_dates.append(closed)
    age_days.append(event_age)

quality_events = pd.DataFrame({
    "event_id": [f"QE-{i:04d}" for i in range(1, n + 1)],
    "event_type": event_type,
    "process_area": process_area,
    "opened_date": opened_dates,
    "closed_date": closed_dates,
    "status": status,
    "severity": severity,
    "root_cause_category": root_cause_category,
    "target_days": target_days,
    "age_days": age_days
})

quality_events["overdue"] = (
    (quality_events["status"] == "Open") &
    (quality_events["age_days"] > quality_events["target_days"])
)

quality_events["high_risk"] = quality_events["severity"].isin(
    ["High", "Critical"]
)

quality_events.to_csv(
    DATA / "quality_events.csv",
    index=False
)

# ---------------------------------------------------------------------
# CAPA
# Functioning system with a small overdue backlog and strong,
# but not perfect, effectiveness.
# ---------------------------------------------------------------------
n = 95

status = np.array(["Closed"] * 77 + ["Open"] * 18, dtype=object)
rng.shuffle(status)

opened_dates = []
due_dates = []
completion_dates = []
effectiveness_results = []

for i in range(n):
    if status[i] == "Open":
        if rng.random() < 0.75:
            age = int(rng.integers(5, 46))
        else:
            age = int(rng.integers(46, 101))

        opened = today - pd.Timedelta(days=age)
        due_days = int(rng.integers(45, 91))
        due = opened + pd.Timedelta(days=due_days)
        completion = pd.NaT
        effectiveness = "Pending"

    else:
        open_age = int(rng.integers(40, 331))
        opened = today - pd.Timedelta(days=open_age)

        due_days = int(rng.integers(45, 91))
        due = opened + pd.Timedelta(days=due_days)

        max_cycle = max(20, min(100, open_age))
        cycle = int(rng.integers(20, max_cycle + 1))
        completion = opened + pd.Timedelta(days=cycle)

        r = rng.random()
        if r < 0.80:
            effectiveness = "Effective"
        elif r < 0.87:
            effectiveness = "Ineffective"
        else:
            effectiveness = "Pending"

    opened_dates.append(opened)
    due_dates.append(due)
    completion_dates.append(completion)
    effectiveness_results.append(effectiveness)

capas = pd.DataFrame({
    "capa_id": [f"CAPA-{i:04d}" for i in range(1, n + 1)],
    "source": rng.choice(
        ["Complaint", "Investigation", "Audit", "Trend", "Supplier"],
        n,
        p=[0.28, 0.30, 0.15, 0.17, 0.10]
    ),
    "opened_date": opened_dates,
    "due_date": due_dates,
    "completion_date": completion_dates,
    "status": status,
    "risk_level": rng.choice(
        ["Low", "Medium", "High"],
        n,
        p=[0.25, 0.55, 0.20]
    ),
    "effectiveness_result": effectiveness_results
})

capas["overdue"] = (
    (capas["status"] == "Open") &
    (today > pd.to_datetime(capas["due_date"]))
)

capas["cycle_days"] = np.where(
    capas["status"] == "Closed",
    (
        pd.to_datetime(capas["completion_date"]) -
        pd.to_datetime(capas["opened_date"])
    ).dt.days,
    (
        today -
        pd.to_datetime(capas["opened_date"])
    ).dt.days
)

capas.to_csv(
    DATA / "capas.csv",
    index=False
)

# ---------------------------------------------------------------------
# CHANGE MANAGEMENT
# Three-stage lifecycle:
# In Progress -> Implemented / Follow-up Pending -> Closed
# ---------------------------------------------------------------------
n = 120

submitted = today - pd.to_timedelta(
    rng.integers(0, 365, n),
    unit="D"
)

approval_days = rng.integers(2, 16, n)
implementation_days = approval_days + rng.integers(5, 36, n)

implementation_candidate = pd.Series(
    submitted + pd.to_timedelta(implementation_days, unit="D")
)

risk_level = rng.choice(
    ["Low", "Medium", "High"],
    n,
    p=[0.40, 0.50, 0.10]
)

training_required = rng.choice(
    [True, False],
    n,
    p=[0.60, 0.40]
)

implementation_eligible = implementation_candidate <= today

implemented_flag = (
    implementation_eligible &
    (rng.random(n) < 0.80)
)

implemented_date = implementation_candidate.where(
    implemented_flag,
    pd.NaT
)

training_complete_pct = np.full(n, 100)

for i in range(n):
    if training_required[i]:
        if not implemented_flag[i]:
            training_complete_pct[i] = int(rng.integers(0, 96))
        else:
            if rng.random() < 0.82:
                training_complete_pct[i] = 100
            else:
                training_complete_pct[i] = int(rng.integers(80, 100))

verification_complete = np.zeros(n, dtype=bool)

for i in range(n):
    if implemented_flag[i]:
        verification_complete[i] = rng.random() < 0.90

training_ok = (
    (~training_required) |
    (training_complete_pct == 100)
)

ready_for_closure = (
    implemented_flag &
    verification_complete &
    training_ok
)

status = np.full(n, "In Progress", dtype=object)
status[implemented_flag] = "Implemented"
status[ready_for_closure] = "Closed"

follow_up_pending = status == "Implemented"

changes = pd.DataFrame({
    "change_id": [f"CHG-{i:04d}" for i in range(1, n + 1)],
    "change_type": rng.choice(
        [
            "Process",
            "Document",
            "Training",
            "ERP / Software",
            "Equipment",
            "Supplier"
        ],
        n
    ),
    "submitted_date": submitted,
    "implemented_date": implemented_date,
    "status": status,
    "risk_level": risk_level,
    "approval_days": approval_days,
    "training_required": training_required,
    "training_complete_pct": training_complete_pct,
    "verification_complete": verification_complete,
    "follow_up_pending": follow_up_pending,
    "ready_for_closure": ready_for_closure
})

changes["cycle_days"] = np.where(
    changes["implemented_date"].notna(),
    (
        pd.to_datetime(changes["implemented_date"]) -
        pd.to_datetime(changes["submitted_date"])
    ).dt.days,
    (
        today -
        pd.to_datetime(changes["submitted_date"])
    ).dt.days
)

changes.to_csv(
    DATA / "changes.csv",
    index=False
)

# ---------------------------------------------------------------------
# TRAINING / ORGANIZATIONAL CAPABILITY
# Mostly healthy coverage with one intentional single-point dependency.
# ---------------------------------------------------------------------
training = pd.DataFrame([
    {
        "process": "Complaint Handling",
        "qualified_personnel": 5,
        "required_coverage": 6
    },
    {
        "process": "Investigation / RCA",
        "qualified_personnel": 5,
        "required_coverage": 5
    },
    {
        "process": "CAPA",
        "qualified_personnel": 1,
        "required_coverage": 1
    },
    {
        "process": "Change Management",
        "qualified_personnel": 4,
        "required_coverage": 5
    },
    {
        "process": "Supplier Quality",
        "qualified_personnel": 5,
        "required_coverage": 6
    },
    {
        "process": "QMS Metrics",
        "qualified_personnel": 4,
        "required_coverage": 5
    },
    {
        "process": "Document Control",
        "qualified_personnel": 5,
        "required_coverage": 5
    },
    {
        "process": "Risk Assessment",
        "qualified_personnel": 4,
        "required_coverage": 4
    }
])

training["backup_personnel"] = (
    training["qualified_personnel"] - 1
).clip(lower=0)

training["coverage_pct"] = (
    training["qualified_personnel"] /
    training["required_coverage"] * 100
).clip(upper=100).round(1)

training["single_point_failure"] = (
    training["qualified_personnel"] <= 1
)

training.to_csv(
    DATA / "training_coverage.csv",
    index=False
)

print("Synthetic QMS datasets generated.")
