"""
Module to Run multiple simulations and capture logs
"""
import pandas as pd
from src.simulation import run_simulation

def exec_runner(iterations:int=10,
                verbose:bool=False,
                export_gif:bool=False)->pd.DataFrame:
    simulation_data = []
    for i in range(iterations):
        sim_name = f"""sim_{i}"""
        sim_name, performance, meta_data = run_simulation(simulation_name=sim_name,verbose=verbose, export_gif = export_gif)
        simulation_data.append({
            "simulation_name": sim_name,
            "performance_evaluation": performance,
            "meta_data": meta_data
        })
        print(f"""Simulation {sim_name} completed in {meta_data["time_elapsed"]}s""")
    
    data = []
    for sim in simulation_data:
        data_row = []
        data_row.append(sim["simulation_name"])
        data_row.append(sim["performance_evaluation"]["performance_metrics"]["percentage_dirt_cleaned"])
        data_row.append(sim["performance_evaluation"]["performance_metrics"]["dirt_cleaned_per_step"])
        data_row.append(sim["performance_evaluation"]["performance_metrics"]["coverage_efficiency"])
        data_row.append(sim["performance_evaluation"]["performance_metrics"]["total_energy_consumed"])
        data_row.append(sim["performance_evaluation"]["performance_metrics"]["percentage_energy_consumed"])
        data_row.append(sim["performance_evaluation"]["performance_metrics"]["percentage_energy_consumed_per_dirty_spot"])
        data_row.append(sim["performance_evaluation"]["performance_metrics"]["percentage_energy_consumed_per_step"])
        data.append(data_row)
    
    df = pd.DataFrame(data=data,
                      columns=["simulation_name",
                                          "percentage_dirt_cleaned",
                                          "dirt_cleaned_per_step",
                                          "coverage_efficiency",
                                          "total_energy_consumed",
                                          "percentage_energy_consumed",
                                          "percentage_energy_consumed_per_dirty_spot",
                                          "percentage_energy_consumed_per_step"
                                          ])
    return df 