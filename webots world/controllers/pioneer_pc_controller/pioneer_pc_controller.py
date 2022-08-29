"""pioneer_pc_controller controller."""

from controller import Robot
from robot_utils import run_robot


if __name__ == '__main__':

    robot = Robot()
    run_robot(
        robot,
        trans=False,
        dx=0,
        dy=0
    )
    print('pioneer finished successfully')
