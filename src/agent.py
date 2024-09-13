"""
Module for Agent programs
"""
import random
from collections import deque
from src.common import euclidean_distance
from src.environment import Environment
from constants import (LOCATION_MARKERS,
                           DIRECTIONS,
                           STRAIGHT_DIRECTIONS,
                           DIAGONAL_DIRECTIONS,
                           ENERGY_CONSUMPTION)

class Agent:
    def __init__(self,
                 environment: Environment,
                 sensor_range: int = 1,
                 initial_position: dict = {"x":0,"y":0},
                 initial_energy: int =  1000):
        # environment
        self.environment = environment

        # initial position of agent
        self.initial_position = {
            "x": initial_position["x"],
            "y": initial_position["y"]
        }
        
        # current position of agent
        self.current_position = {}
        self.current_position["x"]= initial_position["x"]
        self.current_position["y"]= initial_position["y"]

        # next target tile
        self.target_location = {"x":None,"y":None}

        # visited locations
        self.visited_locations = set()
        self.obstacles_detected = set()
        self.path_followed = []

        self.visited_locations.add((self.current_position["x"],self.current_position["y"]))
        self.path_followed.append((self.current_position["x"],self.current_position["y"]))

        #energy
        self.initial_energy = initial_energy
        self.current_energy = initial_energy

    def __step__(self, verbose=False):
        temp_current = (self.current_position["x"],self.current_position["y"])

        dirty_tiles = []
        clean_tiles = []
        obstacle_tiles = []
        for direction,(dx,dy) in DIRECTIONS.items():
            if dx>0:
                nx = min(self.environment.grid_size["x"]-1,temp_current[0]+dx)
            else:
                nx = max(0, temp_current[0]+dx)
            if dy>0:
                ny = min(self.environment.grid_size["y"]-1,temp_current[1]+dy)
            else:
                ny = max(0, temp_current[1]+dy)

            if self.environment.grid_descriptor.grid[nx][ny] == LOCATION_MARKERS["DIRT"]:
                dirty_tiles.append((nx,ny, direction))
            elif self.environment.grid_descriptor.grid[nx][ny] == LOCATION_MARKERS["CLEAN"]:
                clean_tiles.append((nx,ny, direction))
            elif self.environment.grid_descriptor.grid[nx][ny] == LOCATION_MARKERS["OBSTACLE"]:
                obstacle_tiles.append((nx,ny, direction))
                self.obstacles_detected.add((nx,ny, direction))

        # Prioritize unexplored tiles over explored ones
        unexplored_dirty_tiles = [tile for tile in dirty_tiles if (tile[0], tile[1]) not in self.visited_locations]
        unexplored_clean_tiles = [tile for tile in clean_tiles if (tile[0], tile[1]) not in self.visited_locations]

        dirt_found = False

        if unexplored_dirty_tiles:
            # Choose a random unexplored dirty location
            dest = random.choice(unexplored_dirty_tiles)
            dirt_found = True
        elif dirty_tiles:
            # Fallback to explored dirty tiles
            dest = random.choice(dirty_tiles)
            dirt_found = True
        elif unexplored_clean_tiles:
            # Choose a random unexplored clean location
            dest = random.choice(unexplored_clean_tiles)
        elif clean_tiles:
            # Fallback to explored clean tiles
            dest = random.choice(clean_tiles)
        else:
            # No valid move, remain in place (you can adjust this logic)
            dest = temp_current

        # remove agent from prev location
        self.environment.grid_descriptor.grid[self.current_position["x"]][self.current_position["y"]] = LOCATION_MARKERS["CLEAN"]

        # move to the destination
        if verbose:
            print("moving to:", dest)
        self.current_position["x"] = dest[0]
        self.current_position["y"] = dest[1]
        self.visited_locations.add((self.current_position["x"],self.current_position["y"]))
        self.path_followed.append((self.current_position["x"],self.current_position["y"]))

        # move to new location
        self.environment.grid_descriptor.grid[self.current_position["x"]][self.current_position["y"]] = LOCATION_MARKERS["AGENT"]

        # Energy consumption calculations: Movement
        if dest[2] in STRAIGHT_DIRECTIONS:
            movement_energy = ENERGY_CONSUMPTION["MOVE_STRAIGHT"]
        elif dest[2] in DIAGONAL_DIRECTIONS:
            movement_energy = ENERGY_CONSUMPTION["MOVE_DIAGONAL"]

        # Energy consumption calculations: Standard scanning cost
        scan_energy = ENERGY_CONSUMPTION["SCAN"]

        # Energy consumption calculations: Cleaning cost
        # Generating random number for spot cleaning efforts
        cleaning_energy = round(ENERGY_CONSUMPTION["CLEAN"]*round(random.uniform(1,3),2),2)

        step_energy = movement_energy + scan_energy + cleaning_energy

        if self.current_energy - step_energy <= 0:
            self.current_energy = 0
        else:
            self.current_energy -= step_energy

        return dirt_found
