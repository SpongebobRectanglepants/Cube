import math

class Cube:
    def __init__(self, size):
        s = size / 2
        self.base_points = [ # 8 vertices of a cube (x, y, z)
            [-s, -s, -s],  # 0
            [ s, -s, -s],  # 1
            [ s,  s, -s],  # 2
            [-s,  s, -s],  # 3
            [-s, -s,  s],  # 4
            [ s, -s,  s],  # 5
            [ s,  s,  s],  # 6
            [-s,  s,  s],  # 7
        ]
        self.points = [p[:] for p in self.base_points]

        self.edges = [
            (0,1), (1,2), (2,3), (3,0),  
            (4,5), (5,6), (6,7), (7,4),  
            (0,4), (1,5), (2,6), (3,7)   
        ]

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        # Corrected face definitions (counter-clockwise winding)
        self.faces = [
            (0, 1, 2, 3),  # back 
            (4, 5, 6, 7),  # front 
            (0, 3, 7, 4),  # left 
            (1, 5, 6, 2),  # right 
            (0, 4, 5, 1),  # bottom 
            (3, 7, 6, 2),  # top 
        ]

    def reset_points(self): # Reset points to the original cube coordinates
        self.points = [p[:] for p in self.base_points]

    def rotate_x(self, angle): # Rotate all points around the X axis
        for p in self.points:
            y = p[1] * math.cos(angle) - p[2] * math.sin(angle)
            z = p[1] * math.sin(angle) + p[2] * math.cos(angle)
            p[1], p[2] = y, z

    def rotate_y(self, angle): # Rotate all points around the Y axis
        for p in self.points:
            x = p[0] * math.cos(angle) + p[2] * math.sin(angle)
            z = -p[0] * math.sin(angle) + p[2] * math.cos(angle)
            p[0], p[2] = x, z

    def rotate_z(self, angle): # Rotate all points around the Z axis
        for p in self.points:
            x = p[0] * math.cos(angle) - p[1] * math.sin(angle)
            y = p[0] * math.sin(angle) + p[1] * math.cos(angle)
            p[0], p[1] = x, y

    def project(self, width, height, fov, distance): # Project 3D points to 2D screen coordinates
        projectedPoints = []
        for x, y, z in self.points:
            scale = fov / (distance + z)
            x2d = x * scale + width / 2
            y2d = y * scale + height / 2
            projectedPoints.append((x2d, y2d))
        return projectedPoints
