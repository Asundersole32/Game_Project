import sdl2
import sdl2.ext


class Input:
    """Input manager simples. Estado de teclas + quit."""

    def __init__(self):
        self.keys_down: set[int] = set()

    def poll(self) -> bool:
        """Processa eventos. Retorna False se deve encerrar."""
        for ev in sdl2.ext.get_events():
            if ev.type == sdl2.SDL_QUIT:
                return False
            elif ev.type == sdl2.SDL_KEYDOWN:
                key = ev.key.keysym.sym
                self.keys_down.add(key)
                if key == sdl2.SDLK_ESCAPE:
                    return False
            elif ev.type == sdl2.SDL_KEYUP:
                self.keys_down.discard(ev.key.keysym.sym)
        return True

    def is_down(self, key: int) -> bool:
        return key in self.keys_down