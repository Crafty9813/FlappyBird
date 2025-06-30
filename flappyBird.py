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
flying = False
game_over = False

# Images
background = pygame.image.load('images/background.png')
gnd = pygame.image.load('images/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # Update & draw functions built in to pygame
        self.images = []
        self.index = 0 # Start off with first image
        self.counter = 0 # Speed of animation
 
        for i in range (1, 4):
            bird_image = pygame.image.load(f'images/bird{i}.png')
            self.images.append(bird_image)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # create rect for boundary of img
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    # Override the update function in pygame sprite
    def update(self):
        # ----Gravity----
        if flying == True:
            self.vel += 0.5
            if self.vel > 5:
                self.vel = 5
            if self.rect.bottom < 640:
                self.rect.y += int(self.vel)

        # ----flap----
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.vel = -10
            self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        self.counter += 1
        flap_cooldown = 5

        # 5 frames (cooldown value) of the same img, then switch
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0

        self.image = self.images[self.index]

        # Rotate bird
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)


bird_group = pygame.sprite.Group()

bird = Bird(100, 375)

bird_group.add(bird)


run = True
while run:

    # Make sure fps is 60
    clock.tick(fps)

    # Display background
    screen.blit(background, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    # Draw ground
    screen.blit(gnd, (gnd_x, 640))

    # Game over if hit gnd
    if bird.rect.bottom > 640:
        game_over = True
        flying = False

    if game_over == False:
        gnd_x -= gnd_speed
        
        #if gnd past 1st notch reset it to be safe & gnd always is there w/ scroll effect
        if abs (gnd_x) > 35:
            gnd_x = 0


    # Exit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        


    pygame.display.update()

pygame.quit()


