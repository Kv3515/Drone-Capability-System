class Drone:
    """
    Represents a drone record with various attributes.
    """
    def __init__(self, drone_name, drone_class, base_endurance, battery_health, 
                 reliability, total_drones, mission_capable, battery_sets):
        """
        Initialize a Drone instance.
        
        Args:
            drone_name (str): Name of the drone
            drone_class (str): Classification of the drone
            base_endurance (float): Base endurance in hours
            battery_health (float): Battery health percentage (0-100)
            reliability (float): Reliability rating
            total_drones (int): Total number of this drone type
            mission_capable (int): Number of mission-capable drones
            battery_sets (int): Number of battery sets available
        """
        self.drone_name = drone_name
        self.drone_class = drone_class
        self.base_endurance = base_endurance
        self.battery_health = battery_health
        self.reliability = reliability
        self.total_drones = total_drones
        self.mission_capable = mission_capable
        self.battery_sets = battery_sets

    def __repr__(self):
        """Return a string representation of the Drone instance."""
        return (f"Drone(name={self.drone_name}, class={self.drone_class}, "
                f"endurance={self.base_endurance}h, battery_health={self.battery_health}%, "
                f"reliability={self.reliability}, total={self.total_drones}, "
                f"mission_capable={self.mission_capable}, battery_sets={self.battery_sets})")

    def __str__(self):
        """Return a user-friendly string representation."""
        return (f"{self.drone_name} ({self.drone_class}) - "
                f"Endurance: {self.base_endurance}h, Battery Health: {self.battery_health}%, "
                f"Mission Capable: {self.mission_capable}/{self.total_drones}")

    def get_mission_capability_ratio(self):
        """
        Calculate the ratio of mission-capable drones to total drones.
        
        Returns:
            float: Mission capability ratio (0-1)
        """
        if self.total_drones == 0:
            return 0
        return self.mission_capable / self.total_drones

    def is_mission_ready(self):
        """
        Determine if the drone is mission ready based on battery health and reliability.
        
        Returns:
            bool: True if battery health is above 80% and reliability is above 0.8
        """
        return self.battery_health > 80 and self.reliability > 0.8
