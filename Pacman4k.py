import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 680
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)

PACMAN_RADIUS = 15
PELLET_RADIUS = 3
GHOST_SIZE = 30
WALL_THICKNESS = 5
PACMAN_SPEED = 4
GHOST_SPEED = 3
FPS = 60

# --- Game Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meow-Man (Pac-Man Style!)")
clock = pygame.time.Clock()

# --- Game Objects (Simplified) ---
# Pac-Man position
pacman_x = SCREEN_WIDTH // 2
pacman_y = SCREEN_HEIGHT // 2 + 50
pacman_dx = 0
pacman_dy = 0
pacman_mouth_angle = 45 # For drawing the mouth

# Ghost positions (using simple dicts for now)
ghosts = [
    {'x': SCREEN_WIDTH // 2 - 50, 'y': SCREEN_HEIGHT // 2 - 50, 'color': RED, 'dx': GHOST_SPEED, 'dy': 0},
    {'x': SCREEN_WIDTH // 2 + 50, 'y': SCREEN_HEIGHT // 2 - 50, 'color': PINK, 'dx': -GHOST_SPEED, 'dy': 0},
    {'x': SCREEN_WIDTH // 2 - 50, 'y': SCREEN_HEIGHT // 2 + 0, 'color': CYAN, 'dx': GHOST_SPEED, 'dy': 0},
    {'x': SCREEN_WIDTH // 2 + 50, 'y': SCREEN_HEIGHT // 2 + 0, 'color': ORANGE, 'dx': -GHOST_SPEED, 'dy': 0},
]

# Pellets (very simple grid for demonstration)
pellets = []
for r in range(50, SCREEN_HEIGHT - 50, 40):
    for c in range(50, SCREEN_WIDTH - 50, 40):
        pellets.append(pygame.Rect(c - PELLET_RADIUS, r - PELLET_RADIUS, PELLET_RADIUS*2, PELLET_RADIUS*2)) # Use Rect for collision

# Walls (very simplified boundaries)
walls = [
    pygame.Rect(0, 0, SCREEN_WIDTH, WALL_THICKNESS),
    pygame.Rect(0, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_WIDTH, WALL_THICKNESS),
    pygame.Rect(0, 0, WALL_THICKNESS, SCREEN_HEIGHT),
    pygame.Rect(SCREEN_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, SCREEN_HEIGHT),
    # Add more complex maze walls here later!
    pygame.Rect(100, 100, WALL_THICKNESS, 200),
    pygame.Rect(SCREEN_WIDTH-100-WALL_THICKNESS, 100, WALL_THICKNESS, 200),
]

# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_dx = -PACMAN_SPEED
                pacman_dy = 0
            elif event.key == pygame.K_RIGHT:
                pacman_dx = PACMAN_SPEED
                pacman_dy = 0
            elif event.key == pygame.K_UP:
                pacman_dx = 0
                pacman_dy = -PACMAN_SPEED
            elif event.key == pygame.K_DOWN:
                pacman_dx = 0
                pacman_dy = PACMAN_SPEED
        # Optional: Stop movement when key is released
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT and pacman_dx < 0: pacman_dx = 0
        #     if event.key == pygame.K_RIGHT and pacman_dx > 0: pacman_dx = 0
        #     if event.key == pygame.K_UP and pacman_dy < 0: pacman_dy = 0
        #     if event.key == pygame.K_DOWN and pacman_dy > 0: pacman_dy = 0

    # --- Game Logic ---
    # Move Pac-Man
    new_pacman_x = pacman_x + pacman_dx
    new_pacman_y = pacman_y + pacman_dy

    # Simple boundary check (replace with wall collision later)
    pacman_rect = pygame.Rect(new_pacman_x - PACMAN_RADIUS, new_pacman_y - PACMAN_RADIUS, PACMAN_RADIUS*2, PACMAN_RADIUS*2)
    can_move = True
    for wall in walls:
        if pacman_rect.colliderect(wall):
            can_move = False
            # Optional: Stop movement on collision
            # pacman_dx = 0
            # pacman_dy = 0
            break

    if can_move:
        pacman_x = new_pacman_x
        pacman_y = new_pacman_y

    # Keep Pac-Man on screen (basic wrap or stop)
    if pacman_x - PACMAN_RADIUS < 0: pacman_x = PACMAN_RADIUS
    if pacman_x + PACMAN_RADIUS > SCREEN_WIDTH: pacman_x = SCREEN_WIDTH - PACMAN_RADIUS
    if pacman_y - PACMAN_RADIUS < 0: pacman_y = PACMAN_RADIUS
    if pacman_y + PACMAN_RADIUS > SCREEN_HEIGHT: pacman_y = SCREEN_HEIGHT - PACMAN_RADIUS


    # Move Ghosts (very simple random movement for now)
    for ghost in ghosts:
        # Basic wall avoidance (needs improvement)
        potential_x = ghost['x'] + ghost['dx']
        potential_y = ghost['y'] + ghost['dy']
        ghost_rect = pygame.Rect(potential_x, potential_y, GHOST_SIZE, GHOST_SIZE)
        collided_with_wall = False
        for wall in walls:
             if ghost_rect.colliderect(wall):
                 collided_with_wall = True
                 break

        if collided_with_wall or random.random() < 0.01: # Change direction sometimes or on wall hit
            choices = [(GHOST_SPEED, 0), (-GHOST_SPEED, 0), (0, GHOST_SPEED), (0, -GHOST_SPEED)]
            # Prevent immediate reversal if possible
            if (-ghost['dx'], -ghost['dy']) in choices and len(choices) > 1:
                 choices.remove((-ghost['dx'], -ghost['dy']))
            new_dx, new_dy = random.choice(choices)
            ghost['dx'] = new_dx
            ghost['dy'] = new_dy
            # Recalculate potential position after changing direction
            potential_x = ghost['x'] + ghost['dx']
            potential_y = ghost['y'] + ghost['dy']
            ghost_rect = pygame.Rect(potential_x, potential_y, GHOST_SIZE, GHOST_SIZE)
            collided_with_wall = False # Recheck collision after direction change
            for wall in walls:
                if ghost_rect.colliderect(wall):
                    collided_with_wall = True
                    break

        if not collided_with_wall:
            ghost['x'] = potential_x
            ghost['y'] = potential_y
        else: # If still colliding after changing direction, just stop for this frame
             pass

        # Keep ghosts on screen (basic wrap or stop)
        if ghost['x'] < 0: ghost['x'] = 0; ghost['dx'] *= -1
        if ghost['x'] + GHOST_SIZE > SCREEN_WIDTH: ghost['x'] = SCREEN_WIDTH - GHOST_SIZE; ghost['dx'] *= -1
        if ghost['y'] < 0: ghost['y'] = 0; ghost['dy'] *= -1
        if ghost['y'] + GHOST_SIZE > SCREEN_HEIGHT: ghost['y'] = SCREEN_HEIGHT - GHOST_SIZE; ghost['dy'] *= -1

    # Pellet Collision
    pacman_collider = pygame.Rect(pacman_x - PACMAN_RADIUS, pacman_y - PACMAN_RADIUS, PACMAN_RADIUS*2, PACMAN_RADIUS*2)
    eaten_pellets = []
    for i, pellet_rect in enumerate(pellets):
        if pacman_collider.colliderect(pellet_rect):
            eaten_pellets.append(i)

    # Remove eaten pellets (iterate backwards to avoid index issues)
    for i in sorted(eaten_pellets, reverse=True):
        del pellets[i]
        # Add score later! Nya!

    # --- Drawing ---
    screen.fill(BLACK)

    # Draw Walls
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)

    # Draw Pellets
    for pellet_rect in pellets:
        pygame.draw.circle(screen, WHITE, pellet_rect.center, PELLET_RADIUS)

    # Draw Pac-Man
    # Calculate points for the Pac-Man shape with mouth
    points = []
    # Determine mouth direction based on movement
    if pacman_dx > 0: start_angle_rad = 0 + (pacman_mouth_angle / 2 * (3.14159 / 180.0))
    elif pacman_dx < 0: start_angle_rad = 3.14159 + (pacman_mouth_angle / 2 * (3.14159 / 180.0))
    elif pacman_dy > 0: start_angle_rad = 1.57079 + (pacman_mouth_angle / 2 * (3.14159 / 180.0))
    elif pacman_dy < 0: start_angle_rad = 4.71238 + (pacman_mouth_angle / 2 * (3.14159 / 180.0))
    else: start_angle_rad = 0 + (pacman_mouth_angle / 2 * (3.14159 / 180.0)) # Default right

    end_angle_rad = start_angle_rad + ((360 - pacman_mouth_angle) * (3.14159 / 180.0))

    # Simple circle if not moving or mouth angle is small
    if pacman_dx == 0 and pacman_dy == 0 or pacman_mouth_angle <= 5:
         pygame.draw.circle(screen, YELLOW, (int(pacman_x), int(pacman_y)), PACMAN_RADIUS)
    else:
        # Draw Pac-Man with Arc - Note: Pygame's arc drawing can be limited
        # We'll draw a filled circle and then cover the mouth segment with black
        pygame.draw.circle(screen, YELLOW, (int(pacman_x), int(pacman_y)), PACMAN_RADIUS)
        # Approximate mouth with a black triangle
        mouth_center_x = pacman_x + (PACMAN_RADIUS * 0.6 * (1 if pacman_dx >= 0 else -1) if pacman_dx != 0 else 0)
        mouth_center_y = pacman_y + (PACMAN_RADIUS * 0.6 * (1 if pacman_dy >= 0 else -1) if pacman_dy != 0 else 0)

        angle_rad = start_angle_rad - (pacman_mouth_angle / 2 * (3.14159 / 180.0)) # Midpoint angle of mouth opening
        tip_x = pacman_x + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate_rad(angle_rad).x
        tip_y = pacman_y + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate_rad(angle_rad).y

        corner1_angle_rad = start_angle_rad
        corner2_angle_rad = end_angle_rad

        corner1_x = pacman_x + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate_rad(corner1_angle_rad).x
        corner1_y = pacman_y + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate_rad(corner1_angle_rad).y
        corner2_x = pacman_x + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate_rad(corner2_angle_rad).x
        corner2_y = pacman_y + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate_rad(corner2_angle_rad).y

        #pygame.draw.polygon(screen, BLACK, [(pacman_x, pacman_y), (corner1_x, corner1_y), (corner2_x, corner2_y)])
        # More accurate pie slice drawing for mouth
        pygame.draw.arc(screen, BLACK, (pacman_x - PACMAN_RADIUS, pacman_y - PACMAN_RADIUS, PACMAN_RADIUS*2, PACMAN_RADIUS*2), start_angle_rad, end_angle_rad, PACMAN_RADIUS) # Draw black arc first
        pygame.draw.line(screen, BLACK, (pacman_x, pacman_y), (corner1_x, corner1_y), 2) # Line to one edge
        pygame.draw.line(screen, BLACK, (pacman_x, pacman_y), (corner2_x, corner2_y), 2) # Line to other edge



    # Draw Ghosts (simple rectangles for now)
    for ghost in ghosts:
        pygame.draw.rect(screen, ghost['color'], (ghost['x'], ghost['y'], GHOST_SIZE, GHOST_SIZE))
        # Add cute eyes later, nyaa!
        eye_offset_x = GHOST_SIZE // 4
        eye_offset_y = GHOST_SIZE // 3
        eye_radius = GHOST_SIZE // 8
        pygame.draw.circle(screen, WHITE, (int(ghost['x'] + eye_offset_x), int(ghost['y'] + eye_offset_y)), eye_radius)
        pygame.draw.circle(screen, WHITE, (int(ghost['x'] + GHOST_SIZE - eye_offset_x), int(ghost['y'] + eye_offset_y)), eye_radius)
        # Pupil (simple black dot)
        pupil_radius = eye_radius // 2
        pygame.draw.circle(screen, BLACK, (int(ghost['x'] + eye_offset_x), int(ghost['y'] + eye_offset_y)), pupil_radius)
        pygame.draw.circle(screen, BLACK, (int(ghost['x'] + GHOST_SIZE - eye_offset_x), int(ghost['y'] + eye_offset_y)), pupil_radius)


    # --- Update Display ---
    pygame.display.flip()

    # --- Frame Rate ---
    clock.tick(FPS) # Meow! 60 times per second!

# --- Quit Pygame ---
pygame.quit()
sys.exit()
