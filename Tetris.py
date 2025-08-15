import pygame
import random

pygame.init()
screen = pygame.display.set_mode((300, 600))
clock = pygame.time.Clock()
grid = [[0 for _ in range(10)] for _ in range(20)]
shapes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]
colors = [
    (0, 255, 255),  # I
    (255, 255, 0),  # O
    (128, 0, 128),  # T
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (0, 0, 255),    # L
    (255, 165, 0),  # J
]
current_shape = random.choice(shapes)
current_color = random.choice(colors)
shape_x, shape_y = 3, 0
score = 0
font = pygame.font.Font(None, 36)

def can_move(shape,x , y ):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell and (x+j <0 or x+j >= 10 or y+i >= 20 or (y+i >= 0 and grid[y+i][x+j])):
                return False
    return True

def place_shape():
    global current_shape, current_color, shape_x, shape_y, score
    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell:
                grid[shape_y + i][shape_x + j] = current_color
    for i in range(19,-1,-1):
        if all(grid[i]):
            del grid[i]
            grid.insert(0, [0 for _ in range(10)])
            score += 100
    # Try to spawn a new piece
    new_shape = random.choice(shapes)
    new_color = random.choice(colors)
    new_x, new_y = 3, 0
    if not can_move(new_shape, new_x, new_y):
        global running
        running = False
    else:
        current_shape = new_shape
        current_color = new_color
        shape_x, shape_y = new_x, new_y

running = True
fall_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and can_move(current_shape, shape_x - 1, shape_y):
                shape_x -= 1
            if event.key == pygame.K_RIGHT and can_move(current_shape, shape_x + 1, shape_y):
                shape_x += 1
            if event.key == pygame.K_DOWN and can_move(current_shape, shape_x, shape_y + 1):
                shape_y += 1
            if event.key == pygame.K_UP:
                # Rotate the shape clockwise
                rotated_shape = [list(row) for row in zip(*current_shape[::-1])]
                if can_move(rotated_shape, shape_x, shape_y):
                    current_shape = rotated_shape

    fall_time += clock.get_time()
    if fall_time >= 500:
        if can_move(current_shape, shape_x, shape_y + 1):
            shape_y += 1
        else:
            place_shape()
        fall_time = 0

    screen.fill((0, 0, 0))
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (j * 30, i * 30, 30, 30))
    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_color, ((shape_x + j) * 30, (shape_y + i) * 30, 30, 30))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()