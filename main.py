# main.py
import pygame
import numpy as np
from config import *
from pyfly_wrapper import PyFlyWrapper
from renderer import Renderer

def main():
    # Initialize components
    physics_engine = PyFlyWrapper()
    renderer = Renderer()
    
    clock = pygame.time.Clock()
    
    # Control input dictionary
    controls = {
        "throttle": 0.0,
        "aileron": 0.0,
        "elevator": 0.0,
        "rudder": 0.0
    }

    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()
        
        # Throttle control
        if keys[pygame.K_UP]:
            controls["throttle"] = min(1.0, controls["throttle"] + THROTTLE_SENSITIVITY)
        if keys[pygame.K_DOWN]:
            controls["throttle"] = max(0.0, controls["throttle"] - THROTTLE_SENSITIVITY)
            
        # Aileron (roll) control
        if keys[pygame.K_LEFT]:
            controls["aileron"] = max(-1.0, controls["aileron"] - AILERON_SENSITIVITY)
        elif keys[pygame.K_RIGHT]:
            controls["aileron"] = min(1.0, controls["aileron"] + AILERON_SENSITIVITY)
        else:
            controls["aileron"] *= 0.9 # Smoothly return to neutral
            
        # Elevator (pitch) control
        if keys[pygame.K_w]:
            controls["elevator"] = min(1.0, controls["elevator"] + ELEVATOR_SENSITIVITY)
        elif keys[pygame.K_s]:
            controls["elevator"] = max(-1.0, controls["elevator"] - ELEVATOR_SENSITIVITY)
        else:
            controls["elevator"] *= 0.9
            
        # Rudder (yaw) control
        if keys[pygame.K_a]:
            controls["rudder"] = max(-1.0, controls["rudder"] - RUDDER_SENSITIVITY)
        elif keys[pygame.K_d]:
            controls["rudder"] = min(1.0, controls["rudder"] + RUDDER_SENSITIVITY)
        else:
            controls["rudder"] *= 0.9

        # --- Physics Update ---
        dt = clock.tick(FPS) / 1000.0  # Time step in seconds
        physics_engine.update(dt, controls)
        
        # --- Rendering ---
        aircraft_pos = physics_engine.get_position()
        aircraft_quat = physics_engine.get_orientation()
        renderer.render(aircraft_pos, aircraft_quat)

    pygame.quit()

if __name__ == "__main__":
    main()
