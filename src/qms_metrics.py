from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
CONFIG = ROOT / "config"

OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------------
# Load validated synthetic QMS datasets
# ---------------------------------------------------------------------
qe = pd.read_csv(DATA / "quality_events.csv")
capas = pd.read_csv(DATA / "capas.csv")
changes = pd.read_csv(DATA / "changes.csv")
training = pd.read_csv(DATA / "training_coverage.csv")

with open(CONFIG / "kpi_targets.json", "r", encoding="utf-8") as f:
    targets = json.load(f)

# ---------------------------------------------------------------------
# Quality-event KPIs
# ---------------------------------------------------------------------
open_qe = qe[qe["status"] == "Open"]
overdue_qe = open_qe[open_qe["overdue"] == True]
high_risk_open_qe = open_qe[open_qe["high_risk"] == True]

overdue_quality_event_pct = (
    len(overdue_qe) / len(open_qe) * 100
    if len(open_qe)
    else 0.0
)

# ---------------------------------------------------------------------
# CAPA KPIs
# ---------------------------------------------------------------------
open_capas = capas[capas["status"] == "Open"]
overdue_capas = open_capas[open_capas["overdue"] == True]

overdue_capa_pct = (
    len(overdue_capas) / len(open_capas) * 100
    if len(open_capas)
    else 0.0
)

closed_capas = capas[capas["status"] == "Closed"]

evaluated_capas = closed_capas[
    closed_capas["effectiveness_result"].isin(
        ["Effective", "Ineffective"]
    )
]

capa_effectiveness_pct = (
    (
        evaluated_capas["effectiveness_result"]
        .eq("Effective")
        .mean()
        * 100
    )
    if len(evaluated_capas)
    else 0.0
)

# ---------------------------------------------------------------------
# Change-management KPIs
# ---------------------------------------------------------------------
implemented_or_closed = changes[
    changes["implemented_date"].notna()
]

median_change_cycle_days = (
    implemented_or_closed["cycle_days"].median()
    if len(implemented_or_closed)
    else 0.0
)

follow_up_pending_changes = int(
    changes["follow_up_pending"].sum()
)

high_risk_not_closed = int(
    (
        (changes["risk_level"] == "High") &
        (changes["status"] != "Closed")
    ).sum()
)

# ---------------------------------------------------------------------
# Organizational-capability KPIs
# ---------------------------------------------------------------------
mean_training_coverage_pct = training["coverage_pct"].mean()

single_point_failure_processes = int(
    training["single_point_failure"].sum()
)

single_point_failure_pct = (
    single_point_failure_processes /
    len(training) * 100
    if len(training)
    else 0.0
)

# ---------------------------------------------------------------------
# KPI summary
# ---------------------------------------------------------------------
summary = {
    "total_quality_events": int(len(qe)),
    "open_quality_events": int(len(open_qe)),
    "overdue_quality_events": int(len(overdue_qe)),
    "overdue_quality_event_pct": round(
        overdue_quality_event_pct, 1
    ),
    "high_risk_open_quality_events": int(
        len(high_risk_open_qe)
    ),

    "total_capas": int(len(capas)),
    "open_capas": int(len(open_capas)),
    "overdue_capas": int(len(overdue_capas)),
    "overdue_capa_pct": round(
        overdue_capa_pct, 1
    ),
    "capa_effectiveness_pct": round(
        capa_effectiveness_pct, 1
    ),

    "closed_changes": int(
        (changes["status"] == "Closed").sum()
    ),
    "follow_up_pending_changes": follow_up_pending_changes,
    "in_progress_changes": int(
        (changes["status"] == "In Progress").sum()
    ),
    "high_risk_not_closed_changes": high_risk_not_closed,
    "median_change_cycle_days": round(
        float(median_change_cycle_days), 1
    ),

    "mean_training_coverage_pct": round(
        float(mean_training_coverage_pct), 1
    ),
    "single_point_failure_processes":
        single_point_failure_processes,
    "single_point_failure_pct": round(
        single_point_failure_pct, 1
    )
}

pd.DataFrame([summary]).to_csv(
    OUT / "kpi_summary.csv",
    index=False
)

