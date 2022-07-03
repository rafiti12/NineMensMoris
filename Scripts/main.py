import pygame
from constants import *
from Tile import Tile


def initiate():
    pygame.init()
    global screen, clock, board, smallfont, phase, black_tiles, red_tiles, BOARD_X, BOARD_Y, TILES_POSITION
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    board = pygame.image.load('../board.png')
    smallfont = pygame.font.SysFont('Corbel', 60)
    phase = 1
    black_tiles = 9
    red_tiles = 9
    if SCREEN_WIDTH >= SCREEN_HEIGHT:
        board = pygame.transform.scale(board, (SCREEN_HEIGHT - MARGIN, SCREEN_HEIGHT - MARGIN))
        BOARD_X = 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN)
        BOARD_Y = MARGIN * 0.5
        TILES_POSITION = [(0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + OFFSET, SCREEN_HEIGHT - MARGIN + OFFSET),
                          (0.5 * SCREEN_WIDTH, SCREEN_HEIGHT - MARGIN + OFFSET),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - OFFSET + SCREEN_HEIGHT - MARGIN, SCREEN_HEIGHT - MARGIN + OFFSET),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1/6 * SCREEN_HEIGHT, SCREEN_HEIGHT - MARGIN + OFFSET - 1/6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1 / 2 * (SCREEN_HEIGHT - MARGIN), SCREEN_HEIGHT - MARGIN + OFFSET - 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 1/6 * SCREEN_HEIGHT, SCREEN_HEIGHT - MARGIN + OFFSET - 1/6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 2/6 * (SCREEN_HEIGHT - MARGIN/2), SCREEN_HEIGHT - MARGIN + OFFSET - 2/6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * SCREEN_WIDTH, SCREEN_HEIGHT - MARGIN + OFFSET - 2/6 * (SCREEN_HEIGHT - MARGIN)),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 2/6 * (SCREEN_HEIGHT - MARGIN/2), SCREEN_HEIGHT - MARGIN + OFFSET - 2 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + OFFSET, SCREEN_HEIGHT / 2),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1/6 * SCREEN_HEIGHT, SCREEN_HEIGHT / 2),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 2/6 * (SCREEN_HEIGHT - MARGIN/2), SCREEN_HEIGHT / 2),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 2 / 6 * (SCREEN_HEIGHT - MARGIN / 2), SCREEN_HEIGHT / 2),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 1/6 * SCREEN_HEIGHT, SCREEN_HEIGHT / 2),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - OFFSET + SCREEN_HEIGHT - MARGIN, SCREEN_HEIGHT / 2),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 2 / 6 * (SCREEN_HEIGHT - MARGIN / 2), SCREEN_HEIGHT - MARGIN/2 + OFFSET - 4 / 6 * (SCREEN_HEIGHT - MARGIN/2)),
                          (0.5 * SCREEN_WIDTH, SCREEN_HEIGHT - MARGIN/2 + OFFSET - 4 / 6 * (SCREEN_HEIGHT - MARGIN/2)),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 2 / 6 * (SCREEN_HEIGHT - MARGIN / 2), SCREEN_HEIGHT - MARGIN/2 + OFFSET - 4 / 6 * (SCREEN_HEIGHT - MARGIN/2)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1 / 6 * SCREEN_HEIGHT, MARGIN/2 + OFFSET + 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1 / 2 * (SCREEN_HEIGHT - MARGIN), MARGIN/2 + OFFSET + 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 1 / 6 * SCREEN_HEIGHT, MARGIN/2 + OFFSET + 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + OFFSET, MARGIN * 0.5 + OFFSET),
                          (0.5 * SCREEN_WIDTH, MARGIN * 0.5 + OFFSET),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - OFFSET + SCREEN_HEIGHT - MARGIN, MARGIN * 0.5 + OFFSET)]
    else:
        board = pygame.transform.scale(board, (SCREEN_WIDTH - MARGIN, SCREEN_WIDTH - MARGIN))
        BOARD_X = MARGIN * 0.5
        BOARD_Y = 0.5 * (SCREEN_HEIGHT - SCREEN_WIDTH + MARGIN)
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        print("In progress.")
        TILES_POSITION = []
    load_tiles()


