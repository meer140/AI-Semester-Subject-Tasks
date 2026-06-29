import pygame
from pygame.locals import *


# Define square object
class Square(pygame.sprite.Sprite):

    def __init__(self):
        super(Square, self).__init__()

        # Create square surface
        self.surf = pygame.Surface((25, 25))

        # Fill square color (cyan)
        self.surf.fill((0, 200, 255))

        # Get rectangle of square
        self.rect = self.surf.get_rect()



# Initialize pygame
pygame.init()


# Create window
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Four Squares Game")


# Create square objects
square1 = Square()
square2 = Square()
square3 = Square()
square4 = Square()


# Game running variable
gameOn = True


# Main game loop
while gameOn:


    # Check events
    for event in pygame.event.get():


        # Check keyboard event
        if event.type == KEYDOWN:


            # Exit using Backspace
            if event.key == K_BACKSPACE:
                gameOn = False



        # Close window
        elif event.type == QUIT:
            gameOn = False



    # Clear screen
    screen.fill((0, 0, 0))


    # Draw squares on screen
    screen.blit(square1.surf, (40, 40))

    screen.blit(square2.surf, (40, 530))

    screen.blit(square3.surf, (730, 40))

    screen.blit(square4.surf, (730, 530))


    # Update display
    pygame.display.flip()



# Close pygame
pygame.quit()