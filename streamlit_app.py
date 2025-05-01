import streamlit as st
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Set page config
st.set_page_config(
    page_title="Stroke Prediction App",
    page_icon="🏥",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("Stroke Prediction App")
st.markdown("""
This application predicts the likelihood of a stroke based on various health parameters.
Please fill in the details below to get a prediction.
""")

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    bmi = st.number_input("BMI", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
    avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, max_value=300.0, value=100.0, step=0.1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    ever_married = st.selectbox("Ever Married", ["Yes", "No"])

with col2:
    residence_type = st.selectbox("Residence Type", ["Urban", "Rural"])
    work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"])
    smoking_status = st.selectbox("Smoking Status", ["formerly smoked", "never smoked", "smokes", "Unknown"])
    hypertension = st.selectbox("Hypertension", ["Yes", "No"])
    heart_disease = st.selectbox("Heart Disease", ["Yes", "No"])

# Convert Yes/No to 1/0
hypertension = 1 if hypertension == "Yes" else 0
heart_disease = 1 if heart_disease == "Yes" else 0

# Prediction button
if st.button("Predict Stroke Risk"):
    try:
        # Create custom data object
        data = CustomData(
            age=age,
            bmi=bmi,
            avg_glucose_level=avg_glucose_level,
            gender=gender,
            ever_married=ever_married,
            Residence_type=residence_type,
            work_type=work_type,
            smoking_status=smoking_status,
            hypertension=hypertension,
            heart_disease=heart_disease
        )

        # Get prediction
        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        
        # Display results
        if results[0] == 1:
            st.error("⚠️ High Risk of Stroke")
            st.markdown("""
            Based on the provided information, there is a high risk of stroke.
            Please consult with a healthcare professional for further evaluation.
            """)
        else:
            st.success("✅ Low Risk of Stroke")
            st.markdown("""
            Based on the provided information, there is a low risk of stroke.
            However, it's always good to maintain a healthy lifestyle and regular check-ups.
            """)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>This is a prediction tool and should not be used as a substitute for professional medical advice.</p>
    </div>
    """, unsafe_allow_html=True) 