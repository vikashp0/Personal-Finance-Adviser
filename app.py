import os
import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. APPLICATION & PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="FinWise Pro - Enterprise Financial Adviser",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. PERSISTENT SESSION STATE ENGINE (DATABASE SIMULATOR)
# ==============================================================================
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"ID": "TXN-101", "Date": "2026-09-01", "Category": "Base Salary", "Type": "Income", "Amount": 65000.0, "Payment Method": "Bank Transfer", "Note": "Monthly Company Payroll"},
        {"ID": "TXN-102", "Date": "2026-09-02", "Category": "Housing & Rent", "Type": "Expense", "Amount": 16000.0, "Payment Method": "UPI", "Note": "Apartment Maintenance & Rent"},
        {"ID": "TXN-103", "Date": "2026-09-03", "Category": "Groceries & Food", "Type": "Expense", "Amount": 7500.0, "Payment Method": "Credit Card", "Note": "Supermarket Monthly Restock"},
        {"ID": "TXN-104", "Date": "2026-09-05", "Category": "Index Mutual Funds", "Type": "Investment", "Amount": 15000.0, "Payment Method": "Auto-Debit", "Note": "Nifty 50 Index SIP"},
        {"ID": "TXN-105", "Date": "2026-09-07", "Category": "Utilities & Bills", "Type": "Expense", "Amount": 3200.0, "Payment Method": "UPI", "Note": "Electricity & High-Speed Wifi"},
        {"ID": "TXN-106", "Date": "2026-09-10", "Category": "Car Loan EMI", "Type": "Debt", "Amount": 5500.0, "Payment Method": "Auto-Debit", "Note": "Monthly Vehicle Loan EMI"},
        {"ID": "TXN-107", "Date": "2026-09-12", "Category": "Dining & Leisure", "Type": "Expense", "Amount": 4200.0, "Payment Method": "Credit Card", "Note": "Weekend Dinners & Movies"},
        {"ID": "TXN-108", "Date": "2026-09-15", "Category": "Freelance Design", "Type": "Income", "Amount": 12000.0, "Payment Method": "Bank Transfer", "Note": "Client Consulting Project"}
    ])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "financial_goals" not in st.session_state:
    st.session_state.financial_goals = [
        {"Goal Name": "Emergency Fund", "Target Amount": 200000.0, "Current Amount": 120000.0, "Target Date": "2027-03-31"},
        {"Goal Name": "International Vacation", "Target Amount": 150000.0, "Current Amount": 45000.0, "Target Date": "2027-10-15"},
        {"Goal Name": "Wealth Corpus 2030", "Target Amount": 2000000.0, "Current Amount": 350000.0, "Target Date": "2030-12-31"}
    ]

if "historical_snapshots" not in st.session_state:
    st.session_state.historical_snapshots = pd.DataFrame([
        {"Month": "Apr 2026", "Income": 60000.0, "Expenses": 32000.0, "Savings": 12000.0, "Debt": 6000.0, "Fuzzy Score": 72.4},
        {"Month": "May 2026", "Income": 62000.0, "Expenses": 31000.0, "Savings": 14000.0, "Debt": 6000.0, "Fuzzy Score": 75.8},
        {"Month": "Jun 2026", "Income": 62000.0, "Expenses": 35000.0, "Savings": 11000.0, "Debt": 6000.0, "Fuzzy Score": 68.2},
        {"Month": "Jul 2026", "Income": 65000.0, "Expenses": 30000.0, "Savings": 16000.0, "Debt": 5500.0, "Fuzzy Score": 81.0},
        {"Month": "Aug 2026", "Income": 65000.0, "Expenses": 29000.0, "Savings": 18000.0, "Debt": 5500.0, "Fuzzy Score": 84.5},
        {"Month": "Sep 2026", "Income": 77000.0, "Expenses": 30900.0, "Savings": 15000.0, "Debt": 5500.0, "Fuzzy Score": 82.1}
    ])

# ==============================================================================
# 3. MAMDANI FUZZY LOGIC MATHEMATICAL ENGINE
# ==============================================================================
def trimf(x, a, b, c):
    """Triangular Membership Function"""
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    if b < x < c:
        return (c - x) / (c - b) if c != b else 1.0
    return 0.0

