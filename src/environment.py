"""
Module for simulation environment
"""
import numpy as np
from constants import LOCATION_MARKERS, POPULATION_DENSITY, DIRECTIONS

class Grid:
    def __init__(self, x:int = 10, y:int = 10, static_grid = None):
        self.x = x
        self.y = y

        if static_grid is None:
            self.grid = np.zeros((x, y), dtype=int)
        else:
            self.grid = np.array(static_grid)

    def __get_grid__(self):
        return self.grid

class Environment:
    def __init__(self):
        self.grid_descriptor = None
        self.grid_size = {
                "x":0,
                "y":0
            }
        self.initial_dirty_locations = []
        self.initial_obstacles = []
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
        self.initial_obstacles = [x for x in obstacles]
        self.initial_dirty_locations = [x for x in dirty_locations]
        self.obstacles = obstacles
        self.dirty_locations = dirty_locations

    def __static_environment__(self):
        temp_grid = [[0, 1, 0, 0, 1, 0, 0, 1, 1, 1], 
        [0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
        [1, 1, 0, 0, 0, 1, 1, 0, 1, 1], 
        [0, 0, 1, 8, 0, 0, 1, 2, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 2, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 2, 0, 0, 1],
        [1, 0, 1, 1, 2, 0, 1, 0, 1, 0],
        [2, 0, 1, 1, 2, 1, 1, 2, 0, 2],
        [2, 1, 0, 0, 0, 1, 2, 0, 0, 1]]
        self.grid_size={"x":10,"y":10}
        self.grid_descriptor = Grid(static_grid=temp_grid)
        self.initial_dirty_locations = []
        self.initial_obstacles = []
        self.obstacles = []
        self.dirty_locations = []
        for i in range(len(self.grid_descriptor.grid[0])):
            for j in range(len(self.grid_descriptor.grid)):
                if self.grid_descriptor.grid[i][j] == 1:
                    self.initial_obstacles.append({"x":i,"y":j})
                    self.obstacles.append({"x":i,"y":j})
                elif self.grid_descriptor.grid[i][j] == 2:
                    self.initial_dirty_locations.append({"x":i,"y":j})
                    self.dirty_locations.append({"x":i,"y":j})
        
        # self.__print_obstacles__()
        # self.__print_dirty_locations__()

        self.__populate_obstacles__()
        self.__populate_dirt__()

        # self.__print_grid__()

    def __populate_grid__(self):
        self.obstacles, self.dirty_locations = self.__generate_random_obstacles_and_dirt__(POPULATION_DENSITY["OBSTACLES"],
                                                                                           POPULATION_DENSITY["DIRT"])
        self.initial_obstacles = [x for x in self.obstacles]
        self.initial_dirty_locations = [x for x in self.dirty_locations]

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
    

    def __generate_random_obstacles_and_dirt__(self, obstacle_density: float = 0.1, dirt_density: float = 0.1):
        x_max = self.grid_size["x"]
        y_max = self.grid_size["y"]

        # Generate all possible locations
        all_locations = [{'x': x, 'y': y} for x in range(x_max) for y in range(y_max)]
        
        # Shuffle to randomize locations
        np.random.shuffle(all_locations)
        
        total_locations = len(all_locations)
        
        # Calculate counts for obstacles and dirt
        max_obstacles = int(total_locations * obstacle_density)
        max_dirt = int(total_locations * dirt_density)
        
        # Select locations for obstacles
        obstacle_locations = all_locations[:max_obstacles]
        
        # Remove obstacle locations from all_locations
        remaining_locations = all_locations[max_obstacles:]
        
        # Select locations for dirt
        dirt_locations = remaining_locations[:max_dirt]
        
        return obstacle_locations, dirt_locations

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
    
    def __generate_random_dirty_locations__(self,
                                            dirt_density: float = 0.1):
        x_max = self.grid_size["x"]
        y_max = self.grid_size["y"]

        max_count = int(self.grid_size["x"] * self.grid_size["y"] * dirt_density)

        dirt_array = []

        def is_surrounded_by_obstacles(x, y):
            for direction, (dx, dy) in DIRECTIONS.items():
                # nx, ny = x + dx, y + dy
                if dx>0:
                    nx = min(self.environment.grid_size["x"]-1,x+dx)
                else:
                    nx = max(0, x+dx)
                if dy>0:
                    ny = min(self.environment.grid_size["y"]-1,y+dy)
                else:
                    ny = max(0, y+dy)
                if 0 <= nx < x_max and 0 <= ny < y_max:
                    if self.grid_descriptor.grid[nx][ny] != LOCATION_MARKERS["OBSTACLE"]:
                        return False  # Found at least one non-obstacle tile
            return True  # All surrounding tiles are obstacles

        for _ in range(max_count):
            while True:
                new_dirt_loc = {
                    "x": np.random.randint(0, x_max),
                    "y": np.random.randint(0, y_max)
                }

                # Ensure the dirt isn't encapsulated by obstacles
                if not is_surrounded_by_obstacles(new_dirt_loc["x"], new_dirt_loc["y"]):
                    dirt_array.append(new_dirt_loc)
                    break  # Exit the loop once a valid location is found

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
    
    def __get_global_dirty_locations__(self):
        global_dirty_locations = []
        for i in range(self.grid_size["y"]):
            for j in range(self.grid_size["x"]):
                if self.grid_descriptor.grid[i][j] == LOCATION_MARKERS["DIRT"]:
                    global_dirty_locations.append((i,j))
        return global_dirty_locations

    def __is_grid_clean__(self):
        if len(self.__get_global_dirty_locations__()) == 0:
            return True
        return False