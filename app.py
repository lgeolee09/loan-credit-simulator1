import io
import textwrap
from datetime import date

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Maybank One | Finance Planner",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --navy:#111111; --deep:#080808; --gold:#ffd400; --silver:#c7cbd0; --ink:#171717; --muted:#667085; --line:#c6cbd1; }
    html, body, [class*="css"] { font-family:'DM Sans', sans-serif; }
    h1, h2, h3 { font-family:'Space Grotesk', sans-serif; color:#ffffff; }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background:#050505 !important; color:#f4f4f4 !important; }
    [data-testid="stToolbar"] { background:#050505 !important; }
    @keyframes page-enter { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
    @keyframes card-enter { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
    .main .block-container { background:#050505; box-shadow:0 0 0 1px #222222, 0 18px 50px rgba(0,0,0,.55); padding-top:2.2rem; animation:page-enter .65s ease-out both; }
    [data-testid="stMarkdownContainer"] p, [data-testid="stCaptionContainer"] { color:#f4f4f4; }
    [data-testid="stSidebar"] { background:var(--deep); }
    [data-testid="stSidebar"] * { color:#eef4f8 !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div, [data-testid="stSidebar"] input { background:#1d1d1d !important; border-color:#4a4a4a !important; }
    .brand { padding:8px 0 24px; border-bottom:1px solid #353535; margin-bottom:24px; }
    .fake-logo { display:flex; align-items:center; gap:10px; color:#ffffff; font:700 25px 'Space Grotesk',sans-serif; letter-spacing:-1.2px; }
    .fake-logo-badge { width:34px; height:34px; display:grid; place-items:center; background:var(--gold); color:#111111; font:700 22px 'Space Grotesk',sans-serif; transform:skew(-8deg); box-shadow:4px 4px 0 #ffffff; }
    .fake-logo-note { color:#909090; font-size:10px; letter-spacing:1.3px; text-transform:uppercase; margin:7px 0 0 44px; }
    .hero { background:linear-gradient(125deg,#050505 0%,#191919 57%,#5a4a00 100%); color:white; padding:34px 40px; border-radius:4px; margin-bottom:22px; position:relative; overflow:hidden; border:1px solid #111111; border-bottom:6px solid var(--gold); box-shadow:10px 10px 0 rgba(255,212,0,.82), 0 18px 28px rgba(0,0,0,.24); }
    .hero:after { content:''; position:absolute; width:330px; height:330px; border:2px solid rgba(255,212,0,.54); border-radius:50%; right:-65px; top:-145px; box-shadow:0 0 32px rgba(255,212,0,.32); }
    .hero h1 { color:white; font-size:clamp(28px,4vw,46px); margin:0; letter-spacing:-1.5px; }
    .hero p { color:#d6e3ec; max-width:680px; margin:12px 0 0; font-size:16px; }
    .eyebrow, .section-label { color:var(--gold); text-transform:uppercase; letter-spacing:1.5px; font-weight:700; font-size:11px; }
    .section-label { color:var(--gold); margin:18px 0 8px; }
    .metric-card { background:#171717; border:1px solid #444444; border-top:4px solid var(--gold); padding:18px 20px; min-height:112px; box-shadow:5px 5px 0 #000000, 0 7px 18px rgba(0,0,0,.32); animation:card-enter .55s ease-out both; }
    .metric-card .metric-title, .metric-card .metric-value { color:#ffffff; }
    .metric-card .metric-note { color:#c7cbd0; }
    .metric-title { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.7px; }
    .metric-value { color:var(--navy); font:700 25px 'Space Grotesk',sans-serif; margin-top:9px; }
    .metric-note { color:var(--muted); font-size:12px; margin-top:3px; }
    .info-strip { background:#171717; border:1px solid #4b4b4b; border-left:4px solid var(--gold); padding:12px 16px; color:#ffffff; font-size:13px; margin:12px 0 20px; }
    .package-card { background:linear-gradient(145deg,#1b1b1b 0%,#0d0d0d 100%); border:1px solid #4b4b4b; padding:20px; height:100%; box-shadow:6px 6px 0 #000000; }
    .package-card h3 { color:#ffffff; margin:8px 0 6px; font-size:20px; }
    .package-type { color:var(--gold); text-transform:uppercase; font-weight:700; font-size:11px; letter-spacing:1.2px; }
    .package-rate { color:var(--gold); font:700 29px 'Space Grotesk',sans-serif; margin:16px 0 4px; }
    .package-detail { color:#d7d7d7; font-size:13px; line-height:1.6; }
    .chat-user { background:#111111; color:white; padding:11px 14px; margin:10px 0 8px 12%; border-radius:4px; border-left:4px solid var(--gold); }
    .chat-bot { background:#171717; border:1px solid #4b4b4b; color:#ffffff; padding:13px 15px; margin:0 12% 8px 0; border-radius:4px; line-height:1.55; }
    .chat-bot strong, .chat-bot p { color:#ffffff; }
    .chart-guide { color:#ffffff; background:#171717; border-left:4px solid var(--gold); padding:12px 16px; margin:10px 0 14px; font-size:13px; line-height:1.55; }
    .chart-detail { color:#ffffff; background:#171717; border:1px solid var(--gold); border-left:6px solid var(--gold); padding:16px 18px; margin:12px 0 20px; box-shadow:5px 5px 0 #000000; line-height:1.55; }
    .chart-detail strong { color:var(--gold); }
    .stExpander, [data-testid="stDataFrame"] { color:#ffffff; background:#171717; }
    [data-testid="stExpander"] details, [data-testid="stExpander"] summary { background:#171717 !important; color:#ffffff !important; border-color:#4b4b4b !important; }
    [data-testid="stDataFrame"] div { color:#ffffff !important; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:2px solid #111111; }
    .stTabs [data-baseweb="tab"] { color:#ffffff; font-weight:700; }
    .stTabs [aria-selected="true"] { color:var(--gold) !important; border-bottom-color:var(--gold) !important; }
    .stButton > button, .stDownloadButton > button { background:#111111; color:#ffffff; border:1px solid #111111; box-shadow:4px 4px 0 var(--gold); border-radius:2px; }
    .stButton > button:hover, .stDownloadButton > button:hover { background:var(--gold); color:#111111; border-color:#111111; }
    .fine-print { color:#c7cbd0; font-size:11px; line-height:1.5; }
    </style>
    """,
    unsafe_allow_html=True,
)

PRODUCTS = {
    "Personal Loan": [
        {"name":"Maybank One Personal Loan", "rate":6.50, "term":5, "amount":20000, "detail":"Illustrative unsecured personal loan for planned expenses."},
        {"name":"Maybank One Flexi Loan", "rate":7.25, "term":7, "amount":35000, "detail":"Illustrative longer-tenure loan for a lower monthly commitment."},
    ],
    "Credit Card": [
        {"name":"Maybank One Everyday Card", "rate":18.00, "term":36, "amount":8000, "detail":"Illustrative revolving balance scenario for monthly repayment planning."},
        {"name":"Maybank One Travel Card", "rate":15.00, "term":24, "amount":5000, "detail":"Illustrative card balance scenario with a shorter planning horizon."},
    ],
    "Home Loan": [
        {"name":"Maybank One Home Loan", "rate":4.20, "term":30, "amount":450000, "detail":"Illustrative home-loan scenario. Actual packages use bank-specific terms."},
        {"name":"Maybank One Flexi Home Loan", "rate":4.45, "term":25, "amount":450000, "detail":"Illustrative flexi home-loan scenario for comparison only."},
    ],
}
MAX_MONTHS = 600


def money(value: float) -> str:
    return f"RM {value:,.2f}"


def simulate(principal, monthly_rate, base_payment, mode, extra_pct=0, late_pct=0, miss_every=0, max_months=MAX_MONTHS):
    balance = float(principal)
    rows, month = [], 0
    total_interest = total_paid = 0.0
    stalled = False
    while balance > 0.01 and month < max_months:
        month += 1
        interest = balance * monthly_rate
        if mode == "on_time":
            payment = base_payment
        elif mode == "early":
            payment = base_payment * (1 + extra_pct / 100)
        elif miss_every and month % miss_every == 0:
            payment = 0.0
        else:
            payment = base_payment * (1 - late_pct / 100)
        payment = min(max(payment, 0), balance + interest)
        if payment <= interest:
            stalled = True
        principal_paid = payment - interest
        balance = max(balance - principal_paid, 0)
        total_interest += interest
        total_paid += payment
        rows.append({"Month":month, "Payment":round(payment,2), "Interest":round(interest,2), "Principal Paid":round(principal_paid,2), "Remaining Balance":round(balance,2)})
        if stalled and month > 36 and balance >= principal * 0.999:
            break
    return pd.DataFrame(rows), total_interest, total_paid, month, stalled


def simulate_package(principal, annual_rate, monthly_payment, behavior, max_months=MAX_MONTHS):
    """Build a cumulative package schedule with capitalized late charges."""
    if principal <= 0 or annual_rate < 0 or monthly_payment <= 0:
        raise ValueError("Principal, payment, and rate inputs must be valid positive values.")

    monthly_rate = annual_rate / 100 / 12
    behavior_key = behavior.lower().replace("-", "_").replace(" ", "_")
    balance = float(principal)
    rows = []
    cumulative_interest = 0.0
    cumulative_fees = 0.0
    total_paid = 0.0

    for month in range(1, max_months + 1):
        if balance <= 0.01:
            break

        opening_balance = balance
        interest_paid = opening_balance * monthly_rate
        late_fee = 0.0

        if behavior_key == "early":
            scheduled_payment = monthly_payment * 1.25
        elif behavior_key == "late":
            scheduled_payment = 0.0 if month % 3 == 0 else monthly_payment * 0.70
            if month % 3 == 0:
                late_fee = max(25.0, monthly_payment * 0.05)
        else:
            scheduled_payment = monthly_payment

        balance_before_payment = opening_balance + interest_paid + late_fee
        payment = min(scheduled_payment, balance_before_payment)
        interest_component = min(payment, interest_paid)
        principal_paid = max(payment - interest_component, 0.0)
        balance = max(balance_before_payment - payment, 0.0)

        cumulative_interest += interest_paid
        cumulative_fees += late_fee
        total_paid += payment
        rows.append({
            "Month": month,
            "Opening Balance": round(opening_balance, 2),
            "Interest Paid": round(interest_paid, 2),
            "Principal Paid": round(principal_paid, 2),
            "Late Fees": round(late_fee, 2),
            "Payment": round(payment, 2),
            "Remaining Balance": round(balance, 2),
            "Cumulative Interest": round(cumulative_interest, 2),
            "Cumulative Late Fees": round(cumulative_fees, 2),
            "Cumulative Paid": round(total_paid, 2),
        })

    return pd.DataFrame(rows)


def payoff_months_for_sensitivity(principal, annual_rate, monthly_payment, max_months=MAX_MONTHS):
    """Return payoff months for one heatmap scenario without rendering UI."""
    schedule = simulate_package(principal, annual_rate, monthly_payment, "on_time", max_months)
    if schedule.empty or schedule["Remaining Balance"].iloc[-1] > 0.01:
        return max_months
    return int(schedule["Month"].iloc[-1])


def assistant_reply(prompt, context):
    """Answer using only the current simulation context and transparent rules."""
    question = prompt.lower().strip()
    if not question:
        return "Ask about payment, interest, payoff time, late fees, strategy comparison, or the assumptions in this report."

    interest_share = (context["interest"] / context["total_paid"] * 100) if context["total_paid"] else 0
    if any(word in question for word in ("rate", "interest", "profit", "cost")):
        return (f"This scenario uses {context['rate']:.2f}% annual interest. Estimated interest is "
                f"{money(context['interest'])}, which is {interest_share:.1f}% of estimated payments. "
                "This is a modelled estimate, not an official quote.")
    if any(word in question for word in ("payment", "monthly", "installment")):
        return (f"The estimated monthly payment is {money(context['payment'])}. "
                f"The selected {context['strategy']} scenario pays off in about {context['months']} months. "
                "Changing the payment amount recalculates the charts and report metrics.")
    if any(word in question for word in ("late", "miss", "penalty", "fee")):
        return (f"The selected late-payment model estimates {money(context['late_fees'])} in fees and "
                f"{context['late_months']} months to repay under the comparison late scenario. "
                "Actual fees and credit-reporting effects depend on the lender and agreement.")
    if any(word in question for word in ("early", "extra", "save", "saving")):
        return (f"The comparison early-payment scenario takes {context['early_months']} months and estimates "
                f"{money(context['early_interest'])} interest. The selected scenario estimates {money(context['interest'])}. "
                "Paying more can reduce interest, but the model does not assess affordability or liquidity needs.")
    if any(word in question for word in ("compare", "difference", "strategy", "on time")):
        return (f"Compared with on-time repayment, the selected scenario changes the estimated cost by "
                f"{money(context['interest'] - context['on_time_interest'])}. On-time payoff is "
                f"{context['on_time_months']} months; early is {context['early_months']} months; late is "
                f"{context['late_months']} months in this illustration.")
    if any(word in question for word in ("assumption", "accurate", "reliable", "official", "advice")):
        return ("The assistant uses deterministic values from the current simulation. It does not access bank systems, "
                "credit files, live rates, eligibility rules, or legal terms. Verify all rates, fees, and disclosures with the lender.")
    if any(word in question for word in ("report", "pdf", "download")):
        return "Open Advanced Analytics & Cumulative Insights to review the grounded analysis and download the current scenario as a PDF report."
    return ("I can explain the current payment, interest cost, payoff time, late fees, strategy comparison, "
            "assumptions, or PDF report. Try asking: What happens if I pay late?")


def build_report_pdf(context, schedule_df, package_schedule_df, compare_df):
    """Create a local, calculation-grounded PDF report for download."""
    output = io.BytesIO()
    with PdfPages(output) as pdf:
        summary = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        summary.text(0.08, 0.94, "Finance Planner Report", fontsize=24, weight="bold", color="#111111")
        summary.text(0.08, 0.912, "Illustrative scenario analysis | Generated " + date.today().isoformat(), fontsize=9, color="#665500")
        summary.text(0.08, 0.865, context["product"], fontsize=15, weight="bold", color="#111111")
        summary.text(0.08, 0.835, f"Strategy: {context['strategy']} | Amount: {money(context['principal'])} | Annual rate: {context['rate']:.2f}%", fontsize=10, color="#333333")

        metrics = [
            ("Monthly payment", money(context["payment"])),
            ("Total interest", money(context["interest"])),
            ("Time to payoff", f"{context['months']} months"),
            ("Total repaid", money(context["total_paid"])),
            ("Late fees", money(context["late_fees"])),
            ("Interest share", f"{context['interest_share']:.1f}%"),
        ]
        y_position = 0.77
        for index, (label, value) in enumerate(metrics):
            x_position = 0.08 + (index % 2) * 0.44
            if index and index % 2 == 0:
                y_position -= 0.075
            summary.text(x_position, y_position, label.upper(), fontsize=8, color="#665500")
            summary.text(x_position, y_position - 0.028, value, fontsize=16, weight="bold", color="#111111")

        analysis = (
            f"Analysis: The selected scenario estimates {money(context['interest'])} in interest over "
            f"{context['months']} months. The early-payment comparison reaches payoff in "
            f"{context['early_months']} months, while the late-payment comparison reaches payoff in "
            f"{context['late_months']} months and includes {money(context['late_fees'])} in modelled fees."
        )
        summary.text(0.08, 0.545, "AI-GROUNDED SUMMARY", fontsize=10, weight="bold", color="#665500")
        summary.text(0.08, 0.515, "\n".join(textwrap.wrap(analysis, 86)), fontsize=10, color="#222222", va="top", linespacing=1.5)
        summary.text(0.08, 0.34, "ASSUMPTIONS AND LIMITS", fontsize=10, weight="bold", color="#665500")
        assumptions = ("Fixed monthly interest model; payment is applied after interest. "
                       "Illustrative product and rate data only. No taxes, insurance, credit reporting, "
                       "eligibility, lender-specific fees, or official approval decision is included.")
        summary.text(0.08, 0.31, "\n".join(textwrap.wrap(assumptions, 86)), fontsize=9, color="#333333", va="top", linespacing=1.5)
        summary.text(0.08, 0.12, "This report is educational and should be checked against current official lender documentation.", fontsize=8, color="#777777")
        pdf.savefig(summary, bbox_inches="tight")
        plt.close(summary)

        charts, axes = plt.subplots(2, 2, figsize=(8.27, 11.69), facecolor="white")
        axes = axes.flatten()
        axes[0].plot(package_schedule_df["Month"], package_schedule_df["Remaining Balance"], color="#111111", linewidth=2.5)
        axes[0].set_title("Overview: remaining balance", loc="left", color="#111111", weight="bold")
        axes[0].set_xlabel("Month")
        axes[0].set_ylabel("Balance (RM)")
        axes[0].grid(alpha=0.2)
        axes[1].bar(compare_df["Strategy"], compare_df["Total Interest"], color=["#c7cbd0", "#d4a900", "#111111"])
        axes[1].set_title("Overview: interest by strategy", loc="left", color="#111111", weight="bold")
        axes[1].set_ylabel("Interest (RM)")
        axes[1].tick_params(axis="x", rotation=25)
        axes[1].grid(axis="y", alpha=0.2)
        axes[2].bar(compare_df["Strategy"], compare_df["Payoff Months"], color=["#c7cbd0", "#d4a900", "#111111"])
        axes[2].set_title("Overview: payoff time", loc="left", color="#111111", weight="bold")
        axes[2].set_ylabel("Months")
        axes[2].tick_params(axis="x", rotation=25)
        axes[2].grid(axis="y", alpha=0.2)
        axes[3].pie([context["principal"], context["interest"]], labels=["Principal", "Interest"], autopct="%1.1f%%", colors=["#c7cbd0", "#ffd400"], textprops={"color": "#111111"})
        axes[3].set_title("Overview: payment composition", loc="left", color="#111111", weight="bold")
        charts.suptitle("Overview charts and what they mean", fontsize=17, weight="bold", color="#111111", x=0.08, ha="left")
        charts.text(0.08, 0.015, "Balance shows how quickly debt falls. Strategy bars compare cost and time. The composition chart shows how much of total cost is interest.", fontsize=8, color="#444444")
        charts.tight_layout(rect=[0, 0.04, 1, 0.96])
        pdf.savefig(charts, bbox_inches="tight")
        plt.close(charts)

        advanced, axes = plt.subplots(2, 2, figsize=(8.27, 11.69), facecolor="white")
        axes = axes.flatten()
        advanced_title = "Advanced cumulative insights"
        axes[0].bar(package_schedule_df["Month"], package_schedule_df["Principal Paid"], label="Principal", color="#c7cbd0")
        axes[0].bar(package_schedule_df["Month"], package_schedule_df["Interest Paid"], bottom=package_schedule_df["Principal Paid"], label="Interest", color="#ffd400")
        axes[0].set_title("1. Monthly payment split", loc="left", color="#111111", weight="bold")
        axes[0].set_xlabel("Month")
        axes[0].set_ylabel("Payment (RM)")
        axes[0].legend(fontsize=7)
        axes[0].grid(axis="y", alpha=0.2)
        axes[1].plot(package_schedule_df["Month"], package_schedule_df["Cumulative Interest"], color="#d4a900", linewidth=2.5)
        axes[1].fill_between(package_schedule_df["Month"], package_schedule_df["Cumulative Interest"], color="#ffd400", alpha=0.35)
        axes[1].set_title("2. Cumulative interest", loc="left", color="#111111", weight="bold")
        axes[1].set_xlabel("Month")
        axes[1].set_ylabel("Interest (RM)")
        axes[1].grid(alpha=0.2)
        cost_labels = ["Principal", "Interest", "Late fees", "Final cost"]
        cost_values = [context["principal"], context["interest"], context["late_fees"], context["principal"] + context["interest"] + context["late_fees"]]
        axes[2].bar(cost_labels, cost_values, color=["#c7cbd0", "#ffd400", "#d4a900", "#111111"])
        axes[2].set_title("3. Total cost breakdown", loc="left", color="#111111", weight="bold")
        axes[2].set_ylabel("Cost (RM)")
        axes[2].tick_params(axis="x", rotation=25)
        axes[2].grid(axis="y", alpha=0.2)
        payment_grid = sorted({max(1.0, context["payment"] * factor) for factor in (0.6, 0.8, 1.0, 1.2, 1.4)})
        rate_grid = sorted({max(0.0, context["rate"] + offset) for offset in (-4, -2, 0, 2, 4)})
        heat_values = [[payoff_months_for_sensitivity(context["principal"], rate, payment) for payment in payment_grid] for rate in rate_grid]
        image = axes[3].imshow(heat_values, aspect="auto", cmap="cividis")
        axes[3].set_title("4. Payment sensitivity", loc="left", color="#111111", weight="bold")
        axes[3].set_xlabel("Payment level: low to high")
        axes[3].set_ylabel("Annual rate: low to high")
        axes[3].set_xticks(range(len(payment_grid)), [f"{value:,.0f}" for value in payment_grid], rotation=35)
        axes[3].set_yticks(range(len(rate_grid)), [f"{value:.1f}%" for value in rate_grid])
        advanced.colorbar(image, ax=axes[3], label="Payoff months", fraction=0.046, pad=0.04)
        advanced.suptitle(advanced_title, fontsize=17, weight="bold", color="#111111", x=0.08, ha="left")
        advanced.text(0.08, 0.015, "The split chart shows payment composition. The area trend shows interest accumulating. The cost chart isolates fees. The heatmap shows how higher payments usually shorten payoff time.", fontsize=8, color="#444444")
        advanced.tight_layout(rect=[0, 0.04, 1, 0.96])
        pdf.savefig(advanced, bbox_inches="tight")
        plt.close(advanced)

        tables = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        tables.text(0.08, 0.95, "Detailed schedule tables", fontsize=20, weight="bold", color="#111111")
        tables.text(0.08, 0.925, "Spreadsheet-style extracts from the current scenario", fontsize=10, color="#665500")
        tables.text(0.08, 0.885, "Comparison summary", fontsize=12, weight="bold", color="#111111")
        comparison_table = tables.add_axes([0.08, 0.72, 0.84, 0.14])
        comparison_table.axis("off")
        comparison_values = compare_df.round(2).values.tolist()
        table = comparison_table.table(cellText=comparison_values, colLabels=list(compare_df.columns), loc="center", cellLoc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.6)
        for cell in table.get_celld().values():
            cell.set_edgecolor("#c7cbd0")
        for cell in table.get_celld().values():
            if cell.get_text().get_text() in compare_df.columns:
                cell.set_facecolor("#ffd400")
                cell.set_text_props(weight="bold", color="#111111")

        table_rows = schedule_df.copy()
        if len(table_rows) > 24:
            table_rows = pd.concat([table_rows.head(12), table_rows.tail(12)])
        table_rows = table_rows[["Month", "Payment", "Interest", "Principal Paid", "Remaining Balance"]].round(2)
        tables.text(0.08, 0.67, "Payment schedule extract", fontsize=12, weight="bold", color="#111111")
        schedule_table = tables.add_axes([0.08, 0.19, 0.84, 0.45])
        schedule_table.axis("off")
        schedule_values = table_rows.values.tolist()
        schedule_display = [[str(value) for value in row] for row in schedule_values]
        schedule_plot = schedule_table.table(cellText=schedule_display, colLabels=list(table_rows.columns), loc="center", cellLoc="right")
        schedule_plot.auto_set_font_size(False)
        schedule_plot.set_fontsize(7)
        schedule_plot.scale(1, 1.35)
        for cell in schedule_plot.get_celld().values():
            cell.set_edgecolor("#d5d5d5")
        for cell in schedule_plot.get_celld().values():
            if cell.get_text().get_text() in table_rows.columns:
                cell.set_facecolor("#ffd400")
                cell.set_text_props(weight="bold", color="#111111")
        tables.text(0.08, 0.11, "If the schedule is longer than 24 months, the table shows the first and last 12 months. The complete schedule remains available as CSV in the app.", fontsize=8, color="#555555")
        pdf.savefig(tables, bbox_inches="tight")
        plt.close(tables)
    output.seek(0)
    return output.getvalue()


st.sidebar.markdown('<div class="brand"><div class="fake-logo"><span class="fake-logo-badge">M</span><span>maybank one</span></div><div class="fake-logo-note">sample finance planner</div></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="section-label">Plan setup</div>', unsafe_allow_html=True)
category = st.sidebar.selectbox("Product category", list(PRODUCTS))
product_names = [product["name"] for product in PRODUCTS[category]]
selected_name = st.sidebar.selectbox("Sample package", product_names)
selected_product = next(item for item in PRODUCTS[category] if item["name"] == selected_name)
principal = st.sidebar.number_input("Amount (RM)", min_value=100.0, value=float(selected_product["amount"]), step=500.0, key=f"amount_{selected_name}")
annual_rate = st.sidebar.number_input("Annual rate (%)", min_value=0.0, max_value=36.0, value=float(selected_product["rate"]), step=0.1, format="%.2f", key=f"rate_{selected_name}")
if category == "Home Loan":
    term_years = st.sidebar.slider("Term (years)", 1, 35, int(selected_product["term"]), key=f"years_{selected_name}")
    term_months = term_years * 12
else:
    max_term = 120 if category == "Credit Card" else 180
    default_months = int(selected_product["term"] if category == "Credit Card" else selected_product["term"] * 12)
    term_months = st.sidebar.slider("Planning horizon (months)", 6, max_term, min(default_months, max_term), key=f"months_{selected_name}")
monthly_rate = annual_rate / 100 / 12
suggested_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -term_months) if monthly_rate else principal / term_months
monthly_payment = st.sidebar.number_input("Monthly payment (RM)", min_value=1.0, value=float(round(suggested_payment, 2)), step=50.0, format="%.2f", key=f"payment_{selected_name}")
strategy_label = st.sidebar.radio("Repayment strategy", ["On-time", "Pay extra", "Pay less / miss payments"])
extra_pct = late_pct = miss_every = 0
if strategy_label == "Pay extra":
    extra_pct = st.sidebar.slider("Extra payment (%)", 0, 200, 25, step=5)
elif strategy_label == "Pay less / miss payments":
    late_pct = st.sidebar.slider("Payment reduction (%)", 0, 90, 30, step=5)
    miss_every = st.sidebar.slider("Skip every Nth month (0 = never)", 0, 12, 3)
mode = {"On-time":"on_time", "Pay extra":"early", "Pay less / miss payments":"late"}[strategy_label]
schedule_df, total_interest, total_paid, months_taken, stalled = simulate(principal, monthly_rate, monthly_payment, mode, extra_pct, late_pct, miss_every)
on_time = simulate(principal, monthly_rate, monthly_payment, "on_time")
early = simulate(principal, monthly_rate, monthly_payment, "early", extra_pct=25)
late = simulate(principal, monthly_rate, monthly_payment, "late", late_pct=30, miss_every=3)
package_schedule_df = simulate_package(
    principal=principal,
    annual_rate=annual_rate,
    monthly_payment=monthly_payment,
    behavior=mode,
)
package_interest = float(package_schedule_df["Interest Paid"].sum())
package_late_fees = float(package_schedule_df["Late Fees"].sum())
package_total_paid = float(package_schedule_df["Payment"].sum())
assistant_context = {
    "product": selected_product["name"],
    "principal": principal,
    "rate": annual_rate,
    "interest": package_interest,
    "total_paid": package_total_paid,
    "payment": monthly_payment,
    "months": len(package_schedule_df),
    "strategy": strategy_label,
    "late_fees": package_late_fees,
    "late_months": late[3],
    "early_months": early[3],
    "early_interest": early[1],
    "on_time_months": on_time[3],
    "on_time_interest": on_time[1],
}
assistant_context["interest_share"] = (
    package_interest / package_total_paid * 100 if package_total_paid else 0
)

st.markdown('<div class="hero"><div class="eyebrow">Malaysia finance planning</div><h1>Make the cost of borrowing visible.</h1><p>Explore illustrative Maybank One-style packages, test repayment behaviour, and understand the trade-offs before you make a financial decision.</p></div>', unsafe_allow_html=True)
st.markdown('<div class="info-strip"><strong>Illustrative model:</strong> This planner is for education and comparison. It is not an application, quotation, approval decision, or official Maybank product page.</div>', unsafe_allow_html=True)
tab_overview, tab_packages, tab_assistant = st.tabs(["Overview", "Packages", "Ask the planner"])

with tab_overview:
    st.markdown(f"<div class='section-label'>Selected scenario / {category}</div><h2>{selected_product['name']}</h2>", unsafe_allow_html=True)
    st.caption(selected_product["detail"])
    c1, c2, c3, c4 = st.columns(4)
    metrics = [("Estimated monthly payment", money(monthly_payment), "Based on your inputs"), ("Estimated total interest", money(total_interest), f"At {annual_rate:.2f}% p.a."), ("Estimated time to payoff", f"{months_taken} months", "Maximum model horizon: 600 months"), ("Estimated total repaid", money(total_paid), "Principal plus interest")]
    for column, (title, value, note) in zip((c1, c2, c3, c4), metrics):
        with column:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>{title}</div><div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>", unsafe_allow_html=True)
    if stalled:
        st.warning("This payment does not consistently cover the estimated monthly interest. Increase the payment or review the scenario before relying on the payoff estimate.")
    st.markdown('<div class="section-label">View 1 / How your balance falls over time</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-guide"><strong>Explore this chart:</strong> Hover over the line for exact figures. Click any point to see what your remaining balance and monthly payment mean at that moment.</div>', unsafe_allow_html=True)
    fig_balance = go.Figure(go.Scatter(x=schedule_df["Month"], y=schedule_df["Remaining Balance"], mode="lines", line=dict(color="#ffd400", width=3), name="Balance"))
    fig_balance.update_traces(hovertemplate="Month %{x}<br>Remaining balance: RM %{y:,.2f}<extra></extra>")
    fig_balance.update_layout(height=360, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor="#111111", plot_bgcolor="#171717", font=dict(color="#ffd400"), hovermode="x unified", title="Remaining balance by month", xaxis_title="Repayment month", yaxis_title="Remaining balance (RM)", xaxis=dict(gridcolor="#444444"), yaxis=dict(gridcolor="#444444"))
    balance_event = st.plotly_chart(fig_balance, use_container_width=True, key="balance_chart", on_select="rerun", selection_mode="points")
    selected_points = getattr(getattr(balance_event, "selection", None), "point_indices", []) if balance_event else []
    if selected_points:
        selected_row = schedule_df.iloc[selected_points[0]]
        selected_interest = float(selected_row["Interest"])
        selected_principal = float(selected_row["Principal Paid"])
        st.markdown(
            f"<div class='chart-detail'><strong>Month {int(selected_row['Month'])} in plain language</strong><br>"
            f"You pay <strong>{money(float(selected_row['Payment']))}</strong>. About <strong>{money(selected_interest)}</strong> covers interest, while <strong>{money(selected_principal)}</strong> reduces what you owe. "
            f"Your remaining balance after this payment is <strong>{money(float(selected_row['Remaining Balance']))}</strong>.</div>",
            unsafe_allow_html=True,
        )
    compare_df = pd.DataFrame({"Strategy":["On-time", "Pay extra", "Pay less / miss"], "Total interest":[on_time[1], early[1], late[1]], "Payoff months":[on_time[3], early[3], late[3]]})
    left, right = st.columns(2)
    with left:
        fig_interest = px.bar(compare_df, x="Strategy", y="Total interest", color="Strategy", color_discrete_sequence=["#c7cbd0", "#ffd400", "#ffea72"], title="Total interest paid by strategy")
        fig_interest.update_traces(hovertemplate="%{x}<br>Total interest: RM %{y:,.2f}<extra></extra>")
        fig_interest.update_layout(height=330, showlegend=False, margin=dict(l=10, r=10, t=45, b=10), paper_bgcolor="#111111", plot_bgcolor="#171717", font=dict(color="#ffd400"), yaxis_title="Total interest paid (RM)", xaxis=dict(gridcolor="#444444"), yaxis=dict(gridcolor="#444444"))
        st.plotly_chart(fig_interest, use_container_width=True)
    with right:
        fig_time = px.bar(compare_df, x="Strategy", y="Payoff months", color="Strategy", color_discrete_sequence=["#c7cbd0", "#ffd400", "#ffea72"], title="Time needed to repay")
        fig_time.update_traces(hovertemplate="%{x}<br>Time to repay: %{y} months<extra></extra>")
        fig_time.update_layout(height=330, showlegend=False, margin=dict(l=10, r=10, t=45, b=10), paper_bgcolor="#111111", plot_bgcolor="#171717", font=dict(color="#ffd400"), yaxis_title="Months to repay", xaxis=dict(gridcolor="#444444"), yaxis=dict(gridcolor="#444444"))
        st.plotly_chart(fig_time, use_container_width=True)
    st.markdown('<div class="section-label">View 3 / Where your money goes</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-guide">This chart separates the original amount borrowed from the estimated interest cost. Hover over a segment to see its amount.</div>', unsafe_allow_html=True)
    pie = pd.DataFrame({"Component":["Principal", "Interest"], "Amount":[principal, total_interest]})
    fig_pie = px.pie(pie, names="Component", values="Amount", hole=0.58, color="Component", color_discrete_map={"Principal":"#c7cbd0", "Interest":"#ffd400"})
    fig_pie.update_traces(hovertemplate="%{label}<br>Amount: RM %{value:,.2f}<br>Share: %{percent}<extra></extra>")
    fig_pie.update_layout(height=330, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#111111", plot_bgcolor="#171717", font=dict(color="#ffd400"), title="Principal versus interest")
    st.plotly_chart(fig_pie, use_container_width=True)
    with st.expander("Review assumptions and payment schedule"):
        st.write("The model applies a fixed monthly rate, assumes payments are made monthly, and does not include fees, taxes, insurance, compounding variations, late charges, eligibility rules, or credit-reporting outcomes.")
        st.dataframe(schedule_df, use_container_width=True, hide_index=True)
        st.download_button("Download schedule CSV", schedule_df.to_csv(index=False).encode("utf-8"), "finance_planner_schedule.csv", "text/csv")

with tab_packages:
    st.markdown('<div class="section-label">Illustrative catalogue</div><h2>Choose a starting point</h2>', unsafe_allow_html=True)
    st.write("These sample packages make it easier to compare product types. They are deliberately labelled illustrative and should be checked against current official bank information.")
    for package_category, packages in PRODUCTS.items():
        st.markdown(f"<div class='section-label'>{package_category}</div>", unsafe_allow_html=True)
        package_columns = st.columns(len(packages))
        for column, package in zip(package_columns, packages):
            with column:
                term_label = "years" if package_category == "Home Loan" else ("months" if package_category == "Credit Card" else "years")
                st.markdown(f"<div class='package-card'><div class='package-type'>{package_category}</div><h3>{package['name']}</h3><div class='package-rate'>{package['rate']:.2f}% <span style='font:400 13px DM Sans'>illustrative p.a.</span></div><div class='package-detail'>{package['detail']}<br><br>Sample amount: {money(package['amount'])}<br>Sample term: {package['term']} {term_label}</div></div>", unsafe_allow_html=True)

with tab_assistant:
    st.markdown('<div class="section-label">Guided answers</div><h2>Ask the planner</h2>', unsafe_allow_html=True)
    st.write("Ask about this scenario in plain language. The assistant uses the numbers currently visible in the planner and does not provide regulated financial advice.")
    if "chat" not in st.session_state:
        st.session_state.chat = []
    for message in st.session_state.chat:
        st.markdown(f"<div class='chat-{message['role']}'>{message['text']}</div>", unsafe_allow_html=True)
    prompt = st.chat_input("For example: How much interest will I pay?")
    if prompt:
        st.session_state.chat.append({"role":"user", "text":prompt})
        st.session_state.chat.append({"role":"bot", "text":assistant_reply(prompt, assistant_context)})
        st.rerun()
    st.markdown("**Try asking**  \nWhat happens if I pay late?  \nHow much interest will I pay?  \nIs this an official bank quote?", unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="fine-print">Maybank One Finance Planner is a sample educational interface. Maybank, its products, and its trademarks are referenced only as inspiration for a prototype. Confirm current rates, fees, eligibility, disclosures, and terms directly with the relevant financial institution.</div>', unsafe_allow_html=True)


# =====================================================================
# ADVANCED ANALYTICS - appended without changing the existing interface
# =====================================================================
with st.expander("Advanced Analytics & Cumulative Insights", expanded=False):
    st.subheader("Cumulative package analysis")
    st.caption(
        "These additional views use the cumulative package engine. Interest is "
        "applied to the opening balance each month; late fees are added to the balance."
    )
    report_compare_df = pd.DataFrame({
        "Strategy": ["On-time", "Early", "Late"],
        "Total Interest": [on_time[1], early[1], late[1]],
        "Payoff Months": [on_time[3], early[3], late[3]],
    })
    report_bytes = build_report_pdf(
        assistant_context,
        schedule_df,
        package_schedule_df,
        report_compare_df,
    )
    st.download_button(
        "Download PDF analysis report",
        data=report_bytes,
        file_name="finance_planner_analysis_report.pdf",
        mime="application/pdf",
        help="Downloads a two-page report with the current scenario, grounded analysis, assumptions, and charts.",
    )
    st.caption("The PDF uses the current inputs and deterministic chart calculations. It is not an official bank document.")

    # Chart 1: monthly principal and interest components.
    amortization_df = package_schedule_df.melt(
        id_vars="Month",
        value_vars=["Principal Paid", "Interest Paid"],
        var_name="Payment Component",
        value_name="Amount (RM)",
    )
    fig_amortization = px.bar(
        amortization_df,
        x="Month",
        y="Amount (RM)",
        color="Payment Component",
        barmode="stack",
        title="Chart 1: Monthly payment split between principal and interest",
        labels={"Month": "Repayment month", "Amount (RM)": "Amount paid (RM)"},
        color_discrete_map={"Principal Paid": "#c7cbd0", "Interest Paid": "#ffd400"},
    )
    fig_amortization.update_traces(
        hovertemplate="Month %{x}<br>%{fullData.name}: RM %{y:,.2f}<extra></extra>"
    )
    fig_amortization.update_layout(height=420, paper_bgcolor="#111111", plot_bgcolor="#171717", font=dict(color="#ffd400"), xaxis=dict(gridcolor="#444444"), yaxis=dict(gridcolor="#444444"))
    st.plotly_chart(fig_amortization, use_container_width=True)

    # Chart 2: cumulative interest over the life of the package.
    fig_cumulative_interest = px.area(
        package_schedule_df,
        x="Month",
        y="Cumulative Interest",
        title="Chart 2: Cumulative interest paid over time",
        labels={"Month": "Repayment month", "Cumulative Interest": "Running interest total (RM)"},
    )
    fig_cumulative_interest.update_traces(
        line_color="#ffd400",
        fillcolor="rgba(255, 212, 0, 0.42)",
        hovertemplate="Month %{x}<br>Cumulative interest: RM %{y:,.2f}<extra></extra>",
    )
    fig_cumulative_interest.update_layout(height=420, paper_bgcolor="#111111", plot_bgcolor="#171717", font=dict(color="#ffd400"), xaxis=dict(gridcolor="#444444"), yaxis=dict(gridcolor="#444444"))
    st.plotly_chart(fig_cumulative_interest, use_container_width=True)

    # Chart 3: principal, interest, late fees, and final out-of-pocket cost.
    total_package_interest = float(package_schedule_df["Interest Paid"].sum())
    total_late_fees = float(package_schedule_df["Late Fees"].sum())
    final_out_of_pocket = principal + total_package_interest + total_late_fees
    waterfall_df = pd.DataFrame({
        "Step": ["Starting Principal", "Total Interest Paid", "Total Late Fees", "Final Out-of-Pocket Cost"],
        "Amount": [principal, total_package_interest, total_late_fees, final_out_of_pocket],
        "Measure": ["absolute", "relative", "relative", "total"],
    })
    fig_waterfall = go.Figure(
        go.Waterfall(
            x=waterfall_df["Step"],
            y=waterfall_df["Amount"],
            measure=waterfall_df["Measure"],
            text=[money(value) for value in waterfall_df["Amount"]],
            textposition="outside",
            connector={"line": {"color": "#777777"}},
            increasing={"marker": {"color": "#ffd400"}},
            totals={"marker": {"color": "#ffd400"}},
            hovertemplate="%{x}<br>Amount: RM %{y:,.2f}<extra></extra>",
        )
    )
    fig_waterfall.update_layout(
        title="Chart 3: How the final borrowing cost is built",
        yaxis_title="Cost (RM)",
        height=420,
        paper_bgcolor="#111111",
        plot_bgcolor="#171717",
        font={"color": "#ffd400"},
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

    # Chart 4: payoff sensitivity to payment amount and annual interest rate.
    payment_values = sorted({
        max(1.0, monthly_payment * 0.60),
        max(1.0, monthly_payment * 0.80),
        max(1.0, monthly_payment),
        monthly_payment * 1.20,
        monthly_payment * 1.40,
    })
    rate_values = sorted({
        max(0.0, annual_rate - 4.0),
        max(0.0, annual_rate - 2.0),
        annual_rate,
        annual_rate + 2.0,
        annual_rate + 4.0,
    })
    sensitivity_rows = []
    for rate_value in rate_values:
        for payment_value in payment_values:
            sensitivity_rows.append({
                "Annual Rate (%)": round(rate_value, 2),
                "Monthly Payment (RM)": round(payment_value, 2),
                "Time to Payoff (Months)": payoff_months_for_sensitivity(
                    principal, rate_value, payment_value
                ),
            })
    sensitivity_df = pd.DataFrame(sensitivity_rows)
    fig_heatmap = px.density_heatmap(
        sensitivity_df,
        x="Monthly Payment (RM)",
        y="Annual Rate (%)",
        z="Time to Payoff (Months)",
        histfunc="avg",
        text_auto=True,
        title="Chart 4: How payment size and interest rate affect payoff time",
        labels={"z": "Payoff months"},
        color_continuous_scale=["#ffd400", "#777777", "#111111"],
    )
    fig_heatmap.update_traces(
        hovertemplate="Payment: RM %{x:,.2f}<br>Rate: %{y:.2f}%<br>Payoff: %{z} months<extra></extra>"
    )
    fig_heatmap.update_layout(height=460, paper_bgcolor="#111111", plot_bgcolor="#171717", font=dict(color="#ffd400"), xaxis=dict(gridcolor="#444444"), yaxis=dict(gridcolor="#444444"))
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Chart 5: payoff progress at a user-selected month.
    max_gauge_month = max(1, len(package_schedule_df))
    selected_month = st.slider(
        "Chart 5: Select a month to inspect payoff progress",
        min_value=1,
        max_value=max_gauge_month,
        value=min(12, max_gauge_month),
        key="advanced_payoff_month",
    )
    selected_balance = float(
        package_schedule_df.loc[
            package_schedule_df["Month"] == selected_month, "Remaining Balance"
        ].iloc[0]
    )
    payoff_percentage = max(0.0, min(100.0, (1 - selected_balance / principal) * 100))
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=payoff_percentage,
            number={"suffix": "%", "valueformat": ".1f"},
            title={"text": f"Principal paid off by month {selected_month}"},
            gauge={
                "axis": {"range": [0, 100], "ticksuffix": "%"},
                "bar": {"color": "#ffd400"},
                "steps": [
                    {"range": [0, 50], "color": "#eeeeee"},
                    {"range": [50, 100], "color": "#777777"},
                ],
                "threshold": {"line": {"color": "#111111", "width": 4}, "value": payoff_percentage},
            },
        )
    )
    fig_gauge.update_layout(height=380, paper_bgcolor="#111111", font=dict(color="#ffd400"))
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.caption(
        f"At month {selected_month}, the estimated remaining balance is {money(selected_balance)}. "
        f"The gauge shows {payoff_percentage:.1f}% of the original principal paid off."
    )

    # Chart 6: how each monthly payment is allocated.
    st.markdown("---")
    st.subheader("Chart 6: Where each monthly payment goes")
    st.caption(
        "This view separates the amount reducing the balance from interest and any "
        "late fees charged during the selected scenario."
    )
    payment_mix_df = package_schedule_df.melt(
        id_vars="Month",
        value_vars=["Principal Paid", "Interest Paid", "Late Fees"],
        var_name="Payment Component",
        value_name="Amount (RM)",
    )
    fig_payment_mix = px.area(
        payment_mix_df,
        x="Month",
        y="Amount (RM)",
        color="Payment Component",
        groupnorm="percent",
        title="Monthly payment allocation (%)",
        labels={"Month": "Repayment month", "Amount (RM)": "Share of monthly cost"},
        color_discrete_map={
            "Principal Paid": "#c7cbd0",
            "Interest Paid": "#ffd400",
            "Late Fees": "#d97706",
        },
    )
    fig_payment_mix.update_traces(
        hovertemplate="Month %{x}<br>%{fullData.name}: %{y:.1f}% of monthly cost<extra></extra>"
    )
    fig_payment_mix.update_layout(
        height=420,
        paper_bgcolor="#111111",
        plot_bgcolor="#171717",
        font=dict(color="#ffd400"),
        yaxis=dict(title="Share of monthly cost (%)", ticksuffix="%", gridcolor="#444444"),
        xaxis=dict(title="Repayment month", gridcolor="#444444"),
    )
    st.plotly_chart(fig_payment_mix, use_container_width=True)

    # Chart 7: debt reduction compared with total cash paid to date.
    st.subheader("Chart 7: Debt remaining versus money paid")
    st.caption(
        "The debt line should fall as payments accumulate. The gap between cumulative "
        "cash paid and principal reduction represents interest and fees."
    )
    progress_df = package_schedule_df[[
        "Month", "Remaining Balance", "Cumulative Paid", "Cumulative Interest", "Cumulative Late Fees"
    ]].melt(
        id_vars="Month",
        var_name="Measure",
        value_name="Amount (RM)",
    )
    progress_labels = {
        "Remaining Balance": "Debt remaining",
        "Cumulative Paid": "Total cash paid",
        "Cumulative Interest": "Interest paid to date",
        "Cumulative Late Fees": "Late fees to date",
    }
    progress_df["Measure"] = progress_df["Measure"].map(progress_labels)
    fig_progress = px.line(
        progress_df,
        x="Month",
        y="Amount (RM)",
        color="Measure",
        title="Debt remaining and cumulative costs",
        labels={"Month": "Repayment month", "Amount (RM)": "Amount (RM)"},
        color_discrete_map={
            "Debt remaining": "#ffd400",
            "Total cash paid": "#c7cbd0",
            "Interest paid to date": "#f59e0b",
            "Late fees to date": "#d97706",
        },
    )
    fig_progress.update_traces(
        mode="lines+markers",
        hovertemplate="Month %{x}<br>%{fullData.name}: RM %{y:,.2f}<extra></extra>",
    )
    fig_progress.update_layout(
        height=420,
        paper_bgcolor="#111111",
        plot_bgcolor="#171717",
        font=dict(color="#ffd400"),
        hovermode="x unified",
        xaxis=dict(title="Repayment month", gridcolor="#444444"),
        yaxis=dict(title="Amount (RM)", gridcolor="#444444"),
    )
    st.plotly_chart(fig_progress, use_container_width=True)
