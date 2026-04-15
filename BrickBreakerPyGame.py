# Import necessary modules
import pygame
import random
import sys

# Initialize all Pygame modules
pygame.init()

#Screen Settings
WIDTH, HEIGHT = 600, 500  # Window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the display window
pygame.display.set_caption("Brick Breaker")  # Set window title
clock = pygame.time.Clock()  # Create a clock to manage FPS
FPS = 60  # Frames per second

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

#Fonts
font = pygame.font.SysFont(None, 30)       # Regular font for score and buttons
large_font = pygame.font.SysFont(None, 50) # Large font for titles

# Game Element Sizes 
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
paddle_speed = 7  # Speed at which paddle moves

# Function: Draw Text 
def draw_text(text, font, color, surface, x, y):
    #Renders and centers text on the screen at (x, y)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    surface.blit(render, rect)

#Function: Draw Button
def draw_button(text, x, y, w, h, color, hover_color):
    #Creates a clickable button
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
        if click[0] == 1:  # Left mouse button click
            return True
    else:
        pygame.draw.rect(screen, color, rect)

    draw_text(text, font, BLACK, screen, x + w // 2, y + h // 2)
    return False

# Start Screen 
def start_screen():
    #Displays the start screen with the 'Start Game' button.
    while True:
        screen.fill(BLACK)
        draw_text("BRICK BREAKER", large_font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        
        # Start button
        if draw_button("Start Game", WIDTH // 2 - 75, HEIGHT // 2, 150, 50, GRAY, GREEN):
            pygame.time.delay(300)
            return
        
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Game Over Screen 
def game_over_screen(score):
    #Displays the Game Over screen and score with options to restart or exit.
    while True:
        screen.fill(BLACK)
        draw_text("Game Over", large_font, RED, screen, WIDTH // 2, HEIGHT // 3)
        draw_text(f"Final Score: {score}", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 20)

        # Restart button
        if draw_button("Start Again", WIDTH // 2 - 75, HEIGHT // 2 + 30, 150, 50, GRAY, GREEN):
            pygame.time.delay(300)
            return True  # Restart game

        # Exit button
        if draw_button("Exit", WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50, GRAY, RED):
            pygame.quit()
            sys.exit()

        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

#Main Game Loop
def main_game():
    #Handles the entire game logic, rendering, and interaction.
    
    # Create the paddle
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Create the ball
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_speed_x = 4 * random.choice((1, -1))  # Random horizontal direction
    ball_speed_y = -4  # Ball always starts moving upward

    # Create bricks
    BRICK_ROWS = 5
    BRICK_COLS = 8
    BRICK_WIDTH = WIDTH // BRICK_COLS
    BRICK_HEIGHT = 25
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 40, BRICK_WIDTH - 5, BRICK_HEIGHT - 5)
            bricks.append(brick)

    score = 0
    running = True

    while running:
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed_x *= -1
        if ball.top <= 0:
            ball_speed_y *= -1
        if ball.bottom >= HEIGHT:
            running = False  # Ball went off screen, end game

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_speed_y *= -1

        # Ball collision with bricks
        hit_index = ball.collidelist(bricks)
        if hit_index != -1:
            del bricks[hit_index]         # Remove the brick hit
            ball_speed_y *= -1            # Bounce the ball
            score += 10                   # Increase score

        #Drawing Everything
        screen.fill(BLACK)  # Clear the screen

        pygame.draw.rect(screen, BLUE, paddle)        # Draw paddle
        pygame.draw.ellipse(screen, WHITE, ball)      # Draw ball

        for brick in bricks:
            pygame.draw.rect(screen, RED, brick)      # Draw each brick

        draw_text(f"Score: {score}", font, WHITE, screen, 60, 20)  # Show score

        pygame.display.flip()  # Update the display

    # If game over
    restart = game_over_screen(score)
    if restart:
        main_game()  # Restart the game if player chooses to
start_screen()
main_game()