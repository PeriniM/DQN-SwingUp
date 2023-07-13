import serial
import time
import numpy as np

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 9800, timeout=1, parity=serial.PARITY_NONE) # Establish the connection on a specific port
time.sleep(2)

# Define a global variable to store the start time of the program
start_time = time.perf_counter()

# Define a function to return the elapsed time in milliseconds
def millis():
    return round((time.perf_counter() - start_time) * 1000)

speed_range = [-150, 150]
action_steps = 51
action = np.linspace(speed_range[0], speed_range[1], action_steps)
action_space = [i for i in range(action_steps)]

data2send = 'r\n'

while True:
    time_millis = millis()
    # read the serial every 10 milliseconds
    if time_millis % 5 == 0:
        # read the serial data
        data = ser.readline()
        if data:
            # decode the data from
            data = data.decode('latin-1').rstrip()
            # if data is different than 'r', then it is the data from the arduino
            if data != data2send:
                # split the data into theta, theta_dot, and done_limit
                theta, theta_dot, done_limit = data.split(',')
                # convert the data to float
                # remove all the characters except the digits and the decimal point and the minus sign
                theta = ''.join(c for c in theta if c.isdigit() or c == '.' or c == '-')
                # if there is a minus sign and a number right after it, keep only the last 5 characters
                if '-' in theta and theta[theta.index('-') + 1].isdigit():
                    theta = theta[-5:]
                theta = float(theta)
                theta_dot = float(theta_dot)
                done_limit = int(done_limit)
                print(theta,theta_dot,done_limit)
              
                # print time it took to get the data from the arduino
                # print('Time: ', millis() - time_millis)
        
        # send the data to the arduino every 100 milliseconds
        if time_millis % 10 == 0:
            # take a random number from the action space
            action_index = np.random.choice(action_space)
            # send the action to the arduino
            data2send = str(action[action_index]) + '\n'
            ser.write(data2send.encode('utf-8'))

ser.close()