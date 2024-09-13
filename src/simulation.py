"""
Module for running simulations
"""
import os
import time
from datetime import datetime
from src.environment import Environment
from src.agent import Agent
from src.metrics import evaluate_simulation
from src.visualization import plot_grid, create_gif
from constants import BASE_PATH, IDLE_LIMIT,INITIAL_ENERGY, TERMINATION_CODE

def run_simulation(simulation_name:str=None,
                   verbose:bool=False,
                   export_gif:bool=False):

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S") + f"""-{now.microsecond // 1000:03d}"""

    if not simulation_name:
        simulation_name = f"""simulation_{timestamp}"""

    if export_gif is True:
        simulation_gif_name = f"""{simulation_name}.gif"""
        png_folder_name = f"""{BASE_PATH}/assets/png/{simulation_name}"""
        gif_folder_name = f"""{BASE_PATH}/assets/gif/{simulation_name}"""
        os.makedirs(png_folder_name, exist_ok=True)
        os.makedirs(gif_folder_name, exist_ok=True)

    start_time = time.time()

    environ = Environment()
    environ.__generate_environment__()
    environ.__populate_grid__()

    agent = Agent(environment=environ,
                  sensor_range=3,
                  initial_position={"x":3,"y":3},
                  initial_energy=INITIAL_ENERGY)

    if verbose:
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
            if verbose:
                print("===================================")
                print("Simulation Terminated: All Dirt Cleaned")
                print("===================================")
            termination_code = TERMINATION_CODE["GOAL_COMPLETE"]
            break
        elif idle_count >= IDLE_LIMIT:
            if verbose:
                print("===================================")
                print("Simulation Terminated: Agent Idle")
                print("===================================")
            termination_code = TERMINATION_CODE["IDLE"]
            break
        elif agent.current_energy <= 0:
            if verbose:
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
        
        if export_gif is True:
            plot_grid(
                environment=environ,
                path_followed=agent.path_followed,
                obstacles=environ.obstacles,
                dirt=environ.dirty_locations,
                file_path=png_folder_name,
                fig_name=iteration
            )

    if export_gif is True:
        create_gif(image_folder=png_folder_name,
                gif_folder=gif_folder_name,
                    gif_filename=simulation_gif_name)

    performance_evaluation = evaluate_simulation(environment=environ,
                                                    agent=agent)
    
    if verbose:
        print("TERMINATION CODE:", termination_code)

    end_time = time.time()
    time_elapsed = end_time - start_time

    if verbose:
        print(f"""Executed in {round(time_elapsed,2)}s""")

        print("===================================")
        print("===================================")

    meta_data = {
        "termination_code": termination_code,
        "start_time": start_time,
        "end_time": end_time,
        "time_elapsed": time_elapsed
    }

    return simulation_name, performance_evaluation, meta_data
