import streamlit as st
import joblib
import pandas as pd
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Forensic Insurance Risk Assessment",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🛡️ Forensic Insurance Risk Assessment")
st.markdown(
    "### AI-Based Insurance Claim Risk Classification"
)

st.info(
    "Enter the claim details below. The trained Version 4 "
    "Random Forest model will classify the claim risk."
)

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

    # V4 model is stored as a dictionary
    if not isinstance(data, dict):
        raise TypeError(
            "The V4 model file does not contain the expected dictionary."
        )

    required_keys = ["model", "label_encoder", "features"]

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

    st.success("✅ Version 4 ML model loaded successfully!")

except Exception as e:
    st.error("❌ Unable to load the trained ML model.")
    st.error(str(e))
    st.stop()


# ============================================================
# DISPLAY MODEL INFORMATION
# ============================================================

with st.expander("🔍 Model Information"):
    st.write("**Model:** Random Forest Classifier")
    st.write("**Version:** 4")
    st.write("**Features used by model:**")

    for feature in features:
        st.write(f"- {feature}")


# ============================================================
# INPUT SECTION
# ============================================================

st.header("📋 Insurance Claim Details")

col1, col2 = st.columns(2)

with col1:

    claim_amount = st.number_input(
        "Claim Amount",
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
        options=["No", "Yes"]
    )

    document_consistency = st.selectbox(
        "Document Consistency",
        options=["No", "Yes"]
    )

    claim_after_policy = st.selectbox(
        "Claim After Policy",
        options=["No", "Yes"]
    )


# ============================================================
# CONVERT YES / NO TO NUMERIC
# ============================================================

evidence_status_value = 1 if evidence_status == "Yes" else 0

document_consistency_value = (
    1 if document_consistency == "Yes" else 0
)

claim_after_policy_value = (
    1 if claim_after_policy == "Yes" else 0
)


# ============================================================
# CREATE INPUT DATA
# ============================================================

input_values = {
    "claim_amount": claim_amount,
    "previous_claims": previous_claims,
    "rejected_claims": rejected_claims,
    "claim_frequency": claim_frequency,
    "evidence_status": evidence_status_value,
    "document_consistency": document_consistency_value,
    "claim_after_policy": claim_after_policy_value
}


# ============================================================
# PREPARE DATA ACCORDING TO TRAINED FEATURE ORDER
# ============================================================

try:

    # Make sure the exact feature order used during training
    # is maintained.

    input_data = pd.DataFrame(
        [[input_values[feature] for feature in features]],
        columns=features
    )

except KeyError as e:

    st.error(
        f"❌ Feature mismatch: {e}"
    )

    st.write(
        "Features stored in model:",
        features
    )

    st.stop()


# ============================================================
# SHOW INPUT DATA
# ============================================================

with st.expander("📊 View Model Input Data"):

    st.dataframe(
        input_data,
        use_container_width=True
    )


# ============================================================
# PREDICTION BUTTON
# ============================================================

st.markdown("---")

predict_button = st.button(
    "🔎 Assess Insurance Risk",
    type="primary",
    use_container_width=True
)


# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    try:

        # ----------------------------------------------------
        # MAKE PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(input_data)

        # Convert encoded prediction back to original label
        risk_level = label_encoder.inverse_transform(
            prediction
        )[0]

        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------

        st.markdown("---")

        st.header("📌 Risk Assessment Result")

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            st.metric(
                "Predicted Risk Level",
                str(risk_level).upper()
            )

        # ----------------------------------------------------
        # PROBABILITY
        # ----------------------------------------------------

        with result_col2:

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(
                    input_data
                )[0]

                classes = model.classes_

                # Find probability corresponding to prediction
                predicted_class = prediction[0]

                probability = 0.0

                for i, class_value in enumerate(classes):

                    if class_value == predicted_class:
                        probability = probabilities[i] * 100
                        break

                st.metric(
                    "Prediction Confidence",
                    f"{probability:.2f}%"
                )

        # ----------------------------------------------------
        # RISK INTERPRETATION
        # ----------------------------------------------------

        risk_text = str(risk_level).lower()

        if "high" in risk_text:

            st.error(
                "🚨 HIGH RISK CLAIM\n\n"
                "The claim shows characteristics associated "
                "with a higher insurance risk level. "
                "Further investigation and verification "
                "may be recommended."
            )

        elif "medium" in risk_text:

            st.warning(
                "⚠️ MEDIUM RISK CLAIM\n\n"
                "The claim shows characteristics associated "
                "with moderate insurance risk. "
                "Additional verification may be appropriate."
            )

        elif "low" in risk_text:

            st.success(
                "✅ LOW RISK CLAIM\n\n"
                "The claim shows characteristics associated "
                "with a lower insurance risk level."
            )

        else:

            st.info(
                f"Predicted risk category: {risk_level}"
            )


        # ====================================================
        # PROBABILITY BREAKDOWN
        # ====================================================

        if hasattr(model, "predict_proba"):

            st.subheader("📈 Risk Probability Breakdown")

            probability_data = []

            for i, class_value in enumerate(classes):

                probability_data.append({
                    "Risk Category": str(
                        label_encoder.inverse_transform(
                            [class_value]
                        )[0]
                    ),
                    "Probability (%)": round(
                        probabilities[i] * 100,
                        2
                    )
                })

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


        # ====================================================
        # FEATURE IMPORTANCE
        # ====================================================

        if hasattr(model, "feature_importances_"):

            st.subheader("📊 Feature Importance")

            importance_df = pd.DataFrame({
                "Feature": features,
                "Importance": model.feature_importances_
            })

            importance_df = importance_df.sort_values(
                by="Importance",
                ascending=False
            )

            importance_df["Importance"] = (
                importance_df["Importance"].round(4)
            )

            st.dataframe(
                importance_df,
                use_container_width=True,
                hide_index=True
            )

            st.bar_chart(
                importance_df.set_index("Feature")
            )


    except Exception as e:

        st.error(
            "❌ Prediction failed."
        )

        st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Forensic Insurance Risk AI • Version 4 • "
    "Random Forest Classification"
)