def trapmf(x, a, b, c, d):
    """Trapezoidal Membership Function"""
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
    Computes Mamdani Fuzzy Inference Health Score (0-100) using Centroid Defuzzification.
    """
    # 1. Fuzzification for Expense Ratio
    exp_low = trapmf(exp_ratio, 0, 0, 30, 50)
    exp_med = trimf(exp_ratio, 40, 55, 70)
    exp_high = trapmf(exp_ratio, 60, 80, 100, 100)

    # 2. Fuzzification for Savings Ratio
    sav_poor = trapmf(sav_ratio, 0, 0, 10, 20)
    sav_mod = trimf(sav_ratio, 15, 25, 35)
    sav_good = trapmf(sav_ratio, 30, 45, 100, 100)

    # 3. Fuzzification for Debt Ratio
    dbt_low = trapmf(dbt_ratio, 0, 0, 15, 30)
    dbt_med = trimf(dbt_ratio, 20, 35, 50)
    dbt_high = trapmf(dbt_ratio, 40, 60, 100, 100)

    # 4. Rule Base Evaluation
    rules = {"Poor": 0.0, "Fair": 0.0, "Good": 0.0, "Excellent": 0.0}
    
    # Rule 1: IF Expense is Low AND Savings is Good AND Debt is Low THEN Excellent
    rules["Excellent"] = max(rules["Excellent"], min(exp_low, sav_good, dbt_low))
    # Rule 2: IF Expense is Med AND Savings is Mod AND Debt is Low THEN Good
    rules["Good"] = max(rules["Good"], min(exp_med, sav_mod, dbt_low))
    # Rule 3: IF Expense is High OR Debt is High THEN Poor
    rules["Poor"] = max(rules["Poor"], max(exp_high, dbt_high))
    # Rule 4: IF Expense is Med AND Savings is Poor THEN Fair
    rules["Fair"] = max(rules["Fair"], min(exp_med, sav_poor))
    # Rule 5: IF Savings is Good AND Debt is Med THEN Good
    rules["Good"] = max(rules["Good"], min(sav_good, dbt_med))

    # 5. Aggregation & Centroid Defuzzification
    x_grid = np.linspace(0, 100, 101)
    aggregated = np.zeros_like(x_grid)
    for i, x in enumerate(x_grid):
        p_val = min(rules["Poor"], trapmf(x, 0, 0, 20, 40))
        f_val = min(rules["Fair"], trimf(x, 30, 50, 70))
        g_val = min(rules["Good"], trimf(x, 60, 75, 90))
        e_val = min(rules["Excellent"], trapmf(x, 80, 90, 100, 100))
        aggregated[i] = max(p_val, f_val, g_val, e_val)

    sum_agg = np.sum(aggregated)
    score = float(np.sum(x_grid * aggregated) / sum_agg) if sum_agg != 0 else 50.0

    if score >= 80:
        category = "Excellent"
    elif score >= 60:
        category = "Good"
    elif score >= 40:
        category = "Fair"
    else:
        category = "Poor"

    return round(score, 1), category, rules, {
        "exp": {"Low": exp_low, "Med": exp_med, "High": exp_high},
        "sav": {"Poor": sav_poor, "Mod": sav_mod, "Good": sav_good},
        "dbt": {"Low": dbt_low, "Med": dbt_med, "High": dbt_high}
    }

# ==============================================================================
# 4. LANGCHAIN & GOOGLE GEMINI AI INTEGRATION ENGINE
# ==============================================================================
def get_ai_advice(query, inc, exp, sav, dbt, score, cat):
    """
    Connects to LangChain + Gemini LLM to synthesize financial metrics into advisory outputs.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return f"""
### 📊 FinWise Automated Health Summary
* **Mamdani Fuzzy Health Rating:** **{score}/100 ({cat})**[cite: 1]
* **Expense Ratio:** {exp/inc*100:.1f}% | **Savings Ratio:** {sav/inc*100:.1f}% | **Debt Ratio:** {dbt/inc*100:.1f}%

#### 💡 Key Action Steps:
1. **Reduce High-Interest Obligations:** Ensure your total EMI/Debt payments remain below 30% of gross income[cite: 1].
2. **Systematic Savings:** Increase monthly SIP contributions to at least 20% of net monthly income[cite: 1].
3. **Emergency Cushion:** Build a liquid cash reserve equal to 6 months of mandatory living expenses.
        """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import PromptTemplate
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.3)
        template = """
You are FinWise Pro AI, a Senior Certified Financial Planner (CFP) and Executive Wealth Adviser.
Client Financial Snapshot:
- Gross Monthly Income: ₹{inc:,.2f}
- Total Monthly Expenses: ₹{exp:,.2f}
- Monthly Investments & Savings: ₹{sav:,.2f}
- Monthly Debt Obligations: ₹{dbt:,.2f}
- Calculated Mamdani Fuzzy Financial Health Score: {score}/100 ({cat})

Client Query / Focus Area: "{query}"

Please provide a highly structured, professional, and encouraging wealth management response:
1. **Executive Evaluation:** Analyze why the client received a score of {score}/100 ({cat}).
2. **Vulnerability Assessment:** Highlight risks regarding expense leakage or debt exposure.
3. **Strategic Action Roadmap:** 3 actionable, high-impact financial steps for liquidity optimization and long-term wealth growth.
Formatting: Use clear Markdown with headings, bullet points, and clean spacing.
"""
        prompt = PromptTemplate(input_variables=["inc", "exp", "sav", "dbt", "score", "cat", "query"], template=template)
        chain = prompt | llm
        res = chain.invoke({"inc": inc, "exp": exp, "sav": sav, "dbt": dbt, "score": score, "cat": cat, "query": query if query else "Provide comprehensive financial optimization report"})
        return res.content
    except Exception as e:
        return f"**Financial Health Evaluation:** {score}/100 ({cat}). Focus on optimizing discretionary expenses and strengthening investment allocations."

