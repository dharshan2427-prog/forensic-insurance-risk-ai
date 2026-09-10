import streamlit as st
import joblib
import pandas as pd
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Insurix | Insurance Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ---------- MAIN PAGE ---------- */

    .stApp {
        background: #f6f8fc;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07152f 0%, #0b1d3d 100%);
        min-width: 260px;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    section[data-testid="stSidebar"] * {
        color: #e8f0ff;
    }

    .brand {
        padding: 10px 10px 25px 10px;
    }

    .brand-title {
        font-size: 30px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
    }

    .brand-title span {
        color: #4da3ff;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #9fb4d4;
        line-height: 1.5;
        margin-top: 6px;
    }

    .sidebar-status {
        position: fixed;
        bottom: 25px;
        left: 25px;
        font-size: 12px;
        color: #b8c8df;
    }

    .status-dot {
        color: #42e89b;
        font-size: 18px;
        vertical-align: middle;
    }

    /* ---------- HEADER ---------- */

    .breadcrumb {
        color: #1769e0;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }

    .page-title {
        font-size: 52px;
        line-height: 1.05;
        font-weight: 800;
        color: #0b1730;
        letter-spacing: -2px;
        margin: 0;
    }

    .page-subtitle {
        font-size: 19px;
        color: #7183a5;
        margin-top: 10px;
        margin-bottom: 25px;
    }

    /* ---------- HERO ---------- */

    .hero {
        background:
            radial-gradient(
                circle at 80% 40%,
                rgba(44, 100, 255, 0.35),
                transparent 30%
            ),
            linear-gradient(
                110deg,
                #07152f,
                #10285d 65%,
                #123b89
            );
        border-radius: 18px;
        padding: 45px;
        min-height: 250px;
        color: white;
        margin: 15px 0 30px 0;
        box-shadow: 0 12px 35px rgba(13, 37, 85, 0.15);
    }

    .hero-label {
        color: #4db7ff;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2px;
    }

    .hero-title {
        font-size: 43px;
        font-weight: 800;
        line-height: 1.05;
        margin: 18px 0 10px 0;
    }

    .hero-title span {
        color: #55b8ff;
    }

    .hero-text {
        color: #d4def1;
        font-size: 16px;
    }

    /* ---------- CARDS ---------- */

    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 27px;
        min-height: 190px;
        border: 1px solid #e7ecf5;
        box-shadow: 0 8px 25px rgba(22, 43, 78, 0.06);
    }

    .card-icon {
        font-size: 27px;
        margin-bottom: 15px;
    }

    .card-number {
        float: right;
        color: #8ea0bf;
        font-size: 13px;
        font-weight: 700;
    }

    .card-title {
        font-size: 20px;
        font-weight: 750;
        color: #0c1932;
        margin-bottom: 8px;
    }

    .card-text {
        color: #7b8da9;
        font-size: 14px;
        line-height: 1.6;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        color: #0b1730;
        font-size: 28px;
        font-weight: 800;
        margin-top: 15px;
    }

    .section-subtitle {
        color: #7b8da9;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* ---------- ASSESSMENT PANEL ---------- */

    .assessment-panel {
        background: white;
        border: 1px solid #e5eaf3;
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 8px 28px rgba(22, 43, 78, 0.06);
    }

    /* ---------- RISK RESULT ---------- */

    .risk-card {
        border-radius: 18px;
        padding: 30px;
        background: white;
        border: 1px solid #e3e8f2;
        box-shadow: 0 10px 30px rgba(22, 43, 78, 0.08);
        margin-top: 20px;
    }

    .risk-label {
        color: #7c8da9;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .risk-value {
        font-size: 42px;
        font-weight: 850;
        margin-top: 8px;
    }

    .confidence-value {
        font-size: 30px;
        font-weight: 800;
        color: #1769e0;
    }

    /* ---------- INFO BOX ---------- */

    .info-box {
        background: #eef5ff;
        border-left: 4px solid #1769e0;
        border-radius: 8px;
        padding: 15px 18px;
        color: #3d5375;
        font-size: 14px;
        margin: 15px 0;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #8998b0;
        font-size: 12px;
        padding-top: 30px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD VERSION 4 MODEL
# ============================================================

MODEL_FILE = "insurance_risk_model_v4.pkl"


@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            f"{MODEL_FILE} was not found in the application folder."
        )

    data = joblib.load(MODEL_FILE)

    if not isinstance(data, dict):
        raise TypeError(
            "The V4 model file does not contain the expected dictionary."
        )

    required_keys = [
        "model",
        "label_encoder",
        "features"
    ]

    for key in required_keys:

        if key not in data:
            raise KeyError(
                f"Required key '{key}' is missing from the V4 model."
            )

    model = data["model"]
    label_encoder = data["label_encoder"]
    features = data["features"]

    return model, label_encoder, features


# ============================================================
# MODEL INITIALIZATION
# ============================================================

try:

    model, label_encoder, features = load_model()

except Exception as e:

    st.error("Unable to load the trained ML model.")
    st.error(str(e))
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">

        <div class="brand-title">
            🛡️ Insur<span>ix</span>
        </div>

        <div class="brand-subtitle">
            AI-Powered Forensic<br>
            Insurance Risk Assessment
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Overview",
            "🔍 Claim Assessment",
            "📄 Documents",
            "📊 Claim Status"
        ],
        label_visibility="collapsed"
    )

    st.markdown(
        """
        <div class="sidebar-status">
            <span class="status-dot">●</span>
            &nbsp; System operational
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        '<div class="breadcrumb">INSURIX / 01</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-title">Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'A clear starting point for every insurance claim.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="hero">

        <div class="hero-label">
            INSURIX × INSURANCE
        </div>

        <div class="hero-title">
            Make the evidence<br>
            <span>work harder.</span>
        </div>

        <div class="hero-text">
            Capture the claim. Understand the risk.
            Move forward with confidence.
        </div>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="feature-card">

            <div class="card-number">01 →</div>

            <div class="card-icon">🔍</div>

            <div class="card-title">
                Claim Assessment
            </div>

            <div class="card-text">
                Turn claim information into a transparent
                preliminary risk assessment using machine learning.
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card">

            <div class="card-number">02 →</div>

            <div class="card-icon">📄</div>

            <div class="card-title">
                Documents
            </div>

            <div class="card-text">
                Organize supporting documents and keep
                evidence requirements visible during review.
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="feature-card">

            <div class="card-number">03 →</div>

            <div class="card-icon">📊</div>

            <div class="card-title">
                Claim Status
            </div>

            <div class="card-text">
                Review assessment status and identify
                claims that may require additional verification.
            </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">

        <b>AI-assisted assessment:</b>
        Insurix provides a preliminary risk classification.
        It does not independently determine fraud or automatically
        reject claims.

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CLAIM ASSESSMENT PAGE
# ============================================================

elif page == "🔍 Claim Assessment":

    st.markdown(
        '<div class="breadcrumb">INSURIX / 02</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-title">Claim Assessment</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Evaluate claim characteristics using the Version 4 '
        'machine-learning model.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="assessment-panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Claim Information</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Enter the available claim information below.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        claim_amount = st.number_input(
            "Claim Amount (₹)",
            min_value=0.0,
            value=50000.0,
            step=1000.0
        )

        previous_claims = st.number_input(
            "Previous Claims",
            min_value=0,
            value=0,
            step=1
        )

        rejected_claims = st.number_input(
            "Rejected Claims",
            min_value=0,
            value=0,
            step=1
        )

        claim_frequency = st.number_input(
            "Claim Frequency",
            min_value=0.0,
            value=1.0,
            step=1.0
        )

    with col2:

        evidence_status = st.selectbox(
            "Evidence Status",
            ["Yes", "No"]
        )

        document_consistency = st.selectbox(
            "Document Consistency",
            ["Yes", "No"]
        )

        claim_after_policy = st.selectbox(
            "Claim After Policy",
            ["No", "Yes"]
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.caption(
            "The selected information is processed by the trained "
            "Random Forest model."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # CONVERT YES / NO TO NUMERIC
    # ========================================================

    evidence_status_value = (
        1 if evidence_status == "Yes" else 0
    )

    document_consistency_value = (
        1 if document_consistency == "Yes" else 0
    )

    claim_after_policy_value = (
        1 if claim_after_policy == "Yes" else 0
    )

    # ========================================================
    # INPUT VALUES
    # ========================================================

    input_values = {

        "claim_amount": claim_amount,

        "previous_claims": previous_claims,

        "rejected_claims": rejected_claims,

        "claim_frequency": claim_frequency,

        "evidence_status": evidence_status_value,

        "document_consistency": document_consistency_value,

        "claim_after_policy": claim_after_policy_value
    }

    # ========================================================
    # PREPARE DATA
    # ========================================================

    try:

        input_data = pd.DataFrame(
            [
                [
                    input_values[feature]
                    for feature in features
                ]
            ],
            columns=features
        )

    except KeyError as e:

        st.error(f"Feature mismatch: {e}")

        st.write(
            "Features stored in model:",
            features
        )

        st.stop()

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================
    # PREDICTION BUTTON
    # ========================================================

    if st.button(
        "🔎  Assess Insurance Risk",
        type="primary",
        use_container_width=True
    ):

        try:

            # =================================================
            # MAKE PREDICTION
            # =================================================

            prediction = model.predict(
                input_data
            )

            risk_level = (
                label_encoder
                .inverse_transform(prediction)[0]
            )

            # =================================================
            # PROBABILITY
            # =================================================

            probabilities = None
            probability = 0.0
            classes = None

            if hasattr(
                model,
                "predict_proba"
            ):

                probabilities = (
                    model.predict_proba(
                        input_data
                    )[0]
                )

                classes = model.classes_

                predicted_class = prediction[0]

                for i, class_value in enumerate(classes):

                    if class_value == predicted_class:

                        probability = (
                            probabilities[i] * 100
                        )

                        break

            # =================================================
            # SAVE RESULT
            # =================================================

            st.session_state["last_risk"] = (
                str(risk_level).upper()
            )

            st.session_state["last_confidence"] = (
                probability
            )

            # =================================================
            # RISK INTERPRETATION
            # =================================================

            risk_text = str(
                risk_level
            ).lower()

            if "high" in risk_text:

                risk_display = "HIGH"

                risk_message = (
                    "Higher-risk characteristics detected. "
                    "Further investigation and verification "
                    "may be recommended."
                )

            elif "medium" in risk_text:

                risk_display = "MEDIUM"

                risk_message = (
                    "Moderate-risk characteristics detected. "
                    "Additional verification may be appropriate."
                )

            elif "low" in risk_text:

                risk_display = "LOW"

                risk_message = (
                    "The claim shows characteristics associated "
                    "with a lower insurance risk level."
                )

            else:

                risk_display = (
                    str(risk_level).upper()
                )

                risk_message = (
                    "Risk category generated by the trained model."
                )

            # =================================================
            # RESULT HEADER
            # =================================================

            st.markdown(
                '<div class="section-title">'
                'Assessment Result'
                '</div>',
                unsafe_allow_html=True
            )

            result_col1, result_col2 = st.columns(2)

            # =================================================
            # RISK LEVEL CARD
            # =================================================

            with result_col1:

                st.markdown(
                    f"""
                    <div class="risk-card">

                        <div class="risk-label">
                            Predicted Risk Level
                        </div>

                        <div class="risk-value">
                            {risk_display}
                        </div>

                        <p style="color:#7183a5;">
                            {risk_message}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # =================================================
            # CONFIDENCE CARD
            # =================================================

            with result_col2:

                st.markdown(
                    f"""
                    <div class="risk-card">

                        <div class="risk-label">
                            Prediction Confidence
                        </div>

                        <div class="confidence-value">
                            {probability:.2f}%
                        </div>

                        <p style="color:#7183a5;">
                            Model probability for the predicted
                            risk category.
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # =================================================
            # PROBABILITY BREAKDOWN
            # =================================================

            if probabilities is not None:

                st.markdown(
                    '<div class="section-title">'
                    'Risk Probability'
                    '</div>',
                    unsafe_allow_html=True
                )

                probability_data = []

                for i, class_value in enumerate(classes):

                    decoded_class = (
                        label_encoder
                        .inverse_transform(
                            [class_value]
                        )[0]
                    )

                    probability_data.append(
                        {
                            "Risk Category":
                                str(
                                    decoded_class
                                ).upper(),

                            "Probability (%)":
                                round(
                                    probabilities[i] * 100,
                                    2
                                )
                        }
                    )

                probability_df = pd.DataFrame(
                    probability_data
                )

                st.dataframe(
                    probability_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.bar_chart(
                    probability_df.set_index(
                        "Risk Category"
                    )
                )

            # =================================================
            # FEATURE IMPORTANCE
            # =================================================

            if hasattr(
                model,
                "feature_importances_"
            ):

                st.markdown(
                    '<div class="section-title">'
                    'Model Feature Importance'
                    '</div>',
                    unsafe_allow_html=True
                )

                importance_df = pd.DataFrame(
                    {
                        "Feature":
                            features,

                        "Importance":
                            model.feature_importances_
                    }
                )

                importance_df = (
                    importance_df
                    .sort_values(
                        by="Importance",
                        ascending=False
                    )
                )

                importance_df["Importance"] = (
                    importance_df["Importance"]
                    .round(4)
                )

                st.dataframe(
                    importance_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.bar_chart(
                    importance_df.set_index(
                        "Feature"
                    )
                )

            # =================================================
            # FORENSIC INTERPRETATION
            # =================================================

            st.markdown("""
            <div class="info-box">

                <b>Forensic interpretation:</b>
                This result is an AI-assisted preliminary risk
                assessment. A high-risk classification should be
                treated as a signal for additional verification,
                not as proof of fraud.

            </div>
            """, unsafe_allow_html=True)

        except Exception as e:

            st.error("Prediction failed.")
            st.exception(e)


# ============================================================
# DOCUMENTS PAGE
# ============================================================

elif page == "📄 Documents":

    st.markdown(
        '<div class="breadcrumb">INSURIX / 03</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-title">Documents</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Supporting evidence and document review workspace.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="feature-card">

            <div class="card-icon">📁</div>

            <div class="card-title">
                Evidence Workspace
            </div>

            <div class="card-text">
                Organize claim-related documents and supporting
                evidence for further review.
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card">

            <div class="card-icon">🔎</div>

            <div class="card-title">
                Evidence Verification
            </div>

            <div class="card-text">
                Review document consistency and identify
                information that may require additional verification.
            </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        "Document upload and automated forensic document analysis "
        "are planned as future extensions of the prototype."
    )


# ============================================================
# CLAIM STATUS PAGE
# ============================================================

elif page == "📊 Claim Status":

    st.markdown(
        '<div class="breadcrumb">INSURIX / 04</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-title">Claim Status</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Review the latest assessment generated during this session.'
        '</div>',
        unsafe_allow_html=True
    )

    if "last_risk" in st.session_state:

        risk = st.session_state["last_risk"]

        confidence = st.session_state.get(
            "last_confidence",
            0.0
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Assessment Status",
                "Completed"
            )

        with col2:

            st.metric(
                "Risk Level",
                risk
            )

        with col3:

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">

            <b>Next step:</b>
            Use the risk classification as a preliminary
            decision-support indicator. Claims requiring
            additional attention should undergo appropriate
            verification and human review.

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="feature-card">

            <div class="card-icon">📊</div>

            <div class="card-title">
                No assessment yet
            </div>

            <div class="card-text">
                Complete a claim assessment first.
                The latest result will appear here.
            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        INSURIX • AI-Powered Forensic Insurance Risk Assessment
        • Version 4 • Random Forest Classification
    </div>
    """,
    unsafe_allow_html=True
)
