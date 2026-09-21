import os
import time
import datetime
import math
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# SECTION 1: SYSTEM & STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="FinWise Pro - Enterprise iOS Glass Adviser",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application Metadata Constants
APP_NAME = "FinWise Pro"
APP_VERSION = "2026.4.0"
APP_BUILD = "Build-8921-Enterprise"
AUTHOR_NAME = "Vikas Ramsevak Pal"
PLATFORM_TAG = "iOS Liquid Glass Enterprise Suite"

# ==============================================================================
# SECTION 2: APPLICATION STATE & DATABASE SIMULATION
# ==============================================================================
if "app_initialized" not in st.session_state:
    st.session_state.app_initialized = True
    st.session_state.init_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {
            "ID": "TXN-8001",
            "Date": "2026-09-01",
            "Category": "Base Salary",
            "Type": "Income",
            "Amount": 70000.0,
            "Method": "Direct Deposit / Bank",
            "Status": "Cleared",
            "Note": "Monthly Corporate Payroll Credit"
        },
        {
            "ID": "TXN-8002",
            "Date": "2026-09-02",
            "Category": "Housing & Rent",
            "Type": "Expense",
            "Amount": 18000.0,
            "Method": "UPI Direct",
            "Status": "Cleared",
            "Note": "Apartment Maintenance & Monthly Rent"
        },
        {
            "ID": "TXN-8003",
            "Date": "2026-09-03",
            "Category": "Groceries & Supplies",
            "Type": "Expense",
            "Amount": 8500.0,
            "Method": "Credit Card",
            "Status": "Cleared",
            "Note": "Supermarket Restock & Household Items"
        },
        {
            "ID": "TXN-8004",
            "Date": "2026-09-05",
            "Category": "Index Mutual Funds",
            "Type": "Investment",
            "Amount": 18000.0,
            "Method": "Auto-Debit SIP",
            "Status": "Cleared",
            "Note": "Nifty 50 Index Fund Systematic Plan"
        },
        {
            "ID": "TXN-8005",
            "Date": "2026-09-07",
            "Category": "Utilities & Internet",
            "Type": "Expense", "Amount": 3800.0,
            "Method": "UPI Direct",
            "Status": "Cleared",
            "Note": "Electricity, Water, & Fiber Broadband"
        },
        {
            "ID": "TXN-8006",
            "Date": "2026-09-10",
            "Category": "Vehicle Loan EMI",
            "Type": "Debt",
            "Amount": 6500.0,
            "Method": "Auto-Debit",
            "Status": "Cleared",
            "Note": "Bank Car Loan Fixed Installment"
        },
        {
            "ID": "TXN-8007",
            "Date": "2026-09-12",
            "Category": "Dining & Leisure",
            "Type": "Expense",
            "Amount": 4500.0,
            "Method": "Credit Card",
            "Status": "Cleared",
            "Note": "Weekend Dinners & Entertainment"
        },
        {
            "ID": "TXN-8008",
            "Date": "2026-09-15",
            "Category": "Freelance Design",
            "Type": "Income",
            "Amount": 15000.0,
            "Method": "Wire Transfer",
            "Status": "Cleared",
            "Note": "UI/UX Design Client Project Fee"
        },
        {
            "ID": "TXN-8009",
            "Date": "2026-09-18",
            "Category": "Tech Subscriptions",
            "Type": "Expense",
            "Amount": 2200.0,
            "Method": "Credit Card",
            "Status": "Cleared",
            "Note": "Cloud Services & Software Licenses"
        },
        {
            "ID": "TXN-8010",
            "Date": "2026-09-20",
            "Category": "Emergency Fund Deposit",
            "Type": "Investment",
            "Amount": 5000.0,
            "Method": "Bank Transfer",
            "Status": "Cleared",
            "Note": "High-Yield Savings Deposit"
        }
    ])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "financial_goals" not in st.session_state:
    st.session_state.financial_goals = pd.DataFrame([
        {
            "Goal ID": "G-101",
            "Goal Name": "Emergency Liquid Cushion",
            "Category": "Risk Reserve",
            "Target Amount (₹)": 250000.0,
            "Current Saved (₹)": 160000.0,
            "Target Date": "2027-03-31",
            "Priority": "High"
        },
        {
            "Goal ID": "G-102",
            "Goal Name": "International Tech Summit",
            "Category": "Travel & Learning",
            "Target Amount (₹)": 180000.0,
            "Current Saved (₹)": 75000.0,
            "Target Date": "2027-08-15",
            "Priority": "Medium"
        },
        {
            "Goal ID": "G-103",
            "Goal Name": "Long-Term Retirement SIP",
            "Category": "Wealth Corpus",
            "Target Amount (₹)": 5000000.0,
            "Current Saved (₹)": 650000.0,
            "Target Date": "2032-12-31",
            "Priority": "Critical"
        }
    ])