# ==============================================================================
# 5. LIQUID GLASSMORPHISM STYLING & CUSTOM CSS
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

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

/* Enhanced Glass Panels */
.glass-panel, .top-metric-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    backdrop-filter: blur(40px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
    border-radius: 20px !important;
    padding: 22px;
}

.metric-badge {
    width: 44px; height: 44px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center; font-size: 20px;
    margin-bottom: 12px;
}
.bg-green { background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); box-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }
.bg-pink { background: rgba(244, 63, 94, 0.25); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4); box-shadow: 0 0 15px rgba(244, 63, 94, 0.3); }
.bg-blue { background: rgba(59, 130, 246, 0.25); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); box-shadow: 0 0 15px rgba(59, 130, 246, 0.3); }
.bg-purple { background: rgba(139, 92, 246, 0.25); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.4); box-shadow: 0 0 15px rgba(139, 92, 246, 0.3); }

.top-metric-label { font-size: 11px; color: rgba(255,255,255,0.7); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.top-metric-val { font-size: 26px; font-weight: 800; color: #ffffff; margin: 4px 0 2px 0; }

/* Custom Inputs Styling */
.stNumberInput input, .stTextInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important; color: #ffffff !important;
    font-weight: 600 !important; font-size: 15px !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.02) 100%) !important;
    backdrop-filter: blur(40px) saturate(180%) !important;
    border-right: 1px solid rgba(255,255,255,0.18) !important;
}

div[data-testid="stRadio"] > label { display: none; }
div[data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px; padding: 12px 16px;
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 600; cursor: pointer; transition: all 0.2s;
    width: 100%;
}
div[data-testid="stRadio"] label:hover { background: rgba(255, 255, 255, 0.15); }

