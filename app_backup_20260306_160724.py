import streamlit as st

# Page configuration
st.set_page_config(page_title="Drone Capability Calculator", layout="wide")

# Initialize session state for platoon
if "platoon" not in st.session_state:
    st.session_state.platoon = []

st.title("🚁 Drone Capability Calculator")
st.markdown("---")

st.write("""
Welcome to the Drone Capability Calculator! This application helps you:
- **Build and manage** your drone platoon inventory
- **Calculate** capability metrics for each drone class
- **Plan missions** and get optimal drone allocation recommendations

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

## 🎯 How It Works

1. **Add Drones**: Start by building your platoon in the Platoon Capability page
2. **Configure Parameters**: Set up drone specifications and operational constraints
3. **Plan Missions**: Use the Mission Planner to allocate drones for specific mission requirements
4. **Analyze Results**: Review coverage, feasibility, and margins for decision making

## 📊 Key Metrics

- **Effective Endurance**: Base endurance adjusted for battery health and reliability
- **Mission Coverage**: Total available flight time for mission execution
- **Reserve Margin**: Additional coverage beyond mission requirements
- **Mission Feasible**: Whether the platoon can complete the mission

---
**Start by navigating to the Platoon Capability page using the sidebar menu.**
""")




