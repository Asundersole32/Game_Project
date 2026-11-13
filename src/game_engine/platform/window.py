import sdl2
import sdl2.ext
import moderngl


class Window:
    """Janela SDL2 com contexto OpenGL 3.3 core + wrapper moderngl."""

    def __init__(self, title: str = "engine", width: int = 1280, height: int = 720):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise RuntimeError(f"SDL_Init falhou: {sdl2.SDL_GetError()}")

        # Pede OpenGL 3.3 core
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 3)
        sdl2.SDL_GL_SetAttribute(
            sdl2.SDL_GL_CONTEXT_PROFILE_MASK,
            sdl2.SDL_GL_CONTEXT_PROFILE_CORE,
        )
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)

        self._win = sdl2.ext.Window(
            title,
            size=(width, height),
            flags=sdl2.SDL_WINDOW_OPENGL,
        )
        self._win.show()

        self._gl_ctx = sdl2.SDL_GL_CreateContext(self._win.window)
        if not self._gl_ctx:
            raise RuntimeError(f"SDL_GL_CreateContext falhou: {sdl2.SDL_GetError()}")

        sdl2.SDL_GL_SetSwapInterval(1)  # vsync

        # moderngl usa o contexto GL que a SDL acabou de criar
        self.ctx = moderngl.create_context(standalone=False)
        self.ctx.disable(moderngl.DEPTH_TEST)  # 2D-first; habilite em cenas 3D

        self.width = width
        self.height = height

    def swap(self) -> None:
        sdl2.SDL_GL_SwapWindow(self._win.window)

    def close(self) -> None:
        try:
            self.ctx.release()
        except Exception:
            pass
        sdl2.SDL_GL_DeleteContext(self._gl_ctx)
        self._win.close()
        sdl2.SDL_Quit()