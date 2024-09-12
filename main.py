"""
Entry Point
"""

from src.environment import Environment
from src.agent import Agent
from src.constants import IDLE_LIMIT

def run_simulation():
    environ = Environment()
    environ.__generate_environment__()
    environ.__populate_grid__()

    agent = Agent(environment=environ,
                  sensor_range=3,
                  initial_position={"x":3,"y":3},
                  initial_energy=600)

    print("------------------------------------")
    print("INITIAL SETUP")
    print("Current Location:", agent.current_position)
    print("Path Followed:", agent.path_followed)
    print("------------------------------------")
    environ.__print_grid__()

    iteration = 0
    idle_count = 0

    while True:
        if environ.__is_grid_clean__()==True:
            print("===================================")
            print("Simulation Terminated: All Dirt Cleaned")
            print("===================================")
            break
        elif idle_count >= IDLE_LIMIT:
            print("===================================")
            print("Simulation Terminated: Agent Idle")
            print("===================================")
            break
        elif agent.current_energy <= 0:
            print("===================================")
            print("Simulation Terminated: Battery Dead")
            print("===================================")
            break

        iteration += 1
        print("===================================")
        print("Iteration:",iteration)
        print("===================================")
        dirt_found = agent.__step__()

        if dirt_found == True:
            # if dirt was found, reset idle count
            idle_count = 0
        else:
            # increment idle counter
            idle_count += 1
        
        environ.__print_grid__()
        print("------------------------------------")
        print("Current Location:\n", agent.current_position)
        print("Path Followed:\n", agent.path_followed)
        print("------------------------------------")

    print("===================================")
    initial_dirt_count = len(environ.initial_dirty_locations)
    final_dirt_count = len(environ.__get_global_dirty_locations__())
    total_dirt_cleaned = initial_dirt_count - final_dirt_count
    total_steps_taken = len(agent.path_followed)
    unique_locations_visited = len(agent.visited_locations)
    percentage_dirt_cleaned = round(((initial_dirt_count-final_dirt_count)/initial_dirt_count)*100)
    dirt_cleaned_per_step = round((initial_dirt_count-final_dirt_count)/total_steps_taken,2)
    coverage_efficiency = round((unique_locations_visited/total_steps_taken)*100)
    total_obstacles = len(environ.initial_obstacles)
    total_obstacles_detected = len(agent.obstacles_detected)
    initial_energy = agent.initial_energy
    current_energy = agent.current_energy
    total_energy_consumed = initial_energy - current_energy
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

if __name__ == "__main__":
    run_simulation()
