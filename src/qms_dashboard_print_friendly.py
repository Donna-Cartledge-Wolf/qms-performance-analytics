from pathlib import Path

import matplotlib.pyplot as plt
import html
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

# Add ?view=report to the dashboard URL for the GoFullPage-friendly view.
# The original interactive dashboard is unchanged when this query is absent.
REPORT_MODE = st.query_params.get("view", "").lower() == "report"

# ------------------------------------------------------------
# Presentation styling
# ------------------------------------------------------------

# Typography system: one clear hierarchy across Streamlit and Matplotlib.
# Section titles use Streamlit/CSS. Chart text uses one shared body size.
CHART_BODY_SIZE = 11

plt.rcParams.update({
    "font.size": CHART_BODY_SIZE,
    "axes.labelsize": CHART_BODY_SIZE,
    "xtick.labelsize": CHART_BODY_SIZE,
    "ytick.labelsize": CHART_BODY_SIZE,
    "legend.fontsize": CHART_BODY_SIZE,
})

st.markdown(
    """
    <style>
    :root {
        --wa-title-size: 30px;
        --wa-section-size: 22px;
        --wa-subsection-size: 18px;
        --wa-body-size: 14px;
        --wa-caption-size: 13px;
        --wa-metric-value-size: 26px;
    }

    h1 {
        font-size: var(--wa-title-size) !important;
        line-height: 1.18 !important;
        margin-bottom: 0.35rem !important;
    }
    h2 {
        font-size: var(--wa-section-size) !important;
        line-height: 1.22 !important;
        margin-top: 0.9rem !important;
        margin-bottom: 0.55rem !important;
    }
    h3 {
        font-size: var(--wa-subsection-size) !important;
        line-height: 1.22 !important;
        margin-top: 0.7rem !important;
        margin-bottom: 0.4rem !important;
    }

    /* One body-text size everywhere outside intentional KPI values. */
    p, li, label,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMetricLabel"] p,
    [data-testid="stAlert"] p {
        font-size: var(--wa-body-size) !important;
        line-height: 1.42 !important;
    }

    [data-testid="stCaptionContainer"] p {
        font-size: var(--wa-caption-size) !important;
        line-height: 1.38 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: var(--wa-metric-value-size) !important;
        line-height: 1.1 !important;
    }

    /* Keep dataframe text visually aligned with dashboard body copy. */
    [data-testid="stDataFrame"] {
        font-size: var(--wa-body-size) !important;
    }
    [data-testid="stDataFrame"] * {
        font-size: var(--wa-body-size) !important;
    }

    /* All chart titles use the same Streamlit-rendered typography. */
    .chart-title {
        font-size: var(--wa-subsection-size);
        line-height: 1.22;
        font-weight: 600;
        text-align: center;
        margin: 0.15rem 0 0.45rem 0;
    }

    @media print {
        :root {
            --wa-title-size: 22pt;
            --wa-section-size: 16pt;
            --wa-subsection-size: 13pt;
            --wa-body-size: 10.5pt;
            --wa-caption-size: 9.5pt;
            --wa-metric-value-size: 18pt;
        }
        .print-page-break {
            break-before: page;
            page-break-before: always;
        }
        h1, h2, h3, .chart-title {
            break-after: avoid-page;
            page-break-after: avoid;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
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
    "high_risk": "High Risk",
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

# Use the square, full-logo artwork for the PDF report, while leaving
# the existing branding unchanged in the interactive dashboard.
if REPORT_MODE:
    logo_path = ASSETS / "Wolf_Analytics_Logo_Report.png"
    if not logo_path.exists():
        logo_path = ASSETS / "Wolf_Analytics_Logo.png"
else:
    logo_path = ASSETS / "Wolf_Analytics_Logo.png"

if logo_path.exists():
    left, center, right = st.columns([1, 1, 1])
    with center:
        # The image is square and includes built-in whitespace: show it
        # at its original aspect ratio rather than trimming or stretching.
        st.image(str(logo_path), width=210 if REPORT_MODE else 230)

if not REPORT_MODE:
    st.markdown(
        '<div style="text-align:right; font-size:14px;">'
        '<a href="?view=report" target="_self">'
        'Open PDF-friendly management review ↗</a></div>',
        unsafe_allow_html=True,
    )

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
# Optional full-width PDF report view (GoFullPage or Chrome Print)
# ------------------------------------------------------------

if REPORT_MODE:
    # GoFullPage captures screen styles, not @media print styles. Therefore
    # the report uses larger on-screen type and fixed, full-row HTML tables.
    # Chrome's native Print > Save as PDF additionally respects page breaks.
    st.markdown(
        """
        <style>
        /* Keep the report centered without wasting most of the page width. */
        [data-testid="stMainBlockContainer"], .block-container {
            max-width: 1420px !important;
            padding-top: 5rem !important;
            padding-bottom: 1.2rem !important;
        }
        :root {
            --wa-title-size: 34px;
            --wa-section-size: 28px;
            --wa-subsection-size: 23px;
            --wa-body-size: 19px;
            --wa-caption-size: 17px;
            --wa-metric-value-size: 33px;
        }
        h1 { font-weight: 700 !important; }
        h2 { margin-top: 0.9rem !important; margin-bottom: 0.4rem !important; }
        p, li { line-height: 1.38 !important; }
        .wa-report-table {
            border-collapse: collapse;
            border-spacing: 0;
            width: 100%;
            table-layout: auto;
            margin: 0.3rem 0 1.2rem;
            background: white;
        }
        .wa-report-table th, .wa-report-table td {
            font-size: 18px !important;
            line-height: 1.3 !important;
            padding: 9px 11px !important;
            border: 1px solid #d7e0e8 !important;
            color: #24354a;
            vertical-align: top;
            overflow-wrap: anywhere;
            text-align: left;
        }
        .wa-report-table thead th {
            font-weight: 700;
            background: #eaf0f6;
            color: #16395c;
        }
        .wa-report-table tbody tr:nth-child(even) {
            background: #f8fafc;
        }
        .wa-kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0,1fr));
            gap: 14px;
            margin: 0.4rem 0 1rem;
        }
        .wa-kpi-card {
            border: 1px solid #d7e0e8;
            border-radius: 6px;
            padding: 13px 14px;
            background: #f7faff;
        }
        .wa-kpi-label {
            font-size: 18px;
            color: #3b526b;
            line-height: 1.25;
        }
        .wa-kpi-value {
            color: #103c63;
            font-weight: 750;
            font-size: 32px;
            line-height: 1.25;
            margin-top: 6px;
        }
        .wa-kpi-note { font-size: 16px; color: #4b6175; }
        .wa-alerts { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
        .wa-alert {
            border-radius: 6px;
            font-size: 19px;
            padding: 14px 16px;
            line-height: 1.4;
        }
        .wa-attention { background: #fff5d9; color: #714a00; }
        .wa-pass { background: #e6f6ec; color: #185d3a; }
        .wa-section-label {
            font-size: 21px;
            font-weight: 650;
            margin: 12px 0 6px;
            color: #16395c;
        }
        /* Never cap the image height globally: that cropped/shrank the logo
           and also made Matplotlib charts tiny in the exported PDF. */
        [data-testid="stImage"] { margin-top: 0 !important; }
        [data-testid="stImage"] img {
            max-height: none !important;
            height: auto !important;
            object-fit: contain;
        }
        [data-testid="stVerticalBlock"] { gap: 0.55rem; }
        .wa-report-footer { font-size: 17px; color: #53657a; margin: 12px 0; }
        @media (max-width: 800px) {
            .wa-kpi-grid { grid-template-columns: repeat(2, minmax(0,1fr)); }
            .wa-alerts { grid-template-columns: 1fr; }
        }
        @media print {
            @page { size: landscape; margin: 12mm; }
            [data-testid="stHeader"], [data-testid="stToolbar"],
            [data-testid="stDecoration"], footer { display: none !important; }
            .wa-kpi-card, .wa-alert, tr, figure { break-inside: avoid; }
            h2, h3 { break-after: avoid; }
            .wa-report-table thead { display: table-header-group; }
            [data-testid="stMainBlockContainer"], .block-container {
                max-width: none !important;
            }
            .wa-report-table th, .wa-report-table td {
                font-size: 11pt !important;
                padding: 4pt 5pt !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def report_table(df: pd.DataFrame) -> None:
        """Display every row as regular HTML, not a scrolling Streamlit grid."""
        visible = df.copy().fillna("")
        for column in visible.columns:
            # Explicitly label booleans; no tiny checkboxes in a PDF.
            if pd.api.types.is_bool_dtype(df[column]):
                visible[column] = df[column].map({True: "Yes", False: "No"})
            else:
                visible[column] = visible[column].map(
                    lambda value: "Yes" if value is True else
                    ("No" if value is False else value)
                )
        st.markdown(
            visible.to_html(
                index=False,
                escape=True,
                classes="wa-report-table",
                border=0,
            ),
            unsafe_allow_html=True,
        )

    def report_kpis(items: list[tuple[str, str, str]]) -> None:
        cards = "".join(
            '<div class="wa-kpi-card">'
            f'<div class="wa-kpi-label">{html.escape(label)}</div>'
            f'<div class="wa-kpi-value">{html.escape(str(value))}</div>'
            f'<div class="wa-kpi-note">{html.escape(note)}</div>'
            '</div>'
            for label, value, note in items
        )
        st.markdown(
            '<div class="wa-kpi-grid">' + cards + '</div>',
            unsafe_allow_html=True,
        )

    def report_label(title: str) -> None:
        st.markdown(
            f'<div class="wa-section-label">{html.escape(title)}</div>',
            unsafe_allow_html=True,
        )

    def report_divider() -> None:
        st.divider()

    action_items = review[review["status"] == "ACTION"].copy()
    pass_items = review[review["status"] == "PASS"].copy()

    st.header("Management Priorities")
    st.markdown(
        '<div class="wa-alerts">'
        f'<div class="wa-alert wa-attention">{len(action_items)} KPI areas currently '
        'require management action.</div>'
        f'<div class="wa-alert wa-pass">{len(pass_items)} KPI areas currently '
        'meet the portfolio target.</div></div>',
        unsafe_allow_html=True,
    )
    if len(action_items):
        report_table(review_table(action_items))
    report_divider()

    st.header("Executive KPI Overview")
    report_kpis([
        ("Open Quality Events", str(len(open_qe)), ""),
        ("Overdue Open Events", str(int(open_qe["overdue"].sum())),
         f"{open_qe['overdue'].mean()*100:.1f}% of open quality events"),
        ("High-Risk Open Events", str(int(open_qe["high_risk"].sum())), ""),
        ("Open CAPAs", str(len(open_capas)),
         f"{int(open_capas['overdue'].sum())} currently overdue"),
        ("CAPA Effectiveness", f"{capa_effectiveness:.1f}%", ""),
        ("Median Change Cycle", f"{median_change_cycle:.0f} days", ""),
        ("Mean Capability Coverage", f"{mean_training_coverage:.1f}%", ""),
        ("Single-Point Failures", str(single_point_failures), ""),
    ])
    report_divider()

    st.header("Quality Event Aging and Risk")
    risk_events = open_qe[
        open_qe["overdue"] | open_qe["high_risk"]
    ].copy().sort_values(
        ["high_risk", "overdue", "age_days"],
        ascending=[False, False, False],
    )
    risk_display = clean_table(risk_events, [
        "event_id", "event_type", "severity", "root_cause_category",
        "age_days", "target_days", "overdue", "high_risk",
    ])
    report_table(risk_display)
    report_divider()

    st.header("Root-Cause Frequency and Risk")
    report_label("Quality Events by Root-Cause Category")
    plot_data = root_summary.sort_values("total_events")
    fig, ax = plt.subplots(figsize=(11, 5.3))
    bars = ax.barh(plot_data["root_cause_category"], plot_data["total_events"])
    ax.bar_label(bars, padding=4, fontsize=15)
    ax.set_xlabel("Quality Events", fontsize=15)
    ax.tick_params(axis="both", labelsize=14)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    report_label("Root-Cause Category Summary")
    report_table(clean_table(root_summary, [
        "root_cause_category", "total_events", "open_events",
        "overdue_events", "high_risk_open_events", "frequency_pct",
    ], percent_columns=["frequency_pct"]))

    report_label("Root-Cause Trend by Month")
    root_trend = root_monthly.pivot(
        index="opened_month",
        columns="root_cause_category",
        values="event_count",
    ).fillna(0)
    root_trend.index = pd.to_datetime(root_trend.index, format="%Y-%m")
    root_trend = root_trend.sort_index()
    fig, ax = plt.subplots(figsize=(11.8, 5.4))
    for column in root_trend.columns:
        ax.plot(root_trend.index, root_trend[column], marker="o",
                linewidth=1.8, markersize=5, label=column)
    ax.set_ylabel("Quality Events", fontsize=15)
    ax.tick_params(axis="both", labelsize=13)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20),
              ncol=4, frameon=False, fontsize=13)
    fig.autofmt_xdate(rotation=35)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    report_divider()

    st.header("CAPA Performance")
    report_kpis([
        ("Total CAPAs", str(len(capas)), ""),
        ("Overdue Open CAPAs", str(int(open_capas["overdue"].sum())), ""),
        ("Effectiveness", f"{capa_effectiveness:.1f}%", ""),
    ])
    capa_display = open_capas.sort_values(
        ["overdue", "opened_date"], ascending=[False, True]
    )
    capa_display = clean_table(capa_display, [
        "capa_id", "source", "opened_date", "due_date", "status",
        "effectiveness_result", "overdue", "cycle_days",
    ], date_columns=["opened_date", "due_date"])
    report_label("Open CAPAs")
    report_table(capa_display)
    report_divider()

    st.header("Change Management Performance")
    change_counts = changes["status"].value_counts().reindex(
        ["Closed", "Implemented", "In Progress"], fill_value=0,
    )
    report_label("Change Status")
    fig, ax = plt.subplots(figsize=(10.8, 4.6))
    bars = ax.bar(change_counts.index, change_counts.values)
    ax.bar_label(bars, padding=4, fontsize=15)
    ax.set_ylabel("Changes", fontsize=15)
    ax.tick_params(axis="both", labelsize=14)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    report_kpis([
        ("Closed Changes", str(int((changes["status"] == "Closed").sum())), ""),
        ("Awaiting Follow-Up",
         str(int((changes["status"] == "Implemented").sum())), ""),
        ("High-Risk Not Closed", str(high_risk_not_closed), ""),
    ])
    change_attention = changes[
        changes["status"] != "Closed"
    ].copy().sort_values(["status", "cycle_days"], ascending=[True, False])
    change_display = clean_table(change_attention, [
        "change_id", "change_type", "submitted_date", "implemented_date",
        "status", "cycle_days", "risk_level", "verification_complete",
        "training_required", "training_complete_pct",
    ], date_columns=["submitted_date", "implemented_date"],
        percent_columns=["training_complete_pct"])
    report_label("Changes Requiring Follow-Up")
    # Split the wide 10-column table into two readable, matching tables.
    report_label("Change Status and Risk")
    report_table(change_display[[
        "Change ID", "Change Type", "Status", "Cycle, Days", "Risk Level",
    ]])
    report_label("Implementation and Training Readiness")
    report_table(change_display[[
        "Change ID", "Submitted Date", "Implemented Date",
        "Verification Complete", "Training Required", "Training Complete",
    ]])
    report_divider()

    st.header("Training and Organizational Capability")
    capability = training.sort_values("coverage_pct", ascending=True).copy()
    report_label("Capability Coverage by QMS Process")
    fig, ax = plt.subplots(figsize=(11.5, 5.3))
    bars = ax.barh(capability["process"], capability["coverage_pct"])
    ax.bar_label(bars, labels=[f"{x:.1f}%" for x in capability["coverage_pct"]],
                 padding=4, fontsize=15)
    ax.axvline(95, linestyle="--", linewidth=1.6,
               label="95% portfolio target")
    ax.set_xlim(0, 110)
    ax.set_xlabel("Coverage", fontsize=15)
    ax.tick_params(axis="both", labelsize=14)
    ax.legend(frameon=False, fontsize=14)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    training_display = clean_table(capability, [
        "process", "qualified_personnel", "required_coverage",
        "backup_personnel", "coverage_pct", "single_point_failure",
    ], percent_columns=["coverage_pct"])
    report_table(training_display)

    single_points = capability[capability["single_point_failure"]].copy()
    if len(single_points):
        st.subheader("Single-Point-of-Failure Exposure")
        st.warning(
            "CAPA currently meets its nominal staffing requirement, "
            "but the process has no qualified backup coverage. "
            "This creates an organizational resilience risk."
        )
        report_table(clean_table(single_points, [
            "process", "qualified_personnel", "required_coverage",
            "backup_personnel", "coverage_pct", "single_point_failure",
        ], percent_columns=["coverage_pct"]))
    report_divider()

    st.header("Management Review Status")
    report_table(review_table(review))
    st.markdown(
        '<div class="wa-report-footer">All records and KPI values shown '
        'in this management review are derived from synthetic portfolio data. '
        'Scenario targets are not industry benchmarks.</div>',
        unsafe_allow_html=True,
    )
    st.stop()  # Do not render the interactive dashboard underneath.


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
        width="stretch",
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
    width="stretch",
    hide_index=True,
)

st.divider()


# ------------------------------------------------------------
# Root-cause frequency and risk
# ------------------------------------------------------------

# Keep this section heading with its content when printing to PDF.
st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
st.header("Root-Cause Frequency and Risk")

root_outer_left, root_center, root_outer_right = st.columns([0.35, 5, 0.35])

with root_center:
    root_chart_col, root_table_col = st.columns([1.15, 1])

    with root_chart_col:
        plot_data = root_summary.sort_values("total_events")

        fig, ax = plt.subplots(figsize=(6.3, 3.8))

        bars = ax.barh(
            plot_data["root_cause_category"],
            plot_data["total_events"],
        )

        ax.bar_label(bars, padding=3, fontsize=CHART_BODY_SIZE)
        ax.set_xlabel("Quality Events", fontsize=CHART_BODY_SIZE)
        ax.set_ylabel("")
        ax.tick_params(axis="both", labelsize=CHART_BODY_SIZE)

        st.markdown(
            '<div class="chart-title">Quality Events by Root-Cause Category</div>',
            unsafe_allow_html=True,
        )
        st.pyplot(fig)
        plt.close(fig)

    with root_table_col:
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
            width="stretch",
            hide_index=True,
        )

st.markdown(
    '<div class="chart-title">Root-Cause Trend by Month</div>',
    unsafe_allow_html=True,
)

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

fig, ax = plt.subplots(figsize=(8, 3.6))

for column in root_trend.columns:
    ax.plot(
        root_trend.index,
        root_trend[column],
        marker="o",
        linewidth=1.4,
        markersize=4,
        label=column,
    )

ax.set_ylabel("Quality Events", fontsize=CHART_BODY_SIZE)
ax.set_xlabel("")
ax.tick_params(axis="both", labelsize=CHART_BODY_SIZE)
ax.grid(axis="y", alpha=0.25)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.20),
    ncol=4,
    frameon=False,
    fontsize=CHART_BODY_SIZE,
)

fig.autofmt_xdate(rotation=45)
fig.tight_layout()

trend_left, trend_center, trend_right = st.columns([1, 3.4, 1])

with trend_center:
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
    width="stretch",
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

fig, ax = plt.subplots(figsize=(6.5, 3.1))

bars = ax.bar(
    change_counts.index,
    change_counts.values,
)

ax.bar_label(bars, padding=3, fontsize=CHART_BODY_SIZE)
ax.set_ylabel("Changes", fontsize=CHART_BODY_SIZE)
ax.set_xlabel("")
ax.tick_params(axis="both", labelsize=CHART_BODY_SIZE)
fig.tight_layout()

change_left, change_center, change_right = st.columns([1, 2.5, 1])

with change_center:
    st.markdown(
        '<div class="chart-title">Change Status</div>',
        unsafe_allow_html=True,
    )
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
    width="stretch",
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

fig, ax = plt.subplots(figsize=(8, 4))

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
    fontsize=CHART_BODY_SIZE,
)

ax.axvline(
    95,
    linestyle="--",
    linewidth=1.5,
    label="95% portfolio target",
)

ax.set_xlim(0, 110)
ax.set_xlabel("Coverage", fontsize=CHART_BODY_SIZE)
ax.set_ylabel("")
ax.tick_params(axis="both", labelsize=CHART_BODY_SIZE)
ax.legend(frameon=False, fontsize=CHART_BODY_SIZE)
fig.tight_layout()

cap_left, cap_center, cap_right = st.columns([1, 4, 1])

with cap_center:
    st.markdown(
        '<div class="chart-title">Capability Coverage by QMS Process</div>',
        unsafe_allow_html=True,
    )
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
    width="stretch",
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
        width="stretch",
        hide_index=True,
    )

st.divider()


# ------------------------------------------------------------
# Management review status
# ------------------------------------------------------------

st.header("Management Review Status")

st.dataframe(
    review_table(review),
    width="stretch",
    hide_index=True,
)

st.caption(
    "All records and KPI values shown in this dashboard are derived "
    "from synthetic portfolio data."
)
