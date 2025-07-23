# Домашнє завдання - Лабіринт
# Спосіб організації програми - процедурно-орієнтованний спосіб
# Допомагаємо Шаріку знайти кісточку.
# Потрібно написати код, який перевіряє, чи правильно Шарік йде по лабіринту.

import os
import pygame
from collections import deque

# Ініціалізація та налаштування
# Налаштування бібліотеки SDL
# Вікно програми відкриється по центру екрана
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Шлях до файлу з лабіринтом
FILE_PATH = "levels/0.txt"
horizontal_length = 0


# Читаємо рівень з файлу
def read_file_to_list(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            lines = [line.rstrip('\n') for line in lines]
            return lines

    except FileNotFoundError:
        print(f"Помилка: Файл не знайден по шляху: {filepath}")
        return None
    except Exception as e:
        print(f"Виникла помилка при читанні файла: {e}")
        return None

level = read_file_to_list(FILE_PATH)
if level is None:
    exit()


# Визначаємо старт і фініш
# Тут припустимо, що старт — це перший відкритий вхід (зовнішня клітинка без стін)
# і аналогічно для фінішу.
def find_start_end(level):
    start = None
    end = None
    rows = len(level)
    cols = len(level[0])
    for r in range(rows):
        for c in range(cols):
            if level[r][c] != "W":
                # пошук старту в перших або останніх рядках/стовпцях
                if r == 0 or r == rows -1 or c == 0 or c == cols -1:
                    if start is None:
                        start = (r, c)
                    else:
                        end = (r, c)
    return start, end

start_pos, end_pos = find_start_end(level)
if start_pos is None or end_pos is None:
    print("Не знайдено старт або фініш.")
    exit()
else:
    print("Старт та фініш знайдені")

# Алгоритм BFS для пошуку шляху
def find_path_bfs(level, start, end):
    rows = len(level)
    cols = len(level[0])
    visited = [[False]*cols for _ in range(rows)]
    parent = [[None]*cols for _ in range(rows)]
    queue = deque()

    queue.append(start)
    visited[start[0]][start[1]] = True

    directions = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
    }

    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            # Відновлюємо шлях
            path = []
            while (r, c) != start:
                pr, pc = parent[r][c]
                if pr == r - 1:
                    path.append('DOWN')
                elif pr == r + 1:
                    path.append('UP')
                elif pc == c - 1:
                    path.append('RIGHT')
                elif pc == c + 1:
                    path.append('LEFT')
                r, c = pr, pc
            path.reverse()
            return path

        for move, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if not visited[nr][nc] and level[nr][nc] != "W":  # не стіна
                    visited[nr][nc] = True
                    parent[nr][nc] = (r, c)
                    queue.append((nr, nc))
    return []

# Знаходимо шлях
CORRECT_PATH = find_path_bfs(level, start_pos, end_pos)
print("Знайдено шлях:", CORRECT_PATH)



# Налаштування екрана
MAZE_LENGTH = len(level) * 5
SCREEN_WIDTH = SCREEN_HEIGHT = MAZE_LENGTH + 100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лабіринт")
BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)

# Завантаження зображень
DOG_IMAGE = pygame.transform.scale(pygame.image.load('img/dog.jpg').convert_alpha(), (40, 50))
BONE_IMAGE = pygame.transform.scale(pygame.image.load('img/bone.jpg').convert_alpha(), (50, 40))

#Параметри гравця
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 15
PLAYER_COLOR = (255, 0, 0)
PLAYER_X = (SCREEN_WIDTH - MAZE_LENGTH) / 2 + 15
PLAYER_Y = (SCREEN_HEIGHT - MAZE_LENGTH) / 2 + 10
player_rect = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)

