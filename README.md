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

2. **Controlling Environment**

    Edit the following Variables in the `constants.py`
    
    | **Variable**   | **Description**                                                                                                                        | **Value** |
    |----------------|----------------------------------------------------------------------------------------------------------------------------------------|-----------|
    | OBSTACLES      | The density of obstacles. Expected value 0 to 1                                                                                        | eg: 0.15  |
    | DIRT           | The density of dirt. Expected value 0 to 1                                                                                             | eg: 0.3   |
    | INITIAL_ENERGY | Amount of Energy the Agents has as the beginning of the simulation                                                                     | eg: 2000  |
    | IDLE_LIMIT     | Number of steps for which the Agent can navigate without detecting dirt. Simulation ends when agent is idle for longer than this value | eg: 20    |
    | MOVE_STRAIGHT  | Energy requirements for moving straight                                                                                                | eg: 1     |
    | MOVE_DIAGONAL  | Energy requiremnts for moving diagonally                                                                                               | eg: 1.5   |
    | SCAN           | Energy requirements for scanning surrounding                                                                                           | eg: 2     |
    | CLEAN          | Energy requirements for cleaning a spot                                                                                                | eg: 5     |
    | GRID_WIDTH     | Width of the environment                                                                                                               | eg: 30    |
    | GRID_HEIGHT    | Height of the environment                                                                                                              | eg: 30    |

## Sample Visualizations

### Agent Movement Animation
![img](https://github.com/Aditya-Dawadikar/vaccum-cleaner-simulation/blob/single-simulation-runner/views/simulation_2024-09-14_01-35-33-140.gif)
### Battery Usage over Time
![img](https://github.com/Aditya-Dawadikar/vaccum-cleaner-simulation/blob/single-simulation-runner/views/battery_usage_over_time.png)
### Energy Expenditure Per Step
![img](https://github.com/Aditya-Dawadikar/vaccum-cleaner-simulation/blob/single-simulation-runner/views/energy_expenditure_per_step.png)
### Steps taken to clean each dirt spot
![img](https://github.com/Aditya-Dawadikar/vaccum-cleaner-simulation/blob/single-simulation-runner/views/steps_taken_to_clean_each_dirt_spot.png)
### Number of dirt spots left over time
![img](https://github.com/Aditya-Dawadikar/vaccum-cleaner-simulation/blob/single-simulation-runner/views/number_of_dirt_spots_left_over_time.png)

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