if "historical_performance" not in st.session_state:
    st.session_state.historical_performance = pd.DataFrame([
        {"Month": "Apr 2026", "Income": 70000.0, "Expenses": 38000.0, "Savings": 15000.0, "Debt": 7000.0, "Score": 71.2},
        {"Month": "May 2026", "Income": 72000.0, "Expenses": 36000.0, "Savings": 17000.0, "Debt": 7000.0, "Score": 74.8},
        {"Month": "Jun 2026", "Income": 72000.0, "Expenses": 41000.0, "Savings": 12000.0, "Debt": 7000.0, "Score": 66.5},
        {"Month": "Jul 2026", "Income": 75000.0, "Expenses": 35000.0, "Savings": 19000.0, "Debt": 6500.0, "Score": 80.4},
        {"Month": "Aug 2026", "Income": 75000.0, "Expenses": 34000.0, "Savings": 21000.0, "Debt": 6500.0, "Score": 83.9},
        {"Month": "Sep 2026", "Income": 85000.0, "Expenses": 37000.0, "Savings": 23000.0, "Debt": 6500.0, "Score": 85.2}
    ])

# ==============================================================================
# SECTION 3: MAMDANI FUZZY LOGIC MATHEMATICAL ENGINE
# ==============================================================================
def trimf(x, a, b, c):
    """
    Evaluates Triangular Membership Function value at x given vertices a <= b <= c.
    """
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    if b < x < c:
        return (c - x) / (c - b) if c != b else 1.0
    return 0.0

def trapmf(x, a, b, c, d):
    """
    Evaluates Trapezoidal Membership Function value at x given vertices a <= b <= c <= d.
    """
    if x <= a or x >= d:
        return 0.0
    if a <= x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    if b <= x <= c:
        return 1.0
    if c <= x <= d:
        return (d - x) / (d - c) if d != c else 1.0
    return 0.0

