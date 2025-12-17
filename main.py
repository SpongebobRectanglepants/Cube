import pygame
import math
from settings import *
from cube import Cube

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Cube")
clock = pygame.time.Clock()

cube = Cube(CUBE_SIZE)

running = True
total_rotx = 0
total_roty = 0
mouseDown = False
lastMousePos = (0, 0)
DISTANCE = DEFAULT_DISTANCE

# --- Helper functions ---

def get_face_normal(p1, p2, p3):
    """Compute normal vector of a face (3 points)"""
    ux, uy, uz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    vx, vy, vz = p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]
    return (uy * vz - uz * vy,
            uz * vx - ux * vz,
            ux * vy - uy * vx)

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def normalize(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length == 0: return (0,0,0)
    return (v[0]/length, v[1]/length, v[2]/length)


# --- Main loop ---
while running:
    clock.tick(FPS)

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseDown = True
            lastMousePos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouseDown = False

        elif event.type == pygame.MOUSEMOTION and mouseDown:
            mousex, mousey = pygame.mouse.get_pos()
            dx = mousex - lastMousePos[0]
            dy = mousey - lastMousePos[1]
            total_roty += dx * 0.005
            total_rotx += dy * 0.005
            lastMousePos = (mousex, mousey)

        elif event.type == pygame.MOUSEWHEEL:
            DISTANCE -= event.y * 40
            DISTANCE = max(300, min(1200, DISTANCE))

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            DISTANCE = DEFAULT_DISTANCE
            cube.reset_points()
            total_rotx = 0
            total_roty = 0

    # --- Clear screen ---
    screen.fill(BACKGROUND)

    # --- Rotate cube ---
    cube.reset_points()
    cube.rotate_x(total_rotx)
    cube.rotate_y(total_roty)

    # --- Project points ---
    points2d = cube.project(WIDTH, HEIGHT, FOV, DISTANCE)

    # --- Lighting ---
    LIGHT_DIR = normalize((0, 0, 1))
    BASE_COLOR = (60, 120, 200)

    # --- Draw faces ---
    faces_to_draw = []

    for face in cube.faces:
        p1, p2, p3 = [cube.points[i] for i in face[:3]]
        normal = normalize(get_face_normal(p1, p2, p3))

        # Lighting
        brightness = 0.3 + 0.7 * abs(dot(normal, LIGHT_DIR))
        color = (
            int(BASE_COLOR[0] * brightness),
            int(BASE_COLOR[1] * brightness),
            int(BASE_COLOR[2] * brightness),
        )

        avg_z = sum(cube.points[i][2] for i in face) / 4
        faces_to_draw.append((avg_z, face, color))

    # Sort faces back-to-front
    faces_to_draw.sort(reverse=True)

    # Draw polygons
    for _, face, color in faces_to_draw:
        polygon = [points2d[i] for i in face]
        pygame.draw.polygon(screen, color, polygon)

    # --- Draw edges ---
    for edge in cube.edges:
        p1 = points2d[edge[0]]
        p2 = points2d[edge[1]]
        pygame.draw.line(screen, LINE_COLOR, p1, p2, 2)

    # --- Draw vertices ---
    if SHOW_VERTICIES:
        for p in points2d:
            pygame.draw.circle(screen, (255, 0, 0), (int(p[0]), int(p[1])), 4)

    pygame.display.flip()

pygame.quit()
