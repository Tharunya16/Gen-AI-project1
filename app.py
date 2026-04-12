import streamlit as st
import random

# -----------------------------
# INIT SESSION STATE (IMPORTANT FIX)
# -----------------------------
if "analysis_done" not in st.session_state:
    st.session_state["analysis_done"] = False
if "fertility" not in st.session_state:
    st.session_state["fertility"] = ""
if "crops" not in st.session_state:
    st.session_state["crops"] = ""
if "soil_score" not in st.session_state:
    st.session_state["soil_score"] = 0

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="GenAI Smart Agriculture Assistant", layout="wide")

st.title("🌱 GenAI Smart Agriculture Assistant")
st.write("AI-Based Soil Analysis, Crop Recommendation & Advisory System")

st.markdown("## 🧪 Enter Soil Nutrient Values")

# -----------------------------
# Input Fields
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Macronutrients")
    N = st.number_input("Nitrogen (N)", min_value=0.0)
    P = st.number_input("Phosphorus (P)", min_value=0.0)
    K = st.number_input("Potassium (K)", min_value=0.0)

with col2:
    st.subheader("Soil Properties")
    pH = st.number_input("pH", min_value=0.0)
    EC = st.number_input("Electrical Conductivity (EC)", min_value=0.0)
    OC = st.number_input("Organic Carbon (OC)", min_value=0.0)
    S = st.number_input("Sulphur (S)", min_value=0.0)

with col3:
    st.subheader("Micronutrients")
    Zn = st.number_input("Zinc (Zn)", min_value=0.0)
    Fe = st.number_input("Iron (Fe)", min_value=0.0)
    Cu = st.number_input("Copper (Cu)", min_value=0.0)
    Mn = st.number_input("Manganese (Mn)", min_value=0.0)
    B = st.number_input("Boron (B)", min_value=0.0)

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🔍 Analyze Soil"):

    with st.spinner("Analyzing soil using AI... 🌱"):

        score = 0
        explanation = []
        recommendation = []

        # Soil Type
        if pH < 6:
            soil_type = "Acidic Soil"
            soil_tamil = "அமில மண்"
        elif pH > 7.5:
            soil_type = "Alkaline Soil"
            soil_tamil = "கார மண்"
        else:
            soil_type = "Neutral Soil"
            soil_tamil = "நடுநிலை மண்"

        # -----------------------------
        # SMART SCORING SYSTEM (UPGRADE)
        # -----------------------------
        if 150 <= N <= 250:
            score += 35
            explanation.append("Nitrogen is in optimal range supporting healthy growth.")
        else:
            score += 10
            explanation.append("Nitrogen imbalance detected affecting crop growth.")
            recommendation.append("Adjust nitrogen using organic manure or urea.")

        if P >= 8:
            score += 25
        else:
            score += 10
            explanation.append("Low phosphorus affecting root development.")
            recommendation.append("Use phosphate fertilizers.")

        if K >= 100:
            score += 25
        else:
            score += 10
            explanation.append("Low potassium reducing plant resistance.")
            recommendation.append("Apply potash fertilizers.")

        if OC >= 0.8:
            score += 15
        else:
            score += 5
            explanation.append("Low organic carbon affecting soil fertility.")
            recommendation.append("Add compost and organic matter.")

        # Soil Health Level
        if score >= 80:
            fertility = "High Fertility"
        elif score >= 50:
            fertility = "Medium Fertility"
        else:
            fertility = "Low Fertility"

        # Crop Recommendation
        if fertility == "Low Fertility":
            crops = "Millets, Pulses"
        elif fertility == "Medium Fertility":
            crops = "Rice, Wheat"
        else:
            crops = "Sugarcane, Cotton"

        # STORE FOR CHATBOT
        st.session_state["fertility"] = fertility
        st.session_state["crops"] = crops
        st.session_state["analysis_done"] = True
        st.session_state["soil_score"] = score

        # -----------------------------
        # GENAI STYLE TEXT
        # -----------------------------
        intro = random.choice([
            "AI has carefully analyzed your soil data and generated insights.",
            "Your soil parameters were evaluated using intelligent analysis.",
            "The system processed nutrient levels and produced this advisory report."
        ])

        conclusion = random.choice([
            "Healthy soil management ensures sustainable farming success.",
            "Balanced nutrients are key to long-term productivity.",
            "Consistent soil care leads to better agricultural output."
        ])

        result = f"""
# 🌱 AI Soil Intelligence Report

📊 **Soil Health Score:** {score}/100  
🌾 **Soil Fertility:** {fertility}  
🌍 **Soil Type:** {soil_type} ({soil_tamil})

---

## 🧠 AI Analysis
{intro}

{" ".join(explanation)}

---

## 🌱 Recommendations (Priority Based)
{" • ".join(recommendation) if recommendation else "Soil conditions are well balanced."}

---

## 🌾 Suitable Crops
👉 {crops}

---

## 📌 Final Insight
{conclusion}
"""

    st.success("Analysis Completed ✅")
    st.markdown(result)

# -----------------------------
# 💬 CHATBOT (UPGRADED GENAI FEEL)
# -----------------------------
st.markdown("## 💬 Ask AI about Soil / Crops")

user_q = st.text_input("Ask your question:")

if user_q:

    if not st.session_state.get("analysis_done", False):
        st.warning("⚠ Please analyze soil first before asking questions.")
    else:
        fertility = st.session_state["fertility"]
        crops = st.session_state["crops"]
        score = st.session_state["soil_score"]

        q = user_q.lower()

        # -----------------------------
        # SMART CONTEXT RESPONSES
        # -----------------------------
        if any(word in q for word in ["crop", "grow", "rice", "wheat", "millet"]):
            response = f"""
Based on your soil intelligence report:

🌾 Fertility Level: **{fertility}**  
📊 Soil Score: **{score}/100**

👉 Recommended Crops:
{crops}

💡 This recommendation is based on nutrient balance analysis.
"""

        elif "fertility" in q:
            response = f"""
Your soil is classified as:

🌱 **{fertility}**

This is derived from overall nutrient balance including NPK and organic carbon levels.
"""

        elif any(word in q for word in ["improve", "better", "fertilizer"]):
            response = f"""
To improve your soil:

✔ Add organic compost  
✔ Maintain balanced NPK levels  
✔ Improve organic carbon content  
✔ Follow crop rotation practices  

💡 Current Soil Score: {score}/100
"""

        else:
            response = """
I am your Soil Intelligence Assistant 🤖

You can ask:
🌾 Best crops for my soil  
🌱 How to improve fertility  
📊 Soil health explanation  
"""

        st.info("🤖 AI Response")
        st.write(response)