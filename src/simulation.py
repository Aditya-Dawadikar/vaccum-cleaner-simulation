"""
Module for running simulations
"""
from src.environment import Environment
from src.agent import Agent
from src.metrics import evaluate_simulation
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

    performance_evaluation = evaluate_simulation(environment=environ,
                                                    agent=agent)

    return performance_evaluation
