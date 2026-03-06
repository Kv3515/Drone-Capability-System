import streamlit as st
import pandas as pd
from capability import calculate_drone_capability, calculate_platoon_capability, suggest_drone_allocation
from drone import Drone

# Page configuration
st.set_page_config(page_title="Drone Capability Calculator", layout="wide")

# Initialize session state for platoon
if "platoon" not in st.session_state:
    st.session_state.platoon = []

st.title("🚁 Drone Capability Calculator")
st.markdown("---")

# Create two columns for input layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Drone Configuration")
    
    # Drone Name dropdown
    drone_name = st.selectbox(
        "Drone Name",
        ["Switch UAV", "Tunga", "DJI Air 3S", "DJI Mavic 2 Enterprise", "Black Hornet"]
    )
    
    # Drone Class dropdown
    drone_class = st.selectbox(
        "Drone Class",
        ["Persistent ISR", "Tactical ISR", "Rapid Recon", "Micro Recon"]
    )
    
    # Base Endurance dropdown (in minutes)
    base_endurance_minutes = st.selectbox(
        "Base Endurance (minutes)",
        [15, 20, 30, 45, 60, 90, 120],
        index=4  # Default to 60 minutes
    )
    # Convert to hours
    base_endurance = base_endurance_minutes / 60
    
    # Battery Health slider
    battery_health = st.slider(
        "Battery Health (0-1)",
        min_value=0.5,
        max_value=1.0,
        value=0.9,
        step=0.05
    )
    
    # Reliability dropdown
    reliability = st.selectbox(
        "Reliability",
        [1.0, 0.9, 0.8, 0.7],
        index=1  # Default to 0.9
    )

with col2:
    st.subheader("Operational Parameters")
    
    # Total Drones slider
    total_drones = st.slider(
        "Total Drones Available",
        min_value=1,
        max_value=10,
        value=5
    )
    
    # Mission Capable Drones slider
    mission_capable = st.slider(
        "Mission Capable Drones",
        min_value=0,
        max_value=10,
        value=4
    )
    
    # Validate mission_capable doesn't exceed total_drones
    if mission_capable > total_drones:
        st.warning("⚠️ Mission capable drones cannot exceed total drones available.")
        mission_capable = total_drones
    
    # Battery Sets slider
    battery_sets = st.slider(
        "Battery Sets Available",
        min_value=1,
        max_value=10,
        value=3
    )
    
    # Operators Available slider
    operators = st.slider(
        "Operators Available",
        min_value=1,
        max_value=10,
        value=2
    )

# Enhanced divider between input and results
st.markdown("")
st.markdown("""
    <hr style="border: 2px solid #1f77b4; margin: 30px 0;">
""", unsafe_allow_html=True)
st.markdown("")

# Add Drone to Platoon button
if st.button("Add Drone to Platoon", use_container_width=True, type="primary"):
    # Create drone configuration dictionary
    drone_data = {
        "drone_name": drone_name,
        "drone_class": drone_class,
        "base_endurance": base_endurance,
        "battery_health": battery_health,
        "reliability": reliability,
        "total_drones": total_drones,
        "mission_capable": mission_capable,
        "battery_sets": battery_sets,
        "operators": operators
    }
    
    # Add drone to platoon
    st.session_state.platoon.append(drone_data)
    
    # Show success message
    st.success("Drone added to platoon inventory.")

# Platoon Inventory Section
st.divider()
st.subheader("Platoon Inventory")

if st.session_state.platoon:
    # Convert platoon list to DataFrame
    df = pd.DataFrame(st.session_state.platoon)
    
    # Select only the columns to display
    display_columns = ["drone_name", "drone_class", "mission_capable", "battery_sets", "operators"]
    df_display = df[display_columns]
    
    # Rename columns for better display
    df_display.columns = ["Drone Name", "Drone Class", "Mission Capable", "Battery Sets", "Operators"]
    
    # Display the DataFrame
    st.dataframe(df_display, use_container_width=True)
    
    # Clear Platoon Inventory button
    if st.button("Clear Platoon Inventory", use_container_width=True):
        st.session_state.platoon = []
        st.success("Platoon inventory cleared.")
        st.rerun()
else:
    st.info("No drones in platoon inventory yet. Add a drone to get started!")

# Editable Platoon Inventory Section
st.divider()
st.subheader("Editable Platoon Inventory")

if st.session_state.platoon:
    # Convert platoon list to DataFrame
    df_editable = pd.DataFrame(st.session_state.platoon)
    
    # Select columns for editing
    edit_columns = ["drone_name", "drone_class", "mission_capable", "battery_sets", "operators", "battery_health", "reliability"]
    df_edit = df_editable[edit_columns].copy()
    
    # Rename columns for better display
    df_edit.columns = ["Drone Name", "Drone Class", "Mission Capable", "Battery Sets", "Operators", "Battery Health", "Reliability"]
    
    # Define column configuration for data editor
    column_config = {
        "Drone Name": st.column_config.TextColumn(disabled=True),
        "Drone Class": st.column_config.TextColumn(disabled=True),
        "Mission Capable": st.column_config.NumberColumn(min_value=0, max_value=10),
        "Battery Sets": st.column_config.NumberColumn(min_value=1, max_value=10),
        "Operators": st.column_config.NumberColumn(min_value=1, max_value=10),
        "Battery Health": st.column_config.NumberColumn(min_value=0.5, max_value=1.0, step=0.05),
        "Reliability": st.column_config.NumberColumn(min_value=0.0, max_value=1.0, step=0.1),
    }
    
    # Display editable data
    st.info("💡 Tip: Click row numbers on the left to select and delete drones from the inventory.")
    
    edited_df = st.data_editor(
        df_edit,
        column_config=column_config,
        hide_index=False,
        use_container_width=True,
        key="platoon_editor",
        num_rows="dynamic"
    )
    
    # Save Changes button
    if st.button("Save Changes to Operational Inventory", use_container_width=True, type="primary"):
        # Handle deleted rows and update edited values
        updated_platoon = []
        
        for idx, row in edited_df.iterrows():
            updated_platoon.append({
                "drone_name": st.session_state.platoon[idx]["drone_name"],
                "drone_class": st.session_state.platoon[idx]["drone_class"],
                "base_endurance": st.session_state.platoon[idx]["base_endurance"],
                "mission_capable": int(row["Mission Capable"]),
                "battery_sets": int(row["Battery Sets"]),
                "operators": int(row["Operators"]),
                "battery_health": row["Battery Health"],
                "reliability": row["Reliability"],
                "total_drones": st.session_state.platoon[idx]["total_drones"]
            })
        
        # Update session state with all rows (deleted rows are not in edited_df)
        st.session_state.platoon = updated_platoon
        st.success("Operational inventory updated successfully.")
        st.rerun()
