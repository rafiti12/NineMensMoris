import pygame
import pygame_menu

from constants import *
from Tile import Tile
import math
import copy


def initiate():
    global screen, clock, board, smallfont, phase, black_tiles, red_tiles, BOARD_X, BOARD_Y, TILES_POSITION, PLAYER0, PLAYER1, PLAYER_CPU
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    board = pygame.image.load('../board.png')
    smallfont = pygame.font.SysFont('Corbel', 60)
    font = pygame.font.SysFont('ArialBlack', 26)
    PLAYER0 = font.render("Player 1 round", True, (0, 0, 0))
    PLAYER1 = font.render("Player 2 round", True, (0, 0, 0))
    PLAYER_CPU = font.render("CPU round", True, (0, 0, 0))
    phase = 1
    black_tiles = 9
    red_tiles = 9
    if SCREEN_WIDTH >= SCREEN_HEIGHT:
        board = pygame.transform.scale(board, (SCREEN_HEIGHT - MARGIN, SCREEN_HEIGHT - MARGIN))
        BOARD_X = 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN)
        BOARD_Y = MARGIN * 0.5
        TILES_POSITION = [(0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + OFFSET, SCREEN_HEIGHT - MARGIN + OFFSET),
                          (0.5 * SCREEN_WIDTH, SCREEN_HEIGHT - MARGIN + OFFSET),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - OFFSET + SCREEN_HEIGHT - MARGIN,
                           SCREEN_HEIGHT - MARGIN + OFFSET),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1 / 6 * SCREEN_HEIGHT,
                           SCREEN_HEIGHT - MARGIN + OFFSET - 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1 / 2 * (SCREEN_HEIGHT - MARGIN),
                           SCREEN_HEIGHT - MARGIN + OFFSET - 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 1 / 6 * SCREEN_HEIGHT,
                           SCREEN_HEIGHT - MARGIN + OFFSET - 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 2 / 6 * (SCREEN_HEIGHT - MARGIN / 2),
                           SCREEN_HEIGHT - MARGIN + OFFSET - 2 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * SCREEN_WIDTH, SCREEN_HEIGHT - MARGIN + OFFSET - 2 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 2 / 6 * (
                                  SCREEN_HEIGHT - MARGIN / 2),
                           SCREEN_HEIGHT - MARGIN + OFFSET - 2 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + OFFSET, SCREEN_HEIGHT / 2),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1 / 6 * SCREEN_HEIGHT, SCREEN_HEIGHT / 2),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 2 / 6 * (SCREEN_HEIGHT - MARGIN / 2),
                           SCREEN_HEIGHT / 2),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 2 / 6 * (
                                  SCREEN_HEIGHT - MARGIN / 2), SCREEN_HEIGHT / 2),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 1 / 6 * SCREEN_HEIGHT,
                           SCREEN_HEIGHT / 2),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - OFFSET + SCREEN_HEIGHT - MARGIN,
                           SCREEN_HEIGHT / 2),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 2 / 6 * (SCREEN_HEIGHT - MARGIN / 2),
                           SCREEN_HEIGHT - MARGIN / 2 + OFFSET - 4 / 6 * (SCREEN_HEIGHT - MARGIN / 2)),
                          (0.5 * SCREEN_WIDTH,
                           SCREEN_HEIGHT - MARGIN / 2 + OFFSET - 4 / 6 * (SCREEN_HEIGHT - MARGIN / 2)),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 2 / 6 * (
                                  SCREEN_HEIGHT - MARGIN / 2),
                           SCREEN_HEIGHT - MARGIN / 2 + OFFSET - 4 / 6 * (SCREEN_HEIGHT - MARGIN / 2)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1 / 6 * SCREEN_HEIGHT,
                           MARGIN / 2 + OFFSET + 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + 1 / 2 * (SCREEN_HEIGHT - MARGIN),
                           MARGIN / 2 + OFFSET + 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (SCREEN_WIDTH - 0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - 1 / 6 * SCREEN_HEIGHT,
                           MARGIN / 2 + OFFSET + 1 / 6 * (SCREEN_HEIGHT - MARGIN)),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) + OFFSET, MARGIN * 0.5 + OFFSET),
                          (0.5 * SCREEN_WIDTH, MARGIN * 0.5 + OFFSET),
                          (0.5 * (SCREEN_WIDTH - SCREEN_HEIGHT + MARGIN) - OFFSET + SCREEN_HEIGHT - MARGIN,
                           MARGIN * 0.5 + OFFSET)]
    else:
        board = pygame.transform.scale(board, (SCREEN_WIDTH - MARGIN, SCREEN_WIDTH - MARGIN))
        BOARD_X = MARGIN * 0.5
        BOARD_Y = 0.5 * (SCREEN_HEIGHT - SCREEN_WIDTH + MARGIN)
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        print("In progress.")
        TILES_POSITION = []
    load_tiles()


