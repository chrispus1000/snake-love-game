
import pygame
import sys
from game import Game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Game settings
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    GRID_SIZE = 20
    FPS = 10
    
    # Create the game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("💕 Snake Love - Eat the Beating Heart! 💕")
    
    # Create game instance
    game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    game.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    game.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    game.change_direction('RIGHT')
                elif event.key == pygame.K_SPACE and game.game_over:
                    game.reset()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update game
        if not game.game_over:
            game.update()
        
        # Draw everything
        game.draw(screen)
        pygame.display.flip()
        
        # Control game speed
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()