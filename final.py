import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load the dataset with correct delimiter and remove quotes from column names
dataset = pd.read_csv("bank-additional-full.csv", sep=';')
dataset.columns = [col.strip('"') for col in dataset.columns]

# Ensure 'duration' is included in the dataset
dataset['duration'] = dataset['duration'].astype(int)  # Convert duration to integer if it's not

# Preprocess the data (this should be consistent with your previous preprocessing)
X = dataset.drop(['y'], axis=1)
y = dataset['y']

# Encode categorical variables as needed
X = pd.get_dummies(X, drop_first=True)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=1)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Logistic Regression Model
logreg = LogisticRegression(C=0.18420699693267145, random_state=0)
logreg.fit(X_train, y_train)

# Set the page configuration
st.set_page_config(page_title="CampaignInsight", layout="wide", page_icon=":bar_chart:")

# Subheader
st.subheader("Insights that Shape the Future of Bank Marketing")

# User input fields
age = st.number_input("Enter the client's age : ", min_value=0, step=1)
edu = st.selectbox("Enter the client's education : ", ['', 'university.degree', 'professional.course', 'high.school', 'basic.9y', 'basic.6y', 'basic.4y', 'illiterate', 'unknown'])
job = st.selectbox("Enter the client's job", ['', 'admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown'])
status = st.selectbox("Enter the client's status", ['', 'married', 'single', 'divorced', 'unknown'])
hloan = st.selectbox("Does the client have a housing loan?", ['', 'yes', 'no'])
ploan = st.selectbox("Does the client have a personal loan?", ['', 'yes', 'no'])
cloan = st.selectbox("Does the client have a credit loan?", ['', 'yes', 'no', 'unknown'])
duration = st.number_input("Enter the call duration with the client (seconds) : ", min_value=0, step=1)

# Define a mapping function for categorical features
def map_education(edu):
    mapping = {'university.degree': 1, 'professional.course': 2, 'high.school': 3, 'basic.9y': 4, 'basic.6y': 5, 'basic.4y': 6, 'illiterate': 7, 'unknown': 8}
    return mapping.get(edu, 0)

def map_job(job):
    mapping = {'admin.': 1, 'blue-collar': 2, 'entrepreneur': 3, 'housemaid': 4, 'management': 5, 'retired': 6, 'self-employed': 7, 'services': 8, 'student': 9, 'technician': 10, 'unemployed': 11, 'unknown': 12}
    return mapping.get(job, 0)

def map_status(status):
    mapping = {'married': 1, 'single': 2, 'divorced': 3, 'unknown': 4}
    return mapping.get(status, 0)

def map_binary(choice):
    mapping = {'yes': 1, 'no': 0}
    return mapping.get(choice, 0)

# Display output based on user inputs
if st.button("Submit"):
    # Determine the output based on duration and logistic regression model
    if duration >= 260:
        output = "yes"
    else:
        # Prepare the input data for logistic regression
        input_data = np.array([[age, map_education(edu), map_job(job), map_status(status), map_binary(hloan), map_binary(ploan), map_binary(cloan), duration]])
        input_data_df = pd.DataFrame(input_data, columns=['age', 'education', 'job', 'marital', 'housing', 'loan', 'default', 'duration'])
        
        # Encode categorical variables in input data
        input_data_df = pd.get_dummies(input_data_df, drop_first=True)
        
        # Ensure input data has the same columns as training data
        input_data_df = input_data_df.reindex(columns=X.columns, fill_value=0)
        
        # Standardize the input data
        input_data_scaled = scaler.transform(input_data_df)
        
        # Predict using the trained model
        prediction = logreg.predict(input_data_scaled)
        
        # Determine the output based on model prediction
        if prediction[0] == 1:
            output = "yes"
        else:
            output = "no"
    
    st.write(f"Will the client place the deposit? : {output}")