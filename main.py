import pygame
#notwendig um Spaceship zu laden aus Assetsordner
import os
import random
pygame.font.init()
#sound library
pygame.mixer.init()


WIDTH,HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SPACE COW vs DOLPHIN!")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED =(255,0,0)
YELLOW =(255,255,0)

#Grenze für die Raumschiffe
BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)

BULLET_FIRE_SOUND_COW = pygame.mixer.Sound("Assets/muh.mp3")
BULLET_FIRE_SOUND_DOLPHIN = pygame.mixer.Sound("Assets/dolphin.mp3")
BULLET_HIT_SOUND = pygame.mixer.Sound("Assets/ouch.mp3")

BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("ヒラキノ角コシックw8",40)
WINNER_FONT = pygame.font.SysFont("ヒラキノ角コシックw8",100)
#print(pygame.font.get_fonts())

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60,50

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACE_COW_IMAGE = pygame.image.load(
    os.path.join("Assets", "cow.png"))
SPACE_COW = pygame.transform.rotate(pygame.transform.scale(
    SPACE_COW_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),0)

SPACE_DOLPHIN_IMAGE = pygame.image.load(
    os.path.join("Assets", "dolphin.png"))
SPACE_DOLPHIN = pygame.transform.rotate(pygame.transform.scale(
    SPACE_DOLPHIN_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),0)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH,HEIGHT))

def draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    #WIN.fill(WHITE)
    #Teilung des Fensters
    pygame.draw.rect(WIN,BLACK,BORDER)
    #use blit to draw surfaces/images

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() -10, 10))
    WIN.blit(red_health_text, (10,10))

    WIN.blit(SPACE_COW, (yellow.x, yellow.y))
    WIN.blit(SPACE_DOLPHIN, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)


   # q_text = HEALTH_FONT.render("Press q to quit",1,WHITE)
   # WIN.blit(q_text, (10,200))

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_j] and yellow.x - VEL > BORDER.x + BORDER.width:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_l] and yellow.x + VEL + yellow.width < WIDTH:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_i] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_k] and yellow.y + VEL +yellow.height < HEIGHT:  # DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow,red):
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    #Position des Textest direkt in der Mitte
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) #5 Sek



def main():
    red =pygame.Rect(100,300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT )
    yellow =pygame.Rect(700,300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT )

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
   # print("Press 'p' to pause 'r' to resume")
   # instruction = print("Player DOLPHIN - w 'up' - a 'left' - d 'right' - s 'down' - c 'shoot'")

    run = True
    print("Press q to quit")
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            #Feuern!!!
            if event.type == pygame.KEYDOWN:
                #QUIT with q
                if event.key == pygame.K_q:
                    run = False
                    pygame.quit()
                    exit()
                #LEFTCONTROL
                if event.key == pygame.K_n and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x, yellow.y + yellow.height/2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND_COW.play()

                #RIGHTCONTROL
                if event.key == pygame.K_c and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x+red.width, red.y+7, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND_DOLPHIN.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text =""
        if red_health <= 0:
            winner_text = "COW WINS!"

        if yellow_health <= 0:
            winner_text = "DOLPHIN WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        #print(red_bullets, yellow_bullets)
#Bewegung der Raumschiffe
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)
#Aktualisierung Fenster
        draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health)

   # pygame.quit()
    main()

if __name__ == "__main__":
    main()