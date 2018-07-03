import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print(os.getcwd())

# Screen size
WINDOW_SIZE = WIDTH, HEIGHT = 480, 640
FPS = 30
TITLE = "GALACTICA" # Game Name

# Colour codes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
CYAN = (0, 255, 255)

# Score font size
SCORE_FONT_SIZE = 25
SCORE_LOCATION = (WIDTH/2, 10)

# Game over font
GAME_OVER_SIZE = 100
GAME_OVER_LOCATION = (WIDTH/2, HEIGHT/2)
GAME_OVER_SCORE_LOCATION = (WIDTH/2, HEIGHT/2 + 2*GAME_OVER_SIZE)

# Default shields
GALACTIAN_SHIELDS = 100
SHIELD_BAR_LOCATION = (5, 5)
