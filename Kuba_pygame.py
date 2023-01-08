import sys
import time

import pygame
from KubaGame import *

pygame.init()

size = width, height = 1280, 960

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Kuba!")

click_sound = pygame.mixer.Sound('assets/click_sound.wav')
swash_sound = pygame.mixer.Sound('assets/swash_sound.wav')


# board coordinates
A1, A2, A3, A4, A5, A6, A7 = (416, 256), (480, 256), (544, 256), (608, 256), (672, 256), (736, 256), (800, 256)
B1, B2, B3, B4, B5, B6, B7 = (416, 320), (480, 320), (544, 320), (608, 320), (672, 320), (736, 320), (800, 320)
C1, C2, C3, C4, C5, C6, C7 = (416, 384), (480, 384), (544, 384), (608, 384), (672, 384), (736, 384), (800, 384)
D1, D2, D3, D4, D5, D6, D7 = (416, 448), (480, 448), (544, 448), (608, 448), (672, 448), (736, 448), (800, 448)
E1, E2, E3, E4, E5, E6, E7 = (416, 512), (480, 512), (544, 512), (608, 512), (672, 512), (736, 512), (800, 512)
F1, F2, F3, F4, F5, F6, F7 = (416, 576), (480, 576), (544, 576), (608, 576), (672, 576), (736, 576), (800, 576)
G1, G2, G3, G4, G5, G6, G7 = (416, 640), (480, 640), (544, 640), (608, 640), (672, 640), (736, 640), (800, 640)

# captured zone coordinates

# if (<0, 0 or higher)
W1, W2, W3, W4, W5, W6, W7 = (416, 192), (480, 192), (544, 192), (608, 192), (672, 192), (736, 192), (800, 192)
# if (0 or higher, <0)
X1, X2, X3, X4, X5, X6, X7 = (352, 256), (352, 320), (352, 384), (352, 448), (352, 512), (352, 576), (352, 640)
# if (0 or higher, >6)
Y1, Y2, Y3, Y4, Y5, Y6, Y7 = (864, 256), (864, 320), (864, 384), (864, 448), (864, 512), (864, 576), (864, 640)
# if (>6, 0 or higher)
Z1, Z2, Z3, Z4, Z5, Z6, Z7 = (416, 704), (480, 704), (544, 704), (608, 704), (672, 704), (736, 704), (800, 704)

captured_coords = {(-1, 0): W1, (-1, 1): W2, (-1, 2): W3, (-1, 3): W4, (-1, 4): W5, (-1, 5): W6, (-1, 6): W7,
                   (0, -1): X1, (1, -1): X2, (2, -1): X3, (3, -1): X4, (4, -1): X5, (5, -1): X6, (6, -1): X7,
                   (0, 7): Y1, (1, 7): Y2, (2, 7): Y3, (3, 7): Y4, (4, 7): Y5, (5, 7): Y6, (6, 7): Y7,
                   (7, 0): Z1, (7, 1): Z2, (7, 2): Z3, (7, 3): Z4, (7, 4): Z5, (7, 5): Z6, (7, 6): Z7}

coord_pairs = {(0, 0): A1, (0, 1): A2, (0, 2): A3, (0, 3): A4, (0, 4): A5, (0, 5): A6, (0, 6): A7,
               (1, 0): B1, (1, 1): B2, (1, 2): B3, (1, 3): B4, (1, 4): B5, (1, 5): B6, (1, 6): B7,
               (2, 0): C1, (2, 1): C2, (2, 2): C3, (2, 3): C4, (2, 4): C5, (2, 5): C6, (2, 6): C7,
               (3, 0): D1, (3, 1): D2, (3, 2): D3, (3, 3): D4, (3, 4): D5, (3, 5): D6, (3, 6): D7,
               (4, 0): E1, (4, 1): E2, (4, 2): E3, (4, 3): E4, (4, 4): E5, (4, 5): E6, (4, 6): E7,
               (5, 0): F1, (5, 1): F2, (5, 2): F3, (5, 3): F4, (5, 4): F5, (5, 5): F6, (5, 6): F7,
               (6, 0): G1, (6, 1): G2, (6, 2): G3, (6, 3): G4, (6, 4): G5, (6, 5): G6, (6, 6): G7, (-1, 0): W1, (-1, 1): W2, (-1, 2): W3, (-1, 3): W4, (-1, 4): W5, (-1, 5): W6, (-1, 6): W7,
                   (0, -1): X1, (1, -1): X2, (2, -1): X3, (3, -1): X4, (4, -1): X5, (5, -1): X6, (6, -1): X7,
                   (0, 7): Y1, (1, 7): Y2, (2, 7): Y3, (3, 7): Y4, (4, 7): Y5, (5, 7): Y6, (6, 7): Y7,
                   (7, 0): Z1, (7, 1): Z2, (7, 2): Z3, (7, 3): Z4, (7, 4): Z5, (7, 5): Z6, (7, 6): Z7}