/* Glowing Primary Button */
.stButton > button {
    width: 100%; border-radius: 14px; padding: 14px;
    font-size: 16px; font-weight: 700; color: #ffffff;
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.6) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 35px rgba(124, 58, 237, 0.8) !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. SIDEBAR NAVIGATION CONTROLLER
# ==============================================================================
with st.sidebar:
    st.html("""
    <div style="display:flex; align-items:center; gap:12px; padding:10px 5px 15px 5px;">
        <div style="width:44px; height:44px; border-radius:14px; background:linear-gradient(135deg, #2563eb, #7c3aed); display:flex; align-items:center; justify-content:center; font-size:22px; box-shadow:0 0 25px rgba(37,99,235,0.7);">💎</div>
        <div>
            <div style="font-size:22px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">FinWise Pro</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.6);">Enterprise Finance Copilot</div>
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
            "📜 Transaction History & Audit",
            "⚙️ Settings & Goals"
        ],
        index=0
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.html("""
    <div style="padding:14px; border-radius:16px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12);">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg, #2563eb, #10b981); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:14px;">V</div>
            <div>
                <div style="font-size:14px; font-weight:700;">Vikas Ramsevak Pal</div>
                <div style="font-size:11px; color:#34d399;">● Pro Subscriber</div>
            </div>
        </div>
    </div>
    """)

# Compute Dynamic Aggregation Metrics from Ledger
df_trans = st.session_state.transactions
inc_tot = df_trans[df_trans["Type"] == "Income"]["Amount"].sum()
exp_tot = df_trans[df_trans["Type"] == "Expense"]["Amount"].sum()
inv_tot = df_trans[df_trans["Type"] == "Investment"]["Amount"].sum()
dbt_tot = df_trans[df_trans["Type"] == "Debt"]["Amount"].sum()

if inc_tot == 0:
    inc_tot = 1.0  # Prevent division by zero

exp_ratio = min((exp_tot / inc_tot) * 100, 100.0)
sav_ratio = min((inv_tot / inc_tot) * 100, 100.0)
dbt_ratio = min((dbt_tot / inc_tot) * 100, 100.0)

fz_score, fz_cat, fz_rules, fz_mems = evaluate_fuzzy_health(exp_ratio, sav_ratio, dbt_ratio)

# ==============================================================================
# TAB 1: 📊 EXECUTIVE DASHBOARD
# ==============================================================================
if nav_choice == "📊 Executive Dashboard":
    h_c1, h_c2 = st.columns([3, 1])
    with h_c1:
        st.html("""
        <div style="font-size:11px; font-weight:700; color:#60a5fa; letter-spacing:2px; text-transform:uppercase;">ENTERPRISE FINANCIAL INTELLIGENCE</div>
        <div style="font-size:38px; font-weight:800; color:#ffffff; line-height:1.15; margin:4px 0;">Executive Wealth & Health Dashboard</div>
        <div style="font-size:14px; color:rgba(255,255,255,0.7);">Real-time Mamdani Fuzzy Logic Scoring & LangChain AI Advisory.</div>
        """)
    with h_c2:
        st.html(f"""
        <div class="glass-panel" style="padding:16px; text-align:center;">
            <div style="font-size:11px; color:rgba(255,255,255,0.6); text-transform:uppercase;">Fuzzy Health Rating</div>
            <div style="font-size:28px; font-weight:800; color:#60a5fa;">{fz_score}/100</div>
            <div style="font-size:12px; font-weight:700; color:#c084fc;">{fz_cat}</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.html(f'<div class="top-metric-card"><div class="metric-badge bg-green">💼</div><div class="top-metric-label">Total Monthly Income</div><div class="top-metric-val">₹{inc_tot:,.2f}</div></div>')
    with m2:
        st.html(f'<div class="top-metric-card"><div class="metric-badge bg-pink">💳</div><div class="top-metric-label">Total Expenses</div><div class="top-metric-val">₹{exp_tot:,.2f}</div></div>')
    with m3:
        st.html(f'<div class="top-metric-card"><div class="metric-badge bg-blue">📈</div><div class="top-metric-label">Investments & Savings</div><div class="top-metric-val">₹{inv_tot:,.2f}</div></div>')
    with m4:
        st.html(f'<div class="top-metric-card"><div class="metric-badge bg-purple">🏦</div><div class="top-metric-label">Debt Obligations</div><div class="top-metric-val">₹{dbt_tot:,.2f}</div></div>')

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        fig_cash = go.Figure(data=[
            go.Bar(name='Cashflow (₹)', x=['Income', 'Expenses', 'Savings', 'Debt'], y=[inc_tot, exp_tot, inv_tot, dbt_tot],
                   marker_color=['#34d399', '#fb7185', '#60a5fa', '#c084fc'])
        ])
        fig_cash.update_layout(
            title="Monthly Cashflow Allocation",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'), height=290
        )
        st.plotly_chart(fig_cash, use_container_width=True)

    with c2:
        df_outflow = df_trans[df_trans["Type"] != "Income"]
        if not df_outflow.empty:
            fig_pie = px.pie(df_outflow, values='Amount', names='Category', hole=0.4, title="Outflow Category Breakdown")
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=290)
            st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.html("<div style='font-size:18px; font-weight:700;'>📈 6-Month Historical Financial Health Trajectory</div>")
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(x=st.session_state.historical_snapshots['Month'], y=st.session_state.historical_snapshots['Income'], name='Income', line=dict(color='#34d399', width=3)))
    fig_hist.add_trace(go.Scatter(x=st.session_state.historical_snapshots['Month'], y=st.session_state.historical_snapshots['Expenses'], name='Expenses', line=dict(color='#fb7185', width=3)))
    fig_hist.add_trace(go.Scatter(x=st.session_state.historical_snapshots['Month'], y=st.session_state.historical_snapshots['Savings'], name='Savings', line=dict(color='#60a5fa', width=3)))
    fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=280)
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.html("<div style='font-size:18px; font-weight:700;'>🤖 AI-Generated Executive Advisory Report</div>")
    q_input = st.text_input("Specific Inquiry for AI Report:", placeholder="e.g. How can I optimize my housing expenses?")
    if st.button("✨ Generate Comprehensive AI Report"):
        with st.spinner("Analyzing profile with LangChain & Gemini LLM..."):
            report = get_ai_advice(q_input, inc_tot, exp_tot, inv_tot, dbt_tot, fz_score, fz_cat)
            st.html(f"""
            <div class="glass-panel" style="border-left:4px solid #a855f7;">
                <div style="font-size:14px; color:rgba(255,255,255,0.9); line-height:1.7;">{report}</div>
            </div>
            """)

