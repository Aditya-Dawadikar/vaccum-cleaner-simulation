"""
Entry Point
"""
from src.runner import exec_runner
from src.visualization import (dirt_clean_percentage,
                               energy_consumption_vs_dirt_cleaned,
                               efficiency_and_energy_consumption_per_step,
                               metrics_correlation,
                               energy_consumption_per_empty_spot
                               )
from src.simulation import run_simulation

if __name__ == "__main__":
    data_df = exec_runner(iterations=10)

    dirt_clean_percentage(data_df)
    energy_consumption_vs_dirt_cleaned(data_df)
    efficiency_and_energy_consumption_per_step(data_df)
    metrics_correlation(data_df)
    energy_consumption_per_empty_spot(data_df)
