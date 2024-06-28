import pygame
import random
import sys
import time
from env import *
from Player import *
from typing import Callable, List, Tuple

def Exit():
    pygame.quit()
    sys.exit()

def Menu(screen: pygame.Surface, menu_items: List[str], actions: List[Callable], 
         events, message=None, messageColor=white):
    
    font = pygame.font.Font(None, 74)
    screen.fill(black)
    mouse_pos = pygame.mouse.get_pos()

    bg = pygame.transform.scale(background,( screen.get_width(), screen.get_height()))
    
    dark_surface = pygame.Surface(( screen.get_width(), screen.get_height()))
    dark_surface.fill(black)
    dark_surface.set_alpha(200)

    screen.blit(bg,(0,0))
    screen.blit(dark_surface,(0,0))

    label_rects = []

    if message!=None:
        color = messageColor
        label = font.render(message, True, color)
        label_x = screen.get_width() // 2 - label.get_width() // 2
        label_y = screen.get_height() // 2 - len(menu_items) * label.get_height() // 2 - label.get_height() * 2
        
        screen.blit(label, (label_x, label_y))

    
    for index, item in enumerate(menu_items):
        color = white
        label = font.render(item, True, color)

        
        
        label_x = screen.get_width() // 2 - label.get_width() // 2
        label_y = screen.get_height() // 2 - len(menu_items) * label.get_height() // 2 + index * label.get_height() * 2
        
        
        label_rect = label.get_rect(center=(screen.get_width() // 2, label_y + label.get_height() // 2))
        
        label_rects.append(label_rect)
        
        
        if label_rect.collidepoint(mouse_pos):
            color = green
            label = font.render(item, True, color)
            pygame.draw.rect(screen, blue, label_rect.inflate(10, 10), 0)
            pygame.draw.rect(screen, yellow, label_rect.inflate(10, 10), 5) 
        
        screen.blit(label, (label_x, label_y))
    
    #print("MenuEventsUpdate")
   # print("Events")
    for event in events:
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, rect in enumerate(label_rects):
                if rect.collidepoint(mouse_pos):
                    if(actions[index]!=None):
                        actions[index]()
                    else:
                        #print("NoneType Action called")
                        pass
                    return menu_items[index]


def draw_stats(screen:pygame.Surface, player):
    screen_height = screen.get_height()
    font = pygame.font.Font(None, 36)

    dark_surface = pygame.Surface(( 250, 150))
    dark_surface.fill((0, 0, 0))
    dark_surface.set_alpha(200)
    screen.blit(dark_surface,(0, screen_height-140))
    
    stats = font.render("Stats", True,white)
    screen.blit(stats, (10, screen_height - 120))
                
    barWidth = 150
    heart = pygame.transform.scale(heart_img, (40,40))
    screen.blit(heart,(8, screen_height - 92))
    fill = (player.player_health / 100) * barWidth
    pygame.draw.rect(screen, black, (48, screen_height - 92, barWidth+4, 34))
    pygame.draw.rect(screen, red, (50, screen_height - 90, fill, 30))

    bolt = pygame.transform.scale(lightningBolt_img, (40,40))
    screen.blit(bolt,(8, screen_height - 52))
    fill = (player.player_energy / 100) * barWidth
    pygame.draw.rect(screen, black, (48, screen_height - 52, barWidth+4, 34))
    pygame.draw.rect(screen, yellow, (50, screen_height - 50, fill, 30))


def get_menu_corner(screen, menu_size):
    x:int = screen.get_width() // 2 - menu_size[0] // 2
    y:int = screen.get_height() // 2 - menu_size[1] // 2
    return (x,y)

def create_dark_surface(menu_size):
    dark_surface = pygame.Surface(menu_size)
    dark_surface.fill((0, 0, 0))
    dark_surface.set_alpha(200)
    return dark_surface

def create_inventory_surface(player, menu_size, scroll_y, menu_corner):
    item_height = 100
    item_width = 100
    margin = 10
    items_per_row = menu_size[0] // 2 // (item_width + margin)

    total_items = len(player.inventory)
    total_rows = (total_items + items_per_row - 1) // items_per_row
    content_height = total_rows * (item_height + margin)

    item_surface = pygame.Surface((menu_size[0] // 2, max(content_height, menu_size[1] - 300)),
                                  pygame.SRCALPHA, 32)
    item_surface.convert_alpha()

    x_offset = margin
    y_offset = margin
    current_col = 0

    font = pygame.font.Font(None, 24)

    item_rects = []
    for item, details in player.inventory.items():
        if details['icon']!=None:
            img = pygame.transform.scale(details['icon'], (item_width, item_height))
        else:
            img =  pygame.transform.scale(noimg, (item_width, item_height))

        item_surface.blit(img, (x_offset, y_offset))
        item_rect = pygame.Rect(menu_corner[0] + x_offset+menu_size[0]//2, menu_corner[1] + y_offset + 400 + scroll_y, 
                                item_width, item_height)
        item_rects.append((item, item_rect))

        quantity_text = font.render(str(details['quantity']), True, white)
        item_surface.blit(quantity_text, (x_offset + item_width - quantity_text.get_width(), 
                                          y_offset + item_height - quantity_text.get_height()))

        current_col += 1
        if current_col >= items_per_row:
            current_col = 0
            x_offset = margin
            y_offset += item_height + margin
        else:
            x_offset += item_width + margin

    return item_surface, item_rects



def create_crafting_surface(player, menu_size, crafting_scroll_y, menu_corner):
    crafting_panel_width = menu_size[0] // 2
    crafting_surface = pygame.Surface((crafting_panel_width, menu_size[1]),pygame.SRCALPHA, 32)
    crafting_surface.convert_alpha()

    crafting_item_height = 50
    crafting_item_margin = 10
    crafting_y_offset = crafting_item_margin + crafting_scroll_y

    font = pygame.font.Font(None, 24)
    
    item_rects = []
    for recipe_name, recipe in crafting_recipes.items():
        can_craft = player.can_craft(recipe)

        text_color = green if can_craft else red
        recipe_text = font.render(recipe_name, True, text_color)

        box_color = gray if can_craft else darkgray
        box = pygame.Rect(crafting_item_margin, crafting_y_offset, 
                          crafting_panel_width - 2 * crafting_item_margin, crafting_item_height)
        pygame.draw.rect(crafting_surface, box_color, box)

        
        item_rect = pygame.Rect(menu_corner[0]+ crafting_item_margin, menu_corner[1] + crafting_y_offset, 
                                crafting_panel_width - 2 * crafting_item_margin, crafting_item_height)
        item_rects.append((recipe_name, item_rect))
        crafting_surface.blit(recipe_text,(crafting_item_margin +crafting_panel_width//2-recipe_text.get_width()//2, 
                                            crafting_y_offset+crafting_item_height//2-recipe_text.get_height()//2))

        crafting_y_offset += crafting_item_height + crafting_item_margin

    return crafting_surface, item_rects

def handle_events(events, cursor, item_rects, crafting_rects, player:Player, 
                  crafting_surface_rect, inventory_surface_rect,
                  scroll_y, crafting_scroll_y, screen=None):
    
    for event in events:
        if event.type == pygame.MOUSEWHEEL:
            if crafting_surface_rect.collidepoint(cursor):
                crafting_scroll_y += event.y * 20
            elif inventory_surface_rect.collidepoint(cursor):
                scroll_y += event.y * 20
            if crafting_scroll_y>0:crafting_scroll_y=0
            if scroll_y>0:scroll_y=0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if inventory_surface_rect.collidepoint(cursor):
                for item, item_rect in item_rects:
                    if item_rect.collidepoint(cursor):
                        if item == "banana" and player.inventory["banana"]["quantity"] > 0:
                            player.inventory["banana"]["quantity"] -= 1
                            player.player_health += 5
                            player.player_energy += 10
                        player.holding_item = item
            if crafting_surface_rect.collidepoint(cursor):
                for item, rect in crafting_rects:
                    if rect.collidepoint(cursor):
                        player.craft(item)
                       # print(item)

    return scroll_y, crafting_scroll_y

def draw_inventory(screen: pygame.Surface, player, scroll_y, crafting_scroll_y, events):
    cursor = pygame.mouse.get_pos()
    menu_size = (1000, 800)
    menu_corner = get_menu_corner(screen, menu_size)

    dark_surface = create_dark_surface(menu_size)
    screen.blit(dark_surface, menu_corner)

    inventory_surface, item_rects = create_inventory_surface(player, menu_size, scroll_y, menu_corner)
    inventory_surface_rect = screen.blit(inventory_surface, (menu_corner[0] + menu_size[0] // 2, 
                                                             menu_corner[1] + 400),
                                        area=pygame.Rect(0, -scroll_y, menu_size[0] // 2, 
                                                         menu_size[1] - 400))

    crafting_surface, crafting_rects = create_crafting_surface(player, menu_size, crafting_scroll_y,menu_corner)
    crafting_surface_rect = screen.blit(crafting_surface, (menu_corner[0], menu_corner[1]),
                                        area=pygame.Rect(0, 0, menu_size[0] // 2, 
                                                         menu_size[1]))
    #for _, rect in item_rects:
   #     pygame.draw.rect(screen,red,rect)
    scroll_y, crafting_scroll_y = handle_events(events, cursor, item_rects, crafting_rects, player, 
                                                crafting_surface_rect, inventory_surface_rect,
                                                scroll_y,crafting_scroll_y,screen)
    #print(scroll_y, crafting_scroll_y)
    return scroll_y, crafting_scroll_y
