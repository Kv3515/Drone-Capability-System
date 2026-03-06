from drone import Drone


def calculate_drone_capability(drone):
    """
    Calculate complete drone capability metrics from a drone dictionary.
    
    Args:
        drone (dict): Dictionary containing:
            - base_endurance: Base endurance in hours
            - battery_health: Battery health as a decimal (0-1)
            - reliability: Reliability rating (0-1)
            - battery_sets: Number of battery sets available
            - mission_capable: Number of mission-capable drones
            - operators: Number of available operators
    
    Returns:
        dict: Dictionary containing:
            - effective_endurance: Effective endurance in minutes
            - total_flight_time: Total flight time in minutes
            - concurrent_flights: Number of concurrent flights
            - continuous_isr_hours: Continuous ISR coverage in hours
    """
    return calculate_capability_metrics(
        base_endurance=drone["base_endurance"],
        battery_health=drone["battery_health"],
        reliability=drone["reliability"],
        battery_sets=drone["battery_sets"],
        mission_capable=drone["mission_capable"],
        operators=drone["operators"]
    )


def calculate_platoon_capability(platoon):
    """
    Calculate aggregated capability metrics for the entire platoon, grouped by drone class.
    
    Args:
        platoon (list): List of drone dictionaries from st.session_state["platoon"]
    
    Returns:
        dict: Dictionary containing continuous ISR minutes totals by drone class:
            - Persistent ISR: Total continuous ISR minutes
            - Tactical ISR: Total continuous ISR minutes
            - Rapid Recon: Total continuous ISR minutes
            - Micro Recon: Total continuous ISR minutes
    """
    # Initialize totals for each drone class
    class_totals = {
        "Persistent ISR": 0.0,
        "Tactical ISR": 0.0,
        "Rapid Recon": 0.0,
        "Micro Recon": 0.0
    }
    
    # Loop through each drone in the platoon
    for drone in platoon:
        # Calculate capability for this drone
        capability = calculate_drone_capability(drone)
        
        # Get the drone class
        drone_class = drone["drone_class"]
        
        # Add continuous ISR to the class total
        if drone_class in class_totals:
            class_totals[drone_class] += capability["continuous_isr_hours"] * 60  # Convert hours to minutes
    
    return class_totals


def suggest_drone_allocation(mission_hours, platoon):
    """
    Suggest optimal drone allocation for a mission based on required mission duration.
    
    Args:
        mission_hours (float): Required mission duration in hours
        platoon (list): List of drone dictionaries from st.session_state["platoon"]
    
    Returns:
        dict: Dictionary containing:
            - allocation: List of allocated drones with their contributions
            - total_coverage_minutes: Total mission time coverage in minutes
            - remaining_margin: Excess coverage beyond mission requirement in minutes
            - mission_feasible: Boolean indicating if mission can be completed
            - mission_minutes: Mission duration in minutes
    """
    # Convert mission hours to minutes
    mission_minutes = mission_hours * 60
    
    # Calculate effective endurance for each drone
    drone_endurances = []
    for idx, drone in enumerate(platoon):
        effective_endurance = drone["base_endurance"] * drone["battery_health"] * drone["reliability"]
        effective_endurance_minutes = effective_endurance * 60
        
        drone_endurances.append({
            "index": idx,
            "drone_name": drone["drone_name"],
            "drone_class": drone["drone_class"],
            "effective_endurance_minutes": effective_endurance_minutes,
            "mission_capable": drone["mission_capable"],
            "battery_sets": drone["battery_sets"]
        })
    
    # Sort drones by effective endurance in descending order
    drone_endurances.sort(key=lambda x: x["effective_endurance_minutes"], reverse=True)
    
    # Allocate drones sequentially
    allocation = []
    total_coverage_minutes = 0
    remaining_minutes = mission_minutes
    
    for drone_info in drone_endurances:
        if remaining_minutes <= 0:
            break
        
        # Calculate contribution based on mission-capable drones and battery sets
        drone_index = drone_info["index"]
        original_drone = platoon[drone_index]
        
        # Each drone can fly battery_sets sorties
        total_available_minutes = drone_info["effective_endurance_minutes"] * original_drone["battery_sets"]
        
        # Allocate what's needed for this drone
        contribution = min(total_available_minutes, remaining_minutes)
        
        allocation.append({
            "drone_name": drone_info["drone_name"],
            "drone_class": drone_info["drone_class"],
            "contribution_minutes": contribution,
            "contribution_hours": contribution / 60,
            "effective_endurance_minutes": drone_info["effective_endurance_minutes"],
            "battery_sets": original_drone["battery_sets"]
        })
        
        total_coverage_minutes += contribution
        remaining_minutes -= contribution
    
    # Calculate remaining margin
    remaining_margin = total_coverage_minutes - mission_minutes
    mission_feasible = total_coverage_minutes >= mission_minutes
    
    return {
        "allocation": allocation,
        "total_coverage_minutes": total_coverage_minutes,
        "remaining_margin": max(0, remaining_margin),
        "mission_feasible": mission_feasible,
        "mission_minutes": mission_minutes
    }


