# traffic_manager.py
import pyfly
import numpy as np
import time

class TrafficManager:
    def __init__(self, player_aircraft_file="assets/aircraft/aircraft_x8.json"):
        self.aircraft = {}
        self.add_player_aircraft(player_aircraft_file)
        
    def add_player_aircraft(self, aircraft_file):
        player_id = "player"
        self.aircraft[player_id] = {
            "physics": pyfly.PyFly(parameter_file=aircraft_file),
            "model_path": "assets/models/cessna.obj"
        }
        
    def add_ai_aircraft(self, ai_id, aircraft_file, model_path):
        self.aircraft[ai_id] = {
            "physics": pyfly.PyFly(parameter_file=aircraft_file),
            "model_path": model_path
        }
        
    def update_all_aircraft(self, dt, player_controls):
        for aircraft_id, data in self.aircraft.items():
            if aircraft_id == "player":
                # Apply player controls
                data["physics"].set_input("throttle", player_controls.get("throttle", 0.0))
                data["physics"].set_input("aileron", player_controls.get("aileron", 0.0))
                data["physics"].set_input("elevator", player_controls.get("elevator", 0.0))
                data["physics"].set_input("rudder", player_controls.get("rudder", 0.0))
            else:
                # Apply AI controls (placeholder for now)
                data["physics"].set_input("throttle", 0.5)
                
            data["physics"].run_time_step(dt)
            data["state"] = data["physics"].get_state()

