import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px
from statsmodels.stats.proportion import proportion_confint, proportions_ztest

st.set_page_config(
    page_title="Getaround Delay Analysis Dashboard",
    page_icon="🚗",
    layout="wide"
)

# -------------------
# LOAD DATA
# -------------------
@st.cache_data
def load_data():
    return pd.read_excel("data/get_around_delay_analysis.xlsx")

df = load_data()
df_problem = df.copy()
df_problem = df_problem[(df_problem["delay_at_checkout_in_minutes"] >= -1440) & (df_problem["delay_at_checkout_in_minutes"] <= 4320)]
df_problem["problem_case"] = (df_problem["delay_at_checkout_in_minutes"] > df_problem["time_delta_with_previous_rental_in_minutes"])
df_problem = df_problem[
df_problem["time_delta_with_previous_rental_in_minutes"].notna()
]
# -------------------
# SIDEBAR
# -------------------
st.sidebar.title("🚗 Getaround Dashboard")
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Revenue Impact", "Threshold Simulation", "Late Checkout Analysis"]
)

scope = st.sidebar.selectbox(
    "Scope",
    ["All cars", "Connect only"]
)

threshold = st.sidebar.slider(
    "Minimum delay threshold (minutes)",
    min_value=0,
    max_value=180,
    value=60,
    step=15
)
if scope == "Connect only":
    df_scope = df_problem[df_problem["checkin_type"] == "connect"].copy()
else:
    df_scope = df_problem.copy()

df_threshold = df_scope[
    df_scope["time_delta_with_previous_rental_in_minutes"] < threshold
]

# -------------------
# HEADER
# -------------------
st.title("🚗 Getaround Delay Analysis Dashboard")
st.markdown(
    "Explore how minimum delay thresholds impact rentals, late checkouts and owner revenue."
)

# -------------------
# OVERVIEW PAGE
# -------------------
if page == "Overview":
    st.header("Overview")
    
    if scope == "Connect only":
        df_scope = df_problem[df_problem["checkin_type"] == "connect"].copy()
    else:
        df_scope = df_problem.copy()

    df_threshold = df_scope[
        df_scope["time_delta_with_previous_rental_in_minutes"] < threshold
    ]
    
    total_rentals = len(df_scope)

    median_delay = df_scope["delay_at_checkout_in_minutes"].median()

    late_checkouts = (df_scope["delay_at_checkout_in_minutes"] > 0).mean()

    conflicts_solved = df_threshold["problem_case"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total rentals", len(df))
    col2.metric("Median delay", f"{df['delay_at_checkout_in_minutes'].median():.0f} min")
    col3.metric("Late checkouts", f"{(df['delay_at_checkout_in_minutes'] > 0).mean()*100:.1f}%")
    col4.metric("Conflicts solved", conflicts_solved)
    

    st.subheader("Checkin Type vs Conflict")

    # Same logic as notebook
    df_delay = df[df["state"] == "ended"].copy()
    df_delay = df_delay[df_delay["delay_at_checkout_in_minutes"].notna()]

    df_delay_analysis = df_delay.copy()
    df_delay_analysis["problem_case"] = (
        df_delay_analysis["delay_at_checkout_in_minutes"]
        > df_delay_analysis["time_delta_with_previous_rental_in_minutes"]
    )

    checkin_types = df_delay_analysis["checkin_type"].unique().tolist()
    conflict_states = ["Conflict", "No Conflict"]

    nodes = checkin_types + conflict_states
    node_map = {label: i for i, label in enumerate(nodes)}

    df_links = df_delay_analysis.copy()
    df_links["conflict_label"] = df_links["problem_case"].apply(
        lambda x: "Conflict" if x else "No Conflict"
    )

    link_counts = (
        df_links.groupby(["checkin_type", "conflict_label"])
        .size()
        .reset_index(name="count")
    )

    link_counts["source"] = link_counts["checkin_type"].map(node_map)
    link_counts["target"] = link_counts["conflict_label"].map(node_map)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes
        ),
        link=dict(
            source=link_counts["source"],
            target=link_counts["target"],
            value=link_counts["count"]
        )
    )])

    fig.update_layout(title_text="Checkin Type vs Conflict", font_size=12)

    st.plotly_chart(fig, use_container_width=True)

