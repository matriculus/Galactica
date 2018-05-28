import pygame
from random import randrange, choice
from settings import *
from os.path import join
import glob

# initialising the pygame environment along with mixer for audio
pygame.init()
pygame.mixer.init()

# creating main screen using the window size from the settings file
main_screen = pygame.display.set_mode(WINDOW_SIZE)
# Giving a window title
pygame.display.set_caption(TITLE)
# setting clock for FPS control
clock = pygame.time.Clock()

# Game image assets
images = "img"
# Sound assets
sounds = "sounds"

# background score
background_music_score = pygame.mixer.music
background_music_score.load(join(sounds, "seal.ogg"))
background_music_score.set_volume(0.2)

# Shooting and explosion sounds
shoot_sound = pygame.mixer.Sound(join(sounds, "laser.wav"))
shoot_sound.set_volume(0.1)
galactican_explosion = pygame.mixer.Sound(join(sounds, "hit.wav"))
galactican_explosion.set_volume(0.1)
blacknite_explosion = pygame.mixer.Sound(join(sounds, "hit1.wav"))
blacknite_explosion.set_volume(0.1)

# Image preprocessing for loading
def preprocess(image_path, size):
    image = pygame.image.load(image_path).convert()
    image = pygame.transform.scale(image, size)
    return image

# background
BACKGROUND = preprocess(join(images, "scene03.png"), WINDOW_SIZE)
BACKGROUND_rect = BACKGROUND.get_rect()
# print(BACKGROUND_rect)

# player properties
galactican_image_folder = join(images, "galacticans")
galactican = preprocess(join(galactican_image_folder, "galactican.png"), (50, 50))

# slaves properties
blacknite_images = glob.glob(join(images, "blacknites", "*.png"))
blacknite = [preprocess(img, (50, 50)) for img in blacknite_images]

# lightspear properties
redspear = preprocess(join(images, "redspear.png"), (5, 15))
orangespear = preprocess(join(images, "orangespear.png"), (5, 15))
yellowspear = preprocess(join(images, "yellowspear.png"), (5, 15))

# explosion animation
anim_expl = join(images, "explosion")
animated_explosion = {}
animated_explosion["large"] = []
animated_explosion["small"] = []
for i in range(9):
    fname = "explosion0{}.png".format(i)
    im = preprocess(join(anim_expl, fname), (75, 75))
    im.set_colorkey(BLACK)
    animated_explosion["large"].append(im)
    im = pygame.transform.scale(im, (25, 25))
    im.set_colorkey(BLACK)
    animated_explosion["small"].append(im)

# player movement animation
player_animation = {}
player_animation["left"] = []
player_animation["right"] = []

for i in range(1, 10):
    fname = "redfighter000{}.png".format(i)
    im = preprocess(join(galactican_image_folder, fname), (50, 50))
    im.set_colorkey(BLACK)
    if i <= 5:
        player_animation["left"].append(im)
    if i >= 5:
        player_animation["right"].append(im)
    if i == 5:
        player_animation["straight"] = im

player_animation["left_rev"] = player_animation["left"]
player_animation["left"].reverse()
player_animation["right_rev"] = player_animation["right"][::-1]

# Rendering text
font_name = pygame.font.match_font('freesansbold')
def display_text(surface, text, size, location):
    x, y = location
    text = "Score: " + str(text)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def shield_bar(surface, location, shield):
    x, y = location
    if shield < 0:
        shield = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = (shield / GALACTIAN_SHIELDS) * BAR_LENGTH
    if fill >= 50:
        colour = GREEN
    elif fill >= 25:
        colour = YELLOW
    else:
        colour = RED
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, colour, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)