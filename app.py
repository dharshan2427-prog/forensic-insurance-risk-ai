import streamlit as st

st.set_page_config(
    page_title="Forensic Insurance Risk AI",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Forensic Insurance Risk Assessment")
st.subheader("AI-Powered Insurance Claim Analysis")

st.write(
    "This system assists insurance investigators in identifying "
    "claims that may require further investigation."
)

st.divider()

st.header("📋 Claim Information")

claim_id = st.text_input("Claim ID")

claim_type = st.selectbox(
    "Claim Type",
    ["Vehicle", "Property", "Health", "Life", "Other"]
)

claim_amount = st.number_input(
    "Claim Amount (₹)",
    min_value=0.0,
    step=1000.0
)

previous_claims = st.number_input(
    "Number of Previous Claims",
    min_value=0,
    step=1
)

evidence_status = st.selectbox(
    "Evidence Status",
    ["Complete", "Incomplete", "Inconsistent"]
)

if st.button("🔍 Assess Risk"):

    if claim_id == "":
        st.warning("Please enter a Claim ID.")

    else:
        st.success("Claim information received.")

        st.header("📊 Risk Assessment")

        if claim_amount > 500000 or previous_claims >= 5 or evidence_status == "Inconsistent":
            risk = "HIGH RISK"
        elif claim_amount > 200000 or previous_claims >= 2:
            risk = "MEDIUM RISK"
        else:
            risk = "LOW RISK"

        st.metric("Risk Level", risk)

        st.info(
            "⚠️ This assessment is a decision-support tool. "
            "It does not prove insurance fraud. Further investigation "
            "should be conducted by qualified personnel."
        )
