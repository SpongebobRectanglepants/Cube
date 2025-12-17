import math

class Pyramid:
    def __init__(self, size, height=None):
        s = size / 2
        self.height = height if height is not None else size

        self.base_points = [
            [-s, -s, 0],  
            [ s, -s, 0],  
            [ s,  s, 0],  
            [-s,  s, 0],  
            [ 0,  0, self.height],  
        ]
        self.points = [p[:] for p in self.base_points]

        self.edges = [
            (0,1), (1,2), (2,3), (3,0), 
            (0,4), (1,4), (2,4), (3,4)   
        ]

        self.faces = [
            (0,1,2,3),  # base
            (0,1,4),    # side 1
            (1,2,4),    # side 2
            (2,3,4),    # side 3
            (3,0,4),    # side 4
        ]

    def reset_points(self):

        self.points = [p[:] for p in self.base_points]

    def rotate_x(self, angle):
        for p in self.points:
            y = p[1] * math.cos(angle) - p[2] * math.sin(angle)
            z = p[1] * math.sin(angle) + p[2] * math.cos(angle)
            p[1], p[2] = y, z

    def rotate_y(self, angle):
        for p in self.points:
            x = p[0] * math.cos(angle) + p[2] * math.sin(angle)
            z = -p[0] * math.sin(angle) + p[2] * math.cos(angle)
            p[0], p[2] = x, z

    def rotate_z(self, angle):
        for p in self.points:
            x = p[0] * math.cos(angle) - p[1] * math.sin(angle)
            y = p[0] * math.sin(angle) + p[1] * math.cos(angle)
            p[0], p[1] = x, y

    def project(self, width, height, fov, distance):
        projectedPoints = []
        for x, y, z in self.points:
            scale = fov / (distance + z)
            x2d = x * scale + width / 2
            y2d = y * scale + height / 2
            projectedPoints.append((x2d, y2d))
        return projectedPoints
