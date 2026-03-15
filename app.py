import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os

MODEL_PATH = "model_trojmiasto.pkl"

# Load model
def load_model():
    return joblib.load(MODEL_PATH)

# Sidebar input
def user_input():
    st.sidebar.header("Apartment parameters")
    city = st.sidebar.selectbox("City", ["Gdansk", "Gdynia", "Sopot"])
    area = st.sidebar.number_input("Area (m²)", min_value=10.0, max_value=300.0, value=50.0, step=1.0)
    rooms = st.sidebar.number_input("Number of rooms", min_value=1, max_value=10, value=2, step=1)
    # Optionally, allow image upload (not used in prediction)
    st.sidebar.file_uploader("Upload photo (optional)", type=["jpg", "jpeg", "png"])
    return {"city": city.lower(), "area": area, "rooms": rooms}

# Main app
def main():
    st.title("Trójmiasto Apartment Price Predictor")
    st.write("Enter apartment details to estimate the price.")
    model = load_model()
    user_data = user_input()
    # Prepare input for model
    input_df = pd.DataFrame([{
        "city": user_data["city"],
        "area": user_data["area"],
        "rooms": user_data["rooms"],
        "price_per_m2": user_data["area"],  # Placeholder, not used in prediction
        "area_per_room": user_data["area"] / user_data["rooms"]
    }])
    if st.button("Calculate price"):
        price_pred = model.predict(input_df)[0]
        st.success(f"Estimated price: {int(price_pred):,} zł")
        # Comparison plot
        df = pd.read_csv("data/mieszkania_trojmiasto_clean.csv")
        fig = px.histogram(df[df["city"] == user_data["city"]], x="price", nbins=30, title=f"Price distribution in {user_data['city'].capitalize()}")
        fig.add_vline(x=price_pred, line_dash="dash", line_color="red", annotation_text="Your estimate", annotation_position="top right")
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
