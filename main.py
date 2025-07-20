# Домашнє завдання - Лабіринт
# Спосіб організації програми - процедурно-орієнтований
# Допомагаємо Шаріку знайти кісточку.
# Потрібно написати код, який перевіряє, чи правильно Шарік йде по лабіринту.

import os
#import sys
#import random
import pygame

# Ініціалізація гри
# Налаштування бібліотеки SDL
# Встановлення змінної середовища SDL_VIDEO_CENTERED у значення 1
# Вікно програми відкриється по центру екрана
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

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

level = read_file_to_list(FILE_PATH)

# Встановлюємо параметри програми
MAZE_LENGTH = len(level) * 5
SCREEN_WIDTH = SCREEN_HEIGHT = MAZE_LENGTH + 100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лабіринт")
BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
DOG_IMAGE = pygame.transform.scale(pygame.image.load('img/dog.jpg').convert_alpha(), (40, 50))
BONE_IMAGE = pygame.transform.scale(pygame.image.load('img/bone.jpg').convert_alpha(), (50, 40))

#Параметри гравця
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 15
PLAYER_COLOR = (255, 0, 0)
player_x = (SCREEN_WIDTH - MAZE_LENGTH) / 2 + 5
player_y = (SCREEN_HEIGHT - MAZE_LENGTH) / 2 + 10
player_speed = 1
player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)


# Функція малювання лабіринту
def load_level():
    x = (SCREEN_WIDTH - MAZE_LENGTH) / 2
    y = (SCREEN_HEIGHT - MAZE_LENGTH) / 2
    for row in level:
        for col in row:
            if col == "W":
                r = pygame.Rect(x, y, 5, 5)
                pygame.draw.rect(SCREEN, WALL_COLOR, r, 0)
            if col == "E":
                end_rect = pygame.Rect(x, y, 16, 16)
            x += 5
        y += 5
        x = (SCREEN_WIDTH - MAZE_LENGTH) / 2


# Обробка натискань клавіш
def processing_keystrokes():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > SCREEN_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Готуємо фон
    SCREEN.fill(BACKGROUND_COLOR)

    # Готуємо рівень
    load_level()
    SCREEN.blit(DOG_IMAGE, [(SCREEN_WIDTH - MAZE_LENGTH) / 2 - 40, (SCREEN_HEIGHT - MAZE_LENGTH) / 2 - 15])
    SCREEN.blit(BONE_IMAGE, [MAZE_LENGTH + 40, MAZE_LENGTH + 15])

    # Встановлюємо гравця в початкове положення
    pygame.draw.rect(SCREEN, PLAYER_COLOR, player_rect)
    # Обробляємо натискання клавіш
    processing_keystrokes()

    # Обновляем экран
    pygame.display.flip()

pygame.quit()