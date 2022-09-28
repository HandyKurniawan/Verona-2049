import random
import numpy as np
from typing import List
from assets.scenes.games import Games
import pygame
from assets.classes.measurementbase import MeasurementBase, BitBase

from assets.classes.input_boxes import InputBox

import sys

FONT = pygame.font.Font("freesansbold.ttf", 32)

class Games_3(Games):

    # creating a group of Sprite, this is like an array of sprite (object of image)
    romeo_bit_display = pygame.sprite.Group()
    romeo_base_display = pygame.sprite.Group()
    juliet_base_display = pygame.sprite.Group()

    # user defined function
    event_hide_box = pygame.USEREVENT + 1

    romeo_bits = [pygame.K_0, pygame.K_1, pygame.K_0, pygame.K_0, pygame.K_1, pygame.K_1, pygame.K_0, pygame.K_1, pygame.K_1, pygame.K_0]
    romeo_bases = [pygame.K_z, pygame.K_x, pygame.K_z, pygame.K_x, pygame.K_x, pygame.K_z, pygame.K_z, pygame.K_x, pygame.K_z, pygame.K_x]
    juliet_bases = [pygame.K_x, pygame.K_x, pygame.K_z, pygame.K_z, pygame.K_x, pygame.K_x, pygame.K_z, pygame.K_x, pygame.K_x, pygame.K_z]

    hides = []
    hides.append(random.sample(range(0, 9), 2))
    hides.append(random.sample(range(0, 9), 2))
    hides.append(random.sample(range(0, 9), 2))

    def __init__(self, pygame):
        super().__init__()
        self.background = pygame.image.load("background3.png")

        # timer for user defined function
        pygame.time.set_timer(self.event_hide_box, 700)

        self.input_box = InputBox(300, 400, 140, 44)
        self.answer_key = ""
        self.input_key = ""

        self.get_answer_key()

        i = 0
        for type in self.romeo_bits:
            b = BitBase(type, _idx=i)
            b.rect = b.image.get_rect(topleft=(270 + 50 * i, 100))
            self.romeo_bit_display.add(b)

            i += 1

        i = 0
        for type in self.romeo_bases:
            b = MeasurementBase(type, _idx=i)
            b.rect = b.image.get_rect(topleft=(270 + 50 * i, 200))
            self.romeo_base_display.add(b)

            i += 1

        i = 0
        for type in self.juliet_bases:
            b = MeasurementBase(type, _idx=i)
            b.rect = b.image.get_rect(topleft=(270 + 50 * i, 300))
            self.juliet_base_display.add(b)

            i += 1

    def draw_table(self, window: pygame.Surface, list_hide, start_pos_x:int, start_pos_y: int):
        # Initialing Color
        color = (0, 0, 0)

        i = 0

        for b in self.romeo_bit_display:

            x = start_pos_x + (50 * i)
            y = start_pos_y

            if i in (list_hide):
                # Drawing Rectangle
                pygame.draw.rect(window, color, pygame.Rect(x, y, 52, 52))
            else:
                pygame.draw.rect(window, color, pygame.Rect(x, y, 52, 52), 2)


            i += 1

    def get_answer_key(self):
        for i in range(len(self.romeo_bits)):
            if (self.romeo_bases[i] == self.juliet_bases[i]):
                if (self.romeo_bits[i] == pygame.K_0):
                    self.answer_key += "0"
                else:
                    self.answer_key += "1"

        print("answer_key", self.answer_key)

    def check_answer_key(self):
        if self.answer_key == self.input_key:
            print("Correct")
        else:
            print("False")
            self.input_box.text = ""
            self.input_box.txt_surface = FONT.render("", True, self.input_box.color)

    def call_event(self, window: pygame.Surface):
        # to show the background
        window.blit(self.background, (0, 0))

        # getting all event happens on the game (mouse hover, keyboard press, user defined function)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # for quiting the game
                pygame.quit()
                sys.exit()
            elif event.type == self.event_hide_box:
                self.hides[0] = random.sample(range(0, 9), 2)
                self.hides[1] = random.sample(range(0, 9), 2)
                self.hides[2] = random.sample(range(0, 9), 2)


            self.input_key = self.input_box.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.check_answer_key()



        self.input_box.update()
        self.input_box.draw(window)

        # to keep the object refreshing on the screen
        self.romeo_bit_display.draw(window)
        self.romeo_base_display.draw(window)
        self.juliet_base_display.draw(window)

        self.draw_table(window, self.hides[0], 260, 90)
        self.draw_table(window, self.hides[1], 260, 190)
        self.draw_table(window, self.hides[2], 260, 290)

