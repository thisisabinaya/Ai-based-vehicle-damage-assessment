import streamlit as st
import os
import hashlib
import uuid

# Insurance amount mapping (fake damage types)
damage_costs = {
    "scratch": 1000,
    "dents": 2000,
    "torn": 3000,
    "punctured": 2500
}

# Function to create a consistent hash from the image
def get_image_hash(image_path):
    # Open the image to generate a hash
    with open(image_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# Streamlit UI
st.title("🚗 Vehicle Damage Detection & Insurance Estimation")

uploaded_file = st.file_uploader("Upload an image of the vehicle", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    # Save uploaded image
    UPLOAD_FOLDER = "uploads"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    unique_name = str(uuid.uuid4()) + ".jpg"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Generate a consistent hash for the uploaded image
    image_hash = get_image_hash(file_path)

    # Check if we already have a prediction for this image (simulating storage)
    if st.session_state.get(image_hash):
        total_cost = st.session_state[image_hash]
    else:
        # Pick a random amount from the damage costs (no damage prediction)
        total_cost = 1000  # You can modify this to any constant value for fake amount

        # Store the predicted amount for this image so it stays the same after reloading
        st.session_state[image_hash] = total_cost

    # Show the fake prediction
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Show output
    st.markdown(f"### 💰 Estimated Insurance Claim Amount: ₹{total_cost}")
