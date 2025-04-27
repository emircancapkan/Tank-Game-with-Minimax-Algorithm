import pygame
import random
import time
import sys

# --- Game area ---
TILE_SIZE = 40
ROWS = 15
COLS = 15
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Tank Game")
clock = pygame.time.Clock()

# Loading tank sprites
player_img = pygame.image.load('360_F_243103099_vsIDZgaQvobOKW8GGyIpQ0jxbfzmcJjO.jpg')
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
ai_img = pygame.image.load('360_F_484301605_l8x99s7uqY8D5N1h7ydt7a7ZSqqP1kcp.jpg')
ai_img = pygame.transform.scale(ai_img, (TILE_SIZE, TILE_SIZE))

# Tank class
class Tank:
    def __init__(self, x, y, image, is_player=True):
        self.x = x
        self.y = y
        self.image = image
        self.is_player = is_player
        self.direction = 'UP'

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS:
            if maze[new_y][new_x] == 0:
                self.x = new_x
                self.y = new_y
        if dx == -1:
            self.direction = 'LEFT'
        elif dx == 1:
            self.direction = 'RIGHT'
        elif dy == -1:
            self.direction = 'UP'
        elif dy == 1:
            self.direction = 'DOWN'

    def draw(self):
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        rotated_image = pygame.transform.rotate(self.image, {'UP':0, 'RIGHT':270, 'DOWN':180, 'LEFT':90}[self.direction])
        screen.blit(rotated_image, rect)

# Bullet class
class Bullet:
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.direction = direction
        self.owner = owner

    def move(self):
        if self.direction == 'UP':
            self.y -= 1
        elif self.direction == 'DOWN':
            self.y += 1
        elif self.direction == 'LEFT':
            self.x -= 1
        elif self.direction == 'RIGHT':
            self.x += 1

    def draw(self):
        rect = pygame.Rect(self.x * TILE_SIZE + TILE_SIZE//4, self.y * TILE_SIZE + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2)
        pygame.draw.rect(screen, (255, 255, 0), rect)

# Map
def generate_maze():
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for _ in range(20):  # walls (obstacles)
        wall_x = random.randint(0, COLS - 1)
        wall_y = random.randint(0, ROWS - 1)
        maze[wall_y][wall_x] = 1

    return maze

# AI vision
def ai_can_see_player():
    if ai_tank.y == player_tank.y:
        x_range = range(min(ai_tank.x, player_tank.x) + 1, max(ai_tank.x, player_tank.x))
        for x in x_range:
            if maze[ai_tank.y][x] == 1:
                return False
        ai_tank.direction = 'LEFT' if ai_tank.x > player_tank.x else 'RIGHT'
        return True
    if ai_tank.x == player_tank.x:
        y_range = range(min(ai_tank.y, player_tank.y) + 1, max(ai_tank.y, player_tank.y))
        for y in y_range:
            if maze[y][ai_tank.x] == 1:
                return False
        ai_tank.direction = 'UP' if ai_tank.y > player_tank.y else 'DOWN'
        return True
    return False

# AI movement
def ai_move():
    if ai_can_see_player():
        bullets.append(Bullet(ai_tank.x, ai_tank.y, ai_tank.direction, ai_tank))
    else:
        moves = [(-1,0), (1,0), (0,-1), (0,1)]
        random.shuffle(moves)
        for dx, dy in moves:
            new_x = ai_tank.x + dx
            new_y = ai_tank.y + dy
            if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
                ai_tank.move(dx, dy)
                break

# Start maze and the tanks
def reset_game():
    global maze, player_tank, ai_tank, bullets, player_turn, game_over, result_text
    maze = generate_maze()
    player_tank = Tank(1, 1, player_img, is_player=True)
    ai_tank = Tank(COLS - 2, ROWS - 2, ai_img, is_player=False)
    bullets = []
    player_turn = True
    game_over = False
    result_text = ""

reset_game()

# Draw maze
def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, GRAY, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

# Restart function
def draw_restart_button():
    font = pygame.font.SysFont(None, 48)
    button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50)
    pygame.draw.rect(screen, (0, 200, 0), button_rect)
    text = font.render("Restart", True, WHITE)
    screen.blit(text, (button_rect.x + 40, button_rect.y + 5))
    return button_rect

# Game loop
game_over = False
result_text = ""
running = True
while running:
    screen.fill(WHITE)
    draw_maze()
    player_tank.draw()
    ai_tank.draw()

    for bullet in bullets:
        bullet.draw()

    if game_over:
        font = pygame.font.SysFont(None, 72)
        text = font.render(result_text, True, (255,0,0))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()))
        button_rect = draw_restart_button()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()

        if player_turn:
            moved = False
            if keys[pygame.K_LEFT]:
                player_tank.move(-1, 0)
                moved = True
            if keys[pygame.K_RIGHT]:
                player_tank.move(1, 0)
                moved = True
            if keys[pygame.K_UP]:
                player_tank.move(0, -1)
                moved = True
            if keys[pygame.K_DOWN]:
                player_tank.move(0, 1)
                moved = True
            if keys[pygame.K_SPACE]:
                bullets.append(Bullet(player_tank.x, player_tank.y, player_tank.direction, player_tank))

            if moved:
                player_turn = False
                time.sleep(0.1)
        else:
            ai_move()
            player_turn = True
            time.sleep(0.1)

        # Move the bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.x < 0 or bullet.x >= COLS or bullet.y < 0 or bullet.y >= ROWS:
                bullets.remove(bullet)
                continue
            if maze[bullet.y][bullet.x] == 1:
                bullets.remove(bullet)
                continue
            if bullet.owner.is_player and bullet.x == ai_tank.x and bullet.y == ai_tank.y:
                result_text = "WIN"
                game_over = True
            if not bullet.owner.is_player and bullet.x == player_tank.x and bullet.y == player_tank.y:
                result_text = "LOSE"
                game_over = True

    clock.tick(30)

pygame.quit()
sys.exit()
