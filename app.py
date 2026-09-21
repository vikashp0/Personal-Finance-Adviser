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
        {"ID": "TXN-8001", "Date": "2026-09-01", "Category": "Base Salary", "Type": "Income", "Amount": 70000.0, "Method": "Direct Deposit / Bank", "Status": "Cleared", "Note": "Monthly Corporate Payroll Credit"},
        {"ID": "TXN-8002", "Date": "2026-09-02", "Category": "Housing & Rent", "Type": "Expense", "Amount": 18000.0, "Method": "UPI Direct", "Status": "Cleared", "Note": "Apartment Maintenance & Monthly Rent"},
        {"ID": "TXN-8003", "Date": "2026-09-03", "Category": "Groceries & Supplies", "Type": "Expense", "Amount": 8500.0, "Method": "Credit Card", "Status": "Cleared", "Note": "Supermarket Restock & Household Items"},
        {"ID": "TXN-8004", "Date": "2026-09-05", "Category": "Index Mutual Funds", "Type": "Investment", "Amount": 18000.0, "Method": "Auto-Debit SIP", "Status": "Cleared", "Note": "Nifty 50 Index Fund Systematic Plan"},
        {"ID": "TXN-8005", "Date": "2026-09-07", "Category": "Utilities & Internet", "Type": "Expense", "Amount": 3800.0, "Method": "UPI Direct", "Status": "Cleared", "Note": "Electricity, Water, & Fiber Broadband"},
        {"ID": "TXN-8006", "Date": "2026-09-10", "Category": "Vehicle Loan EMI", "Type": "Debt", "Amount": 6500.0, "Method": "Auto-Debit", "Status": "Cleared", "Note": "Bank Car Loan Fixed Installment"},
        {"ID": "TXN-8007", "Date": "2026-09-12", "Category": "Dining & Leisure", "Type": "Expense", "Amount": 4500.0, "Method": "Credit Card", "Status": "Cleared", "Note": "Weekend Dinners & Entertainment"},
        {"ID": "TXN-8008", "Date": "2026-09-15", "Category": "Freelance Design", "Type": "Income", "Amount": 15000.0, "Method": "Wire Transfer", "Status": "Cleared", "Note": "UI/UX Design Client Project Fee"},
        {"ID": "TXN-8009", "Date": "2026-09-18", "Category": "Tech Subscriptions", "Type": "Expense", "Amount": 2200.0, "Method": "Credit Card", "Status": "Cleared", "Note": "Cloud Services & Software Licenses"},
        {"ID": "TXN-8010", "Date": "2026-09-20", "Category": "Emergency Fund Deposit", "Type": "Investment", "Amount": 5000.0, "Method": "Bank Transfer", "Status": "Cleared", "Note": "High-Yield Savings Deposit"}
    ])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "financial_goals" not in st.session_state:
    st.session_state.financial_goals = pd.DataFrame([
        {"Goal ID": "G-101", "Goal Name": "Emergency Liquid Cushion", "Category": "Risk Reserve", "Target Amount (₹)": 250000.0, "Current Saved (₹)": 160000.0, "Target Date": "2027-03-31", "Priority": "High"},
        {"Goal ID": "G-102", "Goal Name": "International Tech Summit", "Category": "Travel & Learning", "Target Amount (₹)": 180000.0, "Current Saved (₹)": 75000.0, "Target Date": "2027-08-15", "Priority": "Medium"},
        {"Goal ID": "G-103", "Goal Name": "Long-Term Retirement SIP", "Category": "Wealth Corpus", "Target Amount (₹)": 5000000.0, "Current Saved (₹)": 650000.0, "Target Date": "2032-12-31", "Priority": "Critical"}
    ])

# ==============================================================================
# SECTION 3: MAMDANI FUZZY LOGIC MATHEMATICAL ENGINE
# ==============================================================================
def trimf(x, a, b, c):
    if x <= a or x >= c: return 0.0
    if a < x <= b: return (x - a) / (b - a) if b != a else 1.0
    if b < x < c: return (c - x) / (c - b) if c != b else 1.0
    return 0.0

def trapmf(x, a, b, c, d):
    if x <= a or x >= d: return 0.0
    if a <= x <= b: return (x - a) / (b - a) if b != a else 1.0
    if b <= x <= c: return 1.0
    if c <= x <= d: return (d - x) / (d - c) if d != c else 1.0
    return 0.0

