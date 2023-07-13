import pygame
from ._Entity import Entity


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.font = None
        self.size = self.weight, self.height = 720, 345
        self.background = None
        self.entities = []

    def on_init(self):
        try:
            pygame.init()
            self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
            self._running = True
            self.set_sprites()
            self.font = pygame.font.SysFont(None, 25)
            return True
        except Exception as ex:
            raise ex

    def set_sprites(self):
        self.background = pygame.image.load('src/static/images/Sprite-0006.png').convert_alpha()
        self.entities.extend([
            Entity('src/static/images/boy.png', name='npc1', start_node=1, show_data='top'),
            Entity('src/static/images/boy2.png', name='npc2', start_node=11, show_data='bottom')
        ])

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self._display_surf.blit(self.background, (0, 0))
        for entity in self.entities:
            entity.take_decision()
            entity.draw(self._display_surf, self.font)

    def on_render(self):
        pygame.display.update()
        self._display_surf.fill((0, 0, 0))

    def on_cleanup(self):
        for entity in self.entities:
            entity.on_app_shutdown()
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
