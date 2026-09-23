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
    initial_sidebar_state="collapsed"
)

# Application Metadata Constants & Versioning Information
APP_NAME = "FinWise Pro"
APP_VERSION = "2026.4.0"
APP_BUILD = "Build-8921-Enterprise"
AUTHOR_NAME = "Vikas Ramsevak Pal"
PLATFORM_TAG = "iOS Liquid Glass Enterprise Suite"

# ==============================================================================
# SECTION 2: APPLICATION STATE & DATABASE INITIALIZATION SIMULATION
# ==============================================================================
if "app_initialized" not in st.session_state:
    st.session_state.app_initialized = True
    st.session_state.init_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "income" not in st.session_state:
    st.session_state.income = 70000.0

if "expenses" not in st.session_state:
    st.session_state.expenses = 30300.0

if "savings" not in st.session_state:
    st.session_state.savings = 23000.0

if "debt" not in st.session_state:
    st.session_state.debt = 6500.0

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
            "Type": "Expense",
            "Amount": 3800.0,
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

# ==============================================================================
# SECTION 3: MAMDANI FUZZY LOGIC MATHEMATICAL ENGINE
# ==============================================================================
def trimf(x, a, b, c):
    """Triangular Membership Function for Fuzzy Sets"""
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    if b < x < c:
        return (c - x) / (c - b) if c != b else 1.0
    return 0.0

def trapmf(x, a, b, c, d):
    """Trapezoidal Membership Function for Fuzzy Sets"""
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
    """Computes Mamdani Fuzzy Inference Engine Score and Category with Rule Base."""
    exp_low = trapmf(exp_ratio, 0.0, 0.0, 30.0, 50.0)
    exp_med = trimf(exp_ratio, 40.0, 55.0, 70.0)
    exp_high = trapmf(exp_ratio, 60.0, 80.0, 100.0, 100.0)

    sav_poor = trapmf(sav_ratio, 0.0, 0.0, 10.0, 20.0)
    sav_mod = trimf(sav_ratio, 15.0, 25.0, 35.0)
    sav_good = trapmf(sav_ratio, 30.0, 45.0, 100.0, 100.0)

    dbt_low = trapmf(dbt_ratio, 0.0, 0.0, 15.0, 30.0)
    dbt_med = trimf(dbt_ratio, 20.0, 35.0, 50.0)
    dbt_high = trapmf(dbt_ratio, 40.0, 60.0, 100.0, 100.0)

    rules = {
        "Poor": 0.0,
        "Fair": 0.0,
        "Good": 0.0,
        "Excellent": 0.0
    }

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
    """Interfaces with LangChain and Google GenAI Gemini-2.5-flash for advisory."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return f"""
### 📊 FinWise Automated Health Assessment
* **Mamdani Fuzzy Rating:** **{score}/100 ({cat})**
* **Monthly Income:** ₹{inc:,.2f} | **Expenses:** ₹{exp:,.2f}
* **Investments/Savings:** ₹{sav:,.2f} | **Debt Obligations:** ₹{dbt:,.2f}

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

Provide a structured, executive financial advisory report with clear, actionable bullet points.
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
        return f"**Mamdani Evaluation Score:** {score}/100 ({cat}). Focus on reducing high-interest debt and boosting systematic SIP investments. Error: {str(e)}"

# ==============================================================================
# SECTION 5: ULTRA RESPONSIVE iOS LIQUID GLASS CSS ENGINE
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"], .main {
    max-width: 100vw !important;
    overflow-x: hidden !important;
    touch-action: pan-y !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: 
        radial-gradient(circle at 12% 15%, rgba(16, 185, 129, 0.28), transparent 40%),
        radial-gradient(circle at 85% 18%, rgba(139, 92, 246, 0.35), transparent 45%),
        radial-gradient(circle at 50% 80%, rgba(59, 130, 246, 0.30), transparent 50%),
        radial-gradient(circle at 80% 85%, rgba(244, 63, 94, 0.20), transparent 45%),
        linear-gradient(135deg, #050b18 0%, #0a1128 50%, #030712 100%) !important;
    color: #ffffff !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { 
    padding-top: 1rem !important; 
    padding-bottom: 2rem !important; 
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
    max-width: 100vw !important; 
}

