"""
Module for running simulations
"""
import time
from src.environment import Environment
from src.agent import Agent
from src.metrics import evaluate_simulation
from src.constants import IDLE_LIMIT,INITIAL_ENERGY, TERMINATION_CODE

def run_simulation(verbose:bool=False):

    start_time = time.time()

    environ = Environment()
    environ.__generate_environment__()
    environ.__populate_grid__()

    agent = Agent(environment=environ,
                  sensor_range=3,
                  initial_position={"x":3,"y":3},
                  initial_energy=INITIAL_ENERGY)

    print("------------------------------------")
    print("INITIAL SETUP")
    print("Current Location:", agent.current_position)
    print("Path Followed:", agent.path_followed)
    print("------------------------------------")
    environ.__print_grid__()

    iteration = 0
    idle_count = 0

    termination_code = -1

    while True:
        if environ.__is_grid_clean__()==True:
            print("===================================")
            print("Simulation Terminated: All Dirt Cleaned")
            print("===================================")
            termination_code = TERMINATION_CODE["GOAL_COMPLETE"]
            break
        elif idle_count >= IDLE_LIMIT:
            print("===================================")
            print("Simulation Terminated: Agent Idle")
            print("===================================")
            termination_code = TERMINATION_CODE["IDLE"]
            break
        elif agent.current_energy <= 0:
            print("===================================")
            print("Simulation Terminated: Battery Dead")
            print("===================================")
            termination_code = TERMINATION_CODE["BATTERY_DEAD"]
            break

        iteration += 1
        
        if verbose:
            print("===================================")
            print("Iteration:",iteration)
            print("===================================")
        dirt_found = agent.__step__(verbose)

        if dirt_found == True:
            # if dirt was found, reset idle count
            idle_count = 0
        else:
            # increment idle counter
            idle_count += 1
        
        if verbose:
            environ.__print_grid__()
            print("------------------------------------")
            print("Current Location:\n", agent.current_position)
            print("Path Followed:\n", agent.path_followed)
            print("------------------------------------")

    performance_evaluation = evaluate_simulation(environment=environ,
                                                    agent=agent)
    
    print("TERMINATION CODE:", termination_code)
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(f"""Executed in {round(time_elapsed,2)}s""")

    print("===================================")
    print("===================================")

    return performance_evaluation, termination_code
