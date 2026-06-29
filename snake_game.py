import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

# Snake settings
block = 20
snake_speed = 10

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 70)


def show_score(score):
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, [10,10])


def game_over(score):

    text = big_font.render(
        "GAME OVER",
        True,
        RED
    )

    screen.blit(
        text,
        [WIDTH/2-150, HEIGHT/2-80]
    )

    score_text = font.render(
        "Score: "+str(score),
        True,
        WHITE
    )

    screen.blit(
        score_text,
        [WIDTH/2-50, HEIGHT/2]
    )

    pygame.display.update()

    pygame.time.wait(3000)



def game_loop():

    global snake_speed


    x = WIDTH//2
    y = HEIGHT//2


    dx = 0
    dy = 0


    snake = []

    length = 1


    food_x = random.randrange(
        0, WIDTH-block, block
    )

    food_y = random.randrange(
        0, HEIGHT-block, block
    )


    yellow_food = False


    # Obstacles
    obstacles = [
        [200,200],
        [220,200],
        [240,200],
        [500,400],
        [520,400],
        [540,400]
    ]


    running = True


    while running:


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running=False


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    dx=-block
                    dy=0

                elif event.key == pygame.K_RIGHT:
                    dx=block
                    dy=0

                elif event.key == pygame.K_UP:
                    dy=-block
                    dx=0

                elif event.key == pygame.K_DOWN:
                    dy=block
                    dx=0



        x += dx
        y += dy


        # Wall collision

        if (
            x < 0 or
            x >= WIDTH or
            y < 0 or
            y >= HEIGHT
        ):
            game_over(length-1)
            return



        screen.fill(BLACK)


        # Create snake

        head = [x,y]

        snake.append(head)


        if len(snake)>length:
            del snake[0]



        # Snake hits itself

        if head in snake[:-1]:

            game_over(length-1)
            return



        # Draw snake

        for part in snake:

            pygame.draw.rect(
                screen,
                GREEN,
                [
                    part[0],
                    part[1],
                    block,
                    block
                ]
            )



        # Draw obstacles

        for obs in obstacles:

            pygame.draw.rect(
                screen,
                BLUE,
                [
                    obs[0],
                    obs[1],
                    block,
                    block
                ]
            )


        # Normal fruit

        if not yellow_food:

            pygame.draw.rect(
                screen,
                RED,
                [
                    food_x,
                    food_y,
                    block,
                    block
                ]
            )


        # Yellow special fruit

        else:

            pygame.draw.rect(
                screen,
                YELLOW,
                [
                    food_x,
                    food_y,
                    block,
                    block
                ]
            )



        # Obstacle collision

        if [x,y] in obstacles:

            game_over(length-1)
            return



        # Eat fruit

        if x == food_x and y == food_y:


            if yellow_food:

                length += 2

            else:

                length += 1



            food_x = random.randrange(
                0, WIDTH-block, block
            )

            food_y = random.randrange(
                0, HEIGHT-block, block
            )



        score = length-1



        # Speed increase

        if score > 100:

            snake_speed = 20

        else:

            snake_speed = 10



        # Add yellow fruit after score 150

        if score > 150:

            yellow_food=True



        show_score(score)


        pygame.display.update()


        clock.tick(snake_speed)



    pygame.quit()



game_loop()