import random
import globals
import numpy as np
import sys
import pygame

from assets.scenes.games import Games
from assets.classes.measurementbase import MeasurementBase, BitBase
from assets.classes.utils import *


class Games_2(Games):

    # creating a group of Sprite, this is like an array of sprite (object of image)
    bits = pygame.sprite.Group()
    measured_bits = pygame.sprite.Group()

    # user defined function
    event_bit_moving = pygame.USEREVENT + 1
    event_bit_change_direction = pygame.USEREVENT + 2
    event_bit_diminishing = pygame.USEREVENT + 3
    event_measuring= pygame.USEREVENT + 4

    def __init__(self, pygame, par_romeo_bits = [], par_romeo_bases = []):
        super().__init__()
        self.background = pygame.image.load("assets/images/games_2.jpg")

        self.bit_options = [globals.keyboard_bit_0, pygame.K_f]
        self.unmeasured_bits = []

        self.romeo_bits = par_romeo_bits
        self.romeo_bases = par_romeo_bases

        if globals.testing:
            for i in range(globals.maxBit):
                self.unmeasured_bits.append(random.choice(self.bit_options))
        else:
            for i in range(globals.selectedBit):
                self.unmeasured_bits.append(random.choice(self.bit_options))

        self.measured_count_seconds = np.ones(len(self.unmeasured_bits)) * 3

        # timer for user defined function
        pygame.time.set_timer(self.event_bit_moving, 30)
        pygame.time.set_timer(self.event_bit_change_direction, 5000)
        pygame.time.set_timer(self.event_bit_diminishing, 500)
        pygame.time.set_timer(self.event_measuring, 500)

        self.finish = False
        self.win = False

        i = 0
        for type in self.unmeasured_bits:
            b = BitBase(type, _idx= i)

            b.set_x_change(random.randint(-3, 3))
            b.set_y_change(random.randint(-3, 3))
            b.rect = b.image.get_rect(topleft=(random.randint(50, 920), random.randint(50, 450)))
            self.bits.add(b)

            mb = BitBase(type, _idx=i)
            mb.rect = mb.image.get_rect(topleft=(60 + 60 * i , 645))
            self.measured_bits.add(mb)

            i += 1

        for b in self.bits:
            b.fill(b.image, pygame.Color(250, 10, 40))

        for mb in self.measured_bits:
            mb.fill(mb.image, pygame.Color(250, 10, 40))
            mb.image.set_alpha(2000)

    def check_wall(self):
        for b in self.bits:
            if b.rect.x <= 55:
                b.set_x_change(random.randint(1, 4))
            elif b.rect.x >= 950:
                b.set_x_change(random.randint(-4, -1))

            if b.rect.y <= 55:
                b.set_y_change(random.randint(1, 4))
            elif b.rect.y >= 445:
                b.set_y_change(random.randint(-4, -1))

    def revealed_measured_bit(self, idx:int):
        for mb in self.measured_bits:
            if mb.idx == idx:
                mb.measured = True

    def is_win(self):
        is_win = True

        for mb in self.measured_bits:
            if mb.measured is False:
                is_win = False

        return is_win


    def call_event(self, window: pygame.Surface):
        # to show the background
        window.blit(self.background, (0, 0))

        # getting all event happens on the game (mouse hover, keyboard press, user defined function)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # for quiting the game
                pygame.quit()
                sys.exit()
            elif event.type == self.event_bit_moving:
                for b in self.bits:
                    b.move()
            elif event.type == self.event_bit_change_direction:
                for b in self.bits:
                    b.set_x_change(random.randint(-3, 3))
                    b.set_y_change(random.randint(-3, 3))
            elif event.type == self.event_bit_diminishing:
                for b in self.bits:
                    b.image.set_alpha( b.image.get_alpha() - 2)
            elif event.type == self.event_measuring:
                for b in self.bits:
                    self.measured_count_seconds[b.idx] = self.measured_count_seconds[b.idx] - 1
            elif event.type == self.timer_event:
                self.process_timer()


        # get mouse position
        mouse_pos = pygame.mouse.get_pos()
        for b in self.bits:
            # do something if mouse_pos collide with surface position
            if b.rect.collidepoint(mouse_pos):
                b.get_initialize_image(b.key)

                if self.measured_count_seconds[b.idx] <= 0:
                    b.measured = True

            elif b.measured:
                # if the bits measured, open the measured bit on the table below
                self.revealed_measured_bit(b.idx)
            else:
                b.fill(b.image, pygame.Color(250, 10, 40))
                self.measured_count_seconds[b.idx] = 3



        for mb in self.measured_bits:
            if mb.measured:
                mb.get_initialize_image(mb.key)
            else:
                mb.fill(mb.image, pygame.Color(250, 10, 40))

        if self.is_win() and self.gameover == False:
            self.finish = True
            self.win = True


        # to keep the object refreshing on the screen
        self.bits.draw(window)
        self.measured_bits.draw(window)
        self.check_wall()

        # global drawing (score, timer, hearts
        self.draw(window)