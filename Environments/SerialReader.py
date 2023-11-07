import threading
import time
import numpy as np

class SerialReader(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.daemon = True  # Set thread as daemon so it will end with the main program
        self.state = np.zeros(2)
        self.episode_done = False
        self.lock = threading.Lock()  # Lock to prevent simultaneous read/write of state

    def run(self):
        while True:
            if self.ser.in_waiting:
                line = self.ser.readline().decode().strip()
                parts = line.split(',')
                if len(parts) == 3:
                    with self.lock:
                        self.state = np.array([float(parts[0]), float(parts[1])])
                        self.episode_done = bool(float(parts[2]))
                        # print(self.state, self.episode_done)

    def get_state(self):
        time.sleep(0.1)
        with self.lock:
            return self.state.copy(), self.episode_done
