import pygame, sys, random

pygame.init()

# Suara (opsional)
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
except:
    eat_sound = None

# ====== KONSTANTA ======
WINDOW_X = 600
WINDOW_Y = 400
BLOCK = 10

game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption("Snake with Extra Apple")

fps = pygame.time.Clock()

# ====== KELAS GAMEOBJECT ======
class GameObject:
    def __init__(self, color, position):
        self.color = color
        self.position = position
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(
            self.position[0], self.position[1], BLOCK, BLOCK
        ))

# ====== KELAS SNAKE ======
class Snake(GameObject):
    def __init__(self):
        super().__init__((0, 255, 0), [100, 50])
        self.body = [
            [100, 50],
            [90, 50],
            [80, 50]
        ]
        self.direction = 'RIGHT'
        self.change_to = self.direction
    
    def change_direction(self, key):
        if key == pygame.K_UP and self.direction != 'DOWN':
            self.change_to = 'UP'
        if key == pygame.K_DOWN and self.direction != 'UP':
            self.change_to = 'DOWN'
        if key == pygame.K_LEFT and self.direction != 'RIGHT':
            self.change_to = 'LEFT'
        if key == pygame.K_RIGHT and self.direction != 'LEFT':
            self.change_to = 'RIGHT'
    
    def move(self):
        self.direction = self.change_to
        
        if self.direction == 'UP':
            self.position[1] -= BLOCK
        if self.direction == 'DOWN':
            self.position[1] += BLOCK
        if self.direction == 'LEFT':
            self.position[0] -= BLOCK
        if self.direction == 'RIGHT':
            self.position[0] += BLOCK
        
        self.body.insert(0, list(self.position))
    
    def shrink(self):
        self.body.pop()
    
    def draw(self, surface):
        for pos in self.body:
            pygame.draw.rect(surface, (0, 255, 0),
                             pygame.Rect(pos[0], pos[1], BLOCK, BLOCK))
    
    def check_collision(self):
        # dinding
        if self.position[0] < 0 or self.position[0] > WINDOW_X - BLOCK:
            return True
        if self.position[1] < 0 or self.position[1] > WINDOW_Y - BLOCK:
            return True
        
        # tubuh sendiri
        if self.position in self.body[1:]:
            return True
        
        return False

# ====== KELAS APPLE ======
class Apple(GameObject):
    def __init__(self, color):
        self.color = color
        self.respawn()
    
    def respawn(self):
        self.position = [
            random.randrange(1, WINDOW_X // BLOCK) * BLOCK,
            random.randrange(1, WINDOW_Y // BLOCK) * BLOCK
        ]

# ====== KELAS GAME ======
class Game:
    def __init__(self):
        self.snake = Snake()
        self.apple1 = Apple((255, 0, 0))   # merah
        self.apple2 = Apple((0, 0, 255))   # biru (Tugas)
        self.score = 0
    
    def show_score(self):
        font = pygame.font.SysFont("Arial", 20)
        score_surface = font.render(f"Score: {self.score}", True, (255, 255, 255))
        game_window.blit(score_surface, (10, 10))
    
    def game_over(self):
        font = pygame.font.SysFont("Arial", 35)
        over = font.render("GAME OVER", True, (255, 0, 0))
        game_window.blit(over, (WINDOW_X//2 - 100, WINDOW_Y//2 - 20))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    self.snake.change_direction(event.key)
            
            # gerak ular
            self.snake.move()
            
            # snake makan apple1
            if self.snake.position == self.apple1.position:
                self.score += 1
                if eat_sound: eat_sound.play()
                self.apple1.respawn()
            # snake makan apple2
            elif self.snake.position == self.apple2.position:
                self.score += 1
                if eat_sound: eat_sound.play()
                self.apple2.respawn()
            else:
                self.snake.shrink()
            
            if self.snake.check_collision():
                self.game_over()
            
            game_window.fill((0, 0, 0))
            
            self.snake.draw(game_window)
            self.apple1.draw(game_window)
            self.apple2.draw(game_window)
            self.show_score()
            
            pygame.display.update()
            fps.tick(15)

# ====== JALANKAN GAME ======
Game().run()
  