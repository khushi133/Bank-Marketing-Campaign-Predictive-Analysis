import streamlit as st
import pickle

st.set_page_config(page_title="CampaignInsight", layout="wide", page_icon=":bar_chart:")

# Set the background image and text color
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url('https://img.freepik.com/premium-photo/gold-chart-point-target-business-concept-3d-rendering_35719-14385.jpg?uid=R63502277&ga=GA1.1.901531248.1712928952&semt=ais_hybrid');
    background-size: cover; /* Cover the entire viewport */
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stAppViewContainer"] .block-container {
    color: #FFFFFF; /* Set text color to white */
}
[data-testid="stAppViewContainer"] .css-1v0mbdj {
    color: #FFFFFF; /* Set title and other text color to white */
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

# Load the pre-trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Function to make predictions
def predict_subscription(job, education, default, day_of_week, dummy_telephone, dummy_nonexistent, dummy_success, marital_ordinal, age, duration, campaign, previous, cons_conf_idx, euribor3m, nr_employed):
    prediction = model.predict([[job, education, default, day_of_week, dummy_telephone, dummy_nonexistent, dummy_success, marital_ordinal, age, duration, campaign, previous, cons_conf_idx, euribor3m, nr_employed]])
    return prediction

# Define the Streamlit app
def main():
    # Set the title of the app
    st.title('Customer Subscription Prediction')
    
    # Add some instructions for the user
    st.write('Please enter the required information to predict customer subscription.')
    
    # Add input fields for user data
    age = st.slider('Age', min_value=10, step=1, max_value=100)
    job = st.selectbox('Job', ['entrepreneur', 'technician', 'retired', 'services', 'blue-collar', 'admin.', 'self-employed', 'management', 'student', 'housemaid', 'unemployed', 'other'])
    education = st.selectbox('Education', ['tertiary', 'secondary', 'primary'])
    default = st.selectbox('Credit in Default(any unpaind loan)', ['no', 'yes'])
    day_of_week = st.selectbox('Day of Week', ['mon', 'tue', 'wed', 'thu', 'fri'])
    dummy_telephone = st.selectbox('Telephone', ['no', 'yes'])
    dummy_nonexistent = st.selectbox('Non-existent Contact', ['no', 'yes'])
    dummy_success = st.selectbox('Success Contact', ['no', 'yes'])
    marital_ordinal = st.selectbox('Marital Status', ['single', 'married', 'divorced'])
    duration = st.number_input('Duration', min_value=0)
    campaign = st.number_input('Campaign', min_value=0)
    previous = st.number_input('Contacts performed', min_value=0, step=1, max_value=30)
    cons_conf_idx = st.number_input('Consumer Confidence Index', min_value=-50.0, step=0.1)
    euribor3m = st.number_input('Euribor 3 Month Rate', min_value=0.0, step=0.01)
    nr_employed = st.number_input('Number of Employees', min_value=1000, step=10)

    # Convert categorical variables to numerical encoding
    job_encoded = ['entrepreneur', 'technician', 'retired', 'services', 'blue-collar', 'admin.', 'self-employed', 'management', 'student', 'housemaid', 'unemployed', 'other'].index(job)
    education_encoded = ['tertiary', 'secondary', 'primary'].index(education)
    default_encoded = ['no', 'yes'].index(default)
    day_of_week_encoded = ['mon', 'tue', 'wed', 'thu', 'fri'].index(day_of_week)
    dummy_telephone_encoded = ['no', 'yes'].index(dummy_telephone)
    dummy_nonexistent_encoded = ['no', 'yes'].index(dummy_nonexistent)
    dummy_success_encoded = ['no', 'yes'].index(dummy_success)
    marital_ordinal_encoded = ['single', 'married', 'divorced'].index(marital_ordinal)

    # When the user clicks the predict button
    if st.button('Predict'):
        # Make prediction
        prediction = predict_subscription(
            job_encoded, education_encoded, default_encoded, day_of_week_encoded,
            dummy_telephone_encoded, dummy_nonexistent_encoded, dummy_success_encoded,
            marital_ordinal_encoded, age, duration, campaign, previous, cons_conf_idx,
            euribor3m, nr_employed
        )
        
        # Display the prediction to the user
        if prediction[0] == 1:
            st.write(f'### The customer is likely to take the loan.')
        else:
            st.write(f'### The customer is unlikely to take the loan.')

if __name__ == "__main__":
    main()