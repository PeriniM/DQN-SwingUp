import numpy as np
import serial
import time
from Environments.SerialReader import SerialReader

class RealPendulum:
    """
    Real rotary pendulum with ESP32
    """
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.reader = SerialReader(self.ser)
        self.reader.start()
        self.name = "RealPendulum"
        self.nbJoint = 1
        self.num_state = 2
        self.state = np.zeros(self.num_state)
        self.iterCount = 0
        self.done = False
        self.homing = False
        self.omega_max = 10.0

    def normalize_state(self, state):

        normalized_angle = state[0] / np.pi  # Normalizes to [-1, 1]
        normalized_velocity = state[1] / self.omega_max  # Normalizes to [-1, 1]
        return np.array([normalized_angle, normalized_velocity])
    
    def reset(self):
        """
        Reset the environment to the initial state.
        """
        # Send command to pendulum to go to home position.
        self.send_serial("0,1")
        # Wait for the pendulum to report it has finished resetting.
        while (1):
            self.state, self.done = self.reader.get_state()
            if not self.done:
                break

        # Reset iteration count
        self.iterCount = 0
        normalized_state = self.normalize_state(self.state)
        return normalized_state

    def step(self, action):
        """
        Take a step in the environment.
        """
        while (1):
            self.state, self.done = self.reader.get_state()
            if self.done:
                self.homing = True
            else:
                break

        # Send action to pendulum if not in homing process.
        if not self.homing:
            self.send_serial(f"{action},0")
            # Read state and episode done flag from serial
            self.state, self.done = self.reader.get_state()

        # Calculate reward only when not homing.
        reward = self.calculate_reward(self.state)
        self.iterCount += 1
        
        # Check for end of episode based on iteration count.
        if self.iterCount >= self.maxIter:
            self.done = True
        if self.homing:
            self.done = True
            self.homing = False
        
        normalized_state = self.normalize_state(self.state)

        return normalized_state, reward, self.done

    def send_serial(self, command):
        """
        Send a command to the pendulum over serial.
        """
        self.ser.write(f"{command}\n".encode())
        time.sleep(0.1)

    def calculate_reward(self, state):

        # Constants to scale the angle and velocity penalties
        ANGLE_WEIGHT = 1.0
        VELOCITY_WEIGHT = 0.1  # Lower value since we want to give less weight to velocity
        ANGLE_TARGET = 0.0  # Upright position

        # Penalize the deviation of the angle from the upright position
        angle_deviation = np.abs(state[0] - ANGLE_TARGET)

        # The cosine of the angle can be used for a bounded reward, peaking at the upright position.
        # angle_penalty = ANGLE_WEIGHT * (1 - np.cos(angle))

        # Alternatively, a quadratic penalty is often used in control tasks
        angle_penalty = ANGLE_WEIGHT * (angle_deviation ** 2)

        # Penalize the angular velocity to prefer solutions that don't require much movement
        velocity_penalty = VELOCITY_WEIGHT * (state[1] ** 2)

        # Reward is higher when penalties are lower
        reward = -(angle_penalty + velocity_penalty)

        return reward

    def render(self):
        """
        Render the state (optional).
        """
        print("Connect the camera to the pendulum and display the video stream.")

    def close(self):
        """
        Close the serial connection.
        """
        self.ser.close()
