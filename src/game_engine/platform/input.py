import sdl2
import sdl2.ext


class Input:
    """Input manager com estado de teclas, botões, delta de mouse e wheel."""

    def __init__(self):
        self.keys_down: set[int] = set()
        self.keys_just_pressed: set[int] = set()
        self.mouse_buttons: set[int] = set()
        self.mouse_dx: int = 0
        self.mouse_dy: int = 0
        self.wheel: int = 0

    def poll(self) -> bool:
        # Reset de estado por frame
        self.keys_just_pressed.clear()
        self.mouse_dx = 0
        self.mouse_dy = 0
        self.wheel = 0

        for ev in sdl2.ext.get_events():
            if ev.type == sdl2.SDL_QUIT:
                return False

            elif ev.type == sdl2.SDL_KEYDOWN:
                key = ev.key.keysym.sym
                if key not in self.keys_down:  # evita repeat
                    self.keys_just_pressed.add(key)
                self.keys_down.add(key)
                if key == sdl2.SDLK_ESCAPE:
                    return False

            elif ev.type == sdl2.SDL_KEYUP:
                self.keys_down.discard(ev.key.keysym.sym)

            elif ev.type == sdl2.SDL_MOUSEMOTION:
                self.mouse_dx += ev.motion.xrel
                self.mouse_dy += ev.motion.yrel

            elif ev.type == sdl2.SDL_MOUSEBUTTONDOWN:
                self.mouse_buttons.add(ev.button.button)

            elif ev.type == sdl2.SDL_MOUSEBUTTONUP:
                self.mouse_buttons.discard(ev.button.button)

            elif ev.type == sdl2.SDL_MOUSEWHEEL:
                self.wheel += ev.wheel.y

        return True

    def is_down(self, key: int) -> bool:
        return key in self.keys_down

    def just_pressed(self, key: int) -> bool:
        return key in self.keys_just_pressed

    def is_mouse_down(self, button: int) -> bool:
        return button in self.mouse_buttons