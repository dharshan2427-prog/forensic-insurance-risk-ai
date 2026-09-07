import streamlit as st
import pandas as pd
import pickle

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Forensic Insurance Risk Assessment",
    page_icon="🔍",
    layout="wide"
)

# --------------------------------------------------
# LOAD MACHINE LEARNING MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    with open("insurance_risk_model_v3b.pkl", "rb") as file:
        model = pickle.load(file)
    return model

try:
    model = load_model()
except Exception as e:
    st.error("Unable to load the trained ML model.")
    st.error(str(e))
    st.stop()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🔍 Forensic Insurance Risk Assessment")
st.write(
    "AI-powered prototype for preliminary insurance claim risk assessment."
)

st.info(
    "This prototype provides a machine-learning-based risk classification "
    "and is not a final fraud determination."
)

# --------------------------------------------------
# CLAIM INFORMATION
# --------------------------------------------------

st.header("📋 Claim Information")

col1, col2 = st.columns(2)

with col1:
    claim_id = st.text_input(
        "Claim ID",
        value="FIR-004"
    )

    claim_type = st.selectbox(
        "Claim Type",
        ["Vehicle", "Property", "Health", "Fire", "Other"]
    )

    claim_amount = st.number_input(
        "Claim Amount (₹)",
        min_value=0.0,
        value=300000.0,
        step=10000.0
    )

    previous_claims = st.number_input(
        "Number of Previous Claims",
        min_value=0,
        max_value=50,
        value=2,
        step=1
    )

with col2:
    rejected_claims = st.number_input(
        "Number of Rejected Claims",
        min_value=0,
        max_value=50,
        value=0,
        step=1
    )

    claim_frequency = st.selectbox(
        "High Claim Frequency?",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    evidence_status = st.selectbox(
        "Evidence Status",
        [0, 1, 2],
        format_func=lambda x: {
            0: "Incomplete",
            1: "Complete",
            2: "Strong"
        }[x]
    )

    document_consistency = st.selectbox(
        "Document Consistency",
        [0, 1, 2],
        format_func=lambda x: {
            0: "Inconsistent",
            1: "Partially Consistent",
            2: "Consistent"
        }[x]
    )

    claim_after_policy = st.number_input(
        "Days After Policy Started",
        min_value=0,
        max_value=3650,
        value=30,
        step=1
    )

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

st.divider()

if st.button("🔍 Assess Risk", use_container_width=True):

    # Features must match the Version 3B training model
    input_data = pd.DataFrame({
        "claim_amount": [claim_amount],
        "previous_claims": [previous_claims],
        "rejected_claims": [rejected_claims],
        "claim_frequency": [claim_frequency],
        "evidence_status": [evidence_status],
        "document_consistency": [document_consistency],
        "claim_after_policy": [claim_after_policy]
    })

    try:
        prediction = model.predict(input_data)[0]

        # Get probability if the model supports it
        try:
            probabilities = model.predict_proba(input_data)[0]
            classes = model.classes_

            probability_dict = {
                str(classes[i]): float(probabilities[i])
                for i in range(len(classes))
            }

            confidence = max(probabilities) * 100

        except Exception:
            probability_dict = {}
            confidence = None

        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        st.header("📊 Risk Assessment")

        risk = str(prediction).upper()

        if risk == "HIGH":
            st.error("🔴 HIGH RISK")
        elif risk == "MEDIUM":
            st.warning("🟡 MEDIUM RISK")
        else:
            st.success("🟢 LOW RISK")

        # --------------------------------------------------
        # CLAIM SUMMARY
        # --------------------------------------------------

        st.subheader("Claim Summary")

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:
            st.metric("Claim ID", claim_id)

        with summary_col2:
            st.metric("Claim Type", claim_type)

        with summary_col3:
            st.metric("Claim Amount", f"₹{claim_amount:,.2f}")

        # --------------------------------------------------
        # CONFIDENCE
        # --------------------------------------------------

        if confidence is not None:
            st.subheader("🤖 Model Confidence")
            st.progress(int(confidence))
            st.write(f"Prediction confidence: **{confidence:.2f}%**")

        # --------------------------------------------------
        # RISK PROBABILITIES
        # --------------------------------------------------

        if probability_dict:

            st.subheader("Risk Probability")

            probability_data = pd.DataFrame({
                "Risk Level": list(probability_dict.keys()),
                "Probability (%)": [
                    value * 100
                    for value in probability_dict.values()
                ]
            })

            st.dataframe(
                probability_data,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # RISK FACTORS
        # --------------------------------------------------

        st.subheader("🔎 Claim Risk Indicators")

        factors = []

        if claim_amount >= 500000:
            factors.append("High claim amount")

        if previous_claims >= 5:
            factors.append("High number of previous claims")

        if rejected_claims >= 2:
            factors.append("Previous rejected claims present")

        if claim_frequency == 1:
            factors.append("High claim frequency")

        if evidence_status == 0:
            factors.append("Incomplete evidence")

        if document_consistency == 0:
            factors.append("Document inconsistency")

        if claim_after_policy <= 30:
            factors.append("Claim submitted shortly after policy started")

        if factors:
            for factor in factors:
                st.write("• " + factor)
        else:
            st.write("No major risk indicators identified from the entered information.")

        # --------------------------------------------------
        # RECOMMENDATION
        # --------------------------------------------------

        st.subheader("📌 Preliminary Recommendation")

        if risk == "HIGH":
            st.error(
                "Recommend detailed investigation and verification "
                "before claim settlement."
            )

        elif risk == "MEDIUM":
            st.warning(
                "Recommend additional document and evidence verification "
                "before final decision."
            )

        else:
            st.success(
                "Claim shows lower predicted risk based on the available "
                "input features. Normal verification procedures should "
                "still be followed."
            )

        # --------------------------------------------------
        # TECHNICAL INFORMATION
        # --------------------------------------------------

        with st.expander("View ML Model Input"):

            st.dataframe(
                input_data,
                use_container_width=True,
                hide_index=True
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Forensic Insurance Risk Assessment – Version 4 ML Prototype"
)