# ---------------------------------------------------------------------
# Management-review threshold assessment
# IMPORTANT:
# These are portfolio scenario targets, not industry benchmarks.
# ---------------------------------------------------------------------
reviews = [
    {
        "kpi": "Overdue quality events",
        "value": round(overdue_quality_event_pct, 1),
        "unit": "%",
        "target": targets[
            "max_overdue_quality_event_pct"
        ],
        "direction": "max",
        "status": (
            "PASS"
            if overdue_quality_event_pct <=
            targets["max_overdue_quality_event_pct"]
            else "ACTION"
        ),
        "management_interpretation":
            "Open quality-event aging requires review."
    },
    {
        "kpi": "Overdue CAPAs",
        "value": round(overdue_capa_pct, 1),
        "unit": "%",
        "target": targets["max_overdue_capa_pct"],
        "direction": "max",
        "status": (
            "PASS"
            if overdue_capa_pct <=
            targets["max_overdue_capa_pct"]
            else "ACTION"
        ),
        "management_interpretation":
            "CAPA backlog requires prioritization."
    },
    {
        "kpi": "CAPA effectiveness",
        "value": round(capa_effectiveness_pct, 1),
        "unit": "%",
        "target": targets[
            "min_capa_effectiveness_pct"
        ],
        "direction": "min",
        "status": (
            "PASS"
            if capa_effectiveness_pct >=
            targets["min_capa_effectiveness_pct"]
            else "ACTION"
        ),
        "management_interpretation":
            "Assess recurrence and effectiveness-check outcomes."
    },
    {
        "kpi": "Median change cycle",
        "value": round(
            float(median_change_cycle_days), 1
        ),
        "unit": "days",
        "target": targets[
            "max_median_change_cycle_days"
        ],
        "direction": "max",
        "status": (
            "PASS"
            if median_change_cycle_days <=
            targets["max_median_change_cycle_days"]
            else "ACTION"
        ),
        "management_interpretation":
            "Review change implementation cycle time."
    },
    {
        "kpi": "Capability coverage",
        "value": round(
            float(mean_training_coverage_pct), 1
        ),
        "unit": "%",
        "target": targets[
            "min_training_coverage_pct"
        ],
        "direction": "min",
        "status": (
            "PASS"
            if mean_training_coverage_pct >=
            targets["min_training_coverage_pct"]
            else "ACTION"
        ),
        "management_interpretation":
            "Cross-training and backup coverage require attention."
    },
    {
        "kpi": "Single-point-of-failure exposure",
        "value": round(
            single_point_failure_pct, 1
        ),
        "unit": "%",
        "target": targets[
            "max_single_point_failure_pct"
        ],
        "direction": "max",
        "status": (
            "PASS"
            if single_point_failure_pct <=
            targets["max_single_point_failure_pct"]
            else "ACTION"
        ),
        "management_interpretation":
            "Reduce dependency on single qualified personnel."
    }
]

review_df = pd.DataFrame(reviews)

review_df.to_csv(
    OUT / "management_review_flags.csv",
    index=False
)
# ------------------------------------------------------------
# Root-cause recurrence and trend analysis
# ------------------------------------------------------------

root_cause_summary = (
    qe.groupby("root_cause_category")
    .agg(
        total_events=("event_id", "count"),
        open_events=("status", lambda s: (s == "Open").sum()),
        overdue_events=("overdue", "sum"),
        high_risk_events=("high_risk", "sum"),
    )
    .reset_index()
)
high_risk_open_by_cause = (
    qe.loc[(qe["status"] == "Open") & (qe["high_risk"])]
    .groupby("root_cause_category")
    .size()
)

root_cause_summary["high_risk_open_events"] = (
    root_cause_summary["root_cause_category"]
    .map(high_risk_open_by_cause)
    .fillna(0)
    .astype(int)
)

root_cause_summary["frequency_pct"] = (
    root_cause_summary["total_events"] / len(qe) * 100
).round(1)

root_cause_summary = root_cause_summary.sort_values(
    ["total_events", "high_risk_open_events"],
    ascending=[False, False],
)

qe_trend = qe.copy()
qe_trend["opened_month"] = (
    pd.to_datetime(qe_trend["opened_date"])
    .dt.to_period("M")
    .astype(str)
)

root_cause_monthly = (
    qe_trend.groupby(["opened_month", "root_cause_category"])
    .size()
    .reset_index(name="event_count")
)

root_cause_summary.to_csv(
    OUT / "root_cause_summary.csv",
    index=False,
)

root_cause_monthly.to_csv(
    OUT / "root_cause_monthly.csv",
    index=False,
)

print("\n=== ROOT-CAUSE FREQUENCY AND RISK ===")
print(root_cause_summary.to_string(index=False))
# ---------------------------------------------------------------------
# Console output
# ---------------------------------------------------------------------
print("\n=== QMS KPI SUMMARY ===")

for key, value in summary.items():
    print(f"{key}: {value}")

print("\n=== MANAGEMENT REVIEW ===")

print(
    review_df[
        ["kpi", "value", "unit", "target", "status"]
    ].to_string(index=False)
)

print(
    "\nNOTE: Thresholds are synthetic portfolio "
    "scenario targets, not industry benchmarks."
)

print("\nSaved:")
print(OUT / "kpi_summary.csv")
print(OUT / "management_review_flags.csv")
