import pygame

# Initialize pygame
pygame.init()


# White color
white = (255, 255, 255)


# Window size
X = 400
Y = 400


# Create display surface
display_surface = pygame.display.set_mode((X, Y))


# Window title
pygame.display.set_caption("Image Display")


# Load image
image = pygame.image.load(
    r"images.jpg"
)


# Game loop
running = True

while running:


    # Fill background with white
    display_surface.fill(white)


    # Draw image on screen
    display_surface.blit(
        image,
        (0, 0)
    )


    # Check events
    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:

            running = False



    # Update display
    pygame.display.update()



# Close pygame
pygame.quit()