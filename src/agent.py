"""
Module for Agent programs
"""
import random
from collections import deque
from src.common import euclidean_distance
from src.environment import Environment
from src.constants import (LOCATION_MARKERS,
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

    def __mark_agent_location__(self):
        # mark agent on grid
        self.environment.grid_descriptor.grid[self.current_position["x"]][self.current_position["y"]] = LOCATION_MARKERS["AGENT"]

    def __clear_agent_location__(self):
        # clear agent from grid
        self.environment.grid_descriptor.grid[self.current_position["x"]][self.current_position["y"]] \
            = LOCATION_MARKERS["CLEAN"]

    def __sense__(self):
        #scan surrounding
        # self.__scan_surrounding__()
        # self.__print_nearby_dirty_locations__()
        # self.__print_nearby_obstacles__()
        pass

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

        dirt_found = False

        if len(dirty_tiles)==0:
            # If no dirty tiles, move in a random direction
            dest = random.choice(clean_tiles)
        else:
            # choose a random dirty location
            dest = random.choice(dirty_tiles)
            dirt_found = True

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

    def __scan_surrounding__(self):

        #reset obstacles and dirt
        self.__reset_nearby_dirt__()
        self.__reset_nearby_obstacles__()

        start_x = max(self.current_position["x"]-self.sensor_range,0)
        start_y = max(self.current_position["y"]-self.sensor_range,0)
        end_x = min(self.current_position["x"]+self.sensor_range,self.environment.grid_size["x"]-1)
        end_y = min(self.current_position["y"]+self.sensor_range,self.environment.grid_size["y"]-1)

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
    
    def __reset_nearby_obstacles__(self):
        self.nearby_obstacles = []
    def __reset_nearby_dirt__(self):
        self.nearby_dirty_locations = []

    def __move__(self, loc: dict = {"x":0,"y":0}):

        # print(loc)

        # remove agent from current position on grid
        self.__clear_agent_location__()

        # update location ref of agent
        self.current_position["x"] = loc["x"]
        self.current_position["y"] = loc["y"]

        # place agent to desirec location on grid
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

    def __find_closest_tile__(self):
        if len(self.nearby_dirty_locations) > 0:
            self.target_location = min(self.nearby_dirty_locations,
                                    key=lambda d: d["distance"])
        else:
            # move in random direction
            pass

    def __find_path__(self,
                      start={"x":0,"y":0},
                      destination={"x":0,"y":0}):

        rows, cols = self.environment.grid_size["y"], self.environment.grid_size["x"]

        start_pos = (start["x"], start["y"])
        destination_pos = (destination["x"], destination["y"])

        # Define the boundary of the search space based on the sensor range
        min_x, max_x = max(0, start_pos[0] - self.sensor_range), min(rows, start_pos[0] + self.sensor_range)
        min_y, max_y = max(0, start_pos[1] - self.sensor_range), min(cols, start_pos[1] + self.sensor_range)


        queue = deque([start_pos])
        came_from = {start_pos:None}
        move_direction = {start_pos:None}

        temp_current = None

        while queue:
            temp_current = queue.popleft()

            if temp_current == destination_pos:
                break

            # choose random direction
            directions_list = list(DIRECTIONS.items())
            random.shuffle(directions_list)

            for direction, (dx,dy) in directions_list:
                if dx>0:
                    nx = min(self.environment.grid_size["x"],temp_current[0]+dx)
                else:
                    nx = max(0, temp_current[0]+dx)
                if dy>0:
                    ny = min(self.environment.grid_size["y"],temp_current[1]+dy)
                else:
                    ny = max(0, temp_current[1]+dy)

                if (min_x <= nx < max_x and 
                    min_y <= ny < max_y and 
                    self.environment.grid_descriptor.grid[nx][ny] != LOCATION_MARKERS["OBSTACLE"] and 
                    (nx, ny) not in came_from):
                    queue.append((nx,ny))
                    came_from[(nx,ny)] = temp_current
                    move_direction[(nx,ny)] = direction

        # If no path was found, move in a random direction within range and rescan
        if destination_pos not in came_from:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("No valid path found within range, moving randomly and updating target")

            # Filter out obstacle locations from potential directions
            valid_directions = [
                direction for direction, (dx, dy) in DIRECTIONS.items()
                if 0 <= temp_current[0] + dx < rows and 
                0 <= temp_current[1] + dy < cols and
                self.environment.grid_descriptor.grid[temp_current[0] + dx][temp_current[1] + dy] != LOCATION_MARKERS["OBSTACLE"]
            ]

            if valid_directions:
                random_move = random.choice(valid_directions)

                # Update target based on the chosen random move
                self.__update_target_based_on_random_move__({
                                                                "x": temp_current[0],
                                                                "y": temp_current[1]
                                                            }, random_move)

                return [random_move]  # Return the random move
            else:
                print("No valid random move available!")
                return []  # No valid moves

        # Reconstruct path
        path = []
        path_coordinates = []
        step = destination_pos
        while step != start_pos:
            # print("!",step)
            prev = came_from[step]
            if prev:
                path.append(move_direction[step])
                path_coordinates.append({
                    "x": step[0],
                    "y": step[1]
                })
                step = prev
        path.reverse()

        return path_coordinates

    def __update_target_based_on_random_move__(self, curr_loc:dict,random_move:str):
        if random_move[0] == "UP":
            self.target_location["x"]= curr_loc["x"]
            self.target_location["y"]= max(0,curr_loc["y"]-1)
            self.target_location["distance"]= euclidean_distance(curr_loc["x"],
                                                                 curr_loc["y"],
                                                                 self.target_location["x"],
                                                                 self.target_location["y"])
        elif random_move[0] == "DOWN":
            self.target_location["x"]= curr_loc["x"]
            self.target_location["y"]= min(self.environment.grid_size["y"],curr_loc["y"]+1)
            self.target_location["distance"]= euclidean_distance(curr_loc["x"],
                                                                 curr_loc["y"],
                                                                 self.target_location["x"],
                                                                 self.target_location["y"])
        elif random_move[0] == "LEFT":
            self.target_location["x"]= max(0,curr_loc["x"]-1)
            self.target_location["y"]= curr_loc["y"]
            self.target_location["distance"]= euclidean_distance(curr_loc["x"],
                                                                 curr_loc["y"],
                                                                 self.target_location["x"],
                                                                 self.target_location["y"])
        elif random_move[0] == "RIGHT":
            self.target_location["x"]= min(self.environment.grid_size["x"], curr_loc["x"]+1)
            self.target_location["y"]= curr_loc["y"]
            self.target_location["distance"]= euclidean_distance(curr_loc["x"],
                                                                 curr_loc["y"],
                                                                 self.target_location["x"],
                                                                 self.target_location["y"])
