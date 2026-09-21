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
    page_title="FinWise Pro - Liquid iOS Glass Adviser",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "FinWise"
AUTHOR_NAME = "Vikas Ramsevak Pal"

# ==============================================================================
# SECTION 2: APPLICATION STATE MANAGEMENT
# ==============================================================================
if "income" not in st.session_state:
    st.session_state.income = 30000.0
if "expenses" not in st.session_state:
    st.session_state.expenses = 20000.0
if "savings" not in st.session_state:
    st.session_state.savings = 5000.0
if "debt" not in st.session_state:
    st.session_state.debt = 2000.0

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"ID": "TXN-8001", "Date": "2026-09-01", "Category": "Base Salary", "Type": "Income", "Amount": 30000.0, "Method": "Direct Deposit / Bank", "Status": "Cleared", "Note": "Monthly Corporate Payroll Credit"},
        {"ID": "TXN-8002", "Date": "2026-09-02", "Category": "Housing & Rent", "Type": "Expense", "Amount": 12000.0, "Method": "UPI Direct", "Status": "Cleared", "Note": "Apartment Maintenance & Monthly Rent"},
        {"ID": "TXN-8003", "Date": "2026-09-03", "Category": "Groceries & Supplies", "Type": "Expense", "Amount": 8000.0, "Method": "Credit Card", "Status": "Cleared", "Note": "Supermarket Restock & Household Items"},
        {"ID": "TXN-8004", "Date": "2026-09-05", "Category": "Index Mutual Funds", "Type": "Investment", "Amount": 5000.0, "Method": "Auto-Debit SIP", "Status": "Cleared", "Note": "Nifty 50 Index Fund Systematic Plan"},
        {"ID": "TXN-8006", "Date": "2026-09-10", "Category": "Vehicle Loan EMI", "Type": "Debt", "Amount": 2000.0, "Method": "Auto-Debit", "Status": "Cleared", "Note": "Bank Loan Fixed Installment"}
    ])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

    return round(score, 1), category

# ==============================================================================
# SECTION 4: AI COPILOT ENGINE
# ==============================================================================
def get_ai_advice(query, inc, exp, sav, dbt, score, cat):
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
# SECTION 5: ULTRA ULTRA LIQUID iOS GLASSMORPHISM CSS ENGINE
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    box-sizing: border-box;
}

/* 1. App Wallpaper Background with Vibrant Fluid Mesh Gradient Orbs */
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
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1440px; }

/* 2. Absolute Streamlit Native Elements Override (Destroys Black Containers Completely) */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(50px) saturate(210%) !important;
    -webkit-backdrop-filter: blur(50px) saturate(210%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: 10px 0 30px rgba(0, 0, 0, 0.3) !important;
}

div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] { gap: 10px !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 18px !important;
    padding: 12px 18px !important;
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0.06) 100%) !important;
    border-color: rgba(255, 255, 255, 0.35) !important;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3) !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label input[type="radio"],
div[data-testid="stRadio"] div[role="radiogroup"] label div[data-aria-hidden="true"],
div[data-testid="stRadio"] div[role="radiogroup"] label svg {
    display: none !important;
}

/* Form Controls Glassmorphism */
div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    backdrop-filter: blur(30px) !important;
}

.stNumberInput input, .stTextInput input, .stTextArea textarea {
    color: #ffffff !important;
    background: transparent !important;
    font-weight: 600 !important;
}

/* Dataframe Clean Glass Override */
div[data-testid="stDataFrame"], div[data-testid="stTable"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 22px !important;
    backdrop-filter: blur(40px) saturate(200%) !important;
    padding: 10px !important;
}
div[data-testid="stDataFrame"] * {
    background: transparent !important;
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* 3. Pure Custom Liquid Glassmorphism Component Cards */
.liquid-glass-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-top: 1px solid rgba(255, 255, 255, 0.4);
    border-left: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(50px) saturate(210%);
    -webkit-backdrop-filter: blur(50px) saturate(210%);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.45), inset 0 1px 2px rgba(255, 255, 255, 0.3);
    border-radius: 24px;
    padding: 22px;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.liquid-glass-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 35px 70px rgba(0, 0, 0, 0.55), inset 0 1px 3px rgba(255, 255, 255, 0.5);
}

/* Metric Cards with Glowing Specular Highlights */
.metric-card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.metric-card-inner {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.10) 0%, rgba(255, 255, 255, 0.02) 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(40px) saturate(200%);
    border-radius: 22px;
    padding: 18px 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.35), inset 0 1px 1px rgba(255,255,255,0.25);
}

