# renderer.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from config import *

class Renderer:
    def __init__(self, model_path="simple_plane.obj"):
        pygame.init()
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
        self.setup_scene()
        self.model_vertices = self.load_obj(model_path)

    def setup_scene(self):
        """Configures the OpenGL viewport and projection."""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, (SCREEN_WIDTH / SCREEN_HEIGHT), NEAR_CLIP, FAR_CLIP)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def load_obj(self, filename):
        """Loads a wavefront .obj file and returns a list of vertices."""
        vertices = []
        try:
            for line in open(filename, "r"):
                if line.startswith('v '):
                    vertices.append(list(map(float, line.strip().split()[1:])))
            print(f"Loaded {len(vertices)} vertices from {filename}")
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Using default triangle.")
            return np.array([
                [1.0, 0.0, 0.0],  # Nose
                [-1.0, 0.5, 0.0], # Left wing
                [-1.0, -0.5, 0.0] # Right wing
            ], dtype=np.float32).tolist()
        return vertices

    def draw_aircraft(self, position, quaternion):
        """Draws the aircraft model at the specified position and orientation."""
        glPushMatrix()
        
        glTranslatef(position[0], position[1], position[2])
        
        q = quaternion
        rot_matrix = [
            1 - 2*q[2]**2 - 2*q[3]**2, 2*q[1]*q[2] - 2*q[0]*q[3], 2*q[1]*q[3] + 2*q[0]*q[2], 0.0,
            2*q[1]*q[2] + 2*q[0]*q[3], 1 - 2*q[1]**2 - 2*q[3]**2, 2*q[2]*q[3] - 2*q[0]*q[1], 0.0,
            2*q[1]*q[3] - 2*q[0]*q[2], 2*q[2]*q[3] + 2*q[0]*q[1], 1 - 2*q[1]**2 - 2*q[2]**2, 0.0,
            0.0, 0.0, 0.0, 1.0
        ]
        glMultMatrixf(rot_matrix)

        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        for vertex in self.model_vertices:
            glVertex3fv(vertex)
        glEnd()

        glPopMatrix()

    def draw_ground(self):
        """Draws a simple ground plane."""
        glColor3f(GROUND_COLOR[0], GROUND_COLOR[1], GROUND_COLOR[2])
        glBegin(GL_QUADS)
        glVertex3f(-100000.0, 0.0, -100000.0)
        glVertex3f(100000.0, 0.0, -100000.0)
        glVertex3f(100000.0, 0.0, 100000.0)
        glVertex3f(-100000.0, 0.0, 100000.0)
        glEnd()

    def render(self, aircraft_position, aircraft_quaternion):
        """Handles the main rendering loop, including camera setup."""
        glClearColor(SKY_COLOR[0], SKY_COLOR[1], SKY_COLOR[2], SKY_COLOR[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Position the camera relative to the aircraft
        camera_pos = aircraft_position - np.array([0, -10, CAMERA_DISTANCE])
        camera_target = aircraft_position
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  camera_target[0], camera_target[1], camera_target[2],
                  0, 1, 0)
        
        self.draw_ground()
        self.draw_aircraft(aircraft_position, aircraft_quaternion)

        pygame.display.flip()


