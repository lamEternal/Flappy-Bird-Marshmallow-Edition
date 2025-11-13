import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 480, 720
TITLE = "Flappy Bird Marshmallow Edition"
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Consolas', 40)
m_font = pygame.font.SysFont('Consolas', 25)

# BACKGROUND

bg_img_0 = pygame.image.load("src/bg_3.png").convert()
bg_img_0 = pygame.transform.scale(bg_img_0, (WIDTH, HEIGHT))

bg_img_1 = pygame.image.load("src/bg_01.jpg").convert()
bg_img_1 = pygame.transform.scale(bg_img_1, (WIDTH, HEIGHT))

bg_img_2 = pygame.image.load("src/bg_02.png").convert()
bg_img_2 = pygame.transform.scale(bg_img_2, (WIDTH, HEIGHT))

bg_img_3 = pygame.image.load("src/bg_4.png").convert()
bg_img_3 = pygame.transform.scale(bg_img_3, (WIDTH, HEIGHT))

bg_list = [[bg_img_0, bg_img_0], [bg_img_2, bg_img_1], [bg_img_3, bg_img_3]]

background = random.choice(bg_list)
bg = background[0].get_rect(center = (WIDTH / 2, HEIGHT / 2))
bg2 = background[1].get_rect(center = (WIDTH + WIDTH / 2, HEIGHT / 2))

# PLAYER
player = pygame.image.load("src/player.png").convert_alpha()
player = pygame.transform.scale(player, (60, 60))
player = pygame.transform.rotozoom(player, -15, 1)
player_rect = player.get_rect(center = (100, 360))
player_vel = 0
gravity = 0.5

pygame.display.set_icon(player)

# SCORE
score = 0
 
# PIPES
pipe_img = pygame.image.load("src/pipe.png").convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (120, 350))
pipes = []
SPAWN_PIPE = pygame.USEREVENT

pygame.time.set_timer(SPAWN_PIPE, 1200)

def create_pipe():
	height = random.choice([380, 480, 580, 630])
	bottom_pipe = pipe_img.get_rect(midtop = (1000, height))
	top_pipe = pipe_img.get_rect(midbottom = (1000, height - 300))

	return bottom_pipe, top_pipe

def rotate_player(player):
	new_player = pygame.transform.rotozoom(player, -player_vel * 5, 1)

	return new_player

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.x > -WIDTH:
			if pipe.y > HEIGHT - pipe.height:
				screen.blit(pipe_img, pipe)
			else:
				flipped_pipe = pygame.transform.flip(pipe_img, False, True)
				screen.blit(flipped_pipe, pipe)

def move_pipes(pipes):
	global score

	count = 0

	if pipes:
		for pipe in pipes:
			if pipe.x < 0:
				count += 1

			pipe.x -= 5

		score = count // 2

def check_collision(pipes):

	if player_rect.y < -10 or player_rect.y > HEIGHT:
		return True

	for pipe in pipes:
		if pipe.colliderect(player_rect):
			return True

	return False

run = True
game_over = True
menu = True

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == SPAWN_PIPE:
			pipes.extend(create_pipe())

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and not game_over and not menu:
				player_vel = 0
				player_vel -= 12

			if event.key == pygame.K_SPACE and game_over and not menu:
				background = random.choice(bg_list)
				bg = background[0].get_rect(center = (WIDTH / 2, HEIGHT / 2))
				bg2 = background[1].get_rect(center = (WIDTH + WIDTH / 2, HEIGHT / 2))
				player_vel = 0
				score = 0
				player_rect.center = (100, 360)
				game_over = False
				pipes.clear()

			if event.key == pygame.K_SPACE and game_over and menu:
				menu = False
				game_over = False
				player_vel = 0
				score = 0
				player_rect.center = (100, 360)
				game_over = False
				pipes.clear()

	# BACKGROUND
	screen.blit(background[0], bg)
	screen.blit(background[1], bg2)

	if not game_over and not menu:

		# BACKGROUND
		if bg.x > -WIDTH:
			bg.x -= 1
		else:
			bg.x = WIDTH

		if bg2.x > -WIDTH:
			bg2.x -= 1
		else:
			bg2.x = WIDTH

		# PLAYER
		rotated_player = rotate_player(player)
		player_vel += gravity
		player_rect.centery += player_vel
		screen.blit(rotated_player, player_rect)

		# PIPES
		draw_pipes(pipes)
		move_pipes(pipes)
		game_over = check_collision(pipes)

		# SCORE
		text_surface = font.render(str(score), True, (200, 200, 200))
		screen.blit(text_surface, (WIDTH / 2 - text_surface.get_width() / 2, 50))

	elif not menu and game_over:
		title_text = m_font.render(TITLE, True, (255, 255, 255))
		screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 100))

		text_surface = font.render(f"Your Score : {score}", True, (200, 200, 200))
		screen.blit(text_surface, (WIDTH / 2 - text_surface.get_width() / 2, 200))

		replay_text = m_font.render("Press SPACEBAR To Play Again", True, (255, 255, 255))
		screen.blit(replay_text, (WIDTH / 2 - replay_text.get_width() / 2, 600))
	else:
		title_text = m_font.render(TITLE, True, (255, 255, 255))
		screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 100))

		play_text = m_font.render("Press SPACEBAR To Play", True, (255, 255, 255))
		screen.blit(play_text, (WIDTH / 2 - play_text.get_width() / 2, 600))

	pygame.display.update()
	clock.tick(FPS)

pygame.quit()
sys.exit()
