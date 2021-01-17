# INSTRUCTIONS
# Use arrow keys to move around
# Press 1 to open the boxes
# Press 2 to Flag
# Dont use the numpad keys
# The game finishes when you open all boxes or open a box having bomb
# u/DarkLord0206

import random
import time
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_1,
    K_2
)

number = 5
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450
wid = int(SCREEN_WIDTH / number)
hig = int(SCREEN_HEIGHT / number)
pygame.init()
pygame.font.init()
typer = pygame.font.SysFont("Comic Sans MS", 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BOMBS = 5
FINAL_TEXT = "PRESS ESCAPE AGAIN"
tiles_turned = 0


class box(pygame.sprite.Sprite):
    def __init__(self, x_coordinate, y_coordinate, value, color):
        super(box, self).__init__()
        self.x = x_coordinate
        self.y = y_coordinate
        self.val = value
        self.surf = pygame.Surface((wid, hig))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center=(int(self.x * wid + wid / 2), int(self.y * hig + hig / 2)))
        if self.val == 0:
            self.text = typer.render("", False, (255, 0, 0))
        else:
            self.text = typer.render(str(value), False, (255, 0, 0))
        self.chk = False
        self.isFlagged = False

    def update_text(self):
        global tiles_turned
        self.chk = True
        tiles_turned += 1
        color = (220, 220, 220)
        self.val = count(hidden, self.x + 1, self.y + 1)
        if self.val == 0:
            color = (220, 220, 220)
        elif self.val == 2:
            color = (0, 0, 255)
        elif self.val == 3:
            color = (220, 20, 60)
        elif self.val == 1:
            color = (34, 139, 34)
        elif self.val == 10:
            color = (255, 0, 0)
        elif self.val > 3:
            color = (255, 0, 0)
        self.text = typer.render(str(self.val), False, color)
        self.surf.fill((220, 220, 220))


def make_bombs(row, col):
    arr = make_2d(row + 2, col + 2)
    bombs_done = 0
    while not bombs_done == BOMBS:
        x = random.randint(1, number)
        y = random.randint(1, number)
        if arr[x][y] != 10:
            arr[x][y] = 10
            bombs_done += 1
    return arr


def make_2d_box(row, col):
    arr = []
    for i in range(row):
        x = []
        for j in range(col):
            x.append(box(i, j, 0, (105, 105, 105)))
        arr.append(x)
    return arr


def make_2d(row, col):
    arr = []
    for i in range(row):
        x = []
        for j in range(col):
            x.append(0)
        arr.append(x)
    return arr


hidden = make_bombs(number, number)
user = make_2d_box(number, number)


def update_values(current, prv):
    if prv[0] == current[0] and prv[1] == current[1]:
        return
    if current[0] < 0 or current[0] >= number:
        return
    if current[1] < 0 or current[1] >= number:
        return
    if user[current[0]][current[1]].chk:
        return
    user[current[0]][current[1]].update_text()
    if user[current[0]][current[1]].val == 0:
        s = [current[0], current[1] + 1]
        update_values(s, current)
        s = [current[0], current[1] - 1]
        update_values(s, current)
        s = [current[0] + 1, current[1] + 1]
        update_values(s, current)
        s = [current[0] - 1, current[1] + 1]
        update_values(s, current)
        s = [current[0] + 1, current[1] - 1]
        update_values(s, current)
        s = [current[0] + 1, current[1]]
        update_values(s, current)
        s = [current[0] - 1, current[1] - 1]
        update_values(s, current)
        s = [current[0] - 1, current[1]]
        update_values(s, current)
    else:
        return


