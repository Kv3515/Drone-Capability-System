import streamlit as st
import pandas as pd
from capability import calculate_platoon_capability

# Page configuration
st.set_page_config(page_title="Home - Drone Capability Calculator", layout="wide")

# Initialize session state for platoon
if "platoon" not in st.session_state:
    st.session_state.platoon = []

# Breadcrumb navigation
st.markdown("🏠 **Home**")
st.divider()

# Page title
st.title("🚁 Drone Capability Calculator")
st.markdown("**Command Overview Dashboard** - Real-time platoon capability summary")
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

# Navigation Cards Section
st.subheader("🗺️ Quick Navigation")

nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    if st.button("🚁 Platoon Capability", use_container_width=True, key="nav_platoon_btn", type="primary"):
        st.switch_page("pages/2_Platoon_Capability.py")

with nav_col2:
    if st.button("🎯 Mission Planner", use_container_width=True, key="nav_mission_btn", type="primary"):
        st.switch_page("pages/3_Mission_Planner.py")

st.divider()

# Information Section
st.write("""
## 📖 About This Application

The **Drone Capability Calculator** is a comprehensive tool for managing drone platoons and planning missions.

### Features

**Platoon Management:**
- Add and manage drones in your inventory
- Configure drone specifications (endurance, battery health, reliability)
- Set operational parameters (total drones, mission capable drones, battery sets)
- View real-time capability calculations by drone class
- Edit and delete drones from inventory

**Mission Planning:**
- Define mission parameters (type, duration, environmental conditions)
- Get optimal drone allocation recommendations
- Analyze mission feasibility and coverage
- Understand reserve margins for contingency

### How It Works

1. **Configure Your Platoon** - Add drones with their specifications
2. **Monitor Capabilities** - See real-time ISR hours available per drone class
3. **Plan Missions** - Use mission planner to allocate optimal drone combinations
4. **Analyze Results** - Review feasibility, coverage, and margins

### Key Metrics

- **Effective Endurance**: Base endurance adjusted for battery health and reliability
- **Mission Coverage**: Total available flight time for mission execution
- **Reserve Margin**: Additional coverage beyond mission requirements
- **Mission Feasible**: Whether the platoon can complete the mission

---

**Get started by managing your drone platoon in the "Platoon Capability" section.**
""")
