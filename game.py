
import pygame
import random
from heart import Heart

class Snake:
    def __init__(self, grid_size, window_width, window_height):
        self.grid_size = grid_size
        self.window_width = window_width
        self.window_height = window_height
        
        # Start in the middle
        start_x = (window_width // 2 // grid_size) * grid_size
        start_y = (window_height // 2 // grid_size) * grid_size
        
        self.body = [
            [start_x, start_y],
            [start_x - grid_size, start_y],
            [start_x - 2 * grid_size, start_y]
        ]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.grow = False
        self.color = (100, 200, 255)  # Light blue snake
        self.head_color = (50, 150, 255)  # Brighter blue head
        
    def move(self):
        """Move the snake in current direction"""
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head = self.body[0].copy()
        
        if self.direction == 'UP':
            head[1] -= self.grid_size
        elif self.direction == 'DOWN':
            head[1] += self.grid_size
        elif self.direction == 'LEFT':
            head[0] -= self.grid_size
        elif self.direction == 'RIGHT':
            head[0] += self.grid_size
        
        # Insert new head
        self.body.insert(0, head)
        
        # Remove tail if not growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, direction):
        """Change snake direction (prevent reversing)"""
        opposites = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }
        if direction != opposites.get(self.direction):
            self.next_direction = direction
    
    def check_collision(self):
        """Check if snake collides with itself or walls"""
        head = self.body[0]
        
        # Wall collision
        if (head[0] < 0 or head[0] >= self.window_width or
            head[1] < 0 or head[1] >= self.window_height):
            return True
        
        # Self collision (skip head)
        if head in self.body[1:]:
            return True
        
        return False
    
    def check_eat(self, heart):
        """Check if snake eats the heart"""
        head = self.body[0]
        heart_rect = heart.get_rect()
        head_rect = pygame.Rect(head[0], head[1], self.grid_size, self.grid_size)
        
        if head_rect.colliderect(heart_rect):
            self.grow = True
            return True
        return False
    
    def draw(self, screen):
        """Draw the snake"""
        for i, segment in enumerate(self.body):
            # Create rounded rectangle effect
            rect = pygame.Rect(segment[0], segment[1], self.grid_size, self.grid_size)
            
            # Head is different color
            if i == 0:
                color = self.head_color
                # Draw eyes on head
                pygame.draw.rect(screen, color, rect, border_radius=8)
                # Draw eyes
                eye_size = 4
                if self.direction == 'RIGHT':
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (segment[0] + self.grid_size - 6, segment[1] + 5), eye_size)
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (segment[0] + self.grid_size - 6, segment[1] + self.grid_size - 5), eye_size)
                elif self.direction == 'LEFT':
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (segment[0] + 6, segment[1] + 5), eye_size)
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (segment[0] + 6, segment[1] + self.grid_size - 5), eye_size)
                elif self.direction == 'UP':
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (segment[0] + 5, segment[1] + 6), eye_size)
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (segment[0] + self.grid_size - 5, segment[1] + 6), eye_size)
                else:  # DOWN
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (segment[0] + 5, segment[1] + self.grid_size - 6), eye_size)
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (segment[0] + self.grid_size - 5, segment[1] + self.grid_size - 6), eye_size)
            else:
                # Gradient effect on body
                color_value = max(100, 200 - (i * 3))
                color = (color_value, color_value, 255)
                pygame.draw.rect(screen, color, rect, border_radius=5)
    
    def reset(self):
        """Reset snake to initial state"""
        start_x = (self.window_width // 2 // self.grid_size) * self.grid_size
        start_y = (self.window_height // 2 // self.grid_size) * self.grid_size
        
        self.body = [
            [start_x, start_y],
            [start_x - self.grid_size, start_y],
            [start_x - 2 * self.grid_size, start_y]
        ]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.grow = False


class Game:
    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.font = None
        self.snake = Snake(grid_size, width, height)
        self.heart = None
        self.spawn_heart()
        
        # Load font
        try:
            self.font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 72)
        except:
            self.font = pygame.font.SysFont('Arial', 36)
            self.big_font = pygame.font.SysFont('Arial', 72)
        
        # Background pattern
        self.bg_color = (20, 20, 35)  # Dark blue-black
        self.grid_color = (40, 40, 60)  # Subtle grid lines
        
    def spawn_heart(self):
        """Spawn a new heart at random position"""
        while True:
            x = random.randint(0, (self.width // self.grid_size) - 1) * self.grid_size
            y = random.randint(0, (self.height // self.grid_size) - 1) * self.grid_size
            
            # Make sure heart doesn't spawn on snake
            if [x, y] not in self.snake.body:
                self.heart = Heart(x, y, self.grid_size)
                break
    
    def change_direction(self, direction):
        """Change snake direction"""
        if not self.game_over:
            self.snake.change_direction(direction)
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        # Move snake
        self.snake.move()
        
        # Check collisions
        if self.snake.check_collision():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return
        
        # Check if snake ate the heart
        if self.snake.check_eat(self.heart):
            self.score += 1
            self.spawn_heart()
            
            # Love message effect on score
            if self.score % 5 == 0:
                print(f"💕 {self.score} hearts of love! 💕")
    
    def reset(self):
        """Reset the game"""
        self.snake.reset()
        self.score = 0
        self.game_over = False
        self.spawn_heart()
    
    def draw(self, screen):
        """Draw everything on screen"""
        # Fill background
        screen.fill(self.bg_color)
        
        # Draw grid (subtle)
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(screen, self.grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(screen, self.grid_color, (0, y), (self.width, y))
        
        # Draw heart
        if self.heart:
            self.heart.draw(screen)
        
        # Draw snake
        self.snake.draw(screen)
        
        # Draw score
        score_text = self.font.render(f"💕 Love: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Draw high score
        high_text = self.font.render(f"🏆 Best: {self.high_score}", True, (255, 215, 0))
        screen.blit(high_text, (10, 50))
        
        # Draw controls hint
        hint_text = self.font.render("⬆⬇⬅➡  |  SPACE to restart", True, (150, 150, 150))
        screen.blit(hint_text, (10, self.height - 40))
        
        # Draw game over overlay
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = self.big_font.render("💔 Game Over", True, (255, 50, 80))
            text_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 50))
            screen.blit(game_over_text, text_rect)
            
            # Score text
            score_text = self.font.render(f"Your love: {self.score} hearts", True, (255, 200, 200))
            score_rect = score_text.get_rect(center=(self.width//2, self.height//2 + 20))
            screen.blit(score_text, score_rect)
            
            # Restart hint
            restart_text = self.font.render("Press SPACE to try again", True, (200, 200, 255))
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 70))
            screen.blit(restart_text, restart_rect)
        
        # Draw love message for milestones
        if self.score > 0 and self.score % 10 == 0 and not self.game_over:
            love_text = self.big_font.render(f"💕 {self.score} Hearts! 💕", True, (255, 100, 150))
            love_rect = love_text.get_rect(center=(self.width//2, self.height//2))
            # Fade effect
            alpha = abs(pygame.time.get_ticks() % 1000 - 500) / 500 * 255
            love_text.set_alpha(int(alpha))
            screen.blit(love_text, love_rect)