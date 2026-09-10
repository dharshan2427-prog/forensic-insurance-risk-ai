import streamlit as st
import joblib
import pandas as pd
import os
import textwrap


# ============================================================
# INSURIX
# AI-POWERED FORENSIC INSURANCE RISK ASSESSMENT
# VERSION 4
# ============================================================


# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Insurix | Insurance Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------
# HELPER FOR HTML RENDERING
# ------------------------------------------------------------

def render_html(content):
    """
    Removes unwanted indentation from HTML before sending it
    to Streamlit. This prevents HTML from being displayed
    as plain text/code.
    """
    st.markdown(
        textwrap.dedent(content),
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown(
    textwrap.dedent("""
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #f6f8fc;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Remove excessive Streamlit spacing */
    div[data-testid="stVerticalBlock"] {
        gap: 0.6rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #07152f 0%,
            #0b1d3d 100%
        );
        min-width: 280px;
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

    .sidebar-divider {
        height: 1px;
        background: rgba(255,255,255,0.12);
        margin: 10px 0 20px 0;
    }

    .sidebar-section-title {
        font-size: 10px;
        font-weight: 700;
        color: #7187a8;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 15px 10px 8px 10px;
    }

    .sidebar-status {
        position: fixed;
        bottom: 25px;
        left: 25px;
        font-size: 12px;
        color: #8da4c7;
    }


    /* ========================================================
       RADIO NAVIGATION
       ======================================================== */

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 5px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: transparent;
        border-radius: 8px;
        padding: 8px 10px;
        transition: 0.2s;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(77,163,255,0.12);
    }


    /* ========================================================
       BREADCRUMB
       ======================================================== */

    .breadcrumb {
        color: #7b8aa3;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }


    /* ========================================================
       PAGE TITLE
       ======================================================== */

    .page-title {
        font-size: 34px;
        font-weight: 800;
        color: #0a1833;
        letter-spacing: -1px;
        margin-bottom: 20px;
    }

    .page-description {
        color: #687892;
        font-size: 14px;
        margin-top: -10px;
        margin-bottom: 25px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        background:
            linear-gradient(
                135deg,
                #07152f 0%,
                #10366b 55%,
                #1769a8 100%
            );
        border-radius: 18px;
        padding: 42px 45px;
        min-height: 265px;
        position: relative;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(7,21,47,0.14);
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 50%;
        right: -60px;
        top: -80px;
    }

    .hero-label {
        color: #76b8ff;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 42px;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -1.5px;
    }

    .hero-title span {
        color: #62b0ff;
    }

    .hero-text {
        color: #c9dbf5;
        font-size: 14px;
        margin-top: 18px;
        max-width: 600px;
        line-height: 1.6;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    .card {
        background: #ffffff;
        border: 1px solid #e3e9f2;
        border-radius: 14px;
        padding: 22px;
        min-height: 155px;
        box-shadow: 0 5px 18px rgba(21,43,77,0.05);
        margin-bottom: 10px;
    }

    .card-number {
        color: #8b9ab0;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }

    .card-icon {
        font-size: 25px;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .card-title {
        color: #0c1c38;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .card-text {
        color: #718096;
        font-size: 12px;
        line-height: 1.5;
    }


    /* ========================================================
       INFO BOX
       ======================================================== */

    .info-box {
        background: #eef7ff;
        border-left: 4px solid #1769a8;
        border-radius: 8px;
        padding: 15px 18px;
        color: #3d5375;
        font-size: 13px;
        line-height: 1.6;
        margin: 15px 0;
    }


    /* ========================================================
       ASSESSMENT HEADER
       ======================================================== */

    .assessment-header {
        background: #ffffff;
        border: 1px solid #e3e9f2;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
    }

    .assessment-header-title {
        color: #0b1c38;
        font-size: 19px;
        font-weight: 800;
    }

    .assessment-header-text {
        color: #718096;
        font-size: 13px;
        margin-top: 5px;
    }


    /* ========================================================
       RESULT CARDS
       ======================================================== */

    .result-card {
        background: #ffffff;
        border: 1px solid #e1e7f0;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        min-height: 145px;
        box-shadow: 0 5px 18px rgba(21,43,77,0.05);
    }

    .result-label {
        color: #8391a7;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .result-value {
        color: #0b1c38;
        font-size: 28px;
        font-weight: 800;
        margin-top: 12px;
    }

    .risk-low {
        color: #18865b;
    }

    .risk-medium {
        color: #c48616;
    }

    .risk-high {
        color: #c53d4b;
    }


    /* ========================================================
       SECTION HEADINGS
       ======================================================== */

    .section-heading {
        color: #0b1c38;
        font-size: 18px;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 12px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #8998b0;
        font-size: 11px;
        padding-top: 30px;
        padding-bottom: 15px;
        letter-spacing: 0.3px;
    }


    /* ========================================================
       STREAMLIT BUTTON
       ======================================================== */

    .stButton > button {
        background: #0d5ea8;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 700;
        width: 100%;
        min-height: 45px;
    }

    .stButton > button:hover {
        background: #084b89;
        color: white;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-baseweb="input"] {
        border-radius: 7px;
    }

    div[data-baseweb="select"] {
        border-radius: 7px;
    }

    </style>
    """),
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# LOAD VERSION 4 MODEL
# ------------------------------------------------------------

MODEL_FILE = "insurance_risk_model_v4.pkl"

if not os.path.exists(MODEL_FILE):
    st.error(
        "Version 4 model file was not found. "
        "Please make sure insurance_risk_model_v4.pkl "
        "is present in the repository."
    )
    st.stop()


try:
    model_package = joblib.load(MODEL_FILE)

    model = model_package["model"]
    label_encoder = model_package["label_encoder"]
    features = model_package["features"]

except Exception as e:
    st.error(f"Unable to load the Version 4 model: {e}")
    st.stop()


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

if "last_risk" not in st.session_state:
    st.session_state.last_risk = None

if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = None

if "last_probabilities" not in st.session_state:
    st.session_state.last_probabilities = None


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:

    render_html("""
    <div class="brand">
        <div class="brand-title">
            🛡️ Insur<span>ix</span>
        </div>

        <div class="brand-subtitle">
            AI-Powered Forensic<br>
            Insurance Risk Assessment
        </div>
    </div>

    <div class="sidebar-divider"></div>

    <div class="sidebar-section-title">
        Navigation
    </div>
    """)

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

    render_html("""
    <div class="sidebar-status">
        ● System operational<br>
        <span style="font-size:10px;">
        Version 4 • Random Forest
        </span>
    </div>
    """)


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    render_html("""
    <div class="breadcrumb">
        INSURIX / 01
    </div>

    <div class="page-title">
        Overview
    </div>

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
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        render_html("""
        <div class="card">
            <div class="card-number">01</div>
            <div class="card-icon">🔍</div>
            <div class="card-title">
                Claim Assessment
            </div>
            <div class="card-text">
                Analyse claim indicators and obtain
                an AI-assisted preliminary risk classification.
            </div>
        </div>
        """)

    with col2:
        render_html("""
        <div class="card">
            <div class="card-number">02</div>
            <div class="card-icon">📄</div>
            <div class="card-title">
                Documents
            </div>
            <div class="card-text">
                Review documentation and evidence
                consistency indicators associated with a claim.
            </div>
        </div>
        """)

    with col3:
        render_html("""
        <div class="card">
            <div class="card-number">03</div>
            <div class="card-icon">📊</div>
            <div class="card-title">
                Claim Status
            </div>
            <div class="card-text">
                View the latest assessment result
                generated during the current session.
            </div>
        </div>
        """)

    render_html("""
    <div class="info-box">
        <strong>AI-assisted assessment:</strong>
        Insurix uses a Version 4 Random Forest classification
        model to provide a preliminary Low, Medium, or High
        risk indication from selected claim characteristics.
        The output is intended to support investigation and
        triage, not replace professional claim decisions.
    </div>
    """)


# ============================================================
# CLAIM ASSESSMENT
# ============================================================

elif page == "🔍 Claim Assessment":

    render_html("""
    <div class="breadcrumb">
        INSURIX / 02
    </div>

    <div class="page-title">
        Claim Assessment
    </div>

    <div class="page-description">
        Enter the available claim indicators to generate a
        preliminary forensic insurance risk assessment.
    </div>

    <div class="assessment-header">
        <div class="assessment-header-title">
            Claim Intelligence Input
        </div>

        <div class="assessment-header-text">
            The Version 4 Random Forest model evaluates seven
            claim-related features.
        </div>
    </div>
    """)

    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        claim_amount = st.number_input(
            "Claim Amount",
            min_value=0.0,
            max_value=10000000.0,
            value=250000.0,
            step=10000.0,
            help="Enter the claimed amount."
        )

        previous_claims = st.number_input(
            "Previous Claims",
            min_value=0,
            max_value=100,
            value=2,
            step=1,
            help="Number of previous insurance claims."
        )

        rejected_claims = st.number_input(
            "Rejected Claims",
            min_value=0,
            max_value=100,
            value=0,
            step=1,
            help="Number of previously rejected claims."
        )

        claim_frequency = st.number_input(
            "Claim Frequency",
            min_value=0.0,
            max_value=100.0,
            value=1.0,
            step=1.0,
            help="Claim frequency indicator used by the model."
        )

    with col2:

        evidence_status = st.selectbox(
            "Evidence Status",
            ["Yes", "No"],
            help="Whether supporting evidence is available."
        )

        document_consistency = st.selectbox(
            "Document Consistency",
            ["Yes", "No"],
            help="Whether the submitted documentation is consistent."
        )

        claim_after_policy = st.selectbox(
            "Claim After Policy",
            ["Yes", "No"],
            help="Whether the claim occurred after policy activation."
        )

    render_html("""
    <div class="info-box">
        <strong>Model features:</strong>
        Claim Amount • Previous Claims • Rejected Claims •
        Claim Frequency • Evidence Status • Document Consistency •
        Claim After Policy
    </div>
    """)

    assess_button = st.button(
        "🔍 Assess Claim Risk"
    )

    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    if assess_button:

        evidence_value = 1 if evidence_status == "Yes" else 0
        document_value = 1 if document_consistency == "Yes" else 0
        after_policy_value = 1 if claim_after_policy == "Yes" else 0

        input_data = {
            "claim_amount": claim_amount,
            "previous_claims": previous_claims,
            "rejected_claims": rejected_claims,
            "claim_frequency": claim_frequency,
            "evidence_status": evidence_value,
            "document_consistency": document_value,
            "claim_after_policy": after_policy_value
        }

        try:

            # Keep EXACT Version 4 feature order
            input_df = pd.DataFrame(
                [[input_data[feature] for feature in features]],
                columns=features
            )

            # Prediction
            prediction = model.predict(input_df)[0]

            # Convert encoded prediction back to risk name
            risk_level = label_encoder.inverse_transform(
                [prediction]
            )[0]

            # Probability
            probabilities = model.predict_proba(input_df)[0]

            confidence = max(probabilities) * 100

            # Save result
            st.session_state.last_risk = risk_level
            st.session_state.last_confidence = confidence
            st.session_state.last_probabilities = probabilities

            # ------------------------------------------------
            # RISK CLASS
            # ------------------------------------------------

            risk_lower = str(risk_level).lower()

            if risk_lower == "low":
                risk_class = "risk-low"
            elif risk_lower == "medium":
                risk_class = "risk-medium"
            else:
                risk_class = "risk-high"

            # ------------------------------------------------
            # RESULT DISPLAY
            # ------------------------------------------------

            render_html("""
            <div class="section-heading">
                Assessment Result
            </div>
            """)

            r1, r2, r3 = st.columns(3)

            with r1:
                render_html(f"""
                <div class="result-card">
                    <div class="result-label">
                        Risk Level
                    </div>

                    <div class="result-value {risk_class}">
                        {str(risk_level).upper()}
                    </div>
                </div>
                """)

            with r2:
                render_html(f"""
                <div class="result-card">
                    <div class="result-label">
                        Model Confidence
                    </div>

                    <div class="result-value">
                        {confidence:.2f}%
                    </div>
                </div>
                """)

            with r3:
                render_html("""
                <div class="result-card">
                    <div class="result-label">
                        Model
                    </div>

                    <div class="result-value">
                        V4
                    </div>
                </div>
                """)

            # ------------------------------------------------
            # PROBABILITY BREAKDOWN
            # ------------------------------------------------

            render_html("""
            <div class="section-heading">
                Risk Probability Breakdown
            </div>
            """)

            probability_data = []

            for class_code, probability in zip(
                model.classes_,
                probabilities
            ):

                class_name = label_encoder.inverse_transform(
                    [class_code]
                )[0]

                probability_data.append({
                    "Risk Level": str(class_name).upper(),
                    "Probability": f"{probability * 100:.2f}%"
                })

            probability_df = pd.DataFrame(probability_data)

            st.dataframe(
                probability_df,
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # FEATURE IMPORTANCE
            # ------------------------------------------------

            render_html("""
            <div class="section-heading">
                Feature Importance
            </div>
            """)

            importance_df = pd.DataFrame({
                "Feature": features,
                "Importance": model.feature_importances_
            })

            importance_df = importance_df.sort_values(
                by="Importance",
                ascending=False
            ).reset_index(drop=True)

            importance_display = importance_df.copy()

            importance_display["Importance"] = (
                importance_display["Importance"] * 100
            ).round(2)

            importance_display = importance_display.rename(
                columns={
                    "Importance": "Importance (%)"
                }
            )

            st.dataframe(
                importance_display,
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # FORENSIC INTERPRETATION
            # ------------------------------------------------

            if risk_lower == "low":

                interpretation = (
                    "The model indicates a relatively low preliminary "
                    "risk based on the supplied claim characteristics. "
                    "Normal claim processing may continue subject to "
                    "standard verification procedures."
                )

            elif risk_lower == "medium":

                interpretation = (
                    "The model indicates a medium preliminary risk. "
                    "Additional documentation or targeted verification "
                    "may be appropriate before reaching a final claim "
                    "decision."
                )

            else:

                interpretation = (
                    "The model indicates a high preliminary risk. "
                    "The result may justify enhanced verification or "
                    "forensic investigation before a final claim "
                    "decision."
                )

            render_html(f"""
            <div class="info-box">
                <strong>Forensic interpretation:</strong><br>
                {interpretation}
            </div>

            <div class="info-box">
                <strong>Important:</strong>
                This is an AI-assisted preliminary risk assessment.
                A high-risk result does not automatically mean that
                a claim is fraudulent or should be rejected.
                Final decisions require appropriate human review,
                evidence verification, and applicable insurance
                procedures.
            </div>
            """)

        except Exception as e:

            st.error(
                f"Assessment failed: {e}"
            )


# ============================================================
# DOCUMENTS
# ============================================================

elif page == "📄 Documents":

    render_html("""
    <div class="breadcrumb">
        INSURIX / 03
    </div>

    <div class="page-title">
        Documents
    </div>

    <div class="page-description">
        Evidence and documentation review area for future
        expansion of the Insurix platform.
    </div>
    """)

    col1, col2 = st.columns(2)

    with col1:

        render_html("""
        <div class="card">
            <div class="card-number">DOCUMENT 01</div>
            <div class="card-icon">📑</div>
            <div class="card-title">
                Claim Documentation
            </div>
            <div class="card-text">
                Organise and review claim-related documents
                before assessment.
            </div>
        </div>
        """)

    with col2:

        render_html("""
        <div class="card">
            <div class="card-number">DOCUMENT 02</div>
            <div class="card-icon">🔬</div>
            <div class="card-title">
                Forensic Evidence
            </div>
            <div class="card-text">
                Future versions can integrate structured
                forensic evidence analysis.
            </div>
        </div>
        """)

    render_html("""
    <div class="info-box">
        <strong>Future development:</strong>
        Document upload, OCR, metadata analysis, consistency
        checking, and evidence extraction can be integrated
        into this section in later versions.
    </div>
    """)


# ============================================================
# CLAIM STATUS
# ============================================================

elif page == "📊 Claim Status":

    render_html("""
    <div class="breadcrumb">
        INSURIX / 04
    </div>

    <div class="page-title">
        Claim Status
    </div>

    <div class="page-description">
        View the latest assessment generated during this session.
    </div>
    """)

    if st.session_state.last_risk is None:

        render_html("""
        <div class="card">
            <div class="card-icon">📊</div>
            <div class="card-title">
                No Assessment Available
            </div>
            <div class="card-text">
                Complete a claim assessment first to display
                the latest risk status here.
            </div>
        </div>
        """)

    else:

        current_risk = str(
            st.session_state.last_risk
        )

        current_confidence = st.session_state.last_confidence

        risk_lower = current_risk.lower()

        if risk_lower == "low":
            risk_class = "risk-low"
        elif risk_lower == "medium":
            risk_class = "risk-medium"
        else:
            risk_class = "risk-high"

        c1, c2 = st.columns(2)

        with c1:

            render_html(f"""
            <div class="result-card">
                <div class="result-label">
                    Current Risk
                </div>

                <div class="result-value {risk_class}">
                    {current_risk.upper()}
                </div>
            </div>
            """)

        with c2:

            render_html(f"""
            <div class="result-card">
                <div class="result-label">
                    Confidence
                </div>

                <div class="result-value">
                    {current_confidence:.2f}%
                </div>
            </div>
            """)

        render_html("""
        <div class="info-box">
            <strong>Status note:</strong>
            The displayed status represents the most recent
            assessment performed during the current application
            session.
        </div>
        """)


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">
    INSURIX • AI-Powered Forensic Insurance Risk Assessment
    • Version 4 • Random Forest Classification
</div>
""")
