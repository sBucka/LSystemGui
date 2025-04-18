custom_tree = {
    "axiom": "0", 
    "variables": {"var1": "1", "var2": "0"},  
    "rules": {"r1": "11", "r2": "1[0]0"},
    "settings": {"angle": 45, "distance": 2, "headingAngle": 90, "turnLeftStack": 45, "turnRightStack": 45}, 
    "goto": {"x": 0, "y": -200}
} 

custom_triangles = {
    "axiom": "F",
    "variables": {"var1": "F", "var2": "f"},
    "rules": {"r1": "F-F++F-F", "r2": "F"},
    "settings": {"angle": 60, "distance": 5, "headingAngle": 0, "turnLeftStack": 0, "turnRightStack": 0},
    "goto" : {"x": 0, "y": 0}
}

custom_koch_curve = {
    "axiom": "F",
    "variables": {"var1": "F", "var2": "f"},
    "rules": {"r1": "F+F-F-F+F", "r2": "F"},
    "settings": {"angle": 90, "distance": 5, "headingAngle": 0, "turnLeftStack": 0, "turnRightStack": 0},
    "goto" : {"x": -220, "y": 0}
}

custom_sierpinski = {
    "axiom": "F-G-G",
    "variables": {"var1": "F", "var2": "G"},
    "rules": {"r1": "F-G+F+G-F", "r2": "GG"},
    "settings": {"angle": 120, "distance": 5, "headingAngle": 0, "turnLeftStack": 0, "turnRightStack": 0},
}

custom_dragon_curve = {
    "axiom": "FX",
    "variables": {"var1": "X", "var2": "Y"},
    "rules": {"r1": "X+YF+", "r2": "-FX-Y"},
    "settings": {"angle": 90, "distance": 5, "headingAngle": 0, "turnLeftStack": 0, "turnRightStack": 0},
    "goto" : {"x": 0, "y": -200}
    
}

custom_fractal_plant = {
    "axiom": "TF",
    "variables": {"var1": "T", "var2": "F"},
    "rules": {"r1":  "F+[[T]-T]-F[-FT]+T", "r2": "FF"},
    "settings": {"angle": 25, "distance": 5, "headingAngle": 90, "turnLeftStack": 0, "turnRightStack": 0},
    "goto" : {"x": 0, "y": -200}
}
systems = {
    "Binary Tree": custom_tree,
    "Triangles": custom_triangles,
    "Koch Curve": custom_koch_curve,
    "Sierpinski Triangle": custom_sierpinski,
    "Dragon Curve": custom_dragon_curve,
    "Fractal Plant": custom_fractal_plant
}

def get_systems():
    """Return the systems dictionary."""
    return systems