def update(bos_up, key):
    if key.key == K_UP:
        bos_up.rect.move_ip(0, -hig)
    if key.key == K_DOWN:
        bos_up.rect.move_ip(0, hig)
    if key.key == K_LEFT:
        bos_up.rect.move_ip(-wid, 0)
    if key.key == K_RIGHT:
        bos_up.rect.move_ip(hig, 0)
    if bos_up.rect.left < 0:
        bos_up.rect.left = 0
    if bos_up.rect.right > SCREEN_WIDTH:
        bos_up.rect.right = SCREEN_WIDTH
    if bos_up.rect.top <= 0:
        bos_up.rect.top = 0
    if bos_up.rect.bottom >= SCREEN_HEIGHT:
        bos_up.rect.bottom = SCREEN_HEIGHT


def count(array, row, col):
    count1 = 0
    if not array[row][col] == 0:
        return 10
    if array[row + 1][col] == 10:
        count1 = count1 + 1
    if array[row + 1][col - 1] == 10:
        count1 = count1 + 1
    if array[row + 1][col + 1] == 10:
        count1 = count1 + 1
    if array[row][col + 1] == 10:
        count1 = count1 + 1
    if array[row][col - 1] == 10:
        count1 = count1 + 1
    if array[row - 1][col] == 10:
        count1 = count1 + 1
    if array[row - 1][col + 1] == 10:
        count1 = count1 + 1
    if array[row - 1][col - 1] == 10:
        count1 = count1 + 1
    return count1


def toggle_Flag(s, p):
    if user[s[0]][s[1]].isFlagged:
        user[s[0]][s[1]].surf.fill((105, 105, 105))
        user[s[0]][s[1]].isFlagged = False
        p = p - 1
    else:
        user[s[0]][s[1]].surf.fill((255, 0, 0))
        user[s[0]][s[1]].isFlagged = True
        p = p + 1
    return p


def game_over(s):
    if s == 1:
        return "YOU HAVE WON"
    elif s == 0:
        return "YOU LOST"


marker = box(0, 0, 0, (41, 75, 244))
marker_pos = (0, 0)
running = True
flags_added = 0
tiles_turned = 0
while running:
    for y in user:
        for x in y:
            screen.blit(x.surf, x.rect)
            screen.blit(x.text, x.rect)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP or event.key == K_DOWN or event.key == K_RIGHT or event.key == K_LEFT:
                update(marker, event)
            elif event.key == K_1:
                if hidden[marker_pos[0] + 1][marker_pos[1] + 1] == 10:
                    FINAL_TEXT = game_over(0)
                    running = False
                else:
                    update_values(marker_pos, (-100, -100))
            elif event.key == K_2:
                flags_added = toggle_Flag(marker_pos, flags_added)
            if tiles_turned == number * number - BOMBS and flags_added == BOMBS:
                FINAL_TEXT = game_over(1)
                running = False

        elif event.type == QUIT:
            running = False
    screen.blit(marker.surf, marker.rect)
    screen.blit(marker.text, marker.rect)
    marker_pos = (int(marker.rect.left / wid), int(marker.rect.top / hig))
    marker.text = user[marker_pos[0]][marker_pos[1]].text
    pygame.display.flip()
running = True
if FINAL_TEXT == "YOU HAVE WON":
    while running:
        t = pygame.font.SysFont("Comic Sans MS", 40)
        r = t.render(FINAL_TEXT, False, (255, 0, 0))
        s = pygame.Surface((600, 600))
        s.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        screen.blit(s, s.get_rect(center=(300, 300)))
        screen.blit(r, s.get_rect(center=(300, 300)))
        pygame.display.flip()
else:
    for i in range(number):
        for j in range(number):
            if count(hidden, i + 1, j + 1) == 10:
                user[i][j].update_text()
                screen.blit(user[i][j].text, user[i][j].rect)
                pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
    t = pygame.font.SysFont("Comic Sans MS", 60)
    r = t.render(FINAL_TEXT, False, (255, 0, 0))
    s = pygame.Surface((600, 600))
    s.fill((0, 0, 0))
    screen.blit(s, s.get_rect(center=(300, 300)))
    screen.blit(r, s.get_rect(center=(300, 300)))
    pygame.display.flip()
pygame.quit()