div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(40px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(200%) !important;
    padding: 20px !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
    width: 100% !important;
}

/* ABSOLUTE CONTRAST OVERRIDE FOR ALL STREAMLIT INPUT FIELDS ACROSS ALL THEMES */
div[data-baseweb="input"], div[data-baseweb="base-input"], .stNumberInput input, .stTextInput input, .stTextArea textarea {
    background-color: rgba(10, 15, 35, 0.95) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stNumberInput div[data-baseweb="input"], .stTextInput div[data-baseweb="input"], .stTextArea div[data-baseweb="textarea"], .stSelectbox div[data-baseweb="select"] {
    background: rgba(10, 15, 35, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    backdrop-filter: blur(30px) !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5) !important;
}

.stNumberInput button {
    background: rgba(255, 255, 255, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

div[data-testid="stDataFrame"], div[data-testid="stTable"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(40px) saturate(200%) !important;
    padding: 10px !important;
}
div[data-testid="stDataFrame"] * {
    background: transparent !important;
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
}

[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(50px) saturate(210%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
}

div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] { gap: 8px !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 16px !important;
    padding: 10px 14px !important;
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    width: 100% !important;
}

.liquid-glass-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-top: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(50px) saturate(210%);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45), inset 0 1px 2px rgba(255, 255, 255, 0.3);
    border-radius: 20px;
    padding: 18px;
    width: 100% !important;
    margin-bottom: 15px;
}

.metric-card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}

.metric-card-inner {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.10) 0%, rgba(255, 255, 255, 0.02) 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(40px) saturate(200%);
    border-radius: 18px;
    padding: 14px;
    box-shadow: 0 15px 30px rgba(0,0,0,0.35), inset 0 1px 1px rgba(255,255,255,0.25);
}

.metric-badge-box {
    width: 36px; height: 36px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center; font-size: 18px; margin-bottom: 8px;
}

