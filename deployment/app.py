# Temporary comment to force upload
import os, json, pickle
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download

# Set page config as the first Streamlit command
st.set_page_config(page_title='Tourism Package Predictor', page_icon='✈️', layout='wide')

HF_MODEL_REPO = os.getenv('HF_MODEL_REPO', '<YOUR_HF_USERNAME>/tourism-model')

@st.cache_resource
def load_model():
    model_path    = hf_hub_download(repo_id=HF_MODEL_REPO, filename='best_model.pkl')
    features_path = hf_hub_download(repo_id=HF_MODEL_REPO, filename='feature_columns.json')
    with open(model_path, 'rb') as f:    model = pickle.load(f)
    with open(features_path, 'r') as f:  feature_cols = json.load(f)
    return model, feature_cols

model, feature_cols = load_model()

st.title('✈️  Wellness Tourism Package Purchase Predictor')
st.markdown('Fill in the customer details below to predict whether they will purchase the package.')

with st.form('prediction_form'):
    col1, col2 = st.columns(2)
    with col1:
        age            = st.number_input('Age', min_value=18, max_value=100, value=35)
        monthly_income = st.number_input('Monthly Income (INR)', min_value=0, value=50000, step=1000)
        num_trips      = st.number_input('Number of Trips per Year', min_value=0, value=2)
        pitch_score    = st.slider('Pitch Satisfaction Score', 1, 5, 3)
        num_followups  = st.number_input('Number of Follow-ups', min_value=0, value=3)
        duration_pitch = st.number_input('Duration of Pitch (min)', min_value=0, value=15)
    with col2:
        num_visiting   = st.number_input('Persons Visiting', min_value=1, value=2)
        num_children   = st.number_input('Children Visiting (under 5)', min_value=0, value=0)
        city_tier      = st.selectbox('City Tier', [1, 2, 3])
        preferred_star = st.selectbox('Preferred Hotel Stars', [3, 4, 5])
        passport       = st.selectbox('Has Passport?', [0, 1], format_func=lambda x: 'Yes' if x else 'No')
        own_car        = st.selectbox('Owns Car?', [0, 1], format_func=lambda x: 'Yes' if x else 'No')
    submitted = st.form_submit_button('Predict')

if submitted:
    raw = {
        'Age': age, 'MonthlyIncome': monthly_income, 'NumberOfTrips': num_trips,
        'PitchSatisfactionScore': pitch_score, 'NumberOfFollowups': num_followups,
        'DurationOfPitch': duration_pitch, 'NumberOfPersonVisiting': num_visiting,
        'NumberOfChildrenVisiting': num_children, 'CityTier': city_tier,
        'PreferredPropertyStar': preferred_star, 'Passport': passport, 'OwnCar': own_car,
    }
    input_df = pd.DataFrame([raw]).reindex(columns=feature_cols, fill_value=0)
    prediction = model.predict(input_df)[0]
    proba      = model.predict_proba(input_df)[0][1]
    st.markdown('---')
    if prediction == 1:
        st.success(f'Customer is LIKELY to purchase — Probability: {proba:.1%}')
    else:
        st.warning(f'Customer is UNLIKELY to purchase — Probability: {proba:.1%}')

st.markdown('---')
st.caption('Visit with Us | Wellness Tourism Package Predictor | MLOps Project')