.metric-badge-box {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 12px;
}

.badge-green { background: rgba(16, 185, 129, 0.25); border: 1px solid rgba(16, 185, 129, 0.5); color: #34d399; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); }
.badge-pink { background: rgba(244, 63, 94, 0.25); border: 1px solid rgba(244, 63, 94, 0.5); color: #fb7185; box-shadow: 0 0 20px rgba(244, 63, 94, 0.4); }
.badge-blue { background: rgba(59, 130, 246, 0.25); border: 1px solid rgba(59, 130, 246, 0.5); color: #60a5fa; box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); }
.badge-purple { background: rgba(139, 92, 246, 0.25); border: 1px solid rgba(139, 92, 246, 0.5); color: #c084fc; box-shadow: 0 0 20px rgba(139, 92, 246, 0.4); }

.metric-title { font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 0.8px; }
.metric-value { font-size: 26px; font-weight: 800; color: #ffffff; margin: 4px 0 6px 0; }
.metric-foot { font-size: 11px; font-weight: 700; display: flex; align-items: center; gap: 8px; }

/* 4. Action Glass Pill Button */
.action-pill-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    width: 100%;
    padding: 16px;
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
    border: 1px solid rgba(255, 255, 255, 0.4);
    border-radius: 20px;
    color: #ffffff;
    font-size: 16px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.5), inset 0 1px 2px rgba(255,255,255,0.4);
    transition: all 0.3s ease;
}

.stButton > button {
    width: 100%; border-radius: 20px; padding: 16px; font-size: 16px; font-weight: 800; color: #ffffff;
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 12px 35px rgba(37, 99, 235, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.008) !important;
    box-shadow: 0 18px 45px rgba(124, 58, 237, 0.7), inset 0 1px 3px rgba(255, 255, 255, 0.6) !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SECTION 6: SIDEBAR NAVIGATION CONTROLLER
# ==============================================================================
with st.sidebar:
    st.html(f"""
    <div style="display:flex; align-items:center; gap:12px; padding:10px 5px 15px 5px;">
        <div style="width:46px; height:46px; border-radius:16px; background:linear-gradient(135deg, #2563eb, #7c3aed); display:flex; align-items:center; justify-content:center; font-size:24px; box-shadow:0 0 25px rgba(37,99,235,0.8);">📊</div>
        <div>
            <div style="font-size:22px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">{APP_NAME}</div>
            <div style="font-size:10px; color:rgba(255,255,255,0.6);">Plan Smarter • Live Better</div>
        </div>
    </div>
    """)
    st.markdown("---")

    nav_choice = st.radio(
        "Navigation",
        [
            "Home",
            "Dashboard",
            "Expenses",
            "AI Adviser",
            "Insights",
            "Settings"
        ],
        index=0
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.html(f"""
    <div style="padding:16px; border-radius:20px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); backdrop-filter:blur(30px);">
        <div style="font-size:11px; color:rgba(255,255,255,0.7); font-style:italic; margin-bottom:12px;">"A better financial future starts with better decisions."</div>
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:38px; height:38px; border-radius:50%; background:linear-gradient(135deg, #2563eb, #10b981); display:flex; align-items:center; justify-content:center; font-weight:800;">V</div>
            <div>
                <div style="font-size:14px; font-weight:700;">{AUTHOR_NAME}</div>
                <div style="font-size:11px; color:rgba(255,255,255,0.6);">Student</div>
            </div>
        </div>
    </div>
    """)

# COMPUTATION OF REAL-TIME AGGREGATES
inc_tot = st.session_state.income
exp_tot = st.session_state.expenses
inv_tot = st.session_state.savings
dbt_tot = st.session_state.debt

exp_ratio = min((exp_tot / (inc_tot if inc_tot > 0 else 1.0)) * 100.0, 100.0)
sav_ratio = min((inv_tot / (inc_tot if inc_tot > 0 else 1.0)) * 100.0, 100.0)
dbt_ratio = min((dbt_tot / (inc_tot if inc_tot > 0 else 1.0)) * 100.0, 100.0)

fz_score, fz_cat = evaluate_fuzzy_health(exp_ratio, sav_ratio, dbt_ratio)

# ==============================================================================
# TAB 1: 🏠 HOME MODULE (MATCHES REFERENCE IMAGE EXACTLY)
# ==============================================================================
if nav_choice == "Home":
    # Header Section
    h1, h2 = st.columns([3, 1.2])
    with h1:
        st.html("""
        <div style="margin-bottom:20px;">
            <div style="font-size:11px; font-weight:800; color:rgba(255,255,255,0.6); letter-spacing:2px; text-transform:uppercase;">WELCOME TO</div>
            <div style="font-size:42px; font-weight:800; color:#ffffff; margin:2px 0 6px 0; letter-spacing:-1px;">Personal Finance and<br>Expense Management Adviser</div>
            <div style="font-size:14px; color:rgba(255,255,255,0.7);">Track. Analyze. Plan. Achieve. — Smarter Money Decisions with AI & Fuzzy Logic.</div>
        </div>
        """)
    with h2:
        now_str = datetime.datetime.now().strftime("%a, %d %b %Y<br>%I:%M %p")
        st.html(f"""
        <div class="liquid-glass-card" style="text-align:center; padding:18px;">
            <div style="font-size:11px; color:rgba(255,255,255,0.6); font-weight:700; text-transform:uppercase; margin-bottom:6px;">{now_str}</div>
            <div style="font-size:13px; font-style:italic; color:#c084fc; font-weight:600;">"Manage your money today for a brighter tomorrow."</div>
        </div>
        """)

    # 4 Top Metric Cards with Sparkline Indicators
    st.html(f"""
    <div class="metric-card-grid">
        <div class="metric-card-inner">
            <div class="metric-badge-box badge-green">💼</div>
            <div class="metric-title">Monthly Income</div>
            <div class="metric-value">₹{inc_tot:,.0f}</div>
            <div class="metric-foot" style="color:#34d399;">
                <span>↑ +0%</span>
                <svg width="60" height="18" viewBox="0 0 60 18"><path d="M0,15 Q15,5 30,12 T60,3" fill="none" stroke="#34d399" stroke-width="2.5"/></svg>
            </div>
        </div>
        <div class="metric-card-inner">
            <div class="metric-badge-box badge-pink">💳</div>
            <div class="metric-title">Monthly Expenses</div>
            <div class="metric-value">₹{exp_tot:,.0f}</div>
            <div class="metric-foot" style="color:#fb7185;">
                <span>↑ +0%</span>
                <svg width="60" height="18" viewBox="0 0 60 18"><path d="M0,12 Q15,16 30,8 T60,14" fill="none" stroke="#fb7185" stroke-width="2.5"/></svg>
            </div>
        </div>
        <div class="metric-card-inner">
            <div class="metric-badge-box badge-blue">📈</div>
            <div class="metric-title">Monthly Savings</div>
            <div class="metric-value">₹{inv_tot:,.0f}</div>
            <div class="metric-foot" style="color:#60a5fa;">
                <span>↑ +0%</span>
                <svg width="60" height="18" viewBox="0 0 60 18"><path d="M0,16 Q15,10 30,14 T60,2" fill="none" stroke="#60a5fa" stroke-width="2.5"/></svg>
            </div>
        </div>
        <div class="metric-card-inner">
            <div class="metric-badge-box badge-purple">🏛️</div>
            <div class="metric-title">Monthly Debt</div>
            <div class="metric-value">₹{dbt_tot:,.0f}</div>
            <div class="metric-foot" style="color:#c084fc;">
                <span>↑ +0%</span>
                <svg width="60" height="18" viewBox="0 0 60 18"><path d="M0,14 Q15,8 30,12 T60,5" fill="none" stroke="#c084fc" stroke-width="2.5"/></svg>
            </div>
        </div>
    </div>
    """)

    # Interactive Input Form Card
    st.html("""
    <div style="margin-bottom:12px; display:flex; align-items:center; justify-content:space-between;">
        <div>
            <div style="font-size:20px; font-weight:800; color:#ffffff;">📊 Enter Your Financial Details</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.7);">Provide your monthly financial information to get AI-powered insights.</div>
        </div>
    </div>
    """)

    # Input Fields in 4 Columns
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        new_inc = st.number_input("Monthly Income (₹)", min_value=0.0, value=float(st.session_state.income), step=1000.0, help="Your total monthly income")
    with i2:
        new_exp = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=float(st.session_state.expenses), step=500.0, help="All your monthly expenses")
    with i3:
        new_sav = st.number_input("Monthly Savings (₹)", min_value=0.0, value=float(st.session_state.savings), step=500.0, help="Amount you save monthly")
    with i4:
        new_dbt = st.number_input("Monthly Debt Payment (₹)", min_value=0.0, value=float(st.session_state.debt), step=500.0, help="EMI or loan payments")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Analyze My Finances", use_container_width=True):
        st.session_state.income = new_inc
        st.session_state.expenses = new_exp
        st.session_state.savings = new_sav
        st.session_state.debt = new_dbt
        st.success("Financial Snapshot Updated Successfully!")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3 Bottom Advisory Feature Cards
    f1, f2, f3 = st.columns(3)
    with f1:
        st.html("""
        <div class="liquid-glass-card" style="border-left:4px solid #10b981;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                <div style="width:36px; height:36px; border-radius:12px; background:rgba(16,185,129,0.25); display:flex; align-items:center; justify-content:center; color:#34d399; font-size:18px;">⚙️</div>
                <div style="font-size:15px; font-weight:800;">AI-Powered Advice</div>
            </div>
            <div style="font-size:12px; color:rgba(255,255,255,0.7);">Get personalized financial recommendations using LangChain and LLM.</div>
        </div>
        """)
    with f2:
        st.html("""
        <div class="liquid-glass-card" style="border-left:4px solid #8b5cf6;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                <div style="width:36px; height:36px; border-radius:12px; background:rgba(139,92,246,0.25); display:flex; align-items:center; justify-content:center; color:#c084fc; font-size:18px;">🧠</div>
                <div style="font-size:15px; font-weight:800;">Fuzzy Logic Analysis</div>
            </div>
            <div style="font-size:12px; color:rgba(255,255,255,0.7);">Advanced fuzzy inference system to analyze your financial health score.</div>
        </div>
        """)
    with f3:
        st.html("""
        <div class="liquid-glass-card" style="border-left:4px solid #f59e0b;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                <div style="width:36px; height:36px; border-radius:12px; background:rgba(245,158,11,0.25); display:flex; align-items:center; justify-content:center; color:#fbbf24; font-size:18px;">🛡️</div>
                <div style="font-size:15px; font-weight:800;">Better Financial Future</div>
            </div>
            <div style="font-size:12px; color:rgba(255,255,255,0.7);">Make informed decisions and achieve your long-term financial goals.</div>
        </div>
        """)

# ==============================================================================
# TAB 2: 📊 DASHBOARD & ANALYTICS MODULE
# ==============================================================================
elif nav_choice == "Dashboard":
    st.html("""
    <div class="liquid-glass-card" style="margin-bottom:20px;">
        <h2>📊 Financial Dashboard & Cashflow Analytics</h2>
        <p style="color:rgba(255,255,255,0.7);">Visual analytics powered by real-time ledger entries and Mamdani Fuzzy Scoring.</p>
    </div>
    """)
    
    # Liquid SVG Cashflow Progress Bars Card
    max_v = max(inc_tot, exp_tot, inv_tot, dbt_tot, 1.0)
    inc_p, exp_p, sav_p, dbt_p = (inc_tot/max_v)*100, (exp_tot/max_v)*100, (inv_tot/max_v)*100, (dbt_tot/max_v)*100

    st.html(f"""
    <div class="liquid-glass-card">
        <div style="font-size:18px; font-weight:800; margin-bottom:20px;">📊 Monthly Cashflow Breakdown</div>
        
        <div style="margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                <span style="color:#34d399;">💼 Income</span><span>₹{inc_tot:,.2f}</span>
            </div>
            <div style="width:100%; height:16px; background:rgba(255,255,255,0.06); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
                <div style="width:{inc_p}%; height:100%; background:linear-gradient(90deg, #10b981, #34d399); box-shadow:0 0 15px rgba(16,185,129,0.6); border-radius:20px;"></div>
            </div>
        </div>

        <div style="margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                <span style="color:#fb7185;">💳 Expenses</span><span>₹{exp_tot:,.2f}</span>
            </div>
            <div style="width:100%; height:16px; background:rgba(255,255,255,0.06); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
                <div style="width:{exp_p}%; height:100%; background:linear-gradient(90deg, #f43f5e, #fb7185); box-shadow:0 0 15px rgba(244,63,94,0.6); border-radius:20px;"></div>
            </div>
        </div>

        <div style="margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                <span style="color:#60a5fa;">📈 Savings / Investments</span><span>₹{inv_tot:,.2f}</span>
            </div>
            <div style="width:100%; height:16px; background:rgba(255,255,255,0.06); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
                <div style="width:{sav_p}%; height:100%; background:linear-gradient(90deg, #3b82f6, #60a5fa); box-shadow:0 0 15px rgba(59,130,246,0.6); border-radius:20px;"></div>
            </div>
        </div>

        <div>
            <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                <span style="color:#c084fc;">🏛️ Debt Service</span><span>₹{dbt_tot:,.2f}</span>
            </div>
            <div style="width:100%; height:16px; background:rgba(255,255,255,0.06); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">
                <div style="width:{dbt_p}%; height:100%; background:linear-gradient(90deg, #8b5cf6, #c084fc); box-shadow:0 0 15px rgba(139,92,246,0.6); border-radius:20px;"></div>
            </div>
        </div>
    </div>
    """)

# ==============================================================================
# TAB 3: 💳 EXPENSES & LEDGER MODULE
# ==============================================================================
elif nav_choice == "Expenses":
    st.html("""
    <div class="liquid-glass-card" style="margin-bottom:20px;">
        <h2>💳 Expense Ledger & Transaction Entry</h2>
        <p style="color:rgba(255,255,255,0.7);">Manage individual transactions to maintain audit trails.</p>
    </div>
    """)
    
    t1, t2, t3 = st.columns(3)
    with t1: t_type = st.selectbox("Transaction Type", ["Income", "Expense", "Investment", "Debt"])
    with t2: t_cat = st.text_input("Category Name", value="General Outflow")
    with t3: t_amt = st.number_input("Amount (₹)", min_value=1.0, value=1500.0, step=100.0)

    if st.button("➕ Record Transaction"):
        new_id = f"TXN-{len(st.session_state.transactions) + 8001}"
        new_row = pd.DataFrame([{"ID": new_id, "Date": str(datetime.date.today()), "Category": t_cat, "Type": t_type, "Amount": float(t_amt), "Method": "Manual App Entry", "Status": "Cleared", "Note": "Recorded Entry"}])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_row], ignore_index=True)
        st.success(f"Transaction {new_id} Successfully Recorded!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(st.session_state.transactions, use_container_width=True)

# ==============================================================================
# TAB 4: ✨ AI ADVISER MODULE
# ==============================================================================
elif nav_choice == "AI Adviser":
    st.html("""
    <div class="liquid-glass-card" style="margin-bottom:20px;">
        <h2>✨ AI Copilot Financial Advisory</h2>
        <p style="color:rgba(255,255,255,0.7);">Get tailored financial strategies generated by Gemini AI.</p>
    </div>
    """)
    
    user_q = st.text_area("Your Financial Inquiry:", value="How can I optimize my monthly budget to allocate 25% towards long-term mutual funds?")
    if st.button("💬 Ask AI Copilot"):
        with st.spinner("Analyzing profile & generating advisory report..."):
            ans = get_ai_advice(user_q, inc_tot, exp_tot, inv_tot, dbt_tot, fz_score, fz_cat)
            st.session_state.chat_history.append({"q": user_q, "a": ans})

    for chat in reversed(st.session_state.chat_history):
        st.html(f"""
        <div class="liquid-glass-card" style="margin-bottom:14px; border-left:4px solid #3b82f6;">
            <b>Q: {chat['q']}</b>
            <hr style="border-color:rgba(255,255,255,0.1); margin:10px 0;">
            <div style="font-size:13px; color:rgba(255,255,255,0.85); line-height:1.6;">{chat['a']}</div>
        </div>
        """)

# ==============================================================================
# TAB 5: 🧠 INSIGHTS & MAMDANI FUZZY LOGIC MODULE
# ==============================================================================
elif nav_choice == "Insights":
    st.html(f"""
    <div class="liquid-glass-card" style="margin-bottom:20px;">
        <h2>🧠 Mamdani Fuzzy Logic Diagnostics</h2>
        <p style="color:rgba(255,255,255,0.7);">Evaluated Financial Health Rating: <b style="color:#60a5fa;">{fz_score}/100 ({fz_cat})</b></p>
    </div>
    """)

# ==============================================================================
# TAB 6: ⚙️ SETTINGS MODULE
# ==============================================================================
elif nav_choice == "Settings":
    st.html("""
    <div class="liquid-glass-card" style="margin-bottom:20px;">
        <h2>⚙️ User Profile & App Settings</h2>
    </div>
    """)
    st.text_input("Legal Account Owner Name:", value=AUTHOR_NAME)
    st.selectbox("Operating Currency:", ["INR (₹)", "USD ($)", "EUR (€)"])

# FOOTER
st.html("""
<div style="text-align:center; padding:30px 0 10px 0; font-size:11px; color:rgba(255,255,255,0.5);">
    Built with Streamlit &nbsp;|&nbsp; Powered by AI & Fuzzy Logic &nbsp;|&nbsp; © 2026 FinWise ❤️
</div>
""")