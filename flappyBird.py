import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# TEXT
font = pygame.font.SysFont('Arial', 60)
text_color = (255, 255, 255)

gnd_x = 0
scroll_speed = 2 # 4 px
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 # ms
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
passed_pipe = False

# Images
background = pygame.image.load('images/background.png')
gnd = pygame.image.load('images/ground.png')

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

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


class Pipe(pygame.sprite.Sprite):
        def __init__(self, x, y, pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('images/pipe.png')
            self.rect = self.image.get_rect()

            # pos 1 is from top, -1 is from bottom
            if pos == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
            if pos == -1:
                self.rect.topleft = [x, y + int(pipe_gap / 2)]

        def update(self):
            self.rect.x -= scroll_speed

            # Delete pipe if pipe is off screen
            if self.rect.right < 0:
                self.kill 
            


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

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

    pipe_group.draw(screen)
    pipe_group.update()

    # Draw ground
    screen.blit(gnd, (gnd_x, 640))

    # Check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and passed_pipe == False:
                passed_pipe = True

        if passed_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                passed_pipe = False

    draw_text(str(score), font, text_color, int(screen_width / 2), 50)

    # Collision with pipes
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0:
        game_over = True

    # Game over if hit gnd
    if bird.rect.bottom >= 640:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        # New pipes
        current_time = pygame.time.get_ticks()

        if current_time - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100) # Random pipe heights

            bottom_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe, top_pipe)
            last_pipe = current_time


        # Scroll ground
        gnd_x -= scroll_speed

        #if gnd past 1st notch reset it to be safe & gnd always is there w/ scroll effect
        if abs (gnd_x) > 35:
            gnd_x = 0

        pipe_group.update()


    # Exit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        


    pygame.display.update()

pygame.quit()


