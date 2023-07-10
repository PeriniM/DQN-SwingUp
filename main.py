from gepetto_pendulum import pendulum as pdl
from gepetto_pendulum import FakeEnv as fake
from DQN.Agent import Agent

isFake = False
nJoints = 1

train = False
evaluate = False
plot_colormaps = True

# select the environment
if isFake:
    env = fake.FakeEnv(nJoints)
else:
    env = pdl.Pendulum(nJoints)

# create the agent
dqn_agent = Agent(env)

if train:
    dqn_agent.train_model(render=False, plot=True, verbose=True, soft_start=False)

if evaluate:
    dqn_agent.evaluate_model(episodes=10, swingUp=True, render=True, verbose=True)

if plot_colormaps and nJoints == 1:
    dqn_agent.plot_value_policy('2D', resolution=100)