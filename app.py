import pygame
import random
import sys
import time
from Game import Game
from Enemy import Enemy
from Player import Player
from env import *
from Menu import *

screen = None
screen_width = None
screen_height = None
paused = False


def init():
    global screen, screen_width, screen_height
    pygame.init()
    pygame.font.init()
    pygame.mixer.init() 
    info = pygame.display.Info()


    screen_width = info.current_w
    screen_height = info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("P.Craftul Lui Romas")

    game = Game(screen_width, screen_height, 64)
    player = Player(game.cols // 2 * game.tile_size + game.tile_size // 2,
                    game.rows // 2 * game.tile_size + game.tile_size // 2, 15, 40)
    min_enemies = 5
    max_enemies = 15
    enemies = [Enemy((random.randint(1, game.cols - 2) * game.tile_size + game.tile_size//2), 
                     (random.randint(1, game.rows - 2)) * game.tile_size + game.tile_size//2, 5,40) 
                     for _ in range(random.randint(min_enemies,max_enemies))]

    for enemy in enemies:
        x = enemy.getPos()[0]//game.tile_size
        y = enemy.getPos()[1]//game.tile_size
        game.map[y][x].tile_type = land

    return game,player,enemies


def switch_pause():
    global paused
    paused = not paused

def runtime(game:Game, player:Player, enemies:List[Enemy]):
    global screen, paused

    clock = pygame.time.Clock()
    running = True
    paused = False

    start_time = time.time()
    hit_anim_time = 0
    hit_anim_duration = 0.15
    hit_box = pygame.Rect(0, 0, 0, 0)

    '''Main Menu'''
    bg_music = pygame.mixer.music
    bg_music.load('./SoundTrack/561394__migfus20__fantasy-background-music-loop.mp3')
    bg_music.play(-1)

    while running:
        buttonPressed = Menu(screen,["New Game", "Exit"],[None, Exit],pygame.event.get())
        #print(buttonPressed)
        if buttonPressed == "New Game": running=False
        pygame.display.flip()

    '''Game Init'''
    running=True
    showInventory = False
    menu_size = (0,0)
    content_height = 0
    dead=False
    win=False
    scroll_y:int= 0
    crafting_scroll_y:int = 0

    immortality = False
    start_time_immortality = 0

    #CODURI DE SAMP
    hesoyam= [pygame.K_h, pygame.K_e, pygame.K_s, pygame.K_o, pygame.K_y, pygame.K_a, pygame.K_m]
    hesoyam_buffer = []

    bg_music.stop()
    '''Game Handle'''
    while running:
        elapsed_time = time.time() - start_time
        frame_events = pygame.event.get()


        #EVENT HANDLER
        for event in frame_events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                ##########  HESOYAM  ##########
                if event.key in hesoyam:
                    hesoyam_buffer.append(event.key)
                    
                    if len(hesoyam_buffer) > len(hesoyam):
                        hesoyam_buffer.pop(0)
                    if hesoyam_buffer == hesoyam:
                        print("HESOYAM, true SAMP player. ")
                        immortality = True
                        start_time_immortality = pygame.time.get_ticks()
                        hesoyam_buffer.clear()
                else:
                    hesoyam_buffer.clear()

                ########  END HESOYAM  ########

                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    if showInventory:
                        showInventory = not showInventory
                        if showInventory:player.lock()
                        else:player.unlock()
                    else:
                        switch_pause()
                if event.key == pygame.K_i:
                    showInventory = not showInventory
                    if showInventory:player.lock()
                    else:player.unlock()
                if event.key == pygame.K_1:
                    player.holding_item = "hand"
            elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
                if event.button == 1: 
                    hit_box = player.hit(screen, game, enemies)
                    hit_anim_time = elapsed_time
         #   elif event.type == pygame.MOUSEWHEEL and not showInventory:
           #     scroll_y += event.y * 10
          #      scroll_y = max(min(scroll_y, 0), menu_size[1] - content_height) 
         #   else:
         #       scroll_y = 0

        if not paused:
            if(player.player_health<=0):
                dead=True
                paused =True
            
            player.update(game)


            if immortality and (pygame.time.get_ticks() - start_time_immortality < 5000):
                player.player_health = 100
            else:
                immortality=False

            screen.fill(blue)
            game.draw_map(screen)
            player.draw(screen)
            dead_enemies = []

            for enemy in enemies:
                if enemy.gorilla==False:
                    enemy.follow_player(player, screen, game)
                enemy_health = enemy.Update(screen, player, game)
                enemy.draw(screen)
                    
                if enemy_health <= 0:  
                    dead_enemies.append(enemy)

            for enemy in dead_enemies:
                if enemy.gorilla == True:
                    win = True
                    paused = True
                enemies.remove(enemy)
                
                sound = pygame.mixer.Sound('./SoundTrack/458396__befig__monkey-cry.ogg')
                sound.set_volume(50)
                sound.play()
                player.collect("banana", random.randint(1,5), 
                                icon = banana_img)
                #print(player.inventory)
            if len(enemies) == 0:
                enemies.append(Enemy(game.cols//2 *game.tile_size,
                                     game.rows//2 *game.tile_size,
                                     0,200, gorilla=True,health=2000
                                     ))
                pygame.mixer.Sound('./SoundTrack/712766__scpsea__alien-gorilla-roar.wav').play()
            if elapsed_time - hit_anim_time < hit_anim_duration:
                player.drawHit(screen, hit_box)
                #pygame.draw.rect(screen,red,hit_box)

            draw_stats(screen,player)
            
            if(showInventory):
                (scroll_y,crafting_scroll_y) = draw_inventory(screen,player, scroll_y, 
                                                        crafting_scroll_y, frame_events)
               # print(player.inventory)
        else:
            if not dead and not win:
                #print("Paused")
                buttonPressed = Menu(screen, ["Continue", "Main Menu", "Exit"], 
                                     [switch_pause, None, Exit], frame_events)
                #print(buttonPressed)
                if buttonPressed == "Main Menu": 
                    player=None
                    game=None
                    enemies=None
                    del player
                    return "Restart"
            elif dead:
                buttonPressed = Menu(screen, ["Main Menu", "Exit"], [None, Exit], frame_events, 
                                     "You Died!!", crimson)
                
                if buttonPressed == "Main Menu": 
                    player=None
                    game=None
                    enemies=None
                    del player
                    return "Restart"
            elif win:
                buttonPressed = Menu(screen, ["Main Menu", "Exit"], [None, Exit], frame_events, 
                                     "Congratulations!! You have beaten the bad Gorilla!", green)
                
                if buttonPressed == "Main Menu": 
                    player=None
                    game=None
                    enemies=None
                    del player
                    return "Restart"

        pygame.display.flip()
        clock.tick(10)
    print("Ended Instance")

def restart():
   # global game, player, enemies
   # if game!=None:del game
   # if player!=None:del player
   # if enemies!=None:del enemies[:]
    global paused 
    paused = False
    print("Restart")
    main()

def main():
    game, player, enemies = init()
    if runtime(game, player, enemies) == "Restart":
        restart()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
