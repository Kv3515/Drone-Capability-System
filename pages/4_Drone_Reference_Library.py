import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Drone Reference Library - Drone Capability Calculator", layout="wide")

# Breadcrumb navigation
breadcrumb_col1, breadcrumb_col2 = st.columns([0.1, 0.9])
with breadcrumb_col1:
    if st.button("🏠", key="breadcrumb_home", help="Go to Home"):
        st.switch_page("pages/1_Home.py")
with breadcrumb_col2:
    st.markdown("🏠 **Home** > 📚 **Drone Reference Library**")

st.divider()

st.title("📚 Drone Reference Library")
st.markdown("Technical specifications and reference data for organizational drone inventory")
st.divider()

# Drone Specification Database
DRONE_DATABASE = {
    "DJI Air 2S Quadcopter": {
        "manufacturer": "DJI",
        "drone_class": "Tactical ISR",
        "endurance_minutes": 31,
        "operational_range_km": 12,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": False,
        "primary_role": "Tactical Intelligence, Surveillance & Reconnaissance",
        "typical_uses": [
            "Midrange area surveillance",
            "Bridge and infrastructure inspection",
            "Thermal imaging (with external payload)",
            "Medium-range reconnaissance missions"
        ]
    },
    
    "DJI Air 3S": {
        "manufacturer": "DJI",
        "drone_class": "Tactical ISR",
        "endurance_minutes": 45,
        "operational_range_km": 20,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": "Limited",
        "primary_role": "Extended Range Tactical ISR",
        "typical_uses": [
            "Long-range area surveillance",
            "Wide coverage reconnaissance",
            "Persistent observation missions",
            "Extended duration monitoring"
        ]
    },
    
    "DJI Mavic 2 Enterprise Advance": {
        "manufacturer": "DJI",
        "drone_class": "Tactical ISR / Thermal ISR",
        "endurance_minutes": 31,
        "operational_range_km": 10,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": "Yes (Thermal)",
        "primary_role": "Thermal & Visual Reconnaissance",
        "typical_uses": [
            "Thermal imaging operations",
            "Night surveillance",
            "Building temperature assessment",
            "Search and rescue support"
        ]
    },
    
    "DJI Mavic Mini": {
        "manufacturer": "DJI",
        "drone_class": "Micro ISR",
        "endurance_minutes": 30,
        "operational_range_km": 6,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": False,
        "primary_role": "Lightweight Micro Reconnaissance",
        "typical_uses": [
            "Short-range area assessment",
            "Urban surveillance",
            "Compact area monitoring",
            "Training and familiarization"
        ]
    },
    
    "DJI Phantom 4": {
        "manufacturer": "DJI",
        "drone_class": "Tactical ISR",
        "endurance_minutes": 28,
        "operational_range_km": 7,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": False,
        "primary_role": "Standard Tactical Surveillance",
        "typical_uses": [
            "General area surveillance",
            "Site reconnaissance",
            "Infrastructure inspection",
            "Tactical ISR operations"
        ]
    },
    
    "DJI Avata 2": {
        "manufacturer": "DJI",
        "drone_class": "FPV Recon",
        "endurance_minutes": 23,
        "operational_range_km": 10,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": False,
        "primary_role": "High-Speed First-Person View Reconnaissance",
        "typical_uses": [
            "Fast-moving target tracking",
            "FPV reconnaissance",
            "Dynamic environment assessment",
            "Real-time video feed operations"
        ]
    },
    
    "DJI Neo": {
        "manufacturer": "DJI",
        "drone_class": "Micro Recon",
        "endurance_minutes": 18,
        "operational_range_km": 7,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": False,
        "primary_role": "Ultra-Compact Micro Reconnaissance",
        "typical_uses": [
            "Indoor operations",
            "Ultra-compact area assessment",
            "Close-range surveillance",
            "Portable rapid deployment"
        ]
    },
    
    "DJI 350 RTK": {
        "manufacturer": "DJI",
        "drone_class": "Heavy ISR / Payload",
        "endurance_minutes": 55,
        "operational_range_km": 20,
        "payload_capable": True,
        "payload_capacity_kg": 2.7,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Heavy Payload Carrier with Extended Endurance",
        "typical_uses": [
            "Payload deployment operations",
            "Extended duration surveillance",
            "Thermal and sensor payload delivery",
            "High-altitude reconnaissance"
        ]
    },
    
    "SVL Copter Q5 HA": {
        "manufacturer": "SVL",
        "drone_class": "Payload / Tactical ISR",
        "endurance_minutes": 40,
        "operational_range_km": 10,
        "payload_capable": True,
        "payload_capacity_kg": 5.0,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Multi-Payload ISR Platform",
        "typical_uses": [
            "Sensor payload deployment",
            "Multi-spectral surveillance",
            "Extended payload missions",
            "Night surveillance with payloads"
        ]
    },
    
    "Mini SVL Copter": {
        "manufacturer": "SVL",
        "drone_class": "Tactical ISR",
        "endurance_minutes": 30,
        "operational_range_km": 8,
        "payload_capable": True,
        "payload_capacity_kg": 2.0,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Compact Tactical Payload Carrier",
        "typical_uses": [
            "Lightweight payload operations",
            "Tactical deployment",
            "Night reconnaissance",
            "Urban payload missions"
        ]
    },
    
    "Multicopter Medium Altitude (Tunga)": {
        "manufacturer": "Garuda / DRDO class",
        "drone_class": "Payload ISR",
        "endurance_minutes": 40,
        "operational_range_km": 10,
        "payload_capable": True,
        "payload_capacity_kg": 5.0,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Medium Altitude Payload Platform",
        "typical_uses": [
            "High-altitude payload delivery",
            "Extended mission ISR",
            "Sensor platform operations",
            "Night thermal payload missions"
        ]
    },
    
    "Mini UAV Switch": {
        "manufacturer": "IdeaForge",
        "drone_class": "Persistent ISR",
        "endurance_minutes": 120,
        "operational_range_km": 15,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Long-Endurance Persistent Surveillance",
        "typical_uses": [
            "Extended surveillance missions",
            "Persistent area monitoring",
            "Long-duration ISR operations",
            "Day and night surveillance"
        ]
    },
    
    "UAV Night Hawk": {
        "manufacturer": "Various ISR platforms",
        "drone_class": "Night ISR",
        "endurance_minutes": 60,
        "operational_range_km": 8,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": False,
        "night_capability": True,
        "primary_role": "Dedicated Night Surveillance",
        "typical_uses": [
            "Night operations only",
            "Thermal surveillance",
            "Night-time reconnaissance",
            "Low-light environment monitoring"
        ]
    },
    
    "Nano Drone (Black Hornet)": {
        "manufacturer": "Teledyne FLIR",
        "drone_class": "Micro Recon",
        "endurance_minutes": 25,
        "operational_range_km": 2,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Micro Reconnaissance & Surveillance",
        "typical_uses": [
            "Ultra-short range reconnaissance",
            "Close-quarter surveillance",
            "Portable tactical operations",
            "Urban micro reconnaissance"
        ]
    },
    
    "Drone Day Camera 1080P (Nano)": {
        "manufacturer": "Nano Drone Systems",
        "drone_class": "Micro Recon",
        "endurance_minutes": 30,
        "operational_range_km": 3,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": False,
        "primary_role": "Day-Light Micro Video Reconnaissance",
        "typical_uses": [
            "Daytime surveillance",
            "Close-range video reconnaissance",
            "Compact area assessment",
            "Building reconnaissance"
        ]
    },
    
    "Mini UAV NAFCL-2": {
        "manufacturer": "NAFCL",
        "drone_class": "Tactical ISR",
        "endurance_minutes": 90,
        "operational_range_km": 12,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Extended Endurance Tactical ISR",
        "typical_uses": [
            "Long-duration tactical surveillance",
            "Extended range reconnaissance",
            "Day and night operations",
            "Persistent area monitoring"
        ]
    },
    
    "Micro Drone IF UAV 60 Min": {
        "manufacturer": "Micro Drone Systems",
        "drone_class": "Micro ISR",
        "endurance_minutes": 60,
        "operational_range_km": 5,
        "payload_capable": False,
        "payload_capacity_kg": 0,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Extended Endurance Micro ISR",
        "typical_uses": [
            "60-minute surveillance missions",
            "Compact endurance operations",
            "Day and night micro reconnaissance",
            "Urban area monitoring"
        ]
    },
    
    "RPAV": {
        "manufacturer": "Various Manufacturers",
        "drone_class": "Medium ISR / Payload",
        "endurance_minutes": 180,
        "operational_range_km": 40,
        "payload_capable": True,
        "payload_capacity_kg": 10.0,
        "day_capability": True,
        "night_capability": True,
        "primary_role": "Long-Endurance Heavy Payload Platform",
        "typical_uses": [
            "Very long-duration missions (3+ hours)",
            "Heavy payload delivery",
            "Extended range operations",
            "Complex multi-sensor ISR operations"
        ]
    }
}

