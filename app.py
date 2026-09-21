import os
import numpy as np
import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="FinWise - Personal Finance Adviser",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# MAMDANI FUZZY LOGIC ENGINE
# --------------------------------------------------
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
    exp_low = trapmf(exp_ratio, 0, 0, 30, 50)
    exp_med = trimf(exp_ratio, 40, 55, 70)
    exp_high = trapmf(exp_ratio, 60, 80, 100, 100)

    sav_poor = trapmf(sav_ratio, 0, 0, 10, 20)
    sav_mod = trimf(sav_ratio, 15, 25, 35)
    sav_good = trapmf(sav_ratio, 30, 45, 100, 100)

    dbt_low = trapmf(dbt_ratio, 0, 0, 15, 30)
    dbt_med = trimf(dbt_ratio, 20, 35, 50)
    dbt_high = trapmf(dbt_ratio, 40, 60, 100, 100)

    rules = {"Poor": 0.0, "Fair": 0.0, "Good": 0.0, "Excellent": 0.0}
    rules["Excellent"] = max(rules["Excellent"], min(exp_low, sav_good, dbt_low))
    rules["Good"] = max(rules["Good"], min(exp_med, sav_mod, dbt_low))
    rules["Poor"] = max(rules["Poor"], max(exp_high, dbt_high))
    rules["Fair"] = max(rules["Fair"], min(exp_med, sav_poor))
    rules["Good"] = max(rules["Good"], min(sav_good, dbt_med))

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

    if score >= 80: category = "Excellent"
    elif score >= 60: category = "Good"
    elif score >= 40: category = "Fair"
    else: category = "Poor"

    return round(score, 1), category, rules, {
        "exp": {"Low": exp_low, "Med": exp_med, "High": exp_high},
        "sav": {"Poor": sav_poor, "Mod": sav_mod, "Good": sav_good},
        "dbt": {"Low": dbt_low, "Med": dbt_med, "High": dbt_high}
    }

# --------------------------------------------------
# LANGCHAIN AI INTEGRATION
# --------------------------------------------------
def get_ai_advice(query, inc, exp, sav, dbt, score, cat):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return f"**Financial Health Overview:** Score is **{score}/100 ({cat})**[cite: 1]. Recommendation: Keep debt under 30% and increase savings ratio above 20%[cite: 1]."
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import PromptTemplate
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.4)
        template = """
You are FinWise AI, an expert Personal Finance Adviser.
User Financials: Income ₹{inc}, Expenses ₹{exp}, Savings ₹{sav}, Debt ₹{dbt}.
Fuzzy Health Evaluation: {score}/100 ({cat}).
User Query: "{query}"

Provide concise, professional financial advice explaining why this score was assigned and actionable steps to improve.
"""
        prompt = PromptTemplate(input_variables=["inc", "exp", "sav", "dbt", "score", "cat", "query"], template=template)
        chain = prompt | llm
        res = chain.invoke({"inc": inc, "exp": exp, "sav": sav, "dbt": dbt, "score": score, "cat": cat, "query": query if query else "Analyze my overall health"})
        return res.content
    except Exception as e:
        return f"Score {score}/100 ({cat}). Focus on reducing high expense categories."

# --------------------------------------------------
# LIQUID GLASSMORPHISM STYLING
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp {
    background: 
        radial-gradient(circle at 15% 15%, rgba(37, 99, 235, 0.45), transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(147, 51, 234, 0.40), transparent 45%),
        radial-gradient(circle at 50% 85%, rgba(13, 148, 136, 0.30), transparent 50%),
        linear-gradient(135deg, #030712 0%, #0b1329 50%, #030712 100%) !important;
    color: #ffffff;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }

/* Enhanced Glass Panels */
.glass-panel, .top-metric-card, .feat-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    backdrop-filter: blur(40px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
    border-radius: 20px !important;
    padding: 20px;
}

/* Metric Badges */
.metric-badge {
    width: 38px; height: 38px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
    margin-bottom: 12px;
}
.bg-green { background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); box-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }
.bg-pink { background: rgba(244, 63, 94, 0.25); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4); box-shadow: 0 0 15px rgba(244, 63, 94, 0.3); }
.bg-blue { background: rgba(59, 130, 246, 0.25); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); box-shadow: 0 0 15px rgba(59, 130, 246, 0.3); }
.bg-purple { background: rgba(139, 92, 246, 0.25); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.4); box-shadow: 0 0 15px rgba(139, 92, 246, 0.3); }

