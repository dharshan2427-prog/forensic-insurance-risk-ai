import streamlit as st
import joblib
import pandas as pd
import os
import re
import textwrap
import sqlite3
import hashlib
import hmac

from pypdf import PdfReader
from docx import Document


# ============================================================
# INSURIX | INSURANCE RISK INTELLIGENCE
# VERSION 4 - RANDOM FOREST + DOCUMENT INTELLIGENCE
# ============================================================

st.set_page_config(
    page_title="Insurix | Insurance Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# INSURIX ACCOUNT AUTHENTICATION
# ============================================================

USER_DB = "insurix_users.db"


def init_user_database():
    """Create the local prototype account database if needed."""
    connection = sqlite3.connect(USER_DB)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            organization TEXT,
            role TEXT,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.commit()
    connection.close()


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        120000
    )
    return password_hash.hex(), salt.hex()


def create_user(full_name, email, organization, role, password):
    password_hash, password_salt = hash_password(password)
    try:
        connection = sqlite3.connect(USER_DB)
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO users
            (full_name, email, organization, role, password_hash, password_salt)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                full_name.strip(),
                email.strip().lower(),
                organization.strip(),
                role,
                password_hash,
                password_salt
            )
        )
        connection.commit()
        connection.close()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    except Exception:
        return False, "Unable to create the account right now."