# Drone selection dropdown
st.subheader("Select a Drone Type")

selected_drone = st.selectbox(
    "Choose a drone to view its technical specifications",
    options=sorted(DRONE_DATABASE.keys()),
    key="drone_reference_select"
)

st.divider()

if selected_drone:
    drone_info = DRONE_DATABASE[selected_drone]
    
    # Main drone information
    st.subheader(f"🚁 {selected_drone}")
    
    # Key specs in columns
    spec_col1, spec_col2, spec_col3 = st.columns(3)
    
    with spec_col1:
        st.metric(
            "Manufacturer",
            drone_info["manufacturer"],
            help="Manufacturer or supplier"
        )
        st.metric(
            "Drone Class",
            drone_info["drone_class"],
            help="Primary classification"
        )
    
    with spec_col2:
        st.metric(
            "Endurance",
            f"{drone_info['endurance_minutes']} min",
            help="Flight time on single battery"
        )
        st.metric(
            "Operational Range",
            f"{drone_info['operational_range_km']} km",
            help="Maximum operational distance"
        )
    
    with spec_col3:
        day_status = "✅ Yes" if drone_info["day_capability"] else "❌ No"
        night_status = "✅ Yes" if drone_info["night_capability"] else ("⚠️ Limited" if drone_info["night_capability"] == "Limited" else "❌ No")
        
        st.metric(
            "Day Capability",
            day_status,
            help="Daytime operation capability"
        )
        st.metric(
            "Night Capability",
            night_status,
            help="Night operation capability"
        )
    
    st.divider()
    
    # Payload information
    st.subheader("📦 Payload Capability")
    
    payload_col1, payload_col2 = st.columns(2)
    
    with payload_col1:
        if drone_info["payload_capable"]:
            st.success("✅ Payload Capable")
        else:
            st.info("❌ Not Payload Capable")
    
    with payload_col2:
        if drone_info["payload_capable"] and drone_info["payload_capacity_kg"] > 0:
            st.metric(
                "Max Payload Capacity",
                f"{drone_info['payload_capacity_kg']} kg",
                help="Maximum payload weight"
            )
    
    st.divider()
    
    # Operational information
    st.subheader("🎯 Operational Information")
    
    op_col1, op_col2 = st.columns([1, 1])
    
    with op_col1:
        st.write("**Primary Operational Role**")
        st.write(drone_info["primary_role"])
    
    with op_col2:
        st.write("**Typical Uses**")
        for use_case in drone_info["typical_uses"]:
            st.write(f"• {use_case}")
    
    st.divider()
    
    # Technical specifications table
    st.subheader("📋 Technical Specifications Summary")
    
    specs_dict = {
        "Specification": [
            "Manufacturer",
            "Drone Class",
            "Endurance (minutes)",
            "Operational Range (km)",
            "Payload Capable",
            "Payload Capacity (kg)",
            "Day Capability",
            "Night Capability",
        ],
        "Value": [
            drone_info["manufacturer"],
            drone_info["drone_class"],
            drone_info["endurance_minutes"],
            drone_info["operational_range_km"],
            "Yes" if drone_info["payload_capable"] else "No",
            drone_info["payload_capacity_kg"] if drone_info["payload_capable"] else "N/A",
            "Yes" if drone_info["day_capability"] else "No",
            "Yes" if drone_info["night_capability"] == True else ("Limited" if drone_info["night_capability"] == "Limited" else "No"),
        ]
    }
    
    specs_df = pd.DataFrame(specs_dict)
    st.dataframe(specs_df, use_container_width=True, hide_index=True)

st.divider()

# Information footer
st.markdown("""
---
**ℹ️ Reference Library Notes**

This Drone Reference Library provides technical specifications for all drones in the organizational inventory. 
The data presented here is for reference purposes and does not affect operational calculations in the Drone Capability System.

- **Endurance values** are approximate and may vary based on operating conditions, weather, and payload.
- **Operational Range** assumes optimal conditions with good signal strength.
- **Payload Capacity** refers to additional equipment beyond the drone's standard configuration.
- **Day/Night Capability** indicates sensor types and operational limitations.

For detailed technical specifications or mission-specific planning, consult individual drone manuals and operational procedures.
""")