# Визначений правильний шлях (можна змінювати під рівень)
CORRECT_PATH = ['RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'DOWN', 'DOWN', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'DOWN', 'RIGHT', 'RIGHT']  # приклад правильного шляху
path_index = 0  # індекс для правильного шляху
previous_move = None
GAME_OVER = False
game_result = None  # 'WIN', 'HIT_WALL', 'RUN_AWAY', 'LOST'


# Функція для малювання рівня
# Малює лабіринт і повертає список стін
def load_level():
    global walls
    walls = []  # очищаємо список перед завантаженням
    x = (SCREEN_WIDTH - MAZE_LENGTH) / 2
    y = (SCREEN_HEIGHT - MAZE_LENGTH) / 2
    for row in level:
        for col in row:
            if col == "W":
                wall_rect = pygame.Rect(x, y, 5, 5)
                pygame.draw.rect(SCREEN, WALL_COLOR, wall_rect, 0)
                walls.append(wall_rect)
            x += 5
        y += 5
        x = (SCREEN_WIDTH - MAZE_LENGTH) / 2


# Функція для показу повідомлень у конкретних координатах
def show_message(text, x, y):
    font = pygame.font.SysFont("Arial", 20)
    message = font.render(text, True, (255, 0, 0))
    message_rect = message.get_rect(topleft=(x, y))
    SCREEN.blit(message, message_rect)
    pygame.display.flip()


# Функція перевірки правильності руху
def check_move(direction):
    global path_index, previous_move, GAME_OVER, game_result
    if GAME_OVER:
        return

    # Перевірити чи правильний напрямок
    if path_index < len(CORRECT_PATH) and direction == CORRECT_PATH[path_index]:
        print("Шарік знайшов правильний шлях")
        path_index += 1
        previous_move = direction
        # Перевірка чи пройшли весь шлях
        if path_index == len(CORRECT_PATH):
            print("Вітаємо! Шарік пройшов лабіринт! Перемога!")
            show_message("Перемога! Шарік пройшов лабіринт", 10, 10)
            GAME_OVER = True
            game_result = 'WIN'
    else:
        # Перевірка чи йде у бік стіни
        if direction == 'INVALID':
            print("Шарік вдарився об стіну, гра завершена.")
            GAME_OVER = True
            game_result = 'HIT_WALL'
        # Перевірка чи повернув назад
        elif previous_move and ((direction == 'LEFT' and previous_move == 'RIGHT') or
                                (direction == 'RIGHT' and previous_move == 'LEFT') or
                                (direction == 'UP' and previous_move == 'DOWN') or
                                (direction == 'DOWN' and previous_move == 'UP')):
            print("Шарік злякався і втік, гра завершена.")
            GAME_OVER = True
            game_result = 'RUN_AWAY'
        else:
            print("Шарік заблукав, гра завершена.")
            GAME_OVER = True
            game_result = 'LOST'

# Переміщення гравця
def move_player(dx, dy):
    global player_rect
    new_rect = player_rect.move(dx / 2, dy / 2)

    # Перевірка зіткнення зі стінами
    for wall in walls:
        if new_rect.colliderect(wall):
            check_move('INVALID')
            return  # рух заборонений, вихід

    # Визначаємо напрямок
    if dx > 0:
        check_move('RIGHT')
    elif dx < 0:
        check_move('LEFT')
    elif dy > 0:
        check_move('DOWN')
    elif dy < 0:
        check_move('UP')
    else:
        # Якщо руху немає
        return

    # Якщо гра не завершена, виконуємо рух
    if not GAME_OVER:
        player_rect.x += dx
        player_rect.y += dy


# Основний цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not GAME_OVER:
                if event.key == pygame.K_LEFT:
                    move_player(-30, 0)
                elif event.key == pygame.K_RIGHT:
                    move_player(30, 0)
                elif event.key == pygame.K_UP:
                    move_player(0, -30)
                elif event.key == pygame.K_DOWN:
                    move_player(0, 30)
                elif event.key == pygame.K_ESCAPE:
                    running = False


    # Малюємо фон
    SCREEN.fill(BACKGROUND_COLOR)

    if GAME_OVER:
        # Після завершення гри виводимо повідомлення
        if game_result == 'WIN':
            show_message("Вітаємо з перемогою!", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
        elif game_result == 'HIT_WALL':
            show_message("Шарік вдарився об стіну, гра завершена.", SCREEN_WIDTH // 10, SCREEN_HEIGHT // 3)
        elif game_result == 'RUN_AWAY':
            show_message("Шарік злякався і втік, гра завершена.", SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3)
        elif game_result == 'LOST':
            show_message("Шарік заблукав, гра завершена.", SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3)
    else:
        # Готуємо рівень
        load_level()
        SCREEN.blit(DOG_IMAGE, [(SCREEN_WIDTH - MAZE_LENGTH) / 2 - 40, (SCREEN_HEIGHT - MAZE_LENGTH) / 2 - 15])
        SCREEN.blit(BONE_IMAGE, [MAZE_LENGTH + 40, MAZE_LENGTH + 15])
        # Малюємо рівень та гравця
        pygame.draw.rect(SCREEN, PLAYER_COLOR, player_rect)


    # Оновлюємо екран
    pygame.display.flip()

pygame.quit()