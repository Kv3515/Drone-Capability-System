import streamlit as st
import pandas as pd
from capability import calculate_drone_capability, calculate_platoon_capability, calculate_platoon_payload_capability

# Page configuration
st.set_page_config(page_title="Platoon Capability - Drone Capability Calculator", layout="wide")

# Initialize session state for platoon
if "platoon" not in st.session_state:
    st.session_state.platoon = []

# Breadcrumb navigation
breadcrumb_col1, breadcrumb_col2 = st.columns([0.1, 0.9])
with breadcrumb_col1:
    if st.button("🏠", key="breadcrumb_home", help="Go to Home"):
        st.switch_page("pages/1_Home.py")
with breadcrumb_col2:
    st.markdown("🏠 **Home** > 🚁 **Platoon Capability**")

st.divider()

st.title("📊 Platoon Capability")
st.markdown("---")

# Drone Configuration Section
st.subheader("Drone Configuration")

col1, col2 = st.columns(2)

with col1:
    st.write("**Drone Specifications**")
    
    # Drone Name dropdown
    drone_name = st.selectbox(
        "Drone Name",
        [
            "DJI Air 2S Quadcopter",
            "SVL Copter Q5 HA",
            "DJI Air 3S",
            "DJI Mavic 2 Enterprise Advance",
            "DJI 350 RTK",
            "DJI Avata 2",
            "DJI Neo",
            "DJI Phantom 4",
            "Nano Drone (Black Hornet)",
            "DJI Mavic Mini",
            "Quadcopter Day Medium Range",
            "Quadcopter Day & Night Medium Range",
            "Mini UAV NAFCL-2",
            "Multicopter Medium Altitude (Tunga)",
            "Drone Day Camera 1080P (Nano)",
            "UAV Night Hawk",
            "Mini UAV Switch",
            "Micro Drone IF UAV 60 Min",
            "Mini SVL Copter",
            "RPAV"
        ],
        key="drone_name_select"
    )
    
    # Drone Class dropdown
    drone_class = st.selectbox(
        "Drone Class",
        ["Persistent ISR", "Tactical ISR", "Rapid Recon", "Micro Recon"],
        key="drone_class_select"
    )
    
    # Base Endurance dropdown (in minutes)
    base_endurance_minutes = st.selectbox(
        "Base Endurance (minutes)",
        [15, 20, 30, 45, 60, 90, 120],
        index=4,  # Default to 60 minutes
        key="base_endurance_select"
    )
    # Convert to hours
    base_endurance = base_endurance_minutes / 60
    
    # Battery Health slider
    battery_health = st.slider(
        "Battery Health (0-1)",
        min_value=0.5,
        max_value=1.0,
        value=0.9,
        step=0.05,
        key="battery_health_slider"
    )
    
    # Reliability dropdown
    reliability = st.selectbox(
        "Reliability",
        [1.0, 0.9, 0.8, 0.7],
        index=1,  # Default to 0.9
        key="reliability_select"
    )

with col2:
    st.write("**Operational Parameters**")
    
    # Total Drones slider
    total_drones = st.slider(
        "Total Drones Available",
        min_value=1,
        max_value=10,
        value=5,
        key="total_drones_slider"
    )
    
    # Mission Capable Drones slider
    mission_capable = st.slider(
        "Mission Capable Drones",
        min_value=0,
        max_value=10,
        value=4,
        key="mission_capable_slider"
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
        value=3,
        key="battery_sets_slider"
    )
    
    # Operators Available slider
    operators = st.slider(
        "Operators Available",
        min_value=1,
        max_value=10,
        value=2,
        key="operators_slider"
    )

st.divider()

# Payload Configuration Section
st.subheader("Payload Capability")

payload_col1, payload_col2 = st.columns(2)

with payload_col1:
    st.write("**Payload Configuration**")
    
    # Payload Capable toggle
    payload_capable = st.radio(
        "Payload Capable",
        ["Yes", "No"],
        horizontal=True,
        key="payload_capable_radio"
    )
    payload_capable_bool = payload_capable == "Yes"

with payload_col2:
    st.write("")
    st.write("")
    
    # Payload Capacity (only if payload capable)
    if payload_capable_bool:
        payload_capacity_kg = st.number_input(
            "Payload Capacity (kg)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.5,
            key="payload_capacity_input"
        )
    else:
        payload_capacity_kg = 0.0
        st.info("ℹ️ Payload capacity is disabled for this drone.")

st.divider()

# Add Drone to Platoon button
if st.button("Add Drone to Platoon", use_container_width=True, type="primary", key="add_drone_button"):
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
        "operators": operators,
        "payload_capable": payload_capable_bool,
        "payload_capacity_kg": payload_capacity_kg
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
    edit_columns = ["drone_name", "drone_class", "mission_capable", "battery_sets", "operators", "battery_health", "reliability", "payload_capable", "payload_capacity_kg"]
    df_edit = df_editable[edit_columns].copy()
    
    # Rename columns for better display
    df_edit.columns = ["Drone Name", "Drone Class", "Mission Capable", "Battery Sets", "Operators", "Battery Health", "Reliability", "Payload Capable", "Payload Capacity (kg)"]
    
    # Define column configuration for data editor
    column_config = {
        "Drone Name": st.column_config.TextColumn(disabled=True),
        "Drone Class": st.column_config.TextColumn(disabled=True),
        "Mission Capable": st.column_config.NumberColumn(min_value=0, max_value=10),
        "Battery Sets": st.column_config.NumberColumn(min_value=1, max_value=10),
        "Operators": st.column_config.NumberColumn(min_value=1, max_value=10),
        "Battery Health": st.column_config.NumberColumn(min_value=0.5, max_value=1.0, step=0.05),
        "Reliability": st.column_config.NumberColumn(min_value=0.0, max_value=1.0, step=0.1),
        "Payload Capable": st.column_config.CheckboxColumn(),
        "Payload Capacity (kg)": st.column_config.NumberColumn(min_value=0.0, max_value=100.0, step=0.5),
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
                "total_drones": st.session_state.platoon[idx]["total_drones"],
                "payload_capable": row["Payload Capable"],
                "payload_capacity_kg": row["Payload Capacity (kg)"]
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

# Payload Capability Dashboard Section
st.divider()
st.subheader("📦 Payload Deployment Capability")

if st.session_state.platoon:
    # Calculate payload capability
    payload_capability = calculate_platoon_payload_capability(st.session_state.platoon)
    
    # Display payload metrics
    payload_metric_col1, payload_metric_col2 = st.columns(2)
    
    with payload_metric_col1:
        st.metric(
            "Max Payload Per Sortie",
            f"{payload_capability['max_payload_per_sortie']:.1f} kg",
            help="Maximum payload capacity among available payload-capable drones"
        )
    
    with payload_metric_col2:
        st.metric(
            "Total Payload Sorties",
            f"{payload_capability['total_payload_sorties']}",
            help="Total payload sorties available across platoon (mission_capable × battery_sets)"
        )
    
    # Display payload capability table
    if payload_capability['payload_drones']:
        st.markdown("**Payload Deployment by Drone Type**")
        
        payload_df = pd.DataFrame(payload_capability['payload_drones'])
        payload_df_display = payload_df[['drone_name', 'drone_class', 'payload_capacity_kg', 'payload_sorties']].copy()
        payload_df_display.columns = ['Drone Name', 'Drone Class', 'Payload per Sortie (kg)', 'Available Sorties']
        
        st.dataframe(payload_df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No payload-capable drones in platoon inventory.")
else:
    st.info("Add drones to the platoon to see payload capability totals.")

