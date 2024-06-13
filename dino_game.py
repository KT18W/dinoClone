import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = test_font.render(f'Score: {current_time}', False, (46,94,199))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 350:
                screen.blit(snail_surface, obstacle_rect)

            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -42]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return True

    return False

pygame.init()
screen = pygame.display.set_mode((800,400)) #game window (width, height)
pygame.display.set_caption('The Immortal Man')
clock = pygame.time.Clock()
test_font = pygame.font.Font('dinoAss/Pixeltype.ttf', 50)

game_start = True
game_active = False
game_end = False
start_time = 0
score = 0
current_screen = 'start'


#scenery
sky_surface = pygame.image.load('dinoAss/background.jpg').convert_alpha()#convert makes game run faster
ground_surface = pygame.image.load('dinoAss/ground.png').convert_alpha()

#obstacles
snail_surface = pygame.image.load('dinoAss/snail.png').convert_alpha()
snail_x_pos = 600
snail_rect = snail_surface.get_rect(midbottom = (snail_x_pos,350))

fly_surface = pygame.image.load('dinoAss/fly1.png').convert_alpha()

obstacle_rect_list = []

#player
player_surface = pygame.image.load('dinoAss/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,350)) #takes the surface and draws rectangle around it
player_gravity = 0

#intro screen
player_stand = pygame.image.load('dinoAss/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('The Man and the Snail', False, (111, 196, 196))
game_name_rect = game_name.get_rect(center = (400, 60))

game_message = test_font.render('Press enter to run', False, (111, 196, 196))
game_message_rect = game_message.get_rect(center = (400, 330))
game_over_message = test_font.render('Press enter to start again', False, (111, 196, 196))
game_over_message_rect = game_over_message.get_rect(center = (400, 365))


game_instruct = test_font.render('Space to jump', False, (111, 196, 196))
game_instruct_rect = game_message.get_rect(center = (446, 365))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


#update and draw
while True:


    #event statements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #play
        if event.type == pygame.KEYDOWN and player_rect.bottom == 350:
            if event.key == pygame.K_SPACE:
                player_gravity = -22


        #restart
        if event.type == pygame.KEYDOWN and game_end:
            if event.key == pygame.K_RETURN:
                game_active = True
                game_end = False
                start_time = pygame.time.get_ticks()
                print ('two')

        #start
        if event.type == pygame.KEYDOWN and score == 0: #and skip_start == False:
            if event.key == pygame.K_RETURN:
                game_active = True
                game_end = False
                print('three')

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100),350)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100),250)))
            

    #actual game    
    if game_active:
        #skip_start = False
        screen.blit(sky_surface, (0,0))#block image trasfer, surfact, pos
        screen.blit(ground_surface, (0,350))
        score = display_score()

        #player stuff
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 350:
            player_rect.bottom = 350
        screen.blit(player_surface, player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        if collisions(player_rect, obstacle_rect_list):
            game_active = False
            game_end = True
            #skip_start = True
            

    if game_active == False:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your Score: {score}', False, (111, 196,196))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
            screen.blit(game_instruct, game_instruct_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(game_over_message, game_over_message_rect)



    pygame.display.update()
    clock.tick(60)
    
