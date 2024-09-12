"""
Constants
"""

IDLE_LIMIT = 35

POPULATION_DENSITY = {
    "OBSTACLES": 0.7,
    "DIRT": 0.3
}

ENERGY_CONSUMPTION = {
    "MOVE_STRAIGHT": 1,
    "MOVE_DIAGONAL": 1.5,
    "SCAN": 2,
    "CLEAN": 5
}

LOCATION_MARKERS = {
    "DIRT": 2,
    "CLEAN": 0,
    "OBSTACLE": 1,
    "AGENT": 8
}

DIRECTIONS = {
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
    "UP": (0,-1),
    "DOWN": (0,1),
    "UP_LEFT": (-1,-1),
    "UP_RIGHT": (1,-1),
    "DOWN_LEFT": (-1, 1),
    "DOWN_RIGHT": (1,1)
}

STRAIGHT_DIRECTIONS = ["LEFT","RIGHT","UP","DOWN"]
DIAGONAL_DIRECTIONS = ["UP_LEFT","UP_RIGHT","DOWN_LEFT","DOWN_RIGHT"]