# main.py
import pygame
import numpy as np
import asyncio
from config import *
from renderer import Renderer
from traffic_manager import TrafficManager

async def main():
    traffic_manager = TrafficManager()
    renderer = Renderer()
    
    # Add a sample AI plane
    traffic_manager.add_ai_aircraft(
        "ai_plane_1", 
        "assets/aircraft/aircraft_x8.json", 
        "assets/models/cessna.obj"
    )

    clock = pygame.time.Clock()
    controls = { "throttle": 0.0, "aileron": 0.0, "elevator": 0.0, "rudder": 0.0 }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()
        
        # Update player controls
        if keys[pygame.K_UP]: controls["throttle"] = min(1.0, controls["throttle"] + THROTTLE_SENSITIVITY)
        if keys[pygame.K_DOWN]: controls["throttle"] = max(0.0, controls["throttle"] - THROTTLE_SENSITIVITY)
        if keys[pygame.K_LEFT]: controls["aileron"] = max(-1.0, controls["aileron"] - AILERON_SENSITIVITY)
        elif keys[pygame.K_RIGHT]: controls["aileron"] = min(1.0, controls["aileron"] + AILERON_SENSITIVITY)
        else: controls["aileron"] *= 0.9
        if keys[pygame.K_w]: controls["elevator"] = min(1.0, controls["elevator"] + ELEVATOR_SENSITIVITY)
        elif keys[pygame.K_s]: controls["elevator"] = max(-1.0, controls["elevator"] - ELEVATOR_SENSITIVITY)
        else: controls["elevator"] *= 0.9
        if keys[pygame.K_a]: controls["rudder"] = max(-1.0, controls["rudder"] - RUDDER_SENSITIVITY)
        elif keys[pygame.K_d]: controls["rudder"] = min(1.0, controls["rudder"] + RUDDER_SENSITIVITY)
        else: controls["rudder"] *= 0.9

        dt = clock.tick(60) / 1000.0
        traffic_manager.update_all_aircraft(dt, controls)
        renderer.render(traffic_manager.aircraft)

        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
