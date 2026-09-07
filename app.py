import streamlit as st

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Forensic Insurance Risk AI",
    page_icon="🔎",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🔎 Forensic Insurance Risk Assessment")
st.subheader("AI-Powered Insurance Claim Analysis")

st.write(
    "A decision-support prototype for preliminary insurance "
    "claim risk assessment."
)

st.divider()

# ============================================================
# 1. CLAIM INFORMATION
# ============================================================

st.header("📋 1. Claim Information")

col1, col2 = st.columns(2)

with col1:
    claim_id = st.text_input(
        "Claim ID",
        placeholder="Example: FIR-1001"
    )

    claim_type = st.selectbox(
        "Claim Type",
        [
            "Vehicle",
            "Property",
            "Health",
            "Life",
            "Travel",
            "Other"
        ]
    )

with col2:
    claim_amount = st.number_input(
        "Claim Amount (₹)",
        min_value=0.0,
        step=1000.0
    )

    claim_date = st.date_input(
        "Claim Date"
    )

# ============================================================
# 2. POLICY INFORMATION
# ============================================================

st.divider()
st.header("📄 2. Policy Information")

col1, col2 = st.columns(2)

with col1:
    policy_type = st.selectbox(
        "Policy Type",
        [
            "Comprehensive",
            "Third Party",
            "Health Insurance",
            "Life Insurance",
            "Property Insurance",
            "Travel Insurance",
            "Other"
        ]
    )

    policy_status = st.selectbox(
        "Policy Status",
        [
            "Active",
            "Expired",
            "Cancelled",
            "Under Review"
        ]
    )

with col2:
    policy_duration = st.number_input(
        "Policy Duration (months)",
        min_value=1,
        max_value=600,
        value=12
    )

    claim_after_policy = st.number_input(
        "Months Between Policy Start and Claim",
        min_value=0,
        max_value=600,
        value=6
    )

# ============================================================
# 3. CLAIMANT INFORMATION
# ============================================================

st.divider()
st.header("👤 3. Claimant Information")

col1, col2 = st.columns(2)

with col1:
    claimant_age = st.number_input(
        "Claimant Age",
        min_value=18,
        max_value=100,
        value=30
    )

    previous_claims = st.number_input(
        "Number of Previous Claims",
        min_value=0,
        max_value=100,
        value=0
    )

with col2:
    rejected_claims = st.number_input(
        "Number of Previously Rejected Claims",
        min_value=0,
        max_value=100,
        value=0
    )

    claim_frequency = st.selectbox(
        "Recent Claim Frequency",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

# ============================================================
# 4. EVIDENCE INFORMATION
# ============================================================

st.divider()
st.header("🔬 4. Evidence Information")

col1, col2 = st.columns(2)

with col1:
    evidence_status = st.selectbox(
        "Evidence Status",
        [
            "Complete",
            "Incomplete",
            "Inconsistent"
        ]
    )

    document_count = st.number_input(
        "Number of Supporting Documents",
        min_value=0,
        max_value=100,
        value=3
    )

    document_consistency = st.selectbox(
        "Document Consistency",
        [
            "Consistent",
            "Minor Differences",
            "Major Differences"
        ]
    )

with col2:
    police_report = st.selectbox(
        "Police Report Available?",
        [
            "Yes",
            "No",
            "Not Applicable"
        ]
    )

    medical_report = st.selectbox(
        "Medical / Repair Report Available?",
        [
            "Yes",
            "No",
            "Not Applicable"
        ]
    )

# ============================================================
# 5. RISK ASSESSMENT
# ============================================================

st.divider()
st.header("📊 5. Preliminary Risk Assessment")

if st.button("🔍 Assess Claim Risk", use_container_width=True):

    if claim_id == "":
        st.warning("Please enter a Claim ID.")

    else:

        # -----------------------------
        # SIMPLE PROTOTYPE SCORING
        # -----------------------------

        risk_score = 0
        risk_factors = []

        # Claim amount
        if claim_amount >= 500000:
            risk_score += 25
            risk_factors.append(
                "High claim amount"
            )

        elif claim_amount >= 200000:
            risk_score += 15
            risk_factors.append(
                "Moderately high claim amount"
            )

        # Previous claims
        if previous_claims >= 5:
            risk_score += 25
            risk_factors.append(
                "Multiple previous claims"
            )

        elif previous_claims >= 2:
            risk_score += 15
            risk_factors.append(
                "Several previous claims"
            )

        # Rejected claims
        if rejected_claims >= 3:
            risk_score += 20
            risk_factors.append(
                "Multiple previously rejected claims"
            )

        elif rejected_claims >= 1:
            risk_score += 10
            risk_factors.append(
                "Previous rejected claim(s)"
            )

        # Claim frequency
        if claim_frequency == "High":
            risk_score += 15
            risk_factors.append(
                "High recent claim frequency"
            )

        elif claim_frequency == "Medium":
            risk_score += 5

        # Evidence
        if evidence_status == "Inconsistent":
            risk_score += 20
            risk_factors.append(
                "Inconsistent evidence"
            )

        elif evidence_status == "Incomplete":
            risk_score += 10
            risk_factors.append(
                "Incomplete evidence"
            )

        # Documents
        if document_consistency == "Major Differences":
            risk_score += 15
            risk_factors.append(
                "Major differences between documents"
            )

        elif document_consistency == "Minor Differences":
            risk_score += 5

        # Policy timing
        if claim_after_policy <= 1:
            risk_score += 10
            risk_factors.append(
                "Claim made shortly after policy start"
            )

        # Limit score
        risk_score = min(risk_score, 100)

        # -----------------------------
        # RISK LEVEL
        # -----------------------------

        if risk_score >= 60:
            risk_level = "🔴 HIGH RISK"
            recommendation = (
                "Further investigation is recommended."
            )

        elif risk_score >= 30:
            risk_level = "🟡 MEDIUM RISK"
            recommendation = (
                "Additional verification may be appropriate."
            )

        else:
            risk_level = "🟢 LOW RISK"
            recommendation = (
                "No major risk indicators identified "
                "from the information provided."
            )

        # -----------------------------
        # DISPLAY RESULT
        # -----------------------------

        st.success("Claim information received.")

        st.subheader("Risk Assessment Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Risk Score",
                f"{risk_score}/100"
            )

        with col2:
            st.metric(
                "Risk Level",
                risk_level
            )

        st.progress(risk_score / 100)

        # -----------------------------
        # RISK FACTORS
        # -----------------------------

        st.subheader("⚠️ Identified Risk Indicators")

        if risk_factors:
            for factor in risk_factors:
                st.write("• " + factor)
        else:
            st.write(
                "No major risk indicators identified."
            )

        # -----------------------------
        # RECOMMENDATION
        # -----------------------------

        st.subheader("🕵️ Investigator Recommendation")

        st.info(recommendation)

        # -----------------------------
        # DISCLAIMER
        # -----------------------------

        st.warning(
            "This is a prototype decision-support system. "
            "A high-risk result does not prove fraud. "
            "Final decisions should be made by qualified "
            "insurance and forensic professionals."
        )