# ==============================================================================
# TAB 2: 💳 EXPENSE & INCOME MANAGER
# ==============================================================================
elif nav_choice == "💳 Expense & Income Manager":
    st.html("""
    <div class="glass-panel">
        <h2>💳 Transaction & Cashflow Manager</h2>
        <p style="color:rgba(255,255,255,0.7);">Add, edit, and filter real-time transactions to dynamically update your financial health score.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.html("<div style='font-size:16px; font-weight:700; margin-bottom:10px;'>➕ Record New Financial Transaction</div>")
    t_c1, t_c2, t_c3, t_c4, t_c5 = st.columns([2, 2, 2, 2, 3])
    with t_c1:
        t_date = st.date_input("Date", datetime.date.today())
    with t_c2:
        t_type = st.selectbox("Type", ["Income", "Expense", "Investment", "Debt"])
    with t_c3:
        t_cat = st.text_input("Category", value="General")
    with t_c4:
        t_amt = st.number_input("Amount (₹)", min_value=1.0, value=2000.0, step=500.0)
    with t_c5:
        t_note = st.text_input("Note", value="Transaction Details")

    if st.button("➕ Record Transaction"):
        new_id = f"TXN-{len(st.session_state.transactions) + 101}"
        new_row = pd.DataFrame([{"ID": new_id, "Date": str(t_date), "Category": t_cat, "Type": t_type, "Amount": float(t_amt), "Payment Method": "Manual Entry", "Note": t_note}])
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_row], ignore_index=True)
        st.success(f"Transaction {new_id} Recorded Successfully!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.html("<div style='font-size:16px; font-weight:700; margin-bottom:10px;'>📋 Active Ledger Table</div>")
    st.dataframe(st.session_state.transactions, use_container_width=True)

# ==============================================================================
# TAB 3: 🧠 MAMDANI FUZZY ANALYTICS
# ==============================================================================
elif nav_choice == "🧠 Mamdani Fuzzy Analytics":
    st.html("""
    <div class="glass-panel">
        <h2>🧠 Mamdani Fuzzy Inference Engine Diagnostics</h2>
        <p style="color:rgba(255,255,255,0.7);">Detailed mathematical breakdown of membership functions ($\mu$), active rule base firing, and centroid defuzzification.</p>
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
    st.html("<div style='font-size:18px; font-weight:700;'>🔥 Fired Rule Strength Distribution</div>")
    rule_df = pd.DataFrame({
        'Fuzzy Category': list(fz_rules.keys()),
        'Firing Strength': list(fz_rules.values())
    })
    fig_rules = px.bar(rule_df, x='Fuzzy Category', y='Firing Strength', color='Fuzzy Category', title="Mamdani Consequent Aggregation Strengths")
    fig_rules.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=280)
    st.plotly_chart(fig_rules, use_container_width=True)

