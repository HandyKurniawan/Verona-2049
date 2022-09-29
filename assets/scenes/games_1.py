import pygame
import globals
import sys

from assets.scenes.games import Games
from assets.classes.measurementbase import MeasurementBase, BitBase

from assets.classes.utils import *
from assets.scenes.scene import Scene, FadeTransitionScene, TransitionScene
from assets.classes.inputstream import InputStream
from assets.classes.ui import ButtonUI
from assets.scenes.games_2 import Games2Scene
from assets.scenes.main_menu import GameOverScene

class Games_1(Games):
    def __init__(self, pygame):
        super().__init__()

        if globals.selectedBit == 0:
            globals.selectedBit = 5

        self.background = pygame.image.load("assets/images/games_1.jpg")

        # creating a group of Sprite, this is like an array of sprite (object of image)
        self.measurements = pygame.sprite.Group()
        self.retrieved_measurements = pygame.sprite.Group()
        self.bits = pygame.sprite.Group()
        self.retrieved_bits = pygame.sprite.Group()

        # the image in game 1 for getting the bit and base
        self.static_bit_0 = BitBase(globals.keyboard_bit_0, par_x=60, par_y=50)
        self.static_bit_1 = BitBase(globals.keyboard_bit_1, par_x=60, par_y=127)
        self.static_base_x = MeasurementBase(globals.keyboard_base_x, par_x=60, par_y=203)
        self.static_base_z = MeasurementBase(globals.keyboard_base_z, par_x=60, par_y=283)


        # user defined function
        self.measurement_event = pygame.USEREVENT + 1
        self.bit_event = pygame.USEREVENT + 2
        self.move_event = pygame.USEREVENT + 3

        self.total_bit = 0
        self.total_measurement = 0

        self.finish = False

        # timer for user defined function
        pygame.time.set_timer(self.measurement_event, 3000)  # 2000 milliseconds = 2 seconds
        pygame.time.set_timer(self.bit_event, 2500)  # 2000 milliseconds = 2 seconds
        pygame.time.set_timer(self.move_event, 5)  # 2000 milliseconds = 2 seconds

        globals.timer_minute = globals.starting_timer_minute
        globals.timer_seconds = globals.starting_timer_seconds

    def get_measurement(self, key: int):
        """
        get the measurement base and put into the table
        :param key: key press (X, Z)
        :return: boolean
        """
        if len(self.retrieved_measurements) >= globals.selectedBit:
            return False

        for l in self.measurements:
            if l.rect.x >= 20 and l.rect.x <= 90 and l.key == key:
                # creating new object for the static measurement
                self.retrieved_measurement = MeasurementBase(key)
                self.retrieved_measurement.rect = self.retrieved_measurement.image.get_rect(
                    topleft=(60 + (60 * len(self.retrieved_measurements)), 637))
                self.retrieved_measurements.add(self.retrieved_measurement)

                # delete the sprite object
                l.kill()
                return True

        return False

    def get_bit(self, key: int):
        """
            get the bit base and put into the table
            :param key: key press (0, 1)
            :return: boolean
            """

        if len(self.retrieved_bits) >= globals.selectedBit:
            return False

        for l in self.bits:
            if l.rect.x >= 20 and l.rect.x <= 90 and l.key == key:
                # creating new object for the static bit
                self.retrieved_bit = BitBase(key)
                self.retrieved_bit.rect = self.retrieved_bit.image.get_rect(topleft=(60 + (60 * len(self.retrieved_bits)), 467))
                self.retrieved_bits.add(self.retrieved_bit)

                # delete the sprite object
                l.kill()
                return True

        return False

    def is_measurement_miss(self):
        """
        to detect if the user miss the measurement base
        :return: boolean
        """
        for l in self.measurements:
            if l.rect.x <= 0:
                l.kill()
                return True

        return False

    def is_bit_miss(self):
        """
            to detect if the user miss the bit base
            :return: boolean
            """
        for l in self.bits:
            if l.rect.x <= 0:
                l.kill()
                return True

        return False

    def finish_game(self):
        if len(self.retrieved_measurements) >= globals.selectedBit and len(self.retrieved_bits) >= globals.selectedBit:
            for m in self.measurements:
                m.kill()

            for b in self.bits:
                b.kill()

            self.finish = True
            self.win = True


    def call_event(self, window: pygame.Surface):
        # to show the background
        window.blit(self.background, (0, 0))

        # getting all event happens on the game (mouse hover, keyboard press, user defined function)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # for quiting the game
                pygame.quit()
                sys.exit()
            elif event.type == self.measurement_event and len(
                    self.retrieved_measurements) < globals.selectedBit:  # to keep spawning the measurement base until reach x values
                # spawn new object
                self.measurements.add(MeasurementBase())
                self.total_measurement += 1

            elif event.type == self.bit_event and len(
                    self.retrieved_bits) < globals.selectedBit:  # to keep spawning the bit base until reach x values
                # spawn new object
                self.bits.add(BitBase())
                self.total_bit += 1

            elif event.type == self.move_event:
                for m in self.measurements:
                    m.move()

                for b in self.bits:
                    b.move()
            elif event.type == self.timer_event:
                self.process_timer()


            if event.type == pygame.KEYDOWN:
                if self.get_bit(event.key) or self.get_measurement(event.key):
                    self.point.add_value(1)

        #if self.is_measurement_miss():
        #    self.missing.add_value(1)

        #if self.is_bit_miss():
        #    self.missing.add_value(1)

        self.finish_game()

        # to keep the object refreshing on the screen
        self.measurements.draw(window)
        self.bits.draw(window)
        self.retrieved_measurements.draw(window)
        self.retrieved_bits.draw(window)
        self.static_bit_0.update(window)
        self.static_bit_1.update(window)
        self.static_base_x.update(window)
        self.static_base_z.update(window)

        # global drawing (score, timer, hearts
        self.draw(window)