# -------------------
# REVENUE IMPACT PAGE
# -------------------
elif page == "Revenue Impact":
    st.header("Revenue Impact")

    st.markdown(
        f"""
        Estimated impact of the minimum delay policy for:
        - **Scope:** {scope}
        - **Threshold:** {threshold} minutes
        """
    )

    # -------------------
    # CORE METRICS
    # -------------------

    total_rentals = len(df_scope)

    blocked_rentals = df_threshold.shape[0]

    share_affected = blocked_rentals / total_rentals

    conflicts_solved = df_threshold["problem_case"].sum()

    # -------------------
    # DISPLAY KPIs
    # -------------------

    col1, col2 = st.columns(2)

    col1.metric(
        "Rentals potentially impacted",
        blocked_rentals
    )

    col2.metric(
        "Share of impacted rentals",
        f"{share_affected:.1%}"
    )

    st.markdown("---")

    # -------------------
    # INTERPRETATION BLOCK
    # -------------------

    st.subheader("Interpretation")

    st.markdown(
        f"""
        With a **{threshold}-minute threshold**, approximately
        **{share_affected:.1%} of rentals** would be impacted
        under the selected scope (**{scope}**).

        This represents the operational trade-off between:
        - reducing late checkout conflicts
        - and potentially restricting booking availability
        """
    )

    # -------------------
    # OPTIONAL BREAKDOWN
    # -------------------

    col3, col4 = st.columns(2)

    col3.metric(
        "Conflicts solved",
        conflicts_solved
    )

    col4.metric(
        "Net usable rentals",
        total_rentals - blocked_rentals
    )


# -------------------
# THRESHOLD SIMULATION
# -------------------
elif page == "Threshold Simulation":
    st.header("Threshold Simulation")

    st.markdown(
        "Evaluate the tradeoff between operational reliability and booking availability."
    )

    # -------------------
    # QUICK SUMMARY TABLE
    # -------------------
    threshold_summary = [60, 30, 20]
    summary_results = []
    df_problem = df.copy()
    df_problem = df_problem[(df_problem["delay_at_checkout_in_minutes"] >= -1440) & (df_problem["delay_at_checkout_in_minutes"] <= 4320)]
    df_problem["problem_case"] = (df_problem["delay_at_checkout_in_minutes"] > df_problem["time_delta_with_previous_rental_in_minutes"])
    df_problem = df_problem[
    df_problem["time_delta_with_previous_rental_in_minutes"].notna()
    ]
    for t in threshold_summary:
        df_threshold = df_problem[
            df_problem["time_delta_with_previous_rental_in_minutes"] < t
        ]

        conflicts = df_threshold["problem_case"].sum()
        no_conflicts = len(df_threshold) - conflicts

        summary_results.append({
            "Threshold (min)": t,
            "Conflicts solved": conflicts,
            "Rentals blocked": no_conflicts
        })

    df_summary = pd.DataFrame(summary_results)

    st.subheader("Key threshold scenarios")
    st.dataframe(df_summary, use_container_width=True)

    # -------------------
    # FULL THRESHOLD CURVE
    # -------------------
    thresholds = [60, 50, 40, 31, 30, 20]
    results = []
    df_problem = df.copy()
    df_problem = df_problem[(df_problem["delay_at_checkout_in_minutes"] >= -1440) & (df_problem["delay_at_checkout_in_minutes"] <= 4320)]
    df_problem["problem_case"] = (df_problem["delay_at_checkout_in_minutes"] > df_problem["time_delta_with_previous_rental_in_minutes"])
    df_problem = df_problem[
    df_problem["time_delta_with_previous_rental_in_minutes"].notna()
    ]

    for t in thresholds:
        df_thresh = df_problem[
            df_problem["time_delta_with_previous_rental_in_minutes"] < t
        ]

        conflicts = df_thresh["problem_case"].sum()
        blocked = len(df_thresh) - conflicts

        results.append({
            "threshold": t,
            "conflicts_solved": conflicts,
            "rentals_blocked": blocked
        })

    df_results = pd.DataFrame(results)

    st.subheader("Conflicts solved vs rentals blocked")

    fig = px.line(
        df_results,
        x="threshold",
        y=["conflicts_solved", "rentals_blocked"],
        markers=True,
        title="Threshold Simulation: Conflicts Solved vs Rentals Blocked",
        labels={
            "value": "Number of Rentals",
            "threshold": "Minimum Delay Threshold (minutes)",
            "variable": "Metric"
        }
    )

    fig.update_layout(xaxis=dict(autorange="reversed"))

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Higher thresholds solve more operational conflicts but also block more bookings. "
        "This helps identify the point where operational gains begin to flatten relative to booking loss."
    )


