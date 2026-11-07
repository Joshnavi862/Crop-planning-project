import streamlit as st
import pandas as pd
import plotly.express as px
from modules.input_validation import validate_inputs
from modules.crop_recommendation import recommend_crops, estimate_yield, calculate_budget, cultivation_plan
from modules.prompt_generator import build_crop_prompt, compare_prompt_styles, answer_agriculture_question

st.set_page_config(page_title="Smart Crop Planner", page_icon="🌱", layout="wide")
st.title("🌱 AI-Based Crop Planning & Yield Recommendation")
st.caption("A student-friendly agriculture decision-support prototype. Verify recommendations with local agricultural experts.")

with st.sidebar:
    st.header("Farmer profile")
    location = st.text_input("Location / District", "Ongole, Andhra Pradesh")
    season = st.selectbox("Growing season", ["Kharif", "Rabi", "Summer", "Year-round"])
    soil = st.selectbox("Soil type", ["Loamy", "Clay", "Sandy", "Silty", "Black", "Red"])
    ph = st.slider("Soil pH", 3.5, 10.0, 6.5, 0.1)
    n = st.number_input("Nitrogen (N) - soil test value", min_value=0.0, max_value=500.0, value=60.0)
    p = st.number_input("Phosphorus (P) - soil test value", min_value=0.0, max_value=500.0, value=35.0)
    k = st.number_input("Potassium (K) - soil test value", min_value=0.0, max_value=500.0, value=40.0)
    water = st.selectbox("Irrigation availability", ["Reliable", "Limited", "Rain-fed"])
    area = st.number_input("Land area (acres)", min_value=0.1, max_value=10000.0, value=2.0, step=0.1)
    budget = st.number_input("Available budget (₹)", min_value=0, value=50000, step=1000)
    market_price = st.number_input("Expected selling price (₹ per quintal)", min_value=0, value=2200, step=50)

inputs = {"location": location, "season": season, "soil": soil, "ph": ph, "n": n, "p": p, "k": k,
          "water": water, "area": area, "budget": budget, "market_price": market_price}
errors = validate_inputs(inputs)
if errors:
    for err in errors:
        st.error(err)

tabs = st.tabs(["Dashboard", "Crop recommendations", "Cultivation plan", "Budget & yield", "AI agriculture chatbot", "Prompt lab"])
crops = recommend_crops(inputs) if not errors else []
yield_rows = []
for crop in crops:
    y = estimate_yield(crop, area)
    yield_rows.append({"Crop": crop["name"], "Expected yield (quintals)": y["typical"], "Revenue (₹)": y["typical"] * market_price})

with tabs[0]:
    st.subheader("Recommendation dashboard")
    if crops:
        best = crops[0]
        y = estimate_yield(best, area)
        costs = calculate_budget(best, area, market_price, y["typical"])
        a, b, c, d = st.columns(4)
        a.metric("Top recommendation", best["name"])
        b.metric("Typical estimated yield", f'{y["typical"]:,.1f} q')
        c.metric("Estimated cost", f'₹{costs["total"]:,.0f}')
        d.metric("Estimated profit", f'₹{costs["profit"]:,.0f}')
        st.info(f"Profile: {location} · {season} · {soil} soil · {area:g} acres")
        df = pd.DataFrame(yield_rows)
        st.plotly_chart(px.bar(df, x="Crop", y="Expected yield (quintals)", title="Illustrative yield comparison"), use_container_width=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Enter valid farmer details to view recommendations.")

with tabs[1]:
    st.subheader("Suitable crop options")
    for i, crop in enumerate(crops, start=1):
        with st.expander(f"{i}. {crop['name']} — suitability score {crop['score']}/100", expanded=(i == 1)):
            st.write(crop["reason"])
            st.write(f"**Water need:** {crop['water_need']} · **Growing duration:** {crop['duration_days']} days")
            st.write(f"**Typical yield assumption:** {crop['yield_quintals_per_acre']} quintals/acre")
            st.caption("Suitability score is a simple prototype score, not a validated agronomic prediction.")

with tabs[2]:
    st.subheader("Smart cultivation plan")
    selected_name = st.selectbox("Choose a crop", [c["name"] for c in crops] or ["No recommendation"])
    selected = next((c for c in crops if c["name"] == selected_name), None)
    if selected:
        st.dataframe(pd.DataFrame(cultivation_plan(selected, season)), use_container_width=True, hide_index=True)
        st.warning("Adjust timing and inputs to local crop calendars, soil-test advice, and extension officer recommendations.")

with tabs[3]:
    st.subheader("Budget calculator and yield scenarios")
    selected_name2 = st.selectbox("Crop for financial estimate", [c["name"] for c in crops] or ["No recommendation"], key="budget_crop")
    selected2 = next((c for c in crops if c["name"] == selected_name2), None)
    if selected2:
        y = estimate_yield(selected2, area)
        costs = calculate_budget(selected2, area, market_price, y["typical"])
        left, right = st.columns(2)
        with left:
            st.markdown("**Yield scenarios (quintals)**")
            st.write(f"Conservative: {y['low']:,.1f}")
            st.write(f"Typical: {y['typical']:,.1f}")
            st.write(f"Optimistic: {y['high']:,.1f}")
        with right:
            st.markdown("**Estimated budget (₹)**")
            st.write(f"Seeds: ₹{costs['seeds']:,.0f}")
            st.write(f"Fertilizer & soil inputs: ₹{costs['fertilizer']:,.0f}")
            st.write(f"Labour: ₹{costs['labour']:,.0f}")
            st.write(f"Irrigation & machinery: ₹{costs['operations']:,.0f}")
            st.write(f"Other costs: ₹{costs['other']:,.0f}")
            st.write(f"**Total cost: ₹{costs['total']:,.0f}**")
            st.write(f"Expected revenue: ₹{costs['revenue']:,.0f}")
            st.write(f"**Estimated profit/loss: ₹{costs['profit']:,.0f}**")
        if costs["total"] > budget:
            st.error(f"Estimated cost exceeds your stated budget by ₹{costs['total'] - budget:,.0f}.")
        else:
            st.success(f"Estimated cost is within your stated budget (₹{budget - costs['total']:,.0f} remaining).")
        st.caption("All cost, price, and yield values are editable prototype assumptions; actual values vary by region and season.")

with tabs[4]:
    st.subheader("AI agriculture chatbot")
    question = st.text_area("Ask an agriculture question", placeholder="Example: How should I prepare loamy soil before sowing?")
    if st.button("Get guidance", type="primary"):
        if question.strip():
            st.markdown(answer_agriculture_question(question, inputs))
        else:
            st.warning("Please enter a question.")

with tabs[5]:
    st.subheader("Prompt templates and comparison")
    question = st.text_area("Agriculture task to prompt", "Recommend suitable crops for a farmer with loamy soil and limited irrigation.", key="prompt_q")
    context = {"location": location, "season": season, "soil": soil, "ph": ph, "n": n, "p": p, "k": k, "water": water, "area": area, "budget": budget}
    if st.button("Generate and compare prompts"):
        prompts = compare_prompt_styles(question, context)
        col1, col2, col3 = st.columns(3)
        for col, (label, prompt) in zip([col1, col2, col3], prompts.items()):
            with col:
                st.markdown(f"**{label}**")
                st.code(prompt, language="text")
        st.caption("Compare specificity, role/context, output structure, and safety instructions. These are prompt drafts, not verified agricultural advice.")

st.divider()
st.caption("Educational prototype · No crop, yield, profit, pesticide, or fertilizer outcome is guaranteed.")