# ==============================================================================
# TAB 4: 🔮 WEALTH PREDICTIONS & SIP
# ==============================================================================
elif nav_choice == "🔮 Wealth Predictions & SIP":
    st.html("""
    <div class="glass-panel">
        <h2>🔮 Wealth Projection & Future SIP Engine</h2>
        <p style="color:rgba(255,255,255,0.7);">Simulate compound interest accumulation, inflation impact, and emergency fund runways over 1 to 20 years.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        sip_amt = st.number_input("Monthly SIP Investment (₹)", value=inv_tot if inv_tot > 0 else 15000.0, step=1000.0)
    with pc2:
        rate = st.slider("Expected Annual Return (%)", min_value=1.0, max_value=25.0, value=12.0)
    with pc3:
        years = st.slider("Horizon (Years)", min_value=1, max_value=25, value=10)

    m_count = years * 12
    r_monthly = (rate / 100) / 12
    timeline = []
    invested_timeline = []
    curr = 0
    inv_curr = 0
    for m in range(1, m_count + 1):
        curr = (curr + sip_amt) * (1 + r_monthly)
        inv_curr += sip_amt
        timeline.append(curr)
        invested_timeline.append(inv_curr)

    pred_df = pd.DataFrame({
        "Month": range(1, m_count + 1),
        "Projected Corpus (₹)": timeline,
        "Total Invested (₹)": invested_timeline
    })
    
    fig_p = px.line(pred_df, x="Month", y=["Projected Corpus (₹)", "Total Invested (₹)"], title=f"{years}-Year Wealth Growth Curve")
    fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=320)
    st.plotly_chart(fig_p, use_container_width=True)
    
    res_inv = invested_timeline[-1]
    res_corp = timeline[-1]
    res_gain = res_corp - res_inv
    st.success(f"🎯 **Projected Corpus:** ₹{res_corp:,.2f} | **Total Invested:** ₹{res_inv:,.2f} | **Wealth Gain:** ₹{res_gain:,.2f}")

# ==============================================================================
# TAB 5: ✨ AI COPILOT ADVISOR
# ==============================================================================
elif nav_choice == "✨ AI Copilot Advisor":
    st.html("""
    <div class="glass-panel">
        <h2>✨ FinWise Conversational AI Copilot</h2>
        <p style="color:rgba(255,255,255,0.7);">Ask open-ended questions regarding tax optimization, debt repayment strategies, and asset allocation.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    user_q = st.text_area("Your Financial Question:", value="How can I reduce my tax liabilities under the New Tax Regime while building a ₹10 Lakh corpus?")
    if st.button("💬 Ask FinWise AI Copilot"):
        with st.spinner("Generating Strategic Advisory Response..."):
            ans = get_ai_advice(user_q, inc_tot, exp_tot, inv_tot, dbt_tot, fz_score, fz_cat)
            st.session_state.chat_history.append({"q": user_q, "a": ans})

    st.markdown("<br>", unsafe_allow_html=True)
    st.html("<div style='font-size:16px; font-weight:700; margin-bottom:10px;'>💬 Chat Conversation History</div>")
    for chat in reversed(st.session_state.chat_history):
        st.html(f"""
        <div class="glass-panel" style="margin-bottom:12px;">
            <b>Q: {chat['q']}</b>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="font-size:13px; color:rgba(255,255,255,0.85); line-height:1.6;">{chat['a']}</div>
        </div>
        """)

# ==============================================================================
# TAB 6: 📜 TRANSACTION HISTORY & AUDIT
# ==============================================================================
elif nav_choice == "📜 Transaction History & Audit":
    st.html("""
    <div class="glass-panel">
        <h2>📜 Audit Log & Export Center</h2>
        <p style="color:rgba(255,255,255,0.7);">Review full audit trails and export transaction data in standard CSV format.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(st.session_state.transactions, use_container_width=True)
    
    csv_data = st.session_state.transactions.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Complete Audit Ledger (CSV)",
        data=csv_data,
        file_name=f"FinWise_Ledger_{datetime.date.today()}.csv",
        mime="text/csv"
    )

# ==============================================================================
# TAB 7: ⚙️ SETTINGS & GOALS
# ==============================================================================
elif nav_choice == "⚙️ Settings & Goals":
    st.html("""
    <div class="glass-panel">
        <h2>⚙️ Account Configuration & Goal Tracking</h2>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.text_input("Legal Account Owner Name:", value="Vikas Ramsevak Pal")
        st.selectbox("Base Operating Currency:", ["INR (₹)", "USD ($)", "EUR (€)"])
        api_key_env = os.getenv("GOOGLE_API_KEY")
        st.info(f"LangChain Gemini LLM Connection Status: {'Connected ✅' if api_key_env else 'Missing API Key ⚠️'}")
    
    with s_col2:
        st.html("<div style='font-size:16px; font-weight:700; margin-bottom:10px;'>🎯 Financial Target Goals</div>")
        st.dataframe(pd.DataFrame(st.session_state.financial_goals), use_container_width=True)

# ==============================================================================
# 7. FOOTER
# ==============================================================================
st.html("""
<div style="text-align:center; padding:30px 0 10px 0; font-size:11px; color:rgba(255,255,255,0.5);">
    FinWise Pro Enterprise Suite © 2026 &nbsp;|&nbsp; Powered by Streamlit, Mamdani Fuzzy Engine & LangChain AI
</div>
""")