# Домашнє завдання - Лабіринт
# Спосіб організації програми - процедурно-орієнтованний спосіб
# Допомагаємо Шаріку знайти кісточку.
# Потрібно написати код, який перевіряє, чи правильно Шарік йде по лабіринту.

import os
import pygame

# Ініціалізація гри
# Налаштування бібліотеки SDL
# Встановлення змінної середовища SDL_VIDEO_CENTERED у значення 1
# Вікно програми відкриється по центру екрана
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Шлях до файлу з лабіринтом
FILE_PATH = "levels/0.txt"
horizontal_length = 0

# Функція читання схеми лабіринту в список
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

# Читаємо рівень
level = read_file_to_list(FILE_PATH)
if level is None:
    exit()

# Встановлюємо параметри програми
MAZE_LENGTH = len(level) * 5
SCREEN_WIDTH = SCREEN_HEIGHT = MAZE_LENGTH + 100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лабіринт")
BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
ENTER_COLOR = (255, 255, 255)
DOG_IMAGE = pygame.transform.scale(pygame.image.load('img/dog.jpg').convert_alpha(), (40, 50))
BONE_IMAGE = pygame.transform.scale(pygame.image.load('img/bone.jpg').convert_alpha(), (50, 40))

#Параметри гравця
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 15
PLAYER_COLOR = (255, 0, 0)
PLAYER_X = (SCREEN_WIDTH - MAZE_LENGTH) / 2 + 15
PLAYER_Y = (SCREEN_HEIGHT - MAZE_LENGTH) / 2 + 10
player_rect = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)

# Правильний шлях до виходу
CORRECT_PATH = ['RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'DOWN', 'DOWN', 'RIGHT', 'RIGHT', 'RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'DOWN', 'RIGHT']  # приклад правильного шляху
path_index = 0  # індекс для правильного шляху
previous_move = None
GAME_OVER = False


# Функція малювання лабіринту
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

def check_move(direction):
    global path_index, previous_move, GAME_OVER
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
            GAME_OVER = True
    else:
        # Перевірка чи йде у бік стіни
        if direction == 'INVALID':
            print("Шарік вдарився об стіну, гра завершена.")
            GAME_OVER = True
        # Перевірка чи повернув назад
        elif previous_move and ((direction == 'LEFT' and previous_move == 'RIGHT') or
                                (direction == 'RIGHT' and previous_move == 'LEFT') or
                                (direction == 'UP' and previous_move == 'DOWN') or
                                (direction == 'DOWN' and previous_move == 'UP')):
            print("Шарік злякався і втік, гра завершена.")
            GAME_OVER = True
        else:
            print("Шарік заблукав, гра завершена.")
            GAME_OVER = True

def move_player(dx, dy):
    new_rect = player_rect.move(dx / 2, dy / 2)

    # Перевірка колізій з усіма стінками
    for wall in walls:
        if new_rect.colliderect(wall):
            check_move('INVALID')
            return  # рух заборонений, вихід

    # Перевірка напрямку
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


    # Готуємо фон
    SCREEN.fill(BACKGROUND_COLOR)

    # Готуємо рівень
    load_level()
    SCREEN.blit(DOG_IMAGE, [(SCREEN_WIDTH - MAZE_LENGTH) / 2 - 40, (SCREEN_HEIGHT - MAZE_LENGTH) / 2 - 15])
    SCREEN.blit(BONE_IMAGE, [MAZE_LENGTH + 40, MAZE_LENGTH + 15])

    # Готує гравця
    pygame.draw.rect(SCREEN, PLAYER_COLOR, player_rect)

    # Обновляем экран
    pygame.display.flip()

pygame.quit()