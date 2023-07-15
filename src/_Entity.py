import time
import math
import pygame
import random
import threading

from src.ML import BaseAI
from src.PathFinder import BFS
from .utils import Colors


class Entity:
    def __init__(
            self,
            sprite_path: str,
            start_node: int,
            name: str,
            ml_model: BaseAI,
            choose_house: int,
            show_data: str = 'bottom',
            fill_bar: float = 25,
            speed: float = 0.07
    ):
        self._necessities = {
            'health': fill_bar,
            'bladder': fill_bar,
            'hygiene': fill_bar,
            'energy': fill_bar,
            'hunger': fill_bar,
        }
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.speed = speed
        self.name = name
        self._path = []
        self._path_finder = BFS(choose_house=choose_house)
        self._current_node = start_node
        self._reach_destiny = True
        self._is_app_running = False
        self._is_alive = True
        self._started_time = None
        self._death_time = None
        self._show_data = show_data
        self._ml_model = ml_model
        self._is_action_in_progress = False
        self._current_decision = None
        self._action_timeout = 4
        self.position = list(self._path_finder.get_coord_node(start_node))

    def on_app_shutdown(self):
        self._is_app_running = False

    def take_decision(self):
        if not self._is_app_running:
            self._is_app_running = True
            self._started_time = time.time()
            th = threading.Thread(target=self._decrease_bars)
            th.daemon = True
            th.start()
        if not self._is_alive or self._is_action_in_progress:
            return
        
        if self._reach_destiny:
            self._reach_destiny = False
            # the input is ['bladder', 'hygiene', 'energy', 'hunger', 'health']
            decision = self._ml_model.make_decision([
                self._necessities['bladder'], self._necessities['hygiene'],
                self._necessities['energy'], self._necessities['hunger'],
                self._necessities['health']
            ])[0]
            self._current_decision = decision
            print('the survivor {} decided {}'.format(self.name, decision))
            node = self._path_finder.get_node_by_necessity(decision)
            self._path = self._path_finder.shortest_path(self._current_node, node)[::-1]
            print('path:', self._path)
            self._current_node = self._path.pop()
        else:
            self._move()

    def draw(self, display_surf, font):
        if self._show_data == 'bottom':
            y = 320
            y_prof = 200
            adjust = -30
        else:
            y = y_prof = 10
            adjust = 30
        # SPRITE
        display_surf.blit(
            pygame.transform.scale(self.sprite, (18, 18)),
            self.position
        )
        # HUNGER
        text_surf = font.render("HUNGER:", True, Colors.WHITE)
        display_surf.blit(text_surf, (420, y, 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y, 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y, self._necessities['hunger'], 20])
        # ENERGY
        text_surf = font.render("ENERGY:", True, Colors.WHITE)
        display_surf.blit(text_surf, (420, y + adjust, 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y + adjust, 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y + adjust, self._necessities['energy'], 20])
        # BLADDER
        text_surf = font.render("BLADDER:", True, Colors.WHITE)
        display_surf.blit(text_surf, (410, y + (adjust * 2), 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y + (adjust * 2), 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y + (adjust * 2), self._necessities['bladder'], 20])
        # HYGIENE
        text_surf = font.render("HYGIENE:", True, Colors.WHITE)
        display_surf.blit(text_surf, (415, y + (adjust * 3), 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y + (adjust * 3), 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y + (adjust * 3), self._necessities['hygiene'], 20])
        # HEALTH
        text_surf = font.render("HEALTH:", True, Colors.WHITE)
        display_surf.blit(text_surf, (420, y + (adjust * 4), 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y + (adjust * 4), 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y + (adjust * 4), self._necessities['health'], 20])
        # PROFILE IMG
        profile = pygame.transform.scale(self.sprite, (100, 100))
        display_surf.blit(profile, (610, y_prof))

    def _move(self):
        coords = self._path_finder.get_coord_node(self._current_node)
        distance = self._euclidean_distance(self.position, coords)
        if distance >= 1:
            if self.position[0] < coords[0]:
                self.position[0] += self.speed
            elif self.position[0] > coords[0] + self.speed:
                self.position[0] -= self.speed
                pass

            if self.position[1] < coords[1]:
                self.position[1] += self.speed
            elif self.position[1] > coords[1] + self.speed:
                self.position[1] -= self.speed
        elif len(self._path) > 0:
            self._current_node = self._path.pop()
        else:
            self._reach_destiny = True
            th = threading.Thread(target=self._execute_action)
            th.daemon = True
            th.start()

    @staticmethod
    def _euclidean_distance(pt1, pt2) -> float:
        return math.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
    
    def _decrease_bars(self):
        while self._is_app_running:
            for key in self._necessities:
                if self._current_decision != key or not self._is_action_in_progress:
                    self._necessities[key] -= 0.5
                if self._current_decision == 'nothing' and self._current_node == 21 and key == 'energy':
                    self._necessities[key] -= 1
                if self._necessities[key] <= 0:
                    self._is_alive = False
                    self._death_time = time.time() - self._started_time
                    print("dead at time: ", self._death_time)
                    break
            if not self._is_alive:
                break
            time.sleep(2)
    
    def _execute_action(self):
        self._is_action_in_progress = True
        timer = 0
        while timer < self._action_timeout:
            if self._current_decision != 'nothing':
                self._necessities[self._current_decision] += 10
            time.sleep(1)
            timer += 1
        print('action of survivor {} ended'.format(self.name))
        self._is_action_in_progress = False