class Games1Scene(Scene):
    def __init__(self):
        #self.esc = ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 20)
        self.d = ButtonUI(globals.keyboard_bit_0, '[d = bit-0]', 50, 10)
        self.f = ButtonUI(globals.keyboard_bit_1, '[f = bit-1]', 150, 10)
        self.j = ButtonUI(globals.keyboard_base_x, '[j = base-X]', 240, 10)
        self.k = ButtonUI(globals.keyboard_base_z, '[k = base-Z]', 360, 10)

        pygame.event.clear()
        self.g1 = Games_1(pygame)
        self.g1.reset_flags()
    def onEnter(self):
        pass
        #globals.soundManager.playMusicFade('solace')
    def update(self, sm, inputStream):

        #self.esc.update(inputStream)
        self.d.update(inputStream)
        self.f.update(inputStream)
        self.j.update(inputStream)
        self.k.update(inputStream)

    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN) and self.g1.finish and self.g1.win:
            self.romeo_bits = []
            for b in self.g1.retrieved_bits:
                self.romeo_bits.append(b.key)

            self.romeo_bases = []
            for b in self.g1.retrieved_measurements:
                self.romeo_bases.append(b.key)


            print(self.romeo_bits, self.romeo_bases)

            sm.push(FadeTransitionScene([self], [Games2Scene(self.romeo_bits, self.romeo_bases)]))
        elif inputStream.keyboard.isKeyPressed(pygame.K_RETURN) and self.g1.finish and self.g1.gameover:
            sm.push(FadeTransitionScene([self], [GameOverScene()]))

    def draw(self, sm, screen):
        self.g1.call_event(screen)
        self.d.draw(screen, par_colour = globals.WHITE)
        self.f.draw(screen, par_colour = globals.WHITE)
        self.j.draw(screen, par_colour = globals.WHITE)
        self.k.draw(screen, par_colour = globals.WHITE)


        if self.g1.finish and self.g1.win:
            drawText(screen, 'CLEAR! Press Enter to continue...', 50, 300, globals.BLACK, 255, 40)
            self.g1.pause = True
        elif self.g1.finish and self.g1.gameover:
            drawText(screen, 'Game over!', 50, 300, globals.BLACK, 255, 40)