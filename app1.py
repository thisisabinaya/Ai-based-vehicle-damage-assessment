import streamlit as st
import pandas as pd
import os
import random
import ast
from PIL import Image

# Constants
CSV_PATH = r"D:\dataset\annotations\train_annotations_updated.csv"

# Mapping damage class to severity
DAMAGE_SEVERITY_MAP = {
    'scratch': 'Low',
    'dent': 'Medium',
    'broken glass': 'High',
    'broken lights': 'High',
    'punctured': 'Medium',
    'torn': 'High',
    'lost parts': 'High',
}

# Random insurance generator
def generate_insurance_amount(severity_level):
    if severity_level == 'Low':
        return random.randint(5000, 10000)
    elif severity_level == 'Medium':
        return random.randint(10000, 25000)
    elif severity_level == 'High':
        return random.randint(25000, 50000)
    else:
        return 0

def polygon_area(coords):
    x = [pt[0] for pt in coords]
    y = [pt[1] for pt in coords]
    return 0.5 * abs(sum(x[i] * y[(i+1)%len(coords)] - x[(i+1)%len(coords)] * y[i] for i in range(len(coords))))

# Load annotations
@st.cache_data
def load_annotations():
    return pd.read_csv(CSV_PATH)

# UI Setup
st.set_page_config(page_title="Damage Estimator", layout="centered")
st.title("🚗 Vehicle Damage Detection & Insurance Estimator")
st.write("Upload an image to simulate AI-based damage analysis and insurance calculation.")

# Load CSV
df = load_annotations()

# Upload image
uploaded_file = st.file_uploader("📂 Upload a damage image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption=uploaded_file.name, use_column_width=True)

    filename = uploaded_file.name

    # Search for this image filename in CSV
    damage_info = df[df['filename'] == filename]

    if damage_info.empty:
        st.error("No annotation found for this image.")
    else:
        try:
            polygon_str = damage_info['polygon'].values[0]
            polygon = ast.literal_eval(polygon_str)
            area = polygon_area(polygon)
            max_area = 2000000
            severity_score = round(min(area / max_area, 1.0), 2)
        except Exception as e:
            st.warning(f"Polygon parsing failed: {e}")
            severity_score = 0.0

        damage_type = damage_info['class'].values[0]
        severity_label = DAMAGE_SEVERITY_MAP.get(damage_type.lower(), "Unknown")

        if severity_label == "Unknown":
            insurance_amount = round(severity_score * 50000 + random.randint(-1000, 1000), -2)
        else:
            insurance_amount = generate_insurance_amount(severity_label)

        # Display predictions
        st.success("✅ Prediction Complete!")
        st.markdown(f"**Damage Type:** `{damage_type}`")
        st.markdown(f"**Severity Level:** `{severity_label}`")
        st.markdown(f"**Severity Score (based on area):** `{severity_score}`")
        st.markdown(f"**💰 Estimated Insurance Amount:** ₹ `{insurance_amount}`")

        # Debug Info
        with st.expander("📄 Debug Info"):
            st.write("Polygon Points:", polygon)
            st.write("Calculated Area:", area)