def pve_phase1():
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    showMenu()

            if curr_player == 1:
                temp_tiles = None
                temp_tiles = copy.deepcopy(tiles)
                best_score = -math.inf
                moves = generate_possible_moves_phase1(tiles, current_move, Owner.RED)

                for m in moves:
                    if current_move == Move.PLACE:
                        temp_tiles[m].owner = Owner.RED
                    elif current_move == Move.TAKE:
                        temp_tiles[m].owner = Owner.NONE
                    score = -minimax_phase1(temp_tiles, 4, -math.inf, math.inf, current_move, True)
                    if current_move == Move.PLACE:
                        temp_tiles[m].owner = Owner.NONE
                    elif current_move == Move.TAKE:
                        temp_tiles[m].owner = Owner.RED
                    # print(score)
                    if score > best_score:
                        best_score = score
                        best_move = m
                # print("--------------------")
                if current_move == Move.PLACE:
                    tiles[best_move].owner = Owner.RED
                elif current_move == Move.TAKE:
                    tiles[best_move].owner = Owner.NONE

                if current_move == Move.PLACE:
                    tiles_to_place -= 1
                    if tiles[best_move].checkForMill(tiles) and checkTakePossible(tiles, Owner.RED):
                        current_move = Move.TAKE
                        break
                elif current_move == Move.TAKE:
                    black_tiles -= 1
                    current_move = Move.PLACE

                curr_player = 0

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
        printGameStatus(curr_player, True)
        pygame.display.update()
        clock.tick(60)


def pvp_phase1():
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    crashed = True
                    showMenu()

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
        printGameStatus(curr_player, False)
        pygame.display.update()
        clock.tick(60)


def pve_phase2():
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    showMenu()

            if curr_player == 1:
                temp_tiles = copy.deepcopy(tiles)
                best_score = -math.inf
                moves = generate_possible_moves_phase2(tiles, current_move, Owner.RED)
                for m in moves:
                    if current_move == Move.MOVE1:
                        temp_tiles[m.frm].owner = Owner.NONE
                        temp_tiles[m.to].owner = Owner.RED
                    elif current_move == Move.TAKE:
                        temp_tiles[m].owner = Owner.NONE
                    score = -minimax_phase2(temp_tiles, 4, -math.inf, math.inf, current_move, True)
                    if current_move == Move.MOVE1:
                        temp_tiles[m.frm].owner = Owner.RED
                        temp_tiles[m.to].owner = Owner.NONE
                    elif current_move == Move.TAKE:
                        temp_tiles[m].owner = Owner.RED
                    if score > best_score:
                        best_score = score
                        best_move = m
                print(best_score)
                print(best_move)
                if current_move == Move.MOVE1:
                    tiles[best_move.frm].owner = Owner.NONE
                    tiles[best_move.to].owner = Owner.RED
                elif current_move == Move.TAKE:
                    tiles[best_move].owner = Owner.NONE

                if current_move == Move.MOVE1:
                    if tiles[best_move[1]].checkForMill(tiles) and checkTakePossible(tiles, Owner.RED):
                        current_move = Move.TAKE
                        break
                elif current_move == Move.TAKE:
                    black_tiles -= 1
                    current_move = Move.MOVE1

                curr_player = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                for t in tiles:
                    if t.POSITION[0] - TILE_RADIUS <= mouse[0] <= t.POSITION[0] + TILE_RADIUS and t.POSITION[
                        1] - TILE_RADIUS <= mouse[1] <= t.POSITION[1] + TILE_RADIUS:
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
            # Jeśli z komputerem to True, jeśli z graczem False
            printGameStatus(curr_player, True)

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    showMenu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for t in tiles:
                    if t.POSITION[0] - TILE_RADIUS <= mouse[0] <= t.POSITION[0] + TILE_RADIUS and t.POSITION[
                        1] - TILE_RADIUS <= mouse[1] <= t.POSITION[1] + TILE_RADIUS:
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
            # Jeśli z komputerem to True, jeśli z graczem False
            printGameStatus(curr_player, False)

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
    text_rect = phase_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(phase_text, text_rect)
    for t in tiles:
        if t.owner == Owner.BLACK:
            pygame.draw.circle(screen, BLACK, t.POSITION, TILE_RADIUS)
        elif t.owner == Owner.RED:
            pygame.draw.circle(screen, RED, t.POSITION, TILE_RADIUS)
    if selected_index >= 0:
        pygame.draw.circle(screen, YELLOW, tiles[selected_index].POSITION, TILE_RADIUS)
    # pygame.draw.circle(screen, RED, tiles[23].POSITION, TILE_RADIUS)


def checkTakePossible(tiles, owner):
    for t in tiles:
        if t.owner == owner or t.owner == Owner.NONE:
            continue
        else:
            if not t.checkForMill(tiles):
                return True

    return False


def evaluate_phase1(_tiles, player):
    ai = Owner.RED
    ai_mill_points = 250
    player_mill_points = 300
    ai_possible_mill_points = 60
    player_possible_mill_points = 80

    score = 0

    # red = 0
    # black = 0

    for t in _tiles:
        #     if t.owner == Owner.RED:
        #         red += 1
        #     else:
        #         black += 1

        # return  black - red
        if t.checkForMill(_tiles) and t.owner == player:
            if player == ai:
                score += ai_mill_points
            else:
                score += player_mill_points

        possible_mills = t.countPossibleMills(_tiles)
        if possible_mills > 0 and t.owner == player:
            if player == ai:
                score += ai_possible_mill_points * possible_mills
            else:
                score += player_possible_mill_points * possible_mills

        if t.owner == ai:
            score += 1

    return score


def generate_possible_moves_phase1(_tiles, move, player):
    possible_moves = []

    if move == Move.PLACE:
        for t in _tiles:
            if t.owner == Owner.NONE:
                possible_moves.append(t.INDEX)
    else:
        for t in _tiles:
            if t.owner != Owner.NONE and t.owner != player and not t.checkForMill(_tiles):
                possible_moves.append(t.INDEX)
        pass

    return possible_moves


def evaluate_phase2(_tiles, player):
    #print(player)
    ai = Owner.RED
    ai_mill_points = 250
    player_mill_points = 300
    ai_possible_mill_points = 60
    player_possible_mill_points = 80

    score = 0

    for t in _tiles:
        if t.checkForMill(_tiles) and t.owner == player:
            if player == ai:
                score += ai_mill_points
            else:
                score += player_mill_points

        possible_mills = t.countPossibleMills(_tiles)
        if possible_mills > 0 and t.owner == player:
            if player == ai:
                score += ai_possible_mill_points * possible_mills
            else:
                score += player_possible_mill_points * possible_mills

    return score


def generate_possible_moves_phase2(_tiles, move, player):
    possible_moves = []
    if move == Move.MOVE1:
        for t in tiles:
            if t.owner == player:
                for n in t.NEIGHBORS:
                    if _tiles[n].owner == Owner.NONE:
                        possible_moves.append(TileMove(t.INDEX, n))
    else:
        for t in _tiles:
            if t.owner != Owner.NONE and t.owner != player and not t.checkForMill(_tiles):
                possible_moves.append(t.INDEX)
        pass

    return possible_moves


# minimax with alpha-beta pruning
def minimax_phase1(_tiles, depth, alpha, beta, move, maximizing):
    if depth == 0:
        return evaluate_phase1(_tiles, (Owner.RED, Owner.BLACK)[maximizing])

    if maximizing:
        max_eval = -math.inf
        moves = generate_possible_moves_phase1(_tiles, move, Owner.RED)
        for m in moves:
            if move == Move.PLACE:
                _tiles[m].owner = Owner.RED
            elif move == Move.TAKE:
                _tiles[m].owner = Owner.NONE
            eval = -minimax_phase1(_tiles, depth - 1, alpha, beta, move, False)
            if move == Move.PLACE:
                _tiles[m].owner = Owner.NONE
            elif move == Move.TAKE:
                _tiles[m].owner = Owner.RED

            max_eval = max(eval, max_eval)

            alpha = max(alpha, eval)

            if beta <= alpha:
                break

        return max_eval
    else:
        min_eval = math.inf
        moves = generate_possible_moves_phase1(_tiles, move, Owner.BLACK)
        for m in moves:
            if move == Move.PLACE:
                _tiles[m].owner = Owner.BLACK
            elif move == Move.TAKE:
                _tiles[m].owner = Owner.NONE
            eval = minimax_phase1(_tiles, depth - 1, alpha, beta, move, True)
            if move == Move.PLACE:
                _tiles[m].owner = Owner.NONE
            elif move == Move.TAKE:
                _tiles[m].owner = Owner.BLACK

            min_eval = min(eval, min_eval)

            beta = min(beta, eval)

            if beta <= alpha:
                break

        return min_eval


def minimax_phase2(_tiles, depth, alpha, beta, move, maximizing):
    if depth == 0:
        return evaluate_phase2(_tiles, (Owner.RED, Owner.BLACK)[maximizing])

    if maximizing:
        max_eval = -math.inf
        moves = generate_possible_moves_phase2(_tiles, move, Owner.RED)
        for m in moves:
            if move == Move.MOVE1:
                _tiles[m.frm].owner = Owner.NONE
                _tiles[m.to].owner = Owner.RED
            elif move == Move.TAKE:
                _tiles[m].owner = Owner.NONE
            eval = -minimax_phase2(_tiles, depth - 1, alpha, beta, move, False)
            if move == Move.MOVE1:
                _tiles[m.frm].owner = Owner.RED
                _tiles[m.to].owner = Owner.NONE
            elif move == Move.TAKE:
                _tiles[m].owner = Owner.RED

            max_eval = max(eval, max_eval)

            alpha = max(alpha, eval)

            if beta <= alpha:
                break

        return max_eval
    else:
        min_eval = math.inf
        moves = generate_possible_moves_phase2(_tiles, move, Owner.BLACK)
        for m in moves:
            if move == Move.PLACE:
                _tiles[m.frm].owner = Owner.NONE
                _tiles[m.to].owner = Owner.BLACK
            elif move == Move.TAKE:
                _tiles[m].owner = Owner.NONE
            eval = minimax_phase2(_tiles, depth - 1, alpha, beta, move, True)
            if move == Move.PLACE:
                _tiles[m.frm].owner = Owner.BLACK
                _tiles[m.to].owner = Owner.NONE
            elif move == Move.TAKE:
                _tiles[m].owner = Owner.BLACK

            min_eval = min(eval, min_eval)

            beta = min(beta, eval)

            if beta <= alpha:
                break

        return min_eval


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
        t.append(18)
    elif i == 11:
        t.append(6)
        t.append(10)
        t.append(15)
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


def printGameStatus(player, cpu):
    global PLAYER0, PLAYER1, PLAYER_CPU
    if player == 0:
        screen.blit(PLAYER0, (SCREEN_WIDTH / 2 - 105, SCREEN_HEIGHT / 2 + 28))
    elif player == 1 and not cpu:
        screen.blit(PLAYER1, (SCREEN_WIDTH / 2 - 105, SCREEN_HEIGHT / 2 + 28))
    elif player == 1 and cpu:
        screen.blit(PLAYER_CPU, (SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 + 28))


def startTheGamePVP():
    initiate()
    pvp_phase1()
    test_phase2()


def startTheGamePVE():
    initiate()
    pve_phase1()
    pve_phase2()


def showMenu():
    menu_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = pygame_menu.Menu('NineMensMoris', SCREEN_WIDTH, SCREEN_HEIGHT,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play vs Player', startTheGamePVP)
    menu.add.button('Play vs Computer', startTheGamePVE)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(menu_surface)


def init():
    pygame.init()
    showMenu()


init()
pygame.quit()
quit()
