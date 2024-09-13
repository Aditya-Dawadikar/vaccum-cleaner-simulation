# Vacuum Cleaner Simulation

## Overview

This project simulates a vacuum cleaner agent navigating a grid-based environment to clean dirt while avoiding obstacles.

## Features

- **Agent Behavior**: Moves to tiles based on the cleaning priority, avoiding obstacles
- **Grid Environment**: A 2D grid where tiles can be dirt, clean, empty, or obstacles.
- **Energy Consumption**: Calculations for movement, scanning, and cleaning.

## Installation

To run the simulation, you need to have Python and the required packages installed. Follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Aditya-Dawadikar/vaccum-cleaner-simulation.git
    cd vacuum-cleaner-simulation
    ```

2. **Install the required packages:**

    It is recommended to create a virtual environment first:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

    Then install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. **Export Env variables:**
    It requires following env variable

    | Variable  | Description                                | Value    |
    |-----------|--------------------------------------------|-----------------|
    | BASE_PATH | location of the root folder of the project | eg: /Users/spartan/Desktop/vaccum-cleaner-simulation |

## Usage

1. **Run the Simulation:**

    `cd vaccum-cleaner-simulation`

    `python3 main.py`

2. **Generating Console based Logs**

    main.py
    ~~~
    data_df = exec_runner(iterations=10, verbose=True)
    ~~~

3. **Visualizing**
    main.py
    ~~~
    data_df = exec_runner(iterations=10)

    dirt_clean_percentage(data_df)
    energy_consumption_vs_dirt_cleaned(data_df)
    efficiency_and_energy_consumption_per_step(data_df)
    metrics_correlation(data_df)
    energy_consumption_per_empty_spot(data_df)
    ~~~

4. **Animation**
    main.py
    ~~~
    data_df = exec_runner(iterations=10, verbose=True, export_gif=True)
    ~~~

## Sample Visualizations

### Agent Movement Animation
### Percentage of Dirt Cleaned Per Simulation
### Energy Consumption Vs Dirt Cleaned
### Efficiency and Energy Consumption per step
### Metrics Correlation
### Energy Consumption per Empty Spot

## Development

### Code Structure

- **`src/`**: Contains the main simulation code.
  - **`environment.py`**: Defines the grid and environment setup.
  - **`agent.py`**: Contains the agent logic and movement functions.
  - **`metrics.py`**: Contains logic for performance evaluation metrics.
  - **`visualization.py`**: Contains functions for generating charts and visualizing agent movement
  - **`simulation.py`**: Contains logic for running one simulation
  - **`runner.py`**: Contains logic for running multiple simulations and aggregating results for visualization
- **`constants.py`**: Contains constant values used throughout the simulation.
- **`requirements.txt`**: Lists the required Python packages.

### Adding New Features

To add new features, follow these steps:

1. Modify the appropriate modules or add new ones.
2. Ensure to update the `README.md` with any new functionalities or dependencies.
3. Write tests to verify the correctness of new features.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your fork.
4. Create a pull request describing your changes.

## Contact

For questions or feedback, please contact [mail.aditya.dawadikar@gmail.com](mail.aditya.dawadikar@gmail.com)