def authenticate_user(email, password):
    connection = sqlite3.connect(USER_DB)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, full_name, email, organization, role,
               password_hash, password_salt
        FROM users
        WHERE email = ?
        """,
        (email.strip().lower(),)
    )
    row = cursor.fetchone()
    connection.close()

    if not row:
        return None

    user_id, full_name, user_email, organization, role, stored_hash, stored_salt = row
    candidate_hash, _ = hash_password(password, stored_salt)

    if hmac.compare_digest(candidate_hash, stored_hash):
        return {
            "id": user_id,
            "full_name": full_name,
            "email": user_email,
            "organization": organization or "",
            "role": role or "Claims Analyst"
        }

    return None


init_user_database()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"


# ============================================================
# OWNER / ADMIN ACCESS CONFIGURATION
# ============================================================

def get_owner_access_key():
    """Read the owner key from Streamlit secrets or environment.

    For a prototype/demo, a fallback key is provided so the owner can
    access the app without creating an email account first. For deployment,
    set INSURIX_OWNER_KEY in Streamlit Secrets.
    """
    try:
        secret_key = st.secrets.get("INSURIX_OWNER_KEY", "")
        if secret_key:
            return str(secret_key)
    except Exception:
        pass

    return os.environ.get("INSURIX_OWNER_KEY", "INSURIX-OWNER-2026")


OWNER_ACCESS_KEY = get_owner_access_key()


# ============================================================
# AUTHENTICATION SCREEN
# ============================================================

if not st.session_state.authenticated:

    st.markdown(
        """
        <style>
        .auth-shell {
            min-height: 82vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px 10px;
        }
        .auth-card {
            width: 100%;
            max-width: 1080px;
            background: #ffffff;
            border: 1px solid #e1e9f4;
            border-radius: 28px;
            box-shadow: 0 24px 70px rgba(8, 35, 75, 0.12);
            overflow: hidden;
        }
        .auth-brand {
            background: linear-gradient(145deg, #061b3d, #0b3d78);
            color: #ffffff;
            padding: 54px 46px;
            min-height: 610px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .auth-logo {
            font-size: 36px;
            font-weight: 850;
            letter-spacing: -1px;
        }
        .auth-kicker {
            color: #75c9ff;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.6px;
            margin-top: 8px;
        }
        .auth-heading {
            font-size: 38px;
            line-height: 1.08;
            font-weight: 800;
            margin: 0 0 16px 0;
        }
        .auth-copy {
            color: #cbd9ec;
            font-size: 16px;
            line-height: 1.6;
            max-width: 430px;
        }
        .auth-feature {
            color: #e8f2ff;
            margin-top: 22px;
            font-size: 14px;
        }
        .auth-form-title {
            color: #071b3b;
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 4px;
        }
        .auth-form-copy {
            color: #718096;
            margin-bottom: 22px;
        }
        .owner-access-card {
            background: #f4f8ff;
            border: 1px solid #d9e6f7;
            border-radius: 16px;
            padding: 16px 18px;
            margin-top: 20px;
        }
        .owner-access-title {
            color: #12325f;
            font-size: 14px;
            font-weight: 800;
            margin-bottom: 4px;
        }
        .owner-access-copy {
            color: #6d7c91;
            font-size: 12px;
            line-height: 1.5;
        }
        .auth-footer {
            text-align: center;
            color: #8a97aa;
            font-size: 12px;
            margin-top: 18px;
        }
        div[data-testid="stForm"] {
            border: 0 !important;
            padding: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="auth-shell"><div class="auth-card">', unsafe_allow_html=True)
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown(
            """
            <div class="auth-brand">
                <div>
                    <div class="auth-logo">🛡️ INSURIX</div>
                    <div class="auth-kicker">FORENSIC × INSURANCE</div>
                </div>
                <div>
                    <div class="auth-heading">Smarter insurance.<br>Stronger evidence.</div>
                    <div class="auth-copy">
                        A professional workspace for preliminary AI-assisted
                        claim risk assessment and forensic document intelligence.
                    </div>
                    <div class="auth-feature">✓ AI-assisted risk classification</div>
                    <div class="auth-feature">✓ Claim document intelligence</div>
                    <div class="auth-feature">✓ Evidence-focused workflow</div>
                    <div class="auth-feature">✓ Role-based workspace access</div>
                </div>
                <div style="color:#9fb7d5;font-size:12px;">INSURIX • VERSION 4 • RANDOM FOREST</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown('<div style="padding:54px 48px 38px 20px;">', unsafe_allow_html=True)

        # --------------------------------------------------------
        # NORMAL USER LOGIN
        # --------------------------------------------------------
        if st.session_state.auth_mode == "login":
            st.markdown('<div class="auth-form-title">Welcome back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-form-copy">Sign in to access your Insurix workspace.</div>', unsafe_allow_html=True)

            with st.form("login_form"):
                login_email = st.text_input("Work email", placeholder="name@company.com")
                login_password = st.text_input("Password", type="password", placeholder="Enter your password")
                remember_me = st.checkbox("Keep me signed in for this session")
                login_submit = st.form_submit_button("Sign in  →", use_container_width=True)

            if login_submit:
                if not login_email or not login_password:
                    st.error("Please enter your email and password.")
                else:
                    user = authenticate_user(login_email, login_password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.current_user = user
                        st.session_state.page = "Overview"
                        st.session_state.remember_me = remember_me
                        st.rerun()
                    else:
                        st.error("Incorrect email or password.")

            st.write("")
            if st.button("👑 Owner / Admin Access", use_container_width=True, key="go_owner"):
                st.session_state.auth_mode = "owner"
                st.rerun()

            if st.button("Create a new account", use_container_width=True, key="go_create"):
                st.session_state.auth_mode = "create"
                st.rerun()

        # --------------------------------------------------------
        # OWNER / ADMIN ACCESS
        # --------------------------------------------------------
        elif st.session_state.auth_mode == "owner":
            st.markdown('<div class="auth-form-title">Owner / Admin Access</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="auth-form-copy">Access the Insurix administrative workspace without using a user email.</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="owner-access-card">
                    <div class="owner-access-title">👑 Platform Owner</div>
                    <div class="owner-access-copy">
                        This access is reserved for the Insurix owner or administrator.
                        Use your private owner access key to enter the platform.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.form("owner_login_form"):
                owner_key_input = st.text_input(
                    "Owner access key",
                    type="password",
                    placeholder="Enter owner access key"
                )
                owner_submit = st.form_submit_button(
                    "Enter Owner Workspace  →",
                    use_container_width=True
                )

            if owner_submit:
                if owner_key_input and hmac.compare_digest(owner_key_input, OWNER_ACCESS_KEY):
                    st.session_state.authenticated = True
                    st.session_state.current_user = {
                        "id": 0,
                        "full_name": "Insurix Owner",
                        "email": "owner@insurix.local",
                        "organization": "Insurix",
                        "role": "Administrator"
                    }
                    st.session_state.page = "Overview"
                    st.session_state.remember_me = False
                    st.rerun()
                else:
                    st.error("Invalid owner access key.")

            st.info("For deployment, store INSURIX_OWNER_KEY in Streamlit Secrets instead of using the demo fallback key.")

            st.write("")
            if st.button("← Back to sign in", use_container_width=True, key="owner_back"):
                st.session_state.auth_mode = "login"
                st.rerun()

        # --------------------------------------------------------
        # CREATE NORMAL USER ACCOUNT
        # --------------------------------------------------------
        else:
            st.markdown('<div class="auth-form-title">Create your account</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-form-copy">Set up your secure Insurix workspace.</div>', unsafe_allow_html=True)

            with st.form("create_account_form"):
                create_name = st.text_input("Full name", placeholder="Your full name")
                create_email = st.text_input("Work email", placeholder="name@company.com")
                create_org = st.text_input("Organization", placeholder="Company / Agency / Institution")
                create_role = st.selectbox(
                    "Role",
                    ["Claims Analyst", "Forensic Investigator", "Insurance Manager"]
                )
                create_password = st.text_input("Password", type="password", placeholder="At least 8 characters")
                create_confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter your password")
                create_submit = st.form_submit_button("Create account  →", use_container_width=True)

            if create_submit:
                email_ok = bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", create_email.strip()))
                if not create_name.strip() or not create_email.strip() or not create_org.strip():
                    st.error("Please complete all required fields.")
                elif not email_ok:
                    st.error("Please enter a valid work email address.")
                elif len(create_password) < 8:
                    st.error("Password must contain at least 8 characters.")
                elif create_password != create_confirm:
                    st.error("Passwords do not match.")
                else:
                    created, message = create_user(
                        create_name,
                        create_email,
                        create_org,
                        create_role,
                        create_password
                    )
                    if created:
                        st.success(message + " You can now sign in.")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error(message)

            st.write("")
            if st.button("👑 Owner / Admin Access", use_container_width=True, key="create_owner"):
                st.session_state.auth_mode = "owner"
                st.rerun()

            if st.button("← Back to sign in", use_container_width=True, key="go_login"):
                st.session_state.auth_mode = "login"
                st.rerun()

        st.markdown(
            '<div class="auth-footer">Protected Insurix workspace • Preliminary AI-assisted risk assessment</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()


# ============================================================
# LOAD VERSION 4 RANDOM FOREST MODEL
# ============================================================

MODEL_FILE = "insurance_risk_model_v4.pkl"

if not os.path.exists(MODEL_FILE):

    st.error(
        "Version 4 model file was not found. "
        "Please make sure insurance_risk_model_v4.pkl "
        "is in the repository."
    )

    st.stop()


try:

    model_package = joblib.load(MODEL_FILE)

    model = model_package["model"]
    label_encoder = model_package["label_encoder"]
    features = model_package["features"]


except Exception as e:

    st.error(
        "Unable to load the Version 4 Random Forest model."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# DOCUMENT TEXT EXTRACTION
# ============================================================

def extract_text_from_document(uploaded_file):

    file_name = uploaded_file.name.lower()

    try:

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        if file_name.endswith(".pdf"):

            reader = PdfReader(uploaded_file)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

            return text


        # ----------------------------------------------------
        # DOCX
        # ----------------------------------------------------

        elif file_name.endswith(".docx"):

            document = Document(uploaded_file)

            text = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

            return text


        # ----------------------------------------------------
        # TXT
        # ----------------------------------------------------

        elif file_name.endswith(".txt"):

            return uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )


        else:

            return ""


    except Exception as e:

        return f"DOCUMENT_ERROR: {str(e)}"


# ============================================================
# DOCUMENT ANALYSIS
# ============================================================

def analyse_claim_document(
    document_text,
    claim_amount,
    incident_date
):

    text = document_text.lower()

    findings = []

    # ========================================================
    # CLAIM AMOUNT CHECK
    # ========================================================

    amount_patterns = [
        r'₹\s?[\d,]+(?:\.\d+)?',
        r'rs\.?\s?[\d,]+(?:\.\d+)?',
        r'inr\s?[\d,]+(?:\.\d+)?'
    ]

    document_amounts = []

    for pattern in amount_patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            number = re.sub(
                r'[^\d.]',
                '',
                match
            )

            if number:

                try:

                    document_amounts.append(
                        float(number)
                    )

                except:

                    pass


    if document_amounts:

        closest_amount = min(
            document_amounts,
            key=lambda x: abs(x - claim_amount)
        )

        difference = abs(
            closest_amount - claim_amount
        )

        if claim_amount > 0:

            difference_percentage = (
                difference / claim_amount
            ) * 100

        else:

            difference_percentage = 0


        if difference_percentage <= 10:

            findings.append(
                f"Claim amount appears consistent "
                f"with document amount "
                f"(₹{closest_amount:,.0f})."
            )

            amount_consistent = True

        else:

            findings.append(
                f"Possible claim amount mismatch detected. "
                f"Entered: ₹{claim_amount:,.0f}, "
                f"document: ₹{closest_amount:,.0f}."
            )

            amount_consistent = False


    else:

        findings.append(
            "No clear claim amount was extracted "
            "from the document."
        )

        amount_consistent = False


    # ========================================================
    # INCIDENT DATE CHECK
    # ========================================================

    date_formats = [

        incident_date.strftime("%d-%m-%Y"),

        incident_date.strftime("%d/%m/%Y"),

        incident_date.strftime("%d.%m.%Y"),

        incident_date.strftime("%Y-%m-%d")

    ]


    date_found = False

    for date_format in date_formats:

        if date_format.lower() in text:

            date_found = True

            break


    if date_found:

        findings.append(
            "Incident date appears in the document."
        )

    else:

        findings.append(
            "Incident date was not clearly found "
            "in the document."
        )


    # ========================================================
    # POLICE / FIR CHECK
    # ========================================================

    police_keywords = [

        "fir",

        "police report",

        "police complaint",

        "first information report",

        "crime number",

        "case number"

    ]


    police_found = any(
        keyword in text
        for keyword in police_keywords
    )


    if police_found:

        findings.append(
            "Police/FIR-related evidence detected."
        )

    else:

        findings.append(
            "No clear police/FIR reference detected."
        )


    # ========================================================
    # INVOICE / REPAIR CHECK
    # ========================================================

    invoice_keywords = [

        "invoice",

        "repair bill",

        "garage bill",

        "repair estimate",

        "estimate",

        "quotation",

        "work order"

    ]


    invoice_found = any(
        keyword in text
        for keyword in invoice_keywords
    )


    if invoice_found:

        findings.append(
            "Repair/invoice-related evidence detected."
        )

    else:

        findings.append(
            "No clear repair invoice or estimate detected."
        )


    # ========================================================
    # SUPPORTING EVIDENCE CHECK
    # ========================================================

    evidence_keywords = [

        "photograph",

        "photographs",

        "photo",

        "evidence",

        "inspection",

        "surveyor",

        "inspection report",

        "damage assessment"

    ]


    evidence_found = any(
        keyword in text
        for keyword in evidence_keywords
    )


    if evidence_found:

        findings.append(
            "Supporting evidence references detected."
        )

    else:

        findings.append(
            "Limited supporting evidence references detected."
        )


    # ========================================================
    # DOCUMENT CONSISTENCY
    # ========================================================

    consistency_score = 1

    if not amount_consistent:

        consistency_score = 0


    # ========================================================
    # EVIDENCE STATUS
    # ========================================================

    evidence_score = 1 if evidence_found else 0


    # ========================================================
    # RETURN ANALYSIS
    # ========================================================

    return {

        "findings": findings,

        "document_consistency":
            consistency_score,

        "evidence_status":
            evidence_score,

        "document_amounts":
            document_amounts,

        "police_found":
            police_found,

        "invoice_found":
            invoice_found,

        "evidence_found":
            evidence_found,

        "amount_consistent":
            amount_consistent,

        "date_found":
            date_found

    }


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


if "document_analysis" not in st.session_state:

    st.session_state.document_analysis = None


if "last_risk_score" not in st.session_state:

    st.session_state.last_risk_score = None


if "last_risk_factors" not in st.session_state:

    st.session_state.last_risk_factors = []


if "last_missing_information" not in st.session_state:

    st.session_state.last_missing_information = []


if "last_claim_id" not in st.session_state:

    st.session_state.last_claim_id = ""


if "last_policyholder" not in st.session_state:

    st.session_state.last_policyholder = ""


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f9fc;
    }

    section[data-testid="stSidebar"] {
        background-color: #07152f;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

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

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 8px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e4eaf2;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: #e3e8ef;
    }


    .result-card {
        background: #ffffff;
        border: 1px solid #e2e9f3;
        border-radius: 24px;
        padding: 34px;
        margin-top: 24px;
        box-shadow: 0 10px 35px rgba(20, 45, 90, 0.08);
    }
    .result-layout {
        display: grid;
        grid-template-columns: 220px 1fr;
        gap: 38px;
        align-items: center;
    }
    .score-ring {
        width: 178px;
        height: 178px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        background: conic-gradient(var(--risk-color) calc(var(--score) * 1%), #dce5f2 0);
    }
    .score-inner {
        width: 134px;
        height: 134px;
        border-radius: 50%;
        background: #ffffff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .score-number {
        font-size: 50px;
        font-weight: 800;
        line-height: 1;
        color: var(--risk-color);
    }
    .score-label {
        font-size: 13px;
        color: #66758d;
        font-weight: 700;
        margin-top: 7px;
    }
    .risk-badge {
        display: inline-block;
        padding: 7px 15px;
        border-radius: 18px;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .badge-low { background: #dff5e5; color: #23803d; }
    .badge-medium { background: #fff0cf; color: #a56800; }
    .badge-high { background: #ffe0e5; color: #d92745; }
    .result-title {
        font-size: 38px;
        font-weight: 800;
        color: #142b5c;
        margin: 0 0 10px 0;
    }
    .result-description {
        font-size: 16px;
        line-height: 1.55;
        color: #61718a;
        max-width: 900px;
    }
    .result-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 50px;
        margin-top: 34px;
    }
    .result-section-title {
        font-size: 17px;
        font-weight: 800;
        color: #142b5c;
        margin-bottom: 13px;
        letter-spacing: .3px;
    }
    .risk-item, .missing-item {
        font-size: 15px;
        color: #60708a;
        margin: 9px 0;
        line-height: 1.45;
    }
    .risk-item::before {
        content: "•";
        color: #ed334f;
        font-size: 22px;
        font-weight: 800;
        margin-right: 10px;
    }
    .missing-item::before {
        content: "•";
        color: #f0a21a;
        font-size: 22px;
        font-weight: 800;
        margin-right: 10px;
    }
    @media (max-width: 800px) {
        .result-layout { grid-template-columns: 1fr; }
        .result-columns { grid-template-columns: 1fr; gap: 20px; }
        .result-title { font-size: 30px; }
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

    current_user = st.session_state.current_user or {}
    st.markdown("### ACCOUNT")
    st.markdown(f"**{current_user.get('full_name', 'User')}**")
    st.caption(current_user.get("role", "Claims Analyst"))
    if st.button("↪ Sign out", use_container_width=True, key="sidebar_logout"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.auth_mode = "login"
        st.rerun()

    st.divider()

    st.markdown("### SYSTEM")

    st.success("System operational")

    st.caption(
        "Version 4 • Random Forest"
    )

    st.caption(
        "Document Intelligence enabled"
    )

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


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    hero_left, hero_right = st.columns([2.2, 1])


    with hero_left:

        st.info("FORENSIC × INSURANCE")

        st.header(
            "Make the evidence work harder."
        )

        st.write(
            "Capture the claim. Analyse supporting "
            "documents. Understand the risk. "
            "Move forward with confidence."
        )

        st.write("")


        if st.button(
            "Start Claim Assessment →",
            key="overview_assessment"
        ):

            st.session_state.page = (
                "Claim Assessment"
            )

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

        st.metric(
            "DOCUMENT ANALYSIS",
            "Enabled"
        )


    st.divider()


    # --------------------------------------------------------
    # PLATFORM
    # --------------------------------------------------------

    st.subheader("Platform")

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            "### 🔍 Claim Assessment"
        )

        st.write(
            "Evaluate claim indicators using "
            "the Version 4 Random Forest model."
        )


        if st.button(
            "Open Assessment →",
            key="overview_claim"
        ):

            st.session_state.page = (
                "Claim Assessment"
            )

            st.rerun()


    with col2:

        st.markdown(
            "### 📄 Document Intelligence"
        )

        st.write(
            "Extract information from supporting "
            "PDF, DOCX and TXT claim documents."
        )


        if st.button(
            "Open Documents →",
            key="overview_documents"
        ):

            st.session_state.page = (
                "Documents"
            )

            st.rerun()


    with col3:

        st.markdown(
            "### 📊 Claim Status"
        )

        st.write(
            "Review the most recent assessment "
            "generated during this session."
        )


        if st.button(
            "View Status →",
            key="overview_status"
        ):

            st.session_state.page = (
                "Claim Status"
            )

            st.rerun()


    st.divider()


    # --------------------------------------------------------
    # HOW INSURIX WORKS
    # --------------------------------------------------------

    st.subheader(
        "How Insurix Works"
    )

    step1, step2, step3 = st.columns(3)


    with step1:

        st.markdown("### 01")

        st.markdown("**Capture**")

        st.write(
            "Enter the available claim "
            "information and risk indicators."
        )


    with step2:

        st.markdown("### 02")

        st.markdown("**Analyse**")

        st.write(
            "Extract information from claim "
            "documents and perform preliminary "
            "consistency checks."
        )


    with step3:

        st.markdown("### 03")

        st.markdown("**Assess**")

        st.write(
            "The Version 4 Random Forest model "
            "provides a preliminary Low, Medium "
            "or High risk classification."
        )


    st.divider()


    st.caption(
        "INSURIX • AI-Powered Forensic "
        "Insurance Risk Assessment • Version 4"
    )


# ============================================================
# CLAIM ASSESSMENT PAGE
# ============================================================

elif st.session_state.page == "Claim Assessment":

    st.caption(
        "INSURIX WORKSPACE / CLAIM ASSESSMENT"
    )

    st.title("Claim Assessment")

    st.write(
        "Build a consistent evidence record "
        "before review."
    )

    st.divider()


    # ========================================================
    # CLAIM IDENTITY
    # ========================================================

    st.subheader(
        "01  •  Claim identity"
    )

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


    # ========================================================
    # EVIDENCE AVAILABILITY
    # ========================================================

    st.subheader(
        "02  •  Evidence availability"
    )

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


    st.divider()


    # ========================================================
    # DOCUMENT INTELLIGENCE
    # ========================================================

    st.subheader(
        "03  •  Document intelligence"
    )

    st.write(
        "Upload a claim-related PDF, DOCX or TXT "
        "document. Insurix will extract readable text "
        "and perform preliminary consistency checks."
    )


    claim_document = st.file_uploader(
        "Upload claim document",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        key="claim_document"
    )


    document_analysis = None


    if claim_document:

        st.success(
            f"Document uploaded: "
            f"{claim_document.name}"
        )


        extracted_text = (
            extract_text_from_document(
                claim_document
            )
        )


        if extracted_text.startswith(
            "DOCUMENT_ERROR"
        ):

            st.error(
                "The document could not be analysed."
            )

            st.code(extracted_text)


        elif not extracted_text.strip():

            st.warning(
                "No readable text was extracted "
                "from this document. This may be "
                "a scanned/image-only document."
            )


        else:

            document_analysis = (
                analyse_claim_document(
                    extracted_text,
                    estimated_amount,
                    incident_date
                )
            )


            # Save document analysis
            st.session_state.document_analysis = (
                document_analysis
            )


            st.markdown(
                "### Document Analysis"
            )


            for finding in (
                document_analysis["findings"]
            ):

                finding_lower = finding.lower()


                if "mismatch" in finding_lower:

                    st.warning(
                        "⚠️ " + finding
                    )


                elif (
                    "not clearly" in finding_lower
                    or "not detected" in finding_lower
                    or "limited" in finding_lower
                ):

                    st.warning(
                        "⚠️ " + finding
                    )


                else:

                    st.success(
                        "✓ " + finding
                    )


            st.write("")


            doc_col1, doc_col2 = st.columns(2)


            with doc_col1:

                if (
                    document_analysis[
                        "document_consistency"
                    ] == 1
                ):

                    st.metric(
                        "Document Consistency",
                        "Consistent"
                    )

                else:

                    st.metric(
                        "Document Consistency",
                        "Needs Review"
                    )


            with doc_col2:

                if (
                    document_analysis[
                        "evidence_status"
                    ] == 1
                ):

                    st.metric(
                        "Evidence Status",
                        "Evidence Detected"
                    )

                else:

                    st.metric(
                        "Evidence Status",
                        "Limited Evidence"
                    )


            with st.expander(
                "View extracted document text"
            ):

                st.text(
                    extracted_text[:10000]
                )


    st.divider()


    # ========================================================
    # FORENSIC RISK INDICATORS
    # ========================================================

    st.subheader(
        "04  •  Forensic risk indicators"
    )


    model_col1, model_col2 = st.columns(2)


    with model_col1:

        document_consistency_text = st.selectbox(
            "Document consistency",
            ["Yes", "No"],
            key="manual_document_consistency"
        )


    with model_col2:

        evidence_status_text = st.selectbox(
            "Evidence status",
            ["Yes", "No"],
            key="manual_evidence_status"
        )


    model_col3, model_col4 = st.columns(2)


    with model_col3:

        claim_after_policy_text = st.selectbox(
            "Claim after policy",
            ["No", "Yes"]
        )


    with model_col4:

        st.info(
            "If a document is uploaded, "
            "document analysis will automatically "
            "provide the evidence and consistency "
            "values used by the model."
        )


    st.divider()


    st.info(
        "Version 4 evaluates seven model features: "
        "claim amount, previous claims, rejected claims, "
        "claim frequency, evidence status, document "
        "consistency and claim after policy."
    )


    # Keep these values available on every Streamlit rerun so the result
    # card remains stable when the user clicks Generate Report or navigates.
    manual_evidence_status = 1 if evidence_status_text == "Yes" else 0
    manual_document_consistency = (
        1 if document_consistency_text == "Yes" else 0
    )
    claim_after_policy = 1 if claim_after_policy_text == "Yes" else 0

    if document_analysis is not None:
        evidence_status = document_analysis["evidence_status"]
        document_consistency = document_analysis["document_consistency"]
    else:
        evidence_status = manual_evidence_status
        document_consistency = manual_document_consistency


    st.write("")


    # ========================================================
    # RUN ASSESSMENT
    # ========================================================

    run_assessment = st.button(
        "Run Assessment  →",
        key="run_assessment",
        use_container_width=False
    )


    if run_assessment:

        # ----------------------------------------------------
        # MANUAL VALUES
        # ----------------------------------------------------

        manual_evidence_status = (
            1
            if evidence_status_text == "Yes"
            else 0
        )


        manual_document_consistency = (
            1
            if document_consistency_text == "Yes"
            else 0
        )


        claim_after_policy = (
            1
            if claim_after_policy_text == "Yes"
            else 0
        )


        # ----------------------------------------------------
        # DOCUMENT-AWARE VALUES
        # ----------------------------------------------------

        if document_analysis is not None:

            evidence_status = (
                document_analysis[
                    "evidence_status"
                ]
            )


            document_consistency = (
                document_analysis[
                    "document_consistency"
                ]
            )


            st.info(
                "The model is using the document-analysis "
                "results for Evidence Status and "
                "Document Consistency."
            )


        else:

            evidence_status = (
                manual_evidence_status
            )


            document_consistency = (
                manual_document_consistency
            )


            st.info(
                "No readable claim document was supplied. "
                "The model is using the manually entered "
                "Evidence Status and Document Consistency."
            )


        # ----------------------------------------------------
        # CREATE MODEL INPUT
        # ----------------------------------------------------

        input_data = {

            "claim_amount":
                estimated_amount,

            "previous_claims":
                previous_claims,

            "rejected_claims":
                rejected_claims,

            "claim_frequency":
                claim_frequency,

            "evidence_status":
                evidence_status,

            "document_consistency":
                document_consistency,

            "claim_after_policy":
                claim_after_policy

        }


        input_df = pd.DataFrame(
            [input_data],
            columns=features
        )


        # ====================================================
        # RANDOM FOREST PREDICTION
        # ====================================================

        try:

            prediction = model.predict(
                input_df
            )


            prediction_label = (
                label_encoder.inverse_transform(
                    prediction
                )[0]
            )


            probabilities = (
                model.predict_proba(
                    input_df
                )[0]
            )


            class_names = (
                label_encoder.classes_
            )


            probability_dict = {}


            for class_name, probability in zip(
                class_names,
                probabilities
            ):

                probability_dict[class_name] = (
                    float(probability) * 100
                )


            confidence = max(
                probability_dict.values()
            )


            # ------------------------------------------------
            # SAVE RESULT
            # ------------------------------------------------

            st.session_state.last_risk = str(
                prediction_label
            )


            st.session_state.last_confidence = (
                float(confidence)
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


    # ========================================================
    # RESULT — THINK10X-STYLE INSURIX RESULT CARD
    # ========================================================

    if st.session_state.assessment_done:

        st.divider()

        risk = st.session_state.last_risk
        confidence = st.session_state.last_confidence
        probabilities = st.session_state.last_probabilities or {}

        high_prob = float(probabilities.get("High", 0))
        medium_prob = float(probabilities.get("Medium", 0))
        low_prob = float(probabilities.get("Low", 0))

        # Presentation score for the circular UI. It is deliberately
        # labelled as a preliminary risk score and is not model confidence.
        risk_score = round(
            (high_prob * 1.0) +
            (medium_prob * 0.5) +
            (low_prob * 0.1)
        )
        risk_score = max(0, min(100, risk_score))

        risk_lower = str(risk).lower()

        if risk_lower == "high":
            risk_color = "#ed334f"
            badge_class = "badge-high"
            description = (
                "This claim shows multiple risk indicators and requires "
                "further forensic investigation before the final decision."
            )
        elif risk_lower == "medium":
            risk_color = "#f0a21a"
            badge_class = "badge-medium"
            description = (
                "This claim shows some risk indicators and should receive "
                "additional verification before the final decision."
            )
        else:
            risk_color = "#2e9b50"
            badge_class = "badge-low"
            description = (
                "This claim currently shows relatively low-risk indicators. "
                "Routine verification is recommended before the final decision."
            )

        # ----------------------------------------------------
        # Risk factors
        # ----------------------------------------------------
        risk_factors = []

        if estimated_amount >= 300000:
            risk_factors.append(f"High claim amount (₹{estimated_amount:,.0f})")
        elif estimated_amount >= 200000:
            risk_factors.append(f"Elevated claim amount (₹{estimated_amount:,.0f})")

        if previous_claims >= 5:
            risk_factors.append(f"Multiple previous claims ({previous_claims})")
        elif previous_claims >= 3:
            risk_factors.append(f"Several previous claims ({previous_claims})")

        if rejected_claims >= 3:
            risk_factors.append(f"Multiple rejected claims ({rejected_claims})")
        elif rejected_claims >= 1:
            risk_factors.append(f"Previous rejected claim(s) ({rejected_claims})")

        if claim_frequency >= 7:
            risk_factors.append(f"High claim frequency ({claim_frequency})")
        elif claim_frequency >= 4:
            risk_factors.append(f"Moderate claim frequency ({claim_frequency})")

        if claim_after_policy == 1:
            risk_factors.append("Claim after policy")

        if evidence_status == 0:
            risk_factors.append("Limited supporting evidence")

        if document_consistency == 0:
            risk_factors.append("Document consistency issues")

        if not risk_factors:
            risk_factors.append("No major risk indicators identified")

        # ----------------------------------------------------
        # Missing information
        # ----------------------------------------------------
        missing_information = []

        if police_report == "No":
            missing_information.append("Police report not available")
        if vehicle_inspection == "No":
            missing_information.append("Vehicle inspection not available")
        if photos_available == "No":
            missing_information.append("Photographs not available")
        if witness_available == "No":
            missing_information.append("Witness statement not available")
        if cctv_available == "No":
            missing_information.append("CCTV evidence not available")

        if not missing_information:
            missing_information.append("Complete")

        risk_items_html = "".join(
            f'<div class="risk-item">{item}</div>' for item in risk_factors
        )
        missing_items_html = "".join(
            f'<div class="missing-item">{item}</div>' for item in missing_information
        )

        # ----------------------------------------------------
        # THINK10X-style result card
        # ----------------------------------------------------
        result_html = (
            '<div class="result-card">'
            '<div class="result-layout">'
            '<div>'
            f'<div class="score-ring" style="--score:{risk_score}; --risk-color:{risk_color};">'
            '<div class="score-inner">'
            f'<div class="score-number">{risk_score}</div>'
            '<div class="score-label">/100 RISK SCORE</div>'
            '</div></div>'
            '</div>'
            '<div>'
            f'<div class="risk-badge {badge_class}">{str(risk).upper()} RISK</div>'
            f'<div class="result-title">{str(risk).title()} Risk</div>'
            f'<div class="result-description">{description}</div>'
            '</div></div>'
            '<div class="result-columns">'
            '<div>'
            '<div class="result-section-title">RISK FACTORS</div>'
            f'{risk_items_html}'
            '</div>'
            '<div>'
            '<div class="result-section-title">MISSING INFORMATION</div>'
            f'{missing_items_html}'
            '</div></div>'
            '</div>'
        )

        st.markdown(result_html, unsafe_allow_html=True)

        st.session_state.last_risk_score = risk_score
        st.session_state.last_risk_factors = risk_factors
        st.session_state.last_missing_information = missing_information
        st.session_state.last_claim_id = claim_id
        st.session_state.last_policyholder = policyholder_name

        # ----------------------------------------------------
        # Generate report
        # ----------------------------------------------------
        st.write("")
        report_col, _ = st.columns([1, 4])
        with report_col:
            if st.button("📄 Generate Report", key="generate_risk_report"):
                report_lines = [
                    "INSURIX — INSURANCE RISK INTELLIGENCE",
                    "FORENSIC × INSURANCE",
                    "",
                    f"Claim ID: {claim_id}",
                    f"Policyholder: {policyholder_name}",
                    f"Incident Location: {incident_location}",
                    f"Incident Date: {incident_date}",
                    "",
                    "PRELIMINARY RISK ASSESSMENT",
                    f"Risk Level: {str(risk).upper()}",
                    f"Preliminary Risk Score: {risk_score}/100",
                    f"Model Confidence: {confidence:.2f}%",
                    "",
                    "RISK PROBABILITY",
                    f"High: {high_prob:.2f}%",
                    f"Medium: {medium_prob:.2f}%",
                    f"Low: {low_prob:.2f}%",
                    "",
                    "RISK FACTORS",
                ]
                report_lines.extend(f"- {item}" for item in risk_factors)
                report_lines.append("")
                report_lines.append("MISSING INFORMATION")
                report_lines.extend(f"- {item}" for item in missing_information)
                report_lines.extend([
                    "",
                    "DISCLAIMER:",
                    "This AI assessment is preliminary decision-support information. "
                    "It does not establish fraud or criminal activity. Final decisions "
                    "must be made by authorized insurance and forensic professionals."
                ])
                report_text = "\n".join(report_lines)

                st.download_button(
                    label="Download Risk Report",
                    data=report_text,
                    file_name=f"{claim_id or 'Insurix'}_Risk_Report.txt",
                    mime="text/plain",
                    key="download_risk_report"
                )

        # ----------------------------------------------------
        # AI probability breakdown
        # ----------------------------------------------------
        st.divider()
        st.subheader("AI Risk Probability")

        probability_cols = st.columns(3)

        with probability_cols[0]:
            st.metric("High", f"{high_prob:.2f}%")
            st.progress(min(max(high_prob / 100, 0.0), 1.0))

        with probability_cols[1]:
            st.metric("Medium", f"{medium_prob:.2f}%")
            st.progress(min(max(medium_prob / 100, 0.0), 1.0))

        with probability_cols[2]:
            st.metric("Low", f"{low_prob:.2f}%")
            st.progress(min(max(low_prob / 100, 0.0), 1.0))

        st.caption(
            "AI insights are preliminary and do not prove fraud or criminal activity. "
            "Final decisions belong to authorized professionals."
        )

        # ----------------------------------------------------
        # Recommended action
        # ----------------------------------------------------
        if risk_lower == "high":
            st.warning(
                "Recommended action: Prioritise the claim for further "
                "forensic and investigative review."
            )
        elif risk_lower == "medium":
            st.info(
                "Recommended action: Perform additional document and "
                "evidence verification before final claim processing."
            )
        else:
            st.success(
                "Recommended action: Continue normal claim review while "
                "maintaining standard evidence verification."
            )

        # ----------------------------------------------------
        # Feature importance
        # ----------------------------------------------------
        st.divider()
        st.subheader("Model Feature Importance")

        try:
            importance_df = pd.DataFrame(
                {"Feature": features, "Importance": model.feature_importances_}
            )
            importance_df = importance_df.sort_values(
                "Importance", ascending=False
            )
            importance_df["Importance (%)"] = (
                importance_df["Importance"] * 100
            ).round(2)
            st.dataframe(
                importance_df[["Feature", "Importance (%)"]],
                use_container_width=True,
                hide_index=True
            )
        except Exception:
            st.info("Feature importance is not available for this model.")

        # ----------------------------------------------------
        # Document result
        # ----------------------------------------------------
        if st.session_state.document_analysis:
            st.divider()
            st.subheader("Document Intelligence Summary")
            doc_result = st.session_state.document_analysis
            d1, d2, d3 = st.columns(3)

            with d1:
                st.metric(
                    "Amount Check",
                    "Passed" if doc_result["amount_consistent"] else "Needs Review"
                )
            with d2:
                st.metric(
                    "Date Check",
                    "Found" if doc_result["date_found"] else "Not Found"
                )
            with d3:
                st.metric(
                    "Supporting Evidence",
                    "Detected" if doc_result["evidence_found"] else "Limited"
                )

        st.divider()
        st.info(
            "Forensic interpretation: this output is a preliminary AI-assisted "
            "risk assessment. It should support, not replace, professional claim "
            "investigation and evidence review."
        )


# ============================================================
# DOCUMENTS PAGE
# ============================================================

elif st.session_state.page == "Documents":

    st.caption(
        "PUBLIC PORTAL / DOCUMENTS"
    )

    st.title("Documents")

    st.write(
        "Upload and review claim-related documents "
        "for preliminary document intelligence."
    )

    st.divider()


    # ========================================================
    # DOCUMENT UPLOAD
    # ========================================================

    st.subheader(
        "01  •  Claim Documentation"
    )


    uploaded_files = st.file_uploader(
        "Upload claim documents",
        accept_multiple_files=True,
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        key="documents_page_upload"
    )


    if uploaded_files:

        st.divider()

        st.subheader(
            "Uploaded Documents"
        )


        for file in uploaded_files:

            st.write(
                f"📄 {file.name}  •  "
                f"{file.size / 1024:.1f} KB"
            )


        st.success(
            f"{len(uploaded_files)} document(s) selected."
        )


        st.divider()


        st.subheader(
            "Document Review"
        )


        for file in uploaded_files:

            with st.expander(
                f"Analyse {file.name}"
            ):

                extracted_text = (
                    extract_text_from_document(
                        file
                    )
                )


                if extracted_text.startswith(
                    "DOCUMENT_ERROR"
                ):

                    st.error(
                        "Unable to read this document."
                    )

                    st.code(
                        extracted_text
                    )


                elif not extracted_text.strip():

                    st.warning(
                        "No readable text was extracted. "
                        "This may be a scanned image."
                    )


                else:

                    st.success(
                        "Readable text extracted successfully."
                    )


                    st.write(
                        f"Characters extracted: "
                        f"{len(extracted_text):,}"
                    )


                    with st.expander(
                        "View extracted text"
                    ):

                        st.text(
                            extracted_text[:10000]
                        )


    else:

        st.info(
            "No documents uploaded yet."
        )


    st.divider()


    # ========================================================
    # WORKFLOW
    # ========================================================

    st.subheader(
        "Document Intelligence Workflow"
    )


    workflow1, workflow2, workflow3 = (
        st.columns(3)
    )


    with workflow1:

        st.markdown("### 01")

        st.markdown("**Upload**")

        st.write(
            "Collect claim-related PDF, DOCX "
            "or TXT documents."
        )


    with workflow2:

        st.markdown("### 02")

        st.markdown("**Extract**")

        st.write(
            "Extract readable text and identify "
            "important claim information."
        )


    with workflow3:

        st.markdown("### 03")

        st.markdown("**Analyse**")

        st.write(
            "Check preliminary consistency and "
            "supporting evidence indicators."
        )


    st.divider()


    st.info(
        "Current document intelligence supports "
        "text-based PDF, DOCX and TXT files. "
        "OCR for scanned/image-only documents "
        "can be added as a future module."
    )


# ============================================================
# CLAIM STATUS PAGE
# ============================================================

elif st.session_state.page == "Claim Status":

    st.caption(
        "INSURIX WORKSPACE / CLAIM STATUS"
    )

    st.title("Claim Status")

    st.write(
        "Review the latest preliminary risk "
        "assessment generated during this session."
    )

    st.divider()


    if not st.session_state.assessment_done:

        st.info(
            "No claim assessment has been completed "
            "in this session yet."
        )


        if st.button(
            "Start Claim Assessment →",
            key="status_start"
        ):

            st.session_state.page = (
                "Claim Assessment"
            )

            st.rerun()


    else:

        risk = (
            st.session_state.last_risk
        )

        confidence = (
            st.session_state.last_confidence
        )

        risk_score = st.session_state.last_risk_score


        status_col1, status_col2, status_col3, status_col4 = (
            st.columns(4)
        )


        with status_col1:

            st.metric(
                "Risk Level",
                risk
            )


        with status_col2:

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )


        with status_col3:

            st.metric(
                "Risk Score",
                f"{risk_score}/100" if risk_score is not None else "—"
            )


        with status_col4:

            st.metric(
                "Model",
                "V4 Random Forest"
            )


        st.divider()


        risk_lower = risk.lower()


        if risk_lower == "high":

            st.error(
                "Current status: Further investigation "
                "recommended."
            )


        elif risk_lower == "medium":

            st.warning(
                "Current status: Additional verification "
                "recommended."
            )


        else:

            st.success(
                "Current status: Preliminary low-risk "
                "classification."
            )


        if risk_score is not None:
            st.info(
                f"Preliminary risk score: {risk_score}/100. "
                "This presentation score is derived from the model probability "
                "distribution and is not the same as model confidence."
            )


        st.divider()


        st.subheader(
            "Assessment Summary"
        )


        probabilities = (
            st.session_state.last_probabilities
        )


        for class_name, probability in (
            probabilities.items()
        ):

            st.write(
                f"**{class_name.title()} Risk:** "
                f"{probability:.2f}%"
            )


        st.divider()


        st.info(
            "This status represents a preliminary "
            "AI-assisted risk classification and "
            "does not constitute a final claim decision "
            "or a finding of fraud."
        )
