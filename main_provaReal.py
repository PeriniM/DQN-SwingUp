from Environments import RealPendulum as real

env = real.RealPendulum("COM3", 115200)
env.reset()
direction = 1
speed = 100 # 20% of max speed
while True:
    env.step(direction*speed)
    if env.done:
        direction *= -1
        env.reset()