def calculate_capability_metrics(base_endurance, battery_health, reliability, battery_sets, mission_capable, operators):
    """
    Calculate complete drone capability metrics using direct parameters.
    
    Args:
        base_endurance (float): Base endurance in hours
        battery_health (float): Battery health as a decimal (0-1)
        reliability (float): Reliability rating (0-1)
        battery_sets (int): Number of battery sets available
        mission_capable (int): Number of mission-capable drones
        operators (int): Number of available operators
    
    Returns:
        dict: Dictionary containing:
            - effective_endurance: Effective endurance in minutes
            - total_flight_time: Total flight time in minutes
            - concurrent_flights: Number of concurrent flights
            - continuous_isr_hours: Continuous ISR coverage in hours
    """
    # Calculate effective endurance in hours
    effective_endurance_hours = base_endurance * battery_health * reliability
    
    # Convert to minutes
    effective_endurance_minutes = effective_endurance_hours * 60
    
    # Calculate total flight time in hours
    total_flight_time_hours = effective_endurance_hours * battery_sets
    
    # Convert to minutes
    total_flight_time_minutes = total_flight_time_hours * 60
    
    # Calculate concurrent flights
    concurrent_flights = min(mission_capable, operators)
    
    # Calculate continuous ISR in minutes
    if concurrent_flights == 0:
        continuous_isr_minutes = 0
    else:
        continuous_isr_minutes = total_flight_time_minutes / concurrent_flights
    
    # Convert to hours
    continuous_isr_hours = continuous_isr_minutes / 60
    
    return {
        "effective_endurance": effective_endurance_minutes,
        "total_flight_time": total_flight_time_minutes,
        "concurrent_flights": concurrent_flights,
        "continuous_isr_hours": continuous_isr_hours
    }


def calculate_effective_endurance(base_endurance, battery_health, reliability):
    """
    Calculate the effective endurance of a drone.
    
    Formula: effective_endurance = base_endurance * battery_health * reliability
    
    Args:
        base_endurance (float): Base endurance in hours
        battery_health (float): Battery health as a percentage (0-100)
        reliability (float): Reliability rating (0-1)
    
    Returns:
        float: Effective endurance in hours
    """
    # Normalize battery_health from percentage to decimal
    battery_health_decimal = battery_health / 100
    return base_endurance * battery_health_decimal * reliability


def calculate_total_sorties(battery_sets):
    """
    Calculate the total number of sorties.
    
    Formula: total_sorties = battery_sets
    
    Args:
        battery_sets (int): Number of battery sets available
    
    Returns:
        int: Total number of sorties
    """
    return battery_sets


def calculate_total_flight_time(effective_endurance, total_sorties):
    """
    Calculate the total flight time available.
    
    Formula: total_flight_time = effective_endurance * total_sorties
    
    Args:
        effective_endurance (float): Effective endurance in hours
        total_sorties (int): Total number of sorties
    
    Returns:
        float: Total flight time in hours
    """
    return effective_endurance * total_sorties


def calculate_concurrent_flights(mission_capable, operators):
    """
    Calculate the number of concurrent flights that can be conducted.
    
    Formula: concurrent_flights = min(mission_capable, operators)
    
    Args:
        mission_capable (int): Number of mission-capable drones
        operators (int): Number of available operators
    
    Returns:
        int: Number of concurrent flights
    """
    return min(mission_capable, operators)


def calculate_continuous_isr(total_flight_time, concurrent_flights):
    """
    Calculate continuous ISR (Intelligence, Surveillance, Reconnaissance) capability.
    
    Formula: continuous_isr = total_flight_time / concurrent_flights
    
    Args:
        total_flight_time (float): Total flight time in hours
        concurrent_flights (int): Number of concurrent flights
    
    Returns:
        float: Continuous ISR coverage in hours (or infinity if no concurrent flights)
    """
    if concurrent_flights == 0:
        return 0
    return total_flight_time / concurrent_flights


def calculate_drone_capability_from_object(drone, operators):
    """
    Calculate the complete capability metrics for a drone using a Drone object.
    
    Args:
        drone (Drone): A Drone instance with all required attributes
        operators (int): Number of available operators
    
    Returns:
        dict: Dictionary containing:
            - effective_endurance: Effective endurance in hours
            - total_sorties: Total number of sorties
            - total_flight_time: Total flight time in hours
            - concurrent_flights: Number of concurrent flights
            - continuous_isr: Continuous ISR coverage in hours
    """
    effective_endurance = calculate_effective_endurance(
        drone.base_endurance,
        drone.battery_health,
        drone.reliability
    )
    
    total_sorties = calculate_total_sorties(drone.battery_sets)
    
    total_flight_time = calculate_total_flight_time(effective_endurance, total_sorties)
    
    concurrent_flights = calculate_concurrent_flights(drone.mission_capable, operators)
    
    continuous_isr = calculate_continuous_isr(total_flight_time, concurrent_flights)
    
    return {
        "effective_endurance": effective_endurance,
        "total_sorties": total_sorties,
        "total_flight_time": total_flight_time,
        "concurrent_flights": concurrent_flights,
        "continuous_isr": continuous_isr
    }


def calculate_drone_capability_dict(drone_dict, operators):
    """
    Calculate the complete capability metrics for a drone using a dictionary.
    
    Args:
        drone_dict (dict): Dictionary containing drone attributes with keys:
            - base_endurance
            - battery_health
            - battery_sets
            - reliability
            - mission_capable
        operators (int): Number of available operators
    
    Returns:
        dict: Dictionary containing capability metrics
    """
    effective_endurance = calculate_effective_endurance(
        drone_dict["base_endurance"],
        drone_dict["battery_health"],
        drone_dict["reliability"]
    )
    
    total_sorties = calculate_total_sorties(drone_dict["battery_sets"])
    
    total_flight_time = calculate_total_flight_time(effective_endurance, total_sorties)
    
    concurrent_flights = calculate_concurrent_flights(drone_dict["mission_capable"], operators)
    
    continuous_isr = calculate_continuous_isr(total_flight_time, concurrent_flights)
    
    return {
        "effective_endurance": effective_endurance,
        "total_sorties": total_sorties,
        "total_flight_time": total_flight_time,
        "concurrent_flights": concurrent_flights,
        "continuous_isr": continuous_isr
    }
