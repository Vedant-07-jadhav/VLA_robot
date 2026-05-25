import pybullet as p
import pybullet_data
import time


def move_to_target(robotId, target_position):
    end_effector_index = 11

    target_orientation = p.getQuaternionFromEuler([3.14, 0, 0])

    joint_poses = p.calculateInverseKinematics(
        robotId,
        end_effector_index,
        target_position,
        target_orientation
    )

    arm_joint_indices = [0,1,2,3,4,5,6]

    for i, joint_index in enumerate(arm_joint_indices):

        p.setJointMotorControl2(
            bodyIndex=robotId,
            jointIndex=joint_index,
            controlMode=p.POSITION_CONTROL,
            targetPosition=joint_poses[i],
            force=500
        )

def main():

    physicsClient = p.connect(p.GUI)
    p.setRealTimeSimulation(0)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    p.setGravity(0, 0, -9.81)

    planeId = p.loadURDF("plane.urdf")

    start_pos = [0, 0, 0]
    start_orientation = p.getQuaternionFromEuler([0, 0, 0])

    robotId = p.loadURDF(
        "franka_panda/panda.urdf",
        start_pos,
        start_orientation,
        useFixedBase=True
    )

    print(f"Successfully loaded Franka Panda!! RobotId = {robotId}")
    
    for i in range(p.getNumJoints(robotId)):
        print(p.getJointInfo(robotId, i))

    try:

        while True:

            move_to_target(robotId, [0.5, 0.0, 0.5])

            p.stepSimulation()

            time.sleep(1. / 240.)

    except KeyboardInterrupt:

        print("\nDisconnecting...")

        p.disconnect()


if __name__ == "__main__":
    main()