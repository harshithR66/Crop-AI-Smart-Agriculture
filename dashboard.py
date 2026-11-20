import streamlit as st
import requests

# ---------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="Crop AI | Smart Agriculture",
    page_icon="🌱",
    layout="wide"
)

API_URL = "https://crop-ai-smart-agriculture.onrender.com/predict"

# ---------------------------------
# 2. CUSTOM CSS
# ---------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.header {
    font-size: 42px;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #aaaaaa;
    font-size: 17px;
    margin-bottom: 35px;
}

.result-box {
    background-color: #173b28;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #4CAF50;
}

.crop-name {
    font-size: 38px;
    font-weight: bold;
    color: #7CFC98;
}

.section-title {
    color: #4CAF50;
    font-size: 23px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# 3. SIDEBAR
# ---------------------------------

st.sidebar.title("🌱 Crop AI")

st.sidebar.write("Smart Agriculture System")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Crop Prediction", "About Model"]
)

st.sidebar.divider()

st.sidebar.info(
    "AI-powered crop recommendation "
    "using Machine Learning."
)


# ---------------------------------
# 4. HOME PAGE
# ---------------------------------

if page == "Home":

    st.markdown(
        '<div class="header">🌱 Crop Suitability Prediction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Intelligent Crop Recommendation System'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("Welcome to Crop AI")

    st.write(
        """
        Crop AI uses Machine Learning to recommend
        suitable crops based on soil nutrients and
        environmental conditions.

        Enter your agricultural parameters to get
        an intelligent crop recommendation.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ML Algorithm", "Random Forest")

    with col2:
        st.metric("Input Parameters", "7")

    with col3:
        st.metric("Prediction Type", "Crop Selection")

    st.success(
        "Navigate to Crop Prediction to get started."
    )


# ---------------------------------
# 5. CROP PREDICTION PAGE
# ---------------------------------

elif page == "Crop Prediction":

    st.title("🌾 Crop Recommendation")

    st.write(
        "Enter your soil and weather parameters below."
    )

    st.divider()

    with st.form("crop_prediction_form"):

        col1, col2 = st.columns(2)

        # SOIL PARAMETERS

        with col1:

            st.subheader("🌱 Soil Parameters")

            N = st.number_input(
                "Nitrogen (N)",
                min_value=0.0,
                value=90.0
            )

            P = st.number_input(
                "Phosphorus (P)",
                min_value=0.0,
                value=42.0
            )

            K = st.number_input(
                "Potassium (K)",
                min_value=0.0,
                value=43.0
            )

            ph = st.number_input(
                "Soil pH",
                min_value=0.0,
                max_value=14.0,
                value=6.5
            )

        # WEATHER PARAMETERS

        with col2:

            st.subheader("🌤️ Weather Parameters")

            temperature = st.number_input(
                "Temperature (°C)",
                value=20.8
            )

            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=82.0
            )

            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                value=202.9
            )

        st.divider()

        submit = st.form_submit_button(
            "🌾 Recommend Suitable Crop",
            use_container_width=True
        )

    # ---------------------------------
    # 6. PREDICTION
    # ---------------------------------

    if submit:

        input_data = {

            "N": N,
            "P": P,
            "K": K,

            "temperature": temperature,
            "humidity": humidity,

            "ph": ph,
            "rainfall": rainfall
        }

        try:

            with st.spinner("Analyzing soil and weather conditions..."):

                response = requests.post(
                    API_URL,
                    json=input_data,
                    timeout=15
                )

            if response.status_code == 200:

                result = response.json()

                crop = result["recommended_crop"]

                confidence = result.get(
                    "confidence_score"
                )

                algorithm = result.get(
                    "algorithm",
                    "Random Forest"
                )

                st.divider()

                st.subheader("🎯 Prediction Results")

                st.markdown(
                    f"""
                    <div class="result-box">

                        <p style="color:white;font-size:20px;">
                            Recommended Crop
                        </p>

                        <div class="crop-name">
                            🌾 {crop.upper()}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")

                col1, col2 = st.columns(2)

                with col1:

                    if confidence is not None:

                        st.metric(
                            "Prediction Confidence",
                            f"{confidence}%"
                        )

                        st.progress(
                            max(0, min(100, float(confidence))) / 100
                        )

                with col2:

                    st.metric(
                        "ML Algorithm",
                        algorithm
                    )

                st.success(
                    "Crop recommendation generated successfully!"
                )

            else:

                st.error(
                    f"API Error: {response.text}"
                )

        except requests.exceptions.RequestException as e:

            st.error(
                f"Backend connection failed: {e}"
            )


# ---------------------------------
# 7. ABOUT MODEL PAGE
# ---------------------------------

elif page == "About Model":

    st.title("🤖 About the Machine Learning Model")

    st.write(
        """
        This project uses a Random Forest Classifier
        to recommend suitable crops.

        The model was trained using agricultural
        soil and weather parameters.
        """
    )

    st.subheader("Input Features")

    features = [
        "Nitrogen (N)",
        "Phosphorus (P)",
        "Potassium (K)",
        "Temperature",
        "Humidity",
        "Soil pH",
        "Rainfall"
    ]

    for feature in features:
        st.write("✔️", feature)

    st.divider()

    st.subheader("Model Information")

    st.write("Algorithm: Random Forest Classifier")

    st.write("Model File: crop_model.pkl")

    st.write("Backend: FastAPI")

    st.write("Frontend: Streamlit")
