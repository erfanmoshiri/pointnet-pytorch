def translate_pts(p, dx, dy):
    x = -1*p.x + dx
    y = -1*p.y + dy
    z = p.z
    return x, y, z

import os

def write_points_to_file(x, trans=False, dx=0, dy=0):
    print('Here 1')
    if trans:
        path = os.getcwd()
        print(path)
        pth = '/home/erfan/Personal/project/webots/world1/controllers/pioneer_pc_controller/points.pts'
        with open(pth, 'a') as f:
            for p in x:
                if 'inf' in str(p.x) or 'inf' in str(p.y) or 'inf' in str(p.z):
                    continue
                if p.z < -1.85:
                    continue
                x, y, z = translate_pts(p, dx, dy)
                f.write(f'{x:.5f} {y:.5f} {z:.5f}\n')
    else:
        print('Here 3')

        with open('points.pts', 'w') as f:
            for p in x:
                if 'inf' in str(p.x) or 'inf' in str(p.y) or 'inf' in str(p.z):
                    continue
                if p.z < -1.85:
                    continue
                f.write(f'{p.x:.5f} {p.y:.5f} {p.z:.5f}\n')


def run_robot(robot, trans=False, dx=0, dy=0):
    timestep = int(robot.getBasicTimeStep()) #32
    speed = 0


    left_m = robot.getDevice("left wheel motor")
    right_m = robot.getDevice("right wheel motor")
    
    left_m.setPosition(float('inf'))
    right_m.setPosition(float('inf'))
    
    left_m.setVelocity(0)
    right_m.setVelocity(0)

    # lidar
    lidar = robot.getDevice('lidar')
    lidar.enable(timestep)
    lidar.enablePointCloud()
    while robot.step(timestep) != -1:
        pass
        x = lidar.getPointCloud()    
        print('len', len(x))
        write_points_to_file(x, trans, dx, dy)
        break