# -------------------
# LATE CHECKOUT ANALYSIS
# -------------------
elif page == "Late Checkout Analysis":
    st.header("Late Checkout Analysis")

    df_delay = df[df["state"] == "ended"].copy()
    df_delay = df_delay[df_delay["delay_at_checkout_in_minutes"].notna()]

    df_delay = df_delay[
        (df_delay["delay_at_checkout_in_minutes"] >= -1440) &
        (df_delay["delay_at_checkout_in_minutes"] <= 4320)
    ]

    late = df_delay[df_delay["delay_at_checkout_in_minutes"] > 0].copy()
    early = df_delay[df_delay["delay_at_checkout_in_minutes"] < 0].copy()

    late["delay_hours"] = late["delay_at_checkout_in_minutes"] / 60
    col1, col2 = st.columns(2)
    col1.metric("Late checkouts", len(late))
    col2.metric("Average late delay", f"{late['delay_hours'].mean():.1f} h")

    st.subheader("Distribution of late checkout delays")

    fig = px.histogram(
        late,
        x="delay_hours",
        nbins=30,
        title="Late checkout delay distribution",
        labels={"delay_hours": "Delay at checkout (hours)"}
    )

    st.plotly_chart(fig, use_container_width=True)


    st.subheader("Conflict Rate Analysis")
    
    results = []
    df_problem = df.copy()
    df_problem = df_problem[(df_problem["delay_at_checkout_in_minutes"] >= -1440) & (df_problem["delay_at_checkout_in_minutes"] <= 4320)]
    df_problem["problem_case"] = (df_problem["delay_at_checkout_in_minutes"] > df_problem["time_delta_with_previous_rental_in_minutes"])
    df_problem = df_problem[
    df_problem["time_delta_with_previous_rental_in_minutes"].notna()
    ]

    conflicts = df_problem["problem_case"].sum()
    n = len(df_problem)

    p = conflicts / n
    ci_low, ci_high = proportion_confint(conflicts, n, method="wilson")
    se = np.sqrt(p * (1 - p) / n)

    stat, pval = proportions_ztest(conflicts, n, value=0.10)

    col1, col2, col3 = st.columns(3)
    col1.metric("Conflict rate", f"{p:.1%}")
    col2.metric("95% CI", f"[{ci_low:.1%}, {ci_high:.1%}]")
    col3.metric("Standard error", f"{se:.3f}")

    st.markdown("### Hypothesis test")
    st.markdown(
        f"""
     - **Null hypothesis (H₀):** conflict rate = 10%  
     - **Observed conflict rate:** {p:.1%}  
     - **Z-statistic:** {stat:.2f}  
     - **P-value:** {pval:.2e}
        """
    )

    if pval < 0.05:
        st.success("The observed conflict rate is statistically significantly different from 10%.")
    else:
        st.info("The observed conflict rate is not statistically different from 10%.")
        st.subheader("Impact on next driver")
