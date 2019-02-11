"""
 Author: Ashleigh Forbes

 Version: 2.1

 Description: This is the foundation code for the final game, where all sprites are blocks. It includes a bullet feature
  with the enemy blocks scrolling towards the player on the screen. I used the examples from class, and will build on
  this to incorporate the specifics of my game.

How to play:
  Use the LEFT and RIGHT keys to move the player block from side to side.
  Use the UP key to shoot bullets.
"""

import pygame
import random

# Define some colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
BLUE = (0,   0, 255)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode([screen_width, screen_height])

# --- Classes


class SpaceObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def reset_pos(self):
        # when the block falls off the screen
        self.rect.y = random.randrange(-30, -20)
        self.rect.x = random.randrange(screen_width)

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += 1

        if self.rect.y > screen_height + self.rect.height:
            self.reset_pos()


class Asteroid(SpaceObject):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 80, 80)
        self.image = pygame.image.load('aster4.png').convert_alpha()

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        self.rect.y = random.randrange(-30, -20)
        self.rect.x = random.randrange(screen_width - self.image.get_width())

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += 1

        if self.rect.y > screen_height + self.rect.height:
            self.reset_pos()


class Junk(SpaceObject):
    def __init__(self):
        super().__init__()

        self.rect = pygame.Rect(0, 0, 80, 80)
        self.image = pygame.image.load('junk3.png').convert_alpha()

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        self.rect.y = random.randrange(-30, -20)
        self.rect.x = random.randrange(0, screen_width - self.image.get_width())

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += 1

        if self.rect.y > screen_height + self.rect.height:
            self.reset_pos()


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.rect = pygame.Rect(0, 0, 80, 100)
        self.image = pygame.image.load('ship2Move.png').convert_alpha()

        self.change_x = 0
        self.change_y = 0

    def update(self):
        """ Update the player's position. """
        # moving left to right
        self.rect.x += self.change_x

    def go_left(self):
        # this def is called when player hits left arrow
        self.change_x = -3

    def go_right(self):
        # this def is called when player hits left arrow
        self.change_x = 3

    def stop(self):
        # when player lifts their finger
        self.change_x = 0


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # bullet
        self.image = pygame.Surface([2, 8])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.hit_sound = pygame.mixer.Sound("laser5.ogg")

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3


class StopBlock(pygame.sprite.Sprite):
    def __init__(self):
        # calling super class
        super().__init__()

        # create the rectangle
        self.image = pygame.Surface([screen_width, 1])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        # set position of the line
        self.rect.x = 0
        self.rect.y = 5


class Scoring(object):
    score_board = None
    score_print = None
    health_print = None
    font = None

    def __init__(self, scr):
        self.font = pygame.font.SysFont('Calibri', 20, True, False)

        # name the blue rectangle score board
        self.score_board = pygame.draw.rect(screen, BLACK, [screen_width - 100, 0, 100, 50])

        # render the score using the font previously defined in white
        self.score_print = self.font.render("Score: " + str(score), True, WHITE)

        # render the health using the font prev. defined
        self.health_print = self.font.render("Health: " + str(health), True, WHITE)

        # print the score in the same spot as the score board
        scr.blit(self.score_print, [self.score_board.x, self.score_board.y + 20])
        scr.blit(self.health_print, [self.score_board.x, self.score_board.y])

    scr = pygame.display.set_mode([screen_width, screen_height])


# --- Create the window

# Initialize Pygame
pygame.init()

# --- Sprite lists

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
asteroid_list = pygame.sprite.Group()
junk_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the sprites

for i in range(10):
    # This represents a block
    asteroid = Asteroid()

    # Set a random location for the block
    asteroid.rect.x = random.randrange(screen_width)
    asteroid.rect.y = random.randrange(350)

    # Add the block to the list of objects
    asteroid_list.add(asteroid)
    all_sprites_list.add(asteroid)

for i in range(10):
    # This represents a block
    junk = Junk()

    # Set a random location for the block
    junk.rect.x = random.randrange(screen_width)
    junk.rect.y = random.randrange(350)

    # Add the block to the list of objects
    junk_list.add(junk)
    all_sprites_list.add(junk)

# Create a red player block
player = Player()
all_sprites_list.add(player)
player.rect.y = 630

# create the line and add it to all sprites
backstop = StopBlock()
all_sprites_list.add(backstop)

