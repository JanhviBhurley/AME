import streamlit as st
from PIL import Image

st.set_page_config(page_title="Aircraft Maintenance App", layout="wide")

# Initialize page controller
if "page" not in st.session_state:
    st.session_state.page = "home"
    

# Load images from file
airbus_logo = Image.open("data/airbus.png")
boeing_logo = Image.open("data/boeing.png")


# Background styling
background_image_url = "https://flyxo.com/_next/image/?url=https%3A%2F%2Fwebsite-cdn.flyxo.com%2Fdata%2Fwebapi%2Fnew_plane_home_326d044e05.jpg&w=1920&q=80"
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .img-container img {{
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        transition: transform 0.3s;
    }}
    .img-container img:hover {{
        transform: scale(1.05);
    }}
    </style>
""", unsafe_allow_html=True)


# Title
st.markdown("<h1 style='text-align: center; color: white;'>✈️ Aircraft Maintenance Prediction</h1>", unsafe_allow_html=True)

if "selected_brand" not in st.session_state:
    st.markdown("<h1>Select Airbus or Boeing</h1>", unsafe_allow_html=True)

# Layout for Airbus and Boeing
col1, col2 = st.columns(2)

with col1:
    if st.button("Show Airbus Aircraft"):
        st.session_state.selected_brand = "Airbus"
        st.switch_page("pages/aircraft_list.py")
    with st.container():
        st.markdown('<div class="img-container">', unsafe_allow_html=True)
        st.image(airbus_logo, width=300)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if st.button("Show Boeing Aircraft"):
        st.session_state.selected_brand = "Boeing"
        st.switch_page("pages/aircraft_list.py")
    with st.container():
        st.markdown('<div class="img-container">', unsafe_allow_html=True)
        st.image(boeing_logo, width=300)
        st.markdown('</div>', unsafe_allow_html=True)

 