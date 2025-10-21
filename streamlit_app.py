import streamlit as st
from math import pow

st.set_page_config(page_title="URPA", page_icon="💰")
st.title("💰 Ultimate Retirement Planning Agent")
st.write("Educational tool — not financial advice. Helps estimate your retirement savings and investment options.")

# -----------------------------
# User Inputs
# -----------------------------
st.header("👤 Personal Information")
age = st.number_input("Current Age", min_value=18, max_value=100, value=30)
retire_age = st.number_input("Target Retirement Age", min_value=age+1, max_value=100, value=65)
employment = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Government/Nonprofit", "Not Working"])
income = st.number_input("Annual Income ($)", min_value=0, value=80000)
risk = st.radio("Risk Comfort Level", ["Low", "Medium", "High"])
has_401k = False
if employment == "Employed":
    has_401k = st.radio("Do you have access to a 401(k)?", ["Yes", "No"]) == "Yes"

# -----------------------------
# Retirement Account Options
# -----------------------------
st.header("Suggested Retirement Accounts and Risks")

accounts = {
    "401(k)": {"who": "Employed", "return": 0.07, "risk": "Market risk; employer match is free money"},
    "403(b)": {"who": "Nonprofits / Schools", "return": 0.07, "risk": "Similar to 401(k); investment risk applies"},
    "457(b)": {"who": "Government / Nonprofits", "return": 0.07, "risk": "Withdrawal restrictions; market risk"},
    "Roth IRA": {"who": "Individuals (income limits)", "return": 0.07, "risk": "Tax-free withdrawals; market risk"},
    "Traditional IRA": {"who": "Anyone", "return": 0.07, "risk": "Tax-deferred growth; market risk"},
    "SEP IRA": {"who": "Self-employed", "return": 0.07, "risk": "High contribution limits; market risk"},
    "Solo 401(k)": {"who": "Self-employed", "return": 0.07, "risk": "High contribution limits; market risk"},
    "Taxable Brokerage": {"who": "Anyone", "return": 0.07, "risk": "No tax advantages; market risk"}
}

suggested_accounts = []
for name, data in accounts.items():
    if employment.lower() in data["who"].lower() or data["who"]=="Anyone":
        st.subheader(name)
        st.write(f"Who can use: {data['who']}")
        st.write(f"Expected Average Return: {data['return']*100:.1f}% per year")
        st.write(f"Risks: {data['risk']}")
        suggested_accounts.append(name)

# -----------------------------
# Investment Options
# -----------------------------
st.header("Investment Options")
st.write("Select preferred investment type for your retirement accounts:")

investment_options = {
    "Vanguard Target Date Fund": {"return": 0.065, "risk": "Balanced diversified fund; moderate risk"},
    "S&P 500 Index Fund": {"return": 0.08, "risk": "Stocks only; higher growth, higher volatility"},
    "Total Stock Market Fund": {"return": 0.075, "risk": "U.S. stocks diversified; moderate-high risk"},
    "Total Bond Market Fund": {"return": 0.035, "risk": "Bonds; lower risk, lower return"},
    "International Stock Fund": {"return": 0.07, "risk": "Foreign stocks; currency and market risk"}
}

selected_investment = st.selectbox("Choose an investment option", list(investment_options.keys()))
inv_return = investment_options[selected_investment]["return"]
inv_risk = investment_options[selected_investment]["risk"]
st.write(f"Expected Return: {inv_return*100:.1f}% per year | Risk: {inv_risk}")

# -----------------------------
# Savings Calculator
# -----------------------------
st.header("Retirement Savings Calculator")
current_savings = st.number_input("Current Retirement Savings ($)", 0, 5_000_000, 10000)
monthly_contribution = st.number_input("Monthly Contribution ($)", 0, 50_000, 500)
goal = st.number_input("Target Retirement Savings Goal ($)", 0, 10_000_000, 1000000)

def project_savings(current, monthly, years, annual_return):
    r = annual_return / 12
    months = years * 12
    fv = current * pow(1 + r, months)
    for m in range(1, months+1):
        fv += monthly * pow(1 + r, months - m + 1)
    return fv

if st.button("Calculate Overall Savings"):
    years = retire_age - age
    projected = project_savings(current_savings, monthly_contribution, years, inv_return)
    st.subheader(f"Projected Savings at Retirement (age {retire_age}): ${projected:,.2f}")

    if projected < goal:
        shortfall = goal - projected
        st.error(f"⚠️ Shortfall: ${shortfall:,.2f}")
        # Extra monthly contribution needed
        r = inv_return / 12
        months = years * 12
        future_factor = sum(pow(1+r, months - m + 1) for m in range(1, months+1))
        extra_monthly = shortfall / future_factor
        st.info(f"💡 To meet your goal, save an extra **${extra_monthly:.2f} per month**")
    else:
        st.success("✅ On track to meet or exceed your retirement goal!")

st.markdown("---")
st.caption("⚠️ This tool is educational only and not financial advice. Always consult a licensed advisor.")
