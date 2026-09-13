from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
ASSETS = ROOT / "assets"

st.set_page_config(
    page_title="Wolf Analytics QMS Management Review",
    layout="wide",
)


# ------------------------------------------------------------
# Load validated synthetic data
# ------------------------------------------------------------

qe = pd.read_csv(
    DATA / "quality_events.csv",
    parse_dates=["opened_date", "closed_date"],
)

capas = pd.read_csv(
    DATA / "capas.csv",
    parse_dates=["opened_date", "due_date", "completion_date"],
)

changes = pd.read_csv(
    DATA / "changes.csv",
    parse_dates=["submitted_date", "implemented_date"],
)

training = pd.read_csv(DATA / "training_coverage.csv")

review = pd.read_csv(OUT / "management_review_flags.csv")
root_summary = pd.read_csv(OUT / "root_cause_summary.csv")
root_monthly = pd.read_csv(OUT / "root_cause_monthly.csv")


# ------------------------------------------------------------
# Display helpers
# ------------------------------------------------------------

DISPLAY_NAMES = {
    "event_id": "Event ID",
    "event_type": "Event Type",
    "severity": "Severity",
    "root_cause_category": "Root Cause",
    "age_days": "Age, Days",
    "target_days": "Target, Days",
    "overdue": "Overdue",
    "risk_level": "Risk Level",
    "capa_id": "CAPA ID",
    "source": "Source",
    "opened_date": "Opened Date",
    "due_date": "Due Date",
    "completion_date": "Completion Date",
    "effectiveness_result": "Effectiveness Result",
    "cycle_days": "Cycle, Days",
    "change_id": "Change ID",
    "change_type": "Change Type",
    "submitted_date": "Submitted Date",
    "implemented_date": "Implemented Date",
    "status": "Status",
    "verification_complete": "Verification Complete",
    "training_required": "Training Required",
    "training_complete_pct": "Training Complete",
    "process": "Process",
    "qualified_personnel": "Qualified Personnel",
    "required_coverage": "Required Coverage",
    "backup_personnel": "Backup Personnel",
    "coverage_pct": "Coverage",
    "single_point_failure": "Single-Point Failure",
    "total_events": "Total Events",
    "open_events": "Open Events",
    "overdue_events": "Overdue Events",
    "high_risk_open_events": "High-Risk Open Events",
    "frequency_pct": "Frequency",
}


def available_columns(df, requested):
    return [column for column in requested if column in df.columns]


def clean_table(df, columns, date_columns=None, percent_columns=None):
    selected = available_columns(df, columns)
    output = df[selected].copy()

    date_columns = date_columns or []
    percent_columns = percent_columns or []

    for column in date_columns:
        if column in output.columns:
            output[column] = pd.to_datetime(
                output[column],
                errors="coerce",
            ).dt.strftime("%Y-%m-%d")
            output[column] = output[column].fillna("")

    for column in percent_columns:
        if column in output.columns:
            output[column] = output[column].map(
                lambda value: f"{value:.1f}%"
                if pd.notna(value)
                else ""
            )

    return output.rename(columns=DISPLAY_NAMES)


def format_review_value(value, unit):
    if unit == "%":
        return f"{float(value):.1f}%"
    if unit == "days":
        return f"{float(value):.0f} days"
    return f"{value}"


def review_table(df):
    output = df.copy()

    output["Value"] = output.apply(
        lambda row: format_review_value(row["value"], row["unit"]),
        axis=1,
    )

    output["Target"] = output.apply(
        lambda row: format_review_value(row["target"], row["unit"]),
        axis=1,
    )

    output = output[
        [
            "kpi",
            "Value",
            "Target",
            "status",
            "management_interpretation",
        ]
    ].rename(
        columns={
            "kpi": "KPI",
            "status": "Status",
            "management_interpretation": "Management Interpretation",
        }
    )

    output.loc[
        output["KPI"] == "CAPA effectiveness",
        "Management Interpretation",
    ] = "Review CAPA effectiveness-check outcomes and repeat issue patterns."

    return output


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

logo_path = ASSETS / "Wolf_Analytics_Logo.png"

if logo_path.exists():
    left, center, right = st.columns([1, 1, 1])
    with center:
        st.image(str(logo_path), width=230)

st.title("QMS Performance & Change Management Analytics")

st.caption(
    "Wolf Analytics portfolio demonstration using 100% synthetic "
    "quality-system data. Scenario targets are portfolio targets, "
    "not industry benchmarks."
)

st.divider()


# ------------------------------------------------------------
# Core metrics
# ------------------------------------------------------------

open_qe = qe[qe["status"] == "Open"].copy()
open_capas = capas[capas["status"] == "Open"].copy()

evaluated_capas = capas[
    (capas["status"] == "Closed")
    & (capas["effectiveness_result"].isin(["Effective", "Ineffective"]))
].copy()

