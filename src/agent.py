"""
Module for Agent programs
"""
from src.common import euclidean_distance
from src.environment import Environment
from src.constants import LOCATION_MARKERS

class Agent:
    def __init__(self,
                 environment: Environment,
                 sensor_range: int = 1,
                 initial_position: dict = {"x":0,"y":0}):
        # environment
        self.environment = environment

        # sensor range of agent
        self.sensor_range = sensor_range

        # initial position of agent
        self.initial_position = {
            "x": initial_position["x"],
            "y": initial_position["y"]
        }
        
        # current position of agent
        self.current_position = {}
        self.current_position["x"]= initial_position["x"]
        self.current_position["y"]= initial_position["y"]

        self.__mark_agent_location__()

        self.nearby_dirty_locations = []
        self.nearby_obstacles = []

    def __mark_agent_location__(self):
        # mark agent on grid
        self.environment.grid_descriptor.grid[self.current_position["x"]][self.current_position["y"]] \
            = LOCATION_MARKERS["AGENT"]

    def __sense__(self):
        #scan surrounding
        self.__scan_surrounding__()
        self.__print_nearby_dirty_locations__()
        self.__print_nearby_obstacles__()

    def __scan_surrounding__(self):
        start_x = max(self.current_position["x"]-self.sensor_range,0)
        start_y = max(self.current_position["y"]-self.sensor_range,0)
        end_x = min(self.current_position["x"]+self.sensor_range,self.environment.grid_size["x"])
        end_y = min(self.current_position["y"]+self.sensor_range,self.environment.grid_size["y"])

        i = start_x
        j = start_y
        
        for i in range(start_x, end_x+1):
            for j in range(start_y, end_y+1):
                if self.environment.grid_descriptor.grid[i][j] == LOCATION_MARKERS["DIRT"]:
                    self.nearby_dirty_locations.append({
                        "x":i,
                        "y":j,
                        "distance":euclidean_distance(i,j,self.current_position["x"],self.current_position["y"])
                        })
                elif self.environment.grid_descriptor.grid[i][j] == LOCATION_MARKERS["OBSTACLE"]:
                    self.nearby_obstacles.append({
                        "x":i,
                        "y":j,
                        "distance":euclidean_distance(i,j,self.current_position["x"],self.current_position["y"])
                        })

    def __move__(self, loc: dict = {"x":0,"y":0}):
        self.current_position["x"] = loc["x"]
        self.current_position["y"] = loc["y"]

        self.__mark_agent_location__()
        
    
    def __clean__(self, loc: dict = {"x":0,"y":0}):
        new_nearby_dirty_loc = []
        for pos in self.nearby_dirty_locations:
            if loc["x"] == pos["x"] and loc["y"] == pos["y"]:
                # clean this spot
                self.environment.grid_descriptor.grid[pos["x"]][pos["y"]] = LOCATION_MARKERS["CLEAN"]
            else:
                new_nearby_dirty_loc.append(pos)

    def __print_nearby_dirty_locations__(self):
        print("------------------------------------")
        print("Local Dirty Locations")
        print("------------------------------------")
        print(self.nearby_dirty_locations)

    def __print_nearby_obstacles__(self):
        print("------------------------------------")
        print("Local Obstacles")
        print("------------------------------------")
        print(self.nearby_obstacles)
