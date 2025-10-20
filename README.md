# DG-s_retirement_agent_with_shortfall_report.py
import streamlit as st
from math import pow
from datetime import datetime

st.set_page_config(page_title="Retirement Planner", page_icon="💰")

st.title("💰 Simple Retirement Planner & Savings Calculator")
st.write("Educational tool — not financial advice.")

# User Inputs
age = st.number_input("Current age", min_value=18, max_value=100, value=30)
retire_age = st.number_input("Target retirement age", min_value=age+1, max_value=100, value=65)
current_savings = st.number_input("Current retirement savings ($)", min_value=0.0, value=10000.0)
monthly_contribution = st.number_input("Monthly contribution ($)", min_value=0.0, value=500.0)
expected_return = st.slider("Expected annual return (%)", 0.0, 15.0, 6.0)
goal = st.number_input("Retirement savings goal ($)", min_value=0.0, value=1000000.0)

# Function to project savings
def project_savings(current_savings, monthly_contribution, years, annual_return):
    r = annual_return / 100 / 12
    months = years * 12
    fv = current_savings * pow(1 + r, months)
    for m in range(1, months + 1):
        fv += monthly_contribution * pow(1 + r, months - m + 1)
    return fv

years = retire_age - age

if st.button("Calculate"):
    if years <= 0:
        st.error("⚠️ Retirement age must be greater than current age.")
    else:
        projected = project_savings(current_savings, monthly_contribution, years, expected_return)
        st.subheader(f"📊 Projected Savings at Age {retire_age}: ${projected:,.2f}")
        if projected < goal:
            shortfall = goal - projected
            st.error(f"⚠️ You are projected to fall short by ${shortfall:,.2f}")
            # Suggest how much more monthly to save
            r = expected_return / 100 / 12
            months = years * 12
            future_factor = sum(pow(1 + r, months - m + 1) for m in range(1, months + 1))
            needed_extra = shortfall / future_factor
            st.info(f"💡 To hit your goal, you need to save about **${needed_extra:,.2f} more per month.**")
        else:
            st.success("✅ You're on track to reach or exceed your goal!")
