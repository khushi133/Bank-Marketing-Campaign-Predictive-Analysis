import streamlit as st

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obesity"

# Streamlit UI
st.title("BMI Calculator")

weight_placeholder = st.empty()
height_placeholder = st.empty()
calculate_button = st.empty()

weight = weight_placeholder.text_input("Enter your weight (kg)")
height = height_placeholder.text_input("Enter your height (m)")

if calculate_button.button("Calculate BMI"):
    try:
        weight = float(weight)
        height = float(height)
        bmi = calculate_bmi(weight, height)
        interpretation = interpret_bmi(bmi)
        st.success(f"Your BMI is: {bmi:.2f}")
        st.info(f"Interpretation: {interpretation}")
    except ValueError:
        st.error("Please enter valid numeric values for weight and height.")