def test_phase1():
    global phase, black_tiles, red_tiles, tiles
    tiles_to_place = 18
    curr_player = 0
    current_move = Move.PLACE
    crashed = False
    selected = -1
    while not crashed:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for t in tiles:
                    if t.POSITION[0] - TILE_RADIUS <= mouse[0] <= t.POSITION[0] + TILE_RADIUS and t.POSITION[
                        1] - TILE_RADIUS <= mouse[1] <= t.POSITION[1] + TILE_RADIUS:
                        if current_move == Move.PLACE:
                            if t.owner == Owner.NONE:
                                if curr_player == 0:
                                    t.owner = Owner.BLACK
                                else:
                                    t.owner = Owner.RED
                                tiles_to_place -= 1
                                if t.checkForMill(tiles) and checkTakePossible(tiles, t.owner):
                                    current_move = Move.TAKE
                                    break
                                if curr_player == 0:
                                    curr_player = 1
                                else:
                                    curr_player = 0
                                break
                        else:
                            if curr_player == 0:
                                if t.owner == Owner.RED and not t.checkForMill(tiles):
                                    t.owner = Owner.NONE
                                    current_move = Move.PLACE
                                    red_tiles -= 1
                                    curr_player = 1
                                    break
                            else:
                                if t.owner == Owner.BLACK and not t.checkForMill(tiles):
                                    t.owner = Owner.NONE
                                    current_move = Move.PLACE
                                    black_tiles -= 1
                                    curr_player = 0
                                    break

        if tiles_to_place == 0 and current_move != Move.TAKE:
            phase = 2
            break
        display_all(selected, "Phase I")
        pygame.display.update()
        clock.tick(60)

def test_phase2():
    global phase, black_tiles, red_tiles, tiles
    current_move = Move.MOVE1
    curr_player = 0
    selected_index = -1
    selected_tile = tiles[0]
    crashed = False
    while not crashed:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for t in tiles:
                    if t.POSITION[0] - TILE_RADIUS <= mouse[0] <= t.POSITION[0] + TILE_RADIUS and t.POSITION[1] - TILE_RADIUS <= mouse[1] <= t.POSITION[1] + TILE_RADIUS:
                        if current_move == Move.MOVE1:
                            if t.owner == Owner.BLACK and curr_player == 0:
                                selected_tile = t
                                selected_index = t.INDEX
                                current_move = Move.MOVE2
                                break
                            elif t.owner == Owner.RED and curr_player == 1:
                                selected_tile = t
                                selected_index = t.INDEX
                                current_move = Move.MOVE2
                                break

                        elif current_move == Move.MOVE2:
                            if selected_tile == t:
                                current_move = Move.MOVE1
                                selected_index = -1
                                break
                            elif t.checkForMove(selected_tile.INDEX, tiles):
                                if t.owner == Owner.NONE:
                                    if curr_player == 0:
                                        t.owner = Owner.BLACK
                                    else:
                                        t.owner = Owner.RED
                                    selected_tile.owner = Owner.NONE
                                    selected_index = -1
                                    if t.checkForMill(tiles) and checkTakePossible(tiles, t.owner):
                                        current_move = Move.TAKE
                                        break
                                    current_move = Move.MOVE1
                                    if curr_player == 0:
                                        curr_player = 1
                                    else:
                                        curr_player = 0


                        elif current_move == Move.TAKE:
                            if curr_player == 0:
                                if t.owner == Owner.RED and not t.checkForMill(tiles):
                                    t.owner = Owner.NONE
                                    current_move = Move.MOVE1
                                    red_tiles -= 1
                                    curr_player = 1
                                    break
                            else:
                                if t.owner == Owner.BLACK and not t.checkForMill(tiles):
                                    t.owner = Owner.NONE
                                    current_move = Move.MOVE1
                                    black_tiles -= 1
                                    curr_player = 0
                                    break
        if black_tiles < 3:
            display_all(selected_index, "Lose")
        elif red_tiles < 3:
            display_all(selected_index, "Win")
        else:
            display_all(selected_index, "Phase II")
        pygame.display.update()
        clock.tick(60)

def load_tiles():
    global tiles
    tiles = []
    # tiles go from bottom-left to right
    # a0, d0, g0, b1, d1, f1, c2, e2, a3, b3, c3, e3, f3, g3, c4, d4, e4, b5, d5, f5, a6, d6, g6
    i = 0
    for tp in TILES_POSITION:
        tiles.append(Tile(tp, i))
        tiles[i].addMills(addMills(i))
        tiles[i].addNeighbors(addNeighbors(i))
        i += 1

