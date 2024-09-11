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