def evaluate_fuzzy_health(exp_ratio, sav_ratio, dbt_ratio):
    """
    Full Mamdani Fuzzy Inference Engine implementing Membership Function Degree Calculation,
    Fuzzy Rule Base Inference, Aggregation, and Centroid Defuzzification.
    """
    # 1. FUZZIFICATION: Expense Ratio Sets
    exp_low = trapmf(exp_ratio, 0.0, 0.0, 30.0, 50.0)
    exp_med = trimf(exp_ratio, 40.0, 55.0, 70.0)
    exp_high = trapmf(exp_ratio, 60.0, 80.0, 100.0, 100.0)

    # 2. FUZZIFICATION: Savings Ratio Sets
    sav_poor = trapmf(sav_ratio, 0.0, 0.0, 10.0, 20.0)
    sav_mod = trimf(sav_ratio, 15.0, 25.0, 35.0)
    sav_good = trapmf(sav_ratio, 30.0, 45.0, 100.0, 100.0)

    # 3. FUZZIFICATION: Debt Ratio Sets
    dbt_low = trapmf(dbt_ratio, 0.0, 0.0, 15.0, 30.0)
    dbt_med = trimf(dbt_ratio, 20.0, 35.0, 50.0)
    dbt_high = trapmf(dbt_ratio, 40.0, 60.0, 100.0, 100.0)

    # 4. RULE BASE INFERENCE (Mamdani Min Operator)
    rules = {
        "Poor": 0.0,
        "Fair": 0.0,
        "Good": 0.0,
        "Excellent": 0.0
    }

    # Rule 1: IF Expense is Low AND Savings is Good AND Debt is Low THEN Health is Excellent
    r1 = min(exp_low, sav_good, dbt_low)
    rules["Excellent"] = max(rules["Excellent"], r1)

    # Rule 2: IF Expense is Medium AND Savings is Moderate AND Debt is Low THEN Health is Good
    r2 = min(exp_med, sav_mod, dbt_low)
    rules["Good"] = max(rules["Good"], r2)

    # Rule 3: IF Expense is High OR Debt is High THEN Health is Poor
    r3 = max(exp_high, dbt_high)
    rules["Poor"] = max(rules["Poor"], r3)

    # Rule 4: IF Expense is Medium AND Savings is Poor THEN Health is Fair
    r4 = min(exp_med, sav_poor)
    rules["Fair"] = max(rules["Fair"], r4)

    # Rule 5: IF Savings is Good AND Debt is Medium THEN Health is Good
    r5 = min(sav_good, dbt_med)
    rules["Good"] = max(rules["Good"], r5)

    # Rule 6: IF Expense is Low AND Savings is Moderate THEN Health is Good
    r6 = min(exp_low, sav_mod)
    rules["Good"] = max(rules["Good"], r6)

    # Rule 7: IF Debt is High AND Savings is Poor THEN Health is Poor
    r7 = min(dbt_high, sav_poor)
    rules["Poor"] = max(rules["Poor"], r7)

    # 5. AGGREGATION & CENTROID DEFUZZIFICATION
    x_grid = np.linspace(0.0, 100.0, 101)
    aggregated = np.zeros_like(x_grid)

    for i, x in enumerate(x_grid):
        p_val = min(rules["Poor"], trapmf(x, 0.0, 0.0, 20.0, 40.0))
        f_val = min(rules["Fair"], trimf(x, 30.0, 50.0, 70.0))
        g_val = min(rules["Good"], trimf(x, 60.0, 75.0, 90.0))
        e_val = min(rules["Excellent"], trapmf(x, 80.0, 90.0, 100.0, 100.0))
        aggregated[i] = max(p_val, f_val, g_val, e_val)

    sum_agg = np.sum(aggregated)
    score = float(np.sum(x_grid * aggregated) / sum_agg) if sum_agg != 0.0 else 50.0

    if score >= 80.0:
        category = "Excellent"
    elif score >= 60.0:
        category = "Good"
    elif score >= 40.0:
        category = "Fair"
    else:
        category = "Poor"

    membership_details = {
        "exp": {"Low": exp_low, "Med": exp_med, "High": exp_high},
        "sav": {"Poor": sav_poor, "Mod": sav_mod, "Good": sav_good},
        "dbt": {"Low": dbt_low, "Med": dbt_med, "High": dbt_high}
    }

    return round(score, 1), category, rules, membership_details

# ==============================================================================
# SECTION 4: LANGCHAIN & GEMINI LLM INTEGRATION MODULE
# ==============================================================================
def get_ai_advice(query, inc, exp, sav, dbt, score, cat):
    """
    Connects to Google Gemini LLM via LangChain to generate contextual wealth management reports.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return f"""
### 📊 FinWise Automated Health Assessment
* **Mamdani Fuzzy Rating:** **{score}/100 ({cat})**
* **Monthly Income:** ₹{inc:,.2f} | **Expenses:** ₹{exp:,.2f}
* **Investments:** ₹{sav:,.2f} | **Debt Obligations:** ₹{dbt:,.2f}

#### 💡 Executive Advisory Recommendations:
1. **Debt Cap Strategy:** Maintain total monthly debt service payments below 30% of total income.
2. **SIP Acceleration:** Direct at least 20% to 25% of gross income toward equity index funds.
3. **Emergency Reserves:** Build a liquid cash emergency cushion covering 6 months of mandatory living expenses.
        """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import PromptTemplate

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )

        template = """
You are FinWise Pro AI, an Executive Certified Financial Planner (CFP) and Wealth Adviser.
Client Financial Snapshot:
- Gross Monthly Income: ₹{inc:,.2f}
- Monthly Living Expenses: ₹{exp:,.2f}
- Monthly Investments & Savings: ₹{sav:,.2f}
- Monthly Debt Obligations: ₹{dbt:,.2f}
- Calculated Mamdani Fuzzy Health Rating: {score}/100 ({cat})

Client Inquiry / Goal: "{query}"

