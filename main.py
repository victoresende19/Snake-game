import pygame
import random
import asyncio

# Inicialização do Pygame
pygame.init()

# Definição das cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (204, 204, 0)
RED = (255, 0, 0)

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Direções
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Sons
apple_sound = pygame.mixer.Sound("brilho.wav")

# Classe Snake
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = YELLOW

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLACK, (p[0], p[1], GRID_SIZE, GRID_SIZE), 1)  # Adicionando contorno preto

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

# Classe Apple
class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2), GRID_SIZE // 2)
        pygame.draw.circle(surface, BLACK, (self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2), GRID_SIZE // 2, 1)  

async def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake game")

    background_image = pygame.image.load("jungle.jpg").convert()

    snake = Snake()
    apple = Apple()

    clock = pygame.time.Clock()

    while True:
        screen.blit(background_image, (0, 0))
        snake.handle_keys()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            apple_sound.play()  

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(5)
        await asyncio.sleep(0)

asyncio.run(main())