capa_effectiveness = (
    (evaluated_capas["effectiveness_result"] == "Effective").mean() * 100
    if len(evaluated_capas)
    else 0
)

implemented_changes = changes[
    changes["implemented_date"].notna()
].copy()

median_change_cycle = implemented_changes["cycle_days"].median()

mean_training_coverage = training["coverage_pct"].mean()

single_point_failures = int(
    training["single_point_failure"].sum()
)

high_risk_not_closed = int(
    (
        (changes["risk_level"] == "High")
        & (changes["status"] != "Closed")
    ).sum()
)



# ------------------------------------------------------------
# Management priorities
# ------------------------------------------------------------

st.header("Management Priorities")

action_items = review[review["status"] == "ACTION"].copy()
pass_items = review[review["status"] == "PASS"].copy()

summary_left, summary_right = st.columns(2)

with summary_left:
    st.warning(
        f"{len(action_items)} KPI areas currently require management action."
    )

with summary_right:
    st.success(
        f"{len(pass_items)} KPI areas currently meet the portfolio target."
    )

if len(action_items):
    st.dataframe(
        review_table(action_items),
        use_container_width=True,
        hide_index=True,
    )

st.divider()


# ------------------------------------------------------------
# Executive KPI overview
# ------------------------------------------------------------

st.header("Executive KPI Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Open Quality Events",
        f"{len(open_qe)}",
    )

with c2:
    st.metric(
        "Overdue Open Events",
        f"{int(open_qe['overdue'].sum())}",
    )
    st.caption(
        f"{open_qe['overdue'].mean() * 100:.1f}% of open quality events"
    )

with c3:
    st.metric(
        "High-Risk Open Events",
        f"{int(open_qe['high_risk'].sum())}",
    )

with c4:
    st.metric(
        "Open CAPAs",
        f"{len(open_capas)}",
    )
    st.caption(
        f"{int(open_capas['overdue'].sum())} currently overdue"
    )

c5, c6, c7, c8 = st.columns(4)

with c5:
    st.metric(
        "CAPA Effectiveness",
        f"{capa_effectiveness:.1f}%",
    )

with c6:
    st.metric(
        "Median Change Cycle",
        f"{median_change_cycle:.0f} days",
    )

with c7:
    st.metric(
        "Mean Capability Coverage",
        f"{mean_training_coverage:.1f}%",
    )

with c8:
    st.metric(
        "Single-Point Failures",
        f"{single_point_failures}",
    )

st.divider()


# ------------------------------------------------------------
# Quality event aging and risk
# ------------------------------------------------------------

st.header("Quality Event Aging and Risk")

risk_events = open_qe[
    open_qe["overdue"] | open_qe["high_risk"]
].copy()

risk_events = risk_events.sort_values(
    ["high_risk", "overdue", "age_days"],
    ascending=[False, False, False],
)

risk_display = clean_table(
    risk_events,
    [
        "event_id",
        "event_type",
        "severity",
        "root_cause_category",
        "age_days",
        "target_days",
        "overdue",
        "high_risk",
    ],
)

st.dataframe(
    risk_display,
    use_container_width=True,
    hide_index=True,
)

st.divider()


# ------------------------------------------------------------
# Root-cause frequency and risk
# ------------------------------------------------------------

st.header("Root-Cause Frequency and Risk")

left, right = st.columns([1.15, 1])

with left:
    plot_data = root_summary.sort_values("total_events")

    fig, ax = plt.subplots(figsize=(8, 4.8))

    bars = ax.barh(
        plot_data["root_cause_category"],
        plot_data["total_events"],
    )

    ax.bar_label(bars, padding=3)
    ax.set_xlabel("Quality Events")
    ax.set_ylabel("")
    ax.set_title("Quality Events by Root-Cause Category")

    st.pyplot(fig)
    plt.close(fig)

with right:
    root_display = clean_table(
        root_summary,
        [
            "root_cause_category",
            "total_events",
            "open_events",
            "overdue_events",
            "high_risk_open_events",
            "frequency_pct",
        ],
        percent_columns=["frequency_pct"],
    )

    st.dataframe(
        root_display,
        use_container_width=True,
        hide_index=True,
    )


st.subheader("Root-Cause Trend by Month")

root_trend = root_monthly.pivot(
    index="opened_month",
    columns="root_cause_category",
    values="event_count",
).fillna(0)

root_trend.index = pd.to_datetime(
    root_trend.index,
    format="%Y-%m",
)

root_trend = root_trend.sort_index()

fig, ax = plt.subplots(figsize=(12, 5))

for column in root_trend.columns:
    ax.plot(
        root_trend.index,
        root_trend[column],
        marker="o",
        linewidth=1.5,
        label=column,
    )

ax.set_ylabel("Quality Events")
ax.set_xlabel("")
ax.grid(axis="y", alpha=0.25)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.18),
    ncol=4,
    frameon=False,
)

