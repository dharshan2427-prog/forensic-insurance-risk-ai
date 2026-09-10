import streamlit as st
import joblib
import pandas as pd
import os

# ============================================================
# INSURIX | INSURANCE RISK INTELLIGENCE
# Version 4 - Random Forest Classification
# ============================================================

st.set_page_config(
    page_title="Insurix | Insurance Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f5f9ff;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 35px;
        padding-bottom: 40px;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(
                circle at 20% 80%,
                rgba(25, 117, 255, 0.35),
                transparent 35%
            ),
            linear-gradient(
                180deg,
                #031b4e 0%,
                #062b73 55%,
                #0647a5 100%
            );
    }

    section[data-testid="stSidebar"] > div {
        padding: 28px 20px;
    }

    .brand-title {
        font-size: 31px;
        font-weight: 800;
        color: white;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .brand-title span {
        color: #35bfff;
    }

    .brand-subtitle {
        color: #d7e7ff;
        font-size: 13px;
        line-height: 1.55;
        margin-bottom: 28px;
    }

    .sidebar-divider {
        height: 1px;
        background: rgba(255,255,255,0.22);
        margin: 18px 0 28px 0;
    }

    .sidebar-label {
        color: #a9c7ef;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .system-box {
        position: fixed;
        bottom: 25px;
        left: 25px;
        color: #d9e8ff;
        font-size: 12px;
        line-height: 1.8;
    }

    .system-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #32e59a;
        margin-right: 7px;
    }

    /* ---------- SIDEBAR RADIO ---------- */

    section[data-testid="stSidebar"] .stRadio label {
        color: #eaf3ff !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] .stRadio > div {
        gap: 8px;
    }

    section[data-testid="stSidebar"] .stRadio label {
        padding: 10px 12px;
        border-radius: 8px;
    }

    /* ---------- PAGE HEADER ---------- */

    .eyebrow {
        color: #1769c2;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    .page-title {
        color: #06152f;
        font-size: 48px;
        line-height: 1.05;
        font-weight: 850;
        letter-spacing: -2px;
        margin: 0;
    }

    .page-subtitle {
        color: #67809e;
        font-size: 16px;
        margin-top: 10px;
        margin-bottom: 26px;
    }

    /* ---------- HERO ---------- */

    .hero {
        position: relative;
        overflow: hidden;
        min-height: 220px;
        border-radius: 18px;
        padding: 38px 48px;
        margin: 24px 0 24px 0;

        background:
            radial-gradient(
                circle at 90% 35%,
                rgba(0, 186, 255, 0.35),
                transparent 30%
            ),
            linear-gradient(
                120deg,
                #061a48 0%,
                #07347d 55%,
                #087bd1 100%
            );

        box-shadow: 0 18px 45px rgba(6, 52, 110, 0.20);
    }

    .hero-label {
        color: #c7eaff;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 16px;
    }

    .hero-title {
        color: white;
        font-size: 42px;
        line-height: 1.05;
        font-weight: 850;
        letter-spacing: -1.5px;
    }

    .hero-title span {
        color: #22c4ff;
    }

    .hero-text {
        color: #e4f3ff;
        font-size: 15px;
        margin-top: 17px;
        line-height: 1.5;
        max-width: 600px;
    }

    .hero-shield {
        position: absolute;
        right: 80px;
        top: 50px;
        font-size: 100px;
        opacity: 0.25;
    }

    /* ---------- CARDS ---------- */

    .info-card {
        background: white;
        border: 1px solid #e0eafa;
        border-radius: 15px;
        padding: 25px;
        min-height: 190px;
        box-shadow: 0 7px 25px rgba(18, 63, 116, 0.06);
    }

    .card-number {
        float: right;
        color: #3181d4;
        font-size: 12px;
        font-weight: 800;
    }

    .card-icon {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: #e5f3ff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 25px;
        margin-bottom: 18px;
    }

    .card-title {
        color: #071a40;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .card-text {
        color: #6580a1;
        font-size: 14px;
        line-height: 1.55;
    }

    /* ---------- INFO BOX ---------- */

    .ai-box {
        background: linear-gradient(
            100deg,
            #edf7ff,
            #f7fbff
        );
        border: 1px solid #b9ddff;
        border-left: 5px solid #149de2;
        border-radius: 12px;
        padding: 17px 20px;
        margin-top: 20px;
        color: #32658f;
        font-size: 14px;
        line-height: 1.55;
    }

    /* ---------- ASSESSMENT ---------- */

    .section-card {
        background: white;
        border: 1px solid #e0e8f4;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 28px rgba(15, 58, 110, 0.05);
    }

    .section-number {
        color: #2781cf;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }

    .section-title {
        color: #091a36;
        font-size: 22px;
        font-weight: 800;
        margin-top: 4px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #7187a2;
        font-size: 13px;
    }

    /* ---------- RESULT ---------- */

    .result-card {
        background: white;
        border-radius: 16px;
        border: 1px solid #dce8f5;
        padding: 24px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(20, 70, 120, 0.07);
    }

    .result-label {
        color: #6b829d;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    .result-value {
        color: #071b3e;
        font-size: 29px;
        font-weight: 850;
        margin-top: 8px;
    }

    .risk-low {
        color: #15956a;
    }

    .risk-medium {
        color: #d68a00;
    }

    .risk-high {
        color: #d64242;
    }

    /* ---------- STATUS ---------- */

    .status-card {
        background: white;
        border: 1px solid #dce7f4;
        border-radius: 15px;
        padding: 24px;
        min-height: 150px;
        box-shadow: 0 8px 25px rgba(15, 58, 110, 0.05);
    }

    .status-icon {
        font-size: 27px;
        margin-bottom: 10px;
    }

    .status-title {
        color: #071b3d;
        font-size: 18px;
        font-weight: 800;
    }

    .status-text {
        color: #7187a0;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 7px;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        background: linear-gradient(
            90deg,
            #087fc8,
            #18aeea
        );
        color: white;
        border: none;
        border-radius: 9px;
        padding: 12px 25px;
        font-weight: 750;
        min-height: 45px;
        box-shadow: 0 7px 18px rgba(13, 137, 205, 0.22);
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #066eaf,
            #0d9ed8
        );
        color: white;
    }

    /* ---------- INPUTS ---------- */

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stDateInput label,
    .stTextArea label,
    .stFileUploader label {
        color: #375676 !important;
        font-weight: 650 !important;
        font-size: 13px !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #d4e2f1 !important;
        background: #fbfdff !important;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #8ba0b9;
        font-size: 11px;
        padding: 35px 0 10px 0;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 800px) {

        .page-title {
            font-size: 36px;
        }

        .hero-title {
            font-size: 31px;
        }

        .hero {
            padding: 30px;
        }

        .hero-shield {
            display: none;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MODEL LOADER
# ============================================================

@st.cache_resource
def load_model():

    model_path = "insurance_risk_model_v4.pkl"

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "insurance_risk_model_v4.pkl was not found in the repository."
        )

    package = joblib.load(model_path)

    model = package["model"]
    label_encoder = package["label_encoder"]
    features = package["features"]

    return model, label_encoder, features


# ============================================================
# LOAD VERSION 4 MODEL
# ============================================================

try:

    model, label_encoder, features = load_model()

except Exception as e:

    st.error("Unable to load the Version 4 Random Forest model.")
    st.error(str(e))
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "last_risk" not in st.session_state:
    st.session_state.last_risk = None

if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = None

if "last_probabilities" not in st.session_state:
    st.session_state.last_probabilities = None

if "assessment_completed" not in st.session_state:
    st.session_state.assessment_completed = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-title">
            🛡️ Insur<span>ix</span>
        </div>

        <div class="brand-subtitle">
            AI-Powered Forensic<br>
            Insurance Risk Assessment
        </div>

        <div class="sidebar-divider"></div>

        <div class="sidebar-label">
            NAVIGATION
        </div>
        """,
        unsafe_allow_html=True
    )

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
        <div class="system-box">
            <span class="system-dot"></span>
            <b>System operational</b><br>
            &nbsp;&nbsp;&nbsp;&nbsp;Version 4 • Random Forest
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        """
        <div class="eyebrow">
            INSURIX / 01
        </div>

        <div class="page-title">
            Overview
        </div>

        <div class="page-subtitle">
            A clear starting point for every insurance claim.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
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

            <div class="hero-shield">
                🛡️
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="info-card">

                <div class="card-number">
                    01
                </div>

                <div class="card-icon">
                    🔍
                </div>

                <div class="card-title">
                    Claim Assessment
                </div>

                <div class="card-text">
                    Analyse claim indicators and obtain
                    an AI-assisted preliminary risk
                    classification.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">

                <div class="card-number">
                    02
                </div>

                <div class="card-icon">
                    📄
                </div>

                <div class="card-title">
                    Documents
                </div>

                <div class="card-text">
                    Review claim documentation and
                    supporting evidence associated
                    with a claim.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="info-card">

                <div class="card-number">
                    03
                </div>

                <div class="card-icon">
                    📊
                </div>

                <div class="card-title">
                    Claim Status
                </div>

                <div class="card-text">
                    View the latest assessment result
                    generated during the current
                    session.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="ai-box">
            <b>ⓘ AI-assisted assessment:</b>
            Insurix uses a Version 4 Random Forest
            classification model to provide a preliminary
            Low, Medium, or High risk indication from
            selected claim characteristics. The output
            supports investigation and triage and does
            not replace professional claim decisions.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="footer">
            INSURIX • AI-Powered Forensic Insurance Risk Assessment
            • Version 4 • Random Forest Classification
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CLAIM ASSESSMENT
# ============================================================

elif page == "🔍 Claim Assessment":

    st.markdown(
        """
        <div class="eyebrow">
            INSURIX / 02
        </div>

        <div class="page-title">
            Claim Assessment
        </div>

        <div class="page-subtitle">
            Enter the available claim indicators to generate
            a preliminary forensic insurance risk assessment.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">

            <div class="section-number">
                VERSION 4
            </div>

            <div class="section-title">
                Claim Intelligence Input
            </div>

            <div class="section-description">
                The Version 4 Random Forest model evaluates
                seven claim-related features.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        claim_amount = st.number_input(
            "Claim Amount (₹)",
            min_value=0.0,
            value=250000.0,
            step=10000.0
        )

        previous_claims = st.number_input(
            "Previous Claims",
            min_value=0,
            value=2,
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
            step=0.5
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
            ["Yes", "No"]
        )

        st.write("")
        st.write("")

        assess = st.button(
            "🔍  Assess Claim Risk",
            use_container_width=True
        )

    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    if assess:

        evidence_value = 1 if evidence_status == "Yes" else 0
        document_value = 1 if document_consistency == "Yes" else 0
        after_policy_value = 1 if claim_after_policy == "Yes" else 0

        input_data = pd.DataFrame(
            [[
                claim_amount,
                previous_claims,
                rejected_claims,
                claim_frequency,
                evidence_value,
                document_value,
                after_policy_value
            ]],
            columns=features
        )

        try:

            prediction = model.predict(input_data)[0]

            probabilities = model.predict_proba(input_data)[0]

            risk = label_encoder.inverse_transform(
                [prediction]
            )[0]

            confidence = max(probabilities) * 100

            st.session_state.last_risk = risk
            st.session_state.last_confidence = confidence
            st.session_state.last_probabilities = probabilities
            st.session_state.assessment_completed = True

            st.markdown("---")

            st.markdown(
                """
                <div class="section-card">

                    <div class="section-number">
                        ASSESSMENT RESULT
                    </div>

                    <div class="section-title">
                        Preliminary Risk Classification
                    </div>

                    <div class="section-description">
                        Result generated by the Version 4 Random Forest model.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            result_col1, result_col2, result_col3 = st.columns(3)

            if str(risk).lower() == "low":
                risk_class = "risk-low"
            elif str(risk).lower() == "medium":
                risk_class = "risk-medium"
            else:
                risk_class = "risk-high"

            with result_col1:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-label">
                            Risk Level
                        </div>

                        <div class="result-value {risk_class}">
                            {str(risk).upper()}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with result_col2:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-label">
                            Confidence
                        </div>

                        <div class="result-value">
                            {confidence:.2f}%
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with result_col3:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-label">
                            Model
                        </div>

                        <div class="result-value">
                            V4 RF
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ------------------------------------------------
            # PROBABILITY BREAKDOWN
            # ------------------------------------------------

            st.markdown(
                """
                <div class="section-card">
                    <div class="section-title">
                        Risk Probability Breakdown
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            probability_df = pd.DataFrame(
                {
                    "Risk Level": label_encoder.classes_,
                    "Probability (%)": [
                        round(p * 100, 2)
                        for p in probabilities
                    ]
                }
            )

            st.dataframe(
                probability_df,
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # FEATURE IMPORTANCE
            # ------------------------------------------------

            if hasattr(model, "feature_importances_"):

                st.markdown(
                    """
                    <div class="section-card">

                        <div class="section-title">
                            Model Feature Importance
                        </div>

                        <div class="section-description">
                            Relative contribution of each Version 4
                            model feature to the Random Forest.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

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

                importance_df["Importance"] = (
                    importance_df["Importance"] * 100
                ).round(2)

                st.bar_chart(
                    importance_df.set_index("Feature")
                )

                st.dataframe(
                    importance_df,
                    use_container_width=True,
                    hide_index=True
                )

            # ------------------------------------------------
            # FORENSIC NOTE
            # ------------------------------------------------

            st.markdown(
                """
                <div class="ai-box">

                    <b>Forensic interpretation note:</b><br>

                    The prediction is a preliminary machine-learning
                    classification based on the supplied claim indicators.
                    A High-risk classification should be treated as an
                    investigation/verification signal rather than automatic
                    evidence of fraud or a reason for automatic claim rejection.

                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error("Assessment could not be completed.")
            st.error(str(e))

    st.markdown(
        """
        <div class="footer">
            INSURIX • AI-Powered Forensic Insurance Risk Assessment
            • Version 4 • Random Forest Classification
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DOCUMENTS
# ============================================================

elif page == "📄 Documents":

    st.markdown(
        """
        <div class="eyebrow">
            INSURIX / 03
        </div>

        <div class="page-title">
            Documents
        </div>

        <div class="page-subtitle">
            Supporting documents and evidence for claim review.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="info-card">

                <div class="card-number">
                    01
                </div>

                <div class="card-icon">
                    📄
                </div>

                <div class="card-title">
                    Claim Documentation
                </div>

                <div class="card-text">
                    Upload and organise claim-related
                    documents before assessment.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">

                <div class="card-number">
                    02
                </div>

                <div class="card-icon">
                    🔬
                </div>

                <div class="card-title">
                    Forensic Evidence
                </div>

                <div class="card-text">
                    Supporting evidence can be associated
                    with the claim for future forensic
                    analysis.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    st.markdown(
        """
        <div class="section-card">

            <div class="section-number">
                DOCUMENT UPLOAD
            </div>

            <div class="section-title">
                Supporting Claim Evidence
            </div>

            <div class="section-description">
                Upload documents associated with the claim.
                Current Version 4 model classification is based
                on the seven structured claim indicators.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload claim documents",
        type=[
            "pdf",
            "jpg",
            "jpeg",
            "png",
            "docx",
            "xlsx",
            "csv"
        ],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} document(s) uploaded for this session."
        )

        for file in uploaded_files:

            st.write(
                f"📄 **{file.name}** — "
                f"{file.size / 1024:.1f} KB"
            )

    st.markdown(
        """
        <div class="ai-box">

            <b>Future development:</b>
            OCR, metadata analysis, document consistency checking,
            structured evidence extraction and automated document
            analysis can be integrated into this section in later
            versions.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="footer">
            INSURIX • AI-Powered Forensic Insurance Risk Assessment
            • Version 4 • Random Forest Classification
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CLAIM STATUS
# ============================================================

elif page == "📊 Claim Status":

    st.markdown(
        """
        <div class="eyebrow">
            INSURIX / 04
        </div>

        <div class="page-title">
            Claim Status
        </div>

        <div class="page-subtitle">
            View the latest assessment generated during this session.
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # NO ASSESSMENT
    # --------------------------------------------------------

    if not st.session_state.assessment_completed:

        st.markdown(
            """
            <div class="section-card">

                <div class="status-icon">
                    ℹ️
                </div>

                <div class="section-title">
                    No assessment yet
                </div>

                <div class="section-description">
                    Complete a claim assessment first.
                    The latest Version 4 Random Forest result
                    will appear here.

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # ASSESSMENT EXISTS
    # --------------------------------------------------------

    else:

        risk = st.session_state.last_risk
        confidence = st.session_state.last_confidence

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                """
                <div class="status-card">

                    <div class="status-icon">
                        ✅
                    </div>

                    <div class="status-title">
                        Assessment Status
                    </div>

                    <div class="status-text">
                        Completed successfully.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            if str(risk).lower() == "low":
                status_class = "risk-low"
            elif str(risk).lower() == "medium":
                status_class = "risk-medium"
            else:
                status_class = "risk-high"

            st.markdown(
                f"""
                <div class="status-card">

                    <div class="status-icon">
                        🛡️
                    </div>

                    <div class="status-title">
                        Risk Level
                    </div>

                    <div class="status-text {status_class}">
                        <b>{str(risk).upper()}</b>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="status-card">

                    <div class="status-icon">
                        %
                    </div>

                    <div class="status-title">
                        Confidence
                    </div>

                    <div class="status-text">
                        <b>{confidence:.2f}%</b>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            """
            <div class="ai-box">

                <b>Next step:</b>
                Use the risk classification as a preliminary
                decision-support indicator. Additional evidence,
                investigation and professional review should be
                considered before making a claim decision.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            """
            <div class="section-card">

                <div class="section-number">
                    INSURIX / CURRENT SESSION
                </div>

                <div class="section-title">
                    Latest Assessment Available
                </div>

                <div class="section-description">
                    The current session contains a completed
                    Version 4 Random Forest assessment.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="footer">
            INSURIX • AI-Powered Forensic Insurance Risk Assessment
            • Version 4 • Random Forest Classification
        </div>
        """,
        unsafe_allow_html=True
    )