.badge-green { background: rgba(16, 185, 129, 0.25); border: 1px solid rgba(16, 185, 129, 0.5); color: #34d399; }
.badge-pink { background: rgba(244, 63, 94, 0.25); border: 1px solid rgba(244, 63, 94, 0.5); color: #fb7185; }
.badge-blue { background: rgba(59, 130, 246, 0.25); border: 1px solid rgba(59, 130, 246, 0.5); color: #60a5fa; }
.badge-purple { background: rgba(139, 92, 246, 0.25); border: 1px solid rgba(139, 92, 246, 0.5); color: #c084fc; }

.metric-title { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.7); text-transform: uppercase; }
.metric-value { font-size: 22px; font-weight: 800; color: #ffffff; margin: 2px 0 4px 0; }

.stButton > button, div[data-testid="stFormSubmitButton"] > button {
    width: 100%; border-radius: 18px; padding: 14px; font-size: 15px; font-weight: 800; color: #ffffff;
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
}

@media screen and (max-width: 768px) {
    .metric-card-grid {
        grid-template-columns: repeat(2, 1fr) !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SECTION 6: NAVIGATION HUB & CONTROLLER
# ==============================================================================
nav_options = [
    "📊 Executive Dashboard",
    "💳 Expense & Income Manager",
    "🧠 Mamdani Fuzzy Analytics",
    "🔮 Wealth Predictions & SIP",
    "✨ AI Copilot Advisor",
    "📜 Transaction Audit Log",
    "⚙️ Settings & Profile"
]

if "active_nav" not in st.session_state:
    st.session_state.active_nav = nav_options[0]

st.markdown("<div style='font-size:10px; font-weight:800; color:#60a5fa; letter-spacing:1px; margin-bottom:6px; text-transform:uppercase;'>✨ Enterprise Navigation Hub</div>", unsafe_allow_html=True)
selected_tab = st.selectbox("Navigation Hub", nav_options, index=nav_options.index(st.session_state.active_nav), label_visibility="collapsed")
st.session_state.active_nav = selected_tab
nav_choice = selected_tab

with st.sidebar:
    st.html(f"""
    <div style="display:flex; align-items:center; gap:12px; padding:10px 5px 15px 5px;">
        <div style="width:40px; height:40px; border-radius:14px; background:linear-gradient(135deg, #2563eb, #7c3aed); display:flex; align-items:center; justify-content:center; font-size:20px; box-shadow:0 0 20px rgba(37,99,235,0.8);">💎</div>
        <div>
            <div style="font-size:20px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">{APP_NAME}</div>
            <div style="font-size:10px; color:rgba(255,255,255,0.6);">{PLATFORM_TAG}</div>
        </div>
    </div>
    """)
    st.markdown("---")
    st.markdown(f"<div style='font-size:12px; color:rgba(255,255,255,0.7); padding:4px;'>Active Module:<br><b>{nav_choice}</b></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.html(f"""
    <div style="padding:14px; border-radius:18px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); backdrop-filter:blur(30px);">
        <div style="font-size:10px; color:rgba(255,255,255,0.7); font-style:italic; margin-bottom:10px;">"A better financial future starts with better decisions."</div>
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:34px; height:34px; border-radius:50%; background:linear-gradient(135deg, #2563eb, #10b981); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:12px;">V</div>
            <div>
                <div style="font-size:13px; font-weight:700;">{AUTHOR_NAME}</div>
                <div style="font-size:10px; color:#34d399;">● Enterprise Pro User</div>
            </div>
        </div>
    </div>
    """)

# AGGREGATES CALCULATION
inc_tot = st.session_state.income
exp_tot = st.session_state.expenses
inv_tot = st.session_state.savings
dbt_tot = st.session_state.debt

exp_ratio = min((exp_tot / (inc_tot if inc_tot > 0 else 1.0)) * 100.0, 100.0)
sav_ratio = min((inv_tot / (inc_tot if inc_tot > 0 else 1.0)) * 100.0, 100.0)
dbt_ratio = min((dbt_tot / (inc_tot if inc_tot > 0 else 1.0)) * 100.0, 100.0)

fz_score, fz_cat, fz_rules, fz_mems = evaluate_fuzzy_health(exp_ratio, sav_ratio, dbt_ratio)

# ==============================================================================
# TAB 1: 📊 EXECUTIVE DASHBOARD MODULE
# ==============================================================================
if nav_choice == "📊 Executive Dashboard":
    h1, h2 = st.columns([3, 1.2])
    with h1:
        st.html("""
        <div style="margin-bottom:15px;">
            <div style="font-size:10px; font-weight:800; color:#60a5fa; letter-spacing:2px; text-transform:uppercase;">ENTERPRISE FINANCIAL INTELLIGENCE</div>
            <div style="font-size:36px; font-weight:800; color:#ffffff; margin:2px 0 6px 0; letter-spacing:-1px;">Executive Wealth & Health Dashboard</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.7);">Real-time Mamdani Fuzzy Logic Scoring & LangChain AI Advisory.</div>
        </div>
        """)
    with h2:
        st.html(f"""
        <div class="liquid-glass-card" style="text-align:center; padding:14px;">
            <div style="font-size:10px; color:rgba(255,255,255,0.6); font-weight:700;">FUZZY HEALTH RATING</div>
            <div style="font-size:30px; font-weight:800; color:#60a5fa;">{fz_score}/100</div>
            <div style="font-size:12px; font-weight:700; color:#c084fc;">{fz_cat}</div>
        </div>
        """)

    st.html(f"""
    <div class="metric-card-grid">
        <div class="metric-card-inner">
            <div class="metric-badge-box badge-green">💼</div>
            <div class="metric-title">Monthly Income</div>
            <div class="metric-value">₹{inc_tot:,.0f}</div>
        </div>
        <div class="metric-card-inner">
            <div class="metric-badge-box badge-pink">💳</div>
            <div class="metric-title">Monthly Expenses</div>
            <div class="metric-value">₹{exp_tot:,.0f}</div>
        </div>
        <div class="metric-card-inner">
            <div class="metric-badge-box badge-blue">📈</div>
            <div class="metric-title">Investments & SIPs</div>
            <div class="metric-value">₹{inv_tot:,.0f}</div>
        </div>
        <div class="metric-card-inner">
            <div class="metric-badge-box badge-purple">🏛️</div>
            <div class="metric-title">Debt Obligations</div>
            <div class="metric-value">₹{dbt_tot:,.0f}</div>
        </div>
    </div>
    """)

    # FLICKER-FREE INPUT FORM
    with st.form("exec_financial_form"):
        st.markdown("<div style='font-size:18px; font-weight:800; color:#ffffff; margin-bottom:12px;'>📊 Enter Your Financial Details</div>", unsafe_allow_html=True)
        i1, i2, i3, i4 = st.columns(4)
        with i1: new_inc = st.number_input("Monthly Income (₹)", min_value=0.0, value=float(st.session_state.income), step=1000.0)
        with i2: new_exp = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=float(st.session_state.expenses), step=500.0)
        with i3: new_sav = st.number_input("Monthly Savings (₹)", min_value=0.0, value=float(st.session_state.savings), step=500.0)
        with i4: new_dbt = st.number_input("Monthly Debt Payment (₹)", min_value=0.0, value=float(st.session_state.debt), step=500.0)

        submitted = st.form_submit_button("✨ Analyze My Finances")
        if submitted:
            st.session_state.income = new_inc
            st.session_state.expenses = new_exp
            st.session_state.savings = new_sav
            st.session_state.debt = new_dbt
            st.success("Financial Snapshot Updated Successfully!")

    # CASHFLOW GLASS BARS
    max_v = max(inc_tot, exp_tot, inv_tot, dbt_tot, 1.0)
    inc_p, exp_p, sav_p, dbt_p = (inc_tot/max_v)*100, (exp_tot/max_v)*100, (inv_tot/max_v)*100, (dbt_tot/max_v)*100

    st.html(f"""
    <div class="liquid-glass-card">
        <div style="font-size:16px; font-weight:800; margin-bottom:15px;">📊 Monthly Liquid Cashflow Analytics</div>
        
        <div style="margin-bottom:12px;">
            <div style="display:flex; justify-space-between; font-size:12px; font-weight:700; margin-bottom:4px;">
                <span style="color:#34d399;">💼 Income</span><span>₹{inc_tot:,.2f} ({inc_p:.1f}%)</span>
            </div>
            <div style="width:100%; height:14px; background:rgba(255,255,255,0.06); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
                <div style="width:{inc_p}%; height:100%; background:linear-gradient(90deg, #10b981, #34d399); border-radius:20px;"></div>
            </div>
        </div>

        <div style="margin-bottom:12px;">
            <div style="display:flex; justify-space-between; font-size:12px; font-weight:700; margin-bottom:4px;">
                <span style="color:#fb7185;">💳 Expenses</span><span>₹{exp_tot:,.2f} ({exp_p:.1f}%)</span>
            </div>
            <div style="width:100%; height:14px; background:rgba(255,255,255,0.06); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
                <div style="width:{exp_p}%; height:100%; background:linear-gradient(90deg, #f43f5e, #fb7185); border-radius:20px;"></div>
            </div>
        </div>

        <div style="margin-bottom:12px;">
            <div style="display:flex; justify-space-between; font-size:12px; font-weight:700; margin-bottom:4px;">
                <span style="color:#60a5fa;">📈 Investments</span><span>₹{inv_tot:,.2f} ({sav_p:.1f}%)</span>
            </div>
            <div style="width:100%; height:14px; background:rgba(255,255,255,0.06); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
                <div style="width:{sav_p}%; height:100%; background:linear-gradient(90deg, #3b82f6, #60a5fa); border-radius:20px;"></div>
            </div>
        </div>

        <div>
            <div style="display:flex; justify-space-between; font-size:12px; font-weight:700; margin-bottom:4px;">
                <span style="color:#c084fc;">🏛️ Debt Obligations</span><span>₹{dbt_tot:,.2f} ({dbt_p:.1f}%)</span>
            </div>
            <div style="width:100%; height:14px; background:rgba(255,255,255,0.06); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
                <div style="width:{dbt_p}%; height:100%; background:linear-gradient(90deg, #8b5cf6, #c084fc); border-radius:20px;"></div>
            </div>
        </div>
    </div>
    """)

# ==============================================================================
# TAB 2: 💳 EXPENSE & INCOME MANAGER MODULE
# ==============================================================================
elif nav_choice == "💳 Expense & Income Manager":
    st.html('<div class="liquid-glass-card"><h2>💳 Transaction & Cashflow Ledger</h2><p style="color:rgba(255,255,255,0.7);">Record transactions to update metrics real-time.</p></div>')
    
    t_c1, t_c2, t_c3, t_c4 = st.columns(4)
    with t_c1: t_date = st.date_input("Date", datetime.date.today())
    with t_c2: t_type = st.selectbox("Type", ["Income", "Expense", "Investment", "Debt"])
    with t_c3: t_cat = st.text_input("Category", value="General Outflow")
    with t_c4: t_amt = st.number_input("Amount (₹)", min_value=1.0, value=2500.0, step=500.0)

    if st.button("➕ Record Transaction To Ledger"):
        new_id = f"TXN-{len(st.session_state.transactions) + 8001}"
        new_row = pd.DataFrame([{"ID": new_id, "Date": str(t_date), "Category": t_cat, "Type": t_type, "Amount": float(t_amt), "Method": "Manual Entry", "Status": "Cleared", "Note": "Ledger Entry"}])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_row], ignore_index=True)
        st.success(f"Transaction {new_id} Successfully Recorded!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(st.session_state.transactions, use_container_width=True)

# ==============================================================================
# TAB 3: 🧠 MAMDANI FUZZY ANALYTICS MODULE
# ==============================================================================
elif nav_choice == "🧠 Mamdani Fuzzy Analytics":
    st.html('<div class="liquid-glass-card"><h2>🧠 Mamdani Fuzzy Inference Engine Diagnostics</h2><p style="color:rgba(255,255,255,0.7);">Membership degree ($\mu$) evaluation across sub-ratios.</p></div>')

    fc1, fc2, fc3 = st.columns(3)
    with fc1: st.html(f'<div class="liquid-glass-card"><h4>Expense Ratio ({exp_ratio:.1f}%)</h4><p>• Low: <b>{fz_mems["exp"]["Low"]:.2f}</b></p><p>• Medium: <b>{fz_mems["exp"]["Med"]:.2f}</b></p><p>• High: <b>{fz_mems["exp"]["High"]:.2f}</b></p></div>')
    with fc2: st.html(f'<div class="liquid-glass-card"><h4>Savings Ratio ({sav_ratio:.1f}%)</h4><p>• Poor: <b>{fz_mems["sav"]["Poor"]:.2f}</b></p><p>• Moderate: <b>{fz_mems["sav"]["Mod"]:.2f}</b></p><p>• Good: <b>{fz_mems["sav"]["Good"]:.2f}</b></p></div>')
    with fc3: st.html(f'<div class="liquid-glass-card"><h4>Debt Ratio ({dbt_ratio:.1f}%)</h4><p>• Low: <b>{fz_mems["dbt"]["Low"]:.2f}</b></p><p>• Medium: <b>{fz_mems["dbt"]["Med"]:.2f}</b></p><p>• High: <b>{fz_mems["dbt"]["High"]:.2f}</b></p></div>')

# ==============================================================================
# TAB 4: 🔮 WEALTH PREDICTIONS & SIP MODULE
# ==============================================================================
elif nav_choice == "🔮 Wealth Predictions & SIP":
    st.html('<div class="liquid-glass-card"><h2>🔮 Wealth Growth & Compound Investment Simulator</h2></div>')

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

    max_corpus = timeline[-1]
    svg_points = []
    width, height = 900, 220
    for idx, val in enumerate(timeline):
        x = (idx / (m_count - 1)) * width if m_count > 1 else 0
        y = height - ((val / max_corpus) * (height - 30)) - 15
        svg_points.append(f"{x:.1f},{y:.1f}")

    points_str = " ".join(svg_points)

    st.html(f"""
    <div class="liquid-glass-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
            <div style="font-size:16px; font-weight:800;">📈 Projected Portfolio Curve</div>
            <div style="font-size:13px; color:#60a5fa; font-weight:700;">Target: ₹{max_corpus:,.2f}</div>
        </div>
        <div style="width:100%; overflow-x:auto;">
            <svg viewBox="0 0 900 220" style="width:100%; height:220px;">
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
                </defs>
                <polygon points="0,220 {points_str} 900,220" fill="url(#areaGrad)" />
                <polyline points="{points_str}" fill="none" stroke="url(#lineGrad)" stroke-width="4" />
            </svg>
        </div>
    </div>
    """)
    st.success(f"🎯 **Projected Portfolio Value after {years} Years:** ₹{max_corpus:,.2f}")

# ==============================================================================
# TAB 5: ✨ AI COPILOT ADVISOR MODULE
# ==============================================================================
elif nav_choice == "✨ AI Copilot Advisor":
    st.html('<div class="liquid-glass-card"><h2>✨ FinWise Conversational AI Copilot</h2></div>')

    user_q = st.text_area("Your Financial Inquiry:", value="How can I optimize tax planning while building my retirement corpus?")
    if st.button("💬 Ask AI Copilot"):
        with st.spinner("Analyzing profile..."):
            ans = get_ai_advice(user_q, inc_tot, exp_tot, inv_tot, dbt_tot, fz_score, fz_cat)
            st.session_state.chat_history.append({"q": user_q, "a": ans})

    for chat in reversed(st.session_state.chat_history):
        st.html(f'<div class="liquid-glass-card" style="border-left:4px solid #3b82f6;"><b>Q: {chat["q"]}</b><hr style="border-color:rgba(255,255,255,0.1); margin:8px 0;"><div>{chat["a"]}</div></div>')

# ==============================================================================
# TAB 6: 📜 TRANSACTION AUDIT LOG MODULE
# ==============================================================================
elif nav_choice == "📜 Transaction Audit Log":
    st.html('<div class="liquid-glass-card"><h2>📜 Transaction Audit Trail & Exporter</h2></div>')
    st.dataframe(st.session_state.transactions, use_container_width=True)
    csv = st.session_state.transactions.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Audit Ledger CSV", data=csv, file_name="Ledger.csv", mime="text/csv")

# ==============================================================================
# SECTION 7: ⚙️ SETTINGS & PROFILE MODULE
# ==============================================================================
elif nav_choice == "⚙️ Settings & Profile":
    st.html('<div class="liquid-glass-card"><h2>⚙️ Account Profile & Target Goals</h2></div>')
    st.text_input("Name:", value=AUTHOR_NAME)
    st.selectbox("Currency:", ["INR (₹)", "USD ($)", "EUR (€)"])
    st.dataframe(st.session_state.financial_goals, use_container_width=True)
    st.info(f"LangChain Gemini LLM Status: {'Connected ✅' if os.getenv('GOOGLE_API_KEY') else 'Missing API Key ⚠️'}")

# ==============================================================================
# SECTION 8: APPLICATION FOOTER
# ==============================================================================
st.html(f'<div style="text-align:center; padding:20px 0; font-size:11px; color:rgba(255,255,255,0.5);">{APP_NAME} Suite v{APP_VERSION} | Powered by Streamlit, Mamdani Engine & LangChain AI</div>')