def evaluate_fuzzy_health(exp_ratio, sav_ratio, dbt_ratio):
    exp_low = trapmf(exp_ratio, 0.0, 0.0, 30.0, 50.0)
    exp_med = trimf(exp_ratio, 40.0, 55.0, 70.0)
    exp_high = trapmf(exp_ratio, 60.0, 80.0, 100.0, 100.0)

    sav_poor = trapmf(sav_ratio, 0.0, 0.0, 10.0, 20.0)
    sav_mod = trimf(sav_ratio, 15.0, 25.0, 35.0)
    sav_good = trapmf(sav_ratio, 30.0, 45.0, 100.0, 100.0)

    dbt_low = trapmf(dbt_ratio, 0.0, 0.0, 15.0, 30.0)
    dbt_med = trimf(dbt_ratio, 20.0, 35.0, 50.0)
    dbt_high = trapmf(dbt_ratio, 40.0, 60.0, 100.0, 100.0)

    rules = {"Poor": 0.0, "Fair": 0.0, "Good": 0.0, "Excellent": 0.0}

    r1 = min(exp_low, sav_good, dbt_low)
    rules["Excellent"] = max(rules["Excellent"], r1)

    r2 = min(exp_med, sav_mod, dbt_low)
    rules["Good"] = max(rules["Good"], r2)

    r3 = max(exp_high, dbt_high)
    rules["Poor"] = max(rules["Poor"], r3)

    r4 = min(exp_med, sav_poor)
    rules["Fair"] = max(rules["Fair"], r4)

    r5 = min(sav_good, dbt_med)
    rules["Good"] = max(rules["Good"], r5)

    r6 = min(exp_low, sav_mod)
    rules["Good"] = max(rules["Good"], r6)

    r7 = min(dbt_high, sav_poor)
    rules["Poor"] = max(rules["Poor"], r7)

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

    if score >= 80.0: category = "Excellent"
    elif score >= 60.0: category = "Good"
    elif score >= 40.0: category = "Fair"
    else: category = "Poor"

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

