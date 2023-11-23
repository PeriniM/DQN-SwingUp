import pybullet as p
import os
import time
import pybullet_data
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,0]
cubeStartOrientation = p.getQuaternionFromEuler([3.1415/2,0,0])
dir = os.path.abspath(os.path.dirname(__file__))
robot_urdf = "Rotary_Pendulum_URDF.urdf"
dir = os.path.join(dir,'urdf')
robot_urdf=os.path.join(dir,robot_urdf)
robotId = p.loadURDF(robot_urdf,cubeStartPos, cubeStartOrientation, 
                   # useMaximalCoordinates=1, ## New feature in Pybullet
                   flags=p.URDF_USE_INERTIA_FROM_FILE,
                   useFixedBase=True
                   )

# Find the joint index
motor_joint_index = [p.getJointInfo(robotId, i)[1] for i in range(p.getNumJoints(robotId))].index(b'Revolute_3')
bar_joint_index = [p.getJointInfo(robotId, i)[1] for i in range(p.getNumJoints(robotId))].index(b'Revolute_5')

# Disable the motor
p.setJointMotorControl2(bodyUniqueId=robotId,
                        jointIndex=motor_joint_index,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=0,
                        force=0)
p.setJointMotorControl2(bodyUniqueId=robotId,
                        jointIndex=bar_joint_index,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=0,
                        force=0)

p.resetDebugVisualizerCamera(cameraDistance=0.4, cameraYaw=0, cameraPitch=-30, cameraTargetPosition=[0,0,0.1])

for i in range (10000):
    p.stepSimulation()
    time.sleep(1./240.)
cubePos, cubeOrn = p.getBasePositionAndOrientation(robotId)
print(cubePos,cubeOrn)
p.disconnect()