else:
    st.info("No drones in platoon inventory to edit yet.")

# Platoon Capability Dashboard Section
st.divider()
st.subheader("Platoon Capability Dashboard")

if st.session_state.platoon:
    # Calculate platoon capability totals
    capability_totals = calculate_platoon_capability(st.session_state.platoon)
    
    # Create columns for metrics
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    # Convert minutes to hours for display
    persistent_isr_hours = capability_totals["Persistent ISR"] / 60
    tactical_isr_hours = capability_totals["Tactical ISR"] / 60
    rapid_recon_hours = capability_totals["Rapid Recon"] / 60
    micro_recon_hours = capability_totals["Micro Recon"] / 60
    
    with metric_col1:
        st.metric(
            "Persistent ISR",
            f"{persistent_isr_hours:.2f} hrs",
            help="Total continuous ISR hours from Persistent ISR drones"
        )
    
    with metric_col2:
        st.metric(
            "Tactical ISR",
            f"{tactical_isr_hours:.2f} hrs",
            help="Total continuous ISR hours from Tactical ISR drones"
        )
    
    with metric_col3:
        st.metric(
            "Rapid Recon",
            f"{rapid_recon_hours:.2f} hrs",
            help="Total continuous ISR hours from Rapid Recon drones"
        )
    
    with metric_col4:
        st.metric(
            "Micro Recon",
            f"{micro_recon_hours:.2f} hrs",
            help="Total continuous ISR hours from Micro Recon drones"
        )
else:
    st.info("Add drones to the platoon to see capability totals.")

# Mission Planning Section
st.divider()
st.subheader("Mission Planning and Drone Allocation")

# Create two-column layout for mission planning
left_col, right_col = st.columns([1, 2])

# LEFT COLUMN: Mission Parameters Input
with left_col:
    st.write("**Mission Parameters**")
    
    mission_type = st.selectbox(
        "Mission Type",
        ["Persistent ISR", "Tactical ISR", "Rapid Recon", "Micro Recon"]
    )
    
    mission_duration_hours = st.slider(
        "Mission Duration (hours)",
        min_value=1,
        max_value=24,
        value=8
    )
    
    mission_condition = st.selectbox(
        "Mission Condition",
        ["Day", "Night"]
    )
    
    # Generate Mission Plan button
    generate_plan = st.button("Generate Mission Plan", use_container_width=True, type="primary")

# RIGHT COLUMN: Mission Planning Results
with right_col:
    if generate_plan:
        # Check if platoon has drones
        if not st.session_state.platoon:
            st.warning("⚠️ No drones available in platoon inventory.")
        else:
            # Generate mission plan using the suggestion function
            mission_plan = suggest_drone_allocation(mission_duration_hours, st.session_state.platoon)
            
            # Display status message
            if mission_plan["mission_feasible"]:
                st.success("✅ Mission can be completed with current platoon resources!")
            else:
                st.warning(f"⚠️ Mission requirement exceeds available capability. Shortfall: {mission_plan['mission_minutes'] - mission_plan['total_coverage_minutes']:.0f} minutes")
            
            # Display metrics
            results_col1, results_col2, results_col3 = st.columns(3)
            
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
                    "Coverage Margin",
                    f"{mission_plan['remaining_margin']:.0f} min",
                    help="Extra coverage beyond mission requirement"
                )
            
            # Display recommended drone allocation
            st.markdown("**Recommended Drone Allocation**")
            
            if mission_plan["allocation"]:
                allocation_data = []
                for drone_allocation in mission_plan["allocation"]:
                    allocation_data.append({
                        "Drone": drone_allocation["drone_name"],
                        "Class": drone_allocation["drone_class"],
                        "Contribution (hrs)": f"{drone_allocation['contribution_hours']:.2f}",
                        "Endurance (min)": f"{drone_allocation['effective_endurance_minutes']:.0f}",
                        "Battery Sets": drone_allocation["battery_sets"]
                    })
                
                allocation_df = pd.DataFrame(allocation_data)
                st.dataframe(allocation_df, use_container_width=True, hide_index=True)
            else:
                st.info("No drones allocated for this mission.")
            
            # Display mission summary
            st.markdown("**Mission Summary**")
            st.info(f"""
            **Parameters:** {mission_type} | {mission_duration_hours}h | {mission_condition}
            
            **Coverage:** {mission_plan['total_coverage_minutes'] / 60:.2f} hrs | **Margin:** {mission_plan['remaining_margin']:.0f} min | **Drones:** {len(mission_plan['allocation'])}
            """)
    else:
        st.info("👈 Configure mission parameters and click 'Generate Mission Plan' to see results here.")



