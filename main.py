# from Environments import Pendulum as pdl
from Environments import RealPendulum as real
from Environments import PyBulletPendulum as pb
from Environments import FakeEnv as fake
from DQN.Agent import Agent

isFake = False
isPyBullet = True
isReal = False
nJoints = 1

train = True
evaluate = False
plot_colormaps = False

# select the environment
if isFake:
    env = fake.FakeEnv(nJoints)
elif isPyBullet:
    env = pb.PyBulletPendulum()
elif isReal:
    env = real.RealPendulum("COM3", 115200)
else:
    env = pdl.Pendulum(nJoints)

# create the agent
dqn_agent = Agent(env)

if train:
    dqn_agent.train_model(render=True, plot=True, verbose=True, soft_start=False)

if evaluate:
    dqn_agent.evaluate_model(episodes=10, swingUp=True, render=True, verbose=True, final=False)

if plot_colormaps and nJoints == 1:
    dqn_agent.plot_value_policy('2D', resolution=100, final=False)