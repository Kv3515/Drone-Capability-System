import streamlit as st
import pandas as pd
from capability import calculate_platoon_capability

# Page configuration
st.set_page_config(page_title="Drone Capability Calculator", layout="wide")

# Progressive Web App (PWA) Configuration
# Inject manifest link and meta tags for PWA support
st.markdown(
    """
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#0E1117">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="DroneOps">
    <script>
        // Register service worker for offline support and caching
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

st.title("🚁 Drone Capability Calculator")
st.markdown("---")

st.write("**Command Overview Dashboard** - Real-time platoon capability summary")
st.divider()

# Calculate platoon capabilities
if st.session_state.platoon:
    capabilities = calculate_platoon_capability(st.session_state.platoon)
else:
    capabilities = {
        "Persistent ISR": 0.0,
        "Tactical ISR": 0.0,
        "Rapid Recon": 0.0,
        "Micro Recon": 0.0
    }

# Display four capability cards using columns and metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    persistent_hours = capabilities["Persistent ISR"] / 60
    st.metric(
        "🛸 Persistent ISR",
        f"{persistent_hours:.1f} hrs",
        help="Total continuous ISR capability"
    )

with col2:
    tactical_hours = capabilities["Tactical ISR"] / 60
    st.metric(
        "🚁 Tactical ISR",
        f"{tactical_hours:.1f} hrs",
        help="Tactical ISR capability"
    )

with col3:
    rapid_hours = capabilities["Rapid Recon"] / 60
    st.metric(
        "⚡ Rapid Recon",
        f"{rapid_hours:.1f} hrs",
        help="Rapid reconnaissance capability"
    )

with col4:
    micro_hours = capabilities["Micro Recon"] / 60
    st.metric(
        "🎯 Micro Recon",
        f"{micro_hours:.1f} hrs",
        help="Micro reconnaissance capability"
    )

st.divider()

# Capability Visualization Section
st.subheader("📊 Capability Distribution by Drone Class")

# Prepare data for bar chart
capability_data = pd.DataFrame({
    "Drone Class": list(capabilities.keys()),
    "Capability (hours)": [v / 60 for v in capabilities.values()]
})

# Display bar chart
st.bar_chart(capability_data.set_index("Drone Class"))

st.divider()

st.write("""
## 📖 Getting Started

### 1. **Platoon Capability** (Manage Your Drones)
Go to the **Platoon Capability** page to:
- Add drones to your platoon inventory
- Configure drone specifications (endurance, battery health, reliability)
- Edit and manage operational parameters
- View real-time capability calculations by drone class
- See total ISR hours available for each drone type

### 2. **Mission Planner** (Plan Your Missions)
Go to the **Mission Planner** page to:
- Define mission parameters (type, duration, conditions)
- Get optimal drone allocation recommendations
- See mission feasibility and coverage analysis
- Understand reserve margins and coverage capacity

---
**Start by navigating to the Platoon Capability page using the sidebar menu.**
""")