.top-metric-label { font-size: 12px; color: rgba(255,255,255,0.7); font-weight: 500; }
.top-metric-val { font-size: 24px; font-weight: 800; color: #ffffff; margin: 2px 0 6px 0; }
.top-metric-trend { font-size: 11px; font-weight: 600; color: #34d399; }

/* Custom Inputs */
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important; color: #ffffff !important;
    font-weight: 600 !important; font-size: 15px !important;
}
.input-subtext { font-size: 11px; color: rgba(255, 255, 255, 0.5); margin-top: -10px; margin-bottom: 10px; }

/* Custom Radio Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.03) 100%) !important;
    backdrop-filter: blur(40px) saturate(180%) !important;
    border-right: 1px solid rgba(255,255,255,0.18) !important;
}

div[data-testid="stRadio"] > label { display: none; }
div[data-testid="stRadio"] > div { gap: 10px; }
div[data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px; padding: 12px 16px;
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 600; cursor: pointer; transition: all 0.2s;
    width: 100%;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.12);
}

/* Glowing Button */
.stButton > button {
    width: 100%; border-radius: 14px; padding: 14px;
    font-size: 16px; font-weight: 700; color: #ffffff;
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.6), 0 8px 20px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 35px rgba(124, 58, 237, 0.8), 0 12px 25px rgba(0, 0, 0, 0.5) !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FUNCTIONAL SIDEBAR NAVIGATION
# --------------------------------------------------
with st.sidebar:
    st.html("""
    <div style="display:flex; align-items:center; gap:12px; padding:10px 5px 15px 5px;">
        <div style="width:42px; height:42px; border-radius:12px; background:linear-gradient(135deg, #2563eb, #7c3aed); display:flex; align-items:center; justify-content:center; font-size:20px; box-shadow:0 0 20px rgba(37,99,235,0.6);">📊</div>
        <div>
            <div style="font-size:20px; font-weight:800; color:#ffffff;">FinWise</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.6);">Plan Smarter • Live Better</div>
        </div>
    </div>
    """)
    st.markdown("---")
    
    nav_choice = st.radio(
        "Navigation",
        ["🏠 Home", "📊 Dashboard", "💳 Expenses", "✨ AI Adviser", "📈 Insights", "⚙️ Settings"],
        index=1
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.html("""
    <div style="padding:12px; font-size:12px; color:rgba(255,255,255,0.6); font-style:italic; line-height:1.5;">
    "A better financial future starts with better decisions."
    </div>
    <div style="display:flex; align-items:center; gap:10px; padding:12px; border-radius:14px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);">
        <div style="width:32px; height:32px; border-radius:50%; background:#2563eb; display:flex; align-items:center; justify-content:center; font-weight:700;">V</div>
        <div>
            <div style="font-size:13px; font-weight:700;">Vikas</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.6);">Student</div>
        </div>
    </div>
    """)

# --------------------------------------------------
# PAGE 1: 🏠 HOME
# --------------------------------------------------
if nav_choice == "🏠 Home":
    st.html("""
    <div class="glass-panel">
        <h1 style="color:#ffffff; margin-bottom:10px;">Welcome to FinWise Adviser</h1>
        <p style="color:rgba(255,255,255,0.7); font-size:16px;">FinWise is an Intelligent Personal Finance and Expense Management Adviser powered by Mamdani Fuzzy Inference System and LangChain AI.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.html("""
        <div class="glass-panel">
            <h3>🧠 Fuzzy Logic Engine</h3>
            <p style="color:rgba(255,255,255,0.7); font-size:14px;">Evaluates non-linear financial parameters (Income, Expenses, Savings, Debt) using triangular/trapezoidal membership functions and centroid defuzzification to calculate a 0-100 Financial Health Score.</p>
        </div>
        """)
    with col2:
        st.html("""
        <div class="glass-panel">
            <h3>🤖 LangChain AI Contextual Reasoning</h3>
            <p style="color:rgba(255,255,255,0.7); font-size:14px;">Processes natural language queries and synthesizes actual mathematical fuzzy logic metrics into personalized financial advice using Gemini LLM models.</p>
        </div>
        """)

# --------------------------------------------------
# PAGE 2: 📊 DASHBOARD (MAIN FUNCTIONAL PAGE)
# --------------------------------------------------
elif nav_choice == "📊 Dashboard":
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.html("""
        <div style="font-size:11px; font-weight:700; color:#60a5fa; letter-spacing:2px; text-transform:uppercase;">WELCOME TO</div>
        <div style="font-size:38px; font-weight:800; color:#ffffff; line-height:1.15; margin:4px 0;">Personal Finance and<br>Expense Management Adviser</div>
        <div style="font-size:14px; color:rgba(255,255,255,0.7);">Track. Analyze. Plan. Achieve. — Smarter Money Decisions with AI & Fuzzy Logic.</div>
        """)

    with header_col2:
        st.html("""
        <div class="glass-panel" style="padding:18px; text-align:center;">
            <div style="font-size:14px; font-weight:600; font-style:italic; color:rgba(255,255,255,0.95);">"Manage your money today for a brighter tomorrow."</div>
            <div style="width:40px; height:3px; background:linear-gradient(90deg, #2563eb, #7c3aed); margin:12px auto 0 auto; border-radius:2px;"></div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # TOP METRICS SUMMARY
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.html("""
        <div class="top-metric-card">
            <div class="metric-badge bg-green">💼</div>
            <div class="top-metric-label">Monthly Income</div>
            <div class="top-metric-val">₹30,000</div>
            <div class="top-metric-trend">⬆ +0%</div>
        </div>
        """)
    with m_col2:
        st.html("""
        <div class="top-metric-card">
            <div class="metric-badge bg-pink">💳</div>
            <div class="top-metric-label">Monthly Expenses</div>
            <div class="top-metric-val">₹20,000</div>
            <div class="top-metric-trend">⬆ +0%</div>
        </div>
        """)
    with m_col3:
        st.html("""
        <div class="top-metric-card">
            <div class="metric-badge bg-blue">🐷</div>
            <div class="top-metric-label">Monthly Savings</div>
            <div class="top-metric-val">₹5,000</div>
            <div class="top-metric-trend">⬆ +0%</div>
        </div>
        """)
    with m_col4:
        st.html("""
        <div class="top-metric-card">
            <div class="metric-badge bg-purple">🏦</div>
            <div class="top-metric-label">Monthly Debt</div>
            <div class="top-metric-val">₹2,000</div>
            <div class="top-metric-trend">⬆ +0%</div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # INPUT SECTION
    st.html("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <span style="font-size:20px;">📊</span>
        <div>
            <div style="font-size:18px; font-weight:700;">Enter Your Financial Details</div>
            <div style="font-size:12px; color:rgba(255,255,255,0.6);">Provide your monthly financial information to get AI-powered insights.</div>
        </div>
    </div>
    """)

    in_col1, in_col2, in_col3, in_col4 = st.columns(4)
    with in_col1:
        income = st.number_input("Monthly Income (₹)", min_value=1.0, value=30000.0, step=1000.0)
        st.html('<div class="input-subtext">Your total monthly income</div>')
    with in_col2:
        expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=20000.0, step=1000.0)
        st.html('<div class="input-subtext">All your monthly expenses</div>')
    with in_col3:
        savings = st.number_input("Monthly Savings (₹)", min_value=0.0, value=5000.0, step=500.0)
        st.html('<div class="input-subtext">Amount you save monthly</div>')
    with in_col4:
        debt = st.number_input("Monthly Debt Payment (₹)", min_value=0.0, value=2000.0, step=500.0)
        st.html('<div class="input-subtext">EMI or loan payments</div>')

    query_input = st.text_input("💬 Natural Language Financial Query (Optional):", placeholder="e.g. How can I improve my savings with ₹2,000 debt?")

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("✨ Analyze My Finances")

    if analyze_btn:
        exp_ratio = min((expenses / income) * 100, 100.0)
        sav_ratio = min((savings / income) * 100, 100.0)
        dbt_ratio = min((debt / income) * 100, 100.0)
        score, category, rules, mems = evaluate_fuzzy_health(exp_ratio, sav_ratio, dbt_ratio)
        
        st.markdown("<br>", unsafe_allow_html=True)
        res_c1, res_c2 = st.columns([1, 2])
        with res_c1:
            st.html(f"""
            <div class="glass-panel" style="text-align:center;">
                <div style="font-size:13px; color:rgba(255,255,255,0.7);">Fuzzy Financial Health Score</div>
                <div style="font-size:52px; font-weight:800; color:#60a5fa; margin:10px 0;">{score}</div>
                <div style="font-size:16px; font-weight:700;">Status: <span style="color:#c084fc;">{category}</span></div>
            </div>
            """)
        with res_c2:
            st.html(f"""
            <div class="glass-panel">
                <div style="font-size:15px; font-weight:700; margin-bottom:8px;">🧠 Fuzzy Set Evaluation</div>
                <div style="font-size:12px; color:rgba(255,255,255,0.8); line-height:1.8;">
                    • <b>Expense Set Degrees:</b> Low ({mems['exp']['Low']:.2f}), Medium ({mems['exp']['Med']:.2f}), High ({mems['exp']['High']:.2f})<br>
                    • <b>Savings Set Degrees:</b> Poor ({mems['sav']['Poor']:.2f}), Moderate ({mems['sav']['Mod']:.2f}), Good ({mems['sav']['Good']:.2f})<br>
                    • <b>Debt Set Degrees:</b> Low ({mems['dbt']['Low']:.2f}), Medium ({mems['dbt']['Med']:.2f}), High ({mems['dbt']['High']:.2f})
                </div>
            </div>
            """)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.spinner("Generating LangChain Advisory Report..."):
            ai_response = get_ai_advice(query_input, income, expenses, savings, debt, score, category)
            st.html(f"""
            <div class="glass-panel" style="border-left: 4px solid #a855f7;">
                <div style="font-size:15px; font-weight:700; margin-bottom:8px;">🤖 AI Personal Advisory Report</div>
                <div style="font-size:13px; color:rgba(255,255,255,0.9); line-height:1.6;">{ai_response}</div>
            </div>
            """)

# --------------------------------------------------
# PAGE 3: 💳 EXPENSES (INTERACTIVE TRACKER)
# --------------------------------------------------
elif nav_choice == "💳 Expenses":
    st.html("""
    <div class="glass-panel">
        <h2>💳 Expense Categorization & Breakdown</h2>
        <p style="color:rgba(255,255,255,0.7);">Break down your expenses into essential vs discretionary categories.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    ec1, ec2 = st.columns(2)
    with ec1:
        rent = st.number_input("🏠 Rent / Housing (₹)", value=10000.0)
        food = st.number_input("🍔 Food & Groceries (₹)", value=6000.0)
    with ec2:
        utilities = st.number_input("⚡ Utilities & Bills (₹)", value=2000.0)
        leisure = st.number_input("🎬 Shopping & Entertainment (₹)", value=2000.0)
    
    total_e = rent + food + utilities + leisure
    st.markdown("<br>", unsafe_allow_html=True)
    st.html(f"""
    <div class="glass-panel" style="border-left:4px solid #34d399;">
        <h3>Total Categorized Expenses: ₹{total_e:,.0f}</h3>
    </div>
    """)

# --------------------------------------------------
# PAGE 4: ✨ AI ADVISER (FULL CHAT INTERFACE)
# --------------------------------------------------
elif nav_choice == "✨ AI Adviser":
    st.html("""
    <div class="glass-panel">
        <h2>✨ FinWise AI Financial Assistant</h2>
        <p style="color:rgba(255,255,255,0.7);">Ask any natural language financial question. Powered by LangChain and Gemini.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    ai_q = st.text_area("Ask AI Adviser a Question:", value="How can I save ₹10,000 per month on a ₹50,000 salary?")
    if st.button("🤖 Get Financial Advice"):
        with st.spinner("FinWise AI thinking..."):
            res = get_ai_advice(ai_q, 50000, 25000, 15000, 5000, 78.5, "Good")
            st.html(f"""
            <div class="glass-panel" style="border-left:4px solid #38bdf8;">
                <div style="font-size:14px; line-height:1.6; color:#ffffff;">{res}</div>
            </div>
            """)

# --------------------------------------------------
# PAGE 5: 📈 INSIGHTS (ANALYTICS)
# --------------------------------------------------
elif nav_choice == "📈 Insights":
    st.html("""
    <div class="glass-panel">
        <h2>📈 Financial Ratio Analytics</h2>
        <p style="color:rgba(255,255,255,0.7);">Key Performance Ratios recommended by financial planners.</p>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.html("""
        <div class="glass-panel" style="text-align:center;">
            <h4>50-30-20 Rule</h4>
            <p style="font-size:12px; color:rgba(255,255,255,0.7);">50% Needs, 30% Wants, 20% Savings</p>
        </div>
        """)
    with ic2:
        st.html("""
        <div class="glass-panel" style="text-align:center;">
            <h4>Debt-To-Income</h4>
            <p style="font-size:12px; color:rgba(255,255,255,0.7);">Should ideally stay under 36% of gross income.</p>
        </div>
        """)
    with ic3:
        st.html("""
        <div class="glass-panel" style="text-align:center;">
            <h4>Emergency Fund</h4>
            <p style="font-size:12px; color:rgba(255,255,255,0.7);">Maintain at least 3-6 months of expenses.</p>
        </div>
        """)

# --------------------------------------------------
# PAGE 6: ⚙️ SETTINGS
# --------------------------------------------------
elif nav_choice == "⚙️ Settings":
    st.html("""
    <div class="glass-panel">
        <h2>⚙️ App Settings & Configuration</h2>
    </div>
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    st.text_input("User Name:", value="Vikas Pal")
    st.selectbox("Default Currency:", ["INR (₹)", "USD ($)", "EUR (€)"])
    api_status = "Configured ✅" if os.getenv("GOOGLE_API_KEY") else "Missing ⚠️"
    st.info(f"Google Gemini API Status: {api_status}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.html("""
<div style="text-align:center; padding:30px 0 10px 0; font-size:11px; color:rgba(255,255,255,0.5);">
    Built with Streamlit &nbsp;|&nbsp; Powered by AI &nbsp;|&nbsp; © 2026 FinWise ❤️
</div>
""")