Provide a structured, executive financial advisory report.
"""
        prompt = PromptTemplate(
            input_variables=["inc", "exp", "sav", "dbt", "score", "cat", "query"],
            template=template
        )

        chain = prompt | llm
        res = chain.invoke({
            "inc": inc, "exp": exp, "sav": sav, "dbt": dbt,
            "score": score, "cat": cat,
            "query": query if query else "Provide a comprehensive financial health and wealth optimization report"
        })
        return res.content
    except Exception as e:
        return f"**Mamdani Evaluation Score:** {score}/100 ({cat}). Focus on reducing high-interest debt and boosting systematic SIP investments."

# ==============================================================================
# SECTION 5: FUTURISTIC IOS LIQUID GLASS OVERRIDE CSS ENGINE
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Base Wallpaper Background */
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

/* OVERRIDE STREAMLIT DEFAULT BLACK BACKGROUNDS ON INPUTS & TABLES */
.stNumberInput div[data-baseweb="input"], 
.stTextInput div[data-baseweb="input"], 
.stSelectbox div[data-baseweb="select"], 
.stTextArea div[data-baseweb="textarea"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    color: #ffffff !important;
}

.stNumberInput input, .stTextInput input, .stTextArea textarea {
    color: #ffffff !important;
    background: transparent !important;
}

/* DATAFRAME GLASSMORPHISM OVERRIDE */
div[data-testid="stDataFrame"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(25px) !important;
    padding: 8px !important;
}

div[data-testid="stDataFrame"] * {
    background: transparent !important;
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
}

/* NATIVE CHART CONTAINER OVERRIDE */
[data-testid="stVegaLiteChart"], [data-testid="stLineChart"] {
    background: transparent !important;
    border: none !important;
}

/* iOS Glass Card Panel */
.glass-panel, .top-metric-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    backdrop-filter: blur(40px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(200%) !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
    border-radius: 24px !important;
    padding: 24px;
}

.metric-badge {
    width: 46px; height: 46px; border-radius: 16px;
    display: flex; align-items: center; justify-content: center; font-size: 22px;
    margin-bottom: 12px;
}

.bg-green { background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); }
.bg-pink { background: rgba(244, 63, 94, 0.25); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4); box-shadow: 0 0 20px rgba(244, 63, 94, 0.3); }
.bg-blue { background: rgba(59, 130, 246, 0.25); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
.bg-purple { background: rgba(139, 92, 246, 0.25); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.4); box-shadow: 0 0 20px rgba(139, 92, 246, 0.3); }

.top-metric-label { font-size: 11px; color: rgba(255,255,255,0.7); font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; }
.top-metric-val { font-size: 28px; font-weight: 800; color: #ffffff; margin: 4px 0 2px 0; }

/* SIDEBAR NAVIGATION CLEAN RADIO BUTTONS */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.02) 100%) !important;
    backdrop-filter: blur(40px) saturate(200%) !important;
    border-right: 1px solid rgba(255,255,255,0.18) !important;
}

div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] { gap: 10px !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 16px !important;
    padding: 12px 18px !important;
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    width: 100% !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label input[type="radio"],
div[data-testid="stRadio"] div[role="radiogroup"] label div[data-aria-hidden="true"],
div[data-testid="stRadio"] div[role="radiogroup"] label svg {
    display: none !important;
}

/* HIGH-END FUTURISTIC LIQUID GLASS GRAPH CSS */
.ios-chart-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 28px;
    backdrop-filter: blur(30px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);
    margin-top: 15px;
}

.chart-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 25px; }
.chart-title { font-size: 18px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 10px; }
.chart-row { margin-bottom: 20px; }
.chart-label-group { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 14px; font-weight: 700; }
.chart-track { width: 100%; height: 18px; background: rgba(255, 255, 255, 0.06); border-radius: 30px; overflow: hidden; padding: 2px; border: 1px solid rgba(255, 255, 255, 0.1); }
.chart-fill { height: 100%; border-radius: 30px; transition: width 1.2s cubic-bezier(0.34, 1.56, 0.64, 1); }

.fill-income { background: linear-gradient(90deg, #10b981 0%, #34d399 100%); box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
.fill-expense { background: linear-gradient(90deg, #f43f5e 0%, #fb7185 100%); box-shadow: 0 0 20px rgba(244, 63, 94, 0.6); }
.fill-investment { background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%); box-shadow: 0 0 20px rgba(59, 130, 246, 0.6); }
.fill-debt { background: linear-gradient(90deg, #8b5cf6 0%, #c084fc 100%); box-shadow: 0 0 20px rgba(139, 92, 246, 0.6); }

.stButton > button {
    width: 100%; border-radius: 16px; padding: 16px; font-size: 16px; font-weight: 700; color: #ffffff;
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 0 30px rgba(37, 99, 235, 0.6) !important;
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

# COMPUTATION OF AGGREGATES
df_trans = st.session_state.transactions
inc_tot = df_trans[df_trans["Type"] == "Income"]["Amount"].sum()
exp_tot = df_trans[df_trans["Type"] == "Expense"]["Amount"].sum()
inv_tot = df_trans[df_trans["Type"] == "Investment"]["Amount"].sum()
dbt_tot = df_trans[df_trans["Type"] == "Debt"]["Amount"].sum()

if inc_tot == 0.0: inc_tot = 1.0

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
    with m1: st.html(f'<div class="top-metric-card"><div class="metric-badge bg-green">💼</div><div class="top-metric-label">Total Monthly Income</div><div class="top-metric-val">₹{inc_tot:,.2f}</div></div>')
    with m2: st.html(f'<div class="top-metric-card"><div class="metric-badge bg-pink">💳</div><div class="top-metric-label">Total Expenses</div><div class="top-metric-val">₹{exp_tot:,.2f}</div></div>')
    with m3: st.html(f'<div class="top-metric-card"><div class="metric-badge bg-blue">📈</div><div class="top-metric-label">Investments & SIPs</div><div class="top-metric-val">₹{inv_tot:,.2f}</div></div>')
    with m4: st.html(f'<div class="top-metric-card"><div class="metric-badge bg-purple">🏦</div><div class="top-metric-label">Debt Obligations</div><div class="top-metric-val">₹{dbt_tot:,.2f}</div></div>')

    # HIGH-END FUTURISTIC LIQUID GLASS GRAPH
    max_val = max(inc_tot, exp_tot, inv_tot, dbt_tot, 1.0)
    inc_pct = (inc_tot / max_val) * 100
    exp_pct = (exp_tot / max_val) * 100
    inv_pct = (inv_tot / max_val) * 100
    dbt_pct = (dbt_tot / max_val) * 100

    st.html(f"""
    <div class="ios-chart-card">
        <div class="chart-header">
            <div class="chart-title">📊 Monthly Liquid Cashflow Analytics</div>
            <div style="font-size:12px; color:#34d399; font-weight:700;">● Live Ledger Synced</div>
        </div>
        
        <div class="chart-row">
            <div class="chart-label-group">
                <span style="color:#34d399;">💼 Income</span>
                <span>₹{inc_tot:,.2f} ({inc_pct:.1f}%)</span>
            </div>
            <div class="chart-track">
                <div class="chart-fill fill-income" style="width: {inc_pct}%;"></div>
            </div>
        </div>

        <div class="chart-row">
            <div class="chart-label-group">
                <span style="color:#fb7185;">💳 Expenses</span>
                <span>₹{exp_tot:,.2f} ({exp_pct:.1f}%)</span>
            </div>
            <div class="chart-track">
                <div class="chart-fill fill-expense" style="width: {exp_pct}%;"></div>
            </div>
        </div>

        <div class="chart-row">
            <div class="chart-label-group">
                <span style="color:#60a5fa;">📈 Investments</span>
                <span>₹{inv_tot:,.2f} ({inv_pct:.1f}%)</span>
            </div>
            <div class="chart-track">
                <div class="chart-fill fill-investment" style="width: {inv_pct}%;"></div>
            </div>
        </div>

        <div class="chart-row">
            <div class="chart-label-group">
                <span style="color:#c084fc;">🏦 Debt Obligations</span>
                <span>₹{dbt_tot:,.2f} ({dbt_pct:.1f}%)</span>
            </div>
            <div class="chart-track">
                <div class="chart-fill fill-debt" style="width: {dbt_pct}%;"></div>
            </div>
        </div>
    </div>
    """)

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
    st.html('<div class="glass-panel"><h2>💳 Transaction & Cashflow Ledger</h2><p style="color:rgba(255,255,255,0.7);">Record transactions to update metrics real-time.</p></div>')
    st.markdown("<br>", unsafe_allow_html=True)

    t_c1, t_c2, t_c3, t_c4, t_c5 = st.columns([2, 2, 2, 2, 3])
    with t_c1: t_date = st.date_input("Date", datetime.date.today())
    with t_c2: t_type = st.selectbox("Type", ["Income", "Expense", "Investment", "Debt"])
    with t_c3: t_cat = st.text_input("Category", value="General Outflow")
    with t_c4: t_amt = st.number_input("Amount (₹)", min_value=1.0, value=2500.0, step=500.0)
    with t_c5: t_note = st.text_input("Note", value="Details")

    if st.button("➕ Record Transaction To Ledger"):
        new_id = f"TXN-{len(st.session_state.transactions) + 8001}"
        new_row = pd.DataFrame([{"ID": new_id, "Date": str(t_date), "Category": t_cat, "Type": t_type, "Amount": float(t_amt), "Method": "Manual Entry", "Status": "Cleared", "Note": t_note}])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_row], ignore_index=True)
        st.success(f"Transaction {new_id} Successfully Recorded!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(st.session_state.transactions, use_container_width=True)

# ==============================================================================
# TAB 3: 🧠 MAMDANI FUZZY ANALYTICS MODULE
# ==============================================================================
elif nav_choice == "🧠 Mamdani Fuzzy Analytics":
    st.html('<div class="glass-panel"><h2>🧠 Mamdani Fuzzy Inference Engine Diagnostics</h2><p style="color:rgba(255,255,255,0.7);">Membership degree ($\mu$) evaluation.</p></div>')
    st.markdown("<br>", unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1: st.html(f'<div class="glass-panel"><h4>Expense Ratio ({exp_ratio:.1f}%)</h4><p>• Low: <b>{fz_mems["exp"]["Low"]:.2f}</b></p><p>• Medium: <b>{fz_mems["exp"]["Med"]:.2f}</b></p><p>• High: <b>{fz_mems["exp"]["High"]:.2f}</b></p></div>')
    with fc2: st.html(f'<div class="glass-panel"><h4>Savings Ratio ({sav_ratio:.1f}%)</h4><p>• Poor: <b>{fz_mems["sav"]["Poor"]:.2f}</b></p><p>• Moderate: <b>{fz_mems["sav"]["Mod"]:.2f}</b></p><p>• Good: <b>{fz_mems["sav"]["Good"]:.2f}</b></p></div>')
    with fc3: st.html(f'<div class="glass-panel"><h4>Debt Ratio ({dbt_ratio:.1f}%)</h4><p>• Low: <b>{fz_mems["dbt"]["Low"]:.2f}</b></p><p>• Medium: <b>{fz_mems["dbt"]["Med"]:.2f}</b></p><p>• High: <b>{fz_mems["dbt"]["High"]:.2f}</b></p></div>')

# ==============================================================================
# TAB 4: 🔮 WEALTH PREDICTIONS & SIP MODULE (INTERACTIVE GLASS GRAPH)
# ==============================================================================
elif nav_choice == "🔮 Wealth Predictions & SIP":
    st.html('<div class="glass-panel"><h2>🔮 Wealth Growth & Compound Investment Simulator</h2></div>')
    st.markdown("<br>", unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3)
    with pc1: sip_amt = st.number_input("Monthly SIP (₹)", value=inv_tot if inv_tot > 0.0 else 18000.0, step=1000.0)
    with pc2: rate = st.slider("Expected Return (%)", 1.0, 25.0, 12.0)
    with pc3: years = st.slider("Horizon (Years)", 1, 30, 10)

    m_count = years * 12
    r_monthly = (rate / 100.0) / 12.0
    timeline, curr = [], 0.0
    for m in range(1, m_count + 1):
        curr = (curr + sip_amt) * (1.0 + r_monthly)
        timeline.append(curr)

    # FUTURISTIC INTERACTIVE LIQUID GLASS SVG LINE GRAPH
    max_corpus = timeline[-1]
    svg_points = []
    width, height = 900, 260
    for idx, val in enumerate(timeline):
        x = (idx / (m_count - 1)) * width if m_count > 1 else 0
        y = height - ((val / max_corpus) * (height - 30)) - 15
        svg_points.append(f"{x:.1f},{y:.1f}")

    points_str = " ".join(svg_points)

    st.html(f"""
    <div class="ios-chart-card" style="margin-top:10px;">
        <div class="chart-header">
            <div class="chart-title">📈 Projected Portfolio Curve</div>
            <div style="font-size:13px; color:#60a5fa; font-weight:700;">Target: ₹{max_corpus:,.2f}</div>
        </div>
        <div style="width:100%; overflow-x:auto;">
            <svg viewBox="0 0 900 260" style="width:100%; height:260px;">
                <defs>
                    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#3b82f6" />
                        <stop offset="50%" stop-color="#a855f7" />
                        <stop offset="100%" stop-color="#34d399" />
                    </linearGradient>
                    <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="rgba(168, 85, 247, 0.4)" />
                        <stop offset="100%" stop-color="rgba(168, 85, 247, 0.0)" />
                    </linearGradient>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                <polygon points="0,260 {points_str} 900,260" fill="url(#areaGrad)" />
                <polyline points="{points_str}" fill="none" stroke="url(#lineGrad)" stroke-width="4" filter="url(#glow)" />
            </svg>
        </div>
    </div>
    """)
    st.success(f"🎯 **Projected Portfolio Value after {years} Years:** ₹{max_corpus:,.2f}")

# ==============================================================================
# TAB 5: ✨ AI COPILOT ADVISOR MODULE
# ==============================================================================
elif nav_choice == "✨ AI Copilot Advisor":
    st.html('<div class="glass-panel"><h2>✨ FinWise Conversational AI Copilot</h2></div>')
    st.markdown("<br>", unsafe_allow_html=True)

    user_q = st.text_area("Your Inquiry:", value="How can I optimize tax planning while building my retirement corpus?")
    if st.button("💬 Ask AI Copilot"):
        with st.spinner("Analyzing profile..."):
            ans = get_ai_advice(user_q, inc_tot, exp_tot, inv_tot, dbt_tot, fz_score, fz_cat)
            st.session_state.chat_history.append({"q": user_q, "a": ans})

    for chat in reversed(st.session_state.chat_history):
        st.html(f'<div class="glass-panel" style="margin-bottom:14px;"><b>Q: {chat["q"]}</b><hr style="border-color:rgba(255,255,255,0.1);"><div>{chat["a"]}</div></div>')

# ==============================================================================
# TAB 6: 📜 TRANSACTION AUDIT LOG MODULE
# ==============================================================================
elif nav_choice == "📜 Transaction Audit Log":
    st.html('<div class="glass-panel"><h2>📜 Transaction Audit Trail & Exporter</h2></div>')
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(st.session_state.transactions, use_container_width=True)
    csv = st.session_state.transactions.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Audit Ledger CSV", data=csv, file_name="Ledger.csv", mime="text/csv")

# ==============================================================================
# TAB 7: ⚙️ SETTINGS & PROFILE MODULE
# ==============================================================================
elif nav_choice == "⚙️ Settings & Profile":
    st.html('<div class="glass-panel"><h2>⚙️ Account Profile & Target Goals</h2></div>')
    st.markdown("<br>", unsafe_allow_html=True)
    st.text_input("Name:", value=AUTHOR_NAME)
    st.selectbox("Currency:", ["INR (₹)", "USD ($)", "EUR (€)"])
    st.dataframe(st.session_state.financial_goals, use_container_width=True)
    st.info(f"LangChain Gemini LLM Status: {'Connected ✅' if os.getenv('GOOGLE_API_KEY') else 'Missing API Key ⚠️'}")

# FOOTER
st.html(f'<div style="text-align:center; padding:30px 0; font-size:11px; color:rgba(255,255,255,0.5);">{APP_NAME} Enterprise Suite v{APP_VERSION} | Powered by Streamlit, Mamdani Engine & LangChain AI</div>')