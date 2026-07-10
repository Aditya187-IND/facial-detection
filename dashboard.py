import streamlit as st
import cv2
import numpy as np

# --- 1. Dashboard UI Setup ---
st.set_page_config(page_title="Feature Matcher API", layout="centered")

st.title("🔍 Biometric Feature Matcher")
st.write("Upload two images (faces, eyes, lips, etc.) to calculate their matching percentage.")

# Create two columns for the upload buttons
col1, col2 = st.columns(2)

with col1:
    image1_file = st.file_uploader("Upload First Image", type=['jpg', 'jpeg', 'png'])
    if image1_file is not None:
        st.image(image1_file, caption="Input 1", use_container_width=True)

with col2:
    image2_file = st.file_uploader("Upload Second Image", type=['jpg', 'jpeg', 'png'])
    if image2_file is not None:
        st.image(image2_file, caption="Input 2", use_container_width=True)


# --- 2. Processing Logic ---
def process_image(uploaded_file):
    """Converts a web file upload into an OpenCV grayscale image."""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

# Only run the calculation if BOTH images are uploaded
if image1_file and image2_file:
    st.divider()
    st.subheader("Analysis Results")
    
    with st.spinner("Analyzing keypoints..."):
        # Convert web uploads to OpenCV format
        img1 = process_image(image1_file)
        img2 = process_image(image2_file)

        # Initialize ORB
        orb = cv2.ORB_create()

        # Find keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        if des1 is None or des2 is None:
            st.error("Could not detect enough features in one or both images.")
        else:
            # Brute-Force Matcher
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            
            # Match Percentage Calculation
            max_keypoints = max(len(kp1), len(kp2))
            if max_keypoints > 0:
                match_percentage = (len(matches) / max_keypoints) * 100
                similarity = round(match_percentage, 2)
                
                # Display Results beautifully
                st.metric(label="Match Percentage", value=f"{similarity}%")
                
                if similarity > 15.0:
                    st.success("✅ System Decision: MATCH")
                else:
                    st.error("❌ System Decision: NO MATCH")