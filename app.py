import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Drone Capability Calculator",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Progressive Web App (PWA) Configuration
st.markdown(
    """
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#0E1117">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="DroneOps">
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/service-worker.js').then(registration => {
                console.log('Service Worker registered:', registration);
            }).catch(error => {
                console.log('Service Worker registration failed:', error);
            });
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Initialize session state for platoon
if "platoon" not in st.session_state:
    st.session_state.platoon = []

# Application title and branding
st.set_page_config(page_title="Drone Capability Calculator", page_icon="🚁")
st.title("🚁 Drone Capability Calculator")




