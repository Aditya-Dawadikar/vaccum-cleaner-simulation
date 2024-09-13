"""
Module for common functions
"""

def euclidean_distance(x1,y1,x2,y2,rounded=True):
    ed = pow(pow(x2-x1,2)+pow(y2-y1,2),0.5)
    if rounded == True:
        return round(ed,2)
    return ed

def manhatten_distance(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)


def check_dirt_obstacle_overlap(dirt, obstacles):
        dirt_set = {(d["x"], d["y"]) for d in dirt}
        obstacle_set = {(o["x"], o["y"]) for o in obstacles}

        overlaps = dirt_set & obstacle_set
        if overlaps:
            print(f"Overlap detected at locations: {overlaps}")
        else:
            print("No overlaps between dirt and obstacles.")
        return overlaps
    