fig.autofmt_xdate(rotation=45)

st.pyplot(fig)
plt.close(fig)

st.divider()


# ------------------------------------------------------------
# CAPA performance
# ------------------------------------------------------------

st.header("CAPA Performance")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total CAPAs",
        f"{len(capas)}",
    )

with c2:
    st.metric(
        "Overdue Open CAPAs",
        f"{int(open_capas['overdue'].sum())}",
    )

with c3:
    st.metric(
        "Effectiveness",
        f"{capa_effectiveness:.1f}%",
    )

capa_display = open_capas.sort_values(
    ["overdue", "opened_date"],
    ascending=[False, True],
)

capa_display = clean_table(
    capa_display,
    [
        "capa_id",
        "source",
        "opened_date",
        "due_date",
        "status",
        "effectiveness_result",
        "overdue",
        "cycle_days",
    ],
    date_columns=[
        "opened_date",
        "due_date",
    ],
)

st.dataframe(
    capa_display,
    use_container_width=True,
    hide_index=True,
)

st.divider()


# ------------------------------------------------------------
# Change management
# ------------------------------------------------------------

st.header("Change Management Performance")

change_counts = (
    changes["status"]
    .value_counts()
    .reindex(
        ["Closed", "Implemented", "In Progress"],
        fill_value=0,
    )
)

fig, ax = plt.subplots(figsize=(10, 4))

bars = ax.bar(
    change_counts.index,
    change_counts.values,
)

ax.bar_label(bars, padding=3)
ax.set_ylabel("Changes")
ax.set_xlabel("")
ax.set_title("Change Status")

st.pyplot(fig)
plt.close(fig)

m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        "Closed Changes",
        f"{int((changes['status'] == 'Closed').sum())}",
    )

with m2:
    st.metric(
        "Awaiting Follow-Up",
        f"{int((changes['status'] == 'Implemented').sum())}",
    )

with m3:
    st.metric(
        "High-Risk Not Closed",
        f"{high_risk_not_closed}",
    )

change_attention = changes[
    changes["status"] != "Closed"
].copy()

change_attention = change_attention.sort_values(
    ["status", "cycle_days"],
    ascending=[True, False],
)

change_display = clean_table(
    change_attention,
    [
        "change_id",
        "change_type",
        "submitted_date",
        "implemented_date",
        "status",
        "cycle_days",
        "risk_level",
        "verification_complete",
        "training_required",
        "training_complete_pct",
    ],
    date_columns=[
        "submitted_date",
        "implemented_date",
    ],
    percent_columns=[
        "training_complete_pct",
    ],
)

st.subheader("Changes Requiring Follow-Up")

st.dataframe(
    change_display,
    use_container_width=True,
    hide_index=True,
)

st.divider()


# ------------------------------------------------------------
# Organizational capability
# ------------------------------------------------------------

st.header("Training and Organizational Capability")

capability = training.sort_values(
    "coverage_pct",
    ascending=True,
).copy()

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.barh(
    capability["process"],
    capability["coverage_pct"],
)

ax.bar_label(
    bars,
    labels=[
        f"{value:.1f}%"
        for value in capability["coverage_pct"]
    ],
    padding=3,
)

ax.axvline(
    95,
    linestyle="--",
    linewidth=1.5,
    label="95% portfolio target",
)

ax.set_xlim(0, 110)
ax.set_xlabel("Coverage")
ax.set_ylabel("")
ax.set_title("Capability Coverage by QMS Process")
ax.legend(frameon=False)

st.pyplot(fig)
plt.close(fig)

training_display = clean_table(
    capability,
    [
        "process",
        "qualified_personnel",
        "required_coverage",
        "backup_personnel",
        "coverage_pct",
        "single_point_failure",
    ],
    percent_columns=["coverage_pct"],
)

st.dataframe(
    training_display,
    use_container_width=True,
    hide_index=True,
)

single_points = capability[
    capability["single_point_failure"]
].copy()

if len(single_points):
    st.subheader("Single-Point-of-Failure Exposure")

    st.warning(
        "CAPA currently meets its nominal staffing requirement, "
        "but the process has no qualified backup coverage. "
        "This creates an organizational resilience risk."
    )

    single_point_display = clean_table(
        single_points,
        [
            "process",
            "qualified_personnel",
            "required_coverage",
            "backup_personnel",
            "coverage_pct",
            "single_point_failure",
        ],
        percent_columns=["coverage_pct"],
    )

    st.dataframe(
        single_point_display,
        use_container_width=True,
        hide_index=True,
    )

st.divider()


# ------------------------------------------------------------
# Management review status
# ------------------------------------------------------------

st.header("Management Review Status")

st.dataframe(
    review_table(review),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "All records and KPI values shown in this dashboard are derived "
    "from synthetic portfolio data."
)