def display_all(selected_index, message):
    screen.fill(WHITE)
    screen.blit(board, (BOARD_X, BOARD_Y))
    phase_text = smallfont.render(message, True, BLACK)
    text_rect = phase_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(phase_text, text_rect)
    for t in tiles:
        if t.owner == Owner.BLACK:
            pygame.draw.circle(screen, BLACK, t.POSITION, TILE_RADIUS)
        elif t.owner == Owner.RED:
            pygame.draw.circle(screen, RED, t.POSITION, TILE_RADIUS)
    if selected_index >= 0:
        pygame.draw.circle(screen, YELLOW, tiles[selected_index].POSITION, TILE_RADIUS)
    #pygame.draw.circle(screen, RED, tiles[23].POSITION, TILE_RADIUS)

def checkTakePossible(tiles, owner):
    for t in tiles:
        if t.owner == owner or t.owner == Owner.NONE:
            continue
        else:
            if not t.checkForMill(tiles):
                return True

    return False

def addMills(i):
    t = []
    if i == 0:
        t.append((1, 2))
        t.append((9, 21))
    elif i == 1:
        t.append((0, 2))
        t.append((4, 7))
    elif i == 2:
        t.append((0, 1))
        t.append((14, 23))
    elif i == 3:
        t.append((4, 5))
        t.append((10, 18))
    elif i == 4:
        t.append((3, 5))
        t.append((1, 7))
    elif i == 5:
        t.append((3, 4))
        t.append((13, 20))
    elif i == 6:
        t.append((7, 8))
        t.append((11, 15))
    elif i == 7:
        t.append((6, 8))
        t.append((1, 4))
    elif i == 8:
        t.append((6, 7))
        t.append((12, 17))
    elif i == 9:
        t.append((0, 21))
        t.append((10, 11))
    elif i == 10:
        t.append((9, 11))
        t.append((3, 18))
    elif i == 11:
        t.append((9, 10))
        t.append((6, 15))
    elif i == 12:
        t.append((8, 17))
        t.append((13, 14))
    elif i == 13:
        t.append((12, 14))
        t.append((5, 20))
    elif i == 14:
        t.append((12, 13))
        t.append((2, 23))
    elif i == 15:
        t.append((6, 11))
        t.append((16, 17))
    elif i == 16:
        t.append((15, 17))
        t.append((19, 22))
    elif i == 17:
        t.append((15, 16))
        t.append((8, 12))
    elif i == 18:
        t.append((3, 10))
        t.append((19, 20))
    elif i == 19:
        t.append((16, 22))
        t.append((18, 20))
    elif i == 20:
        t.append((18, 19))
        t.append((5, 13))
    elif i == 21:
        t.append((0, 9))
        t.append((22, 23))
    elif i == 22:
        t.append((21, 23))
        t.append((16, 19))
    elif i == 23:
        t.append((21, 22))
        t.append((2, 14))

    return t

def addNeighbors(i):
    t = []
    if i == 0:
        t.append(1)
        t.append(9)
    elif i == 1:
        t.append(0)
        t.append(2)
        t.append(4)
    elif i == 2:
        t.append(1)
        t.append(14)
    elif i == 3:
        t.append(4)
        t.append(10)
    elif i == 4:
        t.append(1)
        t.append(3)
        t.append(5)
        t.append(7)
    elif i == 5:
        t.append(4)
        t.append(13)
    elif i == 6:
        t.append(7)
        t.append(11)
    elif i == 7:
        t.append(4)
        t.append(6)
        t.append(8)
    elif i == 8:
        t.append(7)
        t.append(12)
    elif i == 9:
        t.append(0)
        t.append(10)
        t.append(21)
    elif i == 10:
        t.append(3)
        t.append(9)
        t.append(11)
        t.append(17)
    elif i == 11:
        t.append(6)
        t.append(10)
        t.append(18)
    elif i == 12:
        t.append(8)
        t.append(13)
        t.append(17)
    elif i == 13:
        t.append(5)
        t.append(12)
        t.append(14)
        t.append(20)
    elif i == 14:
        t.append(2)
        t.append(13)
        t.append(23)
    elif i == 15:
        t.append(11)
        t.append(16)
    elif i == 16:
        t.append(15)
        t.append(17)
        t.append(19)
    elif i == 17:
        t.append(12)
        t.append(16)
    elif i == 18:
        t.append(10)
        t.append(19)
    elif i == 19:
        t.append(16)
        t.append(18)
        t.append(20)
        t.append(22)
    elif i == 20:
        t.append(13)
        t.append(19)
    elif i == 21:
        t.append(9)
        t.append(22)
    elif i == 22:
        t.append(19)
        t.append(21)
        t.append(23)
    elif i == 23:
        t.append(14)
        t.append(22)

    return t


initiate()
test_phase1()
test_phase2()
pygame.quit()
quit()
