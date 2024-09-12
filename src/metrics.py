"""
Module for performance metrics
"""
from src.agent import Agent
from src.environment import Environment

def evaluate_simulation(environment:Environment, agent:Agent)->dict:
    print("===================================")
    initial_dirt_count = len(environment.initial_dirty_locations)
    final_dirt_count = len(environment.__get_global_dirty_locations__())
    total_dirt_cleaned = initial_dirt_count - final_dirt_count
    total_steps_taken = len(agent.path_followed)
    unique_locations_visited = len(agent.visited_locations)
    percentage_dirt_cleaned = round(((initial_dirt_count-final_dirt_count)/initial_dirt_count)*100)
    dirt_cleaned_per_step = round((initial_dirt_count-final_dirt_count)/total_steps_taken,2)
    coverage_efficiency = round((unique_locations_visited/total_steps_taken)*100)
    total_obstacles = len(environment.initial_obstacles)
    total_obstacles_detected = len(agent.obstacles_detected)
    initial_energy = agent.initial_energy
    current_energy = agent.current_energy
    total_energy_consumed = round(initial_energy - current_energy,2)
    percentage_energy_consumed = round(((initial_energy-current_energy)/initial_energy)*100,2)
    percentage_energy_consumed_per_dirty_spot = round((total_energy_consumed/total_dirt_cleaned)*100/initial_energy,2)
    percentage_energy_consumed_per_step = round((total_energy_consumed/total_steps_taken)*100/initial_energy,2)

    print("------------------------------------")
    print("Initial Conditions")
    print("------------------------------------")
    print("Initial dirt count:", initial_dirt_count)
    print("Inital Obstacles:", total_obstacles)
    print("Initial Energy:", initial_energy)
    print("------------------------------------")


    print("------------------------------------")
    print("Current State")
    print("------------------------------------")
    print("Steps Taken:", total_steps_taken)
    print("Pending dirt count:", final_dirt_count)
    print("Unique Locations Visited:", unique_locations_visited)
    print("Obstacles Detected:", total_obstacles_detected)
    print("Current Energy:", current_energy)
    print("------------------------------------")

    print("------------------------------------")
    print("Performance Metrics")
    print("------------------------------------")
    print(f"""Percentage Dirt Cleaned: {percentage_dirt_cleaned}%""")
    print("Dirt Cleaned per Step:", dirt_cleaned_per_step)
    print(f"""Coverage Efficiency: {coverage_efficiency}%""")
    print("Total Energy Consumed:", total_energy_consumed)
    print("Percentage Energy Consumed:", percentage_energy_consumed)
    print(f"""Energy Consumed per Spot: {percentage_energy_consumed_per_dirty_spot}%""")
    print(f"""Energy Consumed per Step: {percentage_energy_consumed_per_step}%""")
    print("===================================")

    return {
        "initial_conditions":{
            "initial_dirt_count":initial_dirt_count,
            "total_obstacles":total_obstacles,
            "initial_energy":initial_energy
        },
        "current_state":{
            "total_steps_taken":total_steps_taken,
            "final_dirt_count":final_dirt_count,
            "unique_locations_visited":unique_locations_visited,
            "total_obstacles_detected":total_obstacles_detected,
            "current_energy":current_energy
        },
        "performance_metrics":{
            "percentage_dirt_cleaned":percentage_dirt_cleaned,
            "dirt_cleaned_per_step":dirt_cleaned_per_step,
            "coverage_efficiency":coverage_efficiency,
            "total_energy_consumed":total_energy_consumed,
            "percentage_energy_consumed":percentage_energy_consumed,
            "percentage_energy_consumed_per_dirty_spot":percentage_energy_consumed_per_dirty_spot,
            "percentage_energy_consumed_per_step":percentage_energy_consumed_per_step
        }
    }