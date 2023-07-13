import time
import math
import pygame
import random
import threading

from ._BFS import BFS
from .utils import Colors


class Entity:
    def __init__(
            self,
            sprite_path,
            start_node,
            name,
            show_data='bottom',
            fill_bar=20,
            speed=0.07
    ):
        self.health = fill_bar
        self.bladder = fill_bar
        self.hygiene = fill_bar
        self.energy = fill_bar
        self.hunger = fill_bar
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.speed = speed
        self.name = name
        self._path = []
        self._path_finder = BFS()
        self._current_node = start_node
        self._reach_destiny = True
        self._is_app_running = True
        self._is_alive = True
        self._started_time = time.time()
        self._death_time = None
        self._show_data = show_data
        self.position = list(self._path_finder.get_coord_node(start_node))

        th = threading.Thread(target=self._decrease_bars)
        th.daemon = True
        th.start()

    def on_app_shutdown(self):
        self._is_app_running = False

    def _decrease_bars(self):
        while self._is_app_running:
            self.hunger -= 1
            self.bladder -= 1
            self.hygiene -= 1
            self.energy -= 1
            self.health -= 1
            if self.health <= 0 or self.bladder <= 0 or self.hygiene <= 0 \
                    or self.energy <= 0 or self.hunger <= 0:
                self._is_alive = False
                self._death_time = time.time() - self._started_time
                print("dead at time: ", self._death_time)
                break
            time.sleep(1)

    def take_decision(self):
        if not self._is_alive:
            return

        if self._reach_destiny:
            current_decision = random.randint(0, 20)
            self._reach_destiny = False
            self._path = self._path_finder.shortest_path(self._current_node, current_decision)[::-1]
            print(self._path)
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
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y, self.hunger, 20])
        # ENERGY
        text_surf = font.render("ENERGY:", True, Colors.WHITE)
        display_surf.blit(text_surf, (420, y + adjust, 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y + adjust, 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y + adjust, self.energy, 20])
        # BLADDER
        text_surf = font.render("BLADDER:", True, Colors.WHITE)
        display_surf.blit(text_surf, (410, y + (adjust * 2), 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y + (adjust * 2), 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y + (adjust * 2), self.bladder, 20])
        # HYGIENE
        text_surf = font.render("HYGIENE:", True, Colors.WHITE)
        display_surf.blit(text_surf, (415, y + (adjust * 3), 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y + (adjust * 3), 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y + (adjust * 3), self.hygiene, 20])
        # HEALTH
        text_surf = font.render("HEALTH:", True, Colors.WHITE)
        display_surf.blit(text_surf, (420, y + (adjust * 4), 0, 0))
        pygame.draw.rect(display_surf, Colors.GRAY, [500, y + (adjust * 4), 100, 20])
        pygame.draw.rect(display_surf, Colors.GREEN, [500, y + (adjust * 4), self.health, 20])
        # PROFILE IMG
        profile = pygame.transform.scale(self.sprite, (100, 100))
        display_surf.blit(profile, (610, y_prof))

    def _move(self):
        coords = self._path_finder.get_coord_node(self._current_node)
        distance = self._euclidean_distance(self.position, coords)
        print(distance)
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

    @staticmethod
    def _euclidean_distance(pt1, pt2) -> float:
        return math.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
