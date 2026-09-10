import streamlit as st
import joblib
import pandas as pd
import os


# ============================================================
# INSURIX | INSURANCE RISK INTELLIGENCE
# VERSION 4 - RANDOM FOREST
# ============================================================

st.set_page_config(
    page_title="Insurix | Insurance Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD VERSION 4 RANDOM FOREST MODEL
# ============================================================

MODEL_FILE = "insurance_risk_model_v4.pkl"

if not os.path.exists(MODEL_FILE):
    st.error(
        "Version 4 model file was not found. "
        "Please make sure insurance_risk_model_v4.pkl is in the repository."
    )
    st.stop()

try:
    model_package = joblib.load(MODEL_FILE)

    model = model_package["model"]
    label_encoder = model_package["label_encoder"]
    features = model_package["features"]

except Exception as e:
    st.error("Unable to load the Version 4 Random Forest model.")
    st.code(str(e))
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Overview"

if "last_risk" not in st.session_state:
    st.session_state.last_risk = None

if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = None

if "last_probabilities" not in st.session_state:
    st.session_state.last_probabilities = None

if "assessment_done" not in st.session_state:
    st.session_state.assessment_done = False


# ============================================================
# SIMPLE PROFESSIONAL CSS
# No HTML UI blocks are used.
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #07152f;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main headings */
    h1 {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #07152f !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #07152f !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #12325f !important;
        font-weight: 700 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #159bd7;
        color: white;
        border: none;
        border-radius: 9px;
        padding: 0.65rem 1.2rem;
        font-weight: 700;
        min-height: 44px;
    }

    .stButton > button:hover {
        background-color: #087fba;
        color: white;
        border: none;
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 8px;
    }

    /* Cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e4eaf2;
        border-radius: 14px;
        padding: 18px;
    }

    /* Info boxes */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Horizontal line */
    hr {
        border-color: #e3e8ef;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛡️ Insurix")

    st.caption(
        "AI-Powered Forensic\n"
        "Insurance Risk Assessment"
    )

    st.divider()

    st.markdown("### NAVIGATION")

    selected_page = st.radio(
        "Navigation",
        [
            "Overview",
            "Claim Assessment",
            "Documents",
            "Claim Status"
        ],
        index=[
            "Overview",
            "Claim Assessment",
            "Documents",
            "Claim Status"
        ].index(st.session_state.page),
        label_visibility="collapsed"
    )

    st.session_state.page = selected_page

    st.divider()

    st.markdown("### SYSTEM")

    st.success("System operational")

    st.caption("Version 4 • Random Forest")

    st.divider()

    st.caption(
        "Insurix provides preliminary "
        "AI-assisted claim risk assessment."
    )


# ============================================================
# OVERVIEW PAGE
# ============================================================

if st.session_state.page == "Overview":

    st.caption("INSURIX / 01")

    st.title("Overview")

    st.write(
        "Smarter insurance. Stronger evidence."
    )

    st.divider()

    # Hero section
    hero_left, hero_right = st.columns([2.2, 1])

    with hero_left:

        st.info("FORENSIC × INSURANCE")

        st.header("Make the evidence work harder.")

        st.write(
            "Capture the claim. Understand the risk. "
            "Move forward with confidence."
        )

        st.write("")

        if st.button(
            "Start Claim Assessment →",
            key="overview_assessment"
        ):
            st.session_state.page = "Claim Assessment"
            st.rerun()

    with hero_right:

        st.metric(
            "AI MODEL",
            "V4"
        )

        st.metric(
            "MODEL TYPE",
            "Random Forest"
        )

    st.divider()

    st.subheader("Platform")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 🔍 Claim Assessment")

        st.write(
            "Evaluate claim indicators using the "
            "Version 4 Random Forest model."
        )

        if st.button(
            "Open Assessment →",
            key="overview_claim"
        ):
            st.session_state.page = "Claim Assessment"
            st.rerun()

    with col2:

        st.markdown("### 📄 Documents")

        st.write(
            "Organise supporting documents and "
            "forensic evidence for future review."
        )

        if st.button(
            "Open Documents →",
            key="overview_documents"
        ):
            st.session_state.page = "Documents"
            st.rerun()

    with col3:

        st.markdown("### 📊 Claim Status")

        st.write(
            "Review the most recent assessment "
            "generated during this session."
        )

        if st.button(
            "View Status →",
            key="overview_status"
        ):
            st.session_state.page = "Claim Status"
            st.rerun()

    st.divider()

    st.subheader("How Insurix Works")

    step1, step2, step3 = st.columns(3)

    with step1:

        st.markdown("### 01")

        st.markdown("**Capture**")

        st.write(
            "Enter the available claim indicators."
        )

    with step2:

        st.markdown("### 02")

        st.markdown("**Analyse**")

        st.write(
            "The Version 4 Random Forest model "
            "evaluates the claim."
        )

    with step3:

        st.markdown("### 03")

        st.markdown("**Assess**")

        st.write(
            "Receive a preliminary Low, Medium "
            "or High risk classification."
        )

    st.divider()

    st.caption(
        "INSURIX • AI-Powered Forensic Insurance Risk Assessment • Version 4"
    )


# ============================================================
# CLAIM ASSESSMENT PAGE
# ============================================================

elif st.session_state.page == "Claim Assessment":

    st.caption("PUBLIC PORTAL / CLAIM ASSESSMENT")

    st.title("Claim Assessment")

    st.write(
        "Build a consistent evidence record before review."
    )

    st.divider()

    # --------------------------------------------------------
    # CLAIM IDENTITY
    # --------------------------------------------------------

    st.subheader("01  •  Claim identity")

    identity_col1, identity_col2 = st.columns(2)

    with identity_col1:

        policyholder_name = st.text_input(
            "Policyholder name",
            placeholder="Enter policyholder name"
        )

        incident_location = st.text_input(
            "Incident location",
            placeholder="City / District"
        )

        incident_date = st.date_input(
            "Incident date"
        )

        incident_description = st.text_area(
            "Incident description",
            placeholder="Briefly describe the incident"
        )

    with identity_col2:

        claim_id = st.text_input(
            "Claim ID",
            placeholder="Enter claim ID"
        )

        estimated_amount = st.number_input(
            "Estimated claim amount (₹)",
            min_value=0.0,
            value=250000.0,
            step=10000.0
        )

        previous_claims = st.number_input(
            "Previous claims",
            min_value=0,
            value=2,
            step=1
        )

    st.divider()

    # --------------------------------------------------------
    # EVIDENCE AVAILABILITY
    # --------------------------------------------------------

    st.subheader("02  •  Evidence availability")

    evidence_col1, evidence_col2 = st.columns(2)

    with evidence_col1:

        cctv_available = st.selectbox(
            "CCTV available",
            ["No", "Yes"]
        )

        police_report = st.selectbox(
            "Police report",
            ["No", "Yes"]
        )

        vehicle_inspection = st.selectbox(
            "Vehicle inspection",
            ["No", "Yes"]
        )

        rejected_claims = st.number_input(
            "Rejected claims",
            min_value=0,
            value=0,
            step=1
        )

    with evidence_col2:

        photos_available = st.selectbox(
            "Photos available",
            ["No", "Yes"]
        )

        witness_available = st.selectbox(
            "Witness available",
            ["No", "Yes"]
        )

        claim_frequency = st.number_input(
            "Claim frequency",
            min_value=0,
            value=1,
            step=1
        )

        document_consistency_text = st.selectbox(
            "Document consistency",
            ["Yes", "No"]
        )

    st.divider()

    # --------------------------------------------------------
    # ADDITIONAL MODEL INDICATORS
    # --------------------------------------------------------

    st.subheader("03  •  Forensic risk indicators")

    model_col1, model_col2 = st.columns(2)

    with model_col1:

        evidence_status_text = st.selectbox(
            "Evidence status",
            ["Yes", "No"]
        )

    with model_col2:

        claim_after_policy_text = st.selectbox(
            "Claim after policy",
            ["No", "Yes"]
        )

    st.info(
        "The Version 4 Random Forest model evaluates seven "
        "claim-related features."
    )

    st.write("")

    # --------------------------------------------------------
    # RUN ASSESSMENT
    # --------------------------------------------------------

    run_assessment = st.button(
        "Run Assessment  →",
        key="run_assessment",
        use_container_width=False
    )

    if run_assessment:

        # Convert Yes / No to 1 / 0
        evidence_status = 1 if evidence_status_text == "Yes" else 0

        document_consistency = (
            1 if document_consistency_text == "Yes" else 0
        )

        claim_after_policy = (
            1 if claim_after_policy_text == "Yes" else 0
        )

        # ----------------------------------------------------
        # CREATE MODEL INPUT IN EXACT V4 FEATURE ORDER
        # ----------------------------------------------------

        input_data = {
            "claim_amount": estimated_amount,
            "previous_claims": previous_claims,
            "rejected_claims": rejected_claims,
            "claim_frequency": claim_frequency,
            "evidence_status": evidence_status,
            "document_consistency": document_consistency,
            "claim_after_policy": claim_after_policy
        }

        input_df = pd.DataFrame(
            [input_data],
            columns=features
        )

        try:

            # ------------------------------------------------
            # VERSION 4 RANDOM FOREST PREDICTION
            # ------------------------------------------------

            prediction = model.predict(input_df)

            prediction_label = label_encoder.inverse_transform(
                prediction
            )[0]

            probabilities = model.predict_proba(
                input_df
            )[0]

            class_names = label_encoder.classes_

            probability_dict = {}

            for class_name, probability in zip(
                class_names,
                probabilities
            ):
                probability_dict[class_name] = (
                    float(probability) * 100
                )

            confidence = max(probability_dict.values())

            # Save result
            st.session_state.last_risk = str(
                prediction_label
            )

            st.session_state.last_confidence = float(
                confidence
            )

            st.session_state.last_probabilities = (
                probability_dict
            )

            st.session_state.assessment_done = True

        except Exception as e:

            st.error(
                "The assessment could not be completed."
            )

            st.code(str(e))

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    if st.session_state.assessment_done:

        st.divider()

        st.subheader("Assessment Result")

        risk = st.session_state.last_risk
        confidence = st.session_state.last_confidence

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:

            st.metric(
                "Risk Level",
                risk
            )

        with result_col2:

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

        with result_col3:

            st.metric(
                "Model",
                "V4 Random Forest"
            )

        # Risk message
        risk_lower = risk.lower()

        if risk_lower == "high":

            st.error(
                "High-risk classification. "
                "Further forensic or investigative review "
                "may be appropriate."
            )

        elif risk_lower == "medium":

            st.warning(
                "Medium-risk classification. "
                "Additional verification may be considered."
            )

        else:

            st.success(
                "Low-risk classification based on the "
                "entered indicators."
            )

        st.divider()

        # ----------------------------------------------------
        # PROBABILITY BREAKDOWN
        # ----------------------------------------------------

        st.subheader("Risk Probability Breakdown")

        probabilities = (
            st.session_state.last_probabilities
        )

        probability_cols = st.columns(
            len(probabilities)
        )

        for column, (class_name, probability) in zip(
            probability_cols,
            probabilities.items()
        ):

            with column:

                st.metric(
                    class_name.title(),
                    f"{probability:.2f}%"
                )

                st.progress(
                    min(
                        max(probability / 100, 0.0),
                        1.0
                    )
                )

        st.divider()

        # ----------------------------------------------------
        # FEATURE IMPORTANCE
        # ----------------------------------------------------

        st.subheader("Model Feature Importance")

        try:

            importance_df = pd.DataFrame(
                {
                    "Feature": features,
                    "Importance": model.feature_importances_
                }
            )

            importance_df = importance_df.sort_values(
                "Importance",
                ascending=False
            )

            importance_df["Importance (%)"] = (
                importance_df["Importance"] * 100
            ).round(2)

            st.dataframe(
                importance_df[
                    ["Feature", "Importance (%)"]
                ],
                use_container_width=True,
                hide_index=True
            )

        except Exception:

            st.info(
                "Feature importance is not available "
                "for this model."
            )

        st.divider()

        st.info(
            "Forensic interpretation: this output is a "
            "preliminary AI-assisted risk assessment. "
            "It should support, not replace, professional "
            "claim investigation and evidence review."
        )


# ============================================================
# DOCUMENTS PAGE
# ============================================================

elif st.session_state.page == "Documents":

    st.caption("PUBLIC PORTAL / DOCUMENTS")

    st.title("Documents")

    st.write(
        "Supporting documents can be linked to each "
        "claim assessment."
    )

    st.divider()

    doc_col1, doc_col2 = st.columns(2)

    with doc_col1:

        st.subheader("01  •  Claim Documentation")

        st.write(
            "Upload documents associated with the insurance claim."
        )

        uploaded_files = st.file_uploader(
            "Upload documents",
            accept_multiple_files=True,
            type=[
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "docx",
                "xlsx",
                "csv"
            ]
        )

    with doc_col2:

        st.subheader("02  •  Forensic Evidence")

        st.write(
            "Evidence files can be organised for future "
            "forensic analysis and review."
        )

        st.info(
            "Future versions can integrate OCR, metadata "
            "analysis, consistency checking and automated "
            "evidence extraction."
        )

    if uploaded_files:

        st.divider()

        st.subheader("Uploaded Documents")

        for file in uploaded_files:

            st.write(
                f"📄 {file.name}  •  "
                f"{file.size / 1024:.1f} KB"
            )

        st.success(
            f"{len(uploaded_files)} document(s) selected."
        )

    st.divider()

    st.subheader("Planned Evidence Workflow")

    workflow1, workflow2, workflow3 = st.columns(3)

    with workflow1:

        st.markdown("### 01")

        st.markdown("**Upload**")

        st.write(
            "Collect claim-related supporting files."
        )

    with workflow2:

        st.markdown("### 02")

        st.markdown("**Review**")

        st.write(
            "Review documents for consistency and "
            "available forensic evidence."
        )

    with workflow3:

        st.markdown("### 03")

        st.markdown("**Analyse**")

        st.write(
            "Future AI modules can assist with "
            "document and evidence analysis."
        )


# ============================================================
# CLAIM STATUS PAGE
# ============================================================

elif st.session_state.page == "Claim Status":

    st.caption("PUBLIC PORTAL / CLAIM STATUS")

    st.title("Claim Status")

    st.write(
        "Review the latest preliminary risk assessment "
        "generated in this session."
    )

    st.divider()

    if not st.session_state.assessment_done:

        st.info(
            "No claim assessment has been completed yet."
        )

        if st.button(
            "Go to Claim Assessment →",
            key="status_assessment"
        ):

            st.session_state.page = "Claim Assessment"
            st.rerun()

    else:

        status_col1, status_col2, status_col3 = st.columns(3)

        with status_col1:

            st.metric(
                "Risk Level",
                st.session_state.last_risk
            )

        with status_col2:

            st.metric(
                "Confidence",
                f"{st.session_state.last_confidence:.2f}%"
            )

        with status_col3:

            st.metric(
                "Status",
                "Assessed"
            )

        st.divider()

        risk = st.session_state.last_risk.lower()

        if risk == "high":

            st.error(
                "Current classification: HIGH RISK"
            )

        elif risk == "medium":

            st.warning(
                "Current classification: MEDIUM RISK"
            )

        else:

            st.success(
                "Current classification: LOW RISK"
            )

        st.subheader("Risk Probability")

        probabilities = (
            st.session_state.last_probabilities
        )

        for class_name, probability in probabilities.items():

            st.write(
                f"**{class_name.title()}** — "
                f"{probability:.2f}%"
            )

            st.progress(
                min(
                    max(probability / 100, 0.0),
                    1.0
                )
            )

        st.divider()

        st.info(
            "This status represents the latest preliminary "
            "AI-assisted assessment in the current session."
        )

        if st.button(
            "Run New Assessment →",
            key="new_assessment"
        ):

            st.session_state.page = "Claim Assessment"
            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "INSURIX • AI-Powered Forensic Insurance Risk Assessment "
    "• Version 4 • Random Forest Classification"
)
