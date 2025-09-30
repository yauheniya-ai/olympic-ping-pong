import pygame
import sys

# Initialize Pygame
pygame.init()

# Total window size (includes top score display of 200 height)
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ping Pong")

# Colors
BG_COLOR = "#0074c0"
TOP_SCORE_BG_COLOR = "#202a41"
LEFT_PADDLE_COLOR = "#8b76e9"
RIGHT_PADDLE_COLOR = "#0f172a"
BALL_COLOR = "white"
LINE_COLOR = (200, 200, 200)  # light gray
WHITE = (255, 255, 255)

# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

# Ball properties
BALL_SIZE = 15
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Score tracking
match_score_left = 11
match_score_right = 8
total_matches_left = 4
total_matches_right = 3

# Playing field dimensions and offset for top display
PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT = 900, 500
TOP_FIELD_HEIGHT = 200

# Starting positions (offset y by TOP_FIELD_HEIGHT)
left_paddle = pygame.Rect(50, TOP_FIELD_HEIGHT + PLAYFIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WINDOW_WIDTH - 50 - PADDLE_WIDTH, TOP_FIELD_HEIGHT + PLAYFIELD_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WINDOW_WIDTH // 2 - BALL_SIZE // 2, TOP_FIELD_HEIGHT + PLAYFIELD_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

clock = pygame.time.Clock()

# Fonts (adjust sizes relative to increase in top field)
score_font = pygame.font.SysFont(None, 160)  # Big font for match score (double previous)
matches_font = pygame.font.SysFont(None, 80)  # Smaller font for total matches (double previous)

def draw_text_outline(surface, font, text, color, outline_color, pos):
    # Render the base text surface
    base = font.render(text, True, color)
    # Render the outline text surface
    outline = font.render(text, True, outline_color)

    x, y = pos
    # Blit outline 8 times around base position for a solid outline
    for ox, oy in [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]:
        surface.blit(outline, (x+ox, y+oy))
    # Blit base text on top
    surface.blit(base, (x, y))

def move_paddles(keys):
    if keys[pygame.K_w] and left_paddle.top > TOP_FIELD_HEIGHT:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < WINDOW_HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > TOP_FIELD_HEIGHT:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < WINDOW_HEIGHT:
        right_paddle.y += PADDLE_SPEED

def move_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    if ball.top <= TOP_FIELD_HEIGHT or ball.bottom >= WINDOW_HEIGHT:
        BALL_SPEED_Y *= -1

    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        BALL_SPEED_X *= -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    move_paddles(keys)
    move_ball()

    # Draw background
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, TOP_SCORE_BG_COLOR, (0, 0, WINDOW_WIDTH, TOP_FIELD_HEIGHT))

    # Draw center lines in playing field (offset y by TOP_FIELD_HEIGHT)
    pygame.draw.rect(screen, LINE_COLOR, (WINDOW_WIDTH // 2 - 1, TOP_FIELD_HEIGHT, 3, PLAYFIELD_HEIGHT))
    pygame.draw.line(screen, LINE_COLOR, (0, TOP_FIELD_HEIGHT + PLAYFIELD_HEIGHT // 2), (WINDOW_WIDTH, TOP_FIELD_HEIGHT + PLAYFIELD_HEIGHT // 2), 1)

    # Draw paddles with 1 px white outline
    pygame.draw.rect(screen, WHITE, left_paddle.inflate(2, 2))
    pygame.draw.rect(screen, LEFT_PADDLE_COLOR, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle.inflate(2, 2))
    pygame.draw.rect(screen, RIGHT_PADDLE_COLOR, right_paddle)

    # Draw ball
    pygame.draw.ellipse(screen, BALL_COLOR, ball)

    # Draw match score (big numbers) with white outline
    left_score_text = f"{match_score_left:02d}"
    right_score_text = f"{match_score_right:02d}"

    vertical_offset = 20
    left_score_pos = (WINDOW_WIDTH // 4 - score_font.size(left_score_text)[0] // 2,
                      (TOP_FIELD_HEIGHT // 2 - score_font.get_height() // 2) + vertical_offset)
    right_score_pos = (WINDOW_WIDTH * 3 // 4 - score_font.size(right_score_text)[0] // 2,
                       (TOP_FIELD_HEIGHT // 2 - score_font.get_height() // 2) + vertical_offset)

    draw_text_outline(screen, score_font, left_score_text, pygame.Color(LEFT_PADDLE_COLOR), WHITE, left_score_pos)
    draw_text_outline(screen, score_font, right_score_text, pygame.Color(RIGHT_PADDLE_COLOR), WHITE, right_score_pos)

    # Draw total matches played separately with their colors and white outline and colon in white with outline
    total_left_text = str(total_matches_left)
    total_right_text = str(total_matches_right)
    colon_text = " : "

    total_left_surface = matches_font.render(total_left_text, True, pygame.Color(LEFT_PADDLE_COLOR))
    colon_surface = matches_font.render(colon_text, True, WHITE)
    total_right_surface = matches_font.render(total_right_text, True, pygame.Color(RIGHT_PADDLE_COLOR))

    total_left_rect = total_left_surface.get_rect()
    colon_rect = colon_surface.get_rect()
    total_right_rect = total_right_surface.get_rect()

    total_width = total_left_rect.width + colon_rect.width + total_right_rect.width
    start_x = WINDOW_WIDTH // 2 - total_width // 2
    center_y = TOP_FIELD_HEIGHT // 2 - 40

    total_left_pos = (start_x, center_y - total_left_rect.height // 2)
    colon_pos = (start_x + total_left_rect.width, center_y - colon_rect.height // 2)
    total_right_pos = (start_x + total_left_rect.width + colon_rect.width, center_y - total_right_rect.height // 2)

    # Use the same outline function for each text part
    draw_text_outline(screen, matches_font, total_left_text, pygame.Color(LEFT_PADDLE_COLOR), WHITE, total_left_pos)
    draw_text_outline(screen, matches_font, colon_text, WHITE, WHITE, colon_pos)
    draw_text_outline(screen, matches_font, total_right_text, pygame.Color(RIGHT_PADDLE_COLOR), WHITE, total_right_pos)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS
