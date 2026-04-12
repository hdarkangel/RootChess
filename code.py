import pygame as p
import chess
import os
import sys
from pygame.locals import *
import chess.pgn
SAVE_FILE = "save.pgn"
WIDTH = 800 
BOARD_WIDTH = 600
HEIGHT = 600
SQ_SIZE = HEIGHT // 8
DIMENSION = 8
IMAGES = {}
p.display.set_caption('RootChess')
state = "MENU"
current_piece = 3
THEMES_PIECE = ['images', 'images1', 'images2', 'images3', 'images4']
current_theme = 4
THEMES = [
    [p.Color("#eeeed2"), p.Color("#769656")], 
    [p.Color("#f0d9b5"), p.Color("#b58863")], 
    [p.Color("#dee3e6"), p.Color("#8ca2ad")],
    [p.Color("#be9f9f"), p.Color("#771010")],
    [p.Color("#b9b9b9"), p.Color("#272727")],
    [p.Color("#B6D399"), p.Color("#86A3BE")]
]
current_panel = 4
PANELS =[
    [p.Color("#4D6139FF"), p.Color("#eeeed2")],
    [p.Color("#85644a"), p.Color("#f0d9b5")],
    [p.Color("#67767e"), p.Color("#dee3e6")],
    [p.Color("#550B0B"), p.Color("#be9f9f")],
    [p.Color("#131313"), p.Color("#b9b9b9")],
    [p.Color("#687D91"), p.Color("#B6D399")]
]
current_highlight = 3
HIGHLIGHTS = [
    [p.Color("#b9b98d"), p.Color("#5F7C42")], 
    [p.Color("#b39c78"), p.Color("#916a4a")], 
    [p.Color("#92aab9"), p.Color("#5c7480")],
    [p.Color("#9e7878"), p.Color("#630808")],
    [p.Color("#777777"), p.Color("#131212")],
    [p.Color("#91B36F"), p.Color("#5C7C99")]
]
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
current_menu = 2
MENU = [
    p.image.load(resource_path('меню0.png')),
    p.image.load(resource_path('меню1.png')),
    p.image.load(resource_path('меню2.png'))
]
icon = p.image.load(resource_path('иконка.ico'))
p.display.set_icon(icon)
def save_game_to_file(board):
    game = chess.pgn.Game.from_board(board)
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        f.write(str(game))
def load_game_from_file():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            game = chess.pgn.read_game(f)
            if game:
                return game.end().board() 
    return chess.Board() 
def load_images():
    global current_piece, THEMES_PIECE
    pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 'p', 'r', 'n', 'b', 'q', 'k']
    for piece in pieces:
        filename = ("w" if piece.isupper() else "b") + piece.upper() + ".png"
        a = THEMES_PIECE[current_piece]
        full_path = resource_path(os.path.join(a, filename))
        try:
            IMAGES[piece] = p.transform.scale(p.image.load(full_path), (SQ_SIZE, SQ_SIZE))
        except:
            print(f"Ошибка: Не найден файл {full_path}")
def draw_board(screen):
    global current_theme 
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = THEMES[current_theme][(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
def draw_highlight(screen, board, selected_sq):
    if selected_sq is not None:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100) 
        s.fill(HIGHLIGHTS[current_highlight][0])
        screen.blit(s, (chess.square_file(selected_sq) * SQ_SIZE, (7 - chess.square_rank(selected_sq)) * SQ_SIZE))
        s.fill(HIGHLIGHTS[current_highlight][1])
        for move in board.legal_moves:
            if move.from_square == selected_sq:
                target_sq = move.to_square
                screen.blit(s, (chess.square_file(target_sq) * SQ_SIZE, (7 - chess.square_rank(target_sq)) * SQ_SIZE))
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            square = chess.square(c, r)
            piece = board.piece_at(square)
            if piece:
                screen.blit(IMAGES[piece.symbol()], p.Rect(c * SQ_SIZE, (7 - r) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
def draw_end_game_text(screen, text):
    font = p.font.Font(resource_path("шрифт.ttf"), 32)
    overlay = p.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(p.Color("black"))
    screen.blit(overlay, (0, 0))
    text_object = font.render(text, True, p.Color('White'))
    text_location = text_object.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_object, text_location)
def draw_move_log(screen, board):
    log_rect = p.Rect(BOARD_WIDTH, 0, WIDTH - BOARD_WIDTH, HEIGHT)
    p.draw.rect(screen, PANELS[current_panel][0], log_rect)
    font = p.font.Font(resource_path("шрифт.ttf"), 25) 
    temp_board = chess.Board()
    move_texts = []
    moves = board.move_stack 
    for i in range(0, len(moves), 2):
        move_num = i // 2 + 1
        white_move = temp_board.san(moves[i])
        temp_board.push(moves[i])
        black_move = ""
        if i + 1 < len(moves):
            black_move = temp_board.san(moves[i+1])
            temp_board.push(moves[i+1])
        move_texts.append(f"{move_num}. {white_move} {black_move}")
    visible_moves = move_texts[-25:] 
    for i, text in enumerate(visible_moves):
        text_obj = font.render(text, True, PANELS[current_panel][1])
        screen.blit(text_obj, (BOARD_WIDTH + 10, 20 + i * 22))
def main():
    global current_theme, state, current_piece, current_panel, current_highlight, current_menu
    p.init()
    board = load_game_from_file() 
    game_over = board.is_game_over()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    load_images()
    clock = p.time.Clock()
    selected_sq = None
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_RETURN:
                    if len(board.move_stack) > 0:
                        board.pop()
                        selected_sq = None 
                        game_over = board.is_game_over()
                        save_game_to_file(board)
                if e.key == p.K_q:
                    state = "MENU"
                if e.key == p.K_s:
                    state = "GAME"
                if e.key == p.K_r:
                    board.reset()
                    game_over = False
                    selected_sq = None
                    save_game_to_file(board)
                if e.key == p.K_1:
                    current_panel = (current_panel + 1) % len(PANELS)
                if e.key == p.K_2:
                    current_theme = (current_theme + 1) % len(THEMES)
                if e.key == p.K_3:
                    current_piece = (current_piece + 1) % len(THEMES_PIECE)
                    load_images()
                if e.key == p.K_4:
                    current_highlight = (current_highlight + 1) % len(HIGHLIGHTS)
                if e.key == p.K_5:
                    current_menu = (current_menu + 1) % len(MENU)
            elif e.type == p.MOUSEBUTTONDOWN and not game_over:
                if state == "GAME":
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = 7 - (location[1] // SQ_SIZE)
                    if col >= 8:
                        continue
                    square = chess.square(col, row)
                    if selected_sq is None:
                        piece = board.piece_at(square)
                        if piece and piece.color == board.turn:
                            selected_sq = square
                    else:
                        if selected_sq == square:
                            selected_sq = None
                        else:
                            move = chess.Move(selected_sq, square)
                            piece_to_move = board.piece_at(selected_sq)
                            if piece_to_move and piece_to_move.piece_type == chess.PAWN:
                                if (chess.square_rank(square) == 7 and board.turn == chess.WHITE) or \
                                   (chess.square_rank(square) == 0 and board.turn == chess.BLACK):
                                       move.promotion = chess.QUEEN
                            if move in board.legal_moves:
                                board.push(move)
                                selected_sq = None
                                save_game_to_file(board)
                            else:
                                piece = board.piece_at(square)
                                if piece and piece.color == board.turn:
                                    selected_sq = square
                                else:
                                    selected_sq = None
        if state == "MENU":
            image = MENU[current_menu]
            screen.blit(image, (0, 0))
        else:
            draw_board(screen)
            draw_highlight(screen, board, selected_sq)
            draw_pieces(screen, board)
            draw_move_log(screen, board)
            if board.is_game_over():
                game_over = True
                if board.is_checkmate():
                    if board.turn == chess.WHITE:
                        draw_end_game_text(screen, "Игра завершена, победа черных")
                    else:
                        draw_end_game_text(screen, "Игра завершена, победа белых")
                else:
                    draw_end_game_text(screen, "Ничья")
        clock.tick(30)
        p.display.flip()
    p.quit()

if __name__ == "__main__": 
    main()