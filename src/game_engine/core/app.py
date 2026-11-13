import sdl2

from ..ecs.world import World
from ..platform.input import Input
from ..platform.window import Window
from ..render.camera import Camera
from ..render.renderer import Renderer
from .loop import GameLoop


class App:
    def __init__(self, title: str = "engine", width: int = 1280, height: int = 720):
        self.window = Window(title, width, height)
        self.input = Input()
        self.world = World()
        self.renderer = Renderer(self.window.ctx)
        self.camera = Camera()

        self.systems: list = []
        self.loop = GameLoop(
            update=self._update,
            render=self._render,
            poll=self.input.poll,
            ups=60,
        )

    def add_system(self, system) -> None:
        self.systems.append(system)

    def _update(self, dt: float) -> None:
        if self.input.just_pressed(sdl2.SDLK_TAB):
            self.camera.toggle_mode()
        for system in self.systems:
            system(self, dt)

    def _render(self, alpha: float) -> None:
        self.renderer.begin()
        aspect = self.window.width / self.window.height
        self.renderer.draw_world(self.world, self.camera, aspect)
        self.window.swap()

    def run(self) -> None:
        try:
            self.loop.run()
        finally:
            self.window.close()