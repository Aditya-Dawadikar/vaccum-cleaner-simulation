"""
Module to Run multiple simulations and capture logs
"""
import pandas as pd
from src.simulation import run_simulation
from src.visualization import (plot_energy_expenditure_per_step,
                               plot_battery_usage,
                               plot_steps_to_clean,
                               plot_dirt_spots_left)

def exec_runner(verbose:bool=False,
                export_gif:bool=False)->pd.DataFrame:
    sim_name = f"""sim_{1}"""
    sim_name, performance, meta_data = run_simulation(simulation_name=sim_name,verbose=verbose, export_gif = export_gif)
    
    print(f"""Simulation {sim_name} completed in {meta_data["time_elapsed"]}s""")
 
    print("=================================")

    print(meta_data["moves_made"])


    print("=================================")
    for elem in performance["performance_metrics"]:
        print(f"""{elem}:{performance["performance_metrics"][elem]}""")

    plot_battery_usage(meta_data["battery_usage"])
    plot_energy_expenditure_per_step(meta_data["step_energy_expenditure"])
    plot_steps_to_clean(meta_data["steps_to_clean"])
    plot_dirt_spots_left(meta_data["dirt_spots_left"])