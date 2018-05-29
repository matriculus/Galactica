# Importing libraries for the game mechanics
import pygame
from game_assets import * # importing all game assets

player = Galactican("Aleena")
AllSprites.add(player)

for i in range(5):
    NewSlave()

# Game loop
score = 0
background_music_score.play(loops = -1)
running = True
while running:
    # looping at right speed
    clock.tick(FPS)
    # Process inputs (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    AllSprites.update()

    # checking for collision between Galactican, warheads and Slace using their sprites
    hits = pygame.sprite.groupcollide(LightSpears, BlackNites, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        explosion_animation(hit, "large")
        blacknite_explosion.play()
        score += 1
        NewSlave()

    hits = pygame.sprite.spritecollide(player, BlackNites, True, pygame.sprite.collide_circle)
    for hit in hits:
        explosion_animation(hit, "large")
        blacknite_explosion.play()
        running = player.space_crash()
        if player.shield <= 0:
            explosion_animation(player, "large")

    hits = pygame.sprite.groupcollide(LightSpears, BlackSpears, True, True)
    for hit in hits:
        explosion_animation(hit, "small")
        blacknite_explosion.play()
    
    hits = pygame.sprite.spritecollide(player, BlackSpears, True, pygame.sprite.collide_circle)
    for hit in hits:
        explosion_animation(hit, "large")
        blacknite_explosion.play()
        running = player.spear_crash()
        NewSlave()
        if player.shield <= 0:
            explosion_animation(player, "large")

    # Fill screen
    main_screen.fill(BLACK)
    main_screen.blit(BACKGROUND, BACKGROUND_rect)
    # Draw / render
    AllSprites.draw(main_screen)
    display_text(main_screen, score, SCORE_FONT_SIZE, SCORE_LOCATION)
    shield_bar(main_screen, SHIELD_BAR_LOCATION, player.shield)

    pygame.display.update()

pygame.quit()
