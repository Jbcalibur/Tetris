# Import modules
import pygame
import random
import time

# Initialize Pygame
pygame.init()

# ---------------- Colors -------------------------------------------------------------------------------------------------------------------------
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# ---------------------- Window setup --------------------------------------------------------------------------------------------------------
window_width = 800
window_height = 600
window = pygame.display.set_mode([window_width, window_height])

# Hidden mouse
pygame.mouse.set_visible(False)

# ---------------- Class ---------------------------------------------------------------------------------------------------------------------------


class Block(pygame.sprite.Sprite):
    """
    This class represents the ball. It derives from the
    "Sprite" class in Pygame
    """

    def __init__(self, color, width, height):

        # Always call the parent class constructor at firts
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block
        self.image = pygame.Surface([width, height])

        # fill it with a color
        self.image.fill(color)
        """
        An image can be load for the block :
        self.image = pygame.image.load("player.png").convert()
        Or can be a draw :
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        Then set a transparent color :
        self.image.set_colorkey(white)
        """
        # The attribute rect is an instance of Rect class. It represents
        # the dimension of the sprite.
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1
        if self.rect.y > window_height:
            self.reset()

    def reset(self):
        self.rect.x = random.randrange(0, window_width)
        self.rect.y = random.randrange(-100, -20)


class Player(pygame.sprite.Sprite):
    """ Represente the player class"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Sprite dimensions and color
        self.image = pygame.Surface([20, 20])
        self.image.fill(red)
        self.rect = self.image.get_rect()

        # Speed of the player
        self.x_speed = 0
        self.y_speed = 0

        # Current position of the player
        self.rect.x = 400
        self.rect.y = 550

    def update(self):
        # Move player according to speed vector
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


class Bullet(pygame.sprite.Sprite):
    """ Represent the bullet class"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([4, 10])
        self.image.fill(black)

        self.rect = self.image.get_rect()

    def update(self):
        """ move the bullet"""
        self.rect.y -= 5

# ---------------------------------- Sprites lists ---------------------------------------------------------------------------------------------------


# List of all sprites but the player. Managed by Group class
block_list = pygame.sprite.Group()

# List of all sprites, player included.
all_sprites_list = pygame.sprite.Group()

# List of all bullet
bullet_list = pygame.sprite.Group()

# ---------------------------------- Creation of sprites -----------------------------------------------------------------------------------------

# Creation of 50 obstacle blocks with random x, y
for i in range(50):

    block = Block(black, 20, 15)

    block.rect.x = random.randrange(window_width)
    block.rect.y = random.randrange(window_height)

    block_list.add(block)
    all_sprites_list.add(block)

# Create a red block player
player = Player()
all_sprites_list.add(player)

# ----------------------------------- Other --------------------------------------------------------------------------------------------------------

# Player's score
score = 0
font = pygame.font.SysFont('Calibri', 25, True, False)

# Window upate
clock = pygame.time.Clock()

# fire managment
autofire = True
last_shot = 0
shot_delay = 0.2  # 200ms

# Loop until the user clicks the close button
done = False

# --------- Main Program Loop ---------------------------------------------------------------------------------------------------------------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # User let up on a key
        # If there is a speed, turn it to 0
        # Without that, mouvments are blocked if
        # we switch fastly between opposite directions.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if player.x_speed == -3:
                    player.x_speed = 0
            elif event.key == pygame.K_RIGHT:
                if player.x_speed == 3:
                    player.x_speed = 0
            elif event.key == pygame.K_DOWN:
                if player.y_speed == 3:
                    player.y_speed = 0
            elif event.key == pygame.K_UP:
                if player.y_speed == -3:
                    player.y_speed = 0
            elif event.key == pygame.K_SPACE:
                autofire = False

        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_speed = -3
            if event.key == pygame.K_RIGHT:
                player.x_speed = 3
            if event.key == pygame.K_DOWN:
                player.y_speed = 3
            if event.key == pygame.K_UP:
                player.y_speed = -3
            if event.key == pygame.K_SPACE:  # HERE IS THE PROBLEM
                while autofire:  # the program crashes with that loop
                    if time.time() - last_shot > shot_delay:  # Nothing happen without while loop
                        # Create a bullet when attack button (space) pressed
                        bullet = Bullet()
                        # set x,y bullet egal to player position
                        bullet.rect.x = player.rect.x + 8  # +8 to center the bullet
                        bullet.rect.y = player.rect.y
                        # add bullet to lists used for collisions
                        bullet_list.add(bullet)
                        # add bullet to all sprites list for draw it
                        all_sprites_list.add(bullet)
                        last_shot = time.time()

    # Clear the screen
    window.fill(white)

    # ------------------------ Game logic-----------------------------------------------------------------------------------------------------

    # Update each sprite
    all_sprites_list.update()

    # Check collisions betwwen player and blocks.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
    for player_hit in blocks_hit_list:
        score -= 5

    # Check collisions between bullet and blocks.
    # True to remove block from the list
    for bullet in bullet_list:

        blocks_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        for block in blocks_hit_list:
            # after a collision, remove the bullet
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

            score += 1

        if bullet.rect.y < 0:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    # ------------------ Draw section --------------------------------------------------------------------------------------------------------
    all_sprites_list.draw(window)

    # Print score on the top right of the screen
    score_text = font.render("Score : " + str(score), True, red)
    window.blit(score_text, [700, 10])

    # Limit of frames per second
    clock.tick(60)

    # Update draws
    pygame.display.flip()

pygame.quit()