# load the background image
bg = pygame.image.load('starynight.png').convert_alpha()

ss = pygame.image.load('startem.png').convert_alpha()

os = pygame.image.load('endend.png').convert_alpha()

ws = pygame.image.load('winwin.png').convert_alpha()

pygame.mixer.music.load('bensound-scifi.ogg')

pygame.mixer.get_init()
pygame.mixer.music.play(-1, 0)

# Loop until the user clicks the close button.
done = False

start = True

pause = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0
health = 5

# -------- Main Program Loop -----------
while not done:
    # while player is in the start menu
    while start is True:
        screen.blit(ss, [0, 0])
        pygame.time.delay(800)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True

            # DOWN --> exit out of menu and into game
            # SPACE --> exit out of game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    start = False
                if event.key == pygame.K_SPACE:
                    done = True

    # --- Event Processing of game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Moving left and right
        if event.type == pygame.KEYDOWN:

            # QUIT -- Click space to quit
            if event.key == pygame.K_SPACE:
                done = True

            if event.key == pygame.K_LEFT:
                player.go_left()
                player.image = pygame.image.load('ship2.png').convert_alpha()
            if event.key == pygame.K_RIGHT:
                player.go_right()
                player.image = pygame.image.load('ship2.png').convert_alpha()

            if event.key == pygame.K_UP:
                # Fire a bullet if the user clicks the mouse button
                bullet = Bullet()
                bullet.hit_sound.play()
                # Set the bullet so it is where the player is
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

        # when the player-block gets to the edges of the screen stop block
        if player.rect.x < 0 or player.rect.x > 1280:
            player.stop()
            player.rect.x = 1

        # when the user lifts the keys stop the movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
                player.image = pygame.image.load('ship2Move.png').convert_alpha()
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()
                player.image = pygame.image.load('ship2Move.png').convert_alpha()

    while pause is True:
        for event in pygame.event.get():

            # RESTART -- Click anywhere to restart
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(10):
                    # This represents a block
                    asteroid = Asteroid()

                    # Set a random location for the block
                    asteroid.rect.x = random.randrange(screen_width)
                    asteroid.rect.y = random.randrange(350)

                    # Add the block to the list of objects
                    asteroid_list.add(asteroid)
                    all_sprites_list.add(asteroid)

                for i in range(5):
                    # This represents a block
                    junk = Junk()

                    # Set a random location for the block
                    junk.rect.x = random.randrange(screen_width)
                    junk.rect.y = random.randrange(350)

                    # Add the block to the list of objects
                    junk_list.add(junk)
                    all_sprites_list.add(junk)

                score = 0
                print(score)

                health = 5
                print(health)

                pause = False

                # Clear the screen
                screen.blit(bg, [0, 0])

                # Draw all the spites
                all_sprites_list.draw(screen)
                Scoring(screen)

                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

    # --- Game logic

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a block
        asteroid_hit_list = pygame.sprite.spritecollide(bullet, asteroid_list, True)
        junk_hit_list = pygame.sprite.spritecollide(bullet, junk_list, True)

        # For each block hit, remove the bullet and add to the score
        for asteroid in asteroid_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        for junk in junk_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < 100:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

        pygame.sprite.spritecollide(backstop, bullet_list, True)

    # see if player hits anything
    aster_player_hit = pygame.sprite.spritecollide(player, asteroid_list, True)
    junk_player_hit = pygame.sprite.spritecollide(player, junk_list, True)

    # scoring
    for asteroid in aster_player_hit:
        asteroid_list.remove(asteroid)
        all_sprites_list.remove(asteroid)
        health -= 1
        print(health)

    for junk in junk_player_hit:
        junk_list.remove(junk)
        all_sprites_list.remove(junk)
        health -= 1
        print(health)

    # Call the update() method on all the sprites
    all_sprites_list.update()

    if score == 15:
        screen.blit(ws, [0, 0])
        pygame.display.flip()
        pygame.time.delay(5000)
        pause = True
        score = 0

    if health == -1:
        screen.blit(os, [0, 0])
        pygame.display.update()
        pygame.time.delay(5000)
        pause = True

    # Draw everything!

    # Clear the screen
    screen.blit(bg, [0, 0])

    # Draw all the spites
    all_sprites_list.draw(screen)
    Scoring(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)

pygame.quit()
