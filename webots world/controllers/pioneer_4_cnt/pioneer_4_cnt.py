"""pioneer_pc_controller controller."""

from controller import Robot

def translate_pts(p, dx, dy):
    x = dx - p.y
    y = dy + p.x
    z = p.z
    return x, y, z

if __name__ == '__main__':
    pass
    robot = Robot()

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
        print('len4', len(x))
        
        # ------------------------------------
        pth = '/home/erfan/Personal/project/webots/world1/controllers/pioneer_pc_controller/points.pts'
        with open(pth, 'a') as f:
            for p in x:
                if 'inf' in str(p.x) or 'inf' in str(p.y) or 'inf' in str(p.z):
                    continue
                if p.z < -1.7:
                    continue
                x, y, z = translate_pts(p, 6, -6)
                f.write(f'{x:.5f} {y:.5f} {z:.5f}\n')
        # ------------------------------------

        break
    
    print('pioneer 4 finished successfully')
    