Provide a structured, executive financial advisory report covering:
1. **Executive Evaluation:** Why the client received a Mamdani Fuzzy score of {score}/100 ({cat}).
2. **Vulnerability Assessment:** Highlight risks regarding discretionary leakages or debt service.
3. **Strategic Action Roadmap:** 3 actionable, prioritized financial steps for liquidity optimization and growth.
Format using clean, modern Markdown formatting.
"""
        prompt = PromptTemplate(
            input_variables=["inc", "exp", "sav", "dbt", "score", "cat", "query"],
            template=template
        )

        chain = prompt | llm
        res = chain.invoke({
            "inc": inc,
            "exp": exp,
            "sav": sav,
            "dbt": dbt,
            "score": score,
            "cat": cat,
            "query": query if query else "Provide a comprehensive financial health and wealth optimization report"
        })
        return res.content
    except Exception as e:
        return f"**Mamdani Evaluation Score:** {score}/100 ({cat}). Focus on reducing high-interest debt and boosting systematic SIP investments."

# ==============================================================================
# SECTION 5: HIGH-END IOS GLASSMORPHISM CSS STYLING ENGINE
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stApp {
    background: 
        radial-gradient(circle at 10% 15%, rgba(37, 99, 235, 0.45), transparent 45%),
        radial-gradient(circle at 90% 15%, rgba(147, 51, 234, 0.40), transparent 45%),
        radial-gradient(circle at 50% 85%, rgba(13, 148, 136, 0.30), transparent 50%),
        linear-gradient(135deg, #030712 0%, #0b1329 50%, #030712 100%) !important;
    color: #ffffff;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1440px; }

/* iOS Glass Cards with Smooth Hover Glow Effects */
.glass-panel, .top-metric-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    backdrop-filter: blur(40px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(200%) !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
    border-radius: 22px !important;
    padding: 24px;
}

.glass-panel:hover, .top-metric-card:hover {
    transform: translateY(-4px) scale(1.008);
    box-shadow: 0 30px 60px rgba(37, 99, 235, 0.3), inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

.metric-badge {
    width: 44px; height: 44px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center; font-size: 20px;
    margin-bottom: 12px;
}

.bg-green {
    background: rgba(16, 185, 129, 0.25);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.4);
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}

.bg-pink {
    background: rgba(244, 63, 94, 0.25);
    color: #fb7185;
    border: 1px solid rgba(244, 63, 94, 0.4);
    box-shadow: 0 0 20px rgba(244, 63, 94, 0.3);
}

.bg-blue {
    background: rgba(59, 130, 246, 0.25);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.4);
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

.bg-purple {
    background: rgba(139, 92, 246, 0.25);
    color: #c084fc;
    border: 1px solid rgba(139, 92, 246, 0.4);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}

.top-metric-label {
    font-size: 11px;
    color: rgba(255,255,255,0.7);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.top-metric-val {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin: 4px 0 2px 0;
}

.stNumberInput input, .stTextInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #60a5fa !important;
    box-shadow: 0 0 20px rgba(96, 165, 250, 0.5) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.02) 100%) !important;
    backdrop-filter: blur(40px) saturate(200%) !important;
    border-right: 1px solid rgba(255,255,255,0.18) !important;
}

div[data-testid="stRadio"] > label { display: none; }
div[data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 14px 18px;
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
}

div[data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateX(4px);
}

.stButton > button {
    width: 100%;
    border-radius: 16px;
    padding: 16px;
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 0 30px rgba(37, 99, 235, 0.6) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 0 40px rgba(124, 58, 237, 0.8) !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SECTION 6: SIDEBAR NAVIGATION CONTROLLER
# ==============================================================================
with st.sidebar:
    st.html(f"""
    <div style="display:flex; align-items:center; gap:12px; padding:10px 5px 15px 5px;">
        <div style="width:46px; height:46px; border-radius:16px; background:linear-gradient(135deg, #2563eb, #7c3aed); display:flex; align-items:center; justify-content:center; font-size:24px; box-shadow:0 0 25px rgba(37,99,235,0.8);">💎</div>
        <div>
            <div style="font-size:22px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">{APP_NAME}</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.6);">{PLATFORM_TAG}</div>
        </div>
    </div>
    """)
    st.markdown("---")

    nav_choice = st.radio(
        "Navigation",
        [
            "📊 Executive Dashboard",
            "💳 Expense & Income Manager",
            "🧠 Mamdani Fuzzy Analytics",
            "🔮 Wealth Predictions & SIP",
            "✨ AI Copilot Advisor",
            "📜 Transaction Audit Log",
            "⚙️ Settings & Profile"
        ],
        index=0
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.html(f"""
    <div style="padding:16px; border-radius:18px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15);">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:38px; height:38px; border-radius:50%; background:linear-gradient(135deg, #2563eb, #10b981); display:flex; align-items:center; justify-content:center; font-weight:800;">V</div>
            <div>
                <div style="font-size:14px; font-weight:700;">{AUTHOR_NAME}</div>
                <div style="font-size:11px; color:#34d399;">● Enterprise Pro User</div>
            </div>
        </div>
    </div>
    """)

# COMPUTATION OF REAL-TIME AGGREGATES FROM SESSION STATE LEDGER
df_trans = st.session_state.transactions
inc_tot = df_trans[df_trans["Type"] == "Income"]["Amount"].sum()
exp_tot = df_trans[df_trans["Type"] == "Expense"]["Amount"].sum()
inv_tot = df_trans[df_trans["Type"] == "Investment"]["Amount"].sum()
dbt_tot = df_trans[df_trans["Type"] == "Debt"]["Amount"].sum()

if inc_tot == 0.0:
    inc_tot = 1.0  # Safe fallback for division

exp_ratio = min((exp_tot / inc_tot) * 100.0, 100.0)
sav_ratio = min((inv_tot / inc_tot) * 100.0, 100.0)
dbt_ratio = min((dbt_tot / inc_tot) * 100.0, 100.0)

fz_score, fz_cat, fz_rules, fz_mems = evaluate_fuzzy_health(exp_ratio, sav_ratio, dbt_ratio)

# ==============================================================================
# TAB 1: 📊 EXECUTIVE DASHBOARD MODULE
# ==============================================================================
if nav_choice == "📊 Executive Dashboard":
    h_c1, h_c2 = st.columns([3, 1])
    with h_c1:
        st.html("""
        <div style="font-size:11px; font-weight:700; color:#60a5fa; letter-spacing:2px; text-transform:uppercase;">ENTERPRISE FINANCIAL INTELLIGENCE</div>
        <div style="font-size:38px; font-weight:800; color:#ffffff; margin:4px 0;">Executive Wealth & Health Dashboard</div>
        <div style="font-size:14px; color:rgba(255,255,255,0.7);">Real-time Mamdani Fuzzy Logic Scoring & LangChain AI Advisory.</div>
        """)
    with h_c2:
        st.html(f"""
        <div class="glass-panel" style="padding:18px; text-align:center;">
            <div style="font-size:11px; color:rgba(255,255,255,0.6);">FUZZY HEALTH RATING</div>
            <div style="font-size:32px; font-weight:800; color:#60a5fa;">{fz_score}/100</div>
            <div style="font-size:13px; font-weight:700; color:#c084fc;">{fz_cat}</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.html(f'<div class="top-metric-card"><div class="metric-badge bg-green">💼</div><div class="top-metric-label">Total Monthly Income</div><div class="top-metric-val">₹{inc_tot:,.2f}</div></div>')
    with m2:
        st.html(f'<div class="top-metric-card"><div class="metric-badge bg-pink">💳</div><div class="top-metric-label">Total Expenses</div><div class="top-metric-val">₹{exp_tot:,.2f}</div></div>')
    with m3:
        st.html(f'<div class="top-metric-card"><div class="metric-badge bg-blue">📈</div><div class="top-metric-label">Investments & SIPs</div><div class="top-metric-val">₹{inv_tot:,.2f}</div></div>')
    with m4:
        st.html(f'<div class="top-metric-card"><div class="metric-badge bg-purple">🏦</div><div class="top-metric-label">Debt Obligations</div><div class="top-metric-val">₹{dbt_tot:,.2f}</div></div>')

    st.markdown("<br>", unsafe_allow_html=True)
    st.html("<div style='font-size:18px; font-weight:700;'>📊 Monthly Cashflow Breakdown</div>")

    chart_df = pd.DataFrame({
        "Category": ["Income", "Expenses", "Investments", "Debt"],
        "Amount (₹)": [inc_tot, exp_tot, inv_tot, dbt_tot]
    }).set_index("Category")
    st.bar_chart(chart_df)

    st.markdown("<br>", unsafe_allow_html=True)
    st.html("<div style='font-size:18px; font-weight:700;'>🤖 AI-Generated Executive Advisory Report</div>")
    q_input = st.text_input("Specific Financial Query:", placeholder="e.g. How can I optimize my monthly budget and increase savings?")
    if st.button("✨ Refresh AI Advisory Report"):
        with st.spinner("Synthesizing metrics with LangChain & Gemini LLM..."):
            report = get_ai_advice(q_input, inc_tot, exp_tot, inv_tot, dbt_tot, fz_score, fz_cat)
            st.html(f'<div class="glass-panel" style="border-left:4px solid #a855f7;">{report}</div>')

# ==============================================================================
# TAB 2: 💳 EXPENSE & INCOME MANAGER MODULE
# ==============================================================================
elif nav_choice == "💳 Expense & Income Manager":
    st.html("""
    <div class="glass-panel">
        <h2>💳 Transaction & Cashflow Ledger</h2>
        <p style="color:rgba(255,255,255,0.7);">Record and manage individual transactions to continuously update Mamdani Fuzzy Metrics.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    st.html("<div style='font-size:16px; font-weight:700; margin-bottom:10px;'>➕ Record New Financial Transaction</div>")
    t_c1, t_c2, t_c3, t_c4, t_c5 = st.columns([2, 2, 2, 2, 3])
    with t_c1:
        t_date = st.date_input("Date", datetime.date.today())
    with t_c2:
        t_type = st.selectbox("Transaction Type", ["Income", "Expense", "Investment", "Debt"])
    with t_c3:
        t_cat = st.text_input("Category", value="General Outflow")
    with t_c4:
        t_amt = st.number_input("Amount (₹)", min_value=1.0, value=2500.0, step=500.0)
    with t_c5:
        t_note = st.text_input("Note / Memo", value="Transaction Details")

    if st.button("➕ Record Transaction To Ledger"):
        new_id = f"TXN-{len(st.session_state.transactions) + 8001}"
        new_row = pd.DataFrame([{
            "ID": new_id,
            "Date": str(t_date),
            "Category": t_cat,
            "Type": t_type,
            "Amount": float(t_amt),
            "Method": "Manual App Entry",
            "Status": "Cleared",
            "Note": t_note
        }])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_row], ignore_index=True)
        st.success(f"Transaction {new_id} Successfully Recorded!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.html("<div style='font-size:16px; font-weight:700; margin-bottom:10px;'>📋 Live System Ledger</div>")
    st.dataframe(st.session_state.transactions, use_container_width=True)

# ==============================================================================
# TAB 3: 🧠 MAMDANI FUZZY ANALYTICS MODULE
# ==============================================================================
elif nav_choice == "🧠 Mamdani Fuzzy Analytics":
    st.html("""
    <div class="glass-panel">
        <h2>🧠 Mamdani Fuzzy Inference Engine Diagnostics</h2>
        <p style="color:rgba(255,255,255,0.7);">Mathematical membership function degrees ($\mu$) for Expense, Savings, and Debt ratios.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.html(f"""
        <div class="glass-panel">
            <h4>Expense Ratio ({exp_ratio:.1f}%)</h4>
            <p>• Low Set ($\mu$): <b>{fz_mems['exp']['Low']:.2f}</b></p>
            <p>• Medium Set ($\mu$): <b>{fz_mems['exp']['Med']:.2f}</b></p>
            <p>• High Set ($\mu$): <b>{fz_mems['exp']['High']:.2f}</b></p>
        </div>
        """)
    with fc2:
        st.html(f"""
        <div class="glass-panel">
            <h4>Savings Ratio ({sav_ratio:.1f}%)</h4>
            <p>• Poor Set ($\mu$): <b>{fz_mems['sav']['Poor']:.2f}</b></p>
            <p>• Moderate Set ($\mu$): <b>{fz_mems['sav']['Mod']:.2f}</b></p>
            <p>• Good Set ($\mu$): <b>{fz_mems['sav']['Good']:.2f}</b></p>
        </div>
        """)
    with fc3:
        st.html(f"""
        <div class="glass-panel">
            <h4>Debt Ratio ({dbt_ratio:.1f}%)</h4>
            <p>• Low Set ($\mu$): <b>{fz_mems['dbt']['Low']:.2f}</b></p>
            <p>• Medium Set ($\mu$): <b>{fz_mems['dbt']['Med']:.2f}</b></p>
            <p>• High Set ($\mu$): <b>{fz_mems['dbt']['High']:.2f}</b></p>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.html("<div style='font-size:18px; font-weight:700;'>🔥 Rule Base Activation Strengths</div>")
    rule_df = pd.DataFrame({
        "Rule Consequent": list(fz_rules.keys()),
        "Firing Strength": list(fz_rules.values())
    }).set_index("Rule Consequent")
    st.bar_chart(rule_df)

# ==============================================================================
# TAB 4: 🔮 WEALTH PREDICTIONS & SIP MODULE
# ==============================================================================
elif nav_choice == "🔮 Wealth Predictions & SIP":
    st.html("""
    <div class="glass-panel">
        <h2>🔮 Wealth Growth & Compound Investment Simulator</h2>
        <p style="color:rgba(255,255,255,0.7);">Project long-term portfolio growth using monthly compounding models.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        sip_amt = st.number_input("Monthly SIP Contribution (₹)", value=inv_tot if inv_tot > 0.0 else 18000.0, step=1000.0)
    with pc2:
        rate = st.slider("Expected Annual Return CAGR (%)", 1.0, 25.0, 12.0)
    with pc3:
        years = st.slider("Investment Horizon (Years)", 1, 30, 10)

    m_count = years * 12
    r_monthly = (rate / 100.0) / 12.0
    timeline = []
    curr = 0.0
    for m in range(1, m_count + 1):
        curr = (curr + sip_amt) * (1.0 + r_monthly)
        timeline.append(curr)

    line_df = pd.DataFrame({"Month": range(1, m_count + 1), "Corpus Growth (₹)": timeline}).set_index("Month")
    st.line_chart(line_df)
    st.success(f"🎯 **Projected Portfolio Value after {years} Years:** ₹{timeline[-1]:,.2f}")

# ==============================================================================
# TAB 5: ✨ AI COPILOT ADVISOR MODULE
# ==============================================================================
elif nav_choice == "✨ AI Copilot Advisor":
    st.html("""
    <div class="glass-panel">
        <h2>✨ FinWise Conversational AI Copilot</h2>
        <p style="color:rgba(255,255,255,0.7);">Ask specific wealth management, tax optimization, and investment strategy questions.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    user_q = st.text_area("Your Financial Inquiry:", value="How can I optimize tax planning while building my long-term retirement corpus?")
    if st.button("💬 Ask AI Copilot"):
        with st.spinner("Analyzing profile and generating strategy..."):
            ans = get_ai_advice(user_q, inc_tot, exp_tot, inv_tot, dbt_tot, fz_score, fz_cat)
            st.session_state.chat_history.append({"q": user_q, "a": ans})

    for chat in reversed(st.session_state.chat_history):
        st.html(f"""
        <div class="glass-panel" style="margin-bottom:14px;">
            <b>Q: {chat['q']}</b>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="font-size:13px; color:rgba(255,255,255,0.85); line-height:1.6;">{chat['a']}</div>
        </div>
        """)

# ==============================================================================
# TAB 6: 📜 TRANSACTION AUDIT LOG MODULE
# ==============================================================================
elif nav_choice == "📜 Transaction Audit Log":
    st.html("""
    <div class="glass-panel">
        <h2>📜 Transaction Audit Trail & Exporter</h2>
        <p style="color:rgba(255,255,255,0.7);">Inspect complete historical records and download official CSV ledger exports.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(st.session_state.transactions, use_container_width=True)

    csv = st.session_state.transactions.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Audit Ledger CSV", data=csv, file_name=f"FinWise_Ledger_{datetime.date.today()}.csv", mime="text/csv")

# ==============================================================================
# TAB 7: ⚙️ SETTINGS & PROFILE MODULE
# ==============================================================================
elif nav_choice == "⚙️ Settings & Profile":
    st.html("""
    <div class="glass-panel">
        <h2>⚙️ Account Profile & Target Financial Goals</h2>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    st.text_input("Legal Account Owner Name:", value=AUTHOR_NAME)
    st.selectbox("Base Operating Currency:", ["INR (₹)", "USD ($)", "EUR (€)"])

    st.markdown("### 🎯 Target Financial Goals")
    st.dataframe(st.session_state.financial_goals, use_container_width=True)

    api_status = "Connected ✅" if os.getenv("GOOGLE_API_KEY") else "Missing Key (Using Rule Engine) ⚠️"
    st.info(f"LangChain Gemini LLM Connection Status: {api_status}")

# ==============================================================================
# SECTION 7: SYSTEM FOOTER
# ==============================================================================
st.html(f"""
<div style="text-align:center; padding:30px 0 10px 0; font-size:11px; color:rgba(255,255,255,0.5);">
    {APP_NAME} Enterprise Suite v{APP_VERSION} ({APP_BUILD}) &nbsp;|&nbsp; Developed for Assessment &nbsp;|&nbsp; Powered by Streamlit, Mamdani Fuzzy Engine & LangChain AI ❤️
</div>
""")