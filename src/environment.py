"""
Module for simulation environment
"""
import numpy as np
from src.constants import LOCATION_MARKERS

class Grid:
    def __init__(self, x:int = 10, y:int = 10):
        self.x = x
        self.y = y
        self.grid = np.zeros((x, y), dtype=int)

    def __get_grid__(self):
        return self.grid

class Environment:
    def __init__(self):
        self.grid_descriptor = None
        self.grid_size = {
                "x":0,
                "y":0
            }
        self.obstacles = []
        self.dirty_locations = []

    def __generate_environment__(self,
                                 grid_size: dict = {"x":10,"y": 10},
                                 obstacles:list = [],
                                 dirty_locations:list = []):
        self.grid_descriptor = Grid(x=grid_size["x"],
                         y=grid_size["y"])
        self.grid_size["x"] = grid_size["x"]
        self.grid_size["y"] = grid_size["y"]
        self.obstacles = obstacles
        self.dirty_locations = dirty_locations
        
    def __populate_grid__(self):
        self.obstacles = self.__generate_random_obstacles__(0.5)
        self.dirty_locations = self.__generate_random_dirty_locations__(0.3)

        """
            Note: Currently Obstacles populate the grid first,
            and if there is overlap in obstacle and dirt locations,
            the obstacle location will be overriden by a dirty location.
        """


        self.__populate_obstacles__()
        self.__populate_dirt__()

    def __populate_obstacles__(self):
        for obstacle in self.obstacles:
            self.grid_descriptor.grid[obstacle["x"]][obstacle["y"]] = LOCATION_MARKERS["OBSTACLE"]

    def __populate_dirt__(self):
        for dirt in self.dirty_locations:
            self.grid_descriptor.grid[dirt["x"]][dirt["y"]] = LOCATION_MARKERS["DIRT"]

    def __print_grid__(self):
        for i in range(self.grid_size["x"]):
            for j in range(self.grid_size["y"]):
                print(self.grid_descriptor.grid[j][i], end=' ')
            print()
    
    def __generate_random_obstacles__(self,
                                      obstacle_density: float = 0.1):

        x_max = self.grid_size["x"]
        y_max = self.grid_size["y"]
        
        max_count = int(self.grid_size["x"]*self.grid_size["y"]*obstacle_density)

        obstacle_array = []

        for i in range(max_count):
            new_obstacle_loc = {
                "x": np.random.randint(0, x_max),
                "y": np.random.randint(0, y_max)
            }

            obstacle_array.append(new_obstacle_loc)
    
        return obstacle_array

    def __generate_random_dirty_locations__(self,
                                            dirt_density: float = 0.1):
        x_max = self.grid_size["x"]
        y_max = self.grid_size["y"]
        
        max_count = int(self.grid_size["x"]*self.grid_size["y"]*dirt_density)

        dirt_array = []

        for i in range(max_count):
            new_obstacle_loc = {
                "x": np.random.randint(0, x_max),
                "y": np.random.randint(0, y_max)
            }

            dirt_array.append(new_obstacle_loc)
    
        return dirt_array

    def __print_obstacles__(self):
        print("------------------------------------")
        print("Global Obstacles")
        print("------------------------------------")
        print(self.obstacles)
    
    def __print_dirty_locations__(self):
        print("------------------------------------")
        print("Global Dirty Locations")
        print("------------------------------------")
        print(self.dirty_locations)