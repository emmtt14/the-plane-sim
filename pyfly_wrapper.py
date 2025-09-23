# pyfly_wrapper.py
import pyfly
import numpy as np

class PyFlyWrapper:
    def __init__(self, aircraft_file="aircraft_x8.json"):
        """Initializes the pyfly simulator with an aircraft model."""
        # PyFly comes with an example aircraft model for the Skywalker X8 UAV
        # You can find this file in the pyfly installation folder
        self.sim = pyfly.PyFly(parameter_file=aircraft_file)

        # Get initial state
        self.state = self.sim.get_state()

    def update(self, dt, control_inputs):
        """
        Runs one time step of the simulation.
        control_inputs is a dictionary with keys: throttle, aileron, elevator, rudder.
        """
        # Set the control inputs for the simulator
        self.sim.set_input("throttle", control_inputs.get("throttle", 0.0))
        self.sim.set_input("aileron", control_inputs.get("aileron", 0.0))
        self.sim.set_input("elevator", control_inputs.get("elevator", 0.0))
        self.sim.set_input("rudder", control_inputs.get("rudder", 0.0))

        # Run the simulation for one time step
        self.sim.run_time_step(dt)
        self.state = self.sim.get_state()

    def get_position(self):
        """Returns the aircraft's position (x, y, z)."""
        # Note: PyFly uses z-up, but OpenGL typically uses y-up.
        # We need to swap the axes for rendering.
        pos_array = self.state["pos_inertial"]
        return np.array([pos_array[0], pos_array[2], -pos_array[1]])

    def get_orientation(self):
        """Returns the aircraft's orientation as a quaternion."""
        return self.state["quat"]

    def reset(self):
        """Resets the simulation to its initial state."""
        self.sim.reset()
        self.state = self.sim.get_state()

