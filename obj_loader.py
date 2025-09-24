# obj_loader.py
import numpy as np

def load_obj(filename):
    vertices = []
    try:
        for line in open(filename, "r"):
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []
    
    return np.array(vertices, dtype=np.float32)

