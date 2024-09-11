"""
Entry Point
"""

from src.environment import Environment
from src.agent import Agent

def run_simulation():
    environ = Environment()
    environ.__generate_environment__()
    environ.__populate_grid__()

    agent = Agent(environment=environ,
                  sensor_range=3,
                  initial_position={"x":3,"y":3})

    environ.__print_grid__()

    agent.__sense__()

if __name__ == "__main__":
    run_simulation()