white_coords = []
black_coords = []
red_coords = []

board = pygame.image.load("assets/board.png")
red_ball = pygame.image.load("assets/red_marble.png")
white_ball = pygame.image.load("assets/white_marble.png")
black_ball = pygame.image.load("assets/black_marble.png")
white_ball_hover = pygame.image.load("assets/white_marble_hover.png")
black_ball_hover = pygame.image.load("assets/black_marble_hover.png")

arrow_up_faded = pygame.image.load("assets/arrows/arrow_up_faded.png")
arrow_right_faded = pygame.image.load("assets/arrows/arrow_right_faded.png")
arrow_left_faded = pygame.image.load("assets/arrows/arrow_left_faded.png")
arrow_down_faded = pygame.image.load("assets/arrows/arrow_down_faded.png")

arrow_up = pygame.image.load("assets/arrows/arrow_up.png")
arrow_down = pygame.image.load("assets/arrows/arrow_down.png")
arrow_left = pygame.image.load("assets/arrows/arrow_left.png")
arrow_right = pygame.image.load("assets/arrows/arrow_right.png")

arrow_up_pressed = pygame.image.load("assets/arrows/arrow_up_pressed.png")
arrow_down_pressed = pygame.image.load("assets/arrows/arrow_down_pressed.png")
arrow_left_pressed = pygame.image.load("assets/arrows/arrow_left_pressed.png")
arrow_right_pressed = pygame.image.load("assets/arrows/arrow_right_pressed.png")

main_menu = pygame.image.load("assets/main_menu.png")
new_game_button = pygame.image.load("assets/new_game_button.png")
tutorial_button = pygame.image.load("assets/tutorial_button.png")

new_game_pressed = pygame.image.load("assets/new_game_button_pressed.png")
tutorial_pressed = pygame.image.load("assets/tutorial_button_pressed.png")

font = pygame.font.Font('assets/PixeloidSans.ttf', 60)
fontX = 0
fontY = 0

ball_width = red_ball.get_width()
ball_height = red_ball.get_height()

button_width = new_game_button.get_width()
button_height = new_game_button.get_height()

new_game_rect = pygame.Rect(344, 500, button_width, button_height)
tutorial_rect = pygame.Rect(680, 500, button_width, button_height)

FPS = 60
clock = pygame.time.Clock
run = True

arrow_width = 48
arrow_height = 48

step = 64


# create new kuba game
kuba = KubaGame(("Player_1", "B"), ("Player_2", "W"))
kuba_board = kuba.print_board()


red_rectangles = []
white_rectangles = []
black_rectangles = []
arrow_rectangles = []

def show_current_turn(turn):
    current_turn = font.render("current turn: " + str(turn), False, (0, 0, 0))

def update_coordinates():
    if white_rectangles:
        white_rectangles.clear()
    if black_rectangles:
        black_rectangles.clear()
    if red_rectangles:
        red_rectangles.clear()

    kuba_board = kuba.print_board()
    for coord in kuba_board:
        marble = kuba_board[coord]
        real_coord = coord_pairs[coord]
        if marble == "R":
            rectangle = pygame.Rect(real_coord[0], real_coord[1], ball_width, ball_height)
            red_rectangles.append(rectangle)

        elif marble == "W":
            rectangle = pygame.Rect(real_coord[0], real_coord[1], ball_width, ball_height)
            white_rectangles.append(rectangle)

        elif marble == "B":
            rectangle = pygame.Rect(real_coord[0], real_coord[1], ball_width, ball_height)
            black_rectangles.append(rectangle)




def play_game(coordinates, direction, player):
    keys = coord_pairs.keys()
    simple_coords = 0
    for key in keys:
        if coord_pairs[key] == coordinates:
            simple_coords = key
            break

    if direction == "UP":
        kuba.make_move(player, simple_coords, "F")

    if direction == "DOWN":
        kuba.make_move(player, simple_coords, "B")

    if direction == "LEFT":
        kuba.make_move(player, simple_coords, "L")

    if direction == "RIGHT":
        kuba.make_move(player, simple_coords, "R")


def draw_board():
    screen.blit(board, (0, 0))


def draw_red(coords):
    screen.blit(red_ball, coords)


def draw_white(coords):
    screen.blit(white_ball, coords)

def draw_white_hover(coords):
    screen.blit(white_ball_hover, coords)

def draw_black(coords):
    screen.blit(black_ball, coords)

def draw_black_hover(coords):
    screen.blit(black_ball_hover, coords)

def draw_faded_arrows(coords):
    x = coords[0] + 8
    y = coords[1] - 44
    screen.blit(arrow_up_faded, (x, y))

    x = coords[0] - 44
    y = coords[1] + 8
    screen.blit(arrow_left_faded, (x, y))

    x = coords[0] + 60
    y = coords[1] + 8
    screen.blit(arrow_right_faded, (x, y))

    x = coords[0] + 8
    y = coords[1] + 60
    screen.blit(arrow_down_faded, (x, y))

