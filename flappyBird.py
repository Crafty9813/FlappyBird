import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

gnd_x = 0
gnd_speed = 4 # 4 px


# Images
background = pygame.image.load('images/background.png')
gnd = pygame.image.load('images/ground.png')


run = True
while run:

    # Make sure fps is 60
    clock.tick(fps)

    # Display background
    screen.blit(background, (0, 0))

    # Display and make gnd sliding
    screen.blit(gnd, (gnd_x, 640))
    gnd_x -= gnd_speed

    #if gnd past 1st notch reset it to be safe & gnd always is there w/ scroll effect
    if abs (gnd_x) > 35:
        gnd_x = 0


    # Exit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()


