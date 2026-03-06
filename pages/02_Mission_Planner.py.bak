import streamlit as st
import pandas as pd
from capability import suggest_drone_allocation

# Page configuration
st.set_page_config(page_title="Mission Planner - Drone Capability Calculator", layout="wide")

# Initialize session state for platoon
if "platoon" not in st.session_state:
    st.session_state.platoon = []

# Breadcrumb navigation
breadcrumb_col1, breadcrumb_col2 = st.columns([0.1, 0.9])
with breadcrumb_col1:
    if st.button("🏠", key="breadcrumb_home", help="Go to Home"):
        st.switch_page("pages/1_Home.py")
with breadcrumb_col2:
    st.markdown("🏠 **Home** > 🎯 **Mission Planner**")

st.divider()

st.title("🎯 Mission Planner")
st.markdown("---")

st.write("""
Plan drone missions based on your current platoon inventory.
Configure mission parameters and get optimal drone allocation recommendations.
""")

st.divider()

# Mission Planning Section
st.subheader("Mission Planning and Drone Allocation")

# Create two-column layout for mission planning
left_col, right_col = st.columns([1, 2])

# LEFT COLUMN: Mission Parameters Input
with left_col:
    st.write("**Mission Parameters**")
    
    mission_type = st.selectbox(
        "Mission Type",
        ["Persistent ISR", "Tactical ISR", "Rapid Recon", "Micro Recon"],
        key="mission_type_select"
    )
    
    mission_duration_hours = st.slider(
        "Mission Duration (hours)",
        min_value=1,
        max_value=24,
        value=8,
        key="mission_duration_slider"
    )
    
    mission_condition = st.selectbox(
        "Mission Condition",
        ["Day", "Night"],
        key="mission_condition_select"
    )
    
    # Generate Mission Plan button
    generate_plan = st.button("Generate Mission Plan", use_container_width=True, type="primary")

# RIGHT COLUMN: Mission Planning Results
with right_col:
    if generate_plan:
        # Check if platoon has drones
        if not st.session_state.platoon:
            st.warning("⚠️ No drones available in platoon inventory. Please go to 'Platoon Capability' page to add drones.")
        else:
            # Generate mission plan using the suggestion function
            mission_plan = suggest_drone_allocation(mission_duration_hours, st.session_state.platoon)
            
            # Display status message
            if mission_plan["mission_feasible"]:
                st.success("✅ Mission FEASIBLE - Can be completed with current platoon resources!")
            else:
                shortfall = mission_plan['mission_minutes'] - mission_plan['total_coverage_minutes']
                st.warning(f"⚠️ Mission NOT FEASIBLE - Shortfall: {shortfall:.0f} minutes ({shortfall/60:.2f} hours)")
            
            # Display metrics
            results_col1, results_col2, results_col3, results_col4 = st.columns(4)
            
            with results_col1:
                st.metric(
                    "Mission Duration",
                    f"{mission_plan['mission_minutes'] / 60:.2f} hrs",
                    help="Required mission duration"
                )
            
            with results_col2:
                st.metric(
                    "Coverage Achieved",
                    f"{mission_plan['total_coverage_minutes'] / 60:.2f} hrs",
                    help="Total coverage from allocated drones"
                )
            
            with results_col3:
                st.metric(
                    "Reserve Margin",
                    f"{mission_plan['remaining_margin']:.0f} min",
                    help="Extra coverage beyond mission requirement"
                )
            
            with results_col4:
                feasible_text = "✅ YES" if mission_plan["mission_feasible"] else "❌ NO"
                st.metric(
                    "Mission Feasible",
                    feasible_text,
                    help="Can the mission be completed?"
                )
            
            # Display recommended drone allocation
            st.markdown("---")
            st.markdown("**Recommended Drone Allocation**")
            
            if mission_plan["allocation"]:
                allocation_data = []
                for drone_allocation in mission_plan["allocation"]:
                    allocation_data.append({
                        "Drone Name": drone_allocation["drone_name"],
                        "Drone Class": drone_allocation["drone_class"],
                        "Contribution (hrs)": f"{drone_allocation['contribution_hours']:.2f}",
                        "Effective Endurance (min)": f"{drone_allocation['effective_endurance_minutes']:.0f}",
                        "Battery Sets": drone_allocation["battery_sets"]
                    })
                
                allocation_df = pd.DataFrame(allocation_data)
                st.dataframe(allocation_df, use_container_width=True, hide_index=True)
            else:
                st.info("No drones allocated for this mission.")
            
            # Display mission summary
            st.markdown("---")
            st.markdown("**Mission Summary**")
            
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.info(f"""
                **Mission Parameters:**
                - Type: {mission_type}
                - Duration: {mission_duration_hours} hours
                - Condition: {mission_condition}
                """)
            
            with summary_col2:
                st.info(f"""
                **Coverage Analysis:**
                - Total Coverage: {mission_plan['total_coverage_minutes'] / 60:.2f} hours
                - Reserve Margin: {mission_plan['remaining_margin']:.0f} minutes
                - Drones Allocated: {len(mission_plan['allocation'])}
                - Status: {"✅ FEASIBLE" if mission_plan['mission_feasible'] else "❌ NOT FEASIBLE"}
                """)
    else:
        st.info("👈 Configure mission parameters and click 'Generate Mission Plan' to see results here.")