def draw_arrow(direction, coords):
    if direction == "UP":
        screen.blit(arrow_up, coords)
    elif direction == "LEFT":
        screen.blit(arrow_left, coords)
    elif direction == "RIGHT":
        screen.blit(arrow_right, coords)
    elif direction == "DOWN":
        screen.blit(arrow_down, coords)

def draw_main_menu():
    screen.blit(main_menu, (0, 0))
    screen.blit(new_game_pressed, (344, 500))
    screen.blit(tutorial_pressed, (680, 500))


def draw_new_game():
    screen.blit(new_game_button, (344, 500))

def draw_tutorial():
    screen.blit(tutorial_button, (680, 500))

arrows = False
shut_down = False
arrows_coord = None
active_marble = (0, 0)
game_start = True
update_coordinates()
hover = False
hover_rectangle = None
player = "Player_1"

while run:
    clock().tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if game_start:
                rect = pygame.Rect(344, 500, button_width, button_height)
                if rect.collidepoint(pos):
                    draw_new_game()
                    clock().tick(FPS)
                    game_start = False

            if arrow_rectangles:
                for tup in arrow_rectangles:
                    rect = tup[0]
                    if rect.collidepoint(pos):
                        # play a game
                        play_game(active_marble, tup[1], player)
                        update_coordinates()
                        print(kuba.get_current_turn())
                        player = kuba.get_current_turn()


            for rect in black_rectangles:
                if rect.collidepoint(pos):
                    if arrows:
                        arrows = False
                        arrow_rectangles = []
                    else:
                        active_marble = (rect.x, rect.y)
                        arrows = True
                        arrows_coord = (rect.x, rect.y)

            for rect in white_rectangles:
                if rect.collidepoint(pos):
                    if arrows:
                        arrows = False
                        arrow_rectangles = []
                    else:
                        active_marble = (rect.x, rect.y)
                        arrows = True
                        arrows_coord = (rect.x, rect.y)


    # initiate white and red balls


    if game_start:

        draw_main_menu()
        mouse_pos = pygame.mouse.get_pos()

        if new_game_rect.collidepoint(mouse_pos):
            draw_new_game()

        if tutorial_rect.collidepoint(mouse_pos):
            draw_tutorial()

    else:
        draw_board()


        for rectangle in red_rectangles:
            draw_red((rectangle.x, rectangle.y))

        for rectangle in white_rectangles:
            mouse_pos = pygame.mouse.get_pos()
            if rectangle.collidepoint(mouse_pos):
                draw_white_hover((rectangle.x, rectangle.y))

                if not hover_rectangle:
                    hover = True
                    hover_rectangle = rectangle

                else:
                    if hover_rectangle != rectangle:
                        hover = True
                        hover_rectangle = rectangle

                    else:
                        hover = False

            else:
                draw_white((rectangle.x, rectangle.y))


        for rectangle in black_rectangles:
            draw_black((rectangle.x, rectangle.y))

        for rectangle in black_rectangles:
            mouse_pos = pygame.mouse.get_pos()
            if rectangle.collidepoint(mouse_pos):
                draw_black_hover((rectangle.x, rectangle.y))

                if not hover_rectangle:
                    hover = True
                    hover_rectangle = rectangle

                else:
                    if hover_rectangle != rectangle:
                        hover = True
                        hover_rectangle = rectangle

                    else:
                        hover = False

        if arrows:
            # create rectangles from arrow locations


            draw_faded_arrows((arrows_coord[0], arrows_coord[1]))

            rectangle_1 = pygame.Rect(arrows_coord[0] + 8, arrows_coord[1] - 44, arrow_width, arrow_height)
            rectangle_2 = pygame.Rect(arrows_coord[0] - 44, arrows_coord[1] + 8, arrow_width, arrow_height)
            rectangle_3 = pygame.Rect(arrows_coord[0] + 60, arrows_coord[1] + 8, arrow_width, arrow_height)
            rectangle_4 = pygame.Rect(arrows_coord[0] + 8, arrows_coord[1] + 60, arrow_width, arrow_height)
            arrow_rectangles = [(rectangle_1, "UP"), (rectangle_2, "LEFT"), (rectangle_3, "RIGHT"), (rectangle_4, "DOWN")]


            for rect in arrow_rectangles:
                mouse_pos = pygame.mouse.get_pos()
                if rect[0].collidepoint(mouse_pos):
                    draw_arrow(rect[1], (rect[0].x, rect[0].y))
                    if pygame.mouse.get_pressed()[0]:
                        break
                    break

    pygame.display.update()

    if hover:
        hover = False
        swash_sound.play()
        time.sleep(.04)
        swash_sound.stop()